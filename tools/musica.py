"""Generador de música original para los reels de Momelinv (100 % sintetizada aquí, libre de derechos).

Uso:  python3 musica.py <estilo> <salida.wav> [segundos] [semilla]
Estilos: tropical, lofi, dembow, infantil, synthwave, romantico, house, navidad (ver tools/navidad_music.py)
La semilla cambia tonalidad, melodía y progresión: misma semilla = misma canción.
Registra cada pista usada en audio/USO.md para no repetirla.
"""
import sys
import numpy as np
from scipy.signal import lfilter, butter

SR = 44100


# ---------------------------------------------------------------- utilidades
def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def t_(d):
    return np.arange(int(d * SR)) / SR


def env(n, a=0.005, d=0.3, s=0.0, r=0.05):
    t = np.arange(n) / SR
    e = np.minimum(t / max(a, 1e-4), 1) * (s + (1 - s) * np.exp(-t / max(d, 1e-4)))
    rel = int(r * SR)
    if rel and n > rel:
        e[-rel:] *= np.linspace(1, 0, rel)
    return e


def lp(x, fc, order=2):
    b, a = butter(order, min(fc / (SR / 2), 0.99))
    return lfilter(b, a, x)


def hp(x, fc, order=2):
    b, a = butter(order, min(fc / (SR / 2), 0.99), "high")
    return lfilter(b, a, x)


class Mix:
    def __init__(self, dur):
        self.L = np.zeros(int((dur + 4) * SR)); self.R = np.zeros_like(self.L)

    def add(self, s, at, gain=1.0, pan=0.0):
        o = int(at * SR)
        if o >= len(self.L) or len(s) == 0:
            return
        k = min(len(s), len(self.L) - o)
        self.L[o:o + k] += s[:k] * gain * (1 - max(0, pan))
        self.R[o:o + k] += s[:k] * gain * (1 + min(0, pan))


# ---------------------------------------------------------------- instrumentos
def kick(soft=False):
    t = t_(0.35); f = 45 + 110 * np.exp(-t * 28)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * (9 if soft else 6))
    return np.tanh(s * (1.2 if soft else 2.2))


def snare(rng, soft=False):
    t = t_(0.25); n = hp(rng.standard_normal(len(t)), 1800) * np.exp(-t * (22 if soft else 16))
    return (n * .7 + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * .5) * (.6 if soft else 1)


def clap(rng):
    t = t_(0.22); n = hp(rng.standard_normal(len(t)), 1200)
    e = sum(np.exp(-np.maximum(t - k * .011, 0) * 60) * (t >= k * .011) for k in range(3)) + np.exp(-t * 14) * .6
    return n * e * .6


def hat(rng, open_=False):
    t = t_(0.3 if open_ else 0.06)
    return hp(rng.standard_normal(len(t)), 7000) * np.exp(-t * (12 if open_ else 70)) * .35


def shaker(rng, accent=False):
    t = t_(0.09); n = hp(rng.standard_normal(len(t)), 5000)
    return n * np.minimum(t / .02, 1) * np.exp(-t * 40) * (.32 if accent else .18)


def conga(f, rng):
    t = t_(0.3); fr = f * (1 + .25 * np.exp(-t * 40))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 12) * .6 + hp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 90) * .1


def crackle(rng, dur):
    n = int(dur * SR); s = np.zeros(n)
    idx = rng.integers(0, n, int(dur * 25)); s[idx] = rng.uniform(-.4, .4, len(idx))
    return lp(s, 6000) + lp(rng.standard_normal(n), 900) * .01


def pluck(f, d, bright=0.5, rng=None):
    """Karplus-Strong: guitarra / ukelele / arpa."""
    n = int(d * SR); p = max(2, int(SR / f))
    x = np.zeros(n); x[:p] = (rng or np.random).uniform(-1, 1, p)
    a = 0.5 + bright * 0.49; g = 0.996
    den = np.zeros(p + 2); den[0] = 1; den[p] = -g * a; den[p + 1] = -g * (1 - a)
    out = lfilter([1.0], den, x)
    return out / (np.abs(out).max() + 1e-9) * env(n, .002, d * .7, 0, .03)


def marimba(f, d):
    t = t_(d); s = np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 25)
    return s * env(len(t), .002, .22, 0, .02)


def bell(f, d):
    t = t_(d)
    s = np.sin(2 * np.pi * f * t + 1.5 * np.sin(2 * np.pi * f * 3.5 * t) * np.exp(-t * 4))
    return s * env(len(t), .002, .6, 0, .05)


def epiano(f, d):
    t = t_(d)
    s = np.sin(2 * np.pi * f * t + .9 * np.exp(-t * 3) * np.sin(2 * np.pi * f * t))
    s += .15 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 2)
    return s * env(len(t), .004, .9, .15, .12) * (1 + .1 * np.sin(2 * np.pi * 4.5 * t))


def saw(f, t, det=0.0):
    ph = (f * (1 + det) * t) % 1.0
    return 2 * ph - 1


def pad(fs, d, bright=1800):
    t = t_(d); s = sum(saw(f, t, -.004) + saw(f, t, .004) for f in fs) / max(1, len(fs))
    return lp(s, bright) * env(len(t), .35, 10, .9, .4) * .5


def bass(f, d, kind="sub"):
    t = t_(d)
    if kind == "sub":
        s = np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * 2 * f * t)
    else:
        s = lp(saw(f, t) + saw(f, t, .006), 600 + 900 * np.exp(-t * 8).mean())
    return np.tanh(s * 1.3) * env(len(t), .005, d, .7, .04)


def lead(f, d):
    t = t_(d); vib = 1 + .006 * np.sin(2 * np.pi * 5.5 * t) * np.minimum(t / .25, 1)
    ph = np.cumsum(f * vib) / SR
    s = np.sign(np.sin(2 * np.pi * ph)) * .5 + np.sin(2 * np.pi * ph) * .5
    return lp(s, 2600) * env(len(t), .01, .4, .55, .06) * .6


# ---------------------------------------------------------------- armonía
MAJ, MIN = [0, 2, 4, 5, 7, 9, 11], [0, 2, 3, 5, 7, 8, 10]
PROGS = {
    "maj": [[0, 4, 5, 3], [0, 5, 3, 4], [3, 4, 0, 5], [0, 3, 0, 4], [5, 3, 0, 4]],
    "min": [[0, 5, 2, 6], [0, 3, 4, 0], [0, 6, 5, 6], [5, 6, 0, 0]],
}


def chord(root, scale, deg, seven=False):
    idx = [deg, deg + 2, deg + 4] + ([deg + 6] if seven else [])
    return [root + scale[i % 7] + 12 * (i // 7) for i in idx]


def melody(rng, root, scale, prog, rhythm, bars, oct_=12):
    """Motivo de 1 compás repetido sobre cada acorde, con variación leve: suena a canción, no a notas al azar."""
    motif = [int(rng.integers(0, 3)) * 2 for _ in rhythm]  # índices de nota del acorde (0,2,4)
    notes = []
    for b in range(bars):
        deg = prog[b % len(prog)]
        for (pos, d), k in zip(rhythm, motif):
            step = deg + k + (int(rng.integers(-1, 2)) if (b % 4 == 3 and rng.random() < .5) else 0)
            m = root + oct_ + scale[step % 7] + 12 * (step // 7)
            notes.append((b * 4 + pos, m, d))
    return notes


RHYTHMS = [
    [(0, .5), (.5, .5), (1.5, .5), (2, 1), (3, .5), (3.5, .5)],
    [(0, 1), (1, .5), (1.5, .5), (2.5, 1.5)],
    [(0, .75), (.75, .75), (1.5, .5), (2, .5), (2.5, .5), (3, 1)],
    [(.5, .5), (1, .5), (2, .5), (2.5, .5), (3, .5)],
    [(0, 1.5), (1.5, .5), (2, 1), (3, 1)],
]


# ---------------------------------------------------------------- estilos
def compose(style, dur, seed):
    rng = np.random.default_rng(seed)
    M = Mix(dur)
    cfg = {
        "tropical":  dict(bpm=98, mode="maj", roots=(60, 62, 65, 67)),
        "lofi":      dict(bpm=78, mode="min", roots=(57, 60, 62, 64)),
        "dembow":    dict(bpm=94, mode="min", roots=(57, 59, 62, 64)),
        "infantil":  dict(bpm=124, mode="maj", roots=(60, 62, 65, 67)),
        "synthwave": dict(bpm=108, mode="min", roots=(57, 59, 62, 64)),
        "romantico": dict(bpm=72, mode="maj", roots=(60, 62, 64, 65, 67)),
        "house":     dict(bpm=122, mode="min", roots=(57, 60, 62, 65)),
    }[style]
    beat = 60 / cfg["bpm"]; bar = 4 * beat
    root = int(rng.choice(cfg["roots"]))
    scale = MAJ if cfg["mode"] == "maj" else MIN
    prog = PROGS[cfg["mode"]][int(rng.integers(len(PROGS[cfg["mode"]])))]
    bars = int(np.ceil(dur / bar)) + 1
    rhythm = RHYTHMS[int(rng.integers(len(RHYTHMS)))]
    mel = melody(rng, root, scale, prog, rhythm, bars, 12)
    intro = 1  # primer compás sin batería, para que el gancho respire

    for b in range(bars):
        t0 = b * bar; deg = prog[b % len(prog)]
        ch = chord(root, scale, deg, seven=style in ("lofi", "romantico", "house"))
        drums = b >= intro

        if style == "tropical":  # cumbia: bajo 1-3, guacharaca en corcheas, congas, marimba
            M.add(bass(hz(ch[0] - 24), beat * .9), t0, .55); M.add(bass(hz(ch[2] - 24), beat * .9), t0 + 2 * beat, .5)
            M.add(pad([hz(m) for m in ch], bar, 1400), t0, .18)
            for k in range(8):
                M.add(shaker(rng, k % 2 == 1), t0 + k * beat / 2, 1, .3)
            if drums:
                for k, f in [(1, 220), (1.5, 330), (3, 220), (3.5, 330)]:
                    M.add(conga(f, rng), t0 + k * beat, .45, -.3)
                M.add(kick(True), t0, .5); M.add(kick(True), t0 + 2 * beat, .5)
        elif style == "lofi":
            M.add(crackle(rng, bar), t0, .5)
            for i, m in enumerate(ch):
                M.add(epiano(hz(m), bar * .95), t0 + i * .02, .22)
            M.add(bass(hz(ch[0] - 24), bar * .9), t0, .45)
            if drums:
                sw = beat * .08
                M.add(kick(True), t0, .7); M.add(kick(True), t0 + 2.5 * beat, .55)
                M.add(snare(rng, True), t0 + beat, .55); M.add(snare(rng, True), t0 + 3 * beat, .55)
                for k in range(8):
                    M.add(hat(rng), t0 + k * beat / 2 + (sw if k % 2 else 0), .6, .2)
        elif style == "dembow":
            M.add(pad([hz(m) for m in ch], bar, 1200), t0, .2)
            for k in (0, 1.5, 2, 3.5):
                M.add(bass(hz(ch[0] - 24), beat * .45, "saw"), t0 + k * beat, .22)
            if drums:
                for k in range(4):
                    M.add(kick(), t0 + k * beat, .38)
                for k in (.75, 1.5, 2.75, 3.5):
                    M.add(snare(rng), t0 + k * beat, .45)
                for k in range(8):
                    M.add(hat(rng), t0 + k * beat / 2, .5, .25)
        elif style == "infantil":  # ukelele rasgueado, palmas, glockenspiel
            for k, up in [(0, 0), (1, 1), (1.5, 0), (2.5, 1), (3, 0)]:
                for i, m in enumerate(ch if not up else ch[::-1]):
                    M.add(lp(pluck(hz(m), .5, .5, rng), 4000), t0 + k * beat + i * .012, .28, -.2)
            M.add(bass(hz(ch[0] - 24), beat * .5), t0, .45); M.add(bass(hz(ch[2] - 24), beat * .5), t0 + 2 * beat, .4)
            if drums:
                M.add(kick(True), t0, .5); M.add(kick(True), t0 + 2 * beat, .5)
                M.add(lp(clap(rng), 5000), t0 + beat, .22); M.add(lp(clap(rng), 5000), t0 + 3 * beat, .22)
        elif style == "synthwave":
            M.add(pad([hz(m) for m in ch], bar, 2200), t0, .28)
            for k in range(8):
                M.add(bass(hz(ch[0] - 24), beat * .45, "saw"), t0 + k * beat / 2, .17)
            arp = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 12]
            for k in range(16):
                M.add(pluck(hz(arp[k % 4]), .25, .9, rng), t0 + k * beat / 4, .14, .3 if k % 2 else -.3)
            if drums:
                for k in range(4):
                    M.add(kick(), t0 + k * beat, .35)
                M.add(snare(rng), t0 + beat, .5); M.add(snare(rng), t0 + 3 * beat, .5)
        elif style == "romantico":  # guitarra arpegiada + cuerdas
            M.add(pad([hz(m) for m in ch], bar, 1100), t0, .22)
            arp = [ch[0] - 12, ch[1], ch[2], ch[3] if len(ch) > 3 else ch[0] + 12, ch[2], ch[1]]
            M.add(bass(hz(ch[0] - 24), bar * .95), t0, .35)
            for k in range(8):
                M.add(lp(pluck(hz(arp[k % len(arp)]), 1.2, .2, rng), 2500), t0 + k * beat / 2, .3, -.25 + .5 * (k % 2))
        elif style == "house":
            for k in (0, 1.5, 2.5):
                for i, m in enumerate(ch):
                    M.add(epiano(hz(m + 12), beat * .4), t0 + k * beat + i * .005, .14)
            for k in range(4):
                M.add(bass(hz(ch[0] - 24), beat * .4, "saw"), t0 + k * beat + beat / 2, .38)
            if drums:
                for k in range(4):
                    M.add(kick(), t0 + k * beat, .4); M.add(hat(rng, True), t0 + k * beat + beat / 2, .5, .25)
                M.add(clap(rng), t0 + beat, .45); M.add(clap(rng), t0 + 3 * beat, .45)

    # melodía principal (entra en el compás 2)
    voice = {"tropical": marimba, "lofi": lambda f, d: pluck(f, d * 1.5, .3, rng), "dembow": lambda f, d: pluck(f, d, .8, rng),
             "infantil": bell, "synthwave": lead, "romantico": epiano, "house": lambda f, d: pluck(f, d, .85, rng)}[style]
    for pos, m, d in mel:
        if pos >= 4 * intro:
            M.add(voice(hz(m), d * beat * 1.1), pos * beat, .3 if style != "infantil" else .18, .1)

    n = int(dur * SR)
    L, R = M.L[:n], M.R[:n]
    peak = max(np.abs(L).max(), np.abs(R).max(), 1e-9)
    st = np.stack([L, R], 1) / peak * .89
    fade = int(1.2 * SR); st[-fade:] *= np.linspace(1, 0, fade)[:, None]
    return st, cfg["bpm"], root, prog


if __name__ == "__main__":
    from scipy.io import wavfile
    style, out = sys.argv[1], sys.argv[2]
    dur = float(sys.argv[3]) if len(sys.argv) > 3 else 30
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    st, bpm, root, prog = compose(style, dur, seed)
    wavfile.write(out, SR, (st * 32767).astype(np.int16))
    print(out, style, f"{bpm}bpm", "tono", root, "prog", prog, f"{dur}s", "semilla", seed)
