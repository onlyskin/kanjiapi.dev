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

def data(character):
    reading = readings(character)

    return {
            'kanji': character['literal'],
            'grade': grade(character),
            'stroke_count': stroke_count(character),
            'meanings': meanings(character),
            'on_readings': reading['on'],
            'kun_readings': reading['kun'],
            'name_readings': nanori(character),
            }

def is_heisig(character):
    try:
        dictionary_refs = character['dic_number']['dic_ref']
        if isinstance(dictionary_refs, dict):
            dictionary_refs = [dictionary_refs]

        return any(map(lambda ref: ref['@dr_type'] == 'heisig', dictionary_refs))
    except KeyError:
        return False

def reading_data(kanji_data):
    readings = {}

    for kanji in kanji_data:
        literal = kanji['kanji']
        for reading in kanji['kun_readings'] + kanji['on_readings']:
            if reading not in readings:
                readings[reading] = {'regular': [], 'name': []}
            readings[reading]['regular'].append(literal)
        for reading in kanji['name_readings']:
            if reading not in readings:
                readings[reading] = {'regular': [], 'name': []}
            readings[reading]['name'].append(literal)

    return [{'reading': reading, 'name': data['name'], 'kanji': data['regular']} for reading, data in readings.items()]

if __name__ == '__main__':
    with codecs.open('out/kanjidic2.json', 'r', 'utf8') as f:
        characters = json.load(f)['kanjidic2']['character']

    kanji_data = [data(character) for character in characters if is_heisig(character)]

    for datum in kanji_data:
        with codecs.open('out/kanji/' + datum['kanji'] + '.json', 'w', 'utf8') as f:
            json.dump(datum, f, ensure_ascii=False)

    readings = reading_data(kanji_data)

    for reading in readings:
        with codecs.open('out/reading/' + reading['reading'] + '.json', 'w', 'utf8') as f:
            json.dump(reading, f, ensure_ascii=False)
