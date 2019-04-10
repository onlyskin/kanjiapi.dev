## Requirements:
`python 2.7`
`brew`
`make`

## Installation:
`brew install xq`

Save the kanji dictionary file `kanjidic2.xml` from [EDRDG](http://www.edrdg.org/wiki/index.php/KANJIDIC_Project) to the root of the project.

Save the jmdict dictionary file `JMdict_e` from [EDRDG](http://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project) to the root of the project.

## Build:
`make`

## JQ recipes:

Print out all kanji as `literal: meaning`
`jq '.kanjidic2.character | map([.literal, .reading_meaning.rmgroup.meaning])[] | if (.[1]|type)=="array" then "\(.[0]): \(.[1][0])" else "\(.[0]): \(.[1])" end'`

Count kanji with n meanings
`cat out/kanjidic2.json | jq '.kanjidic2.character[] | .reading_meaning.rmgroup.meaning | if (.|type)=="array" then map(select((.|type)=="string")) else [.] end | length' | sort -V | uniq -c`

## Deployment:
`aws s3 cp out/kanji s3://kanjiapi/kanji --region eu-west-1 --acl public-read --content-type 'application/json' --recursive`
`aws s3 cp out/reading s3://kanjiapi/reading --region eu-west-1 --acl public-read --content-type 'application/json' --recursive`
