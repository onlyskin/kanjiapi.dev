# KanjiApi

Source for [https://kanjiapi.dev/](https://kanjiapi.dev/)

### Kanji `/kanji/{character}`
```json
$ curl https://kanjiapi.dev/kanji/山
{
  "meanings": [
    "mountain"
  ],
  "grade": "1",
  "kanji": "山",
  "stroke_count": "3",
  "name_readings": [
    "さ",
    "やの",
    "やん"
  ],
  "kun_readings": [
    "やま"
  ],
  "on_readings": [
    "サン",
    "セン"
  ]
}
```

```javascript
> fetch('https://kanjiapi.dev/kanji/山').then(r => r.json()).then(console.log);
{
  "meanings": [
    "mountain"
  ],
  "grade": "1",
  "kanji": "山",
  "stroke_count": "3",
  "name_readings": [
    "さ",
    "やの",
    "やん"
  ],
  "kun_readings": [
    "やま"
  ],
  "on_readings": [
    "サン",
    "セン"
  ]
}
```

### Reading `/reading/{reading}`
```json
$ curl https://kanjiapi.dev/reading/クウ
{
  "reading": "クウ",
  "kanji": [
    "宮",
    "供",
    "空"
  ],
  "name": []
}
```

```javascript
> fetch('https://kanjiapi.dev/reading/クウ').then(r => r.json()).then(console.log);
{
  "reading": "クウ",
  "kanji": [
    "宮",
    "供",
    "空"
  ],
  "name": []
}
```

## Development:

### Requirements:

Assumes `python 2.7`, `brew` and `make` are available.

### Setup:

`brew install xq`

Save the kanji dictionary file `kanjidic2.xml` from [EDRDG](http://www.edrdg.org/wiki/index.php/KANJIDIC_Project) to the root of the project.

Save the jmdict dictionary file `JMdict_e` from [EDRDG](http://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project) to the root of the project.

### Building:

Run `make` to build the site and API endpoints as static assets.

### Deployment (Requires google cloud account credentials):

#### Versioning

The API version for deployment is hardcoded in `api_data.py` and the `makefile`.

After building, to sync the built assets to the website bucket run:

`gsutil -m rsync -d out/site gs://kanjiapi-static` (syncs the built site dir (`out/site`) up with the root of the bucket, but non-recursively)

`gsutil -m -h "Content-Type:application/json" rsync -r -d out/v1 gs://kanjiapi-static/v1` (syncs the built api dir (`out/{version}`) up with the dir `/{version}` in the bucket recursively)

NB: it's a good idea to run both these commands with `rsync -n` for a dry-run first

#### Renewing SSL certificate:

The SSL certificate is only trusted for a certain amount of time, the below script mostly automates
the process of getting a new certificate

`./update_cert.sh`

#### Setting CORS policy:

The CORS policy is stored in `cors.json`, it can be updated by editing this file and running `gsutil cors set cors.json gs://kanjiapi-static`

### Useful JQ recipes:

Print out all kanji as `literal: meaning`
`jq '.kanjidic2.character | map([.literal, .reading_meaning.rmgroup.meaning])[] | if (.[1]|type)=="array" then "\(.[0]): \(.[1][0])" else "\(.[0]): \(.[1])" end'`

Count kanji with n meanings
`cat out/kanjidic2.json | jq '.kanjidic2.character[] | .reading_meaning.rmgroup.meaning | if (.|type)=="array" then map(select((.|type)=="string")) else [.] end | length' | sort -V | uniq -c`
