OUT_DIR := out
SITE_SRC_DIR := site
SITE_DIR := $(OUT_DIR)/site
API_DIR := $(OUT_DIR)/v1
KANJI_DIR := $(API_DIR)/kanji
CJK_KANJI_DIR := $(API_DIR)/kanji_cjk
WORDS_DIR := $(API_DIR)/words
CJK_WORDS_DIR := $(API_DIR)/words_cjk
READING_DIR := $(API_DIR)/reading
ESBUILD=node_modules/.bin/esbuild
TACHYONS := node_modules/tachyons/css/tachyons.min.css

# Run by hand, never from a build target. See TODO.md for the file choices.
KANJIDIC_URL := http://ftp.edrdg.org/pub/Nihongo/kanjidic2.xml.gz
JMDICT_URL := http://ftp.edrdg.org/pub/Nihongo/JMdict_e_NG.gz
JMNEDICT_URL := http://ftp.edrdg.org/pub/Nihongo/JMnedict.xml.gz
UNIHAN_URL := https://www.unicode.org/Public/UCD/latest/ucd/Unihan.zip
UNIHAN_FILES := Unihan_OtherMappings.txt Unihan_IRGSources.txt \
	Unihan_DictionaryLikeData.txt Unihan_Readings.txt Unihan_Variants.txt
DICTIONARIES := kanjidic2.xml JMdict_e_NG JMnedict.xml $(UNIHAN_FILES)
DATA_DIR := data
STAGING := .dictionary_staging
DICT_ARCHIVE := data_archive

.PHONY: directories all clean \
	download-dictionaries install-dictionaries update-dictionaries

all: $(OUT_DIR)/kanji.stamp $(SITE_DIR)/index.html $(SITE_DIR)/404.json $(SITE_DIR)/v1

directories: $(OUT_DIR) $(SITE_DIR) $(API_DIR) $(KANJI_DIR) $(CJK_KANJI_DIR) $(WORDS_DIR) $(CJK_WORDS_DIR) $(READING_DIR)

$(OUT_DIR):
	mkdir -p $@

$(SITE_DIR):
	mkdir -p $@

$(API_DIR):
	mkdir -p $@

$(KANJI_DIR):
	mkdir -p $@

$(CJK_KANJI_DIR):
	mkdir -p $@

$(WORDS_DIR):
	mkdir -p $@

$(CJK_WORDS_DIR):
	mkdir -p $@

$(READING_DIR):
	mkdir -p $@

$(SITE_DIR)/v1: $(SITE_DIR)
	ln -sF ../v1 $@

# Fetch and check, without touching the installed files.
download-dictionaries:
	rm -rf $(STAGING)
	mkdir -p $(STAGING)
	curl -fSL --retry 3 -o $(STAGING)/kanjidic2.xml.gz $(KANJIDIC_URL)
	curl -fSL --retry 3 -o $(STAGING)/JMdict_e_NG.gz $(JMDICT_URL)
	curl -fSL --retry 3 -o $(STAGING)/JMnedict.xml.gz $(JMNEDICT_URL)
	curl -fSL --retry 3 -o $(STAGING)/Unihan.zip $(UNIHAN_URL)
	gunzip $(STAGING)/kanjidic2.xml.gz $(STAGING)/JMdict_e_NG.gz $(STAGING)/JMnedict.xml.gz
	unzip -qo $(STAGING)/Unihan.zip -d $(STAGING) $(UNIHAN_FILES)
	python verify_dictionaries.py $(STAGING) $(DATA_DIR)

# Archive what is installed, then swap in what download-dictionaries verified.
install-dictionaries:
	mkdir -p $(DICT_ARCHIVE) $(DATA_DIR)
	for f in $(DICTIONARIES); do \
		if [ -f $(DATA_DIR)/$$f ]; then \
			d=`python dictionary_date.py $(DATA_DIR)/$$f`; \
			gzip -c $(DATA_DIR)/$$f > $(DICT_ARCHIVE)/$$f.$$d.gz; \
		fi; \
	done
	for f in $(DICTIONARIES); do mv $(STAGING)/$$f $(DATA_DIR)/$$f; done
	rm -rf $(STAGING)
	@echo
	@echo "previous dictionaries archived to $(DICT_ARCHIVE)/, stamped with"
	@echo "the release date each one declares"
	@echo "run make to rebuild out/ with the new data"

update-dictionaries: download-dictionaries install-dictionaries

$(OUT_DIR)/kanji.stamp: main.py \
		kanjiapi/api_data.py kanjiapi/entry.py kanjiapi/entry_data.py \
		kanjiapi/canonicalise.py kanjiapi/grades.py kanjiapi/heisig.py \
		kanjiapi/jlpt.py kanjiapi/unihan.py \
		$(DATA_DIR)/kanjidic2.xml $(DATA_DIR)/JMdict_e_NG \
		grades.tsv heisig.tsv jlpt.tsv \
		$(DATA_DIR)/Unihan_OtherMappings.txt \
		$(DATA_DIR)/Unihan_IRGSources.txt | directories
	python main.py
	touch $@

$(SITE_DIR)/index.html: $(SITE_SRC_DIR)/index.html | $(SITE_DIR)/tachyons.min.css $(SITE_DIR)/styling.css directories $(SITE_DIR)/index.js $(SITE_DIR) $(SITE_DIR)/favicon.png
	cp $^ $@

$(SITE_DIR)/favicon.png: | directories
	magick -size 128x128 -gravity center -background '#1f1f1f' -fill white \
		-font "/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc" \
		label:字 -resize 32x32 $@

$(SITE_DIR)/index.js: $(SITE_SRC_DIR)/index.js package.json $(SITE_SRC_DIR)/log_provider.js | directories
	$(ESBUILD) $< --bundle --minify --sourcemap --outfile=$@

$(SITE_DIR)/404.json: $(SITE_SRC_DIR)/404.json | directories
	cp $^ $@

$(SITE_DIR)/styling.css: $(SITE_SRC_DIR)/styling.css | directories
	cp $^ $@

$(SITE_DIR)/tachyons.min.css: $(TACHYONS) | directories
	cp $^ $@

clean:
	rm -rf $(OUT_DIR)
