import codecs
import sys
import json
from collections import defaultdict, OrderedDict

def is_string(x):
    return isinstance(x, basestring)

def meanings(character):
    try:
        meanings = character['reading_meaning']['rmgroup']['meaning']
    except KeyError:
        return []

    if is_string(meanings):
        meanings = [meanings]

    return filter(is_string, meanings)


def grade(character):
    try:
        return character['misc']['grade']
    except KeyError:
        return None

def stroke_count(character):
    try:
        strokes = character['misc']['stroke_count']
        if not is_string(strokes):
            return strokes[0]

        return strokes
    except KeyError, IndexError:
        return None

def readings(character):
    on_readings = []
    kun_readings = []

    try:
        readings = character['reading_meaning']['rmgroup']['reading']
    except KeyError:
        pass
    else:
        if isinstance(readings, dict):
            readings = [readings]

        for reading in readings:
            if reading.get('@r_type') == 'ja_on':
                on_readings.append(reading['#text'])
            elif reading.get('@r_type') == 'ja_kun':
                kun_readings.append(reading['#text'])

    return { 'on': on_readings, 'kun': kun_readings }

def nanori(character):
    try:
        readings = character['reading_meaning']['nanori']
    except KeyError:
        return []

    if is_string(readings):
        readings = [readings]

    return readings

def kanji_data(character):
    reading = readings(character)

    return OrderedDict([
            ('kanji', character['literal']),
            ('grade', grade(character)),
            ('stroke_count', stroke_count(character)),
            ('meanings', meanings(character)),
            ('kun_readings', reading['kun']),
            ('on_readings', reading['on']),
            ('name_readings', nanori(character)),
            ])

def is_heisig(character):
    try:
        dictionary_refs = character['dic_number']['dic_ref']
    except KeyError:
        return False

    if isinstance(dictionary_refs, dict):
        dictionary_refs = [dictionary_refs]

    return any(ref['@dr_type'] == 'heisig' for ref in dictionary_refs)

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
    return u'\uF900' <= character['literal'] <= u'\uFAFF'

if __name__ == '__main__':
    VERSION_PATH = 'v1'
    KANJI_DIR = 'out/' + VERSION_PATH + '/kanji/'
    READING_DIR = 'out/' + VERSION_PATH + '/reading/'
    JOUYOU_GRADES = ['1', '2', '3', '4', '5', '6', '8']
    JINMEIYOU_GRADES = ['9', '10']

    with codecs.open('out/kanjidic2.json', 'r', 'utf8') as f:
        characters = json.load(f)['kanjidic2']['character']

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
