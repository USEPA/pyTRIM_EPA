
import json
import os
import requests
from decimal import Decimal
from matplotlib.path import Path
from trim_db.schema import ureg
from ..utils.file_io import associated_file_helper, get_local_misc_file_loc
from ..utils.logging import make_logger


def compile_mirc_data(scen, latest_model_run, logger=None):
    if not logger:
        logger = make_logger('compile_mirc_data')
    logger.info(f"Compiling required MIRC data for scenario {scen.name}...")

    if latest_model_run and not latest_model_run.is_run_error:
        mass = json.loads(latest_model_run.result_nt)
        mass = json.loads("{"+mass+"}")
        conc = json.loads(latest_model_run.result_conc)
        conc = json.loads("{"+conc+"}")

        logger.info(f"Model run found, using run with id [{latest_model_run.id}]...")

        chems = {c.name: c for c in scen.chemicals}
        timestamps = [f"01/01/{year} 00:00:00 EST" for year in mass['year'].values()]

        trim_data = {
            'scenario_name': scen.name,
            'chemicals': {c.id: c.name for c in scen.chemicals},
            'timestamps': timestamps,
        }
        trim_data["parcels"] = compile_mirc_parcel_data(scen, chems, conc, timestamps, logger)

        logger.debug(f"Checking for AERMOD data used in {scen.name}...")
        try:
            dep_data = associated_file_helper(
                scen.id, 'deposition_overlay', "CHECK"
            )
            if dep_data:
                merge_aermod_data(
                    trim_data, dep_data['presigned_urls']['original.plt'],
                    logger
                )
        except Exception:
            import traceback
            logger.warning(f'Unable to parse AERMOD data:\n{traceback.format_exc()}')

        return {"trim_data": trim_data}
    else:
        return {"trim_data": {"message": "No valid data found"}}


def compile_mirc_parcel_data(scen, chems, conc, timestamps, logger):
    parcels = []
    for parcel in scen.parcels:
        logger.debug(f"Compiling parcel data for {parcel.name}...")
        p = {
            "name": parcel.name,
            "vertices": parcel.utm_vertices,
            "volume_elements": [],
        }
        for volume_element in parcel.volume_elements:
            ve = {
                "name": volume_element.name,
                "compartments": [],
            }
            for compartment in volume_element.compartments:
                c = {
                    "name": compartment.name,
                    "properties": {},
                }

                # properties not relevant for a given compartment can be skipped
                for chem_name in chems.keys():
                    props = {}

                    # constants
                    if "air" in c["name"].lower():
                        props["rho_a"] = {
                            "value": compartment.rho.magnitude,
                            "unit": str(compartment.rho.units),  # "g/cm^3"
                        }

                    chem_kd = chems[chem_name].Kd(compartment=compartment)
                    props["Kd"] = {
                        "value": chem_kd.magnitude,
                        "unit": str(chem_kd.units),  # "L/kg"
                    }

                    chem_fmd = chems[chem_name].FractionMass_Dissolved(compartment=compartment)
                    if chem_fmd:
                        if isinstance(chem_fmd, ureg.Quantity):
                            props["FMD"] = chem_fmd.magnitude
                        else:
                            props["FMD"] = chem_fmd

                    chem_fv = chems[chem_name].FractionMass_Vapor(compartment=compartment)
                    if chem_fv:
                        if isinstance(chem_fv, ureg.Quantity):
                            props["Fv"] = chem_fv.magnitude
                        else:
                            props["Fv"] = chem_fv

                    filtered_key = f'{chem_name}_{compartment.standard_name}'
                    if filtered_key in conc:
                        filtered_conc = list(conc[filtered_key].values())
                        filtered_conc_units = list(conc[filtered_key+"_units"].values())

                        # timestamp values
                        props["C"] = {}  # concentration
                        props["Drwp"] = {}  # deposition rate wet particle
                        chem_wet = chems[chem_name].ParticleVolumetricWetDepositionRate(compartment=compartment)
                        props["Drdp"] = {}  # deposition rate dry particle
                        chem_dry = chems[chem_name].ParticleVolumetricDRYDepositionRate(compartment=compartment)

                        for i, timestamp in enumerate(timestamps):
                            if isinstance(filtered_conc_units[0], str):
                                props["C"][timestamp] = {
                                    "value": filtered_conc[i],
                                    "unit": filtered_conc_units[i]  # "ug/g"
                                }
                            props["Drwp"][timestamp] = {
                                "value": chem_wet.magnitude,
                                "unit": str(chem_wet.units)  # "g/day/m^2"
                            }
                            props["Drdp"][timestamp] = {
                                "value": chem_dry.magnitude,
                                "unit": str(chem_dry.units)  # "g/day/m^2"
                            }
                    if props:
                        c["properties"][chem_name] = props
                ve["compartments"].append(c)
            p["volume_elements"].append(ve)
        parcels.append(p)
    return parcels


def merge_aermod_data(trim_data, aermod_plt_file, logger):
    if aermod_plt_file.startswith('/static'):
        local_file_loc = get_local_misc_file_loc().split(f'{os.path.sep}static{os.path.sep}.uploads')[0]
        aermod_file_loc = os.path.join(local_file_loc, aermod_plt_file[1:])
        with open(aermod_file_loc) as f:
            raw_data = f.read()
    else:
        r = requests.get(aermod_plt_file)
        r.raise_for_status()
        raw_data = r.text

    logger.debug('Parsing AERMOD data...')

    aermod_data = parse_aermod_data(raw_data)

    logger.info('Merging AERMOD data with TRIM parcels...')

    parcels = trim_data['parcels']

    def average_aermod_data(data):
        avg = sum(data) / len(data)
        return avg

    # We use Decimal in this function because floats are sometimes imprecise
    for entry in aermod_data:
        if entry['net_id'] is not None:
            continue

        x = float(entry['x'])
        y = float(entry['y'])

        point = (x, y)

        parcel = None
        for p in parcels:
            vertices = p.get('vertices', None)
            if vertices is None:
                continue
            polygon = Path(vertices)
            if polygon.contains_point(point):
                parcel = p
                break

        if parcel is None:
            logger.debug(
                f'Unable to match AERMOD point {point} to any TRIM parcel'
            )
            continue

        p_aermod = parcel.get('aermod', [])
        p_aermod.append(entry)
        parcel['aermod'] = p_aermod

    has_aermod = False
    for p in parcels:
        if 'aermod' not in p:
            continue

        has_aermod = True
        data = p['aermod']

        conc = average_aermod_data([
            Decimal(x['average_conc']) for x in data
        ])
        dry_dep = average_aermod_data([
            Decimal(x['dry_depo']) for x in data
        ])
        wet_dep = average_aermod_data([
            Decimal(x['wet_depo']) for x in data
        ])

        p['aermod'] = {
            'C_avg': float(conc),
            'Drdp_avg': float(dry_dep),
            'Drwp_avg': float(wet_dep),
            'receptors': [(float(x['x']), float(x['y'])) for x in data]
        }

    trim_data['includes_aermod'] = has_aermod


def parse_aermod_data(raw_data):
    data = []
    cols = []
    lines = [ln for ln in raw_data.split('\n') if ln.strip()]
    for i, ln in enumerate(lines):
        # Skip first 6 lines
        if i == 6:  # Line 7 is colnames
            cols = ln.split('  ')[1:]
            cols = [
                x.strip().lower().replace(' ', '_')
                for x in cols
                if x.strip() != ''
            ]
        elif i > 7:  # Skip line 8, the rest of the lines are data
            vals = ln.split()
            while len(vals) < len(cols):
                vals.append(None)
            data.append(dict(zip(cols, vals)))
    return data
