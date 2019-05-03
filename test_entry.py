import pytest
import json

from entry import Entry, Meaning, KanjiForm, Reading, EntryEncoder


def test_jsonify_simple_entry():
    entry = Entry(
        [KanjiForm('愛猫', set())],
        [Reading('あいびょう', [])],
        [
            Meaning(['pet cat', 'beloved cat']),
            Meaning(['ailurophilia', 'fondness for cats']),
            ],
        )
    output = json.dumps(entry, indent=2, ensure_ascii=False, cls=EntryEncoder)
    assert output == '''{
  "variants": [
    {
      "written": "愛猫",
      "pronounced": "あいびょう",
      "priorities": []
    }
  ],
  "meanings": [
    {
      "glosses": [
        "pet cat",
        "beloved cat"
      ]
    },
    {
      "glosses": [
        "ailurophilia",
        "fondness for cats"
      ]
    }
  ]
}'''


def test_words_for_entry_with_multiple_kanji_forms():
    entry = Entry(
        [KanjiForm('お客さん', set()), KanjiForm('御客さん', set())],
        [Reading('おきゃくさん', [])],
        [
            Meaning(['guest', 'visitor']),
            Meaning(['customer', 'client', 'shopper', 'spectator',
                    'audience', 'tourist', 'sightseer', 'passenger']),
            ],
        )
    output = json.dumps(entry, indent=2, ensure_ascii=False, cls=EntryEncoder)
    assert output == '''{
  "variants": [
    {
      "written": "お客さん",
      "pronounced": "おきゃくさん",
      "priorities": []
    },
    {
      "written": "御客さん",
      "pronounced": "おきゃくさん",
      "priorities": []
    }
  ],
  "meanings": [
    {
      "glosses": [
        "guest",
        "visitor"
      ]
    },
    {
      "glosses": [
        "customer",
        "client",
        "shopper",
        "spectator",
        "audience",
        "tourist",
        "sightseer",
        "passenger"
      ]
    }
  ]
}'''


def test_words_for_entry_with_kanji_priority():
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
    output = json.dumps(entry, indent=2, ensure_ascii=False, cls=EntryEncoder)
    assert output == '''{
  "variants": [
    {
      "written": "其処",
      "pronounced": "そこ",
      "priorities": [
        "spec1"
      ]
    },
    {
      "written": "其所",
      "pronounced": "そこ",
      "priorities": []
    }
  ],
  "meanings": [
    {
      "glosses": [
        "there (place relatively near listener)"
      ]
    },
    {
      "glosses": [
        "there (place just mentioned)",
        "that place"
      ]
    },
    {
      "glosses": [
        "then (of some incident just spoken of)",
        "that (of point just raised)"
      ]
    },
    {
      "glosses": [
        "you"
      ]
    }
  ]
}'''


def test_words_for_entry_with_two_readings():
    entry = Entry(
        [KanjiForm('だぼ鯊', set())],
        [Reading('だぼはぜ', []), Reading('ダボハゼ', [])],
        [Meaning(['goby (fish)'])],
        )
    output = json.dumps(entry, indent=2, ensure_ascii=False, cls=EntryEncoder)
    assert output == '''{
  "variants": [
    {
      "written": "だぼ鯊",
      "pronounced": "だぼはぜ",
      "priorities": []
    },
    {
      "written": "だぼ鯊",
      "pronounced": "ダボハゼ",
      "priorities": []
    }
  ],
  "meanings": [
    {
      "glosses": [
        "goby (fish)"
      ]
    }
  ]
}'''


def test_words_with_restricted_reading():
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
    output = json.dumps(entry, indent=2, ensure_ascii=False, cls=EntryEncoder)
    assert output == '''{
  "variants": [
    {
      "written": "どの位",
      "pronounced": "どのくらい",
      "priorities": [
        "ichi1",
        "spec1"
      ]
    },
    {
      "written": "どの位",
      "pronounced": "どのぐらい",
      "priorities": [
        "ichi1",
        "spec1"
      ]
    },
    {
      "written": "何の位",
      "pronounced": "どのくらい",
      "priorities": []
    },
    {
      "written": "何の位",
      "pronounced": "どのぐらい",
      "priorities": []
    },
    {
      "written": "何のくらい",
      "pronounced": "どのくらい",
      "priorities": []
    }
  ],
  "meanings": [
    {
      "glosses": [
        "how long",
        "how far",
        "how much"
      ]
    }
  ]
}'''
