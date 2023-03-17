import re
import pandas as pd
from functools import partial
from ..schema.parameters.equations import *
from pyproj import CRS, Transformer

__all__ = [
    'read_master_library',
    'safe_name', 'clean_prop', 'clean_unit',
    'UNIT_SUFFIXES',
    'split_unit_suffix',
    'clean_equation',
    'transform_coordinates_to_decimal'
]


def read_master_library(filepath):
    print(f'Reading master library from "{filepath}" ...')
    read_lib = partial(
        pd.read_csv, filepath,
        sep=';', encoding='windows-1252', low_memory=False
    )

    df_lib = read_lib(skiprows=[0], names=read_lib(nrows=0).columns.values)

    from trim_db.schema import Scenario

    constants = [
        ('g_per_kg', 1000, 'g/kg'),
        ('IdealGasConstant', 8.314, '(Pa*m^3)/(mol*K)'),
        ('kg_per_g', 1e-3, 'kg/g'),
        ('kg_per_m3_Water', 1000, 'kg/m^3'),
        ('kg_per_ug', 1e6, 'kg/ug'),
        ('L_per_m3', 1000, 'L/m^3'),
        ('m3_per_kg_Water', 1e-3, 'm^3/kg'),
        ('m3_per_L', 1e-3, 'm^3/L'),
        ('m3_per_um3', 1e-18, 'm^3/um^3'),
        ('pi', 3.14159265358979323846, None),
        ('ug_per_kg', 1e6, 'ug/kg'),
        ('um3_per_m3', 1e18, 'um^3/m^3'),
        ('vonKarmensConstant', 0.74, None),
        ('waterMeltingPoint', 273.15, 'K')
    ]
    for const in constants:
        Scenario.parameters.add(const[0], value=const[1], unit=const[2])

    parsed = parse_master_library_params(df_lib)

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
                    val = clean_equation(val)

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
    'Z_colloid': 'Z_Colloid',
    'Z_purewater': 'Z_PureWater',
    'Z_total': 'Z_Total',
    'conc_colloid': 'conc_Colloid',
    'Kd_colloid': 'Kd_Colloid',
    'rho_colloid': 'rho_Colloid',

    'self.Volume': 'compartment.volume_element.volume',
    'self.Height': 'compartment.volume_element.height',
    'compartment.Volume': 'compartment.volume_element.volume',
    'compartment.Height': 'compartment.volume_element.height',

    'Algorithm.': 'algorithm.',

    'theLink.FractionSpecificcompartmentDiet': '1',
    'TheLink.FractionSpecificcompartmentDiet': '1',
    'theLink.': 'link.',
    'TheLink.': 'link.',
    'TheLink.InterfacialArea': 'sender.volume_element.overlap_with(receiver.volume_element)',  # noqa
    'Thelink.InterfacialArea': 'sender.volume_element.overlap_with(receiver.volume_element)',  # noqa

    'SendingChemical.': 'chemical.',
    'SendingCompartment.Chemical.': f'sender{VAR_SPLITTER}chemical.',  # noqa
    'Sendingcompartment.Chemical.': f'sender{VAR_SPLITTER}chemical.',  # noqa
    'ReceivingCompartment.Chemical.': f'receiver{VAR_SPLITTER}chemical.',  # noqa
    'Receivingcompartment.Chemical.': f'receiver{VAR_SPLITTER}chemical.',  # noqa
    'SendingCompartment.Volume': 'sender.volume_element.volume',
    'Sendingcompartment.Volume': 'sender.volume_element.volume',
    'ReceivingCompartment.Volume': 'receiver.volume_element.volume',
    'Receivingcompartment.Volume': 'receiver.volume_element.volume',
    'SendingCompartment.': 'sender.',
    'Sendingcompartment.': 'sender.',
    'ReceivingCompartment.': 'receiver.',
    'Receivingcompartment.': 'receiver.',

    'link.': f'receiver{VAR_SPLITTER}sender.',
}


def clean_prop(prop, custom_replace={}):
    if prop is None or pd.isna(prop):
        return None

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
        val = val.replace(str(k), str(v))

    val = hacky_value_cleaning(val)

    return val


def hacky_value_cleaning(val):
    # HACKS

    val = val.replace('volume_element.volumeM', 'VolumeM')
    val = val.replace('volume_element.volumeF', 'VolumeF')
    val = val.replace('math.math.', 'math.')

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


def clean_equation(equation):
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

    if 'linkedcompartment' in cleaned.lower():
        cleaned = convert_linked_compartments(cleaned)

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

    cleaned = hacky_equation_cleaning(cleaned)

    return cleaned


def convert_linked_compartments(expression):
    from .environment import MEDIA_MAP

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
            el = el[0]
        el = el.rsplit(']', 1)
        suff = el[1] + suff
        m = el[0].split('|')[-1].strip().replace(' ', '_')
        m = MEDIA_MAP.get(m, m)
        cleaned.append(
            f'.linked_compartments(media="{m}")[0]{suff}'
        )
    return 'compartment'.join(cleaned)


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


def hacky_equation_cleaning(val):
    # HACKS

    # if 'math.' in val:
    #     val = val.replace('math.math.', 'math.')

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
