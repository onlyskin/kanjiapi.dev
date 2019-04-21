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

def data(character):
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

def reading_data(kanji_data):
    readings = defaultdict(lambda: {'regular': [], 'name': []})

    for kanji in kanji_data:
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

if __name__ == '__main__':
    with codecs.open('out/kanjidic2.json', 'r', 'utf8') as f:
        characters = json.load(f)['kanjidic2']['character']

    kanji_data = [data(character) for character in characters]

    for datum in kanji_data:
        with codecs.open('out/site/kanji/' + datum['kanji'], 'w', 'utf8') as f:
            json.dump(datum, f, ensure_ascii=False)

    readings = reading_data(kanji_data)

    for reading in readings:
        with codecs.open('out/site/reading/' + reading['reading'], 'w', 'utf8') as f:
            json.dump(reading, f, ensure_ascii=False)
