"""Genera carruseles Momelinv 1080x1350 (HTML -> JPG con Playwright)."""
import os, sys
from playwright.sync_api import sync_playwright

FONTS = "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Jost:wght@300;400;500;600&display=swap"

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px}
body{background:#F8F2EC;color:#5B463F;font-family:Jost,sans-serif;position:relative;overflow:hidden}
.frame{position:absolute;inset:44px;border:2px solid #C9A36B;border-radius:28px}
.frame:after{content:"";position:absolute;inset:12px;border:1px solid rgba(201,163,107,.45);border-radius:20px}
.blob{position:absolute;border-radius:50%;background:#D4B0A0;opacity:.22}
.top{position:absolute;top:96px;left:110px;right:110px;display:flex;justify-content:space-between;font:500 24px Jost;letter-spacing:.32em;color:#C9A36B}
.wrap{position:absolute;top:190px;left:120px;right:120px;bottom:190px;display:flex;flex-direction:column;justify-content:center}
.foot{position:absolute;bottom:96px;left:110px;right:110px;display:flex;justify-content:space-between;align-items:center;font:400 26px Jost;color:#5B463F;opacity:.8}
.foot b{font-weight:500;color:#C9A36B}
h1{font:600 108px/1.02 'Cormorant Garamond',serif;color:#5B463F}
h1 em,h2 em{font-style:italic;color:#C9A36B;font-weight:600}
h2{font:600 84px/1.05 'Cormorant Garamond',serif;margin-bottom:34px}
.kick{font:500 28px Jost;letter-spacing:.28em;text-transform:uppercase;color:#D4B0A0;margin-bottom:28px}
.sub{font:300 40px/1.4 Jost;margin-top:40px}
p{font:300 38px/1.5 Jost}
p strong{font-weight:500}
.rule{width:140px;height:3px;background:#C9A36B;margin:38px 0}
.num{font:600 230px/0.8 'Cormorant Garamond',serif;color:#D4B0A0;opacity:.9;margin-bottom:10px}
.pill{display:inline-block;align-self:flex-start;background:#5B463F;color:#F8F2EC;font:500 30px Jost;padding:18px 34px;border-radius:999px;margin-top:44px;letter-spacing:.02em}
.pill.r{background:#D4B0A0;color:#5B463F}
.quote{background:#fff;border:2px solid #E8D6C4;border-radius:30px;padding:56px 54px;position:relative;box-shadow:0 18px 40px rgba(91,70,63,.08)}
.quote:before{content:"“";position:absolute;top:-70px;left:30px;font:700 200px 'Cormorant Garamond';color:#D4B0A0}
.quote p{font:500 italic 50px/1.3 'Cormorant Garamond',serif;font-style:italic}
.dots{display:flex;gap:22px;margin:34px 0 10px}
.dots span{width:84px;height:84px;border-radius:50%;border:4px solid #fff;box-shadow:0 6px 18px rgba(91,70,63,.18)}
.center{text-align:center;align-items:center}
.handle{font:600 italic 92px 'Cormorant Garamond';color:#5B463F}
.big{font:600 150px/1 'Cormorant Garamond';color:#C9A36B;letter-spacing:.04em}
.list{list-style:none;margin-top:10px}
.list li{font:300 38px/1.4 Jost;padding:18px 0 18px 64px;position:relative;border-bottom:1px solid rgba(201,163,107,.35)}
.list li:before{content:"✦";position:absolute;left:8px;top:18px;color:#C9A36B}
.bars{margin-top:10px}
.bars .b{margin:0 0 22px}
.bars .b div{display:flex;justify-content:space-between;font:400 32px Jost;margin-bottom:8px}
.bars .b div b{font:600 34px Jost;color:#C9A36B}
.bars .b i{display:block;height:20px;border-radius:10px;background:#D4B0A0}
.emo{width:190px;height:190px;border-radius:50%;background:#fff;border:3px solid #E8D6C4;display:flex;align-items:center;justify-content:center;font-size:110px;box-shadow:0 18px 40px rgba(91,70,63,.1);margin-bottom:30px;position:relative}
.emo span{position:absolute;right:-14px;top:-10px;width:70px;height:70px;border-radius:50%;background:#5B463F;color:#F8F2EC;font:600 40px/70px 'Cormorant Garamond';text-align:center}
.sol{margin-top:40px;background:#fff;border-left:8px solid #C9A36B;border-radius:18px;padding:24px 28px;font:300 32px/1.4 Jost}
.sol b{display:block;font:600 22px Jost;letter-spacing:.22em;color:#C9A36B;margin-bottom:6px}
"""


def page_html(body, i, n, swipe=True):
    foot_r = "Desliza →" if swipe and i < n else ""
    return f"""<!doctype html><html><head><meta charset=utf-8><link href="{FONTS}" rel=stylesheet><style>{CSS}</style></head>
<body><div class=blob style="width:520px;height:520px;right:-180px;top:-160px"></div>
<div class=blob style="width:380px;height:380px;left:-150px;bottom:-120px;opacity:.16"></div>
<div class=frame></div>
<div class=top><span>MOMELINV</span><span>{i:02d} / {n:02d}</span></div>
<div class=wrap>{body}</div>
<div class=foot><span><b>@momelinv</b> · invitaciones digitales</span><span>{foot_r}</span></div></body></html>"""


CLOSE = """<div class="center" style="display:flex;flex-direction:column;align-items:center;text-align:center">
<div class=kick>¿Te sirvió? Guárdalo 📌</div>
<div style="font:300 40px Jost;margin-bottom:10px">Síguenos</div>
<div class=handle>@momelinv</div>
<div class=rule style="margin:44px auto"></div>
<p>Invitaciones digitales e interactivas<br>para bodas, XV años y cumpleaños</p>
<div style="margin-top:60px;font:400 36px Jost">Comenta</div>
<div class=big>INFO</div>
<div style="font:300 34px Jost;margin-top:14px">y te enviamos precios 💌</div></div>"""


def theme(n, name, dots, idea):
    d = "".join(f'<span style="background:{c}"></span>' for c in dots)
    return f"""<div class=num>{n}</div><h2>{name}</h2><div class=dots>{d}</div><div class=rule></div><p>{idea}</p>"""


def step(when, title, text, tag=None):
    t = f'<div class="pill r">{tag}</div>' if tag else ""
    return f"""<div class=kick>{when}</div><h2>{title}</h2><div class=rule></div><p>{text}</p>{t}"""


def frase(kind, txt):
    return f"""<div class=kick>{kind}</div><div class=quote><p>{txt}</p></div>
<p style="margin-top:46px;font-size:32px;opacity:.85">Cópiala tal cual o ajústala a tu estilo ✨</p>"""


CARRUSELES = {
    "cronograma": [
        """<div class=kick>Bodas · XV · Cumpleaños</div><h1>¿Cuándo<br>enviar tu<br><em>invitación?</em></h1>
<p class=sub>El cronograma que nadie te dice<br>(y que evita invitados perdidos)</p><div><span class=pill>Guárdalo 📌</span></div>""",
        step("8 a 10 semanas antes", "Avisa la <em>fecha</em>", "Un mensaje de “reserva la fecha”, sobre todo si tienes invitados que viajan o el evento es en temporada alta.", "Bodas"),
        step("6 semanas antes", "Envía la <em>invitación</em>", "<strong>Bodas:</strong> 6 semanas antes.<br><strong>XV y cumpleaños:</strong> 3 a 4 semanas antes.<br>Así nadie dice “no me enteré”."),
        step("3 semanas antes", "Cierra las <em>confirmaciones</em>", "Pon una fecha límite para confirmar. Con confirmación por WhatsApp llevas la lista sin perseguir a nadie."),
        step("1 semana antes", "Manda el <em>recordatorio</em>", "Hora, ubicación y código de vestimenta. Con una invitación digital solo reenvías el mismo link 📲"),
        step("Temporada de fiestas", "Diciembre se llena <em>rápido</em>", "Si tu evento es en diciembre o enero, adelanta todo <strong>2 semanas</strong>: la agenda de tus invitados se llena de novenas, grados y viajes.", "Tip extra"),
        CLOSE,
    ],
    "temas-xv": [
        """<div class=kick>Ideas para quinceañeras</div><h1>5 temas para<br>tus <em>XV años</em><br>que enamoran</h1>
<p class=sub>Con paleta de colores incluida.<br>Guárdalo y muéstraselo a tu mamá 💛</p><div><span class=pill>Desliza para verlos</span></div>""",
        theme("1", "Jardín <em>encantado</em>", ["#8FA98A", "#F3EEE2", "#C9A36B", "#E9C6C0"], "Mariposas, flores y verde salvia. En la invitación: pétalos que caen y mariposas que vuelan al tocar la pantalla."),
        theme("2", "Princesa <em>de cuento</em>", ["#E8C5CF", "#FFFFFF", "#C9A36B", "#B98FA0"], "Corona, castillo y vestido de gala. Ideal para una entrada con carruaje o vals de película."),
        theme("3", "Una noche <em>en París</em>", ["#D4B0A0", "#1F1F1F", "#F8F2EC", "#C9A36B"], "Rosa empolvado, negro y dorado. Torre Eiffel, macarons y luces cálidas."),
        theme("4", "Cielo de <em>estrellas</em>", ["#1E2A4A", "#C9A36B", "#8E9CC8", "#F2EBDD"], "Azul noche y dorado. Luna, constelaciones y una cuenta regresiva que brilla."),
        theme("5", "Baile de <em>máscaras</em>", ["#6B1E2E", "#C9A36B", "#1A1A1A", "#E7D7C1"], "Vino tinto y dorado, misterio y elegancia. Pide antifaz en el código de vestimenta."),
        CLOSE,
    ],
    "frases-sobres": [
        """<div class=kick>Sin pena y con elegancia</div><h1>Frases para<br>pedir <em>lluvia<br>de sobres</em></h1>
<p class=sub>Para bodas, XV y cumpleaños.<br>Cópialas y úsalas en tu invitación ✨</p><div><span class=pill>Guárdalo 📌</span></div>""",
        frase("Para bodas", "Tu presencia es nuestro mejor regalo. Si además deseas tener un detalle con nosotros, una lluvia de sobres nos ayudará a empezar esta nueva etapa."),
        frase("Para bodas", "Ya tenemos casa, cariño y muchas ganas de celebrar… si quieres sumarte a nuestros sueños, tendremos un buzón de sobres esperándote 💌"),
        frase("Para XV años", "Lo más importante para mí es que estés en mi noche soñada. Si quieres regalarme algo, me encantaría una lluvia de sobres."),
        frase("Para cumpleaños", "Tu compañía es el mejor regalo. Si deseas traer un detalle, habrá una cajita de sobres en la entrada."),
        """<div class=kick>El truco</div><h2>Va en la invitación,<br><em>no en el chat</em></h2><div class=rule></div>
<ul class=list><li>Dale su propia sección, con un ícono bonito</li><li>Usa un tono cálido, nunca de cobro</li><li>Si quieres, agrega tu Nequi o cuenta para quien no pueda ir</li></ul>""",
        CLOSE,
    ],
}


CLOSE2 = CLOSE.replace("para bodas, XV años y cumpleaños", "para bodas, cumpleaños, grados y más")


def close_q(q):
    return CLOSE2.replace('<div class=kick>¿Te sirvió? Guárdalo 📌</div>', f'<div class=kick>{q}</div>')


def bars(rows):
    h = "".join(f'<div class=b><div><span>{n}</span><b>{v} %</b></div><i style="width:{v*2}%"></i></div>' for n, v in rows)
    return f'<div class=bars>{h}</div>'


def tipo(n, emoji, name, txt, sol):
    return f"""<div class=emo>{emoji}<span>{n}</span></div><h2>{name}</h2><p>{txt}</p>
<div class=sol><b>SOLUCIÓN</b>{sol}</div>"""


CARRUSELES.update({
    "presupuesto": [
        """<div class=kick>Bodas · Cumpleaños · Grados</div><h1>¿En qué se va<br><em>la plata</em><br>de tu fiesta?</h1>
<p class=sub>La repartición que usan los organizadores,<br>en porcentajes 💸</p><div><span class=pill>Guárdalo 📌</span></div>""",
        """<div class=kick>Así se reparte (aprox.)</div><h2>Tu presupuesto<br>en <em>7 partes</em></h2>""" + bars([
            ("Comida y bebida", 40), ("Lugar", 15), ("Música y animación", 10), ("Fotos y video", 10),
            ("Decoración", 10), ("Imprevistos", 10), ("Invitaciones y detalles", 5)]),
        step("La parte más grande", "Comida y bebida: <em>40 %</em>", "Es lo que más recuerdan tus invitados. Cotiza <strong>por persona</strong> y multiplica por los que confirmaron, no por los que invitaste.", "Tip"),
        step("Nadie lo planea", "Guarda el <em>10 %</em> para imprevistos", "Siempre aparece algo: hielo extra, transporte, una hora más de música o la mesa que faltó. Si no lo usas, ¡mejor!"),
        """<div class=kick>Sin que se note</div><h2>3 formas de <em>ahorrar</em></h2><div class=rule></div>
<ul class=list><li>Haz la fiesta un viernes o domingo: los lugares suelen cobrar menos</li><li>Menos invitados, mejor atendidos</li><li>Invitación digital: cero impresión y cero mensajería</li></ul>""",
        step("El truco de los que saben", "Presupuesta con <em>confirmados reales</em>", "Cada plato de más es plata perdida. Con confirmación por invitado sabes exactamente cuántos van antes de pagar el catering."),
        close_q("¿Te sirvió? Guárdalo 📌"),
    ],
    "tipos-invitados": [
        """<div class=kick>Todos tenemos uno 😂</div><h1>Los 5 invitados<br>que <em>nunca faltan</em><br>en una fiesta</h1>
<p class=sub>¿Cuál tienes en tu familia?<br>Etiquétalo sin miedo 👇</p><div><span class=pill>Desliza →</span></div>""",
        tipo("1", "🙋", "El <em>“¿puedo llevar<br>a alguien?”</em>", "Confirmó 1 y llega con 3. Uno es “un amigo que está de visita”.", "Escribe los cupos por invitación: “Familia Ríos · 2 cupos”."),
        tipo("2", "👻", "El <em>fantasma</em>", "Nunca respondió el mensaje… pero aparece en la foto de grupo.", "Fecha límite y un botón para confirmar con un toque."),
        tipo("3", "⏰", "El que llega<br><em>antes que el DJ</em>", "Te encuentra en chanclas inflando globos. Termina ayudando con las mesas.", "Pon el itinerario con horarios claros en la invitación."),
        tipo("4", "🍱", "El del <em>táper</em>", "Se lleva medio ponqué “para los de la casa” y un plato de arroz para mañana.", "Ninguna. Este es patrimonio de la familia 😂"),
        tipo("5", "💨", "El que confirma<br><em>y no llega</em>", "Dijo “fijo voy”. Su plato y su silla lo siguen esperando.", "Un recordatorio una semana antes, con el mismo link."),
        close_q("¿Cuál eres tú? 1, 2, 3, 4 o 5 👇"),
    ],
    "ninos-si-o-no": [
        """<div class=kick>Etiqueta para anfitriones</div><h1>¿Niños<br><em>sí o no</em><br>en tu fiesta?</h1>
<p class=sub>Cómo decirlo en la invitación<br>sin que nadie se ofenda</p><div><span class=pill>Guárdalo 📌</span></div>""",
        """<div class=kick>Paso 1</div><h2>Decide primero,<br><em>comunica después</em></h2><div class=rule></div>
<ul class=list><li>Fiesta familiar: todos invitados</li><li>Solo adultos</li><li>Solo los niños de la familia cercana</li></ul>
<p style="margin-top:34px;font-size:34px">Elige una y aplícala igual para todos: <strong>las excepciones son las que ofenden.</strong></p>""",
        frase("Si es solo para adultos", "Queremos que esta noche también sea para que ustedes la disfruten: la celebración será solo para adultos. ¡Gracias por entender! 💛"),
        frase("Si los niños sí van", "¡Los más pequeños también están invitados! Habrá un espacio con actividades para que ellos se diviertan 🎈"),
        step("Paso 2", "Escribe <em>los nombres</em>", "La invitación dice a quién se invita: <strong>“Carlos y Ana”</strong> o <strong>“Familia Gómez · 4 cupos”</strong>. Así nadie asume que van todos.", "Clave"),
        """<div class=kick>Si alguien pregunta…</div><h2>Responde <em>con cariño</em></h2><div class=rule></div>
<ul class=list><li>Sin dar mil explicaciones</li><li>Ofrece algo: “te guardo ponqué para los niños”</li><li>No hagas excepciones de última hora</li></ul>""",
        close_q("¿Niños sí o no? Te leemos 👇"),
    ],
})


def render(name, outdir):
    slides = CARRUSELES[name]
    os.makedirs(outdir, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for i, body in enumerate(slides, 1):
            pg.set_content(page_html(body, i, len(slides)), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(300)
            pg.screenshot(path=f"{outdir}/{i:02d}.jpg", type="jpeg", quality=92)
        b.close()
    print(name, len(slides))


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
