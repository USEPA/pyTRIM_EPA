

def iter_by_longest_key(d):
    keys = sorted(list(d), key=lambda x: len(x))
    for k in reversed(keys):
        v = d[k]
        yield k, v
