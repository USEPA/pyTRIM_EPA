from functools import wraps, partial

__all__ = ['CacheManager']


class CacheManager:
    _CACHERS = {}
    DISABLED = False

    @classmethod
    def cache_key(cls, *args, **kwargs):
        key_args = list(sorted([str(x) for x in args])) + [
            f'{k}={kwargs[k]}' for k in sorted(kwargs.keys())
        ]
        return '&'.join([x for x in key_args if x])

    class Cacher(dict):
        def wrap(self, f):
            @wraps(f)
            def cached(*args, **kwargs):
                if CacheManager.DISABLED:
                    return f(*args, **kwargs)

                k = CacheManager.cache_key(*args, **kwargs)

                if not CacheManager.DISABLED and k in self:
                    # print(f'Cached for "{base_key}" and {k}: {self[k]}')
                    ans = self[k]
                    if isinstance(ans, Exception):
                        raise ans
                    return ans

                try:
                    ans = f(*args, **kwargs)
                except Exception as e:
                    ans = e

                if not CacheManager.DISABLED:
                    # print(f'Caching: {ans} for "{base_key}" and {k}')
                    self[k] = ans

                if isinstance(ans, Exception):
                    raise ans
                return ans
            return cached

    @classmethod
    def subcache(cls, key):
        # print(f'Making sub-cache with "{key}"')
        return cls._CACHERS.setdefault(key, cls.Cacher())

    @classmethod
    def toggle_caching(cls, on_off=None):
        if on_off is None:
            on_off = cls.DISABLED
        cls.DISABLED = not (on_off or False)

    @classmethod
    def without_caching(cls, f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            cls.toggle_caching()
            try:
                return f(*args, **kwargs)
            finally:
                cls.toggle_caching()
        return wrapped

    @classmethod
    def with_caching(cls, base_key=None):
        def decorated(base_key, f):
            if base_key is None:
                base_key = str(f)
            return CacheManager.subcache(base_key).wrap(f)
        return partial(decorated, base_key)
