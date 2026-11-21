"""Reels semana 23-29 nov: 2 invitaciones nuevas (periodico-40, grado-pixel) y 2 escenas de humor (tools/escenas/).
Uso: DPR=2 OUT_W=720 OUT_H=1280 python3 record5.py <tia|mama|periodico|grado>
grado se graba a velocidad normal y se acelera x2 (SPEED) antes de codificar."""
import json, os, sys
from playwright.sync_api import sync_playwright
import record as R
import record2 as R2
from record2 import ev, tap, ripple, center, cap

REPO = os.environ.get("REPO", "/home/claude/momelinv-contenido")
STYLE = {  # fondo del texto, color de énfasis, borde
    "tia": ("rgba(62,92,85,.92)", "#FFE08A"),
    "mama": ("rgba(42,63,122,.9)", "#FFD6A0"),
    "periodico": ("rgba(27,26,23,.9)", "#F0C05A"),
    "grado": ("rgba(177,62,83,.92)", "#FFCD75"),
}


def say(page, side, html, cnt=None):
    ev("tap")
    page.evaluate("([s,h,c]) => msg(s,h,c)", [side, html, cnt])


def reel_tia(page, r):
    page.evaluate("setTime(18,0); day('Lunes')")
    page.evaluate("msg('r','Tía, mi fiesta de 30 es el sábado a las 7 p.m. 🎉 Calle 00 #00-00 💃')")
    r.wait(0.6)
    r.mark("start")
    cap(page, "La tía cuando le mandas<br>la <em>dirección</em> de la fiesta 😂")
    r.wait(1.5)
    page.evaluate("typing(true)"); r.wait(0.6); page.evaluate("typing(false)")
    say(page, "l", "Ay mija qué bueno 😍 ¿y dónde es?", 1); r.wait(1.3)
    say(page, "r", "Calle 00 #00-00, tía 🙂"); r.wait(1.0)
    page.evaluate("day('Jueves')")
    say(page, "l", "Mija, ¿me repites la dirección? Se me borró el chat 🙈", 2); r.wait(1.6)
    page.evaluate("day('Viernes')")
    say(page, "l", page.evaluate("voice('0:47')"), 3)
    cap(page, "Audio de 0:47 preguntando<br><em>lo mismo</em> 🎤"); r.wait(1.9)
    page.evaluate("day('Sábado · 7:40 p.m.')")
    say(page, "l", "Ya salí ¿por dónde es que queda? 🚕", 4); r.wait(1.3)
    say(page, "l", '<div class="pic">🌳⛪🌳</div>Estoy en un parque con una iglesia ¿voy bien? 🤔', 5); r.wait(1.5)
    ev("tick"); page.evaluate("big('x5 😩')"); r.wait(1.1); page.evaluate("big(null)")
    cap(page, "Lo que debí mandar<br><em>desde el principio</em> 👇")
    r.wait(0.4)
    ev("seal")
    page.evaluate("""msg('r', `<div class="card"><div class="img"><small>CARO · 30 AÑOS</small><i>¡Celebremos!</i></div>
      <div class="tx">Invitación · Fiesta de Caro<span>Sábado 7:00 p.m. · toca para abrir</span></div><div class="bt">📍 Ver ubicación en Maps</div></div>`)""")
    r.wait(2.0)
    page.evaluate("typing(true)"); r.wait(0.5); page.evaluate("typing(false)")
    say(page, "l", "Ay qué belleza 😍 le di al botoncito y ya llegué 🥳"); r.wait(1.6)
    cap(page, "Ubicación en <em>un toque</em><br>Comenta <em>INFO</em> 💌"); r.wait(2.6)


def reel_mama(page, r):
    r.wait(0.3)
    r.mark("start")
    cap(page, "POV: le dices a mamá que<br>es <em>“solo para 30”</em> 😅")
    r.wait(1.7)
    ev("tick"); page.evaluate("line('✔ Los 30 de la lista', 30)"); r.wait(1.1)
    cap(page, "Mamá: <em>“solo unos poquitos más”</em>")
    for txt, n in [("+ la comadre Nelly y el esposo", 32), ("+ los vecinos del 3B (son 6)", 38),
                   ("+ el primo Jairo (¿quién?)", 39), ("+ los del trabajo de papá (15)", 54),
                   ("+ la señora de los tintos 💛", 55), ("+ “los que lleguen sin avisar”", "??")]:
        ev("tick"); page.evaluate("([t,n]) => line(t,n,true)", [txt, n]); r.wait(1.05)
    ev("seal"); page.evaluate("note('Mamá… el salón<br>es para 40 😰')"); r.wait(1.8)
    cap(page, "Lo que salva la fiesta 👇")
    r.wait(0.3); ev("seal"); page.evaluate("dash()"); r.wait(2.9)
    cap(page, "Confirman uno por uno<br>Comenta <em>INFO</em> 💌"); r.wait(2.6)


def reel_periodico(page, r):
    x, y = center(page, "#seal"); R.tap(page, x, y); r.wait(2.2)
    page.evaluate("goPage(3,10)"); r.wait(0.6)
    r.mark("start")
    cap(page, "Así confirman en este<br>cumpleaños de <em>40</em> ✂️")
    r.wait(1.4)
    x, y = center(page, "#scissors"); tap(page, x, y, "seal"); r.wait(2.7)
    cap(page, "¿Cómo llegamos aquí?<br><em>Desde el principio</em> ⏪")
    page.evaluate("goPage(0,1300)"); r.wait(1.8)
    cap(page, "Es un <em>periódico</em> 📰<br>de su cumpleaños"); r.wait(1.9)
    cap(page, "Y la cuenta regresiva es<br><em>noticia de última hora</em>"); r.wait(1.9)
    ripple(page, 300, 420)
    cap(page, "La agenda de la noche y<br>el <em>código de vestimenta</em>")
    page.evaluate("goPage(1,800)"); r.wait(2.1)
    ripple(page, 300, 420)
    cap(page, "Y el lugar, en los<br><em>clasificados</em> 📍")
    page.evaluate("goPage(2,800)"); r.wait(2.5)
    cap(page, "Cumple 30, 40 o 50…<br>Comenta <em>INFO</em> 🥂"); r.wait(2.6)


def reel_grado(page, r):
    page.evaluate("""() => { const b=document.createElement('div'); b.textContent='⏩ x2';
      b.style.cssText='position:fixed;right:12px;bottom:14px;z-index:2147483647;font:700 15px Poppins,sans-serif;color:#1A1C2C;background:#FFCD75;padding:5px 10px;border-radius:10px';
      document.body.appendChild(b); }""")
    r.mark("start")
    cap(page, "Un grado en <em>modo videojuego</em> 🎮")
    r.wait(2.6)
    x, y = center(page, "#start"); tap(page, x, y, "seal"); r.wait(1.4)
    cap(page, "Con el <em>puntaje</em><br>de toda la carrera ⭐"); r.wait(3.6)
    tap(page, 300, 560)
    cap(page, "La fiesta se <em>desbloquea</em><br>con la cuenta regresiva 🔓"); r.wait(3.8)
    tap(page, 300, 560)
    cap(page, "Un mapa que te lleva<br>hasta la <em>meta</em> 🏁"); r.wait(4.6)
    tap(page, 300, 560)
    cap(page, "Y confirman como<br><em>Jugador 2</em> 🕹️"); r.wait(2.2)
    x, y = center(page, "#btnA"); tap(page, x, y, "seal"); r.wait(3.4)
    cap(page, "Grados de diciembre 🎓<br>Comenta <em>INFO</em>"); r.wait(5.2)


REELS = {
    "tia": (f"{REPO}/tools/escenas/chat-tia/index.html", reel_tia),
    "mama": (f"{REPO}/tools/escenas/lista-mama/index.html", reel_mama),
    "periodico": (f"{REPO}/invitaciones/periodico-40/index.html", reel_periodico),
    "grado": (f"{REPO}/invitaciones/grado-pixel/index.html", reel_grado),
}


def speed_up(out, k):
    """Acelera la grabación k veces reescribiendo los tiempos de cuadros, marcas y eventos."""
    meta = json.load(open(f"{out}/frames.json"))
    t0 = meta["marks"].get("start", meta["frames"][0][1])
    f = lambda t: t0 + (t - t0) / k
    meta["frames"] = [(fn, f(ts)) for fn, ts in meta["frames"]]
    meta["marks"] = {a: f(t) for a, t in meta["marks"].items()}
    json.dump(meta, open(f"{out}/frames.json", "w"))
    evs = json.load(open(f"{out}/events.json"))
    json.dump([(a, f(t)) for a, t in evs], open(f"{out}/events.json", "w"))


def main(name):
    url, fn = REELS[name]
    tag = os.environ.get("TAG", name)
    out = f"/home/claude/reels/frames_{tag}"
    os.system(f"rm -rf {out}")
    dpr = os.environ.get("DPR", "2")
    bg, em = STYLE[name]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome",
                              args=["--autoplay-policy=no-user-gesture-required", "--force-device-scale-factor=" + dpr])
        ctx = b.new_context(viewport={"width": 360, "height": 640}, device_scale_factor=float(dpr),
                            is_mobile=True, has_touch=False, locale="es-CO", timezone_id="America/Bogota")
        page = ctx.new_page()
        init = R.INIT.replace("__BOTTOM__", "27%").replace("top:14%", "top:5.5%").replace("rgba(18,40,30,.78)", bg).replace("color:#f0d99a", "color:" + em)
        page.add_init_script("window.__demo=true;" + init)
        page.goto(f"file://{url}", wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(1200)
        r = R.Rec(page, out)
        r.start(); r.mark("t0")
        fn(page, r)
        r.mark("end"); r.stop()
        b.close()
    json.dump(R2.EVENTS, open(f"{out}/events.json", "w"))
    k = float(os.environ.get("SPEED", "2" if name == "grado" else "1"))
    if k != 1:
        speed_up(out, k)
    print(name, len(r.frames), "frames")


if __name__ == "__main__":
    main(sys.argv[1])
