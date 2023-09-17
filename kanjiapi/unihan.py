from functools import cache


@cache
def load_unihan_file(filename):
    def is_content_line(line):
        return line and line[0] != '#'

    with open(filename, 'r') as f:
        all_lines = [l.split('\t')
                     for l in f.read().split('\n')
                     if is_content_line(l)]

    return all_lines


@cache
def load_unihan_irg_sources():
    return load_unihan_file('Unihan_IRGSources.txt')


@cache
def load_unihan_other_mappings():
    return load_unihan_file('Unihan_OtherMappings.txt')


@cache
def unicode_to_char(unicode_string):
    raw_code = unicode_string.partition('<')[0].replace('U+', '')
    return chr(int(raw_code, 16))


def line_to_character(line):
    return unicode_to_char(line[0])


@cache
def joyo_list():
    def is_joyo_line(line):
        return line[1] == 'kJoyoKanji'

    return [line_to_character(line)
            for line in load_unihan_other_mappings()
            if is_joyo_line(line)]


@cache
def jinmeiyo_list():
    def is_jinmeiyo_line(line):
        return line[1] == 'kJinmeiyoKanji'

    return [line_to_character(line)
            for line in load_unihan_other_mappings()
            if is_jinmeiyo_line(line)]


@cache
def compatibility_char_to_unified_char():
    def isCompatibilityVariantLine(line):
        return line[1] == 'kCompatibilityVariant'

    def line_to_compatibility_pair(line):
        return (unicode_to_char(line[0]), unicode_to_char(line[2]))

    pairs = [line_to_compatibility_pair(line)
             for line in load_unihan_irg_sources()
             if isCompatibilityVariantLine(line)]

    return {compatibility_char: unified_char
            for compatibility_char, unified_char in pairs}


def compatibility_variant(char):
    return compatibility_char_to_unified_char()[char]
