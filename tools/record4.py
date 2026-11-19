"""Reels con invitaciones propias del repo (invitaciones/*): boda-playa, novena, cumple-espacial.
Uso: DPR=2 OUT_W=720 OUT_H=1280 python3 record4.py <reel>
Las invitaciones ya traen solo datos de ejemplo."""
import json, os, sys
from playwright.sync_api import sync_playwright
import record as R
import record2 as R2
from record2 import ev, tap, ripple, center, cap

REPO = os.environ.get("REPO", "/home/claude/momelinv-contenido")
CAP_BG = {"boda": "rgba(30,58,90,.86)", "novena": "rgba(11,42,32,.86)", "cumple": "rgba(70,40,170,.88)"}
CAP_EM = {"boda": "#F3C8A8", "novena": "#E3BC6A", "cumple": "#FFD34E"}


def reel_boda(page, r):
    r.mark("start")
    cap(page, "Tu boda frente al mar merece<br>una invitación <em>así</em> 🌊")
    r.wait(2.4)
    cap(page, "Tus invitados <em>abordan</em><br>a tu boda ✈️")
    r.wait(1.0)
    x, y = center(page, "#seal"); tap(page, x, y, "seal"); r.wait(2.6)
    for (x, y) in [(110, 330), (250, 300), (180, 470)]:
        tap(page, x, y); r.wait(0.35)
    r.wait(0.5)
    steps = [(".timeline", -190, "Con el <em>itinerario</em><br>de todo el día"),
             ("#count", -120, "Cuenta regresiva<br><em>en vivo</em> ⏳"),
             ("#details", -110, "Ubicación en Maps y<br><em>código de vestimenta</em>"),
             ("#rsvp", -170, "Y confirman<br><em>por WhatsApp</em> 📲")]
    for sel, off, txt in steps:
        cap(page, txt); R.scroll_to(page, sel, 1300, off); r.wait(1.1)
    x, y = center(page, "#rsvp .cta"); ripple(page, x, y); r.wait(0.6)
    cap(page, "¿Te casas en 2027?<br>Comenta <em>INFO</em> 💍")
    r.wait(2.7)


def reel_novena(page, r):
    r.mark("start")
    cap(page, "¿Vas a hacer <em>novena</em> en casa? 🎄<br>Invita así 👇")
    r.wait(2.4)
    x, y = center(page, "#seal"); tap(page, x, y, "seal")
    cap(page, "Un regalo que <em>se abre</em> 🎁")
    r.wait(2.7)
    for (x, y) in [(120, 360), (240, 300), (180, 480)]:
        tap(page, x, y); r.wait(0.35)
    r.wait(0.4)
    steps = [(".program", -200, "Con el <em>programa</em><br>de cada noche"),
             ("#count", -120, "Cuenta regresiva a la<br><em>primera noche</em>"),
             ("#gift", -120, "Y el <em>intercambio</em><br>de regalos 🎁"),
             ("#rsvp", -170, "Te confirman<br><em>con un toque</em> 📲")]
    for sel, off, txt in steps:
        cap(page, txt); R.scroll_to(page, sel, 1300, off); r.wait(1.0)
    x, y = center(page, "#rsvp .cta"); ripple(page, x, y); r.wait(0.6)
    cap(page, "Diciembre se llena rápido<br>Comenta <em>INFO</em> hoy")
    r.wait(2.7)


def reel_cumple(page, r):
    r.mark("start")
    cap(page, "Tu hijo va a querer abrir esta<br>invitación <em>mil veces</em> 🚀")
    r.wait(2.4)
    x, y = center(page, "#seal"); tap(page, x, y, "seal")
    cap(page, None)
    for i in range(3):
        ev("tick"); r.wait(0.6)
    ev("cap"); r.wait(1.6)
    cap(page, "¡Despega y empieza<br>la <em>fiesta</em>! 🎉")
    r.wait(1.4)
    for (x, y) in [(100, 330), (260, 280), (180, 520), (90, 450)]:
        tap(page, x, y); r.wait(0.3)
    r.wait(0.3)
    steps = [(".acts", -200, "Con todas las<br><em>actividades</em> 🎈"),
             ("#count", -120, "Cuenta regresiva<br>para el <em>despegue</em>"),
             ("#details", -110, "Ubicación y<br><em>disfraz</em> del espacio"),
             ("#rsvp", -170, "Y confirman<br><em>por WhatsApp</em> 📲")]
    for sel, off, txt in steps:
        cap(page, txt); R.scroll_to(page, sel, 1300, off); r.wait(1.0)
    x, y = center(page, "#rsvp .cta"); ripple(page, x, y); r.wait(0.6)
    cap(page, "Cumpleaños infantiles<br>Comenta <em>INFO</em> ⭐")
    r.wait(2.7)


REELS = {"boda": ("boda-playa", reel_boda), "novena": ("novena", reel_novena), "cumple": ("cumple-espacial", reel_cumple)}


def main(name):
    folder, fn = REELS[name]
    tag = os.environ.get("TAG", name)
    out = f"/home/claude/reels/frames_{tag}"
    os.system(f"rm -rf {out}")
    dpr = os.environ.get("DPR", "2")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome",
                              args=["--autoplay-policy=no-user-gesture-required", "--force-device-scale-factor=" + dpr])
        ctx = b.new_context(viewport={"width": 360, "height": 640}, device_scale_factor=float(dpr),
                            is_mobile=True, has_touch=False, locale="es-CO", timezone_id="America/Bogota")
        page = ctx.new_page()
        init = R.INIT.replace("__BOTTOM__", "27%").replace("top:14%", "top:5.5%").replace("rgba(18,40,30,.78)", CAP_BG[name]).replace("color:#f0d99a", "color:" + CAP_EM[name])
        page.add_init_script(init)
        page.goto(f"file://{REPO}/invitaciones/{folder}/index.html", wait_until="networkidle")
        page.wait_for_timeout(1200)
        r = R.Rec(page, out)
        r.start(); r.mark("t0")
        fn(page, r)
        r.mark("end"); r.stop()
        b.close()
    json.dump(R2.EVENTS, open(f"{out}/events.json", "w"))
    print(name, len(r.frames), "frames")


if __name__ == "__main__":
    main(sys.argv[1])
