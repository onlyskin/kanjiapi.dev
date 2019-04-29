import codecs
import sys
import json
from collections import defaultdict, OrderedDict
from lxml import etree

def nanori(character):
    readings = character.xpath('./reading_meaning//nanori')
    return [reading.text for reading in readings]

def on_readings(character):
    readings = character.xpath('./reading_meaning//reading[@r_type="ja_on"]')
    return [reading.text for reading in readings]

def kun_readings(character):
    readings = character.xpath('./reading_meaning//reading[@r_type="ja_kun"]')
    return [reading.text for reading in readings]

def meanings(character):
    meanings = character.xpath('./reading_meaning//meaning[not(@m_lang)]')
    return [meaning.text for meaning in meanings]

def grade(character):
    try:
        return character.xpath('./misc/grade')[0].text
    except (AttributeError, IndexError):
        return None

def stroke_count(character):
    return character.xpath('./misc/stroke_count')[0].text

def jlpt(character):
    try:
        return character.xpath('./misc/jlpt')[0].text
    except (AttributeError, IndexError):
        return None

def literal(character):
    return character.xpath('literal')[0].text

def kanji_data(character):
    return OrderedDict([
        ('kanji', literal(character)),
        ('grade', grade(character)),
        ('stroke_count', stroke_count(character)),
        ('meanings', meanings(character)),
        ('kun_readings', kun_readings(character)),
        ('on_readings', on_readings(character)),
        ('name_readings', nanori(character)),
        ('jlpt', jlpt(character)),
        ])

def reading_data(kanjis):
    readings = defaultdict(lambda: {'regular': [], 'name': []})

    for kanji in kanjis:
        literal = kanji['kanji']
        for reading in kanji['kun_readings'] + kanji['on_readings']:
            readings[reading]['regular'].append(literal)
        for reading in kanji['name_readings']:
            readings[reading]['name'].append(literal)

    return [OrderedDict([
        ('reading', reading),
        ('main_kanji', data['regular']),
        ('name_kanji', data['name']),
        ]) for reading, data in readings.items()]

def CJK_compatibility(character):
    return u'\uF900' <= literal(character) <= u'\uFAFF'

if __name__ == '__main__':
    VERSION_PATH = 'v1'
    KANJI_DIR = 'out/' + VERSION_PATH + '/kanji/'
    READING_DIR = 'out/' + VERSION_PATH + '/reading/'
    JOUYOU_GRADES = ['1', '2', '3', '4', '5', '6', '8']
    JINMEIYOU_GRADES = ['9', '10']

    root = etree.parse('kanjidic2.xml')
    characters = root.xpath('./character')

    kanjis = [kanji_data(character) for character in characters if not CJK_compatibility(character)]
    readings = reading_data(kanjis)

    all_kanji = [kanji['kanji'] for kanji in kanjis]
    jouyou_kanji = [kanji['kanji'] for kanji in kanjis if kanji['grade'] in JOUYOU_GRADES]
    jinmeiyou_kanji = [kanji['kanji'] for kanji in kanjis if kanji['grade'] in JINMEIYOU_GRADES]

    for kanji in kanjis:
        with codecs.open(KANJI_DIR + kanji['kanji'], 'w', 'utf8') as f:
            json.dump(kanji, f, ensure_ascii=False)

    for reading in readings:
        with codecs.open(READING_DIR + reading['reading'], 'w', 'utf8') as f:
            json.dump(reading, f, ensure_ascii=False)

    with codecs.open(KANJI_DIR + 'all', 'w', 'utf8') as f:
        json.dump(all_kanji, f, ensure_ascii=False)

    with codecs.open(KANJI_DIR + 'jouyou', 'w', 'utf8') as f:
        json.dump(jouyou_kanji, f, ensure_ascii=False)

    with codecs.open(KANJI_DIR + 'joyo', 'w', 'utf8') as f:
        json.dump(jouyou_kanji, f, ensure_ascii=False)

    with codecs.open(KANJI_DIR + 'jinmeiyou', 'w', 'utf8') as f:
        json.dump(jinmeiyou_kanji, f, ensure_ascii=False)

    with codecs.open(KANJI_DIR + 'jinmeiyo', 'w', 'utf8') as f:
        json.dump(jinmeiyou_kanji, f, ensure_ascii=False)

    for grade in JOUYOU_GRADES:
        grade_kanji = [kanji['kanji'] for kanji in kanjis if kanji['grade'] == grade]
        with codecs.open(KANJI_DIR + 'grade-' + grade, 'w', 'utf8') as f:
            json.dump(grade_kanji, f, ensure_ascii=False)
