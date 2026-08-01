import itertools
from dataclasses import dataclass, asdict


@dataclass(frozen=True, order=True)
class Reading():
    reading: str
    restrictions: tuple[str]
    priorities: tuple[str]


@dataclass(frozen=True, order=True)
class KanjiForm():
    form: str
    priorities: tuple[str]


@dataclass(frozen=True, order=True)
class Meaning():
    glosses: tuple[str]


# A variant is only as common as its rarer half. See CHANGELOG.md
def variant_priorities(
        kanji_form,
        reading,
        any_form_has_priority,
        any_reading_has_priority,
        ):
    if any_form_has_priority and not kanji_form.priorities:
        return ()
    if any_reading_has_priority and not reading.priorities:
        return ()
    return tuple(sorted(set(kanji_form.priorities) | set(reading.priorities)))


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

        any_form_has_priority = any([k for k, r in combinations if k.priorities])
        any_reading_has_priority = any([r for k, r in combinations if r.priorities])

        return [{
            'written': kanji_form.form,
            'pronounced': reading.reading,
            'priorities': variant_priorities(
                kanji_form,
                reading,
                any_form_has_priority,
                any_reading_has_priority,
                ),
            } for kanji_form, reading in combinations]
