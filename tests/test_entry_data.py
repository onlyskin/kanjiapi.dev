import pytest
from lxml import etree

from kanjiapi.entry import Entry, Meaning, KanjiForm, Reading
from kanjiapi.entry_data import word_dict
from test_helper import element_for


root = etree.parse('data/JMdict_e_NG')


def test_extracts_kanji_to_entries_dict_from_single_entry():
    entries = [element_for(root, '1151020')]

    entries_by_kanji = word_dict(entries)

    entry = Entry(
        (KanjiForm('愛猫', ()),),
        (Reading('あいびょう', (), ()),),
        (
            Meaning(('pet cat', 'beloved cat')),
            Meaning(('ailurophilia', 'fondness for cats')),
        ),
        )
    assert entries_by_kanji == dict({
        '愛': {entry},
        '猫': {entry},
        })


def test_entry_with_multiple_kanji_forms():
    entries = [element_for(root, '1001760')]

    entries_by_kanji = word_dict(entries)

    entry = Entry(
        (KanjiForm('お客さん', ()), KanjiForm('御客さん', ())),
        (Reading('おきゃくさん', (), ()),),
        (
            Meaning(('guest', 'visitor')),
            Meaning(('customer', 'client', 'shopper', 'spectator',
                    'audience', 'tourist', 'sightseer', 'passenger')),
        ),
        )
    assert entries_by_kanji == dict({
        '客': {entry},
        '御': {entry},
        })


def test_entry_with_common_and_rare_kanji_forms():
    entries = [element_for(root, '1001950')]

    entries_by_kanji = word_dict(entries)

    entry = Entry(
        (
            KanjiForm('お参り', ('ichi1', 'news2', 'nf36')),
            KanjiForm('御参り', ()),
        ),
        (Reading('おまいり', (), ('ichi1', 'news2', 'nf36')),),
        (Meaning(('visit (to a shrine, grave, etc.)', 'worship')),),
    )
    assert entries_by_kanji == dict({
        '参': {entry},
        '御': {entry},
    })


def test_entry_with_two_rebs():
    entries = [element_for(root, '1007440')]

    entries_by_kanji = word_dict(entries)

    entry = Entry(
        (KanjiForm('だぼ鯊', ()),),
        (Reading('だぼはぜ', (), ()), Reading('ダボハゼ', (), ())),
        (Meaning(('goby (fish)',)),),
        )
    assert entries_by_kanji == dict({
        '鯊': {entry},
        })


def test_entry_with_restricted_reading():
    entries = [element_for(root, '1004000')]

    entries_by_kanji = word_dict(entries)

    entry = Entry(
        (
            KanjiForm('クンクン鳴く', ()),
            KanjiForm('くんくん鳴く', ()),
        ),
        (
            Reading('クンクンなく', ('クンクン鳴く',), ()),
            Reading('くんくんなく', ('くんくん鳴く',), ()),
        ),
        (Meaning(('to whine (of a dog)',)),),
        )
    assert entries_by_kanji == dict({
        '鳴': {entry},
    })


def test_entry_with_reading_priority():
    entries = [element_for(root, '1003660')]

    entries_by_kanji = word_dict(entries)

    entry = Entry(
        (KanjiForm('限り限り', ('ichi1',)),),
        (
            Reading('ぎりぎり', (), ('ichi1',)),
            Reading('ギリギリ', (), ()),
        ),
        (Meaning((
            'just barely', 'only just', 'at the very limit',
            'at the last moment')),),
        )
    assert entries_by_kanji == dict({
        '限': {entry},
        })

def xtest_sense_restricted_by_reading():
    entries = [element_for(root, '1165180')]


def xtest_sense_restricted_by_kanji():
    entries = [element_for(root, '')]


def test_combines_multiple_entries():
    entries = [element_for(root, '1151020'), element_for(root, '1772990')]

    entries_by_kanji = word_dict(entries)

    entry1 = Entry(
        (KanjiForm('愛猫', ()),),
        (Reading('あいびょう', (), ()),),
        (
            Meaning(('pet cat', 'beloved cat')),
            Meaning(('ailurophilia', 'fondness for cats')),
        ),
    )
    entry2 = Entry(
        (KanjiForm('海猫', ()),),
        (Reading('うみねこ', (), ()), Reading('ウミネコ', (), ())),
        (
            Meaning(('black-tailed gull (Larus crassirostris)',)),
        ),
        )
    assert entries_by_kanji == dict({
        '愛': {entry1},
        '猫': {entry1, entry2},
        '海': {entry2},
        })
