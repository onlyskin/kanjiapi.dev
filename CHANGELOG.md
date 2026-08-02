# Changelog

All notable changes to this project will be documented in this file.

Any new feature should be recorded here: new endpoints, new or renamed fields,
and changes to the data a field can hold. Changes which don't affect what the
API serves — internal refactors, dependency updates, and site-only changes —
are deliberately left out.

## [Unreleased]

## [Released under `/v1`]
- canonicalise api data
    - enables easier partial updates to the live API bucket
    - the response data returned on all API endpoints is now canonicalised,
      meaning all dicts are recursively sorted by key and then by value, and
      most lists are also recursively sorted
    - the lists of glosses under the `/words` endpoints are not sorted as these
      are in rough order of importance in the source data
- change jouyou and jinmeiyou list source of truth to Unihan_OtherMappings.txt from Unihan.zip from [Unicode](https://www.unicode.org/versions/components-15.0.0.html)
    - this corrects some kanji which were on the wrong list in KANJIDIC
    - this adds four alternate unicode characters to `/kanji/jouyou` lists (see
      `README.md - List of joyo kanji` for more information
    - this adds CJK compatibility unicode characters to `/kanji/jinmeiyou` lists to bring it up to the full list
    - adds `unihan_cjk_compatibility_variant` field to the CJK compatibility
      jinmeiyo characters referencing the normalised equivalent of the
      character
    - add `notes` field to all `/kanji/{character}` endpoints
    - change all jinmeiyo kanji to have the grade `9`, instead of 9 or 10, (10
      indicated that a jinmeiyo character was in the compatibility block, but
      this information is now available by checking the
      `unihan_cjk_compatibility_variant` field, and anyway is by definition
      derivable from the unicode value itself)
- change `kanji/{character}` grade field to derive from [Ministry of Education list](https://www.mext.go.jp/a_menu/shotou/new-cs/youryou/syo/koku/001.htm) instead of KANJIDIC
- add `/kanji/kyouiku` and `/kanji/kyoiku` endpoints
- and `/kanji/heisig` endpoint listing all kanji with a Heisig keyword
- uppercase the value for the `unicode` field on `kanji/{character}` endpoints
- add `freq_mainichi_shinbun` field to the `/kanji/{character}` endpoints providing kanji frequency information from that analysis
- change the `jlpt` field on `/kanji/{character}` endpoints to derive from [Jonathan Waller's JLPT Resources page](https://www.tanos.co.uk/jlpt/) instead of KANJIDIC
    - the values now refer to the current five level test, so the field ranges
      over `1`-`5` (N1-N5) rather than the `1`-`4` of the pre-2010 test
    - the set of kanji which have a level at all has also changed
- add `/kanji/jlpt-1` through `/kanji/jlpt-5` endpoints listing the kanji for each JLPT level
- change the `priorities` field on `/words/{character}` variants to come from
  the reading rather than the written form, for entries where any reading
  carries priority information
    - entries where no reading has priority information continue to use the
      priorities of the written form
- change the `meanings` list to keep the order it has in the source dictionary
  rather than being sorted by value
    - both dictionaries put the primary sense of an entry first, so this affects
      the senses under `/words/{character}` and the KANJIDIC meanings under
      `/kanji/{character}` and its `-enriched` lists, e.g. `/kanji/親` now gives
      `parent` first rather than `dealer (cards)`
    - the glosses within a `/words` sense were already left unsorted
- change the `kun_readings`, `on_readings` and `name_readings` lists on
  `/kanji/{character}` endpoints and their `-enriched` lists to keep the order
  they have in KANJIDIC rather than being sorted by value
    - KANJIDIC lists the primary reading first, so e.g. `/kanji/生` now gives
      the on readings as `セイ, ショウ` rather than `ショウ, セイ`
- change the `variants` list on `/words/{character}` endpoints to keep the order
  of the written forms in JMdict rather than being sorted by value
    - JMdict lists the written forms of an entry from most to least common, so
      the first variant spelled with the character searched for is now the one
      to show for that word
    - sorting had put forms spelled with kana ahead of the full-kanji form they
      stand in for, since the kana blocks sit below the CJK ones in codepoint
      order, e.g. `親せき` ahead of `親戚`
- change the `priorities` field on `/words/{character}` variants to combine the
  priority information of the written form and the reading, rather than taking
  the reading's alone
    - a variant pairs one written form with one reading, and JMdict tags priority
      on each of those independently (`ke_pri` on the form, `re_pri` on the
      reading), so the field now reflects both rather than the reading only
    - where an entry tags some of its written forms and leaves others untagged,
      the untagged ones are now empty instead of inheriting the reading's
      priorities: `親せき` is now empty while `親戚` keeps
      `ichi1, news2, nf30`. This affects 8989 variants across JMdict, and is the
      reason a rare or search-only spelling used to look exactly as common as the
      entry's main one
    - where a variant's own written form and its own reading are both tagged, the
      field is now the union of the two rather than the reading's tags alone,
      e.g. `どの位/どのくらい` gains the form's `spec1` alongside the reading's
      `ichi1`. This affects 176 variants
    - three cases are unchanged. An entry that tags no written form anywhere
      still gives every variant its reading's priorities, as the reading is then
      the only information available. A reading left untagged in an entry that
      tags another reading is still empty, e.g. `雷/いかづち` beside
      `雷/かみなり`. An entry with no priorities anywhere is still empty
      throughout
- add an `-enriched` counterpart to every `/kanji/{list}` endpoint (e.g.
  `/kanji/joyo-enriched`), containing the full kanji object for each character
  instead of the character on its own
    - the enriched list is in the same order as the plain list
- add an `alternate_stroke_counts` field to the `/kanji/{character}` endpoints
  and their `-enriched` lists
    - KANJIDIC records more than one stroke count for 525 of the 13,108
      characters, and everything after the first was being discarded
    - the extra counts are common miscounts rather than equally correct
      alternatives, so `stroke_count` still holds the first and correct one, and
      the rest are useful for matching a count a learner arrived at, e.g.
      `/kanji/逢` keeps `stroke_count` 10 and gains `9, 11`
    - the field is an empty list for the 12,583 characters with a single count
