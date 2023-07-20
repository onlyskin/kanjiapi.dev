import csv


def grade_to_kanji_list(kanji_by_grade={}):
    if not kanji_by_grade:
        with open('grades.tsv') as f:
            kanji_by_grade.update({ int(grade): list(kanji_list)
                                     for grade, kanji_list
                                     in csv.reader(f, delimiter='\t') })
    return kanji_by_grade


def all_grades():
    return list(grade_to_kanji_list().keys())


def grade_for_char(character_literal, kanji_to_grade = {}):
    if not kanji_to_grade:
        kanji_to_grade.update({kanji: grade for grade, kanji_list in
                               grade_to_kanji_list().items()
                               for kanji in kanji_list})
    return kanji_to_grade[character_literal]


def all_in_grade(grade):
    return grade_to_kanji_list()[grade]


def all_kyoiku(chars=[]):
    if not chars:
        chars = [kanji for kanji_list in
                 grade_to_kanji_list().values()
                 for kanji in kanji_list]
    return chars

def is_kyoiku(character_literal):
    return character_literal in all_kyoiku()
