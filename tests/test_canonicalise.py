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

def test_it_canonicalises_none():
    assert canonicalise(None) is None

def test_it_canonicalises_list_of_objs_with_none_values():
    obj = [
            {'a': 1, 'b': 2},
            {'a': 1, 'b': None},
    ]
    expected = [
            {'a': 1, 'b': None},
            {'a': 1, 'b': 2},
    ]
    assert canonicalise(obj) == expected

def test_it_doesnt_canonicalise_glosses():
    obj = {
        'glosses': ['b', 'a']
    }
    assert canonicalise(obj) == obj

def test_it_doesnt_sort_variants():
    obj = {
        'variants': [
            {'written': '親戚', 'pronounced': 'しんせき'},
            {'written': '親せき', 'pronounced': 'しんせき'},
        ],
    }
    assert [v['written'] for v in canonicalise(obj)['variants']] == [
        '親戚', '親せき',
        ]

def test_it_canonicalises_within_unsorted_variants():
    obj = {'variants': [{'written': '親戚', 'priorities': ['news2', 'ichi1']}]}
    variant = canonicalise(obj)['variants'][0]
    assert tuple(variant.items()) == (
        ('priorities', ['ichi1', 'news2']), ('written', '親戚'),
        )

def test_it_doesnt_sort_kanjidic_meanings():
    obj = {'meanings': ['parent', 'intimacy', 'relative']}
    assert canonicalise(obj) == obj

def test_it_doesnt_sort_jmdict_senses():
    obj = {
        'meanings': [
            {'glosses': ['intimacy', 'closeness']},
            {'glosses': ['close relative']},
        ],
    }
    assert canonicalise(obj) == obj

def test_it_doesnt_sort_kanjidic_readings():
    obj = {
        'kun_readings': ['ふか.い', '-ぶか.い'],
        'on_readings': ['セイ', 'ショウ'],
        'name_readings': ['ぎ', 'ちか', 'のり'],
    }
    assert canonicalise(obj)['kun_readings'] == ['ふか.い', '-ぶか.い']
    assert canonicalise(obj)['on_readings'] == ['セイ', 'ショウ']
    assert canonicalise(obj)['name_readings'] == ['ぎ', 'ちか', 'のり']

def test_it_sorts_reading_endpoint_kanji_lists():
    obj = {'main_kanji': ['深', '侚'], 'name_kanji': ['浤', '泓']}
    assert canonicalise(obj) == {
        'main_kanji': ['侚', '深'],
        'name_kanji': ['泓', '浤'],
        }

def test_it_still_sorts_lists_nested_under_an_ordered_key():
    obj = {'variants': [{'a': ['z', 'a']}]}
    assert canonicalise(obj) == {'variants': [{'a': ['a', 'z']}]}

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

def test_compare_obj_sorts_none_first():
    assert compare_obj(None, None) == 0
    assert compare_obj(None, 1) == -1
    assert compare_obj(1, None) == 1
    assert compare_obj(None, 'a') == -1
    assert compare_obj('a', None) == 1
    assert compare_obj(None, []) == -1
    assert compare_obj([], None) == 1
    assert compare_obj({'a': None}, {'a': 1}) == -1
    assert compare_obj({'a': 1}, {'a': None}) == 1

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
