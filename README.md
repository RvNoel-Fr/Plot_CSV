# Plot_CSV
Tracé basique de fichiers CSV avec paramétrage des axes

## Installation (environnement virtuel recommandé)

```bash
git clone https://github.com/RvNoel-Fr/Plot_CSV.git
cd Plot_CSV
python3 -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Utilisation

```bash
# Une courbe, sauvegarde en PNG
python3 tracer_courbes.py exemple_mesures.csv -x temps -y tension \
    --xlabel "Temps (s)" --ylabel "Tension (V)" --title "Charge RC" -o courbe.png

# Plusieurs courbes Y
python3 tracer_courbes.py exemple_mesures.csv -x temps -y tension -y courant --grid --legend -o courbe.png

# Plusieurs fichiers = plusieurs courbes
python3 tracer_courbes.py fichierA.csv fichierB.csv -x 0 -y 1 -o comparaison.png
```

## Créer un exécutable partageable (PyInstaller)

```bash
./build_exe.sh
# ou manuellement :
pip install -r requirements-dev.txt
pyinstaller --onefile --windowed --name tracer_courbes tracer_courbes.py
```

L'exécutable est généré dans `dist/tracer_courbes` (`.exe` sous Windows) : un seul
fichier à distribuer, utilisable sans installer Python. Taille typique : 50–150 Mo
(Python + matplotlib embarqués). Testez-le sur une machine sans Python :

```bash
./dist/tracer_courbes exemple_mesures.csv -x temps -y tension -o courbe.png
```

## Options principales

| Option | Rôle |
|---|---|
| `-x` / `-y` | colonnes par nom d'en-tête ou numéro (0-based) ; `-y` répétable |
| `--xlabel` `--ylabel` `--title` | libellés des axes et titre |
| `--xscale` `--yscale` | `linear` ou `log` |
| `--xmin/--xmax/--ymin/--ymax` | bornes des axes |
| `--sep` | séparateur (`, ; \t \|`, auto-détecté par défaut) |
| `--decimal` | symbole décimal `.` ou `,` (auto-détecté par défaut) |
| `--sans-entete` | fichier sans ligne d'en-tête |
| `--marker` `--linestyle` `--color` `--label` `--grid` `--legend` | style et affichage |
| `-o` | fichier de sortie (png, pdf, svg…) ; sans `-o` : affichage interactif |

Voir `python3 tracer_courbes.py --help` pour la liste complète.
