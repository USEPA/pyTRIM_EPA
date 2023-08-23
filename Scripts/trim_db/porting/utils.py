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
    'transform_coordinates_to_decimal'
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
        'ignore': ['wt_av_mixingheight',
                   'frac_time_rain',
                   'frac_time_exchange_no_rain',
                   'frac_time_exchange_rain',
                   'frac_time_exchange_day',
                   'frac_time_exchange_not_day']
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
    for file_type, filepath in filepaths.items():
        print(f'Reading external data: {file_type} from "{filepath}" ...')
        read_lib = partial(
            pd.read_csv, filepath,
            sep=',', encoding='windows-1252', low_memory=False
        )
        if file_type == "met_file":
            df_met = read_lib(skiprows=[0], names=[i.lower() for i in read_lib(nrows=0).columns.values])
        elif file_type == "allowexchange_file":
            df_ae = read_lib(skiprows=[0], names=[i.lower() for i in read_lib(nrows=0).columns.values])
        elif file_type == "litterfall_file":
            df_lf = read_lib(skiprows=[0], names=[i.lower() for i in read_lib(nrows=0).columns.values])

    parsed = parse_met_data(df_met, df_ae, df_lf)

    from trim_db.services import ScenarioService, CompartmentService

    scenario = ScenarioService.get(name=scenario_name)
    for k, v in parsed.items():
        if k in list(MET_DATA_MAP.get("Scenario").keys()):
            par = scenario.parameters.get(MET_DATA_MAP["Scenario"][k])
            par.value = v
        elif k in list(MET_DATA_MAP.get("Compartment").keys()):
            compartments = [c for c in scenario.compartments if c.media.isa(MET_DATA_MAP.get("Compartment")[k][1])
                            and not c.media.isa("Coniferous_Forest")]
            for comp in compartments:
                par = comp.parameters.get(MET_DATA_MAP["Compartment"][k][0])
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


def parse_met_data(df, df2, df3):  # one time process all met weighted averages
    df['dlist'] = df['date'].str.split('/')  # split date column into list
    df = df[df.dlist.str.len() == 3]  # drop rows that have less than three elements
    df[['Month', 'Day', 'Year']] = df.date.str.split("/", expand=True)
    df['Month'] = pd.to_numeric(df['Month'], errors='coerce')
    df['Day'] = pd.to_numeric(df['Day'], errors='coerce')
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Hour'] = pd.to_numeric(df['xhour'], errors='coerce')
    df = df.loc[(df.Month < 13) & (df.Day < 32) & (df.Year < 2100) & (df.Hour < 25)]  # drop faulty

    metcol_dict = {'rain': (0, 1), 'airtemperature': (200, 373), 'horizontalwindspeed': (0, 100),
                   'winddirection': (-360, 360), 'mixingheight': (0, 1000), 'isday': (0, 1),
                   'cumulativerain': (0, 1.6)}  # k, v represent name and min-max
    for k, v in metcol_dict.items():
        df['metcol'] = pd.to_numeric(df[k], errors='coerce')
        df = df[(df['metcol'] <= v[1]) & (df['metcol'] >= v[0])]  # keep rows within min max bounds

    df['DT'] = list(pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour']], errors='coerce'))
    df['date_delta'] = (df['DT'] - df['DT'].min()) / timedelta64(1, 'D')
    df['time_delta'] = df['date_delta'].diff()
    df['time_delta'] = df['time_delta'].shift(
        -1)  # shift up the column 1 so that applicability of met condition is aligned to duration

    # clean up non sequential dates. slow

    df['DT_Check'] = df.DT >= (df.DT.shift())
    df = df[df['DT_Check']]
    # df=df[(df['time_delta']<0.05)&(df['time_delta']>0)]# assume all observations valid for an hour since this is an hourly met file. eliminate overinfluential observations. not sure if needed but checking.
    # df=df[df['time_delta']>0]# assume all observations valid for an hour since this is an hourly met file. eliminate overinfluential observations. not sure if needed but checking.
    # df=df[(df['time_delta']<1)&(df['time_delta']>0)]# assume all observations valid for an hour since this is an hourly met file. eliminate overinfluential observations. not sure if needed but checking.

    # need to clean up messy met file to get reasonable averages. This shouldnt be required with a quality met file.

    met_dict = {}

    for k, v in metcol_dict.items():
        df['metcol'] = pd.to_numeric(df[k], errors='coerce')
        df['prod'] = df['metcol'] * df['time_delta']
        wt_ave = df['prod'].sum() / df['time_delta'].sum()
        met_dict['wt_av_' + k] = wt_ave
    df['rain'] = pd.to_numeric(df['rain'], errors='coerce')
    df['is_rain'] = [1 if x > 0 else 0 for x in df['rain']]
    df['raintime'] = df['is_rain'] * df['time_delta']
    rain_frac_time = df['raintime'].sum() / df['time_delta'].sum()
    met_dict['frac_time_rain'] = rain_frac_time
    # met_dict['wt_av_rain']=rain_frac_time # overwrite wt_av_rain with rain_frac_time (superior method, i think)

    # process AE file ## has unusual data column header -- not interfered with original data. Ignored hour resolution.
    df2['dlist'] = df2['##date'].str.split('/')  # split date column into list
    df2 = df2[df2.dlist.str.len() == 3]  # drop rows that have less than three elements
    df2[['Month', 'Day', 'Year']] = df2['##date'].str.split("/", expand=True)
    df2['Month'] = pd.to_numeric(df2['Month'], errors='coerce')
    df2['Day'] = pd.to_numeric(df2['Day'], errors='coerce')
    df2['Year'] = pd.to_numeric(df2['Year'], errors='coerce')
    df2 = df2.loc[(df2.Month < 13) & (df2.Day < 32) & (df2.Year < 2100)]  # drop faulty

    df2['DT'] = list(pd.to_datetime(df2[['Year', 'Month', 'Day']], errors='coerce'))
    df2['date_delta'] = (df2['DT'] - df2['DT'].min()) / timedelta64(1, 'D')
    df2['time_delta'] = df2['date_delta'].diff()
    df2['time_delta'] = df2['time_delta'].shift(
        -1)  # shift up the column 1 so that applicability of met condition is aligned to duration

    df2['ae'] = pd.to_numeric(df2['allowexchange'], errors='coerce')
    df2['prod'] = df2['ae'] * df2['time_delta']
    wt_ave = df2['prod'].sum() / df2['time_delta'].sum()
    met_dict['wt_av_allowexchange'] = wt_ave

    df = df.merge(df2[['DT', 'ae']], how='left', on='DT', indicator=True)  # merge in AE

    first_ind = df.loc[df['_merge'] == 'both'].index[0]  # index first date in AE file
    if first_ind != 0:  # if the first value in the ae file is greater than the first date in the met file assume the opposite condition is true
        first_ae_val = df.loc[first_ind, 'ae']  # first ae value
        if first_ae_val == 1:
            df.loc[0, 'ae'] = 0
        else:
            df.loc[0, 'ae'] = 1

    df.ae.fillna(value=pd.NA, inplace=True)  # fill None values with nan

    df['ae'].fillna(method='ffill', inplace=True)  # fill nan values with previous non nan value

    df['exch_no_rain'] = df['ae'] * (1 - df['is_rain'])
    df['exch_rain'] = df['ae'] * df['is_rain']
    df['exchnoraintime'] = df['exch_no_rain'] * df['time_delta']
    df['exchraintime'] = df['exch_rain'] * df['time_delta']
    exch_no_rain_frac_time = df['exchnoraintime'].sum() / df['time_delta'].sum()
    exch_rain_frac_time = df['exchraintime'].sum() / df['time_delta'].sum()

    met_dict['frac_time_exchange_no_rain'] = exch_no_rain_frac_time
    met_dict['frac_time_exchange_rain'] = exch_rain_frac_time

    ### Compute interaction between isday and allow exchange.
    df = df
    df['isday'] = pd.to_numeric(df['isday'], errors='coerce')
    df = df.loc[(df.isday == 1) | (df.isday == 0)]  # keep only valid isday data
    df['ae_isday'] = df['ae'] * df.isday
    df['aeisdaytime'] = df['ae_isday'] * df['time_delta']
    exch_day_frac_time = df['aeisdaytime'].sum() / df['time_delta'].sum()
    met_dict['frac_time_exchange_day'] = exch_day_frac_time

    df['ae_notday'] = df['ae'] * (1 - df.isday)
    df['aenotdaytime'] = df['ae_notday'] * df['time_delta']
    exch_not_day_frac_time = df['aenotdaytime'].sum() / df['time_delta'].sum()
    met_dict['frac_time_exchange_not_day'] = exch_not_day_frac_time

    # process LF file
    df3['dlist'] = df3['##date'].str.split('/')  # split date column into list
    df3 = df3[df3.dlist.str.len() == 3]  # drop rows that have less than three elements
    df3[['Month', 'Day', 'Year']] = df3['##date'].str.split("/", expand=True)
    df3['Month'] = pd.to_numeric(df3['Month'], errors='coerce')
    df3['Day'] = pd.to_numeric(df3['Day'], errors='coerce')
    df3['Year'] = pd.to_numeric(df3['Year'], errors='coerce')
    # df3['Hour']=pd.to_numeric(df3['hour'], errors='coerce')
    # df3=df3.loc[(df3.Month<13) & (df3.Day<32) & (df3.Year<2100)&(df3.Hour<25)] # drop faulty
    df3 = df3.loc[(df.Month < 13) & (df3.Day < 32) & (df3.Year < 2100)]  # drop faulty

    df3['DT'] = list(pd.to_datetime(df3[['Year', 'Month', 'Day']], errors='coerce'))
    # df['DT']=list(pd.to_datetime(df[['Year', 'Month', 'Day','Hour']],errors='coerce'))
    df3['date_delta'] = (df3['DT'] - df3['DT'].min()) / timedelta64(1, 'D')
    df3['time_delta'] = df3['date_delta'].diff()
    df3['time_delta'] = df3['time_delta'].shift(
        -1)  # shift up the column 1 so that applicability of met condition is aligned to duration

    df3['lf'] = pd.to_numeric(df3['litterfallrate'], errors='coerce')
    df3['prod'] = df3['lf'] * df3['time_delta']
    wt_ave = df3['prod'].sum() / df3['time_delta'].sum()
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
    # name = re.sub('_+', '_', name)
    name = name.replace('Halflife', 'HalfLife')
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
    'containingScenario': 'environment',

    'Chemical.': 'chemical.',
    'currentChemical.': 'chemical.',
    'Compartment.': 'compartment.',
    'compartment.Chemical.': f'compartment{VAR_SPLITTER}chemical.',  # noqa

    'containingVolumeElement.Area': 'compartment.volume_element.parcel.area',
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


    'self.Volume': 'compartment.volume_element.volume',
    'self.Height': 'compartment.volume_element.height',
    'compartment.Volume': 'compartment.volume_element.volume',
    'compartment.Height': 'compartment.volume_element.height',
    'DistanceBetweenMidpoints': '.volume_element.midpoint_distance',

    'Algorithm.': 'algorithm.',

    'theLink.FractionSpecificcompartmentDiet': '1',
    'TheLink.FractionSpecificcompartmentDiet': '1',
    'theLink.': 'link.',
    'TheLink.': 'link.',
    'TheLink.InterfacialArea': 'sender.volume_element.interface_with(receiver.volume_element)',  # noqa
    'Thelink.InterfacialArea': 'sender.volume_element.interface_with(receiver.volume_element)',  # noqa

    'SendingChemical.': 'chemical.',
    'SendingCompartment.Chemical.': f'sender{VAR_SPLITTER}chemical.',  # noqa
    'sendingCompartment.Chemical.': f'sender{VAR_SPLITTER}chemical.',  # noqa
    'Sendingcompartment.Chemical.': f'sender{VAR_SPLITTER}chemical.',  # noqa
    'sendingcompartment.Chemical.': f'sender{VAR_SPLITTER}chemical.',  # noqa
    'ReceivingCompartment.Volume': 'receiver.volume_element.volume',
    'receivingCompartment.Volume': 'receiver.volume_element.volume',
    'Receivingcompartment.Volume': 'receiver.volume_element.volume',
    'receivingcompartment.Volume': 'receiver.volume_element.volume',
    'SendingCompartment.Volume': 'sender.volume_element.volume',
    'sendingCompartment.Volume': 'sender.volume_element.volume',
    'Sendingcompartment.Volume': 'sender.volume_element.volume',
    'sendingcompartment.Volume': 'sender.volume_element.volume',
    'ReceivingCompartment.Area': 'receiver.volume_element.parcel.area',
    'Receivingcompartment.Area': 'receiver.volume_element.parcel.area',
    'receivingcompartment.Area': 'receiver.volume_element.parcel.area',
    'receivingCompartment.Area': 'receiver.volume_element.parcel.area',
    'SendingCompartment.Area': 'sender.volume_element.parcel.area',
    'Sendingcompartment.Area': 'sender.volume_element.parcel.area',
    'sendingcompartment.Area': 'sender.volume_element.parcel.area',
    'sendingCompartment.Area': 'sender.volume_element.parcel.area',
    'ReceivingCompartment.Depth': 'receiver.volume_element.depth',
    'Receivingcompartment.Depth': 'receiver.volume_element.depth',
    'receivingcompartment.Depth': 'receiver.volume_element.depth',
    'receivingCompartment.Depth': 'receiver.volume_element.depth',
    'SendingCompartment.Depth': 'sender.volume_element.depth',
    'Sendingcompartment.Depth': 'sender.volume_element.depth',
    'sendingcompartment.Depth': 'sender.volume_element.depth',
    'sendingCompartment.Depth': 'sender.volume_element.depth',
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

    # Replace longest keys first to avoid substring issues
    keys = sorted(list(replacements), key=lambda x: len(x))
    for k in reversed(keys):
        v = replacements[k]
        # Here we implement a better way to handle case insensitivity for legacy properties in order to eliminate
        # repetition of case variants of the same property
        # if str(k).lower() in str(val).lower():
        #     idx = [i for i in range(len(val)) if str(val).lower().startswith(str(k).lower(), i)]
        #     rep_k = [val[i:i + len(str(k))] for i in idx]
        #     for rk in rep_k:
        #         val = val.replace(str(rk), str(v))
        val = val.replace(str(k), str(v))

    val = hacky_value_cleaning(val)

    return val


def hacky_value_cleaning(val):
    # HACKS

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
            suff = suff.lower().replace('area', 'parcel.area')
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
            suff = suff.lower().replace('area', 'volume_element.parcel.area')
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
        f'{convert_ternary(if_true_val)} if {condition}'
        f' else {convert_ternary(if_false_val)}'
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
    if " if (environment.Rain == 0 and sender.volume_element.volume > 0) else 0" in val:
        val = val.replace(" if (environment.Rain == 0 and sender.volume_element.volume > 0) else 0", "")

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
