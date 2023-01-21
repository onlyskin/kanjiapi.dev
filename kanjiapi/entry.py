import json
import itertools


class Reading():
    __slots__ = ['reading', 'restrictions']

    def __init__(self, reading, restrictions):
        self.reading = reading
        self.restrictions = restrictions

    def __eq__(self, other):
        return (self.reading == other.reading and
                self.restrictions == other.restrictions)

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return f'{{reading:{self.reading},' \
                f' restrictions:{str(self.restrictions)}}}'

    def __lt__(self, other):
        return self.reading < other.reading

    def to_json(self):
        return {
                'reading': self.reading,
                'restrictions': self.restrictions,
                }


class KanjiForm():
    __slots__ = ['form', 'priorities']

    def __init__(self, form, priorities):
        self.form = form
        self.priorities = priorities

    def __eq__(self, other):
        return (self.form == other.form and
                self.priorities == other.priorities)

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return f'{{form:{self.form}, priorities:{str(self.priorities)}}}'

    def __lt__(self, other):
        return self.form < other.form

    def to_json(self):
        return {
                'form': self.form,
                'priorities': self.priorities,
                }


class Meaning():
    __slots__ = ['glosses']

    def __init__(self, glosses):
        self.glosses = glosses

    def __eq__(self, other):
        return (self.glosses == other.glosses)

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return f'{{glosses:{str(self.glosses)}}}'

    def __lt__(self, other):
        return self.glosses < other.glosses

    def to_json(self):
        return {
                'glosses': self.glosses,
                }

    def toDict(self):
        return self.to_json()


class Entry():
    __slots__ = ['kanji_forms', 'readings', 'meanings', 'words']

    def __init__(self, kanji_forms, readings, meanings):
        self.kanji_forms = kanji_forms
        self.readings = readings
        self.meanings = meanings
        self.words = self._words()

    def __eq__(self, other):
        return (self.kanji_forms == other.kanji_forms and
                self.readings == other.readings and
                self.meanings == other.meanings)

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return f'{{\nkanji_forms: {str(self.kanji_forms)},' \
                f'\nreadings: {str(self.readings)},' \
                f'\nmeanings: {str(self.meanings)}}}'

    def __lt__(self, other):
        return self.kanji_forms < other.kanji_forms

    def to_json(self):
        return self.words

    def toDict(self):
        return self.to_json()

    def _words(self):
        return {
                'variants': self._variants(),
                'meanings': self.meanings,
                }

    def _variants(self):
        combinations = [
                [kanji_form, reading] for kanji_form, reading
                in itertools.product(self.kanji_forms, self.readings)
                if (
                    not reading.restrictions
                    or kanji_form.form in reading.restrictions
                    )
                ]

        return [{
            'written': kanji_form.form,
            'pronounced': reading.reading,
            'priorities': tuple(sorted(kanji_form.priorities))
            } for kanji_form, reading in combinations]
