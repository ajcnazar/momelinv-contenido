import base64, json, os, sys, time
from playwright.sync_api import sync_playwright

URL = "https://ajcnazar.github.io/invitacion-flor/"

REPLACE = [
    ("Angella", "Valentina"),
    ("Carrera 7C #67B-93", "Calle 84 #52-30"),
    ("Carrera+7C+%2367B-93", "Calle+84+%2352-30"),
    ("Conjunto Ventura", "Hacienda Las Flores"),
    ("Conjunto+Ventura", "Hacienda+Las+Flores"),
    ("573012019283", "573000000000"),
]

INIT = r"""
(() => {
  const css = `
  #__ov{position:fixed;left:0;right:0;top:14%;z-index:2147483646;display:flex;justify-content:center;pointer-events:none;padding:0 18px}
  #__ov.bottom{top:auto;bottom:__BOTTOM__}
  #__ov .b{font:600 21px/1.25 Poppins,sans-serif;color:#fff;background:rgba(18,40,30,.78);padding:12px 18px;border-radius:16px;
     text-align:center;max-width:320px;box-shadow:0 8px 30px rgba(0,0,0,.25);border:1px solid rgba(240,217,154,.55);
     opacity:0;transform:translateY(10px) scale(.96);transition:opacity .35s ease, transform .35s ease}
  #__ov .b.on{opacity:1;transform:none}
  #__ov .b em{font-style:normal;color:#f0d99a}
  .__tap{position:fixed;width:46px;height:46px;margin:-23px 0 0 -23px;border-radius:50%;z-index:2147483647;pointer-events:none;
     background:rgba(255,255,255,.55);border:2px solid rgba(255,255,255,.9);animation:__tp .6s ease-out forwards}
  @keyframes __tp{from{transform:scale(.5);opacity:1}to{transform:scale(1.6);opacity:0}}
  `;
  const boot = () => {
    const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    const ov = document.createElement('div'); ov.id='__ov'; ov.innerHTML='<div class="b"></div>';
    document.body.appendChild(ov);
    document.addEventListener('pointerdown', e => {
      const t = document.createElement('div'); t.className='__tap';
      t.style.left=e.clientX+'px'; t.style.top=e.clientY+'px'; document.body.appendChild(t);
      setTimeout(()=>t.remove(),700);
    }, true);
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
  window.__cap = (html, pos) => {
    const ov = document.getElementById('__ov'); const b = ov.firstChild;
    if (!html){ b.classList.remove('on'); return; }
    ov.className = pos === 'bottom' ? 'bottom' : '';
    b.classList.remove('on');
    setTimeout(()=>{ b.innerHTML = html; b.classList.add('on'); }, 120);
  };
  window.__scroll = (y, ms) => new Promise(res => {
    const y0 = scrollY, t0 = performance.now();
    const ease = t => t<.5 ? 4*t*t*t : 1-Math.pow(-2*t+2,3)/2;
    const step = now => { const k = Math.min(1,(now-t0)/ms); scrollTo(0, y0+(y-y0)*ease(k));
      if (k<1) requestAnimationFrame(step); else res(); };
    requestAnimationFrame(step);
  });
  window.__top = sel => { const el=document.querySelector(sel); return el.getBoundingClientRect().top + scrollY; };
})();
"""


class Rec:
    def __init__(self, page, outdir):
        self.page, self.outdir = page, outdir
        os.makedirs(outdir, exist_ok=True)
        self.frames = []
        self.cdp = page.context.new_cdp_session(page)
        self.cdp.on("Page.screencastFrame", self.on_frame)
        self.marks = {}

    def on_frame(self, p):
        ts = p["metadata"]["timestamp"]
        fn = os.path.join(self.outdir, f"f{len(self.frames):05d}.jpg")
        with open(fn, "wb") as f:
            f.write(base64.b64decode(p["data"]))
        self.frames.append((fn, ts))
        try:
            self.cdp.send("Page.screencastFrameAck", {"sessionId": p["sessionId"]})
        except Exception:
            pass

    def start(self):
        self.cdp.send("Page.startScreencast", {"format": "jpeg", "quality": int(os.environ.get("JPGQ", 92)),
                                               "maxWidth": int(os.environ.get("OUT_W",1080)), "maxHeight": int(os.environ.get("OUT_H",1920)), "everyNthFrame": 1})

    def stop(self):
        self.cdp.send("Page.stopScreencast")
        with open(os.path.join(self.outdir, "frames.json"), "w") as f:
            json.dump({"frames": self.frames, "marks": self.marks}, f)

    def mark(self, name):
        self.marks[name] = time.time()

    def wait(self, s):
        self.page.wait_for_timeout(int(s * 1000))


def tap(page, x, y):
    page.mouse.move(x, y)
    page.mouse.down(); page.mouse.up()


def cap(page, html, pos=None):
    page.evaluate("([h,p]) => __cap(h,p)", [html, pos])


def scroll_to(page, sel_or_y, ms, offset=0):
    if isinstance(sel_or_y, str):
        y = page.evaluate("s => __top(s)", sel_or_y) + offset
    else:
        y = sel_or_y
    page.evaluate("([y,ms]) => __scroll(y,ms)", [y, ms])


def open_invite(page, r, slow=True):
    seal = page.locator("#seal").bounding_box()
    cx, cy = seal["x"] + seal["width"] / 2, seal["y"] + seal["height"] / 2
    tap(page, cx, cy)
    r.wait(3.9 if slow else 3.6)


def reel_apertura(page, r):
    r.wait(0.4)
    cap(page, "Así reciben tus invitados<br>su <em>invitación de XV</em>")
    r.wait(2.8)
    open_invite(page, r)
    cap(page, None)
    r.wait(1.6)
    for (x, y) in [(110, 260), (250, 200), (180, 420), (90, 520), (270, 470)]:
        tap(page, x, y); r.wait(0.35)
    cap(page, "Toca la pantalla y<br><em>se llena de magia</em>", "bottom")
    r.wait(2.4)
    scroll_to(page, "#welcome", 2200, -40); r.wait(2.6)
    cap(page, "¿Quieres una así?<br>Comenta <em>INFO</em>", "bottom")
    r.wait(3.2)


def reel_recorrido(page, r):
    r.wait(0.3)
    cap(page, "Una invitación de XV<br>que <em>nadie olvida</em>")
    r.wait(2.2)
    open_invite(page, r)
    cap(page, None)
    r.wait(1.8)
    steps = [
        ("#welcome", -30, "Música, mariposas y<br><em>pétalos animados</em>"),
        ("#count", -30, "Cuenta regresiva<br><em>en tiempo real</em>"),
        ("#details", -20, "Fecha, hora y<br><em>ubicación en Maps</em>"),
        ("#gift", -30, "Lluvia de sobres y<br><em>código de vestimenta</em>"),
        ("#rsvp", -60, "Confirman asistencia<br><em>por WhatsApp</em>"),
    ]
    for sel, off, text in steps:
        cap(page, None)
        scroll_to(page, sel, 1700, off); r.wait(1.9)
        cap(page, text, "bottom"); r.wait(2.6)
    cap(page, "Bodas · XV años · Cumpleaños<br>Comenta <em>INFO</em> y te paso precios", "bottom")
    r.wait(3.4)


def reel_sobres(page, r):
    # se abre fuera de cámara y se arranca en la sección del regalo
    open_invite(page, r, slow=False)
    scroll_to(page, "#details", 10, 200); r.wait(0.6)
    r.mark("start")
    cap(page, "¿Cómo pedir <em>lluvia de sobres</em><br>sin que suene raro?")
    r.wait(2.6)
    scroll_to(page, "#gift", 1800, -30); r.wait(2.0)
    cap(page, "Así: bonito, claro<br>y <em>con estilo</em>", "bottom")
    r.wait(3.0)
    cap(page, "Y hasta el <em>color que no</em><br>deben usar", "bottom")
    r.wait(3.0)
    scroll_to(page, "#rsvp", 1600, -60); r.wait(1.8)
    cap(page, "Tu invitación digital<br>Comenta <em>INFO</em>", "bottom")
    r.wait(3.2)


REELS = {"apertura": reel_apertura, "recorrido": reel_recorrido, "sobres": reel_sobres}


def main(name):
    out = f"/home/claude/reels/frames_{os.environ.get('TAG', name)}"
    os.system(f"rm -rf {out}")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome",
                              args=["--autoplay-policy=no-user-gesture-required", "--enable-gpu-rasterization", "--force-device-scale-factor=" + os.environ.get("DPR", "3")])
        ctx = b.new_context(viewport={"width": int(os.environ.get("VW",360)), "height": int(os.environ.get("VH",640))}, device_scale_factor=float(os.environ.get("DPR",3)),
                            is_mobile=True, has_touch=False, locale="es-CO",
                            timezone_id="America/Bogota")
        page = ctx.new_page()

        def handle(route):
            resp = route.fetch()
            body = resp.text()
            for a, bb in REPLACE:
                body = body.replace(a, bb)
            route.fulfill(response=resp, body=body)
        page.route("**/invitacion-flor/", handle)
        page.route("**/invitacion-flor/index.html", handle)
        page.add_init_script(INIT.replace("__BOTTOM__", os.environ.get("CAP_BOTTOM","27%")))
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(800)
        r = Rec(page, out)
        r.start()
        r.mark("t0")
        REELS[name](page, r)
        r.mark("end")
        r.stop()
        b.close()
    print(name, len(r.frames), "frames")


if __name__ == "__main__":
    main(sys.argv[1])
