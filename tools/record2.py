import json, os, sys, time
import record as R

EVENTS = []


def ev(kind):
    EVENTS.append((kind, time.time()))


def tap(page, x, y, kind="tap"):
    ev(kind)
    R.tap(page, x, y)


def ripple(page, x, y):
    """Muestra el toque visual sin hacer clic (para links que abrirían otra pestaña)."""
    ev("tap")
    page.evaluate("""([x,y]) => { const t=document.createElement('div'); t.className='__tap';
      t.style.left=x+'px'; t.style.top=y+'px'; document.body.appendChild(t); setTimeout(()=>t.remove(),700); }""", [x, y])


def center(page, sel):
    b = page.locator(sel).first.bounding_box()
    return b["x"] + b["width"] / 2, b["y"] + b["height"] / 2


def open_seal(page, r, wait=3.9):
    x, y = center(page, "#seal")
    tap(page, x, y, "seal")
    r.wait(wait)


def cap(page, html, pos=None):
    if html:
        ev("cap")
    R.cap(page, html, pos)


def reel_pov(page, r):
    r.mark("start")
    r.wait(0.3)
    cap(page, "POV: abres la invitación<br>de XV de <em>tu mejor amiga</em>")
    r.wait(2.6)
    open_seal(page, r)
    cap(page, None)
    r.wait(1.4)
    for (x, y) in [(120, 250), (240, 190), (180, 400), (95, 470), (265, 330)]:
        tap(page, x, y); r.wait(0.4)
    cap(page, "Y así empieza<br><em>la noche mágica</em>", "bottom")
    r.wait(2.4)
    R.scroll_to(page, "#welcome", 2600, -40); r.wait(2.9)
    cap(page, "¿La quieres para tu evento?<br>Comenta <em>INFO</em>", "bottom")
    r.wait(3.0)


def reel_cuenta(page, r):
    open_seal(page, r, 3.6)
    R.scroll_to(page, "#count", 10, -130); r.wait(1.2)
    r.mark("start")
    cap(page, "Tus invitados ven cuánto falta<br><em>segundo a segundo</em>")
    for _ in range(4):
        ev("tick"); r.wait(1.0)
    cap(page, "Y llegan al lugar<br><em>con un solo toque</em>", "bottom")
    R.scroll_to(page, "#details", 1600, -20); r.wait(2.0)
    x, y = center(page, "#details .cta")
    ripple(page, x, y); r.wait(2.2)
    cap(page, "Invitaciones digitales<br>Comenta <em>INFO</em>", "bottom")
    r.wait(3.0)


def reel_tres(page, r):
    open_seal(page, r, 3.6)
    r.wait(0.8)
    r.mark("start")
    cap(page, "3 cosas que tu invitación<br>de XV <em>debe tener</em>")
    r.wait(2.8)
    cap(page, None)
    R.scroll_to(page, "#details", 1600, -20); r.wait(1.7)
    cap(page, "<em>1.</em> Ubicación directa<br>en Google Maps", "bottom")
    x, y = center(page, "#details .cta"); r.wait(0.6); ripple(page, x, y); r.wait(1.9)
    cap(page, None)
    R.scroll_to(page, "#gift", 1500, -30); r.wait(1.6)
    cap(page, "<em>2.</em> Lluvia de sobres<br>dicha con elegancia", "bottom")
    r.wait(2.6)
    cap(page, None)
    R.scroll_to(page, "#rsvp", 1500, -60); r.wait(1.6)
    cap(page, "<em>3.</em> Confirmación<br>por WhatsApp", "bottom")
    x, y = center(page, "#rsvp .cta"); r.wait(0.6); ripple(page, x, y); r.wait(1.9)
    cap(page, "Las nuestras traen las 3<br>Comenta <em>INFO</em>", "bottom")
    r.wait(3.0)


def reel_recorrido_ev(page, r):
    orig_cap, orig_tap = R.cap, R.tap
    def c(p, h, pos=None):
        if h: ev("cap")
        orig_cap(p, h, pos)
    def t(p, x, y):
        ev("seal"); orig_tap(p, x, y)
    R.cap, R.tap = c, t
    try:
        R.reel_recorrido(page, r)
    finally:
        R.cap, R.tap = orig_cap, orig_tap


def make_ev(base):
    def f(page, r):
        orig_cap, orig_tap = R.cap, R.tap
        n = {"t": 0}
        def c(p, h, pos=None):
            if h: ev("cap")
            orig_cap(p, h, pos)
        def t(p, x, y):
            ev("seal" if n["t"] == 0 else "tap"); n["t"] += 1; orig_tap(p, x, y)
        R.cap, R.tap = c, t
        try:
            base(page, r)
        finally:
            R.cap, R.tap = orig_cap, orig_tap
    return f


R.REELS.update({"recorrido_ev": reel_recorrido_ev, "apertura_ev": make_ev(R.reel_apertura), "sobres_ev": make_ev(R.reel_sobres)})
R.REELS.update({"pov": reel_pov, "cuenta": reel_cuenta, "tres": reel_tres})

if __name__ == "__main__":
    name = sys.argv[1]
    R.main(name)
    json.dump(EVENTS, open(f"/home/claude/reels/frames_{os.environ.get('TAG', name)}/events.json", "w"))
