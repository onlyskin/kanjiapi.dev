from functools import cache
import csv


@cache
def heisig_dict():
    with open('heisig.tsv') as f:
        heisig_keywords = {character: keyword
                           for character, keyword
                           in csv.reader(f, delimiter='\t')}
    heisig_keywords.update({
        '𠮟': 'scold [alt]',
        '塡': 'stuff up [alt]',
        '剝': 'peel off [alt]',
        '頰': 'cheek [alt]',
    })
    return heisig_keywords


def heisig_keyword(character_literal):
    return heisig_dict().get(character_literal)


def all_heisig():
    return list(heisig_dict().keys())
