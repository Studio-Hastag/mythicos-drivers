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
- `git` (utilisé par `make orig`)

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

# 2) Générer l'archive source Debian amont à la racine
make orig

# 3) Optionnel : copier aussi dans dist/
make dist
```

Archive racine : `mythicos-drivers_1.0.orig.tar.gz`.
Archive CI : `dist/mythicos-drivers_1.0.orig.tar.gz`.

## Important : commandes `tar` correctes

L'erreur `L'ancienne option « g » a besoin d'un argument` apparaît si la commande `tar` est incomplète.

Exemples corrects :

```bash
# Créer une archive .tar.gz (méthode recommandée dans ce projet)
	git archive --format=tar.gz --prefix=mythicos-drivers-1.0/ -o mythicos-drivers_1.0.orig.tar.gz HEAD

# Lister le contenu d'une archive .tar.gz
	tar -tzf mythicos-drivers_1.0.orig.tar.gz

# Extraire une archive .tar.gz
	tar -xzf mythicos-drivers_1.0.orig.tar.gz
```
