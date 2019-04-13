## Requirements:
Assumes `python 2.7`, `brew` and `make` are available.

## Setup:
`brew install xq`

Save the kanji dictionary file `kanjidic2.xml` from [EDRDG](http://www.edrdg.org/wiki/index.php/KANJIDIC_Project) to the root of the project.

Save the jmdict dictionary file `JMdict_e` from [EDRDG](http://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project) to the root of the project.

## Building:
`make`

## Deployment:
(Requires google cloud account access, also a good idea to run with `rsync -n` for dry-run first)
`gsutil -m -h "Content-Type:application/json" rsync -d out/kanji gs://kanjiapi-static/kanji`

## Renewing SSL certificate:
`./update_cert.sh`

## Useful JQ recipes:

Print out all kanji as `literal: meaning`
`jq '.kanjidic2.character | map([.literal, .reading_meaning.rmgroup.meaning])[] | if (.[1]|type)=="array" then "\(.[0]): \(.[1][0])" else "\(.[0]): \(.[1])" end'`

Count kanji with n meanings
`cat out/kanjidic2.json | jq '.kanjidic2.character[] | .reading_meaning.rmgroup.meaning | if (.|type)=="array" then map(select((.|type)=="string")) else [.] end | length' | sort -V | uniq -c`
