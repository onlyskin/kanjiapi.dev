import pytest
import json
from lxml import etree

from kanjiapi.api_data import kanji_data, reading_data

root = etree.parse('kanjidic2.xml')


def element_for(root, kanji):
    return root.xpath('./character/literal[.="' + kanji + '"]/..')[0]


def test_kanji_data_xml():
    character = element_for(root, '亜')
    kanji = kanji_data(character)
    output = json.dumps(kanji, indent=2, ensure_ascii=False)
    assert output == '''{
  "kanji": "亜",
  "grade": 8,
  "stroke_count": 7,
  "meanings": [
    "Asia",
    "rank next",
    "come after",
    "-ous"
  ],
  "kun_readings": [
    "つ.ぐ"
  ],
  "on_readings": [
    "ア"
  ],
  "name_readings": [
    "や",
    "つぎ",
    "つぐ"
  ],
  "jlpt": 1,
  "unicode": "4e9c"
}'''


def test_handles_kanji_without_grades():
    character = element_for(root, '唖')
    kanji = kanji_data(character)
    output = json.dumps(kanji, indent=2, ensure_ascii=False)
    assert output == '''{
  "kanji": "唖",
  "grade": null,
  "stroke_count": 10,
  "meanings": [
    "mute",
    "dumb"
  ],
  "kun_readings": [
    "おし"
  ],
  "on_readings": [
    "ア",
    "アク"
  ],
  "name_readings": [],
  "jlpt": null,
  "unicode": "5516"
}'''


def test_handles_kanji_with_multiple_stroke_counts():
    character = element_for(root, '逢')
    kanji = kanji_data(character)
    output = json.dumps(kanji, indent=2, ensure_ascii=False)
    assert output == '''{
  "kanji": "逢",
  "grade": 9,
  "stroke_count": 10,
  "meanings": [
    "meeting",
    "tryst",
    "date",
    "rendezvous"
  ],
  "kun_readings": [
    "あ.う",
    "むか.える"
  ],
  "on_readings": [
    "ホウ"
  ],
  "name_readings": [
    "あい",
    "おう"
  ],
  "jlpt": null,
  "unicode": "9022"
}'''


def test_handles_CJK_character():
    character = element_for(root, '漢')
    kanji = kanji_data(character)
    output = json.dumps(kanji, indent=2, ensure_ascii=False)
    assert output == '''{
  "kanji": "漢",
  "grade": 3,
  "stroke_count": 13,
  "meanings": [
    "Sino-",
    "China"
  ],
  "kun_readings": [],
  "on_readings": [
    "カン"
  ],
  "name_readings": [
    "はん"
  ],
  "jlpt": 3,
  "unicode": "6f22"
}'''


def test_reading_data():
    character = element_for(root, '亜')
    kanjis = [kanji_data(character)]
    readings = reading_data(kanjis)
    output = json.dumps(readings, indent=2, ensure_ascii=False)
    assert output == '''[
  {
    "reading": "つ.ぐ",
    "main_kanji": [
      "亜"
    ],
    "name_kanji": []
  },
  {
    "reading": "ア",
    "main_kanji": [
      "亜"
    ],
    "name_kanji": []
  },
  {
    "reading": "や",
    "main_kanji": [],
    "name_kanji": [
      "亜"
    ]
  },
  {
    "reading": "つぎ",
    "main_kanji": [],
    "name_kanji": [
      "亜"
    ]
  },
  {
    "reading": "つぐ",
    "main_kanji": [],
    "name_kanji": [
      "亜"
    ]
  }
]'''
