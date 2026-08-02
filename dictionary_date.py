"""Report the release date a source dictionary declares about itself.

Used to name archived copies after the release they came from rather than the
day they happened to be replaced. The four sources are on independent release
cycles, so a single date for a whole batch would be wrong for most of it.

Each format states its date differently and all of them state it near the top,
so this reads a prefix of the file rather than parsing it. Prints the date, or
'unknown' for a file that declares none.

Run as `python dictionary_date.py <file>`.
"""
import re
import sys


PREFIX_BYTES = 512 * 1024

PATTERNS = [
        r'<date_of_creation>(\d{4}-\d{2}-\d{2})</date_of_creation>',
        r'created="(\d{4}-\d{2}-\d{2})"',
        r'created:\s*(\d{4}-\d{2}-\d{2})',
        r'#\s*Date:\s*(\d{4}-\d{2}-\d{2})',
        ]


def source_date(path):
    with open(path, encoding='utf8', errors='replace') as f:
        prefix = f.read(PREFIX_BYTES)

    for pattern in PATTERNS:
        match = re.search(pattern, prefix)
        if match:
            return match.group(1)

    return 'unknown'


if __name__ == '__main__':
    print(source_date(sys.argv[1]))
