import json
import types
from datetime import datetime
from decimal import Decimal
from numbers import Number

__all__ = [
    'serialize', 'jsonify',
    'serializer', 'register_serializer'
]


SERIALIZER_ATTR = '__custom_serializer'


def serialize(val):
    # Rather than spinning our own recursive serializer,
    # let the json module do it for us ...
    return json.loads(jsonify(val))


def jsonify(val):
    return json.dumps(val, default=_to_serializable)


def serializer(func=None, *args, **kwargs):
    """
    Mark this function as a serializer which can be used by _to_serializable
    """
    def decorator(f):
        if not hasattr(f, SERIALIZER_ATTR):
            setattr(f, SERIALIZER_ATTR, True)
        return staticmethod(f)
    if func:
        return decorator(func)
    else:
        return decorator


def register_serializer(
    cls, func=None, *args, auto_recursive=True, **kwargs
):
    """
    Set a function ('func') as the default serializer for a class ('cls').
    """

    def decorator(f):
        sf = serializer(f)
        setattr(cls, f.__name__, sf)
        cls.as_serializable = (
            lambda s: serialize(s) if auto_recursive else f(s)
        )

        # Additionally, if this is a model class, add some custom
        # Methods to its query_class for fetching serialized
        # models directly
        if hasattr(cls, 'query_class'):
            cls.query_class.all_serialized = (
                lambda s: serialize(s.all())
            )
            cls.query_class.get_serialized = (
                lambda s, pk: serialize(s.get(pk))
            )

        return f
    if func:
        return decorator(func)
    else:
        return decorator


def _get_attr_with_attr(obj, attr_name):
    def get_cls_attrs(cls):
        for k in vars(cls).keys():
            if not k.endswith('__'):
                yield k

    def search_cls_attrs(obj, term):
        obj_cls = type(obj)
        for p in get_cls_attrs(obj_cls):
            try:
                attr = getattr(obj, p)
                if hasattr(attr, term):
                    return attr
            except Exception:
                continue
        return None

    # Check the attributes of THIS class first
    attr = search_cls_attrs(obj, attr_name)
    if attr:
        return attr

    # And then check attributes of parent classes if we didn't find it
    for c in type(obj).__bases__:
        try:
            parent = c()
            attr = search_cls_attrs(parent, attr_name)
            if attr:
                return attr
        except Exception:
            continue

    return None


def _to_serializable(val):
    """Used by default."""
    serializer = _get_attr_with_attr(val, SERIALIZER_ATTR)
    if serializer:
        return serializer(val)
    elif isinstance(val, Decimal):
        return float(val)  # Sadly, decimals don't convert automatically
    elif isinstance(val, Number):
        return val
    elif isinstance(val, datetime):
        return val.isoformat() + "Z"
    elif isinstance(val, types.FunctionType):
        return None
    return str(val)
