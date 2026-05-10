# LLMBook publishing pipeline
# Usage:
#   make build      - build EPUB and validate (default)
#   make quick      - fast build with smaller images (iteration mode)
#   make validate   - re-run validators on existing EPUB
#   make clean      - remove output + reports
#   make rebuild    - clean + build + validate
#   make spine      - regenerate spine_manifest.json from source tree
#   make cover      - regenerate KDP cover from source PNG
#
# Run from the project root. PYTHON env var overrides default interpreter.

PYTHON ?= /c/Python314/python
ROOT   := $(abspath $(lastword $(MAKEFILE_LIST))/../../..)
KDP    := $(ROOT)/KDP

.PHONY: help build quick validate clean rebuild spine cover all

help:
	@echo "LLMBook publishing pipeline"
	@echo ""
	@echo "Targets:"
	@echo "  build      Build EPUB + structural validation (default)"
	@echo "  quick      Fast build with smaller images (NOT for submission)"
	@echo "  validate   Re-run validators on existing EPUB without rebuild"
	@echo "  clean      Remove output and reports"
	@echo "  rebuild    Clean + build + validate"
	@echo "  spine      Regenerate spine_manifest.json from source tree"
	@echo "  cover      Regenerate KDP cover image from source"
	@echo ""
	@echo "Override the Python interpreter via:"
	@echo "  make PYTHON=/path/to/python build"

build:
	$(PYTHON) "$(KDP)/build/publish.py"

quick:
	$(PYTHON) "$(KDP)/build/publish.py" --quick

validate:
	$(PYTHON) "$(KDP)/build/publish.py" --validate-only

clean:
	$(PYTHON) "$(KDP)/build/publish.py" --clean --validate-only || true
	rm -f "$(KDP)/output"/*.epub
	rm -f "$(KDP)/validation"/*_report.txt
	rm -rf "$(KDP)/build/logs"

rebuild:
	$(PYTHON) "$(KDP)/build/publish.py" --clean --regen-spine

spine:
	$(PYTHON) "$(KDP)/build/generate_spine.py"

cover:
	$(PYTHON) "$(KDP)/cover/process_cover.py"

all: rebuild
