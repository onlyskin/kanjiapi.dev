OUT_DIR := out
JSON_DIR := out/json

.PHONY: directories all clean

all: $(OUT_DIR)/kanjidic2.json $(JSON_DIR)/%.json

directories: $(OUT_DIR) $(JSON_DIR)

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

$(JSON_DIR):
	mkdir -p $(JSON_DIR)

$(OUT_DIR)/kanjidic2.json: kanjidic2.xml | directories
	cat kanjidic2.xml | xq . > $(OUT_DIR)/kanjidic2.json

$(JSON_DIR)/%.json: $(OUT_DIR)/kanjidic2.json | directories api_data.py
	python api_data.py

clean:
	rm -rf $(OUT_DIR)
