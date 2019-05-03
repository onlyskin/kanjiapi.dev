import pytest
from lxml import etree

from entry import Entry, Meaning, KanjiForm, Reading
from entry_data import word_dict
from test_helper import element_for


root = etree.parse('JMDict')


def test_extracts_kanji_to_entries_dict_from_single_entry():
    entries = [element_for(root, '1151020')]

    entries_by_kanji = word_dict(entries)

    entry = Entry(
        [KanjiForm('愛猫', set())],
        [Reading('あいびょう', [])],
        [
            Meaning(['pet cat', 'beloved cat']),
            Meaning(['ailurophilia', 'fondness for cats']),
            ],
        )
    assert entries_by_kanji == dict({
        '愛': {entry},
        '猫': {entry},
        })


def test_entry_with_multiple_kanji_forms():
    entries = [element_for(root, '1001760')]

    entries_by_kanji = word_dict(entries)

    entry = Entry(
        [KanjiForm('お客さん', set()), KanjiForm('御客さん', set())],
        [Reading('おきゃくさん', [])],
        [
            Meaning(['guest', 'visitor']),
            Meaning(['customer', 'client', 'shopper', 'spectator',
                    'audience', 'tourist', 'sightseer', 'passenger']),
            ],
        )
    assert entries_by_kanji == dict({
        '客': {entry},
        '御': {entry},
        })


def test_entry_with_common_and_rare_kanji_forms():
    entries = [element_for(root, '1006670')]

    entries_by_kanji = word_dict(entries)

    entry = Entry(
        [KanjiForm('其処', set(['spec1'])), KanjiForm('其所', set())],
        [Reading('そこ', [])],
        [
            Meaning(['there (place relatively near listener)']),
            Meaning(['there (place just mentioned)', 'that place']),
            Meaning(['then (of some incident just spoken of)',
                    'that (of point just raised)']),
            Meaning(['you']),
            ],
        )
    assert entries_by_kanji == dict({
        '其': {entry},
        '処': {entry},
        '所': {entry},
        })


def test_entry_with_two_rebs():
    entries = [element_for(root, '1007440')]

    entries_by_kanji = word_dict(entries)

    entry = Entry(
        [KanjiForm('だぼ鯊', set())],
        [Reading('だぼはぜ', []), Reading('ダボハゼ', [])],
        [Meaning(['goby (fish)'])],
        )
    assert entries_by_kanji == dict({
        '鯊': {entry},
        })


def test_entry_with_restricted_reading():
    entries = [element_for(root, '1009250')]

    entries_by_kanji = word_dict(entries)

    entry = Entry(
        [
            KanjiForm('どの位', set(['ichi1', 'spec1'])),
            KanjiForm('何の位', set()),
            KanjiForm('何のくらい', set()),
            ],
        [
            Reading('どのくらい', []),
            Reading('どのぐらい', ['どの位', '何の位']),
            ],
        [Meaning(['how long', 'how far', 'how much'])],
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
    entries = [element_for(root, '1151020'), element_for(root, '1267700')]

    entries_by_kanji = word_dict(entries)

    entry1 = Entry(
        [KanjiForm('愛猫', set())],
        [Reading('あいびょう', [])],
        [
            Meaning(['pet cat', 'beloved cat']),
            Meaning(['ailurophilia', 'fondness for cats']),
            ],
        )
    entry2 = Entry(
        [KanjiForm('虎猫', set())],
        [Reading('とらねこ', []), Reading('トラネコ', [])],
        [
            Meaning(['tabby cat', 'tiger cat', 'stripped cat']),
            ],
        )
    assert entries_by_kanji == dict({
        '愛': {entry1},
        '猫': {entry1, entry2},
        '虎': {entry2},
        })
