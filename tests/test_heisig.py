from kanjiapi.heisig import heisig_keyword, all_heisig


def test_heisig_keyword():
    assert heisig_keyword('付') == 'adhere'
    assert heisig_keyword('鼈') == 'snapping turtle'


def test_heisig_list():
    assert '付' in all_heisig()
