import json
import types
from datetime import datetime
from decimal import Decimal
from numbers import Number
from sqlalchemy.orm.exc import DetachedInstanceError
from sqlalchemy.exc import StatementError

__all__ = [
    'serialize', 'jsonify',
    'serializer', 'register_serializer'
]


SERIALIZER_ATTR = '__custom_serializer'


def serializer(func=None, *args, **kwargs):
    """
    Mark this function as a serializer which can be used by _to_serializable
    """
    def decorator(f):
        if not hasattr(f, SERIALIZER_ATTR):
            setattr(f, SERIALIZER_ATTR, True)
        return staticmethod(f)

    return decorator(func) if func else decorator


def safe_serialize(val):
    from sqlalchemy.orm import object_session
    session = object_session(val)
    if session and session.is_active is False:
        print(f"SESSION IS NOT ACTIVE!!! ROLLING BACK for {val}")
        session.rollback()
    try:
        return serialize(val)
    except Exception as e:
        return f"<serialization error: {e}>"


def serialize(val):
    # Rather than spinning our own recursive serializer,
    # let the json module do it for us ...
    try:
        return json.loads(jsonify(val))
    except (DetachedInstanceError, StatementError) as e:
        return f"<DB access error: {e}>"
    except Exception as e:
        return f"<general error: {e}>"


def jsonify(val):
    return json.dumps(val, default=_to_serializable)


def _to_serializable(val):
    """Used by default."""
    serializer = _get_attr_with_attr(val, SERIALIZER_ATTR)
    try:
        if serializer:
            return serializer(val)
    except (DetachedInstanceError, StatementError):
        return f"<unloaded or detached: {val}>"
    except Exception as e:
        return f"<error serializing {val}: {e}>"

    if isinstance(val, Decimal):
        return float(val)  # Sadly, decimals don't convert automatically
    elif isinstance(val, Number):
        return val
    elif isinstance(val, datetime):
        return val.isoformat() + "Z"
    elif isinstance(val, types.FunctionType):
        return None
    return str(val)


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
            lambda s: safe_serialize(s) if auto_recursive else f(s)
        )

        # Additionally, if this is a model class, add some custom
        # Methods to its query_class for fetching serialized
        # models directly
        if hasattr(cls, 'query_class'):
            cls.query_class.all_serialized = (
                lambda s: safe_serialize(s.all())
            )
            cls.query_class.get_serialized = (
                lambda s, pk: safe_serialize(s.get(pk))
            )

        return f
    return decorator(func) if func else decorator


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

