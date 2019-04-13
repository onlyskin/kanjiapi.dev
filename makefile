OUT_DIR := out
SITE_DIR := out/site
KANJI_DIR := out/site/kanji
READING_DIR := out/site/reading

.PHONY: directories all clean

all: $(OUT_DIR)/kanji.stamp $(SITE_DIR)/index.html

directories: $(OUT_DIR) $(SITE_DIR) $(KANJI_DIR) $(READING_DIR)

$(OUT_DIR):
	mkdir -p $@

$(SITE_DIR):
	mkdir -p $@

$(KANJI_DIR):
	mkdir -p $@

$(READING_DIR):
	mkdir -p $@

$(OUT_DIR)/kanjidic2.json: kanjidic2.xml | directories
	cat $^ | xq . -c > $@

$(OUT_DIR)/JMdict_e.json: JMdict_e | directories
	cat $^ | xq . -c > $@

$(OUT_DIR)/kanji.stamp: $(OUT_DIR)/kanjidic2.json api_data.py | directories
	python api_data.py
	touch $@

$(SITE_DIR)/index.html: index.html | $(SITE_DIR)/reset.css directories
	cp $^ $@

$(SITE_DIR)/reset.css: reset.css | directories
	cp $^ $@

clean:
	rm -rf $(OUT_DIR)
