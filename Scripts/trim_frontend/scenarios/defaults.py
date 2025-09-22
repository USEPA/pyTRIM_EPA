from trim_db.schema import Scenario
from trim_db.schema.utils.serialize import register_serializer
from trim_db.services import ParameterService


@register_serializer(Scenario)
def serialize_scenario(scen: Scenario):
    start_time, end_time = scen.sim_begin_end_time
    try:
        erosion_source = scen.erosionRateCalcSource
    except Exception:
        erosion_source = 1
    s = {
        'id': scen.id,
        'name': scen.name,
        'description': scen.description,
        'simulation_start_date': start_time,
        'simulation_end_date': end_time,
        'has_chemicals': len(list(scen.chemicals)) > 0,
        'has_parcels': len(list(scen.parcels)) > 0,
        'erosionRateSource': erosion_source
    }
    return s
   

def get_met_data(scen):
    ambient_air_temp = scen.AirTemperature
    if ambient_air_temp:
        ambient_air_temp = ambient_air_temp.to("K").magnitude
    else:
        ambient_air_temp = None

    # All air compartments are expected to have the same height = mixing height
    air_comps = [
        c for c in scen.get_compartment(media='Air')
        if "Upper" not in c.standard_name
    ]
    if len(air_comps) == 0:
        print("\nThis scenario does not have any parcels containing air volume elements\n")
        mixing_height = -1
    else:
        mixing_height = air_comps[0].volume_element.height.magnitude

    met_data = {
        'ambient_air_static_value': ambient_air_temp,
        'wind_speed_static_value': scen.horizontalWindSpeed,
        'wind_direction_static_value': scen.windDirection,
        'mixing_height_static_value': mixing_height,
        'daytime_indicator_static_value': scen.isDay_Dynamic,
        'precipitation_static_value_rate': scen.Rain.magnitude,
        'cumulative_precip': scen.cumulativeRain,

    }

    wet_dep = {}

    leaf_types = ['Coniferous_Leaf', 'Deciduous_Leaf', 'Grass_Leaf', 'Agriculture_Leaf']
    for x in leaf_types:
        k = x.lower()
        wet_dep[f'wet_dep_interception_frac_{k}'] = get_wet_interception_params(
            scen, 1, x
        )
        wet_dep[f'calc_wet_dep_interception_frac_{k}'] = get_wet_interception_params(
            scen, 2, x, default=0
        )
        wet_dep[f'wet_dep_interception_frac_{k}_calculated'] = get_wet_interception_params(
            scen, 3, x
        )

    # print(wet_dep)

    met_data['wet_dep_interception'] = wet_dep

    return met_data


def get_wet_interception_params(scen, wi_type, media_name, default=-1):
    # TODO Need to figure out why agriculture_leaf does not have CalculateWIF
    try:
        c = scen.get_compartment(media=media_name)
        if not c:
            return default
        c = c[0]
        # IMPORTANT: We are assuming all relevant scenario compartments of this type will have the same value.
        # This requires that when this parameter is updated, it is done so for all compartments of this type for
        # this scenario
        if wi_type == 1:
            wi_data = c.WetDepInterceptionFraction_UserSupplied
        elif wi_type == 2:
            wi_data = c.CalculateWetDepInterceptionFraction
        elif wi_type == 3:
            wi_data = c.WetDepInterceptionFraction_Calculated
        else:
            raise ValueError('Unknown WI_Type!')
        # print(wi_data)
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


def get_seasonal_dynamics(scen):
    sd = {
        'litterfall_coniferous': get_seasonal_dynamics_params(scen, 'lf', 'Coniferous_Leaf'),
        'allow_exchange_coniferous': get_seasonal_dynamics_params(scen, 'ae', 'Coniferous_Leaf'),
        'litterfall_deciduous': get_seasonal_dynamics_params(scen, 'lf', 'Deciduous_Leaf', 0.0126),
        'allow_exchange_deciduous': get_seasonal_dynamics_params(scen, 'ae', 'Deciduous_Leaf'),
        'litterfall_grass': get_seasonal_dynamics_params(scen, 'lf', 'Grass_Leaf', 0.0126),
        'allow_exchange_grass': get_seasonal_dynamics_params(scen, 'ae', 'Grass_Leaf'),
        'litterfall_agriculture': get_seasonal_dynamics_params(scen, 'lf', 'Agriculture_Leaf', 0.0126),
        'allow_exchange_agriculture': get_seasonal_dynamics_params(scen, 'ae', 'Agriculture_Leaf')
    }
    return sd


def get_seasonal_dynamics_params(scen, sd_type, media_name, default=-1):
    try:
        c = scen.get_compartment(media=media_name)
        if not c:
            return default
        c = c[0]
        # IMPORTANT: We are assuming all relevant scenario compartments of this type will have the same value.
        # This requires that when this parameter is updated, it is done so for all compartments of this type for
        # this scenario
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
        'meteo_precipitation_field_name_rate_TS': 'Rain',
        'meteo_precipitation_static_value_cumulative': 'cumulativeRain',
        'meteo_precipitation_field_name_cumulative_TS': 'cumulativeRain',
        'meteo_interception_fractions_static_deciduous': ['Deciduous_Leaf', 'WetDepInterceptionFraction_UserSupplied'],
        'meteo_interception_fractions_static_grass': ['Grass', 'WetDepInterceptionFraction_UserSupplied'],
        'meteo_interception_fractions_static_coniferous': ['Coniferous_Leaf', 'WetDepInterceptionFraction_UserSupplied'],
        'meteo_interception_fractions_static_agriculture': ['Agriculture_Leaf', 'WetDepInterceptionFraction_UserSupplied'],
        'meteo_interception_fractions_calculated_deciduous': ['Deciduous_Leaf', 'CalculateWetDepInterceptionFraction'],
        'meteo_interception_fractions_calculated_grass': ['Grass', 'CalculateWetDepInterceptionFraction'],
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
        'seasonal_grasses_herbs_litterfall_static_value': ['Grass', 'LitterFallRate'],
        'seasonal_grasses_herbs_litterfall_field_name_TS': ['Grass', 'LitterFallRate'],
        'seasonal_grasses_herbs_allowexchange_static_value': ['Grass', 'AllowExchange_Dynamic'],
        'seasonal_grasses_herbs_allowexchange_field_name_TS': ['Grass', 'AllowExchange_Dynamic'],
        'seasonal_agriculture_litterfall_static_value': ['Agriculture_Leaf', 'LitterFallRate'],
        'seasonal_agriculture_litterfall_field_name_TS': ['Agriculture_Leaf', 'LitterFallRate'],
        'seasonal_agriculture_allowexchange_static_value': ['Agriculture_Leaf', 'AllowExchange_Dynamic'],
        'seasonal_agriculture_allowexchange_field_name_TS': ['Agriculture_Leaf', 'AllowExchange_Dynamic'],
    }
}
