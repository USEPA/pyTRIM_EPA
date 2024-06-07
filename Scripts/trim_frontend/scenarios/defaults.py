from trim_db.schema import Scenario
from trim_db.schema.utils.serialize import register_serializer
from trim_db.services import ChemicalService


@register_serializer(Scenario)
def serialize_scenario(scen: Scenario):
    start_time, end_time = scen.sim_begin_end_time
    s = {
        'id': scen.id,
        'name': scen.name,
        'description': scen.description,
        'simulation_start_date': start_time,
        'simulation_end_date': end_time,
        'scenario_chem': [c.name for c in scen.chemicals]
    }
    return s

    ambient_air_temp = scen.AirTemperature
    mixing_height = [
        a.height.magnitude for a in scen.compartments
        if a.media.isa("Air") and "Upper" not in a.standard_name
    ]
    s = {
        **s,
        'erosionRateSource': scen.erosionRateCalcSource or 1,
        'all_chem': [c.name for c in ChemicalService.get_all()],
        'meteo': {
            'ambient_air_temp': (
                ambient_air_temp.to("K").magnitude
                if ambient_air_temp is not None
                else None
            ),
            'horizontal_wind_speed': scen.horizontalWindSpeed,
            'wind_dir': scen.windDirection,
            # TODO scen?.mixingHeight??, # it is in Input_files/1Parameters.csv
            # wired to top of Air comp/VE in Foundries_SS (4) Properties.txt,
            'mixing_height': (
                scen.mixingHeight if scen.mixingHeight
                else (mixing_height[0] if mixing_height else None)
            ),
            'daytime_indicator': scen.isDay_Dynamic,
            'precipitation': scen.Rain,
            'cumulative_precip': scen.cumulativeRain},
        'wet_dep_interception': {
            'wet_dep_interception_frac_coniferous_leaf': get_wet_interception_params(scen, 1, "Coniferous_Leaf"),
            'calc_wet_dep_interception_frac_coniferous_leaf': get_wet_interception_params(scen, 2, "Coniferous_Leaf"),
            'wet_dep_interception_frac_coniferous_leaf_calculated': get_wet_interception_params(scen, 3, "Coniferous_Leaf"),
            'wet_dep_interception_frac_deciduous_leaf': get_wet_interception_params(scen, 1, "Deciduous_Leaf"),
            'calc_wet_dep_interception_frac_deciduous_leaf': get_wet_interception_params(scen, 2, "Deciduous_Leaf"),
            'wet_dep_interception_frac_deciduous_leaf_calculated': get_wet_interception_params(scen, 3, "Deciduous_Leaf"),
            'wet_dep_interception_frac_grass_leaf': get_wet_interception_params(scen, 1, "Grass_Leaf"),
            'calc_wet_dep_interception_frac_grass_leaf': get_wet_interception_params(scen, 2, "Grass_Leaf"),
            'wet_dep_interception_frac_grass_leaf_calculated': get_wet_interception_params(scen, 3, "Grass_Leaf"),
            'wet_dep_interception_frac_agriculture_leaf': get_wet_interception_params(scen, 1, "Agriculture_Leaf"),
            'calc_wet_dep_interception_frac_agriculture_leaf': get_wet_interception_params(scen, 2, "Agriculture_Leaf"),
            'wet_dep_interception_frac_agriculture_leaf_calculated': get_wet_interception_params(scen, 3, "Agriculture_Leaf")
        },
        'seasonal_dynamics': {
            'litterfall_coniferous': get_seasonal_dynamics_params(scen, 'lf', 'Coniferous_Leaf'),
            'allow_exchange_coniferous': get_seasonal_dynamics_params(scen, 'ae', 'Coniferous_Leaf'),
            'litterfall_deciduous': get_seasonal_dynamics_params(scen, 'lf', 'Deciduous_Leaf'),
            'allow_exchange_deciduous': get_seasonal_dynamics_params(scen, 'ae', 'Deciduous_Leaf'),
            'litterfall_grass': get_seasonal_dynamics_params(scen, 'lf', 'Grass_Leaf'),
            'allow_exchange_grass': get_seasonal_dynamics_params(scen, 'ae', 'Grass_Leaf'),
            'litterfall_agriculture': get_seasonal_dynamics_params(scen, 'lf', 'Agriculture_Leaf'),
            'allow_exchange_agriculture': get_seasonal_dynamics_params(scen, 'ae', 'Agriculture_Leaf')
        }
    }
    return s


def get_wet_interception_params(scen, wi_type, media_name, default=-1):
    # TODO Need to figure out why agriculture_leaf does not have CalculateWIF
    try:
        c = scen.get_compartment(media=media_name)
        if not c:
            return default
        c = c[0]
        if wi_type == 1:
            wi_data = c.WetDepInterceptionFraction_UserSupplied
        elif wi_type == 2:
            wi_data = c.CalculateWetDepInterceptionFraction
        elif wi_type == 3:
            wi_data = c.WetDepInterceptionFraction_Calculated
        else:
            raise ValueError('Unknown WI_Type!')
        if wi_data is None:
            return default
        try:
            return float(wi_data.magnitude)
        except AttributeError:
            return float(wi_data)
    except TypeError as e:
        err = str(e)
        if 'unsupported operand' in err:
            pass
        else:
            raise
    return default


def get_seasonal_dynamics_params(scen, sd_type, media_name, default=-1):
    try:
        c = scen.get_compartment(media=media_name)
        if not c:
            return default
        c = c[0]
        if sd_type == 'lf':
            sd_data = c.LitterFallRate
        elif sd_type == 'ae':
            # TODO is allowExchange_forAir correct? should we use _forOther instead?
            #   or should we directly use _Dynamic (which these point to)
            sd_data = c.AllowExchange_forAir
        else:
            raise ValueError('Unknown SD_Data!')
        if sd_data is None:
            return default
        try:
            return float(sd_data.magnitude)
        except AttributeError:
            return float(sd_data)
    except TypeError as e:
        err = str(e)
        if 'unsupported operand' in err:
            pass
        else:
            raise
    return default


param_map = {
    'meteo': {
        'meteo_ambient_air_static_value': 'AirTemperature',
        'meteo_ambient_air_field_name_TS': 'AirTemperature',
        'meteo_wind_speed_static_value': 'horizontalWindSpeed',
        'meteo_wind_speed_field_name_TS': 'horizontalWindSpeed',
        'meteo_wind_direction_static_value': 'windDirection',
        'meteo_wind_direction_field_name_TS': 'windDirection',
        'meteo_mixing_height_static_value': 'mixingHeight',
        'meteo_mixing_height_field_name_TS': 'mixingHeight',
        'meteo_daytime_indicator_static_value': 'isDay_Dynamic',
        'meteo_daytime_indicator_field_name_TS': 'isDay_Dynamic',
        'meteo_precipitation_static_value_rate': 'Rain',
        'meteo_precipitation_field_name_TS': 'Rain',
        'meteo_interception_fractions_static_deciduous': ['Deciduous_Leaf', 'WetDepInterceptionFraction_UserSupplied'],
        'meteo_interception_fractions_static_grass': ['Grass_Leaf', 'WetDepInterceptionFraction_UserSupplied'],
        'meteo_interception_fractions_static_coniferous': ['Coniferous_Leaf', 'WetDepInterceptionFraction_UserSupplied'],
        'meteo_interception_fractions_static_agriculture': ['Agriculture_Leaf', 'WetDepInterceptionFraction_UserSupplied'],
        'meteo_interception_fractions_calculated_deciduous': ['Deciduous_Leaf', 'CalculateWetDepInterceptionFraction'],
        'meteo_interception_fractions_calculated_grass': ['Grass_Leaf', 'CalculateWetDepInterceptionFraction'],
        'meteo_interception_fractions_calculated_coniferous': ['Coniferous_Leaf', 'CalculateWetDepInterceptionFraction'],
        'meteo_interception_fractions_calculated_agriculture': ['Agriculture_Leaf', 'CalculateWetDepInterceptionFraction']
    },
    'seasonal': {
        'seasonal_deciduous_forest_litterfall_static_value': ['Deciduous_Leaf', 'LitterFallRate'],
        'seasonal_deciduous_forest_litterfall_field_name_TS': ['Deciduous_Leaf', 'LitterFallRate'],
        'seasonal_deciduous_forest_allowexchange_field_name_TS': ['Deciduous_Leaf', 'AllowExchange_Dynamic'],
        'seasonal_deciduous_forest_allowexchange_static_value': ['Deciduous_Leaf', 'AllowExchange_Dynamic'],
        'seasonal_coniferous_forest_litterfall_static_value': ['Coniferous_Leaf', 'LitterFallRate'],
        'seasonal_coniferous_forest_litterfall_field_name_TS': ['Coniferous_Leaf', 'LitterFallRate'],
        'seasonal_coniferous_forest_allowexchange_static_value': ['Coniferous_Leaf', 'AllowExchange_Dynamic'],
        'seasonal_coniferous_forest_allowexchange_field_name_TS': ['Coniferous_Leaf', 'AllowExchange_Dynamic'],
        'seasonal_grasses_herbs_litterfall_static_value': ['Grass_Leaf', 'LitterFallRate'],
        'seasonal_grasses_herbs_litterfall_field_name_TS': ['Grass_Leaf', 'LitterFallRate'],
        'seasonal_grasses_herbs_allowexchange_static_value': ['Grass_Leaf', 'AllowExchange_Dynamic'],
        'seasonal_grasses_herbs_allowexchange_field_name_TS': ['Grass_Leaf', 'AllowExchange_Dynamic'],
        'seasonal_agriculture_litterfall_static_value': ['Agriculture_Leaf', 'LitterFallRate'],
        'seasonal_agriculture_litterfall_field_name_TS': ['Agriculture_Leaf', 'LitterFallRate'],
        'seasonal_agriculture_allowexchange_static_value': ['Agriculture_Leaf', 'AllowExchange_Dynamic'],
        'seasonal_agriculture_allowexchange_field_name_TS': ['Agriculture_Leaf', 'AllowExchange_Dynamic'],
    }
}
