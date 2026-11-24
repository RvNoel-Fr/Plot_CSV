#!/usr/bin/env bash
set -e
pip install -r requirements-dev.txt
pyinstaller --onefile --windowed --name tracer_courbes tracer_courbes.py
echo "Exécutable généré dans dist/"
