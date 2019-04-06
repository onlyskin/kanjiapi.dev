OUT_DIR := out
KANJI_DIR := out/kanji
READING_DIR := out/reading

.PHONY: directories all clean

all: $(OUT_DIR)/kanjidic2.json $(KANJI_DIR)/%.json $(READING_DIR)/%.json \
	$(OUT_DIR)/JMdict_e.json

directories: $(OUT_DIR) $(KANJI_DIR) $(READING_DIR)

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

$(KANJI_DIR):
	mkdir -p $(KANJI_DIR)

$(READING_DIR):
	mkdir -p $(READING_DIR)

$(OUT_DIR)/kanjidic2.json: kanjidic2.xml | directories
	cat kanjidic2.xml | xq . -c > $(OUT_DIR)/kanjidic2.json

$(OUT_DIR)/JMdict_e.json: JMdict_e | directories
	cat JMdict_e | xq . -c > $(OUT_DIR)/JMdict_e.json

$(KANJI_DIR)/%.json $(READING_DIR)/%.json: $(OUT_DIR)/kanjidic2.json | directories api_data.py
	python api_data.py

clean:
	rm -rf $(OUT_DIR)
