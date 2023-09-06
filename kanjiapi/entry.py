import itertools
from dataclasses import dataclass, asdict


@dataclass(frozen=True, order=True)
class Reading():
    reading: str
    restrictions: tuple[str]


@dataclass(frozen=True, order=True)
class KanjiForm():
    form: str
    priorities: tuple[str]


@dataclass(frozen=True, order=True)
class Meaning():
    glosses: tuple[str]


@dataclass(frozen=True, order=True)
class Entry():
    kanji_forms: tuple[KanjiForm]
    readings: tuple[Reading]
    meanings: tuple[Meaning]

    def words(self):
        return {
                'variants': self._variants(),
                'meanings': [asdict(meaning) for meaning in self.meanings],
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
            'priorities': kanji_form.priorities,
            } for kanji_form, reading in combinations]
