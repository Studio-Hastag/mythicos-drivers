# mythicos-drivers

`mythicos-drivers` est un gestionnaire de pilotes minimal pour **MythicOS**, écrit en Python, prêt à être empaqueté en `.deb`.

## Arborescence

- `scr/mythicos-drivers.py` : source principale (CLI).
- `assets/icons/mythicos-drivers.svg` : icône de l'application.
- `Makefile` : commandes de vérification et génération de l'archive source.

## Fonctionnalités

- Installation d'un pilote : `install`
- Suppression d'un pilote : `remove`
- Activation d'un pilote : `enable`
- Désactivation d'un pilote : `disable`
- Liste des pilotes installés : `list`

Les données sont stockées en local dans `~/.local/share/mythicos-drivers/drivers.json`.

## Dépendances de build

Pour construire/valider le projet :

- `python3` (>= 3.10 recommandé)
- `make`
- `tar`
- `gzip`

## Dépendances d'exécution

Pour lancer l'application :

- `python3`

Aucune dépendance Python externe n'est requise.

## Utilisation rapide

```bash
python3 scr/mythicos-drivers.py --help
python3 scr/mythicos-drivers.py install nvidia 550.67 "Pilote GPU NVIDIA"
python3 scr/mythicos-drivers.py list
python3 scr/mythicos-drivers.py disable nvidia
python3 scr/mythicos-drivers.py remove nvidia
```

## Commandes pour générer `mythicos-drivers_1.0.orig.tar.gz`

Depuis la racine du dépôt :

```bash
# 1) Vérifier la syntaxe
make check

# 2) Générer l'archive source Debian amont
make dist

# 3) Vérifier l'archive
ls -lh dist/mythicos-drivers_1.0.orig.tar.gz
```

Archive attendue : `dist/mythicos-drivers_1.0.orig.tar.gz`.
