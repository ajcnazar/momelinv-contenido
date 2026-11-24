"""Versiones nuevas (gancho y recorrido distintos) de boda-playa y novena, para volver a publicarlas.
Uso: DPR=2 OUT_W=720 OUT_H=1280 python3 record6.py <boda2|novena2>"""
import sys
import record as R
import record4 as R4
from record2 import ev, tap, center, cap


def reel_boda2(page, r):
    r.mark("start")
    cap(page, "POV: tus invitados<br><em>abordan</em> tu boda ✈️")
    r.wait(1.6)
    x, y = center(page, "#seal"); tap(page, x, y, "seal"); r.wait(2.6)
    cap(page, "Se rasga el talón ✂️<br>y sale el <em>itinerario</em>")
    R.scroll_to(page, ".timeline", 2200, -260); r.wait(2.7)
    cap(page, "Ceremonia, cóctel<br>y <em>fiesta</em> 💃")
    R.scroll_to(page, ".timeline", 1400, -170); r.wait(2.2)
    cap(page, "¿Playa, finca o salón?<br>Comenta <em>INFO</em> 💍"); r.wait(2.6)


def reel_novena2(page, r):
    r.mark("start")
    cap(page, "¿Te toca <em>hacer novena</em><br>en casa este año? 🎄")
    r.wait(1.8)
    x, y = center(page, "#seal"); tap(page, x, y, "seal")
    cap(page, None); r.wait(2.4)
    cap(page, "Qué hay <em>cada noche</em><br>🙏 🎶 🧁 🎁")
    R.scroll_to(page, ".program", 1800, -215); r.wait(2.6)
    cap(page, "Y el <em>intercambio</em><br>de regalos 🎁")
    R.scroll_to(page, "#gift", 1600, -120); r.wait(2.4)
    cap(page, "¿Novena o fin de año?<br>Comenta <em>INFO</em> 🎄"); r.wait(2.6)


R4.REELS.update({"boda2": ("boda-playa", reel_boda2), "novena2": ("novena", reel_novena2)})
R4.CAP_BG.update({"boda2": R4.CAP_BG["boda"], "novena2": R4.CAP_BG["novena"]})
R4.CAP_EM.update({"boda2": R4.CAP_EM["boda"], "novena2": R4.CAP_EM["novena"]})

if __name__ == "__main__":
    R4.main(sys.argv[1])
