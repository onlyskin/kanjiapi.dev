from kanjiapi.unihan import joyo_list, jinmeiyo_list


def test_joyo_list_has_2136_chars_plus_four_duplicated():
    assert len(joyo_list()) == 2136 + 4


def test_joyo_list_doesnt_have_removed_chars():
    for kanji in ('勺', '銑', '脹', '錘', '匁'):
        assert kanji not in joyo_list()


def test_joyo_list_has_both_versions_of_non_jis_chars():
    joyo_kanji = joyo_list()
    for kanji in ('𠮟', '塡', '剝', '頰', '叱', '填', '剥', '頬'):
        assert kanji in joyo_list()


def test_jinmeiyo_list_has_all_863():
    assert len(jinmeiyo_list()) == 863


def test_jinmeiyo_list_has_old_forms_of_CJK_chars_and_not_new_forms():
    assert '\u6D77' not in jinmeiyo_list()
    assert '\uFA45' in jinmeiyo_list()
    assert '\u6F22' not in jinmeiyo_list()
    assert '\uFA47' in jinmeiyo_list()


def test_jinmeiyo_list_has_recent_addition():
    assert '渾' in jinmeiyo_list()
