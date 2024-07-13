from trim_db.services import *

def set_param_default_val(kwargs, val):
    try:
        default_params = ParameterService.definitions.get_all(**kwargs)
        for param in default_params:
            if not param.default_value:
                param.default_value = val
                ParameterService.definitions.update(param)
    except Exception as e:
        print(e)


def init_first_time_default_param_values():
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
        {"kwargs": {"variable_name": "waterEvaporationRate"}, "value": 0.7},

        # Aquatic Food Web
        {"kwargs": {"variable_name": "FoodIngestionRate"}, "value": 0},
    ]

    for obj in default_params:
        set_param_default_val(obj["kwargs"], obj["value"])
    ParameterService.commit()