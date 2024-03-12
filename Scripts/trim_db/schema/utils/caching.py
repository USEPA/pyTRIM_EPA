from functools import wraps, partial

__all__ = ['CacheManager']


class CacheManager:
    _CACHERS = {}
    DISABLED = False  # caching generates multiple problems such as detached db session and old values showing up in the UI rather than the updated value

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
                if CacheManager.DISABLED:
                    return f(*args, **kwargs)

                k = CacheManager.cache_key(*args, **kwargs)

                if not CacheManager.DISABLED and k in self:
                    # print(
                    #     f'Cached for "{self.__base_key__}"'
                    #     f' and {k}: {self[k]}'
                    # )
                    ans = self[k]
                    if print_this:
                        print(f'Existing Cache "{k}" -> {ans}\n')
                    if isinstance(ans, Exception):
                        # print(f"key {k} exists but this exception occurred: {ans}")
                        raise ans
                    return ans

                try:
                    ans = f(*args, **kwargs)
                except Exception as e:
                    ans = e

                if not CacheManager.DISABLED:
                    # print(
                    #     f'Caching: {ans} for "{self.__base_key__}"'
                    #     f' and {k}'
                    # )
                    self[k] = ans
                    if print_this:
                        print(f'New Cache "{k}" -> {ans}\n')

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
            # print(f"BASE KEY IS {base_key}")
            return CacheManager.subcache(base_key).wrap(f)
        return partial(decorated, base_key)
