"""Mezcla música + efectos (sintetizados aquí, libres) sobre un reel ya codificado."""
import json, subprocess, sys
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


SFX = {"tap": sparkle, "seal": seal, "tick": tick, "cap": whoosh}


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
