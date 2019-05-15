from collections import defaultdict
from lxml import etree

from .entry import Entry, Meaning, KanjiForm, Reading


SENSES = etree.XPath('./sense')
GLOSSES = etree.XPath('./gloss[not(@xml:lang)]/text()')
R_ELE = etree.XPath('./r_ele')
REB = etree.XPath('./reb')
RE_RESTR = etree.XPath('./re_restr')
KE_PRI = etree.XPath('./ke_pri')
KEB = etree.XPath('./keb')
K_ELE = etree.XPath('./k_ele')


def reading_from(r_ele):
    reading = REB(r_ele)[0].text
    restrictions = [
            restriction.text
            for restriction in RE_RESTR(r_ele)
            ]
    return Reading(reading, restrictions)


def readings(kanji_forms, entry):
    return [reading_from(r_ele) for r_ele in R_ELE(entry)]


def meanings(entry):
    meanings = []
    for sense in SENSES(entry):
        glosses = GLOSSES(sense)
        if glosses:
            meanings.append(Meaning(glosses))
    return meanings


def k_ele_priorities(element):
    return set([e.text for e in KE_PRI(element)])


def kanji_from(k_ele):
    form = KEB(k_ele)[0].text
    priorities = k_ele_priorities(k_ele)
    return KanjiForm(form, priorities)


def make_entry(entry):
    kanji_forms = [kanji_from(k_ele) for k_ele in K_ELE(entry)]
    return Entry(
            kanji_forms,
            readings(kanji_forms, entry),
            meanings(entry),
            )


def is_kana(character):
    return (
            '\u3040' <= character <= '\u30FF' or
            '\uFF00' <= character <= '\uFFEF' or
            '\u31F0' <= character <= '\u31FF'
            )


def word_dict(xml_entries):
    kanji_to_entries = defaultdict(set)

    for xml_entry in xml_entries:
        entry = make_entry(xml_entry)
        for kanji_form in entry.kanji_forms:
            for char in kanji_form.form:
                if not is_kana(char):
                    kanji_to_entries[char].add(entry)

    return kanji_to_entries


if __name__ == '__main__':
    root = etree.parse('JMDict')
    xml_entries = root.xpath('//entry')
    kanji_to_entries = word_dict(xml_entries)
    print(kanji_to_entries['猫'])
