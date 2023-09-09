import pytest
from lxml import etree

from kanjiapi.entry import Entry, Meaning, KanjiForm, Reading
from kanjiapi.entry_data import word_dict
from test_helper import element_for


root = etree.parse('JMDict')


def test_extracts_kanji_to_entries_dict_from_single_entry():
    entries = [element_for(root, '1151020')]

    entries_by_kanji = word_dict(entries)

    entry = Entry(
        (KanjiForm('愛猫', ()),),
        (Reading('あいびょう', ()),),
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
        (Reading('おきゃくさん', ()),),
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
        (Reading('おまいり', ()),),
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
        (Reading('だぼはぜ', ()), Reading('ダボハゼ', ())),
        (Meaning(('goby (fish)',)),),
        )
    assert entries_by_kanji == dict({
        '鯊': {entry},
        })


def test_entry_with_restricted_reading():
    entries = [element_for(root, '1009250')]

    entries_by_kanji = word_dict(entries)

    entry = Entry(
        (
            KanjiForm('どの位', ('ichi1', 'spec1')),
            KanjiForm('何の位', ()),
            KanjiForm('何のくらい', ()),
        ),
        (
            Reading('どのくらい', ()),
            Reading('どのぐらい', ('どの位', '何の位')),
        ),
        (Meaning(('how long', 'how far', 'how much')),),
        )
    assert entries_by_kanji == dict({
        '位': {entry},
        '何': {entry},
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
        (Reading('あいびょう', ()),),
        (
            Meaning(('pet cat', 'beloved cat')),
            Meaning(('ailurophilia', 'fondness for cats')),
        ),
    )
    entry2 = Entry(
        (KanjiForm('海猫', ()),),
        (Reading('うみねこ', ()), Reading('ウミネコ', ())),
        (
            Meaning(('black-tailed gull (Larus crassirostris)',)),
        ),
        )
    assert entries_by_kanji == dict({
        '愛': {entry1},
        '猫': {entry1, entry2},
        '海': {entry2},
        })
