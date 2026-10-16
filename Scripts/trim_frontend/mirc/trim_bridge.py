
import json
from trim_db.schema import ureg
from ..utils.logging import make_logger


def compile_mirc_data(scen, logger=None):
    if not logger:
        logger = make_logger('compile_mirc_data')
    logger.info(f"Compiling required MIRC data for scenario {scen.name}...")

    latest_model_run = scen.latest_proc_status

    if (not latest_model_run) or latest_model_run.is_run_error:
        return {"trim_data": {"message": "No valid data found"}}

    mass = json.loads(latest_model_run.result_nt)
    mass = json.loads("{"+mass+"}")
    conc = json.loads(latest_model_run.result_conc)
    conc = json.loads("{"+conc+"}")

    logger.info(f"Model run found, using run with id [{latest_model_run.id}]...")

    timestamps = [f"01/01/{year} 00:00:00 EST" for year in mass['year'].values()]

    trim_data = {
        'scenario_name': scen.name,
        'chemicals': {c.id: c.name for c in scen.chemicals},
        'timestamps': timestamps,
    }

    parcels, uses_aermod = compile_mirc_parcel_data(scen, conc, timestamps, logger)
    trim_data['parcels'] = parcels
    trim_data['uses_aermod'] = uses_aermod

    return {"trim_data": trim_data}


def compile_mirc_parcel_data(scen, conc, timestamps, logger):
    chems = list(scen.chemicals)

    uses_aermod = False
    parcels = []
    for parcel in scen.parcels:
        # logger.debug(f"Compiling parcel data for {parcel.name}...")
        p = {
            "name": parcel.name,
            "vertices": parcel.utm_vertices,
            "volume_elements": [],
        }

        wet_dep_rate_src = parcel.get_compartment(media='Source|Wet_Particle')
        if isinstance(wet_dep_rate_src, list):
            wet_dep_rate_src = wet_dep_rate_src[0]

        dry_dep_rate_src = parcel.get_compartment(media='Source|Dry_Particle')
        if isinstance(dry_dep_rate_src, list):
            dry_dep_rate_src = dry_dep_rate_src[0]

        base_dep_rates = {
            chem.name: {
                "drwp": wet_dep_rate_src.surfaceDepositionRate(chemical=chem).to('g/year'),
                "drdp": dry_dep_rate_src.surfaceDepositionRate(chemical=chem).to('g/year')
            }
            for chem in chems
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
                for chem in chems:
                    props = {}

                    comp_drwp = None
                    comp_drdp = None
                    if 'soil_surface' in compartment.name.lower():
                        try:
                            comp_drwp = base_dep_rates[chem.name]['drwp'] / compartment.area
                            comp_drwp = {
                                "value": comp_drwp.magnitude,
                                "unit": str(comp_drwp.units)  # "g/day/m^2"
                            }
                        except Exception:
                            comp_drwp = None

                        try:
                            comp_drdp = base_dep_rates[chem.name]['drdp'] / compartment.area
                            comp_drdp = {
                                "value": comp_drdp.magnitude,
                                "unit": str(comp_drdp.units)  # "g/day/m^2"
                            }
                        except Exception:
                            comp_drdp = None
                    if comp_drwp is None:
                        comp_drwp = {
                            "value": 0,
                            "unit": "g/day/m^2"
                        }
                    if comp_drdp is None:
                        comp_drdp = {
                            "value": 0,
                            "unit": "g/day/m^2"
                        }

                    # constants
                    if "air" in compartment.name.lower():
                        air_density = compartment.AirDensity.to('g/m^3')               
                        props["rho_a"] = {
                            "value": round(air_density.magnitude, 6),
                            "unit": str(air_density.units),  # "g/m^3"
                        }
                        try:
                            aermod_Ca = compartment.aermodAirConcentration(chemical=chem)
                            props["C_aermod"] = {
                                "value": aermod_Ca.magnitude,
                                "unit": str(aermod_Ca.units),  # "ug/m^3"
                            }
                            if aermod_Ca.magnitude > 0:
                                uses_aermod = True
                        except (KeyError, AttributeError):
                            props["C_aermod"] = {
                                "value": 0,
                                "unit": "ug/m^3"
                            }

                    chem_kd = chem.Kd(compartment=compartment)
                    props["Kd"] = {
                        "value": chem_kd.magnitude,
                        "unit": str(chem_kd.units),  # "L/kg"
                    }

                    chem_fmd = chem.FractionMass_Dissolved(compartment=compartment)
                    if chem_fmd:
                        try:
                            props["FMD"] = chem_fmd.magnitude
                        except (KeyError, AttributeError):
                            props["FMD"] = chem_fmd

                    chem_fv = chem.FractionMass_Vapor(compartment=compartment)
                    if chem_fv:
                        try:
                            props["Fv"] = chem_fv.magnitude
                        except (KeyError, AttributeError):
                            props["Fv"] = chem_fv

                    filtered_key = f'{chem.name}_{compartment.standard_name}'
                    if filtered_key in conc:
                        filtered_conc = list(conc[filtered_key].values())
                        filtered_conc_units = list(conc[f'{filtered_key}_units'].values())
                        has_conc = isinstance(filtered_conc_units[0], str)

                        # timestamp values
                        props["C"] = {}  # concentration
                        props["Drwp"] = {}  # deposition rate wet particle
                        props["Drdp"] = {}  # deposition rate dry particle

                        for i, timestamp in enumerate(timestamps):
                            if has_conc:
                                props["C"][timestamp] = {
                                    "value": filtered_conc[i],
                                    "unit": filtered_conc_units[i]  # "ug/g"
                                }
                            # Drwp/Drdp don't actually vary by time ... but we act like they do ...
                            props["Drwp"][timestamp] = comp_drwp
                            props["Drdp"][timestamp] = comp_drdp
                    if props:
                        c["properties"][chem.name] = props
                ve["compartments"].append(c)
            p["volume_elements"].append(ve)
        parcels.append(p)
    return parcels, uses_aermod
