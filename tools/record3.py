"""Reels semana 17-22 nov: antes-ahora, diciembre, mama-xv."""
import json, os, sys
import record as R
import record2 as R2
from record2 import ev, tap, ripple, center, open_seal, cap


def reel_antes(page, r):
    r.mark("start")
    cap(page, "<em>ANTES:</em> imprimir 100 tarjetas<br>y repartirlas casa por casa")
    r.wait(2.6)
    cap(page, "<em>AHORA:</em> un link por WhatsApp<br>y la abren así 👇")
    r.wait(2.2)
    open_seal(page, r, 3.6)
    cap(page, None)
    for (x, y) in [(110, 250), (250, 200), (180, 430)]:
        tap(page, x, y); r.wait(0.35)
    r.wait(0.6)
    cap(page, "Con música, cuenta regresiva<br>y <em>ubicación en Maps</em>", "bottom")
    R.scroll_to(page, "#count", 1800, -30); r.wait(2.6)
    cap(page, None)
    R.scroll_to(page, "#details", 1500, -20); r.wait(1.8)
    x, y = center(page, "#details .cta"); ripple(page, x, y); r.wait(1.0)
    cap(page, "¿Tú cuál prefieres?<br>Comenta <em>INFO</em> y te paso precios", "bottom")
    r.wait(3.2)


def reel_diciembre(page, r):
    open_seal(page, r, 3.6)
    R.scroll_to(page, "#welcome", 10, -40); r.wait(0.6)
    r.mark("start")
    cap(page, "¿Tienes <em>grado, novena o fiesta</em><br>en diciembre? 🎄")
    for (x, y) in [(120, 300), (250, 420)]:
        tap(page, x, y); r.wait(0.5)
    r.wait(1.6)
    cap(page, "Tu invitación lista<br>en <em>pocos días</em>", "bottom")
    R.scroll_to(page, "#count", 1700, -30); r.wait(2.4)
    cap(page, "Llega a todos por WhatsApp<br><em>sin imprimir nada</em>", "bottom")
    R.scroll_to(page, "#details", 1600, -20); r.wait(2.4)
    cap(page, "Y te confirman<br><em>con un toque</em>", "bottom")
    R.scroll_to(page, "#rsvp", 1600, -60); r.wait(1.4)
    x, y = center(page, "#rsvp .cta"); ripple(page, x, y); r.wait(1.2)
    cap(page, "Diciembre se llena rápido<br>Comenta <em>INFO</em> hoy", "bottom")
    r.wait(3.2)


def reel_mama(page, r):
    r.mark("start")
    cap(page, "POV: eres la mamá de la<br>quinceañera y faltan <em>3 semanas</em> 😱")
    r.wait(2.6)
    cap(page, "Envías la invitación<br>a todos <em>en 1 minuto</em> 📲")
    r.wait(1.6)
    open_seal(page, r, 3.6)
    cap(page, None)
    for (x, y) in [(100, 260), (260, 220), (170, 470), (90, 380)]:
        tap(page, x, y); r.wait(0.35)
    cap(page, "Y nadie te llama a preguntar<br>la <em>dirección</em>", "bottom")
    R.scroll_to(page, "#details", 2200, -20); r.wait(2.6)
    cap(page, "Ni si hay <em>lluvia de sobres</em>", "bottom")
    R.scroll_to(page, "#gift", 1500, -30); r.wait(2.2)
    cap(page, "Etiqueta a una mamá que lo necesita<br>Comenta <em>INFO</em>", "bottom")
    r.wait(3.2)


R.REELS.update({"antes": reel_antes, "diciembre": reel_diciembre, "mama": reel_mama})

if __name__ == "__main__":
    name = sys.argv[1]
    R.main(name)
    json.dump(R2.EVENTS, open(f"/home/claude/reels/frames_{os.environ.get('TAG', name)}/events.json", "w"))
