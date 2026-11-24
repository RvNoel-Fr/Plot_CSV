# Plot_CSV
Tracé basique de fichiers CSV avec paramétrage des axes

## Utilisation

```bash
pip install matplotlib

# Une courbe, sauvegarde en PNG
python3 tracer_courbes.py exemple_mesures.csv -x temps -y tension \
    --xlabel "Temps (s)" --ylabel "Tension (V)" --title "Charge RC" -o courbe.png

# Plusieurs courbes Y
python3 tracer_courbes.py exemple_mesures.csv -x temps -y tension -y courant --grid --legend -o courbe.png

# Plusieurs fichiers = plusieurs courbes
python3 tracer_courbes.py fichierA.csv fichierB.csv -x 0 -y 1 -o comparaison.png
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
