from functools import wraps
from types import MethodType


def add_method(obj, name=None, instance_method=False):
    def decorator(f):
        fname = name or f.__name__

        @wraps(f)
        def inner(self, *args, **kwargs):
            if instance_method:
                return f(self, *args, **kwargs)
            else:
                return f(*args, **kwargs)

        # Set the wrapped function as a method of the object
        if instance_method:
            setattr(obj, fname, MethodType(inner, obj))
        else:
            setattr(obj, fname, inner)

        # Return the function, so we can still just call it if needed
        return f
    # Return the decorator factory
    return decorator
