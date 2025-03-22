from functools import cache
import csv


@cache
def grade_to_kanji_list():
    with open('grades.tsv') as f:
        kanji_by_grade = {int(grade): list(kanji_list)
                          for grade, kanji_list
                          in csv.reader(f, delimiter='\t')}
    return kanji_by_grade


@cache
def kanji_to_grade():
    return {kanji: grade for grade, kanji_list in
            grade_to_kanji_list().items()
            for kanji in kanji_list}


def grade_for_char(character_literal):
    return kanji_to_grade()[character_literal]


def all_in_grade(grade):
    return grade_to_kanji_list()[grade]


@cache
def all_kyoiku():
    return [kanji for kanji_list in
            grade_to_kanji_list().values()
            for kanji in kanji_list]

def is_kyoiku(character_literal):
    return character_literal in all_kyoiku()
