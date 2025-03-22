from kanjiapi.grades import all_in_grade, all_kyoiku, grade_for_char, grade_to_kanji_list


def test_grade_1():
    assert len(all_in_grade(1)) == 80


def test_grade_2():
    assert len(all_in_grade(2)) == 160


def test_grade_3():
    assert len(all_in_grade(3)) == 200


def test_grade_4():
    assert len(all_in_grade(4)) == 200


def test_grade_5():
    assert len(all_in_grade(5)) == 185


def test_grade_6():
    assert len(all_in_grade(6)) == 181


def test_all_kyoiku():
    assert len(all_kyoiku()) == 1006


def test_grade_for_char():
    assert grade_for_char('羽') == 2


def test_no_duplication_between_grades():
    full_list = [k for ks in grade_to_kanji_list().values() for k in ks]
    assert len(full_list) == len(set(full_list))
