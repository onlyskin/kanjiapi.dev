OUT_DIR := out
KANJI_DIR := out/kanji
READING_DIR := out/reading

.PHONY: directories all clean

all: $(OUT_DIR)/kanji.stamp

directories: $(OUT_DIR) $(KANJI_DIR) $(READING_DIR)

$(OUT_DIR):
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

clean:
	rm -rf $(OUT_DIR)
