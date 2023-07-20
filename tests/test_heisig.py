from kanjiapi.heisig import heisig_keyword, all_heisig


def test_heisig_keyword():
    assert heisig_keyword('付') == 'adhere'
    assert heisig_keyword('鼈') == 'snapping turtle'


def test_heisig_list():
    assert '付' in all_heisig()


def test_treats_four_extra_joyos_as_their_heisig_equivalents():
    assert heisig_keyword('叱') == 'scold'
    assert heisig_keyword('𠮟') == 'scold [alt]'
    assert heisig_keyword('填') == 'stuff up'
    assert heisig_keyword('塡') == 'stuff up [alt]'
    assert heisig_keyword('剥') == 'peel off'
    assert heisig_keyword('剝') == 'peel off [alt]'
    assert heisig_keyword('頬') == 'cheek'
    assert heisig_keyword('頰') == 'cheek [alt]'

    for kanji in ('叱', '𠮟', '填', '塡', '剥', '剝', '頬', '頰'):
        assert kanji in all_heisig()
