def load_unihan(all_lines=[]):
    def is_content_line(line):
        return line and line[0] != '#'

    if not all_lines:
        with open('Unihan_OtherMappings.txt', 'r') as f:
            all_lines.extend([
                    l.split('\t')
                    for l in f.read().split('\n')
                    if is_content_line(l)
            ])

    return all_lines
    

def unicode_to_char(unicode_string):
    raw_code = unicode_string.replace('U+', '')
    return chr(int(raw_code, 16))


def line_to_character(line):
    return unicode_to_char(line[0])


def joyo_list(chars=[]):
    if not chars:
        def is_joyo_line(line):
            return line[1] == 'kJoyoKanji'

        joyo_lines = list(filter(is_joyo_line, load_unihan()))
        chars.extend(list(map(line_to_character, joyo_lines)))

    return chars


def jinmeiyo_list(chars=[]):
    if not chars:
        def is_jinmeiyo_line(line):
            return line[1] == 'kJinmeiyoKanji'

        jinmeiyo_lines = list(filter(is_jinmeiyo_line, load_unihan()))
        chars.extend(list(map(line_to_character, jinmeiyo_lines)))

    return chars
