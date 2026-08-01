from sys import stdin
import json
from functools import cmp_to_key


def compare_obj(a, b):
    if a is None or b is None:
        if a is None and b is None:
            return 0
        return -1 if a is None else 1

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


# Lists which the source dictionaries already order meaningfully. See
# CHANGELOG.md.
ORDERED_KEYS = (
        'glosses',
        'kun_readings',
        'meanings',
        'name_readings',
        'on_readings',
        'variants',
        )


def canonicalise(obj, sort=True):
    if isinstance(obj, dict):
        res = {}
        for k, v in sorted(obj.items()):
            res[k] = canonicalise(v, sort=k not in ORDERED_KEYS)
        return res

    if isinstance(obj, list) or isinstance(obj, tuple):
        canonicalised = [canonicalise(i) for i in obj]
        if not sort:
            return canonicalised
        return sorted(canonicalised, key=cmp_to_key(compare_obj))

    return obj


if __name__ == '__main__':
    raw_json = stdin.read()
    canonicalised = canonicalise(json.loads(raw_json))
    print(json.dumps(canonicalised))
