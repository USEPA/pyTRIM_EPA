import csv
import io
import os
import pandas as pd
import traceback
import re
import json
import requests as pyRequest
from decimal import Decimal
from flask import Blueprint, request
from flask_security import login_required
from werkzeug.utils import secure_filename
from flask_api import ApiException, ApiResult
from trim_db.schema import *
from trim_db.schema.entities.environment import Parcel
from trim_db.services import *
from trim_db.services.parameters import get_or_create_custom_param
from trim_db.services.entities import ParcelService
from trim_frontend import api
from ..parcels.utils import delete_parcel_contents, get_canonical_land_use_type, get_canonical_parcel_type, get_ve_defaults_for_parcel_type, handle_parcel_update, initialize_parcel_contents
from ..utils.data_structures import calculate_list_depth
from ..utils.file_io import csv_to_df
from ..utils.forms import assemble_json_form
from ..utils.logging import make_logger
from ..utils.spatial import determine_location, determine_nearest_neighbor_distance, ensure_closed_polygon, is_utm_zone_valid, translate_coordinates, translate_position
from shapely.geometry import Polygon


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
            fname = secure_filename(f.filename)

            if fname.lower().endswith('.csv'):
                df = csv_to_df(f, dtype=str)
                # Get rid of carriage returns b/c they mess up output
                df = df.replace('\r', '', regex=True)

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
    scenario_id = [v for k, v in request.form.items() if k == 'scenario_id'][0]
    this_chem = [v for k, v in request.form.items() if k == 'chemical'][0]
    this_spec = [v for k, v in request.form.items() if k == 'species'][0]
    spacing = [v for k, v in request.form.items() if k == 'spacing'][0]
    coord_sys = [v for k, v in request.form.items() if k == 'proj'][0]
    utm_zone = [v for k, v in request.form.items() if k == 'utm_zone'][0]

    logger.info(f'Parsed AERMOD file: {list(files.items())[0][1].filename} for scenario id {scenario_id}, chemical {this_chem} with'
                f' coordinate system {coord_sys} {"and utm zone of " + utm_zone if utm_zone else ""}.')

    scenario = ScenarioService.get(id=scenario_id)
    chem = ChemicalService.get(name=this_chem)

    if not files:
        raise ApiException("No files were uploaded")

    fpn = [f.stream for n, f in files.items()][0]
    try:
        # with open(fpn.stream) as f:
        #     lines = f.readlines()
        fpn.seek(0)
        lines = fpn.read().decode("utf-8")
        lines = lines.split("\r\n")
    except Exception as e:
        print(e)

    row_ind = 0
    for line in lines:
        cols = re.split("  +", line)[1:]  # assumes header row starts with an asterisk that must be dropped
        cols = [x.replace('\n', '') for x in cols]  # assumes the line ends with a new line symbol
        # the ideal header
        if cols == ['X', 'Y', 'DRY DEPO', 'WET DEPO', 'ZELEV', 'ZHILL', 'ZFLAG', 'AVE', 'GRP', 'NUM HRS', 'NET ID']:
            break
        else:
            row_ind += 1

    skip_rows = row_ind+1+1  # one for zero index, one for blank line under header
    # df = pd.read_csv(fpn, delimiter=r"\s+", skiprows=skip_rows, header=None)
    arr = [re.split(r"\s+", ll.lstrip()) for ll in lines[skip_rows:]]
    df = pd.DataFrame(arr)
    df.columns = cols
    df = df[df['X'] != '']

    # drop collocated X,Y receptors while keeping the lowest elevation point
    df = df.sort_values(['X', 'Y', 'ZELEV']).drop_duplicates(['X', 'Y'], keep='first')
    # remove if NET ID = POLGRID. This does not always work. We will also need a user restriction to limit
    # receptors intended for TRIM modeling – i.e., Cartesian grid with no overlapping receptors

    # Convert the aermod X and Y to the default utm coordinates that pyTRIM uses. We need users input for the
    # coordinate system and UTM zone (if UTM coordiantes) for the given file.


    df_aermod = pd.DataFrame(df[df['NET ID'] != 'POLGRID1'])
    df_aermod['NUM HRS'] = pd.to_numeric(df_aermod['NUM HRS'])
    df_aermod['DRY DEPO'] = pd.to_numeric(df_aermod['DRY DEPO'])
    df_aermod['WET DEPO'] = pd.to_numeric(df_aermod['WET DEPO'])

    # make a dictionary of shapely polygon objects based on TRIM layout
    # dict_poly = {p.name: p.polygon() for p in scenario.parcels}
    dict_poly = {p.name: Polygon(p.vertices) for p in scenario.parcels}
    dict_area = {p.name: p.area.magnitude for p in scenario.parcels}

    try:
        df_aermod['newX'] = df_aermod.apply(
            lambda z: translate_position(float(z.X), float(z.Y), 'UTM', 'WGS84_LONGLAT', utm_zone=utm_zone)[0], axis=1)
        df_aermod['newY'] = df_aermod.apply(
            lambda z: translate_position(float(z.X), float(z.Y), 'UTM', 'WGS84_LONGLAT', utm_zone=utm_zone)[1], axis=1)
    except Exception as e:
        print(e)

    try:
        # add parcel location to each receptor in aermod file
        # df_aermod['Parcel'] = df_aermod.apply(lambda z: determine_location(dict_poly=dict_poly, x=z.X, y=z.Y), axis=1)
        df_aermod['Parcel'] = df_aermod.apply(lambda z: determine_location(dict_poly=dict_poly, x=z.newX, y=z.newY), axis=1)
        df_aermod = df_aermod[df_aermod['Parcel'] != ""]  # drop any receptors that are not mapped to layout
        df_aermod['ParcelArea'] = df_aermod.apply(lambda z: dict_area.get(z.Parcel), axis=1)
        df_aermod = df_aermod.reset_index(drop=True)
        ndays = df_aermod['NUM HRS'].loc[1] / 24  # compute number of days of cumulative deposition
    except Exception as e:
        print(f"Error finding parcels corresponding to sources: {e}")
    df_aermod['ParcelArea'] = pd.to_numeric(df_aermod['ParcelArea'])

    try:
        if spacing == r'Uniform':  # compute flat averages of all receptors in the parcel
            # Calculate average deposition for each person (g/m2)
            aggdep = df_aermod.groupby(['Parcel', 'ParcelArea'])[['DRY DEPO', 'WET DEPO']].mean().reset_index()
            # Calculate flux by correcting deposition (g/m2) by number of days in AERMOD modeling period
            aggdep['DRY DEPO'] = (aggdep['DRY DEPO'] / ndays) * aggdep['ParcelArea']  # g/m2/d * m2
            aggdep['WET DEPO'] = (aggdep['WET DEPO'] / ndays) * aggdep['ParcelArea']  # g/m2/d * m2

        elif spacing == r'Non-Uniform':  # computes weighted average of receptors in the parcel using distance of influence of each receptor as weight
            df_aermod['Spacing'] = df_aermod.apply(
                lambda z: determine_nearest_neighbor_distance(df_aermod=df_aermod, point_x=z.newX, point_y=z.newY),
                axis=1)  # compute distance to nearest receptor
            # Calculate receptor area (m2)
            dft = df_aermod  # temp file
            # area of influence of the receptor computed as a square with side equal to distance of nearest receptor
            dft['RepArea'] = (dft['Spacing']) ** 2
            # Calculate deposition (g) for each receptor area (m2)
            dft['DRY DEPO'] = dft['DRY DEPO'] * dft['RepArea']  # first step of weighting by square of area of influence
            dft['WET DEPO'] = dft['WET DEPO'] * dft['RepArea']
            # Sum deposition (g) by parcel
            aggdep = dft.groupby(['Parcel', 'ParcelArea'])[['DRY DEPO', 'WET DEPO', 'Spacing', 'RepArea']].sum().reset_index()
            # Calculate flux by correcting deposition (g) by parcel area (m2) & number of days in AERMOD modeling period
            # second step of weighting (divide by sum of weights in parcel)
            aggdep['DRY DEPO'] = (aggdep['DRY DEPO'] / aggdep['RepArea']) / ndays
            aggdep['WET DEPO'] = (aggdep['WET DEPO'] / aggdep['RepArea']) / ndays
    except Exception as e:
        print(f'Possible Grouping Error: {e}')

    aermod_result_json = json.loads(aggdep.to_json(orient='index'))
    res_json = None
    try:
        res_json = {aermod_result_json.get(str(k)).get('Parcel'): {'DrySource': v["DRY DEPO"],
                                                                   'WetSource': v["WET DEPO"]}
                    for k, v in aermod_result_json.items()}
    except Exception as e:
        print(e)

    source_comps = ["DryVaporSource", "WetVaporSource"] if this_spec == "Vapor" \
        else ["DryParticleSource", "WetParticleSource"]
    try:
        if res_json:
            for k, v in aermod_result_json.items():
                parcel = [p for p in scenario.parcels if p.name == v["Parcel"]][0]
                src_comp = [c for c in parcel.compartments if c.name in source_comps]
                for comp in src_comp:
                    src_par = [par for parn, par in comp.parameters.items() if parn == "surfaceDepositionRate"]
                    if len(src_par) > 0:
                        src_par = src_par[0]
                        src_par = get_or_create_custom_param(
                            src_par,
                            {"requirements": f"(self.id == {comp.id})", "scenario_id": scenario.id},
                            new_formula=True
                        )
                        prefix = "DRY" if comp.name.startswith("Dry") else "WET"
                        stype = f'{prefix} DEPO'
                        eq = src_par.formula.equation
                        # We have the chemical in the formula
                        if f'chemical.id == {str(chem.id)}' in eq:
                            formula_parts = eq.split(f"if chemical.id == {chem.id}")
                            formula_part = formula_parts[0]
                            if "else" in formula_part:
                                arr = formula_part.split("else")[:-1]
                                formula_part = "else".join(arr + [f' {v[stype]} '])
                            else:
                                formula_part = f'{v[stype]} '
                            formula_parts[0] = formula_part
                            new_formula = f"if chemical.id == {chem.id}".join(formula_parts)
                            print(new_formula)
                        # We do not have the chemical in the formula. We need to add it...
                        else:
                            eq_arr = eq.split("else")
                            eq_arr.insert(-2, f' {v[stype]} if chemical.id == {chem.id} ')
                            new_formula = "else".join(eq_arr)
                            print(new_formula)
                        FormulaService.get(src_par.formula.id).equation = new_formula
                FormulaService.commit()
    except Exception as e:
        print(e)

    return ApiResult({'aermod_result': res_json})


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
    coord_system = request.form.get("coord_system")
    raw_utm_zone = request.form.get("utm_zone")

    geojson = request.form.get("geojson")
    files = request.files

    if coord_system == "UTM":
        valid_zone, default_utm_zone = is_utm_zone_valid(raw_utm_zone)
        if not valid_zone:
            errors.append("Invalid default utm zone '{raw_utm_zone}' supplied.")

    if not files and not geojson:
        errors.append("No files were uploaded")

    if len(errors) == 0:
        # delete existing parcels...
        scenario = ScenarioService.get(id=scenario_id)
        for del_parcel in scenario.parcels:
            del_parcel_description = f"'{del_parcel.name}' ({del_parcel.id})"
            print(f"deleting parcel {del_parcel}...")
            try:
                delete_parcel_contents(del_parcel)
                ParcelService.delete(del_parcel.id)
            except Exception as e:
                errors.append(f"Exception deleting parcel {del_parcel_description}: {e}")

    if len(errors) > 0:
        raise ApiException("; ".join(errors))
    
    try:
        if geojson:
            lines = ""
            line_num = 0
            reader = json.loads(geojson)
        else: # assume csv
            fpn = [f.stream for n, f in files.items()][0]
            fpn.seek(0)
            lines = fpn.read().decode("utf-8")
            line_num = 2
            reader = csv.DictReader(io.StringIO(lines))
    except Exception:
        errors.append("Unable to open file")

    for row in reader:
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
            errors.append(f"Error processing CSV line {line_num}: {e}")
            print(f'{60*"*"}\nLINE {line_num}\n{full_stack()}')

        line_num += 1

    lines = lines.split("\r\n")

    if len(errors) > 0:
        raise ApiException("; ".join(errors))
    else:
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
    parsed_coords = json.loads(raw_coords)
    if calculate_list_depth(parsed_coords) == 2:
        parsed_coords = [parsed_coords]

    # now parsed coords is definitely nested3 lists
    fixed_coords = []
    for polygon_definition in parsed_coords:
        # print(f"CHECKING POLYGON: {polygon_definition}")
        polygon_definition = ensure_closed_polygon(polygon_definition)

        if coord_system == "WGS84 Longitude/Latitude":
            fixed_coords.append(polygon_definition)
        else:
            longlat_poly = translate_coordinates(polygon_definition, coord_system, "WGS84_LONGLAT", default_utm_zone=utm_zone)
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
    parcels = ParcelService.get_all(scenario_id=int(scenario_id))
    parcel_names = {p.name : p for p in parcels}

    files = request.files
    presigned_url = request.form.get("presigned_url")
    if not files and not presigned_url:
        return ApiException("No files were uploaded")
    
    try:
        if presigned_url: # getflow generated matrix
            r = pyRequest.get(presigned_url)
            csv_data = io.StringIO(r.content.decode('utf-8'))
            df = pd.read_csv(csv_data, delimiter=',')
            df.rename(columns={ df.columns[0]: 'parcels' }, inplace = True)

            # getflow does not include sink
            if 'sink' not in df.columns:
                df['sink'] = df.sum(axis=1, numeric_only=True)
                for idx, row in df.iterrows():
                    if row['sink'] > 1.0 or row['sink'] <= 0.0:
                        df.loc[idx, 'sink'] = 0
                    else:
                        df.loc[idx, 'sink'] = 1 - df.loc[idx, 'sink']

            reader = df.to_dict('records')
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
                elif header not in parcel_names.keys():
                    return ApiException(f"Parcel '{header}' does not exist in the scenario")
            for row in reader:
                if row.get("parcels") not in parcel_names.keys():
                    return ApiException(f"Parcel '{row.get('parcels')}' does not exist in the scenario")    
            if "sink" not in reader.fieldnames:
                return ApiException("Required header 'sink' is missing")
            
        # verify values are valid
        if files:
            reader = csv.DictReader(io.StringIO(lines))
        for row in reader:
            row_total = []
            for k, v in row.items():
                if k == "parcels": continue
                if Decimal(v) < 0: return ApiException("All values must be positive")
                row_total.append(Decimal(v))
            row_total = float(sum(row_total))
            if row_total != 1 and row_total != 0: 
                return ApiException("Sum of runoff fractions should be 1")

        # submit
        if files:
            reader = csv.DictReader(io.StringIO(lines))
        for row in reader:
            sender_pcl = parcel_names[row.get("parcels")]
            if sender_pcl.name in request.form["water_parcels"]:
                continue
            del row["parcels"]
            
            row_receivers_all = [f"ro_{k}" for k in row.keys()]
            row_vals_all = [(vi, f"{float(Decimal(v))}") for vi, v in enumerate(row.values())]
            row_receivers = [row_receivers_all[vi] for vi, v in row_vals_all if float(Decimal(v)) > 0]
            row_vals = [row_vals_all[vi][1] for vi, v in row_vals_all if float(Decimal(v)) > 0]
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
        return ApiException(e)
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
