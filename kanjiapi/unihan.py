from functools import cache


@cache
def load_unihan():
    def is_content_line(line):
        return line and line[0] != '#'

    with open('Unihan_OtherMappings.txt', 'r') as f:
        all_lines = [l.split('\t')
                     for l in f.read().split('\n')
                     if is_content_line(l)]

    return all_lines
    

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
            for line in load_unihan()
            if is_joyo_line(line)]


@cache
def jinmeiyo_list():
    def is_jinmeiyo_line(line):
        return line[1] == 'kJinmeiyoKanji'

    return [line_to_character(line)
            for line in load_unihan()
            if is_jinmeiyo_line(line)]
