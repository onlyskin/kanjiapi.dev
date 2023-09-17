import os
import ujson
from collections import defaultdict, OrderedDict
from lxml import etree
from zipfile import ZipFile, ZIP_DEFLATED


from .entry_data import word_dict
from .canonicalise import canonicalise
from .unihan import joyo_list, jinmeiyo_list, compatibility_variant
from .heisig import heisig_keyword, all_heisig
from .grades import grade_to_kanji_list, all_kyoiku, grade_for_char


NANORI = etree.XPath('./reading_meaning//nanori')
ON_READINGS = etree.XPath('./reading_meaning//reading[@r_type="ja_on"]')
KUN_READINGS = etree.XPath('./reading_meaning//reading[@r_type="ja_kun"]')
MEANINGS = etree.XPath('./reading_meaning//meaning[not(@m_lang)]')
STROKE_COUNT = etree.XPath('./misc/stroke_count')
CODEPOINT = etree.XPath('.//cp_value[@cp_type="ucs"]')
JLPT = etree.XPath('./misc/jlpt')
LITERAL = etree.XPath('literal')


def nanori(character):
    readings = NANORI(character)
    return [reading.text for reading in readings]


def on_readings(character):
    readings = ON_READINGS(character)
    return [reading.text for reading in readings]


def kun_readings(character):
    readings = KUN_READINGS(character)
    return [reading.text for reading in readings]


def meanings(character):
    meanings = MEANINGS(character)
    return [meaning.text for meaning in meanings]


def stroke_count(character):
    return int(STROKE_COUNT(character)[0].text)


def unicode_codepoint(character):
    return CODEPOINT(character)[0].text.upper()


def jlpt(character):
    try:
        return int(JLPT(character)[0].text)
    except (AttributeError, IndexError):
        return None


def literal(character):
    return LITERAL(character)[0].text


def grade(character_literal):
    if character_literal in all_kyoiku():
        return grade_for_char(character_literal)
    elif character_literal in joyo_list():
        return 8
    elif character_literal in jinmeiyo_list():
        return 9
    else:
        return None


def kanji_data(character):
    character_literal = literal(character)
    notes = []

    fields = [
        ('kanji', character_literal),
        ('grade', grade(character_literal)),
        ('stroke_count', stroke_count(character)),
        ('meanings', meanings(character)),
        ('kun_readings', kun_readings(character)),
        ('on_readings', on_readings(character)),
        ('name_readings', nanori(character)),
        ('jlpt', jlpt(character)),
        ('unicode', unicode_codepoint(character)),
        ('heisig_en', heisig_keyword(character_literal)),
    ]

    if CJK_compatibility(character_literal):
        try:
            fields.append(
                ('unihan_cjk_compatibility_variant', compatibility_variant(character_literal)),
            )
            notes.append(f'The character `{character_literal}` is in the Unicode CJK Compatibility block. The unified codepoint for this character can be found in this response in the field `unihan_cjk_compatibility_variant`. To learn more, look at the kanjiapi.dev `README.md`')
        except KeyError:
            pass

    fields.append(('notes', notes))
    return OrderedDict(fields)


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


def CJK_compatibility(kanji):
    return u'\uF900' <= kanji <= u'\uFAFF'


def dump_json(filename, obj):
    with open(filename, 'w', encoding='utf8') as f:
        ujson.dump(obj, f, ensure_ascii=False)


def main():
    VERSION_PATH = 'v1'
    SITE_PATH = f'out/site'
    OUT_PATH = f'out/{VERSION_PATH}'
    KANJI_DIR = f'{OUT_PATH}/kanji/'
    CJK_KANJI_DIR = f'{OUT_PATH}/kanji_cjk/'
    WORD_DIR = f'{OUT_PATH}/words/'
    CJK_WORD_DIR = f'{OUT_PATH}/words_cjk/'
    READING_DIR = f'{OUT_PATH}/reading/'

    kanjidic_root = etree.parse('kanjidic2.xml')
    jmdict_entries = etree.parse('JMDict').xpath('//entry')

    characters = kanjidic_root.xpath('./character')
    kanji_to_entries = word_dict(jmdict_entries)

    kanjis = [kanji_data(character) for character in characters]

    readings = reading_data(kanjis)

    words = {}
    for kanji in kanjis:
        if CJK_compatibility(kanji['kanji']):
            dump_json(CJK_KANJI_DIR + kanji['kanji'], canonicalise(kanji))
        else:
            dump_json(KANJI_DIR + kanji['kanji'], canonicalise(kanji))
        try:
            entries = kanji_to_entries[kanji['kanji']]
            entry_words = tuple(canonicalise([entry.words() for entry in entries]))
            if CJK_compatibility(kanji['kanji']):
                dump_json(CJK_WORD_DIR + kanji['kanji'], entry_words)
            else:
                dump_json(WORD_DIR + kanji['kanji'], entry_words)
            words[kanji['kanji']] = entry_words
        except KeyError:
            continue

    for reading in readings:
        dump_json(READING_DIR + reading['reading'], canonicalise(reading))

    with ZipFile(f'{SITE_PATH}/kanjiapi_full.zip', 'w', compression=ZIP_DEFLATED) as archive:
        api_data_download = {
            'kanjis': {kanji['kanji']: kanji for kanji in kanjis},
            'readings': {reading['reading']: reading for reading in readings},
            'words': words,
        }
        json_filename = f'{SITE_PATH}/kanjiapi_full.json'

        dump_json(json_filename, canonicalise(api_data_download))
        archive.write(json_filename, arcname='kanjiapi_full.json')
        os.remove(json_filename)

    for grade_numeral, grade_kanji in grade_to_kanji_list().items():
        dump_json(f'{KANJI_DIR}grade-{grade_numeral}', canonicalise(grade_kanji))
    high_school_kanji = [k for k in joyo_list() if k not in all_kyoiku()]
    dump_json(f'{KANJI_DIR}grade-8', canonicalise(high_school_kanji))
    dump_json(f'{KANJI_DIR}kyouiku', canonicalise(all_kyoiku()))
    dump_json(f'{KANJI_DIR}kyoiku', canonicalise(all_kyoiku()))

    all_kanji = [kanji['kanji'] for kanji in kanjis]
    dump_json(KANJI_DIR + 'all', canonicalise(all_kanji))
    dump_json(KANJI_DIR + 'jouyou', canonicalise(joyo_list()))
    dump_json(KANJI_DIR + 'joyo', canonicalise(joyo_list()))
    dump_json(KANJI_DIR + 'jinmeiyou', canonicalise(jinmeiyo_list()))
    dump_json(KANJI_DIR + 'jinmeiyo', canonicalise(jinmeiyo_list()))
    dump_json(KANJI_DIR + 'heisig', canonicalise(all_heisig()))
