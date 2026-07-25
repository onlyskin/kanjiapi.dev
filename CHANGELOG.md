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
- add an `-enriched` counterpart to every `/kanji/{list}` endpoint (e.g.
  `/kanji/joyo-enriched`), containing the full kanji object for each character
  instead of the character on its own
    - the enriched list is in the same order as the plain list
