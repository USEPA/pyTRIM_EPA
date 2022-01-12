from functools import wraps, partial


def cache_key(*args, **kwargs):
    key_args = list(sorted([str(x) for x in args])) + [
        f'{k}={kwargs[k]}' for k in sorted(kwargs.keys())
    ]
    return '&'.join([x for x in key_args if x])


GLOBAL_CACHE = {}


def with_cache(base_key=None):
    def decorated(base_key, f):
        if base_key is None:
            base_key = str(f)
        # print(f'Making cache with "{base_key}"')
        f_cache = GLOBAL_CACHE.setdefault(base_key, {})

        @wraps(f)
        def caching(*args, IGNORE_CACHE=False, **kwargs):
            k = cache_key(*args, **kwargs)
            if not IGNORE_CACHE and k in f_cache:
                # print(f'Cached for "{base_key}" and {k}: {f_cache[k]}')
                ans = f_cache[k]
                if isinstance(ans, Exception):
                    raise ans
                return ans

            try:
                ans = f(*args, **kwargs)
            except Exception as e:
                ans = e

            if not IGNORE_CACHE:
                # print(f'Caching: {ans} for "{base_key}" and {k}')
                f_cache[k] = ans

            if isinstance(ans, Exception):
                raise ans
            return ans
        return caching

    return partial(decorated, base_key)
