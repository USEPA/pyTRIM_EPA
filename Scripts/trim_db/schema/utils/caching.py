import threading
import time
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

    class Cacher:
        def __init__(self, base_key, keymaker=None):
            self._base_key = base_key
            self._keymaker = keymaker if keymaker is not None else CacheManager.cache_key
            self._inner_cache = {}

        @property
        def _threaded_cache(self):
            t = threading.get_ident()
            if t not in self._inner_cache:
                self._inner_cache[t] = {}
            return self._inner_cache[t]

        def has(self, key):
            return key in self._threaded_cache

        def get(self, key):
            if key in self._threaded_cache:
                return self._threaded_cache[key]
            raise KeyError(key)

        def set(self, key, value):
            self._threaded_cache[key] = value

        def clear(self, thread_name=None):
            if thread_name is not None:
                if thread_name in self._inner_cache:
                    self._inner_cache.pop(thread_name)
            else:
                self._inner_cache = {}

        def cached(self, f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                print_this = False
                # if 'AirTemperature' in args:
                #     print_this = True
                #     print(f'\n--- args {args} --- kwargs {kwargs} ---\n f is {f}')
                if CacheManager.DISABLED_REQUESTS:
                    # print(f'{90*"^"}\n{35*" "} CACHE DISABLED!!!! {35*" "}\n{90*"^"}\n')
                    return f(*args, **kwargs)

                k = self._keymaker(*args, **kwargs)

                if self.has(k):
                    ans = self.get(k)
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

                self.set(k, ans)
                if print_this:
                    print(f'New Cache "{k}" -> {ans}\n')
                # We need to clear cache if any object is stale and in detached state.
                # This is important when unhandled exceptions occur and uncleared stale
                # objects in cash prevent scenario load.
                if isinstance(ans, sqlalchemy.orm.exc.DetachedInstanceError):
                    CacheManager.clear()
                    return f(*args, **kwargs)
                if isinstance(ans, Exception):
                    # print(f"key {k} created but this exception occurred: {ans}")
                    raise ans
                return ans

            return wrapped

    @classmethod
    def subcache(cls, key, keymaker=None):
        # print(f'Making sub-cache with {key} -> {cls._CACHERS.get(key)}"')
        return cls._CACHERS.setdefault(key, cls.Cacher(key, keymaker=keymaker))

    @classmethod
    def clear_cache(cls, key, all_threads=False):
        # print(f"CHACHERS ARE {cls._CACHERS}")
        t = None
        if not all_threads:
            t = threading.get_ident()
        cls._CACHERS.get(key, {}).clear(thread_name=t)

    @classmethod
    def clear(cls, all_threads=False):
        for k in cls._CACHERS:
            cls.clear_cache(k, all_threads=all_threads)

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
    def with_caching(cls, base_key=None, keymaker=None):
        def decorated(base_key, f):
            if base_key is None:
                base_key = str(f)
            # print(f"BASE KEY IS {base_key}")
            return CacheManager.subcache(base_key, keymaker=keymaker).cached(f)

        return partial(decorated, base_key)

    @classmethod
    def timeit(cls, func):
        def decorated(*args, **kwargs):
            st = time.time()
            ret = func(*args, **kwargs)
            et = time.time()
            print(f'\t> Ran `{func.__name__}({args}, {kwargs})` in {et - st} seconds')
            return ret
        return decorated
