import os
import pandas as pd
import traceback
import re
import json
from flask import Blueprint, request
from flask_security import login_required
from werkzeug.utils import secure_filename
from flask_api import ApiException, ApiResult
from trim_db.schema import *
from trim_db.services import *
from trim_frontend import api
from ..utils.file_io import csv_to_df
from ..utils.forms import assemble_json_form
from ..utils.logging import make_logger
from ..utils.spatial import *


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

            if fname.endswith('.csv'):
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
    df_aermod = pd.DataFrame(df[df['NET ID'] != 'POLGRID1'])
    df_aermod['NUM HRS'] = pd.to_numeric(df_aermod['NUM HRS'])
    df_aermod['DRY DEPO'] = pd.to_numeric(df_aermod['DRY DEPO'])
    df_aermod['WET DEPO'] = pd.to_numeric(df_aermod['WET DEPO'])

    # make a dictionary of shapely polygon objects based on TRIM layout
    dict_poly = {p.name: p.polygon() for p in scenario.parcels}
    dict_area = {p.name: p.area.magnitude for p in scenario.parcels}
    try:
        # add parcel location to each receptor in aermod file
        df_aermod['Parcel'] = df_aermod.apply(lambda z: determine_location(dict_poly=dict_poly, x=z.X, y=z.Y), axis=1)
        df_aermod = df_aermod[df_aermod['Parcel'] != ""]  # drop any receptors that are not mapped to layout
        df_aermod['ParcelArea'] = df_aermod.apply(lambda z: dict_area.get(z.Parcel), axis=1)
        df_aermod = df_aermod.reset_index(drop=True)
        ndays = df_aermod['NUM HRS'].loc[1] / 24  # compute number of days of cumulative deposition
    except Exception as e:
        print(f"Error finding parcels corresponding to sources: {e}")

    try:
        if spacing == r'Uniform':  # compute flat averages of all receptors in the parcel
            # Calculate average deposition for each person (g/m2)
            aggdep = df_aermod.groupby(['Parcel', 'ParcelArea'])[['DRY DEPO', 'WET DEPO']].mean().reset_index()
            # Calculate flux by correcting deposition (g/m2) by number of days in AERMOD modeling period
            aggdep['DRY DEPO'] = (aggdep['DRY DEPO'] / ndays) * aggdep['ParcelArea']  # g/m2/d * m2
            aggdep['WET DEPO'] = (aggdep['WET DEPO'] / ndays) * aggdep['ParcelArea']  # g/m2/d * m2

        elif spacing == r'Non-Uniform':  # computes weighted average of receptors in the parcel using distance of influence of each receptor as weight
            df_aermod['Spacing'] = df_aermod.apply(
                lambda z: determine_nearest_neighbor_distance(df_aermod=df_aermod, point_x=z.X, point_y=z.Y),
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
