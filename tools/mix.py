"""Mezcla música + efectos (sintetizados aquí, libres) sobre un reel ya codificado."""
import json, os, subprocess, sys
import numpy as np
from scipy.io import wavfile

SR = 48000
rng = np.random.default_rng(7)


def env(n, a=0.004, d=0.4):
    t = np.arange(n) / SR
    return np.minimum(t / a, 1.0) * np.exp(-t / d)


def bell(f, dur, d, amp=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / (d * .4))
    return amp * s * env(n, .002, d)


def sparkle():
    out = np.zeros(int(.7 * SR))
    for i, f in enumerate(rng.choice([2093, 2349, 2637, 3136, 3520, 4186], 4, replace=False)):
        b = bell(f, .55, .12, .35); o = int(i * .045 * SR)
        out[o:o + len(b)] += b[:len(out) - o]
    return out


def seal():
    n = int(2.6 * SR); out = np.zeros(n)
    # "pop" suave del sello
    k = int(.06 * SR); noise = rng.standard_normal(k) * env(k, .001, .015)
    out[:k] += noise * .5 + bell(180, .06, .03, .6)[:k]
    # arpegio mágico ascendente
    for i, f in enumerate([1047, 1319, 1568, 2093, 2637, 3136, 4186]):
        b = bell(f, 1.2, .35, .3); o = int((.12 + i * .07) * SR)
        out[o:o + len(b)] += b[:n - o]
    # brillo de ruido filtrado (shimmer)
    m = int(1.6 * SR); sh = rng.standard_normal(m)
    sh = np.diff(np.concatenate([[0], sh])) * env(m, .3, .5) * .06
    out[int(.1 * SR):int(.1 * SR) + m] += sh
    return out


def tick():
    k = int(.05 * SR); return (rng.standard_normal(k) * env(k, .0005, .006) * .35 + bell(2400, .05, .01, .15))


def whoosh():
    n = int(.35 * SR); s = np.cumsum(rng.standard_normal(n)); s -= np.convolve(s, np.ones(200) / 200, 'same')
    t = np.arange(n) / n
    return s / np.abs(s).max() * np.sin(np.pi * t) ** 2 * .12


def bubble():
    n = int(.12 * SR); t = np.arange(n) / SR
    f = 500 + 1400 * (t / t[-1]) ** .6
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .003, .04) * .5


def wood():
    n = int(.08 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 880 * t) + .5 * np.sin(2 * np.pi * 1320 * t)) * env(n, .001, .018) * .45


def riser():
    n = int(1.6 * SR); t = np.arange(n) / SR
    f = 120 + 900 * (t / t[-1]) ** 2
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(t / 1.2, 1) * .25
    nz = rng.standard_normal(n); nz = np.diff(np.concatenate([[0], nz])) * (t / t[-1]) ** 2 * .12
    k = int(.5 * SR); boom = np.sin(2 * np.pi * np.cumsum(70 * np.exp(-np.arange(k) / SR * 6)) / SR) * env(k, .002, .25)
    out = np.concatenate([s + nz, np.zeros(k)]); out[n - int(.05 * SR):n - int(.05 * SR) + k] += boom * .8
    return out


def pluck_up():
    out = np.zeros(int(.5 * SR))
    for i, f in enumerate([660, 880, 1320]):
        b = bell(f, .35, .08, .4); o = int(i * .06 * SR); out[o:o + len(b)] += b[:len(out) - o]
    return out


def swish():
    n = int(.22 * SR); s = rng.standard_normal(n); s = np.diff(np.concatenate([[0], s]))
    t = np.arange(n) / n
    return s / np.abs(s).max() * np.sin(np.pi * t) ** 3 * .1


# Juegos de efectos: cambia SFX=<juego> en cada reel para no sonar siempre igual.
SETS = {
    "magia":    {"tap": sparkle, "seal": seal, "tick": tick, "cap": whoosh},
    "burbujas": {"tap": bubble, "seal": pluck_up, "tick": wood, "cap": swish},
    "despegue": {"tap": wood, "seal": riser, "tick": tick, "cap": swish},
    "suave":    {"tap": wood, "seal": pluck_up, "tick": wood, "cap": swish},
}
SFX = SETS[os.environ.get("SFX", "magia")]


def main(name, track, music_gain=0.8, offset=0.0):
    d = f"/home/claude/reels/frames_{name}"
    meta = json.load(open(f"{d}/frames.json"))
    start = meta["marks"].get("start", meta["frames"][0][1]); end = meta["marks"]["end"]
    dur = end - start
    events = json.load(open(f"{d}/events.json"))
    fx = np.zeros(int((dur + 3) * SR))
    for kind, ts in events:
        t = ts - start
        if t < -0.05 or t > dur:
            continue
        s = SFX[kind](); o = max(0, int(t * SR))
        fx[o:o + len(s)] += s[:len(fx) - o]
    fx = fx[:int(dur * SR)]
    fx = fx / max(1e-9, np.abs(fx).max()) * .55
    wavfile.write(f"{d}/fx.wav", SR, (fx * 32767).astype(np.int16))
    vid = f"/home/claude/reels/momelinv_reel_{name}.mp4"
    out = f"/home/claude/reels/momelinv_reel_{name}_audio.mp4"
    fo = max(0.0, dur - 1.5)
    filt = (f"[1:a]aresample={SR},atrim=start={offset},asetpts=PTS-STARTPTS,volume={music_gain},"
            f"afade=t=in:d=0.4,afade=t=out:st={fo:.2f}:d=1.5[m];"
            f"[2:a]aresample={SR}[f];[m][f]amix=inputs=2:normalize=0,alimiter=limit=0.95,"
            f"atrim=0:{dur:.3f}[a]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", track, "-i", f"{d}/fx.wav",
                    "-filter_complex", filt, "-map", "0:v", "-map", "[a]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-movflags", "+faststart", out],
                   check=True)
    print(out, f"{dur:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 0.8,
         float(sys.argv[4]) if len(sys.argv) > 4 else 0.0)
