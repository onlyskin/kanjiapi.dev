from kanjiapi.canonicalise import canonicalise, compare_obj


def test_it_canonicalises_string():
    assert canonicalise('kanji') == 'kanji'

def test_it_canonicalises_number():
    assert canonicalise(5) == 5

def test_it_canonicalises_list_of_strings():
    assert canonicalise(['reading', 'kanji']) == ['kanji', 'reading']

def test_it_canonicalises_dict():
    assert tuple(canonicalise({'z': 1, 'a': 3}).items()) == (('a', 3), ('z', 1))

def test_it_canonicalises_dict_with_nested_dict():
    obj = {
            'z': {'z': 1, 'a': 3},
            'a': {'y': 1, 'b': 3},
    }
    expected = {
            'a': {'b': 3, 'y': 1},
            'z': {'a': 3, 'z': 1},
    }
    assert list(elements(canonicalise(obj))) == list(elements(expected))

def test_it_canonicalises_list_of_list_of_strings():
    obj = [['z', 'a'], ['y', 'b']]
    expected = [['a', 'z'], ['b', 'y']]
    assert canonicalise(obj) == expected

def test_it_canonicalises_list_of_objs():
    obj = [
            {'z': 2, 'a': 4},
            {'y': 1, 'b': 3},
            {'z': 1, 'a': 3},
    ]
    expected = [
            {'a': 3, 'z': 1},
            {'a': 4, 'z': 2},
            {'b': 3, 'y': 1},
    ]
    assert list(elements(canonicalise(obj))) == list(elements(expected))

def test_it_doesnt_canonicalise_glosses():
    obj = {
        'glosses': ['b', 'a']
    }
    assert canonicalise(obj) == obj

def test_compare_obj():
    assert compare_obj({}, {}) == 0
    assert compare_obj({'a': 1}, {'a': 1}) == 0
    assert compare_obj({'a': 1}, {'a': 2}) == -1
    assert compare_obj({'a': 1}, {'b': 1}) == -1
    assert compare_obj({'b': 1}, {'a': 1}) == 1
    assert compare_obj({'a': {'a': 1}}, {'a': {'a': 1}}) == 0
    assert compare_obj([], []) == 0
    assert compare_obj(['a', 'b'], ['a', 'b', 'c']) == -1
    assert compare_obj([], [{'b': 1}]) == -1
    assert compare_obj([{'a': 1}], [{'b': 1}]) == -1
    assert compare_obj({'a': {'b': 1}}, {'a': {'a': 1}}) == 1
    assert compare_obj({'a': {'a': 2}}, {'a': {'a': 1}}) == 1

def elements(a):
    if isinstance(a, list):
        for v in a:
            yield v
    else:
        for k, v in a.items():
            if isinstance(v, dict):
                yield k, list(elements(v))
            else:
                yield k, v
