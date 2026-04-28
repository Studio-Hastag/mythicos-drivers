APP_NAME := mythicos-drivers
VERSION := 1.0
DIST_DIR := dist
TARBALL := $(APP_NAME)_$(VERSION).orig.tar.gz
DIST_TARBALL := $(DIST_DIR)/$(TARBALL)
ARCHIVE_PREFIX := $(APP_NAME)-$(VERSION)

.PHONY: help check run clean dist dist-dir orig

help:
	@echo "Cibles disponibles :"
	@echo "  make check  - Vérifie la syntaxe Python"
	@echo "  make run    - Lance l'aide de la CLI"
	@echo "  make orig   - Génère $(TARBALL) à la racine"
	@echo "  make dist   - Génère $(DIST_TARBALL)"
	@echo "  make clean  - Supprime les artefacts"

check:
	python3 -m py_compile scr/mythicos-drivers.py

run:
	python3 scr/mythicos-drivers.py --help

# Archive amont Debian à la racine du dépôt.
# git archive évite les problèmes "file changed as we read it".
orig:
	git archive --format=tar.gz --prefix=$(ARCHIVE_PREFIX)/ -o $(TARBALL) HEAD
	@echo "Archive générée : $(TARBALL)"

dist-dir:
	mkdir -p $(DIST_DIR)

# Copie l'archive amont dans dist/ pour les pipelines CI.
dist: orig dist-dir
	cp -f $(TARBALL) $(DIST_TARBALL)
	@echo "Archive copiée : $(DIST_TARBALL)"

clean:
	rm -rf $(DIST_DIR) __pycache__ scr/__pycache__ $(TARBALL)
