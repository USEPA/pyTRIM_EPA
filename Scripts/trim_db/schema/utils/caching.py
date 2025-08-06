from functools import wraps, partial
from uuid import uuid4

__all__ = ['CacheManager']

import sqlalchemy.orm.exc


class CacheManager:
    _CACHERS = {}
    DISABLED_REQUESTS = {}  # caching generates multiple problems such as detached db session and old values showing up in the UI rather than the updated value

    @classmethod
    def cache_key(cls, *args, **kwargs):
        key_args = list(sorted([str(x) for x in args])) + [
            f'{k}={kwargs[k]}' for k in sorted(kwargs.keys())
        ]
        return '&'.join([x for x in key_args if x])

    class Cacher(dict):
        # def __init__(self, base_key, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.__base_key__ = base_key

        def wrap(self, f):
            @wraps(f)
            def cached(*args, **kwargs):
                print_this = False
                # if 'AirTemperature' in args:
                #     print_this = True
                #     print(f'\n--- args {args} --- kwargs {kwargs} ---\n f is {f}')
                if CacheManager.DISABLED_REQUESTS:
                    # print(f'{90*"^"}\n{35*" "} CACHE DISABLED!!!! {35*" "}\n{90*"^"}\n')
                    return f(*args, **kwargs)

                k = CacheManager.cache_key(*args, **kwargs)

                if not CacheManager.DISABLED_REQUESTS and k in self:
                    # print(
                    #     f'Cached for "{self.__base_key__}"'
                    #     f' and {k}: {self[k]}'
                    # )
                    ans = self[k]
                    if print_this:
                        print(f'Existing Cache "{k}" -> {ans}\n')
                    if isinstance(ans, Exception):
                        #print(f"key {k} exists but this exception occurred: {ans}")
                        raise ans
                    return ans

                try:
                    ans = f(*args, **kwargs)
                except Exception as e:
                    ans = e

                if not CacheManager.DISABLED_REQUESTS:
                    # print(
                    #     f'Caching: {ans} for "{self.__base_key__}"'
                    #     f' and {k}'
                    # )
                    self[k] = ans
                    if print_this:
                        print(f'New Cache "{k}" -> {ans}\n')
                # We need to clear cache if any object is stale and in detached state.
                # This is important when unhandled exceptions occur and uncleared stale
                # objects in cash prevent scenario load.
                if isinstance(ans, sqlalchemy.orm.exc.DetachedInstanceError):
                    for ck in CacheManager._CACHERS:
                        CacheManager.clear_cache(ck)
                    return f(*args, **kwargs)
                if isinstance(ans, Exception):
                    # print(f"key {k} created but this exception occurred: {ans}")
                    raise ans
                return ans

            return cached

    @classmethod
    def subcache(cls, key):
        # print(f'Making sub-cache with {key} -> {cls._CACHERS.get(key)}"')
        return cls._CACHERS.setdefault(key, cls.Cacher())

    @classmethod
    def clear_cache(cls, key):
        # print(f"CHACHERS ARE {cls._CACHERS}")
        cls._CACHERS.get(key, {}).clear()

    @classmethod
    def clear_all(cls):
        for k in cls._CACHERS:
            cls.clear_cache(k)

    @classmethod
    def without_caching(cls, f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            k = str(uuid4())
            cls.DISABLED_REQUESTS[k] = True
            try:
                return f(*args, **kwargs)
            finally:
                cls.DISABLED_REQUESTS.pop(k)

        return wrapped

    @classmethod
    def with_caching(cls, base_key=None):
        def decorated(base_key, f):
            if base_key is None:
                base_key = str(f)
            # print(f"BASE KEY IS {base_key}")
            return CacheManager.subcache(base_key).wrap(f)

        return partial(decorated, base_key)
