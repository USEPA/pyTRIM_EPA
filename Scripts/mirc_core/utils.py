import inspect
import logging
import os
from functools import wraps
from pprint import pformat


def log_vals(log, **kwargs):
    for k, v in kwargs.items():
        log.append(f'\t{k} = {pformat(v)}')


def input_units(**arg_checks):
    def decorated(f):
        param_names = list(inspect.signature(f).parameters.keys())

        @wraps(f)
        def validated(*args, **kwargs):
            # Get all inputs, and convert args to kwargs based on signature
            vals = {**kwargs}
            for i, arg in enumerate(args):
                vals[param_names[i]] = arg
            # Check all inputs in arg_checks
            for k, v in vals.items():
                if k in arg_checks:
                    if isinstance(v, list):
                        for subv in v:
                            check_units(k, subv, dimensionality=arg_checks[k])
                    else:
                        check_units(k, v, dimensionality=arg_checks[k])
            # If we succeeded, call the function
            return f(*args, **kwargs)
        return validated
    return decorated


def check_units(name, val, *, dimensionality=None):
    if val is None:
        return  # This is ok

    is_quantity = hasattr(val, 'dimensionality')

    if not dimensionality:
        if is_quantity and not val.check(''):
            raise TypeError(
                f'{name} must be unitless, but the value passed was {val}'
            )
    else:
        is_real_dimension = (
            len(dimensionality.split('/')) == 1 or  # i.e., not a relation
            len(set(dimensionality.split('/'))) > 1  # e.g., not mass/mass
        )
        if not is_real_dimension and not is_quantity:
            return  # this is ok

        if not is_quantity or not val.check(dimensionality):
            raise TypeError(
                f'{name} must be a quantity of {dimensionality},'
                f' but the value passed was {val}'
            )


def output_units(*units):
    def decorated(f):
        @wraps(f)
        def transformed(*args, **kwargs):
            result = f(*args, **kwargs)

            if isinstance(result, tuple):
                converted = []
                for i, r in enumerate(result):
                    if hasattr(r, 'dimensionality'):
                        converted.append(r.to(units[i]))
                    else:
                        converted.append(r)
                return tuple(converted)

            elif hasattr(result, 'dimensionality'):
                return result.to(units[0])

            return result
        return transformed
    return decorated


def make_logger(name):
    logger = logging.Logger(name)
    h = logging.StreamHandler()

    if os.getenv('FLASK_DEBUG'):
        h.setLevel(logging.DEBUG)
    else:
        h.setLevel(logging.INFO)

    f = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    h.setFormatter(f)

    logger.addHandler(h)

    return logger
