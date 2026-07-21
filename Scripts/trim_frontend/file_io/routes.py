import csv
import io
import os
import pandas as pd
import traceback
import re
import json
import requests as pyRequest
from decimal import Decimal
from flask import Blueprint, request, abort
from flask_security import login_required, current_user
from werkzeug.utils import secure_filename
from flask_api import ApiException, ApiResult
from trim_core.coordinates import CoordinateMapper, ensure_closed_polygon
from trim_db.schema import *
from trim_db.services import *
from trim_db.services.parameters import get_or_create_custom_param
from trim_db.services.entities import ParcelService
from trim_frontend import api
from ..parcels.utils import delete_parcel_contents, get_canonical_land_use_type, get_canonical_parcel_type, handle_parcel_update
from ..utils.data_structures import calculate_list_depth
from ..utils.file_io import csv_to_df, associated_file_helper, convert_sfc_to_meteo, parse_sfc_file_as_dataframe
from ..utils.forms import assemble_json_form
from ..utils.logging import make_logger
from collections import OrderedDict

file_api = Blueprint('file_api', __name__)
api.use_api_errors(file_api)


@file_api.route('/api/file', methods=['POST'])
@login_required
def parse():
    logger = make_logger('file_uploader')

    files = request.files
    if not files:
        raise ApiException("No files were uploaded")

    data = {}
    for n, f in files.items():
        err = None
        fields = []
        entries = 0
        preview = None
        file_data = None
        truncated = False
        record_limit = 1000000
        try:
            df = None
            fname = secure_filename(f.filename)

            if fname.lower().endswith('.csv'):
                df = csv_to_df(f, dtype=str)
                # Get rid of carriage returns b/c they mess up output
                df = df.replace('\r', '', regex=True)
            elif fname.lower().endswith('.sfc'):
                sfc_df = parse_sfc_file_as_dataframe(f)
                df = convert_sfc_to_meteo(sfc_df)

            if df is not None:
                fields = list(df.columns.values)
                entries = len(df.index)
                print(f'NUMBER OF ENTRIES IS {entries} ')
                preview = df.head().where(
                    pd.notnull(df), None
                ).to_dict('records')
                if entries < record_limit:
                    file_data = df.where(
                        pd.notnull(df), None
                    ).to_dict('records')
                else:
                    file_data = df.head(record_limit).where(
                        pd.notnull(df), None
                    ).to_dict('records')

        except Exception as e:
            logger.error(traceback.format_exc())
            err = e

        if err:
            raise ApiException(
                f"Unable to upload file: {err}", 500
            ) from err

        data[n] = {
            'filename': fname,
            'fields': fields,
            'entry_count': entries,
            'preview': preview,
            'file_data': file_data
        }

    return ApiResult({'files': data})


@file_api.route('/api/AERMODfile', methods=['POST'])
@login_required
def parse_aermod():
    logger = make_logger('file_uploader')

    files = request.files
    if not files:
        raise ApiException("No files were uploaded")

    scenario_id = request.form['scenario_id']
    scenario = ScenarioService.get(id=scenario_id)
    if not scenario:
        return ApiException("Unknown Scenario")
    if not current_user.can('edit', scenario):
        abort(403)

    this_chem = request.form['chemical']
    this_spec = request.form['species']
    coord_sys = request.form['coord_sys']
    utm_zone = request.form.get('utm_zone') or None
    zflag_restriction = request.form.get('zflag_restriction') or None
    spacing = request.form['spacing']

    fileField = list(files.values())[0]

    if zflag_restriction is not None:
        try:
            zflag_restriction = float(zflag_restriction)
        except TypeError:
            zflag_restriction = None

    logger.info(
        f'Parsing AERMOD file "{fileField.filename}"'
        f' for scenario id {scenario_id}, chemical {this_chem}, with coordinate system {coord_sys}'
        f'{" and utm zone of " + utm_zone if utm_zone else ""},'
        f' {"and ZFLAG restriction of " + str(zflag_restriction) if (zflag_restriction is not None) else "and no ZFLAG restriction"}.'
    )

    chem = ChemicalService.get(name=this_chem)

    try:
        fpn = fileField.stream
        fpn.seek(0)
        aermod_results = ScenarioService(scenario).import_aermod(
            fpn,
            for_chemical=chem,
            metadata={
                'coordinate_system': coord_sys,
                'utm_zone': utm_zone,
                'zflag_restriction': zflag_restriction,
                'spacing': spacing,
                'chemical_species': this_spec,
            }
        )
    except Exception as e:
        print('Import error:', e)
        import traceback
        traceback.print_exc()
        raise

    return ApiResult({'aermod_results': aermod_results})


@file_api.route('/api/backgroundConc_file', methods=['POST'])
@login_required
def upload_background_conc():
    data = json.loads(request.form["file_data"])
    scenario_id = request.form["scenario_id"]
    chem_name = request.form["chemical_name"]
    scenario = ScenarioService.get(id=scenario_id)
    if not scenario:
        return ApiException("Unknown Scenario")
    if not current_user.can('edit', scenario):
        abort(403)

    chem = ChemicalService.get(name=chem_name)
    # First check if there are any existing CustomParameters
    custom_pars = [c.parameters.get("initialConcentration") for c in scenario.compartments if not isinstance(c.parameters.get("initialConcentration"), ParameterDefinition)]
    # We are going to reset all existing custom background conc values and start clean for file uploads. We do not want
    # to mistakenly keep existing values and have piece-meal addition of values from earlier uploads or manual entries.
    try:
        for cp in custom_pars:
            ParameterService.delete(cp, False)
    except Exception as e:
        print(f"problem deleting existing custom parameters: {e}")
    try:
        for ii, d in enumerate(data):
            print('d:', d)
            val = d["Background Concentration Value"]
            # Check parcel
            parcel = [p for p in scenario.parcels if p.name == d["Parcel Name"]]
            if len(parcel) == 0:
                return ApiException(f"Parcel {d['Parcel Name']} does not exist for scenario {scenario.name}"
                                    f"... Upload aborted...")
            else:
                parcel = parcel[0]
            # Check compartment
            comp_id = [c.id for c in parcel.compartments if c.name == d["Compartment Name"]]
            if len(comp_id) == 0:
                return ApiException(f"compartment {d['Compartment Name']} does not exist for parcel {parcel.name}"
                                    f"... Upload aborted...")
            else:
                comp_id = comp_id[0]

            comp = CompartmentService.get(id=comp_id)

            data[ii].setdefault("Volume Element Name", comp.volume_element.name)

            bc_par = [par for parn, par in comp.parameters.items() if parn == "initialConcentration"]
            if len(bc_par) > 0:
                bc_par = bc_par[0]
                bc_par = get_or_create_custom_param(
                    bc_par,
                    {"requirements": f"(self.id == {comp_id})", "scenario_id": scenario.id},
                    new_formula=True
                )

                # check the unit and see if we can convert to default if we have one that is different from default unit
                input_unit = d['Unit']
                default_unit = "g / m^3" if comp.media.id in [2, 5, 7, 56, 55, 8, 9] else "g / kg" if comp.media.id in [23, 24, 27, 28, 29, 31, 32, 33, 37, 39, 41, 43, 44, 45, 46, 47, 48, 49, 50, 51] else "g / L" if comp.media.id in [10, 4] else ""
                try:
                    input_val = float(val) * ureg(input_unit)
                    conv_val = input_val.to(default_unit)
                    print(f'input {input_val} -> default_unit {conv_val}')
                    val = conv_val.magnitude
                except Exception as e:
                    return ApiException(f'Problem converting the provided unit {input_unit} '
                                        f'to default unit of {default_unit}\n{e}')

                eq = bc_par.formula.equation
                print(f'old eq is {eq}')
                # We have the chemical in the formula
                if f'chemical.id == {str(chem.id)}' in eq:
                    formula_parts = eq.split(f"if chemical.id == {chem.id}")
                    formula_part = formula_parts[0]
                    if "else" in formula_part:
                        arr = formula_part.split("else")[:-1]
                        formula_part = "else".join(arr + [f' {val} '])
                    else:
                        formula_part = f'{val} '
                    formula_parts[0] = formula_part
                    new_formula = f"if chemical.id == {chem.id}".join(formula_parts)
                    print(new_formula)
                # We do not have the chemical in the formula. We need to add it...
                else:
                    eq_arr = eq.split("else")
                    eq_arr.insert(-2, f' {val} if chemical.id == {chem.id} ')
                    new_formula = "else".join(eq_arr)
                    print(new_formula)
                FormulaService.get(bc_par.formula.id).equation = new_formula
                FormulaService.commit()
    except Exception as e:
        print('background conc load error:', e)
    return ApiResult({'background_conc_file_data': data})


@file_api.route('/api/parcel_file', methods=['POST'])
@login_required
def parse_parcel_upload():
    errors = []
    default_utm_zone = None
    return_data = {
        "parcels": []
    }

    def full_stack():
        import traceback, sys
        exc = sys.exc_info()[0]
        stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
        if exc is not None:  # i.e. an exception is present
            del stack[-1]  # remove call of full_stack, the printed exception
            # will contain the caught exception caller instead
        trc = 'Traceback (most recent call last):\n'
        stackstr = trc + ''.join(traceback.format_list(stack))
        if exc is not None:
            stackstr += '  ' + traceback.format_exc().lstrip(trc)
        return stackstr

    scenario_id = request.form["scenario_id"]
    scenario = ScenarioService.get(id=scenario_id)
    if not scenario:
        return ApiException("Unknown Scenario")
    if not current_user.can('edit', scenario):
        abort(403)

    coord_system = request.form.get("coord_system")
    raw_utm_zone = request.form.get("utm_zone")

    geojson = request.form.get("geojson")
    files = request.files

    if coord_system == "UTM":
        try:
            zone_number, zone_letter = CoordinateMapper.decompose_utm_zone(raw_utm_zone)
            default_utm_zone = f'{zone_number}{zone_letter}'
        except Exception:
            errors.append(f"Invalid default utm zone '{raw_utm_zone}' supplied.")

    if not files and not geojson:
        errors.append("No files were uploaded")

    if len(errors) == 0:
        # delete existing parcels...
        for del_parcel in scenario.parcels:
            del_parcel_description = f"'{del_parcel.name}' ({del_parcel.id})"
            print(f"deleting parcel {del_parcel}...")
            try:
                delete_parcel_contents(del_parcel)
                ParcelService.delete(del_parcel.id)
            except Exception as e:
                errors.append(f"Exception deleting parcel {del_parcel_description}: {e}")

    if len(errors) > 0:
        if len(scenario.parcels) > 0:
            raise ApiException("; ".join(errors))
        else:
            # Just move along ... it worked, at any rate
            print('Encountered errors during parcel deletion, but all parcels were deleted:')
            print('\t' + '\n\t'.join(errors))

    try:
        if geojson:
            lines = ""
            line_num = 0
            reader = json.loads(geojson)
            rows_to_process = reader  # GeoJSON is already in correct format
        else:  # assume csv
            fpn = [f.stream for n, f in files.items()][0]
            fpn.seek(0)
            lines = fpn.read().decode("utf-8")
            line_num = 2
            reader = csv.DictReader(io.StringIO(lines))

            # process csv with format detection and normalization
            csv_rows = list(reader)
            rows_to_process = process_csv_parcels(csv_rows)

    except Exception:
        errors.append("Unable to open file")

    for row in rows_to_process:
        try:
            if geojson:
                row_data = get_parcel_row_geojson(row)
            else:
                row_data = get_parcel_row_csv(row, coord_system, default_utm_zone)

            parcel_name = row_data["parcel_name"]
            parcel_type = row_data["parcel_type"]
            parcel_description = row_data["parcel_description"]
            land_use = row_data["land_use"]
            farm_food_chain = row_data["hasFarmFoodChain"]
            wetland = row_data["hasWetland"]
            fish_food_web = row_data["hasFishFoodWeb"]
            coordinates = row_data["coordinates"]

            # TODO - reload page after upload (done; but we could do better...)
            p = ParcelService.create(name=parcel_name, description=parcel_description, scenario_id=scenario_id, vertices=coordinates)
            handle_parcel_update(p, {
                "field": "parcelType",
                "parcelType": parcel_type
            })

            # TODO - verify this logic is sound -- or is it being enforced elsewhere?
            # basically does the upload handler need to worry about e.g. someone saying
            # "Yes" to farm food chain while also saying "air only"?
            if "Land" in parcel_type:
                if land_use is not None:
                    handle_parcel_update(p, {
                        "field": "landUse",
                        "landUse": land_use
                    })

                if land_use == "Tilled Soil" or "Agriculture" in land_use:
                    handle_parcel_update(p, {
                        "field": "hasFarmFoodChain",
                        "hasFarmFoodChain": farm_food_chain
                    })

                # always allow wetland for land editing?
                handle_parcel_update(p, {
                    "field": "hasWetland",
                    "hasWetland": wetland
                })

            if "Water" in parcel_type:
                handle_parcel_update(p, {
                    "field": "hasFishFoodWeb",
                    "hasFishFoodWeb": fish_food_web
                })

            return_data["parcels"].append(p.as_serializable())

            # TODO - verify that "Air" in the csv sample is meaningless?
            # TODO - "Agriculture (General)" doesn't work either in UI or via CSV upload
            # TODO - "Tilled Soil, Untilled Soil, Impervious" are all bused in create_base_land_compartments

            """
            # WHAT'S EDITABLE?
            LAND USE        FARMFOODCHAIN   FISHFOODWEB     WETLAND
            --------------------------------------------------------
            Tilled Soil         yes             -           yes
            Untilled Soil       ??????????????????
            Agri Gen
            Grasses/Herb        -               -           yes
            Decid For           -               -           yes
            Conif For           -               -           yes
            """

            print(f"\tDONE FOR LINE {line_num}")
        except Exception as e:
            errors.append(f"Error processing line {line_num}: {e}")
            print(f'{60*"*"}\nLINE {line_num}\n{full_stack()}')

        line_num += 1

    lines = lines.split("\r\n")

    if len(errors) > 0:
        raise ApiException("; ".join(errors))
    else:
        return ApiResult(return_data)


@file_api.route('/api/misc_scen_file', methods=['GET', 'POST', 'DELETE'])
@login_required
def manage_misc_scenario_file():

    # this is a generic endpoint for handling storage (upload/deletion/retrieval) on S3 of miscellaneous files
    # associated with a scenario. Pass in a 'misc_file_type'==x and you'll get:
    # a file /{scenarioId}/x/data* and /{scenarioId}/x/_metadata.json in the appropriate
    # S3 bucket. the json file is metadata; it will contain any other fields you passed in at upload time, as well as
    # some standard fields like the original file name, etc.

    # this function handles API-oriented I/O; the actual storage/retrieval from 
    # S3 is farmed out to associated_file_helper, so that the same logic can be
    # used in a non-API context.

    # initially modeled after parse_parcel_upload

    errors = []
    return_data = {}

    scenario_id = None
    if request.method == "POST":
        scenario_id = request.form["scenario_id"]
        misc_file_type = request.form["misc_file_type"]
        # upload file to S3...
    else:
        scenario_id = request.args.get("scenario_id")
        misc_file_type = request.args.get("misc_file_type")
        # check S3 for existing file...or delete it...

    if scenario_id is None:
        errors.append("No scenario id supplied")

    s = ScenarioService.get(scenario_id)
    if not s:
        return ApiException("Unknown Scenario")
    if not current_user.can('edit', s):
        abort(403)

    if misc_file_type is None:
        errors.append("No filetype supplied")

    if len(errors) == 0:
        if request.method == "GET":
            try:
                helper_rv = associated_file_helper(scenario_id, misc_file_type, "CHECK")
            except Exception as e:
                print(f"GET ERROR: {e}")
                errors.append(f"Error fetching file: {e}")
        elif request.method == "POST":
            ignore = ["scenario_id", "misc_file_type", "csrf_token"]
            submitted_metadata = { x[0]: x[1] for x in request.form.items() if x[0] not in ignore }

            files = request.files

            if not files:
                errors.append("No file was uploaded")

            if len(errors) == 0:
                try:
                    file_obj = None
                    for _, loop_file_obj in files.items():
                        file_obj = loop_file_obj
                        original_name = secure_filename(loop_file_obj.filename)
                        submitted_metadata["original_file_name"] = original_name
                        break

                    helper_rv = associated_file_helper(scenario_id, misc_file_type, "UPLOAD", file_obj=file_obj, file_metadata=submitted_metadata)
                except Exception as e:
                    print(f"POST ERROR: {e}")

                    try:
                        detailed_error_message = json.loads(str(e))
                        errors.append(detailed_error_message.get("user_facing_error_msg"))
                    except Exception as e:
                        errors.append("generic_error")
        elif request.method == "DELETE":
            try:
                helper_rv = associated_file_helper(scenario_id, misc_file_type, "DELETE")
                return_data["message"] = "file(s) deleted"
            except Exception as e:
                print(f"DELETE ERROR: {e}")
                errors.append(f"Error deleting file: {e}")

    if len(errors) > 0:
        raise ApiException("; ".join(errors))
    else:
        return_data |= helper_rv
        return ApiResult(return_data)


def get_parcel_row_csv(row, coord_system, utm_zone):
    has_farm_food_chain = row.get("FarmFoodChain", "").upper() == "YES"
    has_wetland = row.get("Wetland", "").upper() == "YES"
    has_fish_food_web = row.get("FishFoodWeb", "").upper() == "YES"

    # we'll accept either a 3 level list...
    # OUTERMOST LIST 1 == multiple polygons
    # MIDDLE LIST 2 == group of coords; i.e. the full vertices of the polygon
    # INNERMOST LIST 3 == x/y coord; a single point of a parcel's polygon
    #
    # ...or we'll allow the user to optionally omit the outermost list; we'll add it for them after we check depth
    raw_coords = row.get("coordinates")
    # Add null/empty check
    if not raw_coords:
        raise ValueError(f"Missing coordinates for parcel: {row.get('ParcelName', 'Unknown')}")

    try:
        parsed_coords = json.loads(raw_coords)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in coordinates for parcel {row.get('ParcelName', 'Unknown')}: {e}")

    if calculate_list_depth(parsed_coords) == 2:
        parsed_coords = [parsed_coords]

    # now parsed coords is definitely nested3 lists
    fixed_coords = []
    for polygon_definition in parsed_coords:
        polygon_definition = ensure_closed_polygon(polygon_definition)

        if coord_system == "WGS84 Longitude/Latitude":
            fixed_coords.append(polygon_definition)
        elif 'UTM' in coord_system.upper():
            mapper = CoordinateMapper('UTM', 'WGS84_LONGLAT', utm_zone=utm_zone)
            longlat_poly = [mapper.translate(*pt) for pt in polygon_definition]
            fixed_coords.append(longlat_poly)

    # now fixed_coords is definitely nested3 lists of long/lat pairs

    return {
        "parcel_name": row.get("ParcelName"),
        "parcel_type": get_canonical_parcel_type(row.get("ParcelType")),
        "parcel_description": row.get("Description", ""),
        "land_use": get_canonical_land_use_type(row.get("LandUse", "")),
        "hasFarmFoodChain": "Yes" if has_farm_food_chain else "No",
        "hasWetland": "Yes" if has_wetland else "No",
        "hasFishFoodWeb": "Yes" if has_fish_food_web else "No",
        "coordinates": fixed_coords[0],
    }


def detect_csv_format(csv_rows):
    if not csv_rows:
        raise ValueError("CSV file is empty")
    
    first_row = csv_rows[0]
    
    #checking for Format 1 - multiple rows with X/Y coordinates
    if 'Xcoordinate' in first_row and 'Ycoordinate' in first_row:
        return 'multi_row'
    
    # check for Format 2 - Single row with coordinates JSON
    if 'coordinates' in first_row:
        return 'single_row'
    
    raise ValueError(
        "Unknown CSV format. Expected either:\n"
        "- Format 1: ParcelName, Xcoordinate, Ycoordinate (multiple rows per parcel)\n"
        "- Format 2: ParcelName, coordinates (JSON array, single row per parcel)"
    )


def aggregate_parcel_vertices_from_csv(csv_rows):
    """
    smaple input:
        ParcelName,Air,LandUse,FarmFoodChain,FishFoodWeb,Wetland,Xcoordinate,Ycoordinate
        Upload01,Land & Air,deciduous forest,No,No,No,-78.919926,35.987667
        Upload01,Land & Air,deciduous forest,No,No,No,-78.919279,35.976736
        
    output:
        {
            'ParcelName': 'Upload01',
            'ParcelType': 'Land & Air',
            'LandUse': 'deciduous forest',
            ...
            'coordinates': '[[-78.919926,35.987667],[-78.919279,35.976736],...]'
        }
    """
    parcels = OrderedDict()
    
    for row in csv_rows:
        parcel_name = row.get('ParcelName')
        
        if not parcel_name or parcel_name.strip() == '':
            continue
        
        parcelType = None
        if "Air" in row:
            parcelType = row.get("Air")
        if "Water" in row:
            parcelType = row.get("Water")
        if "Land" in row:
            parcelType = row.get("Land")
        
        if parcel_name not in parcels:
            parcels[parcel_name] = {
                'ParcelName': parcel_name,
                'ParcelType': parcelType,
                'LandUse': row.get('LandUse', ''),
                'FarmFoodChain': row.get('FarmFoodChain', ''),
                'FishFoodWeb': row.get('FishFoodWeb', ''),
                'Wetland': row.get('Wetland', ''),
                'Description': row.get('Description', ''),
                'vertices': []
            }
        
        x_coord = row.get('Xcoordinate')
        y_coord = row.get('Ycoordinate')
        
        
        if x_coord is not None and y_coord is not None and x_coord != '' and y_coord != '':
            try:
                # [x, y] pair
                parcels[parcel_name]['vertices'].append([float(x_coord), float(y_coord)])
            except (ValueError, TypeError) as e:
                print(f"Warning: Invalid coordinates for {parcel_name}: x={x_coord}, y={y_coord} - {e}")
        
        print(f'checking if the info for parcel is saved correctly : {parcels}')
    result = []
    for parcel_name, parcel_data in parcels.items():
        if len(parcel_data['vertices']) < 3:
            print(f"Warning: Parcel '{parcel_name}' has fewer than 3 vertices ({len(parcel_data['vertices'])}). Skipping.")
            continue
        
        parcel_data['coordinates'] = json.dumps(parcel_data['vertices'])
        del parcel_data['vertices']
        
        result.append(parcel_data)
    print(f'\n\n\n checking result  : {result}\n\n')
    return result


def normalize_single_row_parcels(csv_rows):
    result = []
    
    for row in csv_rows:
        parcel_name = row.get('ParcelName')
        
        if not parcel_name or parcel_name.strip() == '':
            continue
        
        #get coordinates - might already be a string or need conversion
        coordinates = row.get('coordinates', '')
        
        #if not lucky coordinates is empty or None, skip
        if not coordinates or coordinates.strip() == '':
            print(f"Warning: Parcel '{parcel_name}' has no coordinates. Skipping.")
            continue
        
        # Validate that coordinates is valid JSON
        try:
            parsed = json.loads(coordinates)
            coordinates = json.dumps(parsed)
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Warning: Invalid JSON coordinates for {parcel_name}: {e}. Skipping.")
            continue
        
        normalized = {
            'ParcelName': parcel_name,
            'ParcelType': row.get("ParcelType"),
            'LandUse': row.get('LandUse', ''),
            'FarmFoodChain': row.get('FarmFoodChain', ''),
            'FishFoodWeb': row.get('FishFoodWeb', ''),
            'Wetland': row.get('Wetland', ''),
            'Description': row.get('Description', ''),
            'coordinates': coordinates
        }
        
        result.append(normalized)
    
    return result


def process_csv_parcels(csv_rows):
    if not csv_rows:
        raise ValueError("No data in CSV file")
    
    #check format
    csv_format = detect_csv_format(csv_rows)
    print(f"Detected CSV format: {csv_format}")
    
    if csv_format == 'multi_row':
        return aggregate_parcel_vertices_from_csv(csv_rows)
    elif csv_format == 'single_row':
        return normalize_single_row_parcels(csv_rows)
    else:
        raise ValueError(f"Unsupported CSV format: {csv_format}")




def get_parcel_row_geojson(row):
    props = row["properties"]
    return {
        "parcel_name": props.get("name").strip(),
        "parcel_type": props.get("parceltype").strip(),
        "parcel_description": props.get("desc", " "),
        "land_use": props["landuse"].get("lu").strip(),
        "hasFarmFoodChain": props.get("farmfoodchain").strip(),
        "hasWetland": props.get("wetland").strip(),
        "hasFishFoodWeb": props.get("fishfoodweb").strip(),
        "coordinates": row["geometry"].get("coordinates")[0],
    }

@file_api.route('/api/runoff_matrix_file', methods=['POST'])
@login_required
def parse_runoff_matrix_upload():
    scenario_id = request.form["scenario_id"]
    s = ScenarioService.get(scenario_id)
    if not s:
        return ApiException("Unknown Scenario")
    if not current_user.can('edit', s):
        abort(403)

    parcels = ParcelService.get_all(scenario_id=int(scenario_id))
    parcel_names = {p.name.lower() : p for p in parcels}

    files = request.files
    presigned_url = request.form.get("presigned_url")
    if not files and not presigned_url:
        return ApiException("No files were uploaded")

    try:
        if presigned_url: # getflow generated matrix
            # START - validate the presigned_url
            # make sure it hasn't been monkeyed with -- URL matches expected pattern,
            # we have exactly the params we expect, etc. If we don't, we'll throw an Exception
            validate_url = True

            if validate_url:
                regex = r"^https:\/\/[-a-z0-9]*\.s3\.amazonaws\.com\/[-0-9a-f]*\/[_a-z]*\.csv.*\?(.*)"
                matches = re.finditer(regex, presigned_url)

                presigned_params = {}
                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        chunks = match.group(1).split("&")
                        i = 0
                        for c in chunks:
                            print(f"\t[{i}] [{c}]")
                            equal_pos = c.find("=")
                            param_name = c[:equal_pos]
                            param_val = c[equal_pos+1:]
                            presigned_params[param_name] = param_val
                            i += 1

                expected = { "AWSAccessKeyId", "Signature", "x-amz-security-token", "Expires" }
                for param_name in presigned_params:
                    if param_name not in expected:
                        return ApiException(f"Encountered unexpected presigned url param '{param_name}'")
                    else:
                        expected.remove(param_name)

                if len(expected) > 0:
                    return ApiException(f"Missing expected presigned url param(s): '{', '.join([x for x in expected])}'")

                # if we make it this far -- presigned_url looks ok. We can proceed.
            # END - validate the presigned_url

            r = pyRequest.get(presigned_url)
            csv_data = io.StringIO(r.content.decode('utf-8'))
            df = pd.read_csv(csv_data, delimiter=',')

            make_adjustments=True
            if make_adjustments:
                df.rename(columns={ df.columns[0]: 'parcels' }, inplace = True)

            """
            # old v10 cleanup of raw values->percents; not needed in v13+
            # clean up extra rows/columns
            total_out_mask = df[df.columns[0]] != 'TOTAL_OUT'
            sink_mask = df[df.columns[0]] != 'SINK'
            df = df[total_out_mask & sink_mask]
            df.drop('TOTAL_IN', axis='columns', inplace=True)
            df.columns = df.columns.str.lower()

            # need to make adjustments for value to equal 1 exactly
            precision = 4
            pcls_col = df.pop('parcels').reset_index(drop=True)
            df = np.trunc(10000 * df) / 10000
            df = pd.concat([pcls_col, df], axis='columns')
            """

            if make_adjustments:
                # getflow v13 is giving percentages like 85.23% == "85.23"; we want ".8523"
                df[df.select_dtypes(include=['number']).columns] /= 100

                # rename SINK->sink and move it to right after parcels (position==1)
                df.insert(1, 'sink', df.pop('SINK'))

            reader = df.to_dict('records')
            row_counter = 1
            precision = 4
            for row in reader:
                row_total = []
                for k, v in row.items():
                    if k == "parcels": continue
                    rounded_val = round(v, precision)
                    # print(f"\trow [{row_counter}] '{k}': {v} -> {rounded_val}")
                    # row_total.append(Decimal(v))
                    row_total.append(rounded_val)
                # row_total = float(sum(row_total))
                row_total = round(sum(row_total), precision)
                # print(f"\t{row_total=}")
                if row_total == 0: continue

                elif row_total != 1:
                    row_diff = round(Decimal(1.0000) - Decimal(row_total), precision)
                    for k, v in row.items():
                        if k == "parcels" or k == 'sink' or v == 0: continue
                        before = v
                        after = round(row_diff + Decimal(v), precision)
                        df.at[row_counter-1, k] = float(after)
                        row[k] = after
                        break

                # print(f"ROW {row_counter} TOTAL {row_total}")
                row_counter += 1
        else:
            fpn = [f.stream for n, f in files.items()][0]
            fpn.seek(0)
            lines = fpn.read().decode("utf-8")
            reader = csv.DictReader(io.StringIO(lines))

            # TODO make sure all parcels are accounted for
            # verify headers are valid parcels + sink exists
            for header in reader.fieldnames:
                if header == 'sink' or header == 'parcels':
                    continue
                elif header.lower() not in parcel_names.keys():
                    return ApiException(f"Parcel '{header}' does not exist in the scenario")
            for row in reader:
                if row.get("parcels").lower() not in parcel_names.keys():
                    return ApiException(f"Parcel '{row.get('parcels')}' does not exist in the scenario")    
            if "sink" not in reader.fieldnames:
                return ApiException("Required header 'sink' is missing")
            
            # verify values are valid
            reader = csv.DictReader(io.StringIO(lines))
            for row in reader:
                row_total = []
                for k, v in row.items():
                    if k == "parcels": continue
                    if Decimal(v) < 0: return ApiException("All values must be positive")
                    row_total.append(Decimal(v))
                row_total = float(sum(row_total))
                if row_total != 1 and row_total != 0:
                    print(row)
                    print(row_total)
                    return ApiException("Sum of runoff fractions should be 1")

        # submit
        if files:
            reader = csv.DictReader(io.StringIO(lines))
        for row in reader:
            sender_pcl = parcel_names[row.get("parcels").lower()]
            if sender_pcl.name in request.form["skip_parcels"]:
                continue
            del row["parcels"]
            
            row_receivers_all = [f"ro_{k}" for k in row.keys()]
            row_vals_all = [(vi, f"{float(Decimal(v))}") for vi, v in enumerate(row.values())]
            row_receivers = [row_receivers_all[vi] for vi, v in row_vals_all]
            row_vals = [row_vals_all[vi][1] for vi, v in row_vals_all]
            if len(row_vals) > 0:
                payload = {
                    "id": sender_pcl.id,
                    "field": "runoff_matrix_value",
                    "sender": f"ro_{sender_pcl.name}",
                    "receiver": ",".join(row_receivers),
                    "ro_value": ",".join(row_vals)
                }
                handle_parcel_update(sender_pcl, payload)
                
    except Exception as e:
        print(traceback.format_exc())
        return ApiException(traceback.format_exc())
    return ApiResult({'matrix_result': "success"})

root = os.path.dirname(os.path.abspath(__file__))
static = os.path.abspath(os.path.join(root, '../static'))


@file_api.route('/api/form', methods=['GET'])
@login_required
def load_json_form():
    forms = request.args.getlist('form')

    json_forms = {}

    for form in forms:
        json_forms[form] = None
        name = form
        if not name.endswith('.json'):
            name += '.json'
        json_forms[form] = assemble_json_form(name)

    return ApiResult(json_forms)
