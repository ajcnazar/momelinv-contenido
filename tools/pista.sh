#!/bin/bash
# Genera una pista de tools/musica.py normalizada a -16 LUFS, lista para mix.py.
# Uso: tools/pista.sh <estilo> <semilla> <segundos> <salida.wav>
set -e
D=$(dirname "$0")
python3 "$D/musica.py" "$1" "$4.raw.wav" "$3" "$2"
ffmpeg -loglevel error -y -i "$4.raw.wav" -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 "$4"
rm -f "$4.raw.wav"
