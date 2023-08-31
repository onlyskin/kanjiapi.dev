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

.PHONY: directories all clean

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

$(OUT_DIR)/kanji.stamp: kanjidic2.xml main.py kanjiapi/api_data.py kanjiapi/entry.py kanjiapi/entry_data.py kanjiapi/canonicalise.py kanjiapi/grades.py kanjiapi/heisig.py kanjiapi/unihan.py | directories
	python main.py
	touch $@

$(SITE_DIR)/index.html: $(SITE_SRC_DIR)/index.html | $(SITE_DIR)/tachyons.min.css $(SITE_DIR)/styling.css directories $(SITE_DIR)/index.js $(SITE_DIR) $(SITE_DIR)/favicon.png
	cp $^ $@

$(SITE_DIR)/favicon.png: | directories
	convert -size 128x128 -gravity center -background '#1f1f1f' -fill white \
		-font /System/Library/Fonts/ヒラギノ丸ゴ\ ProN\ W4.ttc \
		label:字 $@
	convert $@ -size 32x32 $@

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
