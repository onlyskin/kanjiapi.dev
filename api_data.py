import codecs
import sys
import json

def is_string(x):
    return isinstance(x, basestring)

def meanings(character):
    try:
        meanings = character['reading_meaning']['rmgroup']['meaning']
        if is_string(meanings):
            meanings = [meanings]

        return filter(is_string, meanings)

    except KeyError:
        return None

def grade(character):
    try:
        return character['misc']['grade']
    except KeyError:
        return None

def stroke_count(character):
    try:
        return character['misc']['stroke_count']
    except KeyError:
        return None

def readings(character):
    on_readings = []
    kun_readings = []

    try:
        readings = character['reading_meaning']['rmgroup']['reading']

        if isinstance(readings, dict):
            readings = [readings]

        for reading in readings:
            if reading['@r_type'] == 'ja_on':
                on_readings.append(reading['#text'])
            elif reading['@r_type'] == 'ja_kun':
                kun_readings.append(reading['#text'])
    except KeyError:
        pass

    return { 'on': on_readings, 'kun': kun_readings }

def nanori(character):
    try:
        readings = character['reading_meaning']['nanori']
        if is_string(readings):
            readings = [readings]

        return readings
    except KeyError:
        return []

def json_data(character):
    reading = readings(character)

    return {
            'kanji': character['literal'],
            'grade': grade(character),
            'stroke_count': stroke_count(character),
            'meanings': meanings(character),
            'on_readings': reading['on'],
            'kun_readings': reading['kun'],
            'nanori': nanori(character),
            }

def is_heisig(character):
    try:
        dictionary_refs = character['dic_number']['dic_ref']
        if isinstance(dictionary_refs, dict):
            dictionary_refs = [dictionary_refs]

        return any(map(lambda ref: ref['@dr_type'] == 'heisig', dictionary_refs))
    except KeyError:
        return False

if __name__ == '__main__':
    with codecs.open('out/kanjidic2.json', 'r', 'utf8') as f:
        characters = json.load(f)['kanjidic2']['character']

    data = [json_data(character) for character in characters if is_heisig(character)]

    for datum in data:
        with codecs.open('out/json/' + datum['kanji'] + '.json', 'w', 'utf8') as f:
            json.dump(datum, f, ensure_ascii=False)
