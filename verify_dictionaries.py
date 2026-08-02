"""Sanity check freshly downloaded dictionaries before they replace the
installed ones.

A truncated or empty download that still happens to parse would rebuild the
whole API with data missing, and `gcloud storage rsync` would upload the result
without complaining. So compare each staged file against the one it is about to
replace and refuse anything that has lost a meaningful share of its content.

The Unihan files are checked by the fields kanjiapi actually reads rather than
by line count, because they carry many unrelated fields: Unicode 17.0 retired
the legacy national encoding mappings (kHKSCS, kKSC0, kKPS0 and friends), which
cost Unihan_OtherMappings.txt 17% of its lines while leaving kJoyoKanji and
kJinmeiyoKanji untouched.

Run as `python verify_dictionaries.py <staging_dir> <data_dir>`; exits non-zero
on failure, which stops the makefile recipe before the swap.
"""
import sys
import os
from lxml import etree


MINIMUM_RETAINED = 0.95

XML_COUNTS = {
        'kanjidic2.xml': './character',
        'JMdict_e_NG': '//entry',
        'JMnedict.xml': '//entry',
        }

UNIHAN_FIELDS = {
        'Unihan_OtherMappings.txt': ['kJoyoKanji', 'kJinmeiyoKanji'],
        'Unihan_IRGSources.txt': ['kCompatibilityVariant'],
        'Unihan_DictionaryLikeData.txt': [],
        'Unihan_Readings.txt': [],
        'Unihan_Variants.txt': [],
        }


def xml_count(path, xpath):
    return len(etree.parse(path).xpath(xpath))


def unihan_field_count(path, field):
    with open(path, encoding='utf8') as f:
        return sum(1 for line in f
                   if not line.startswith('#')
                   and line.strip()
                   and line.split('\t')[1] == field)


def unihan_line_count(path):
    with open(path, encoding='utf8') as f:
        return sum(1 for line in f if line.strip() and not line.startswith('#'))


def kanjidic_version(path):
    header = etree.parse(path).xpath('//header')[0]
    version = header.xpath('./database_version/text()')
    created = header.xpath('./date_of_creation/text()')
    return f'{version[0]} ({created[0]})'


def check(label, staged, installed, count):
    if not os.path.exists(staged):
        return [f'{label}: missing from the download']

    new = count(staged)
    if new == 0:
        return [f'{label}: nothing in the downloaded file']

    if not os.path.exists(installed):
        print(f'  {label}: {new} (new file, nothing to compare against)')
        return []

    old = count(installed)
    print(f'  {label}: {old} -> {new} ({new - old:+d})')
    if new < old * MINIMUM_RETAINED:
        return [
                f'{label}: {new} is under {MINIMUM_RETAINED:.0%} of the '
                f'installed {old}, refusing to replace it'
                ]
    return []


def main(staging, data_dir):
    print(f'verifying downloads in {staging}/')
    problems = []

    for name, xpath in XML_COUNTS.items():
        problems += check(
                name,
                os.path.join(staging, name),
                os.path.join(data_dir, name),
                lambda path, xpath=xpath: xml_count(path, xpath),
                )

    for name, fields in UNIHAN_FIELDS.items():
        staged = os.path.join(staging, name)
        installed = os.path.join(data_dir, name)
        if not fields:
            problems += check(name, staged, installed, unihan_line_count)
            continue
        for field in fields:
            problems += check(
                    f'{name} {field}',
                    staged,
                    installed,
                    lambda path, field=field: unihan_field_count(path, field),
                    )

    staged_kanjidic = os.path.join(staging, 'kanjidic2.xml')
    if os.path.exists(staged_kanjidic):
        print(f'  kanjidic2 release: {kanjidic_version(staged_kanjidic)}')

    if problems:
        print('\nrefusing to install:', file=sys.stderr)
        for problem in problems:
            print(f'  {problem}', file=sys.stderr)
        return 1

    print('all downloads look sane')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
