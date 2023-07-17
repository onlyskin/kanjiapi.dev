import csv


def heisig_dict(heisig_keywords={}):
    if not heisig_keywords:
        with open('heisig.tsv') as f:
            heisig_keywords.update({ character: keyword
                                     for character, keyword
                                     in csv.reader(f, delimiter='\t') })
    return heisig_keywords


def heisig_keyword(character_literal):
    return heisig_dict().get(character_literal)


def all_heisig():
    return list(heisig_dict().keys())
