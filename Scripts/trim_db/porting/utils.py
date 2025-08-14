import re
import pandas as pd
from numpy import timedelta64
from functools import partial
from pyproj import CRS, Transformer
from .config import MEDIA_MAP
from ..schema.parameters.equations import *
from ..services import *

__all__ = [
    'read_master_library',
    'read_external_data',
    'safe_name', 'clean_prop', 'clean_unit',
    'clean_compartment_name',
    'UNIT_SUFFIXES',
    'split_unit_suffix',
    'clean_equation',
    'transform_coordinates_to_decimal',
    'do_replacements',
    'GLOBAL_REPLACE'
]

MET_DATA_MAP = {
        'Scenario': {
            'wt_av_rain': 'Rain',
            'wt_av_airtemperature': 'AirTemperature',
            'wt_av_horizontalwindspeed': 'horizontalWindSpeed',
            'wt_av_winddirection': 'windDirection',
            'wt_av_isday': 'isDay_Dynamic',
            'wt_av_cumulativerain': 'cumulativeRain',
        },
        'Compartment': {
            'wt_av_allowexchange': ['AllowExchange_Dynamic', 'Flora'],
            'wt_av_litterfallrate': ['LitterFallRate', '$Leaf']
        },
        'ignore': [
            'wt_av_mixingheight',
            'frac_time_rain',
            'frac_time_exchange_no_rain',
            'frac_time_exchange_rain',
            'frac_time_exchange_day',
            'frac_time_exchange_not_day'
        ]
}

def read_master_library(filepath, import_rules={}):
    print(f'Reading master library from "{filepath}" ...')
    read_lib = partial(
        pd.read_csv, filepath,
        sep=';', encoding='windows-1252', low_memory=False
    )

    df_lib = read_lib(skiprows=[0], names=read_lib(nrows=0).columns.values)

    from trim_db.schema import Scenario

    default_entries = import_rules.get('default_entries', {})

    for const in default_entries.get('constants', []):
        Scenario.parameters.add(const[0], value=const[1], unit=const[2])

    parsed = parse_master_library_params(df_lib)

    return parsed


def read_external_data(filepaths, scenario_name):
    external_dfs = {}
    for file_type, filepath in filepaths.items():
        print(f'Reading external data: {file_type} from "{filepath}" ...')
        read_lib = partial(
            pd.read_csv, filepath,
            sep=',', encoding='windows-1252', low_memory=False
        )
        if file_type == "met_file":
            external_dfs['df_met'] = read_lib(
                skiprows=[0],
                names=[i.lower() for i in read_lib(nrows=0).columns.values]
            )
        elif file_type == "allowexchange_file":
            external_dfs['df_ae'] = read_lib(
                skiprows=[0],
                names=[i.lower() for i in read_lib(nrows=0).columns.values]
            )
        elif file_type == "litterfall_file":
            external_dfs['df_lf'] = read_lib(
                skiprows=[0],
                names=[i.lower() for i in read_lib(nrows=0).columns.values]
            )

    parsed = parse_met_data(**external_dfs)

    from trim_db.services import ScenarioService, CompartmentService

    scenario = ScenarioService.get(name=scenario_name)
    for k, v in parsed.items():
        if k in MET_DATA_MAP["Scenario"]:
            n = clean_prop(MET_DATA_MAP["Scenario"][k])
            par = scenario.parameters.get(n)
            if par is None:
                print(
                    f'"{n}" not found in {scenario}! Adding "{n}" = {v} ...'
                )
                par = scenario.parameters.add(n, value=v)
            else:
                par.value = v
        elif k in MET_DATA_MAP["Compartment"]:
            n = clean_prop(MET_DATA_MAP["Compartment"][k][0])
            m = MET_DATA_MAP["Compartment"][k][1]
            compartments = [
                c for c in scenario.compartments
                if c.media.isa(m) and not c.media.isa("Coniferous_Forest")
            ]
            for comp in compartments:
                par = comp.parameters.get(n)
                if par is None:
                    print(
                        f'"{n}" not found in {comp}! Adding "{n}" = {v} ...'
                    )
                    par = comp.parameters.add(n, value=v)
                else:
                    par.value = v

    ScenarioService.commit()
    CompartmentService.commit()

    return parsed


def parse_master_library_params(library_df):
    print('Parsing library parameters ...')

    params = {}
    for object_type in library_df.ObjectType.unique():
        df = library_df[
            library_df.ObjectType == object_type
        ].fillna(pd.NA).replace([pd.NA], [None])

        objs = params.setdefault(object_type, {})

        filter_props = []

        object_type = object_type.lower()

        for name, data in df.groupby('ObjectName'):
            obj_params = objs.setdefault(name, {})

            for param_data in data.itertuples():
                prop, suff = split_unit_suffix(param_data.PropertyName)
                prop = clean_prop(prop)
                if not prop or prop.startswith('log10_'):
                    continue

                val = clean_prop(param_data.PropertyValue)

                if isinstance(val, str):
                    val = clean_equation(val, object_type)

                    check = val.split('.')
                    if len(check) == 2 and check[1] == prop:
                        # This looks like a self-referential relative value?
                        # E.g., x.Param(y) = x.Param
                        # So just skip it??
                        # Any calls to x.Param(y) will be routed to x.Param
                        # by default anyway if the y arg does nothing ...
                        continue

                if val is None or str(val) == 'None':
                    continue

                full_prop = prop + (suff or '')

                if (
                    f'{object_type}.{prop}' in str(val)
                    and f'{object_type}.{full_prop}' not in str(val)
                ):
                    continue

                unit = clean_unit(param_data.Units)

                if suff:
                    filter_props.append(full_prop)

                param = obj_params.setdefault(full_prop, {
                    'value': val,
                    'unit': unit
                })
                chem = param_data.SpecificChemical
                if chem:
                    param.setdefault('for_chemicals', []).append({
                        'target': chem,
                        'value': val,
                        'unit': unit
                    })

        for filter_name in filter_props:
            p = split_unit_suffix(filter_name)[0]
            for obj_params in objs.values():
                if filter_name not in obj_params:
                    continue
                x = obj_params.pop(filter_name, None)
                if p not in obj_params:
                    obj_params[p] = x

    return params


def parse_met_data(df_met, df_ae, df_lf):  # one time process all met weighted averages
    # THIS IS FROM ARUN
    # MAYBE DO THIS DIFFERENTLY? Is this just for Foundries?
    # Scenario-specific stuff shouldn't go here!
    # TODO Move this to default_rules.json. Directly use the keys in the mapper
    arun_met_dict = {
        'frac_time_exchange_day': 0.16225754122155972,
        'frac_time_exchange_no_rain': 0.3262149134948966,
        'frac_time_exchange_not_day': 0.18755320057229782,
        'frac_time_exchange_rain': 0.02359582829896095,
        'frac_time_rain': 0.07951431920086095,
        'wt_av_airtemperature': 280.1595898155025,
        'wt_av_allowexchange': 0.38056526683795966,
        'wt_av_cumulativerain': 0.0006524559583347348,
        'wt_av_horizontalwindspeed': 2.9321140206308054,
        'wt_av_isday': 0.43829251065306357,
        'wt_av_litterfallrate': 0.01235169116344962,
        'wt_av_mixingheight': 308.88146200993845,
        'wt_av_rain': 0.07951431920086095,
        'wt_av_winddirection': 189.88241670957274
    }
    return arun_met_dict

    df_met['dlist'] = df_met['date'].str.split('/')  # split date column into list
    df_met = df_met[df_met.dlist.str.len() == 3]  # drop rows that have less than three elements
    df_met[['Month', 'Day', 'Year']] = df_met.date.str.split("/", expand=True)
    df_met['Month'] = pd.to_numeric(df_met['Month'], errors='coerce')
    df_met['Day'] = pd.to_numeric(df_met['Day'], errors='coerce')
    df_met['Year'] = pd.to_numeric(df_met['Year'], errors='coerce')
    df_met['Hour'] = pd.to_numeric(df_met['xhour'], errors='coerce')
    df_met = df_met.loc[(df_met.Month < 13) & (df_met.Day < 32) & (df_met.Year < 2100) & (df_met.Hour < 25)]  # drop faulty

    metcol_dict = {'rain': (0, 1), 'airtemperature': (200, 373), 'horizontalwindspeed': (0, 100),
                   'winddirection': (-360, 360), 'mixingheight': (0, 1000), 'isday': (0, 1),
                   'cumulativerain': (0, 1.6)}  # k, v represent name and min-max
    for k, v in metcol_dict.items():
        df_met['metcol'] = pd.to_numeric(df_met[k], errors='coerce')
        df_met = df_met[(df_met['metcol'] <= v[1]) & (df_met['metcol'] >= v[0])]  # keep rows within min max bounds

    df_met['DT'] = list(pd.to_datetime(df_met[['Year', 'Month', 'Day', 'Hour']], errors='coerce'))
    df_met['date_delta'] = (df_met['DT'] - df_met['DT'].min()) / timedelta64(1, 'D')
    df_met['time_delta'] = df_met['date_delta'].diff()
    df_met['time_delta'] = df_met['time_delta'].shift(
        -1)  # shift up the column 1 so that applicability of met condition is aligned to duration

    # clean up non sequential dates. slow

    df_met['DT_Check'] = df_met.DT >= (df_met.DT.shift())
    df_met = df_met[df_met['DT_Check']]
    # df_met=df_met[(df_met['time_delta']<0.05)&(df_met['time_delta']>0)]# assume all observations valid for an hour since this is an hourly met file. eliminate overinfluential observations. not sure if needed but checking.
    # df_met=df_met[df_met['time_delta']>0]# assume all observations valid for an hour since this is an hourly met file. eliminate overinfluential observations. not sure if needed but checking.
    # df_met=df_met[(df_met['time_delta']<1)&(df_met['time_delta']>0)]# assume all observations valid for an hour since this is an hourly met file. eliminate overinfluential observations. not sure if needed but checking.

    # need to clean up messy met file to get reasonable averages. This shouldnt be required with a quality met file.

    met_dict = {}

    for k, v in metcol_dict.items():
        df_met['metcol'] = pd.to_numeric(df_met[k], errors='coerce')
        df_met['prod'] = df_met['metcol'] * df_met['time_delta']
        wt_ave = df_met['prod'].sum() / df_met['time_delta'].sum()
        met_dict['wt_av_' + k] = wt_ave
    df_met['rain'] = pd.to_numeric(df_met['rain'], errors='coerce')
    df_met['is_rain'] = [1 if x > 0 else 0 for x in df_met['rain']]
    df_met['raintime'] = df_met['is_rain'] * df_met['time_delta']
    rain_frac_time = df_met['raintime'].sum() / df_met['time_delta'].sum()
    met_dict['frac_time_rain'] = rain_frac_time
    # met_dict['wt_av_rain']=rain_frac_time # overwrite wt_av_rain with rain_frac_time (superior method, i think)

    # process AE file ## has unusual data column header -- not interfered with original data. Ignored hour resolution.
    df_ae['dlist'] = df_ae['##date'].str.split('/')  # split date column into list
    df_ae = df_ae[df_ae.dlist.str.len() == 3]  # drop rows that have less than three elements
    df_ae[['Month', 'Day', 'Year']] = df_ae['##date'].str.split("/", expand=True)
    df_ae['Month'] = pd.to_numeric(df_ae['Month'], errors='coerce')
    df_ae['Day'] = pd.to_numeric(df_ae['Day'], errors='coerce')
    df_ae['Year'] = pd.to_numeric(df_ae['Year'], errors='coerce')
    df_ae = df_ae.loc[(df_ae.Month < 13) & (df_ae.Day < 32) & (df_ae.Year < 2100)]  # drop faulty

    df_ae['DT'] = list(pd.to_datetime(df_ae[['Year', 'Month', 'Day']], errors='coerce'))
    df_ae['date_delta'] = (df_ae['DT'] - df_ae['DT'].min()) / timedelta64(1, 'D')
    df_ae['time_delta'] = df_ae['date_delta'].diff()
    df_ae['time_delta'] = df_ae['time_delta'].shift(
        -1)  # shift up the column 1 so that applicability of met condition is aligned to duration

    df_ae['ae'] = pd.to_numeric(df_ae['allowexchange'], errors='coerce')
    df_ae['prod'] = df_ae['ae'] * df_ae['time_delta']
    wt_ave = df_ae['prod'].sum() / df_ae['time_delta'].sum()
    met_dict['wt_av_allowexchange'] = wt_ave

    df_met = df_met.merge(df_ae[['DT', 'ae']], how='left', on='DT', indicator=True)  # merge in AE

    first_ind = df_met.loc[df_met['_merge'] == 'both'].index[0]  # index first date in AE file
    if first_ind != 0:  # if the first value in the ae file is greater than the first date in the met file assume the opposite condition is true
        first_ae_val = df_met.loc[first_ind, 'ae']  # first ae value
        if first_ae_val == 1:
            df_met.loc[0, 'ae'] = 0
        else:
            df_met.loc[0, 'ae'] = 1

    df_met.ae.fillna(value=pd.NA, inplace=True)  # fill None values with nan

    df_met['ae'].fillna(method='ffill', inplace=True)  # fill nan values with previous non nan value

    df_met['exch_no_rain'] = df_met['ae'] * (1 - df_met['is_rain'])
    df_met['exch_rain'] = df_met['ae'] * df_met['is_rain']
    df_met['exchnoraintime'] = df_met['exch_no_rain'] * df_met['time_delta']
    df_met['exchraintime'] = df_met['exch_rain'] * df_met['time_delta']
    exch_no_rain_frac_time = df_met['exchnoraintime'].sum() / df_met['time_delta'].sum()
    exch_rain_frac_time = df_met['exchraintime'].sum() / df_met['time_delta'].sum()

    met_dict['frac_time_exchange_no_rain'] = exch_no_rain_frac_time
    met_dict['frac_time_exchange_rain'] = exch_rain_frac_time

    ### Compute interaction between isday and allow exchange.
    df_met = df_met
    df_met['isday'] = pd.to_numeric(df_met['isday'], errors='coerce')
    df_met = df_met.loc[(df_met.isday == 1) | (df_met.isday == 0)]  # keep only valid isday data
    df_met['ae_isday'] = df_met['ae'] * df_met.isday
    df_met['aeisdaytime'] = df_met['ae_isday'] * df_met['time_delta']
    exch_day_frac_time = df_met['aeisdaytime'].sum() / df_met['time_delta'].sum()
    met_dict['frac_time_exchange_day'] = exch_day_frac_time

    df_met['ae_notday'] = df_met['ae'] * (1 - df_met.isday)
    df_met['aenotdaytime'] = df_met['ae_notday'] * df_met['time_delta']
    exch_not_day_frac_time = df_met['aenotdaytime'].sum() / df_met['time_delta'].sum()
    met_dict['frac_time_exchange_not_day'] = exch_not_day_frac_time

    # process LF file
    df_lf['dlist'] = df_lf['##date'].str.split('/')  # split date column into list
    df_lf = df_lf[df_lf.dlist.str.len() == 3]  # drop rows that have less than three elements
    df_lf[['Month', 'Day', 'Year']] = df_lf['##date'].str.split("/", expand=True)
    df_lf['Month'] = pd.to_numeric(df_lf['Month'], errors='coerce')
    df_lf['Day'] = pd.to_numeric(df_lf['Day'], errors='coerce')
    df_lf['Year'] = pd.to_numeric(df_lf['Year'], errors='coerce')
    # df_lf['Hour']=pd.to_numeric(df_lf['hour'], errors='coerce')
    # df_lf=df_lf.loc[(df_lf.Month<13) & (df_lf.Day<32) & (df_lf.Year<2100)&(df_lf.Hour<25)] # drop faulty
    df_lf = df_lf.loc[(df_met.Month < 13) & (df_lf.Day < 32) & (df_lf.Year < 2100)]  # drop faulty

    df_lf['DT'] = list(pd.to_datetime(df_lf[['Year', 'Month', 'Day']], errors='coerce'))
    # df_met['DT']=list(pd.to_datetime(df_met[['Year', 'Month', 'Day','Hour']],errors='coerce'))
    df_lf['date_delta'] = (df_lf['DT'] - df_lf['DT'].min()) / timedelta64(1, 'D')
    df_lf['time_delta'] = df_lf['date_delta'].diff()
    df_lf['time_delta'] = df_lf['time_delta'].shift(
        -1)  # shift up the column 1 so that applicability of met condition is aligned to duration

    df_lf['lf'] = pd.to_numeric(df_lf['litterfallrate'], errors='coerce')
    df_lf['prod'] = df_lf['lf'] * df_lf['time_delta']
    wt_ave = df_lf['prod'].sum() / df_lf['time_delta'].sum()
    met_dict['wt_av_litterfallrate'] = wt_ave
    # met_dict['wt_av_litterfallrate']=0.0745 # fix
    # met_dict['wt_av_allowexchange']=5/12

    return met_dict

ILLEGAL_NAME_CHARS = re.compile('[^0-9a-zA-Z]+')


def safe_name(name):
    if not isinstance(name, str):
        return name
    try:
        name = float(name)
        return name
    except Exception:
        pass

    name = ILLEGAL_NAME_CHARS.sub('_', name)
    name = do_replacements(name, GLOBAL_REPLACE)
    return name


def clean_compartment_name(name):
    name = name.replace(' - ', '_').replace(' / ', '_')
    name = name.replace('-', '_').replace('/', '_')
    name = name.strip().replace(' ', '_')
    name = '_'.join(name.split('_'))  # remove multiple __ in a row
    return name


VAR_SPLITTER = '______'

GLOBAL_REPLACE = {
    'Constants': 'environment',
    'constants': 'environment',
    'containingScenario': 'environment',

    'Chemical.': 'chemical.',
    'currentChemical.': 'chemical.',
    'Compartment.': 'compartment.',
    'compartment.Chemical.UseInputCharacteristicDepth_0_MeansNo_ElseYes': 'chemical.UseInputCharacteristicDepth_0_MeansNo_ElseYes',
    'compartment.Chemical.': f'compartment{VAR_SPLITTER}chemical.',  # noqa

    'containingVolumeElement.Area': 'compartment.volume_element.area',
    'containingVolumeElement.': 'compartment.volume_element.',

    'Min(': 'min(',
    'Max(': 'max(',
    'ln(': 'math.log(',
    'log10(': 'math.log10(',
    'sqrt(': 'math.sqrt(',
    'exp(': 'math.exp(',
    'Exp(': 'math.exp(',

    '<Unset>': 'None',
    'Unset': 'None',
    '"Unset"': 'None',

    'cumulativeRain': 'CumulativeRain',
    'molecularWeight': 'MolecularWeight',
    'NumberofZooplanktonpersquaremeter': 'NumberofZooplanktonPerSquareMeter',
    'BoundaryLayerThicknessbelowWater': 'BoundaryLayerThicknessBelowWater',
    'SuspendedSedimentconcentration': 'SuspendedSedimentConcentration',
    'AlgaeDensityinWaterColumn': 'AlgaeDensityInWaterColumn',
    'porosity': 'Porosity',
    'GenericDenominatorforCalculatingFractioninPhases': (
        'GenericDenominatorForCalculatingFractionInPhases'
    ),
    'organiccarboncontent': 'OrganicCarbonContent',
    'fractionsand': 'FractionSand',
    'NumberofFishpersquaremeter': 'NumberOfFishPerSquareMeter',
    'NumberofFishperSquareMeter': 'NumberOfFishPerSquareMeter',
    'totalMass': 'TotalMass',
    'Surfsoil': 'SurfSoil',
    'Halflife': 'HalfLife',
    'isFlowing': 'IsFlowing',
    'D_pureair': 'D_PureAir',
    'D_purewater': 'D_PureWater',
    'D_Purewater': 'D_PureWater',
    'FractionMass_vapor': 'FractionMass_Vapor',
    'fractionmass_dissolved': 'FractionMass_Dissolved',
    'fractionmass_sorbed': 'FractionMass_Sorbed',
    'volumefraction_colloid': 'VolumeFraction_Colloid',
    'VolumeFraction_colloid': 'VolumeFraction_Colloid',
    'volumeFraction_colloid': 'VolumeFraction_Colloid',
    'volumefraction_algae': 'VolumeFraction_Algae',
    'VolumeFraction_algae': 'VolumeFraction_Algae',
    'volumeFraction_algae': 'VolumeFraction_Algae',
    'volumefraction_vapor': 'VolumeFraction_Vapor',
    'VolumeFraction_vapor': 'VolumeFraction_Vapor',
    'volumeFraction_vapor': 'VolumeFraction_Vapor',
    'volumefraction_liquid': 'VolumeFraction_Liquid',
    'VolumeFraction_liquid': 'VolumeFraction_Liquid',
    'volumeFraction_liquid': 'VolumeFraction_Liquid',
    'volumefraction_solid': 'VolumeFraction_Solid',
    'VolumeFraction_solid': 'VolumeFraction_Solid',
    'volumeFraction_solid': 'VolumeFraction_Solid',
    'volumeParticlePerAreaLeaf': 'VolumeParticlePerAreaLeaf',
    'WetVolumeperArea': 'WetVolumePerArea',
    'Z_algae': 'Z_Algae',
    'z_liquid': 'Z_Liquid',
    'Z_vapor': 'Z_Vapor',
    'z_vapor': 'Z_Vapor',
    'Z_pureair': 'Z_PureAir',
    'Z_pureAir': 'Z_PureAir',
    'Z_colloid': 'Z_Colloid',
    'Z_purewater': 'Z_PureWater',
    'Z_total': 'Z_Total',
    'Depth_times_gamma': 'Depth_times_Gamma',
    'conc_colloid': 'conc_Colloid',
    'Kd_colloid': 'Kd_Colloid',
    'rho_colloid': 'rho_Colloid',
    'Depurationrate': 'DepurationRate',
    'Fractionofareaavailableforerosion': 'FractionofAreaAvailableforErosion',
    'FractionOrganicMatteronParticulates': 'FractionOrganicMatterOnParticulates',

    '.Height': '.height',

    'self.Volume': 'compartment.Volume',
    'self.Height': 'compartment.height',
    'self.Area': 'compartment.area',
    'compartment.Volume': 'compartment.Volume',
    'compartment.Height': 'compartment.height',
    'compartment.Area': 'compartment.area',
    '.DistanceBetweenMidpoints': '.volume_element.midpoint_distance',

    'Algorithm.': 'algorithm.',

    'theLink.FractionSpecificcompartmentDiet': '1',
    'TheLink.FractionSpecificcompartmentDiet': '1',
    'theLink.': 'link.',
    'TheLink.': 'link.',
    'TheLink.InterfacialArea': 'sender.interface_with(receiver)',  # noqa
    'Thelink.InterfacialArea': 'sender.interface_with(receiver)',  # noqa
    'TheLink.RechargeRate': 'sender.RechargeRate',
    'Thelink.RechargeRate': 'sender.RechargeRate',

    'SendingChemical.': 'chemical.',
    'SendingCompartment.Chemical.': f'sender{VAR_SPLITTER}chemical.',  # noqa
    'sendingCompartment.Chemical.': f'sender{VAR_SPLITTER}chemical.',  # noqa
    'Sendingcompartment.Chemical.': f'sender{VAR_SPLITTER}chemical.',  # noqa
    'sendingcompartment.Chemical.': f'sender{VAR_SPLITTER}chemical.',  # noqa
    'ReceivingCompartment.Volume': 'receiver.Volume',
    'receivingCompartment.Volume': 'receiver.Volume',
    'Receivingcompartment.Volume': 'receiver.Volume',
    'receivingcompartment.Volume': 'receiver.Volume',
    'SendingCompartment.Volume': 'sender.Volume',
    'sendingCompartment.Volume': 'sender.Volume',
    'Sendingcompartment.Volume': 'sender.Volume',
    'sendingcompartment.Volume': 'sender.Volume',
    'ReceivingCompartment.Area': 'receiver.area',
    'Receivingcompartment.Area': 'receiver.area',
    'receivingcompartment.Area': 'receiver.area',
    'receivingCompartment.Area': 'receiver.area',
    'SendingCompartment.Area': 'sender.area',
    'Sendingcompartment.Area': 'sender.area',
    'sendingcompartment.Area': 'sender.area',
    'sendingCompartment.Area': 'sender.area',
    'ReceivingCompartment.Depth': 'receiver.depth',
    'Receivingcompartment.Depth': 'receiver.depth',
    'receivingcompartment.Depth': 'receiver.depth',
    'receivingCompartment.Depth': 'receiver.depth',
    'SendingCompartment.Depth': 'sender.depth',
    'Sendingcompartment.Depth': 'sender.depth',
    'sendingcompartment.Depth': 'sender.depth',
    'sendingCompartment.Depth': 'sender.depth',
    'ReceivingCompartment.': 'receiver.',
    'receivingCompartment.': 'receiver.',
    'Receivingcompartment.': 'receiver.',
    'receivingcompartment.': 'receiver.',
    'SendingCompartment.': 'sender.',
    'sendingCompartment.': 'sender.',
    'Sendingcompartment.': 'sender.',
    'sendingcompartment.': 'sender.',
    'ReceivingCompartment.Chemical.': f'receiver{VAR_SPLITTER}chemical.',  # noqa
    'receivingCompartment.Chemical.': f'receiver{VAR_SPLITTER}chemical.',  # noqa
    'Receivingcompartment.Chemical.': f'receiver{VAR_SPLITTER}chemical.',  # noqa
    'receivingcompartment.chemical.': f'receiver{VAR_SPLITTER}chemical.',  # noqa
    'Receivingchemical.': f'receiver{VAR_SPLITTER}chemical.',  # noqa
    'ReceivingChemical.': f'receiver{VAR_SPLITTER}chemical.',  # noqa
    'link.': f'receiver{VAR_SPLITTER}sender.',

    'Fractionofareaavailableforverticaldiffusion': 'FractionofAreaAvailableforVerticalDiffusion',

    'MassTransferCoefficientonAirSideofAirSoilBoundary': 'MassTransferCoefficientOnAirSideofAirSoilBoundary',

    'SendingwithinCompositeCompartment': 'SendingWithinCompositeCompartment',
    'sendingWithinCompositeCompartment': 'SendingWithinCompositeCompartment',
    'sendingwithincompositecompartment': 'SendingWithinCompositeCompartment',

    'withinCompositeCompartment': 'WithinCompositeCompartment',
    'WithinCompositeCompartment': 'WithinCompositeCompartment',
    'withincompositecompartment': 'WithinCompositeCompartment',

    'withinContainingVolumeElement': 'WithinContainingVolumeElement',
    'WithinContainingVolumeElement': 'WithinContainingVolumeElement',
    'withincontainingvolumeelement': 'WithinContainingVolumeElement',

    'LitterfallRate': 'LitterFallRate',
    'FractionofTotalErosion': 'FractionOfTotalErosion',
    'FractionofTotalRunoff': 'FractionOfTotalRunoff'
}


def do_replacements(val, replacements):
    # Replace longest keys first to avoid substring issues
    keys = sorted(list(replacements), key=lambda x: len(x))
    for k in reversed(keys):
        v = replacements[k]
        val = val.replace(str(k), str(v))
    return val


def clean_prop(prop, custom_replace={}):
    if prop is None or pd.isna(prop):
        return None

    # We need to eliminate [[ and ]] in the beginning and end of some property values that were probably used by legacy
    # code to identify beginning and end of the property value string
    if str(prop).startswith("[[") and \
            str(prop).endswith("]]"):
        prop = str(prop).replace("[[", "").replace("]]", "")

    val = str(prop).strip()
    try:
        val = float(val)
        return val
    except ValueError:
        val = str(prop).strip()  # Reset

    if val.lower() == 'true':
        return True
    if val.lower() == 'false':
        return False

    replacements = dict(GLOBAL_REPLACE)
    # replacements.update({k: '' for k in UNIT_SUFFIXES})
    if custom_replace:
        replacements.update(custom_replace)

    val = do_replacements(val, replacements)

    val = hacky_value_cleaning(val)

    return val


def hacky_value_cleaning(val):
    # HACKS

    if val.lower() in ['area', 'height', 'volume']:
        return val.lower()

    val = val.replace('volume_element.volumeM', 'VolumeM')
    val = val.replace('volume_element.volumeF', 'VolumeF')
    val = val.replace('math.math.', 'math.')

    for x in ['receiver', 'sender', 'compartment']:
        val = val.replace(
            f'.volume_element.midpoint_distance({x})',
            f'.volume_element.midpoint_distance({x}.volume_element)'
        )

    return val


UNIT_REPLACEMENTS = {
    'm2': 'm^2',
    'm3': 'm^3',
    'degree C': 'degC',
    'degrees C': 'degC',
    'degree K': 'K',
    'degrees K': 'K',
    'mole chemical': 'mole[chemical]',
    '#': '',
    '#/': '1/',
    'Boolean': '',
    'N/A': '',
    'unitless': '',
    'unitless (wet wt)': ''
}


def clean_unit(unit, custom_replace={}):
    unit_replace = dict(UNIT_REPLACEMENTS)
    if custom_replace:
        unit_replace.update(custom_replace)

    clean = clean_prop(unit, custom_replace=unit_replace)

    if not isinstance(clean, str):
        return clean  # No more cleaning

    for word, repl in [('-', ' * ')]:
        if word not in clean:
            continue
        temp = clean.split(word)
        clean = []
        for el in temp:
            clean.append(')/('.join(el.split('/')))
        clean = '(' + repl.join(clean) + ')'

    for word, repl in [(' per ', ' / ')]:
        if word not in clean:
            continue
        temp = clean.split(word)
        clean = []
        for el in temp:
            clean.append('(' + el + ')')
        clean = '(' + repl.join(clean) + ')'

    clean = hacky_unit_cleaning(clean)

    return clean


def hacky_unit_cleaning(val):
    # HACKS

    val = val.replace('[um^2  *  day  *  nmol]', 'um^2  *  day  *  nmol')
    val = val.replace(' [m/m]', '[m/m]')

    if (
        val.startswith('degrees clockwise')
        or val.startswith('degrees counterclockwise')
    ):
        return None

    return val


UNIT_SUFFIXES = {
    '_mg_L': 'mg/L',
    '_mg_m3': 'mg/m^3',
    '_g_per_kg': 'g/kg',
    '_g_per_kg_UserSupplied': 'g/kg',
    '_g_um3': 'g/um^3',
    '_g_cm3': 'g/cm^3',
    '_g_m2_day': 'g/m^2/day',
    '_g_m3': 'g/m^3',
    '_g_per_m3': 'g/m^3',
    '_g_per_m3_UserSupplied': 'g/m^3',
    '_g_per_L': 'g/L',
    '_g_per_L_UserSupplied': 'g/L',
    '_g_L': 'g/L',
    '_kg_m2': 'kg/m^2',
    '_kg_m2_day': 'kg/m^2/day',
    '_kg_m3': 'kg/m^3',
    '_cm2_per_s': 'cm^2/s',
    '_cm2_per_sec': 'cm^2/s',
    '_m': 'm',
    '_m_day': 'm/day',
    '_m_per_day': 'm/day',
    '_m2_s': 'm^2/s',
    '_m2_per_s': 'm^2/s',
    '_m2_per_sec': 'm^2/s',
    '_m3_m2_day': 'm^3/m^2/day',
    '_C': 'degC',
    '_F': 'degF',
    '_K': 'K',
    '_per_year': '1/year'
}


def split_unit_suffix(val):
    if '_' not in val:
        return val, None

    if val.endswith(')'):
        temp = val.rsplit('(', 1)
        stripped = temp[0]
        args = '(' + temp[1]
    else:
        stripped = val
        args = ''

    unit_suff = None
    for suff in sorted(list(UNIT_SUFFIXES), key=lambda x: len(x)):
        if stripped.endswith(suff):
            stripped = stripped[:-len(suff)]
            unit_suff = suff
            break

    return stripped + args, unit_suff


AGGREGATE_FUNCTIONS = {
    'SumOf': 'sum'
}

COMPOSITE_COMPARTMENT_FUNCTIONS = {
    'SendingWithinCompositeCompartment': 'sender',
    'WithinCompositeCompartment': 'self',
    'WithinContainingVolumeElement': 'self'
}

def clean_equation(equation, object_type=None):
    equation = str(equation).strip()
    eq = deconstruct_equation(equation)
    args = find_arguments(equation, combine_partial_args=False)

    cleaned = []
    for el in eq:
        if el == '!':
            el = ' not '
        cleaned.append(el)
        if '_' not in el:
            continue
        if el not in args:
            continue

        clean = el

        if VAR_SPLITTER in clean:
            temp = el.split(VAR_SPLITTER)
            clean = temp[-1] + f'({", ".join(temp[:-1])})'

        temp = split_unit_suffix(clean)
        if temp[1] is not None:
            clean = temp[0] + f'.to("{UNIT_SUFFIXES[temp[1]]}")'
        cleaned[-1] = clean

    cleaned = ' '.join(cleaned)

    for brackets in ['..', '()', '[]', '{}']:
        cleaned = cleaned.replace(f'{brackets[0]} ', brackets[0])
        cleaned = cleaned.replace(f' {brackets[1]}', brackets[1])

    # the above introduces a problem for min(
    # this should fix it
    if "min (" in cleaned:
        cleaned = cleaned.replace("min (", "min(")

    for agg_expression in AGGREGATE_FUNCTIONS:
        if f'volumeelement{agg_expression.lower()}' in cleaned.lower():
            cleaned = convert_property_aggregates(cleaned, agg_expression)

    if 'linkedcompartment' in cleaned.lower():
        cleaned = convert_linked_compartments(cleaned)

    # Must be done AFTER normal linkedcompartment replacement,
    # since this hijacks that functionality
    for k, v in COMPOSITE_COMPARTMENT_FUNCTIONS.items():
        if k.lower() in cleaned.lower():
            cleaned = cleaned.replace(k, 'linkedCompartment')
            cleaned = convert_linked_compartments(
                cleaned, from_compartment=v, restrict_parcel=True
            )

    if '?' in cleaned and ':' in cleaned:
        cleaned = convert_ternary(cleaned)

    cleaned = unit_conversions_to_pint(cleaned)

    if 'log10_' in cleaned:
        cleaned = cleaned.replace(
            'chemical.log10_K_ow', 'math.log10(chemical.K_ow)'
        )
        cleaned = cleaned.replace(
            'chemical.log10_K_OA', 'math.log10(chemical.K_OA)'
        )

    cleaned = hacky_equation_cleaning(cleaned, object_type)

    return cleaned


def convert_property_aggregates(expression, agg_expression):
    agg_func = AGGREGATE_FUNCTIONS[agg_expression]

    cleaned = expression
    if f'VolumeElement{agg_expression}' not in cleaned:
        if f'volumeelement{agg_expression.lower()}' in cleaned:
            cleaned = cleaned.replace(
                f'volumeelement{agg_expression.lower()}',
                f'VolumeElement{agg_expression}'
            )
        else:
            return cleaned

    temp = cleaned.split(f'ingVolumeElement{agg_expression}[')
    cleaned = [temp[0]]
    for el in temp[1:]:
        if ']' not in el:
            raise AssertionError
        suff = ''
        if '[' in el:
            el = el.rsplit('[', 1)
            suff = el[1]
            if suff:
                suff = f'[{suff}'
            el = el[0]

        el = el.rsplit(']', 1)
        suff = el[1] + suff
        suff = suff.split(' ', 1)
        if len(suff) > 1:
            nxt = suff[1]
        else:
            nxt = ''
        suff = suff[0]

        paren = ''
        while suff.endswith(')'):
            paren += ')'
            suff = suff[:-1]

        if suff.lower() in ['.area', '.depth']:
            cleaned.append(f'{suff.lower()}{paren} {nxt}')
            continue

        m = clean_compartment_name(el[0].split('|')[-1])
        if m == 'Surface_Soil_Default':
            m = 'Surface_Soil'
        m = MEDIA_MAP.get(m, m)
        if m == 'Leaf':
            m = '$Leaf'
        c = suff.lower().startswith('.chemical.')
        if c:
            suff = '.' + suff.split('emical.', 1)[-1]
        cleaned.append(f'.agg("{agg_func}", "{suff[1:]}",')
        if c:
            cleaned[-1] += ' chemical=chemical,'
        cleaned[-1] += f' compartment_media="{m}"){paren} {nxt}'

    cleaned = 'er.volume_element'.join(cleaned).strip()

    return cleaned


def convert_linked_compartments(
    expression, from_compartment='compartment', restrict_parcel=False
):
    if 'linkedCompartment' not in expression:
        if 'linkedcompartment' in expression:
            expression = expression.replace(
                'linkedcompartment', 'linkedCompartment'
            )
        elif 'LinkedCompartment' in expression:
            expression = expression.replace(
                'LinkedCompartment', 'linkedCompartment'
            )
        else:
            return expression
    temp = expression.split('linkedCompartment[')
    cleaned = [temp[0]]
    for el in temp[1:]:
        if ']' not in el:
            raise AssertionError
        suff = ''
        if '[' in el:
            el = el.rsplit('[', 1)
            suff = el[1]
            if suff:
                suff = f'[{suff}'
            el = el[0]

        el = el.rsplit(']', 1)
        suff = el[1] + suff
        suff = suff.split(' ', 1)
        if len(suff) > 1:
            nxt = suff[1]
        else:
            nxt = ''
        suff = suff[0]

        paren = ''
        while suff.endswith(')'):
            paren += ')'
            suff = suff[:-1]

        if suff.lower() in ['.area', '.depth']:
            cleaned.append(f'{suff.lower()}{paren} {nxt}')
            continue

        m = clean_compartment_name(el[0].split('|')[-1])
        m = MEDIA_MAP.get(m, m)
        if m == 'Leaf':
            m = '$Leaf'
        compartment_finder = f'.linked_compartments(media="{m}"'
        if restrict_parcel:
            compartment_finder += ', same_parcel=True'
        cleaned.append(f'{compartment_finder})[0]{suff}{paren} {nxt}')
    return from_compartment.join(cleaned)


def convert_ternary(expression):
    # if no if condition, return the expression
    question_mark = expression.find('?')
    if (question_mark < 0):
        return expression
    colon = expression.find(':', question_mark)
    if (colon < 0):
        return expression
    
    # some expressions are uncleaned and are enclosed in "(" and ")"
    if (
        expression.startswith("(")
        and expression.endswith(")")
        and expression.count("(") == 1
        and expression.count(")") == 1
    ):
        expression = expression[1:-1]  # Drop enclosing chars
        question_mark = question_mark - 1  # need to update position of "?"

    # extract outer if condition and expression parts (True & False)
    condition = expression[:question_mark]
    condition = condition.replace('&&', 'and').replace('||', 'or').strip()

    parts = expression[(question_mark + 1):].strip()

    # while looking in pairs, find the location where the colon occurs
    # before the question mark
    question_mark = parts.find('?')
    colon = parts.find(':')
    while ((question_mark >= 0) and (colon >= 0)) and (question_mark < colon):
        question_mark = parts.find('?', question_mark + 1)
        colon = parts.find(':', colon + 1)

    # extract True and False parts
    if_true_val = f'{parts[0:colon].strip()}'
    if_false_val = f'{parts[(colon + 1):len(parts)].strip()}'

    return (
        f'({convert_ternary(if_true_val)}) if {condition}'
        f' else ({convert_ternary(if_false_val)})'
    )


def unit_conversions_to_pint(expression):
    cleaned = expression

    if '1000.0' in cleaned:
        masses = [
            'compartment.BW'
        ]
        for name in masses:
            cleaned = cleaned.replace(
                f'1000.0 * {name}', f'{name}.to("g")'
            )
            cleaned = cleaned.replace(
                f'1000.0*{name}', f'{name}.to("g")'
            )

    if '"K"' in cleaned:
        cleaned = cleaned.replace(
            '.to("K")-273.15', '.to("degC")'
        )
        cleaned = cleaned.replace(
            '.to("K") - 273.15', '.to("degC")'
        )
        cleaned = cleaned.replace(
            '.to("K")-273', '.to("degC")'
        )
        cleaned = cleaned.replace(
            '.to("K") - 273', '.to("degC")'
        )

    if '"mg/L"' in cleaned:
        cleaned = cleaned.replace(
            '.to("mg/L") <', '.to("mg/L").magnitude <'
        )
    if '"mg / L"' in cleaned:
        cleaned = cleaned.replace(
            '.to("mg / L") <', '.to("mg / L").magnitude <'
        )

    for x in ['SedimentDepositionRate', 'SedimentResuspensionRate']:
        if x in cleaned:
            for c in [
                'compartment', 'sender', 'receiver',
                'compartment.linked_compartments(media="Surface_Water")[0]'
            ]:
                for unit in ['m^3/m^2/day', 'm^3 / m^2 / day']:
                    cleaned = cleaned.replace(
                        f'{c}.{x}.to("{unit}")',
                        f'({c}.{x} / {c}.rho)'
                    )

    for x in ['AlgaeSedimentationRate']:
        if x in cleaned:
            for c in [
                'compartment', 'sender', 'receiver',
                'compartment.linked_compartments(media="Surface_Water")[0]'
            ]:
                for unit in ['m^3/m^2/day', 'm^3 / m^2 / day']:
                    cleaned = cleaned.replace(
                        f'{c}.{x}.to("{unit}")',
                        f'({c}.{x} / {c}.AlgaeDensity)'
                    )

    return cleaned


def hacky_equation_cleaning(val, object_type):
    # HACKS

    if val.endswith('.Volume'):
        val = val[:-len('.Volume')] + '.volume'

    val = val.replace('.Volume ', '.volume ')
    val = val.replace('.Volume)', '.volume)')

    if '.Porosity' in val:
        for x in ['chemical', 'self']:
            val = val.replace(
                f'compartment.{x}.Porosity', f'{x}.Porosity(compartment)'
            )

    if object_type == 'compartment':
        for x in ['sender', 'receiver', 'compartment']:
            val = val.replace(f' {x}.', ' self.')
    elif object_type == 'chemical':
        for x in ['chemical']:
            val = val.replace(f' {x}.', ' self.')

    # This is specific for "Particles Blown off from Plant Leaf to Air (DRY)(AlgInstID_4010)"
    if " if (environment.Rain == 0 and sender.volume > 0) else 0" in val:
        val = val.replace(" if (environment.Rain == 0 and sender.volume > 0) else 0", "")

    # These are steady state meteorology hacks
    # to account for rain being static rather than time-dependent value
    # Below was specific to foundries. IGNORE.
    # if (
    #     (
    #         "sender.AllowExchange_forOther" in val
    #         or "receiver.AllowExchange_forOther" in val
    #     )
    #     and "ParticleVolumetricWetDepositionRate" in val
    # ):
    #     val = val.replace("sender.AllowExchange_forOther", "0.02359582829896095")
    #     val = val.replace("receiver.AllowExchange_forOther", "0.02359582829896095")
    # if (
    #     (
    #         "sender.AllowExchange_forOther" in val
    #         or "receiver.AllowExchange_forOther" in val
    #     )
    #     and "ParticleVolumetricDRYDepositionRate" in val
    # ):
    #     val = val.replace("sender.AllowExchange_forOther", "0.3262149134948966")
    #     val = val.replace("receiver.AllowExchange_forOther", "0.3262149134948966")

    return val


def transform_coordinates_to_decimal(poly):
    # Create a transformation object from x to WGS84
    proj = 'PROJCS["WGS_1984_UTM_Zone_16N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-87.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'
    from_crs = CRS.from_wkt(proj)
    to_crs = CRS.from_epsg(4326)
    transformer = Transformer.from_crs(from_crs, to_crs)

    # Create Dictionary of Polygons and Coordinates
    decimal_poly = []
    for coord in poly:
        transformed_point = transformer.transform(coord[0], coord[1])
        decimal_poly.append((transformed_point[1], transformed_point[0]))

    if decimal_poly[0][0] != decimal_poly[decimal_poly.__len__()-1][0] or \
            decimal_poly[0][1] != decimal_poly[decimal_poly.__len__()-1][1]:
        decimal_poly.append((decimal_poly[0][0], decimal_poly[0][1]))

    return decimal_poly
