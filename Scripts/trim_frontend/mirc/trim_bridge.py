
import json
from trim_db.schema import ureg
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
        parcels, uses_aermod = compile_mirc_parcel_data(scen, chems, conc, timestamps, logger)
        trim_data['parcels'] = parcels
        trim_data['uses_aermod'] = uses_aermod

        return {"trim_data": trim_data}
    else:
        return {"trim_data": {"message": "No valid data found"}}


def compile_mirc_parcel_data(scen, chems, conc, timestamps, logger):
    uses_aermod = False
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

                    chem = chems[chem_name]

                    try:
                        wet_dep_rate = parcel.get_compartment(media='Source|Wet_Particle').surfaceDepositionRate(chemical=chem)
                        dry_dep_rate = parcel.get_compartment(media='Source|Dry_Particle').surfaceDepositionRate(chemical=chem)

                        comp_drwp = wet_dep_rate.to('g/year') / compartment.area
                        comp_drdp = dry_dep_rate.to('g/year') / compartment.area
                    except Exception:
                        comp_drwp = None
                        comp_drdp = None

                    # constants
                    if "air" in c["name"].lower():
                        props["rho_a"] = {
                            "value": compartment.rho.magnitude,
                            "unit": str(compartment.rho.units),  # "g/cm^3"
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
                                "value": None,
                                "unit": "ug/m^3"
                            }

                    chem_kd = chem.Kd(compartment=compartment)
                    props["Kd"] = {
                        "value": chem_kd.magnitude,
                        "unit": str(chem_kd.units),  # "L/kg"
                    }

                    chem_fmd = chem.FractionMass_Dissolved(compartment=compartment)
                    if chem_fmd:
                        if isinstance(chem_fmd, ureg.Quantity):
                            props["FMD"] = chem_fmd.magnitude
                        else:
                            props["FMD"] = chem_fmd

                    chem_fv = chem.FractionMass_Vapor(compartment=compartment)
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
                        props["Drdp"] = {}  # deposition rate dry particle

                        for i, timestamp in enumerate(timestamps):
                            if isinstance(filtered_conc_units[0], str):
                                props["C"][timestamp] = {
                                    "value": filtered_conc[i],
                                    "unit": filtered_conc_units[i]  # "ug/g"
                                }
                            if comp_drwp is not None:
                                props["Drwp"][timestamp] = {
                                    "value": comp_drwp.magnitude,
                                    "unit": str(comp_drwp.units)  # "g/day/m^2"
                                }
                            else:
                                props["Drwp"][timestamp] = {
                                    "value": 0,
                                    "unit": "g/day/m^2"
                                }
                            if comp_drdp is not None:
                                props["Drdp"][timestamp] = {
                                    "value": comp_drdp.magnitude,
                                    "unit": str(comp_drdp.units)  # "g/day/m^2"
                                }
                            else:
                                props["Drdp"][timestamp] = {
                                    "value": 0,
                                    "unit": "g/day/m^2"
                                }
                    if props:
                        c["properties"][chem_name] = props
                ve["compartments"].append(c)
            p["volume_elements"].append(ve)
        parcels.append(p)
    return parcels, uses_aermod
