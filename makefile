OUT_DIR := out
SITE_DIR := $(OUT_DIR)/site
API_DIR := $(OUT_DIR)/v1
KANJI_DIR := $(API_DIR)/kanji
READING_DIR := $(API_DIR)/reading

.PHONY: directories all clean

all: $(OUT_DIR)/kanji.stamp $(SITE_DIR)/index.html $(SITE_DIR)/404.html $(SITE_DIR)/v1

directories: $(OUT_DIR) $(SITE_DIR) $(API_DIR) $(KANJI_DIR) $(READING_DIR)

$(OUT_DIR):
	mkdir -p $@

$(SITE_DIR):
	mkdir -p $@

$(API_DIR):
	mkdir -p $@

$(KANJI_DIR):
	mkdir -p $@

$(READING_DIR):
	mkdir -p $@

$(SITE_DIR)/v1: $(SITE_DIR)
	ln -s ../v1 $@

$(OUT_DIR)/kanjidic2.json: kanjidic2.xml | directories
	cat $^ | xq . -c > $@

$(OUT_DIR)/JMdict_e.json: JMdict_e | directories
	cat $^ | xq . -c > $@

$(OUT_DIR)/kanji.stamp: $(OUT_DIR)/kanjidic2.json api_data.py | directories
	python api_data.py
	touch $@

$(SITE_DIR)/index.html: index.html | $(SITE_DIR)/reset.css $(SITE_DIR)/styling.css directories
	cp $^ $@

$(SITE_DIR)/404.html: 404.html | $(SITE_DIR)/reset.css $(SITE_DIR)/styling.css directories
	cp $^ $@

$(SITE_DIR)/reset.css: reset.css | directories
	cp $^ $@

$(SITE_DIR)/styling.css: styling.css | directories
	cp $^ $@

clean:
	rm -rf $(OUT_DIR)
