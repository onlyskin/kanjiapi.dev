from kanjiapi.jlpt import jlpt_level_for_char, jlpt_level_to_kanji_list, all_jlpt


def test_level_5():
    assert len(jlpt_level_to_kanji_list()[5]) == 79


def test_level_4():
    assert len(jlpt_level_to_kanji_list()[4]) == 166


def test_level_3():
    assert len(jlpt_level_to_kanji_list()[3]) == 367


def test_level_2():
    assert len(jlpt_level_to_kanji_list()[2]) == 367


def test_level_1():
    assert len(jlpt_level_to_kanji_list()[1]) == 1232


def test_all_jlpt():
    assert len(all_jlpt()) == 2211


def test_no_duplication_among_levels():
    assert len(all_jlpt()) == len(set(all_jlpt()))


def test_jlpt_level_for_char():
    assert jlpt_level_for_char('予') == 3
