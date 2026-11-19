# Momelinv · contenido

Contenido de Instagram de @momelinv (invitaciones digitales: bodas, XV años, cumpleaños).
Los archivos de `reels/` y `carruseles/` se publican en Instagram desde su enlace público.

## Estructura
- `reels/AAAA-MM-DD-tema.mp4` — reels 1080×1920 con audio.
- `carruseles/AAAA-MM-DD-tema/NN.jpg` — carruseles 1080×1350.
- `audio/` — música propia libre de derechos (vals.mp3, pop.mp3), generada con vidIQ.
- `invitaciones/CATALOGO.md` — tabla de cada invitación (concepto, apertura, navegación, cuenta regresiva, confirmación, tipografía, reel). **Leerlo antes de crear una nueva: cada invitación debe ser distinta en todas las columnas.**
- `invitaciones/` — invitaciones demo propias (HTML/CSS/JS, solo datos de ejemplo), para grabar reels:
  - `boda-playa/` — boda frente al mar, portada de pase de abordar que se rasga.
  - `novena/` — novena navideña, caja de regalo que se abre, luces y destellos.
  - `cumple-espacial/` — cumpleaños infantil, cohete con cuenta 3-2-1 que despega.
  - `baby-shower/` — baby shower con revelación: globo que explota en confeti.
- `tools/` — scripts de grabación:
  - `record4.py <boda|novena|cumple>`: graba las invitaciones de `invitaciones/` (DPR=2 OUT_W=720 OUT_H=1280).
  - `navidad_music.py <salida.wav> [seg]`: música navideña original sintetizada.
  - `record.py` / `record2.py`: graban una invitación web en vertical con Playwright (Chrome headless),
    con textos en pantalla y registro de eventos (toques, sello, textos) para sincronizar efectos.
    Variables: `DPR=2 OUT_W=720 OUT_H=1280 TAG=<nombre>`; Chrome con `--force-device-scale-factor`.
  - `encode.py <tag>`: arma el MP4 (usar `OUT_W=1080 OUT_H=1920`).
  - `mix.py <tag> <musica> <volumen> [offset]`: mezcla música + efectos sintetizados.
  - Los scripts asumen rutas en /home/claude/reels: copiar `tools/*` allí y la música a `/home/claude/reels/audio/` (convertir mp3 a wav).

## Reglas de contenido
- Nunca mostrar datos reales de clientes: en las grabaciones se reemplazan nombre, dirección y teléfono por datos de ejemplo.
- Invitación demo de XV: https://ajcnazar.github.io/invitacion-flor/ — NO usarla más salvo que Alberto lo pida: ya se publicó demasiado contenido de XV.
- Variar eventos: bodas, cumpleaños infantiles y de adultos, baby shower, grados, diciembre (novenas, fin de año), aniversarios. Crear invitaciones nuevas en `invitaciones/` en vez de repetir las mismas.
- Cierre de cada caption: "Comenta INFO" + "Síguenos: cada día un diseño nuevo".
