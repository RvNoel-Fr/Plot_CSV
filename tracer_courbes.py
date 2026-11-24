#!/usr/bin/env python3
"""Trace des courbes à partir de fichiers CSV, avec paramétrage des axes.

Exemples :
  python3 tracer_courbes.py data.csv -x temps -y tension -y courant \
      --xlabel "Temps (s)" --ylabel "Tension (V)" --title "Mesure" -o courbe.png

  python3 tracer_courbes.py a.csv b.csv -x 0 -y 1 --sep ";" --xscale log -o out.pdf
"""

import argparse
import csv
import os
import re
import sys

import matplotlib

if not os.environ.get("DISPLAY") and sys.platform != "win32":
    matplotlib.use("Agg")

import matplotlib.pyplot as plt


def detecter_separateur(sample):
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        return dialect.delimiter
    except csv.Error:
        return ","


def lire_csv(chemin, sep, decimal, sans_entete):
    with open(chemin, newline="", encoding="utf-8-sig") as f:
        sample = f.read(4096)
        f.seek(0)
        if sep is None:
            sep = detecter_separateur(sample)
        if decimal is None:
            decimal = "," if sep != "," and re.search(r"\d,\d", sample) else "."
        if decimal == ",":
            sample = sample.replace(",", ".")
            f.seek(0)
            lignes = (ligne.replace(",", ".") for ligne in f)
            reader = csv.reader(lignes, delimiter=sep)
        else:
            reader = csv.reader(f, delimiter=sep)
        lignes = [ligne for ligne in reader if ligne and any(c.strip() for c in ligne)]

    if not lignes:
        raise ValueError(f"Fichier vide : {chemin}")

    if sans_entete:
        entete = [f"col_{i}" for i in range(len(lignes[0]))]
        donnees = lignes
    else:
        entete = [h.strip() for h in lignes[0]]
        donnees = lignes[1:]

    colonnes = {nom: [] for nom in entete}
    for ligne in donnees:
        for i, nom in enumerate(entete):
            valeur = ligne[i].strip() if i < len(ligne) else ""
            try:
                colonnes[nom].append(float(valeur) if valeur else float("nan"))
            except ValueError:
                colonnes[nom].append(float("nan"))
    return entete, colonnes


def resoudre_colonne(entete, spec):
    if spec is None:
        raise ValueError("Précisez la colonne X avec -x/--x (nom ou numéro, ex. -x 0).")
    if spec.lstrip("-").isdigit():
        i = int(spec)
        if not 0 <= i < len(entete):
            raise ValueError(f"Index X hors limites : {spec} (0..{len(entete) - 1})")
        return entete[i]
    if spec not in entete:
        raise ValueError(f"Colonne inconnue : '{spec}'. Disponibles : {entete}")
    return spec


def analyser_args():
    p = argparse.ArgumentParser(
        description="Trace des courbes depuis des fichiers CSV avec paramétrage des axes.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("fichiers", nargs="+", help="Fichier(s) CSV à tracer")
    p.add_argument("-x", "--x", required=True,
                   help="Colonne des X (nom d'en-tête ou numéro 0-based)")
    p.add_argument("-y", "--y", required=True, nargs="+", action="append",
                   help="Colonne(s) des Y à tracer (nom ou numéro), répétable : -y tension -y courant")
    p.add_argument("--sep", default=None,
                   help="Séparateur de colonnes (auto-détecté par défaut : , ; \\t |)")
    p.add_argument("--decimal", choices=[".", ","], default=None,
                   help="Symbole décimal dans le fichier (auto-détecté par défaut)")
    p.add_argument("--sans-entete", action="store_true",
                   help="Le fichier n'a pas de ligne d'en-tête (colonnes nommées col_0, col_1, ...)")
    p.add_argument("--xlabel", default=None, help="Label de l'axe X")
    p.add_argument("--ylabel", default=None, help="Label de l'axe Y")
    p.add_argument("--title", default=None, help="Titre du graphique")
    p.add_argument("--xscale", choices=["linear", "log"], default="linear", help="Échelle de l'axe X")
    p.add_argument("--yscale", choices=["linear", "log"], default="linear", help="Échelle de l'axe Y")
    p.add_argument("--xmin", type=float, default=None, help="Borne min de l'axe X")
    p.add_argument("--xmax", type=float, default=None, help="Borne max de l'axe X")
    p.add_argument("--ymin", type=float, default=None, help="Borne min de l'axe Y")
    p.add_argument("--ymax", type=float, default=None, help="Borne max de l'axe Y")
    p.add_argument("--label", nargs="+", default=None,
                   help="Légende des courbes (dans l'ordre des -y, ou des fichiers si une seule -y)")
    p.add_argument("--marker", default="", help="Marqueur (ex. o, s, ^, ., none pour aucun)")
    p.add_argument("--linestyle", default="-", help="Style de ligne (-, --, -., :, none)")
    p.add_argument("--color", default=None, help="Couleur unique pour toutes les courbes (ex. red, #1f77b4)")
    p.add_argument("--grid", action="store_true", help="Afficher la grille")
    p.add_argument("--legend", action="store_true", help="Afficher la légende")
    p.add_argument("-o", "--output", default=None,
                   help="Fichier de sortie (png, pdf, svg...). Sans -o : affichage interactif")
    return p.parse_args()


def main():
    args = analyser_args()
    args.y = [col for groupe in args.y for col in groupe]

    fig, ax = plt.subplots(figsize=(10, 6))

    tous_labels = args.label or []
    for chemin in args.fichiers:
        entete, colonnes = lire_csv(chemin, args.sep, args.decimal, args.sans_entete)
        xcol = resoudre_colonne(entete, args.x)
        x = colonnes[xcol]

        for j, yspec in enumerate(args.y):
            ycol = resoudre_colonne(entete, yspec)
            y = colonnes[ycol]
            if len(args.fichiers) > 1 and len(args.y) == 1:
                label = os.path.basename(chemin)
            elif tous_labels:
                label = tous_labels[j] if j < len(tous_labels) else ycol
            else:
                label = ycol if len(args.y) > 1 else os.path.basename(chemin)
            ax.plot(x, y,
                    marker=None if args.marker in ("", "none") else args.marker,
                    linestyle="none" if args.linestyle == "none" else args.linestyle,
                    color=args.color,
                    label=label)

    if args.xlabel:
        ax.set_xlabel(args.xlabel)
    if args.ylabel:
        ax.set_ylabel(args.ylabel)
    if args.title:
        ax.set_title(args.title)
    ax.set_xscale(args.xscale)
    ax.set_yscale(args.yscale)
    if args.xmin is not None or args.xmax is not None:
        ax.set_xlim(args.xmin, args.xmax)
    if args.ymin is not None or args.ymax is not None:
        ax.set_ylim(args.ymin, args.ymax)
    if args.grid:
        ax.grid(True, which="both", linestyle=":", alpha=0.7)
    if args.legend or len(args.fichiers) * len(args.y) > 1:
        ax.legend()

    fig.tight_layout()
    if args.output:
        fig.savefig(args.output, dpi=150)
        print(f"Graphique enregistré : {args.output}")
    else:
        plt.show()


if __name__ == "__main__":
    try:
        main()
    except (ValueError, FileNotFoundError) as e:
        sys.exit(f"Erreur : {e}")
