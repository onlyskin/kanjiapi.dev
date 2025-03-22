from functools import cache
import csv


@cache
def jlpt_level_to_kanji_list():
    with open('jlpt.tsv') as f:
        kanji_by_jlpt_level = {int(level): list(kanji_list)
                               for level, kanji_list
                               in csv.reader(f, delimiter='\t')}
    return kanji_by_jlpt_level


@cache
def kanji_to_jlpt_level():
    return {kanji: level for level, kanji_list in
            jlpt_level_to_kanji_list().items()
            for kanji in kanji_list}


def jlpt_level_for_char(character_literal):
    return kanji_to_jlpt_level()[character_literal]


def all_jlpt():
    return [k for ks in jlpt_level_to_kanji_list().values() for k in ks]
