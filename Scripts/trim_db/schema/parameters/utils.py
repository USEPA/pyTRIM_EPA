import ast
import math
import operator as op
import numpy as np
import pint
import re
import simpleeval
from functools import wraps

__all__ = ['ureg', 'as_quantity', 'is_number']


ureg = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)

EMPERICALLY_DIMENSIONLESS = [
    '[length] ** 3 / [mass]'
]

ALLOW_ZERO_DIVISION = True
EMPERICAL_ZERO_DIVISION = 0

BRACKETED = re.compile('\[.*?\]')  # noqa
NOEXPOSYMBL = re.compile('[a-zA-Z]\d')  # noqa


def is_number(val):
    check = str(val).strip()
    if not check:
        return False
    check = check.replace('.', '').replace('-', '').replace('+', '')
    check = check.split('e')
    for part in check:
        if not part.isnumeric():
            return False
    return True


def as_quantity(val, unit=''):
    if val is None or np.isnan(val):
        return None

    unit = str(unit or '')
    if '[' in unit:
        unit = BRACKETED.sub('', unit)
    elif 'wet weight' in unit or 'dry weight' in unit:
        # TODO Better way to handle will be needed
        unit = unit.replace('wet weight', '').replace('dry weight', '')
    # TODO Better way to handle will be needed
    unit = unit.replace('(or m)/(day)', '')

    for uu in NOEXPOSYMBL.findall(unit):
        nuu = "^".join(list(uu))
        unit = unit.replace(uu, nuu)

    if not unit:
        return val

    unit = unit.split('(or ')[0].split(' or ')[0]
    while unit.count('(') > unit.count(')'):
        unit += ')'

    try:
        return val.to(unit)
    except AttributeError:
        pass

    if not is_number(val):
        raise TypeError(f'Invalid magnitude: "{val}"')
    # import tokenize
    # try:
    #     tmp = ureg(unit)
    # except tokenize.TokenError as msg:
    #     print(f"{msg} ---> {unit}")

    quantity = val * ureg(unit)

    if quantity.units == ureg.Unit(''):
        return val

    return quantity


def auto_sync_emperical_with_quantity(f):
    @wraps(f)
    def synced(a, b, strict_dimensions=False, strict_offset=False):
        if not strict_dimensions:
            if hasattr(a, 'dimensionality'):
                if a.to_base_units().to_compact().units == 'dimensionless':
                    a = a.magnitude
                elif a.dimensionality in EMPERICALLY_DIMENSIONLESS:
                    a = a.magnitude * ureg('')
            if hasattr(b, 'dimensionality'):
                if b.to_base_units().to_compact().units == 'dimensionless':
                    b = b.magnitude
                elif b.dimensionality in EMPERICALLY_DIMENSIONLESS:
                    b = b.magnitude * ureg('')
        try:
            return f(a, b)
        except pint.errors.DimensionalityError as e:
            if strict_dimensions or "'dimensionless'" not in str(e):
                raise
            if hasattr(a, 'dimensionality'):
                b = b * a.units
            elif hasattr(b, 'dimensionality'):
                a = a * b.units
            return synced(
                a, b,
                strict_dimensions=True, strict_offset=strict_offset
            )
        except pint.errors.OffsetUnitCalculusError as e:
            if strict_offset:
                raise
            unit = str(e).split('with offset unit (', 1)[-1].split(')')[0]
            unit = unit.split(', ')[0]
            if hasattr(a, 'dimensionality'):
                a = a.magnitude
            if hasattr(b, 'dimensionality'):
                b = b.magnitude
            return synced(
                a, b,
                strict_dimensions=strict_dimensions, strict_offset=True
            ) * ureg(unit)
        raise AssertionError('How did we get here??')
    return synced


@auto_sync_emperical_with_quantity
def safe_mult_quantity(a, b):
    try:
        return simpleeval.safe_mult(a, b)
    except TypeError as e:
        if 'no len()' in str(e):
            return a * b
        raise


@auto_sync_emperical_with_quantity
def safe_add_quantity(a, b):
    try:
        return simpleeval.safe_add(a, b)
    except TypeError as e:
        if 'no len()' in str(e):
            return a + b
        raise


@auto_sync_emperical_with_quantity
def safe_sub_quantity(a, b):
    return op.sub(a, b)


@auto_sync_emperical_with_quantity
def safe_div_quantity(a, b):
    try:
        return op.truediv(a, b)
    except ZeroDivisionError:
        if ALLOW_ZERO_DIVISION:
            return EMPERICAL_ZERO_DIVISION
        raise

simpleeval.MAX_POWER = 100_000_000


def safe_power_quantity(a, b):
    a_mag = a.magnitude if hasattr(a, 'dimensionality') else a
    b_mag = b.magnitude if hasattr(b, 'dimensionality') else b
    if a_mag != a:
        unit = a.units ** b_mag
    else:
        unit = ''
    return as_quantity(simpleeval.safe_power(a_mag, b_mag), unit)


def safe_gt(a, b):
    try:
        return op.gt(a, b)
    except ValueError as e:
        if 'Cannot compare Quantity' not in str(e):
            raise
        try:
            a = a.magnitude
        except AttributeError:
            pass
        try:
            b = b.magnitude
        except AttributeError:
            pass
        return op.gt(a, b)


def safe_lt(a, b):
    try:
        return op.lt(a, b)
    except ValueError as e:
        if 'Cannot compare Quantity' not in str(e):
            raise
        try:
            a = a.magnitude
        except AttributeError:
            pass
        try:
            b = b.magnitude
        except AttributeError:
            pass
        return op.lt(a, b)


def safe_ge(a, b):
    try:
        return op.ge(a, b)
    except ValueError as e:
        if 'Cannot compare Quantity' not in str(e):
            raise
        try:
            a = a.magnitude
        except AttributeError:
            pass
        try:
            b = b.magnitude
        except AttributeError:
            pass
        return op.ge(a, b)


def safe_le(a, b):
    try:
        return op.le(a, b)
    except ValueError as e:
        if 'Cannot compare Quantity' not in str(e):
            raise
        try:
            a = a.magnitude
        except AttributeError:
            pass
        try:
            b = b.magnitude
        except AttributeError:
            pass
        return op.le(a, b)


UREG_CUSTOM_OPERATORS = {
    **simpleeval.DEFAULT_OPERATORS,
    ast.Mult: safe_mult_quantity,
    ast.Add: safe_add_quantity,
    ast.Sub: safe_sub_quantity,
    ast.Div: safe_div_quantity,
    ast.Pow: safe_power_quantity,
    ast.Gt: safe_gt,
    ast.Lt: safe_lt,
    ast.GtE: safe_ge,
    ast.LtE: safe_le,
}


def exp_quantity(x):
    try:
        return math.exp(x.magnitude)
    except AttributeError:
        return math.exp(x)


def log_quantity(x, *args, **kwargs):
    try:
        return math.log(x.magnitude, *args, **kwargs)
    except AttributeError:
        return math.log(x, *args, **kwargs)


def log10_quantity(x, *args, **kwargs):
    try:
        return math.log10(x.magnitude, *args, **kwargs)
    except AttributeError:
        return math.log10(x, *args, **kwargs)


def sqrt_quantity(x, *args, **kwargs):
    return x ** 0.5

UREG_CUSTOM_FUNCTIONS = {
    **simpleeval.DEFAULT_FUNCTIONS,
    'safe_exp': exp_quantity,
    'safe_log': log_quantity,
    'safe_log10': log10_quantity,
    'safe_sqrt': sqrt_quantity
}
