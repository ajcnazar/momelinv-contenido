# Catálogo de invitaciones demo

Cada invitación nueva debe ser **diferente a todas las de esta tabla en cada columna**, no solo en colores o tipo de evento.
Alberto pidió esto porque las primeras cuatro se veían como copias: misma estructura, mismas secciones, mismo recorrido en el reel.

| Invitación | Concepto / metáfora | Apertura | Navegación | Cuenta regresiva | Ubicación | Confirmación | Tipografía | Recorrido del reel |
|---|---|---|---|---|---|---|---|---|
| boda-playa | Pase de abordar | Tocar botón, el talón se rasga | Scroll vertical por secciones | 4 cajas (días/horas/min/seg) | Tarjeta + botón Maps | Botón WhatsApp | Cormorant + Jost + Great Vibes | Gancho → abrir → scroll por secciones → Comenta INFO |
| novena | Caja de regalo | Tocar caja, la tapa sale volando | Scroll vertical por secciones | 4 cajas | Tarjeta + botón Maps | Botón WhatsApp | Playfair + Jost + Dancing Script | Igual al anterior |
| cumple-espacial | Cohete | Botón, cuenta 3-2-1 y despega | Scroll vertical por secciones | 4 cajas | Tarjeta + botón Maps | Botón WhatsApp | Fredoka | Igual al anterior |
| baby-shower | Globo de revelación | Tocar globo, explota en confeti | Scroll vertical por secciones | 4 cajas | Tarjeta + botón Maps | Botón WhatsApp | Baloo 2 + Pacifico | Igual al anterior |
| periodico-40 | Periódico de cumpleaños (40 años) | Periódico doblado que se desdobla en 3D | Deslizar horizontal, 4 páginas con número de página | Cinta de "ÚLTIMA HORA" que corre abajo + "14 DÍAS" de titular | Aviso clasificado con mapa de tinta y círculo de marcador rojo | Recortar el cupón con tijeras: se desprende y cae, sello "CONFIRMADO" | UnifrakturMaguntia + Old Standard TT + Special Elite + Permanent Marker; papel periódico, tinta negra y rojo | Empieza por el final (recortar cupón) → rebobina a la portada → agenda → clasificados |
| grado-pixel | Videojuego retro 8 bits (grado universitario) | PRESS START + barra de carga | Historias: tocar para avanzar niveles, barras de progreso arriba y HUD | Barra de experiencia "para desbloquear la fiesta" + reloj DD:HH:MM:SS | Mapa de casillas con personaje que camina hasta la meta 🏁 | "¿Jugador 2 se une?": elegir opción y presionar A en un control | Press Start 2P + VT323; azul noche, amarillo, verde y coral pixel | Toda la invitación en velocidad x2 con distintivo ⏩ |

## Ya está gastado (no repetir)
- Estructura "portada → hero centrado → cuenta regresiva → tarjeta de lugar → regalos → confirmar" con scroll vertical.
- Cuenta regresiva en 4 cajitas, tarjetas redondeadas con botón "VER EN MAPS", botón en píldora "CONFIRMAR POR WHATSAPP".
- Estallido de emojis al tocar la pantalla, `.reveal` que sube al hacer scroll.
- Reel que recorre todas las secciones con los textos "Cuenta regresiva", "Ubicación", "Y confirman por WhatsApp".

## Ideas para que cada una sea distinta
- **Concepto completo, no solo decorado:** portada de periódico o revista, chat de WhatsApp que se va escribiendo, tocadiscos/vinilo con lista de canciones, álbum de polaroids, raspa y gana, boleto de cine, menú de restaurante, receta, mapa del tesoro, nivel de videojuego, calendario de pared que se arranca, carta de tarot, postal con estampilla, flor que se abre, telón de teatro, libro que pasa páginas, pantalla de reproductor de música.
- **Navegación distinta:** historias tipo Instagram (tocar para avanzar), deslizar horizontal, una sola tarjeta que gira en 3D, acordeón, páginas de libro, todo en una pantalla sin scroll.
- **Cuenta regresiva distinta:** reloj de tablero que voltea, reloj de arena, velas que se apagan, barra de carga, hojas de calendario, contador de pasos o niveles.
- **Ubicación distinta:** mapa ilustrado con pin animado, señal de carretera, sello en el boleto, coordenadas en una brújula.
- **Confirmación distinta:** "desliza para confirmar", estampar un sello, marcar casillas, elegir sticker, raspar, tocar y mantener.
- **Estilo distinto:** minimalista blanco y negro, brutalista, retro de los 70, acuarela, neón, papel kraft, editorial, pixel art, bordado, Y2K.
- **Reel distinto:** enfocar UNA sola función de cerca, POV, antes vs ahora, "3 detalles que nadie nota", velocidad x2 de toda la invitación, comparar dos diseños, empezar por el final.

Al crear una invitación, agrega su fila a la tabla.


## Escenas de humor (tools/escenas/)
No son invitaciones: son escenarios para reels de humor (100 % originales, nombres inventados).
- `chat-tia/` — chat que se escribe solo (la tía pregunta la dirección 5 veces). API: msg(), day(), typing(), big(), voice().
- `lista-mama/` — cuaderno con la lista de invitados que crece + panel de confirmaciones. API: line(), note(), dash().
