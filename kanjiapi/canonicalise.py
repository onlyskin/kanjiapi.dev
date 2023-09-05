from sys import stdin
import json
from functools import cmp_to_key


def compare_obj(a, b):
    if isinstance(a, list) or isinstance(a, tuple):
        if len(a) == len(b) and len(a) != 0:
            for x, y in zip(a, b):
                comp = compare_obj(x, y)
                if comp != 0:
                    return comp
        else:
            return len(a) - len(b)

    if isinstance(a, dict):
        a_keys = list(a.keys())
        b_keys = list(b.keys())
        if a_keys == b_keys:
            a_values = list(a.values())
            b_values = list(b.values())
            if a_values == b_values:
                return 0
            else:
                return compare_obj(a_values, b_values)
        elif a_keys < b_keys:
            return -1
        else:
            return 1

    if a == b:
        return 0
    elif a < b:
        return -1
    else:
        return 1


def canonicalise(obj):
    if isinstance(obj, dict):
        res = {}
        for k, v in sorted(obj.items()):
            res[k] = v if k == 'glosses' else canonicalise(v)
        return res

    if isinstance(obj, list) or isinstance(obj, tuple):
        canonicalised = [canonicalise(i) for i in obj]
        return sorted(canonicalised, key=cmp_to_key(compare_obj))

    return obj


if __name__ == '__main__':
    raw_json = stdin.read()
    canonicalised = canonicalise(json.loads(raw_json))
    print(json.dumps(canonicalised))
