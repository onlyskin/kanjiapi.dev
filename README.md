## Installation:
`brew install xq`

Save the dictionary file `kanjidic2.xml` from [http://www.edrdg.org/wiki/index.php/KANJIDIC_Project](Kanjidic) to the root of the project.

## Build:
`make`

## JQ recipes:

Print out all kanji as `literal: meaning`
`jq '.kanjidic2.character | map([.literal, .reading_meaning.rmgroup.meaning])[] | if (.[1]|type)=="array" then "\(.[0]): \(.[1][0])" else "\(.[0]): \(.[1])" end'`

Count kanji with n meanings
`cat out/kanjidic2.json | jq '.kanjidic2.character[] | .reading_meaning.rmgroup.meaning | if (.|type)=="array" then map(select((.|type)=="string")) else [.] end | length' | sort -V | uniq -c`
