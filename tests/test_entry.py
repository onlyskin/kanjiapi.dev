import pytest
import ujson

from kanjiapi.entry import Entry, Meaning, KanjiForm, Reading


def test_jsonify_simple_entry():
    entry = Entry(
        (KanjiForm('愛猫', ()),),
        (Reading('あいびょう', (), ()),),
        (
            Meaning(('pet cat', 'beloved cat')),
            Meaning(('ailurophilia', 'fondness for cats')),
        ),
        )
    output = ujson.dumps(entry.words(), indent=2, ensure_ascii=False)
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
        (KanjiForm('お客さん', ()), KanjiForm('御客さん', ())),
        (Reading('おきゃくさん', (), ()),),
        (
            Meaning(('guest', 'visitor')),
            Meaning(('customer', 'client', 'shopper', 'spectator',
                    'audience', 'tourist', 'sightseer', 'passenger')),
        ),
        )
    output = ujson.dumps(entry.words(), indent=2, ensure_ascii=False)
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
        (KanjiForm('其処', ('spec1',)), KanjiForm('其所', ())),
        (Reading('そこ', (), ()),),
        (
            Meaning(('there (place relatively near listener)',)),
            Meaning(('there (place just mentioned)', 'that place',)),
            Meaning(('then (of some incident just spoken of)',
                    'that (of point just raised)')),
            Meaning(('you',)),
        ),
    )
    output = ujson.dumps(entry.words(), indent=2, ensure_ascii=False)
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
        (KanjiForm('だぼ鯊', ()),),
        (Reading('だぼはぜ', (), ()), Reading('ダボハゼ', (), ())),
        (Meaning(('goby (fish)',)),),
        )
    output = ujson.dumps(entry.words(), indent=2, ensure_ascii=False)
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
        (
            KanjiForm('どの位', ('ichi1', 'spec1')),
            KanjiForm('何の位', ()),
            KanjiForm('何のくらい', ()),
        ),
        (
            Reading('どのくらい', (), ()),
            Reading('どのぐらい', ('どの位', '何の位'), ()),
        ),
        (Meaning(('how long', 'how far', 'how much')),),
        )
    output = ujson.dumps(entry.words(), indent=2, ensure_ascii=False)
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

def test_words_with_priority_on_reading():
    entry = Entry(
        (KanjiForm('雷', ('ichi1',)),),
        (
            Reading('かみなり', (), ('ichi1',)),
            Reading('いかづち', (), ()),
        ),
        (
            Meaning(('lightning', 'thunder', 'thunderbolt')),
        ),
        )
    output = ujson.dumps(entry.words(), indent=2, ensure_ascii=False)
    assert output == '''{
  "variants": [
    {
      "written": "雷",
      "pronounced": "かみなり",
      "priorities": [
        "ichi1"
      ]
    },
    {
      "written": "雷",
      "pronounced": "いかづち",
      "priorities": []
    }
  ],
  "meanings": [
    {
      "glosses": [
        "lightning",
        "thunder",
        "thunderbolt"
      ]
    }
  ]
}'''


def xtest_words_with_priority_on_two_readings():
    # see entry 1578010
    pass

def xtest_words_with_priority_on_reading_and_restricted_forms():
    pass
