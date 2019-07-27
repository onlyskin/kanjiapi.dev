# kanjiapi.dev: a modern JSON API for Kanji

Over 13,000 kanji served at [https://kanjiapi.dev](https://kanjiapi.dev)

## Examples

### Kanji `/v1/kanji/{character}`
```
$ curl https://kanjiapi.dev/v1/kanji/猫
{
  "kanji": "猫",
  "grade": 8,
  "stroke_count": 11,
  "meanings": [
    "cat"
  ],
  "kun_readings": [
    "ねこ"
  ],
  "on_readings": [
    "ビョウ"
  ],
  "name_readings": [],
  "jlpt": 2,
  "unicode": "732b"
}
```

```javascript
> fetch('https://kanjiapi.dev/v1/kanji/猫').then(r => r.json()).then(console.log);
{
  "kanji": "猫",
  "grade": 8,
  "stroke_count": 11,
  "meanings": [
    "cat"
  ],
  "kun_readings": [
    "ねこ"
  ],
  "on_readings": [
    "ビョウ"
  ],
  "name_readings": [],
  "jlpt": 2,
  "unicode": "732b"
}
```

#### List of all supported kanji

`$ curl https://kanjiapi.dev/v1/kanji/all`

#### List of joyo kanji

`$ curl https://kanjiapi.dev/v1/kanji/joyo` (also `/jouyou`)

#### List of jinmeiyo kanji

`$ curl https://kanjiapi.dev/v1/kanji/jinmeiyo` (also `/jinmeiyou`)

#### List of kanji of a certain grade

`$ curl https://kanjiapi.dev/v1/kanji/grade-1` (school grades 1-6, with grade 8 signalling remaining highschool grade)

### Reading `/v1/reading/{reading}`
```
$ curl https://kanjiapi.dev/v1/reading/クウ
{
  "reading": "クウ",
  "main_kanji": [
    "宮",
    "供",
    "空",
    "咼",
    "啌",
    "喎",
    "垙",
    "瘸",
    "盉",
    "舙"
  ],
  "name_kanji": []
}
```

```javascript
> fetch('https://kanjiapi.dev/v1/reading/クウ').then(r => r.json()).then(console.log);
{
  "reading": "クウ",
  "main_kanji": [
    "宮",
    "供",
    "空",
    "咼",
    "啌",
    "喎",
    "垙",
    "瘸",
    "盉",
    "舙"
  ],
  "name_kanji": []
}
```

### Words `/v1/words/{character}`
```
$ curl https://kanjiapi.dev/v1/words/猫
[
  {
    "variants": [
      {
        "written": "どら猫",
        "pronounced": "どらねこ",
        "priorities": []
      }
    ],
    "meanings": [
      {
        "glosses": [
          "stray cat"
        ]
      }
    ]
  },
  {
    "variants": [
      {
        "written": "アンゴラ猫",
        "pronounced": "アンゴラねこ",
        "priorities": []
      }
    ],
    "meanings": [
      {
        "glosses": [
          "Angora cat"
        ]
      }
    ]
  },
  ...
]
```

```javascript
> fetch('https://kanjiapi.dev/v1/reading/クウ').then(r => r.json()).then(console.log);
[
  {
    "variants": [
      {
        "written": "どら猫",
        "pronounced": "どらねこ",
        "priorities": []
      }
    ],
    "meanings": [
      {
        "glosses": [
          "stray cat"
        ]
      }
    ]
  },
  {
    "variants": [
      {
        "written": "アンゴラ猫",
        "pronounced": "アンゴラねこ",
        "priorities": []
      }
    ],
    "meanings": [
      {
        "glosses": [
          "Angora cat"
        ]
      }
    ]
  },
  ...
]
```

## Development:

### Requirements:

Assumes `python 3`, `make` and `node` are available.

### Setup:

Install python libraries using requirements.txt

Install node dependencies using `yarn` or `npm install`.

Save and extract the kanji dictionary file `kanjidic2.xml` from [EDRDG](http://www.edrdg.org/wiki/index.php/KANJIDIC_Project) to the root of the project.

Save and extract the jmdict dictionary file `JMdict` from [EDRDG](http://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project) to the root of the project.

Ensure system has `System/Library/Fonts/ヒラギノ丸ゴ\ ProN\ W4.ttc` font
available (for favicon generation).

### Building:

Run `make` to build the site and API endpoints as static assets.

Run `python -m pytest tests` to run the tests.

Note: in order to fetch data from the local build of the API from the local
build of the site, you can set the root of your fileserver to out/site (e.g.
with `serveit`: `serveit -s out/site make`). There is a symlink to `out/v1`
inside `out/site` to enable this.

### Deployment (Requires google cloud account credentials):

#### Versioning

The API version for deployment is hardcoded in `api_data.py` and the `makefile`.

After building, to sync the built assets to the website bucket run:

`gsutil -m rsync -c -d out/site gs://kanjiapi-static` (syncs the built site dir (`out/site`) up with the root of the bucket, but non-recursively)

`gsutil -m -h "Content-Type:application/json" rsync -r -c -d out/v1 gs://kanjiapi-static/v1` (syncs the built api dir (`out/{version}`) up with the dir `/{version}` in the bucket recursively based on file hashes)

NB: it's a good idea to run both these commands with `rsync -n` for a dry-run first

#### Renewing SSL certificate:

The SSL certificate is only trusted for a certain amount of time, the below script mostly automates
the process of getting a new certificate (requires certbot - `brew install certbot`)

`./update_cert.sh`

#### Setting CORS policy:

The CORS policy is stored in `cors.json`, it can be updated by editing this file and running `gsutil cors set cors.json gs://kanjiapi-static`
