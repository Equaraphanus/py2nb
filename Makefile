SRC_DIR=src
IPYNB_DIR=ipynb
OUT_DIR=out
SCRIPTS_DIR=scripts
CUSTOM_TEMPLATE=j2/customlatex
TEMPLATE=$(CUSTOM_TEMPLATE)
PY2NB_SCRIPT=$(SCRIPTS_DIR)/py2nb.py

rwildcard=$(foreach d,$(wildcard $(1:=/*)),$(call rwildcard,$d,$2) $(filter $(subst *,%,$2),$d))

ALL_SOURCES=$(call rwildcard,$(SRC_DIR),*.py)
ALL_IPYNBS=$(patsubst $(SRC_DIR)/%.py,$(IPYNB_DIR)/%.ipynb,$(ALL_SOURCES))
ALL_PDFS=$(patsubst $(IPYNB_DIR)/%.ipynb,$(OUT_DIR)/%.pdf,$(ALL_IPYNBS))

reports: $(ALL_PDFS) Makefile

notebooks: $(ALL_IPYNBS) Makefile

$(IPYNB_DIR)/%.ipynb: $(SRC_DIR)/%.py $(SCRIPTS_DIR) Makefile
	python $(PY2NB_SCRIPT) -e $< -o $@

$(OUT_DIR)/%.pdf: $(IPYNB_DIR)/%.ipynb $(CUSTOM_TEMPLATE) Makefile
	jupyter nbconvert --to pdf --template $(TEMPLATE) --output-dir $(OUT_DIR) $<

.PHONY: notebooks reports
