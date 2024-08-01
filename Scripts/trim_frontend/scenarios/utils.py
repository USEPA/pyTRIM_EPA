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
    default_variable_kwargs = [
        # table 2
        {
            "variable_name": "erosion2-unit_soil_loss",
            "full_name": "erosion2-unit_soil_loss",
            "domain_id": 1,
        },
        {
            "variable_name": "erosion2-empirical_intercept_coefficient",
            "full_name": "erosion2-empirical_intercept_coefficient",
            "domain_id": 1,
        },
        {
            "variable_name": "erosion2-empirical_slope_coefficient",
            "full_name": "erosion2-empirical_slope_coefficient",
            "domain_id": 1,
        },
        {
            "variable_name": "erosion2-sediment_delivery_ratio",
            "full_name": "erosion2-sediment_delivery_ratio",
            "domain_id": 1,
        },
        {
            "variable_name": "erosion2-total_effective_erosion_rate",
            "full_name": "erosion2-total_effective_erosion_rate",
            "domain_id": 1,
        },

        # table 3
        {
            "variable_name": "erosion3-rainfall_erosivity_index",
            "full_name": "erosion3-rainfall_erosivity_index",
            "domain_id": 1,
            "default_value": 300,
        },
        {
            "variable_name": "erosion3-erodibility_index",
            "full_name": "erosion3-erodibility_index",
            "domain_id": 1,
            "default_value": 3.6e-1,
        },
        {
            "variable_name": "erosion3-slope_gradient",
            "full_name": "erosion3-slope_gradient",
            "domain_id": 1,
            "default_value": 1,
        },
        {
            "variable_name": "erosion3-slope_length",
            "full_name": "erosion3-slope_length",
            "domain_id": 1,
            "default_value": 1.5,
        },
        {
            "variable_name": "erosion3-topographical_length-slope_factor",
            "full_name": "erosion3-topographical_length-slope_factor",
            "domain_id": 1,
            "default_value": 1.5e-2,
        },
        {
            "variable_name": "erosion3-cover_management_factor",
            "full_name": "erosion3-cover_management_factor",
            "domain_id": 1,
            "default_value": 0.1,
        },
        {
            "variable_name": "erosion3-supporting_practices_factor",
            "full_name": "erosion3-supporting_practices_factor",
            "domain_id": 1,
            "default_value": 1,
        },
        {
            "variable_name": "erosion3-unit_soil_loss",
            "full_name": "erosion3-unit_soil_loss",
            "domain_id": 1,
        },
        {
            "variable_name": "erosion3-empirical_intercept_coefficient",
            "full_name": "erosion3-empirical_intercept_coefficient",
            "domain_id": 1,
        },
        {
            "variable_name": "erosion3-empirical_slope_coefficient",
            "full_name": "erosion3-empirical_slope_coefficient",
            "domain_id": 1,
        },
        {
            "variable_name": "erosion3-sediment_delivery_ratio",
            "full_name": "erosion3-sediment_delivery_ratio",
            "domain_id": 1,
        },
        {
            "variable_name": "erosion3-total_effective_erosion_rate",
            "full_name": "erosion3-total_effective_erosion_rate",
            "domain_id": 1,
        },
    ]

    for kwargs in default_variable_kwargs:
        if not ParameterService.definitions.get(variable_name=kwargs["variable_name"]):
            ParameterService.definitions.create(**kwargs, no_commit=True)
    ParameterService.commit()
