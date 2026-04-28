APP_NAME := mythicos-drivers
VERSION := 1.0
DIST_DIR := dist
TARBALL := $(DIST_DIR)/$(APP_NAME)_$(VERSION).orig.tar.gz

.PHONY: help check run clean dist dist-dir

help:
	@echo "Cibles disponibles :"
	@echo "  make check  - Vérifie la syntaxe Python"
	@echo "  make run    - Lance l'aide de la CLI"
	@echo "  make dist   - Génère $(TARBALL)"
	@echo "  make clean  - Supprime les artefacts"

check:
	python3 -m py_compile scr/mythicos-drivers.py

run:
	python3 scr/mythicos-drivers.py --help

dist-dir:
	mkdir -p $(DIST_DIR)

dist: dist-dir
	tar --exclude-vcs -czf $(TARBALL) .
	@echo "Archive générée : $(TARBALL)"

clean:
	rm -rf $(DIST_DIR) __pycache__ scr/__pycache__
