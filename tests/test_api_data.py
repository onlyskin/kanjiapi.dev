import pytest
import ujson
from lxml import etree

from kanjiapi.api_data import kanji_data, reading_data, heisig_keyword

root = etree.parse('kanjidic2.xml')


def element_for(root, kanji):
    return root.xpath('./character/literal[.="' + kanji + '"]/..')[0]


def test_kanji_data_xml():
    character = element_for(root, '亜')
    kanji = kanji_data(character)
    output = ujson.dumps(kanji, indent=2, ensure_ascii=False)
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
  "unicode": "4E9C",
  "heisig_en": "Asia",
  "notes": []
}'''


def test_handles_kanji_without_grades():
    character = element_for(root, '唖')
    kanji = kanji_data(character)
    output = ujson.dumps(kanji, indent=2, ensure_ascii=False)
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
  "unicode": "5516",
  "heisig_en": "babble",
  "notes": []
}'''


def test_handles_kanji_with_multiple_stroke_counts():
    character = element_for(root, '逢')
    kanji = kanji_data(character)
    output = ujson.dumps(kanji, indent=2, ensure_ascii=False)
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
  "unicode": "9022",
  "heisig_en": "tryst",
  "notes": []
}'''


def test_handles_character_with_CJK_equivalent():
    character = element_for(root, '海')
    kanji = kanji_data(character)
    output = ujson.dumps(kanji, indent=2, ensure_ascii=False)
    assert output == '''{
  "kanji": "海",
  "grade": 2,
  "stroke_count": 9,
  "meanings": [
    "sea",
    "ocean"
  ],
  "kun_readings": [
    "うみ"
  ],
  "on_readings": [
    "カイ"
  ],
  "name_readings": [
    "あ",
    "あま",
    "うな",
    "うん",
    "え",
    "か",
    "た",
    "ひろ",
    "ひろし",
    "ぶ",
    "まち",
    "まま",
    "み",
    "め",
    "わたる"
  ],
  "jlpt": 3,
  "unicode": "6D77",
  "heisig_en": "sea",
  "notes": []
}'''


def test_handles_character_in_CJK_block():
    character = element_for(root, '海')
    kanji = kanji_data(character)
    output = ujson.dumps(kanji, indent=2, ensure_ascii=False)
    assert output == '''{
  "kanji": "海",
  "grade": 9,
  "stroke_count": 10,
  "meanings": [],
  "kun_readings": [
    "うみ"
  ],
  "on_readings": [
    "カイ"
  ],
  "name_readings": [],
  "jlpt": null,
  "unicode": "FA45",
  "heisig_en": null,
  "unihan_cjk_compatibility_variant": "海",
  "notes": [
    "The character `海` is in the Unicode CJK Compatibility block. The unified codepoint for this character can be found in this response in the field `unihan_cjk_compatibility_variant`. To learn more, look at the kanjiapi.dev `README.md`"
  ]
}'''


class TestGrades:
    def test_kyouiku_grade(self):
        character = element_for(root, '一')
        kanji = kanji_data(character)
        assert kanji['grade'] == 1

    def test_joyo_grade(self):
        character = element_for(root, '蜜')
        kanji = kanji_data(character)
        assert kanji['grade'] == 8

    def test_jinmeiyo_grade(self):
        character = element_for(root, '與')
        kanji = kanji_data(character)
        assert kanji['grade'] == 9

    def test_ungraded(self):
        character = element_for(root, '蠍')
        kanji = kanji_data(character)
        assert kanji['grade'] == None


def test_reading_data():
    character = element_for(root, '亜')
    kanjis = [kanji_data(character)]
    readings = reading_data(kanjis)
    output = ujson.dumps(readings, indent=2, ensure_ascii=False)
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
