#!/usr/bin/env python3
"""Gestionnaire de pilotes pour MythicOS."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List


@dataclass
class Driver:
    """Représente un pilote géré par l'application."""

    nom: str
    version: str
    description: str
    actif: bool = True


class DriverManager:
    """Fournit des opérations CRUD sur une base locale de pilotes."""

    # Chemin par défaut dans le dossier utilisateur pour garder un état persistant.
    DEFAULT_DB_PATH = Path.home() / ".local" / "share" / "mythicos-drivers" / "drivers.json"

    def __init__(self, db_path: Path | None = None) -> None:
        # Initialise le chemin de base de données et crée l'arborescence si besoin.
        self.db_path = db_path or self.DEFAULT_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_path.exists():
            self._save({})

    def _load(self) -> Dict[str, Driver]:
        # Charge le fichier JSON et reconstruit les objets Driver.
        with self.db_path.open("r", encoding="utf-8") as f:
            payload = json.load(f)
        return {name: Driver(**data) for name, data in payload.items()}

    def _save(self, drivers: Dict[str, Driver | dict]) -> None:
        # Sauvegarde les pilotes au format JSON lisible pour simplifier le débogage.
        normalized = {
            name: asdict(driver) if isinstance(driver, Driver) else driver
            for name, driver in drivers.items()
        }
        with self.db_path.open("w", encoding="utf-8") as f:
            json.dump(normalized, f, ensure_ascii=False, indent=2)

    def lister(self) -> List[Driver]:
        # Retourne la liste triée des pilotes.
        return sorted(self._load().values(), key=lambda d: d.nom.lower())

    def installer(self, nom: str, version: str, description: str) -> Driver:
        # Installe un nouveau pilote et échoue s'il existe déjà.
        drivers = self._load()
        if nom in drivers:
            raise ValueError(f"Le pilote '{nom}' est déjà installé.")
        driver = Driver(nom=nom, version=version, description=description, actif=True)
        drivers[nom] = driver
        self._save(drivers)
        return driver

    def supprimer(self, nom: str) -> None:
        # Supprime un pilote existant.
        drivers = self._load()
        if nom not in drivers:
            raise ValueError(f"Le pilote '{nom}' est introuvable.")
        del drivers[nom]
        self._save(drivers)

    def activer(self, nom: str) -> Driver:
        # Active un pilote installé.
        drivers = self._load()
        if nom not in drivers:
            raise ValueError(f"Le pilote '{nom}' est introuvable.")
        drivers[nom].actif = True
        self._save(drivers)
        return drivers[nom]

    def desactiver(self, nom: str) -> Driver:
        # Désactive un pilote installé.
        drivers = self._load()
        if nom not in drivers:
            raise ValueError(f"Le pilote '{nom}' est introuvable.")
        drivers[nom].actif = False
        self._save(drivers)
        return drivers[nom]


# Construit l'interface en ligne de commande pour le paquet Debian futur.
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mythicos-drivers",
        description="Gestionnaire de pilotes MythicOS",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        help="Chemin personnalisé de la base de pilotes (utile pour les tests).",
    )

    subparsers = parser.add_subparsers(dest="commande", required=True)

    subparsers.add_parser("list", help="Lister les pilotes installés")

    install_parser = subparsers.add_parser("install", help="Installer un pilote")
    install_parser.add_argument("nom", help="Nom du pilote")
    install_parser.add_argument("version", help="Version du pilote")
    install_parser.add_argument("description", help="Description fonctionnelle")

    remove_parser = subparsers.add_parser("remove", help="Supprimer un pilote")
    remove_parser.add_argument("nom", help="Nom du pilote")

    enable_parser = subparsers.add_parser("enable", help="Activer un pilote")
    enable_parser.add_argument("nom", help="Nom du pilote")

    disable_parser = subparsers.add_parser("disable", help="Désactiver un pilote")
    disable_parser.add_argument("nom", help="Nom du pilote")

    return parser


# Point d'entrée principal de l'outil CLI.
def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    manager = DriverManager(db_path=args.db_path)

    try:
        if args.commande == "list":
            drivers = manager.lister()
            if not drivers:
                print("Aucun pilote installé.")
                return 0
            for driver in drivers:
                statut = "actif" if driver.actif else "inactif"
                print(f"- {driver.nom} {driver.version} [{statut}] :: {driver.description}")
            return 0

        if args.commande == "install":
            driver = manager.installer(args.nom, args.version, args.description)
            print(f"Pilote installé : {driver.nom} ({driver.version})")
            return 0

        if args.commande == "remove":
            manager.supprimer(args.nom)
            print(f"Pilote supprimé : {args.nom}")
            return 0

        if args.commande == "enable":
            driver = manager.activer(args.nom)
            print(f"Pilote activé : {driver.nom}")
            return 0

        if args.commande == "disable":
            driver = manager.desactiver(args.nom)
            print(f"Pilote désactivé : {driver.nom}")
            return 0

        parser.error("Commande non supportée.")

    except ValueError as err:
        print(f"Erreur : {err}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
