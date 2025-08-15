import pint
from trim_db.services import *
from .defaults import EROSION_TABLE_KWARGS


def set_param_default_val(kwargs, val):
    try:
        default_params = ParameterService.definitions.get_all(**kwargs)
        for param in default_params:
            if not param.default_value:
                param.default_value = val
                ParameterService.definitions.update(param)
    except Exception as e:
        print('error setting param:', e)


def init_first_time_default_param_values():
    # fmt: off
    default_params = [
        # Meteorology
        {"kwargs": {"variable_name":"AirTemperature", "default_unit":"K"}, "value": 298},
        {"kwargs": {"variable_name":"horizontalWindSpeed"}, "value": 1.6},
        {"kwargs": {"variable_name":"windDirection"}, "value": 270},
        {"kwargs": {"variable_name":"isDay_Dynamic"}, "value": 1},
        {"kwargs": {"variable_name":"Rain"}, "value": 0.0041}, # Precipitation

        # Water Body Properties
        {"kwargs": {"variable_name": "WaterTemperature", "default_unit":"K"}, "value": 298},
        {"kwargs": {"variable_name": "pH"}, "value": 7.3},
        {"kwargs": {"variable_name": "AlgaeDensityInWaterColumn"}, "value": 0.0025},
        {"kwargs": {"variable_name": "ChlorideConcentration"}, "value": 8},
        {"kwargs": {"variable_name": "ChlorophyllConcentration"}, "value": 0.0029},
        {"kwargs": {"variable_name": "OrganicCarbonContent"}, "value": 0.02},
        {"kwargs": {"variable_name": "SuspendedSedimentConcentration"}, "value": 0.05},
        {"kwargs": {"variable_name": "ExternalSedimentInflow"}, "value": 0},
        {"kwargs": {"variable_name": "SedimentDepositionVelocity"}, "value": 2},
        {"kwargs": {"variable_name": "waterEvaporationRate"}, "value": 0.7}

        # Aquatic Food Web
        # {"kwargs": {"variable_name": "FoodIngestionRate"}, "value": 0},
    ]
    # fmt: on

    for obj in default_params:
        set_param_default_val(obj["kwargs"], obj["value"])
    ParameterService.commit()


def init_erosion_default_params():
    init_parameter_definitions(EROSION_TABLE_KWARGS)


def init_parameter_definitions(kwarg_list, check_subtypes=False):
    for kwargs in kwarg_list:
        if check_subtypes:
            default_param = ParameterService.definitions.get(**kwargs)
        else:
            default_param = ParameterService.definitions.get(full_name=kwargs["full_name"])
        if not default_param:
            ParameterService.definitions.create(**kwargs, no_commit=True)
    ParameterService.commit()


def compile_mirc_parcel_data(scen, chems, conc, timestamps, logger):
    logger.info(f"Compiling parcel data for...")
    parcels = []
    for parcel in scen.parcels:
        logger.info(f"{parcel.name}")
        p = {
            "name": parcel.name,
            "vertices": parcel.vertices,
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
                    filtered_key = f'{chem_name}_{compartment.standard_name}'
                    filtered_conc = list(conc[filtered_key].values())
                    filtered_conc_units = list(conc[filtered_key+"_units"].values())

                    # constants
                    if "air" in c["name"].lower():
                        props["rho_a"] = {
                            "value": compartment.rho.magnitude,
                            "unit": str(compartment.rho.units), # "g/cm^3"
                        }

                    chem_kd = chems[chem_name].Kd(compartment=compartment)
                    props["Kd"] = {
                        "value": chem_kd.magnitude,
                        "unit": str(chem_kd.units), # "L/kg"
                    }

                    chem_fmd = chems[chem_name].FractionMass_Dissolved(compartment=compartment)
                    if chem_fmd:
                        if isinstance(chem_fmd, pint.Quantity):
                            props["FMD"] = chem_fmd.magnitude
                        else:
                            props["FMD"] = chem_fmd
    
                    chem_fv = chems[chem_name].FractionMass_Vapor(compartment=compartment)
                    if chem_fv:
                        if isinstance(chem_fv, pint.Quantity):
                            props["Fv"] = chem_fv.magnitude
                        else:
                            props["Fv"] = chem_fv

                    # timestamp values
                    props["C"] = {}  # concentration

                    chem_wet = chems[chem_name].ParticleVolumetricWetDepositionRate(compartment=compartment)
                    props["Drwp"] = {}  # deposition rate wet particle

                    chem_dry = chems[chem_name].ParticleVolumetricDRYDepositionRate(compartment=compartment)
                    props["Drdp"] = {}  # deposition rate dry particle
                    for i, timestamp in enumerate(timestamps):
                        if isinstance(filtered_conc_units[0], str):
                            props["C"][timestamp] = {
                                "value": filtered_conc[i],
                                "unit": filtered_conc_units[i] # "ug/g"
                            }
                        props["Drwp"][timestamp] = {
                            "value": chem_wet.magnitude,
                            "unit": str(chem_wet.units) # "g/day/m^2"
                        }
                        props["Drdp"][timestamp] = {
                            "value": chem_dry.magnitude,
                            "unit": str(chem_dry.units) # "g/day/m^2"
                        }

                    c["properties"][chem_name] = props
                ve["compartments"].append(c)
            p["volume_elements"].append(ve)
        parcels.append(p)
    return parcels
