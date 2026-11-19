"""Música navideña original sintetizada (campanas + pad + cascabel), libre de derechos. Salida: wav 48k."""
import sys, numpy as np
from scipy.io import wavfile
SR=48000; rng=np.random.default_rng(3)
bpm=112; beat=60/bpm; dur=float(sys.argv[2]) if len(sys.argv)>2 else 26
N=int(dur*SR); out=np.zeros(N+SR*3)
def note(m): return 440*2**((m-69)/12)
def bell(f,d,amp):
    n=int(d*SR);t=np.arange(n)/SR
    s=np.sin(2*np.pi*f*t)+.4*np.sin(2*np.pi*f*2.0*t)*np.exp(-t*3)+.25*np.sin(2*np.pi*f*3.01*t)*np.exp(-t*6)
    return amp*s*np.minimum(t/.003,1)*np.exp(-t*2.2)
def pad(fs,d,amp):
    n=int(d*SR);t=np.arange(n)/SR;s=sum(np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*f*1.003*t) for f in fs)
    return amp*s*np.minimum(t/.4,1)*np.minimum((d-t)/.5,1)
def add(s,at):
    o=int(at*SR)
    if o>=len(out): return
    k=min(len(s),len(out)-o); out[o:o+k]+=s[:k]
# progresión D - Bm - G - A (2 compases c/u de 4 tiempos)
chords=[[62,66,69],[59,62,66],[55,59,62],[57,61,64]]
mel=[ # (tiempo en beats, midi, dur)
 (0,74,1),(1,76,.5),(1.5,78,.5),(2,81,1.5),(3.5,78,.5),(4,76,1),(5,74,1),(6,73,2),
 (8,71,1),(9,73,.5),(9.5,74,.5),(10,78,1.5),(11.5,76,.5),(12,74,1),(13,71,1),(14,69,2),
 (16,67,1),(17,69,.5),(17.5,71,.5),(18,74,1.5),(19.5,71,.5),(20,69,1),(21,67,1),(22,66,2),
 (24,69,1),(25,73,.5),(25.5,76,.5),(26,79,1),(27,78,1),(28,76,1),(29,73,1),(30,74,2)]
bar=32*beat; t=0
while t<dur:
    for i,c in enumerate(chords):
        add(pad([note(m-12) for m in c],8*beat,.05),t+i*8*beat)
        for b in range(8): add(bell(note(c[0]-24),.6,.12 if b%2==0 else .06),t+i*8*beat+b*beat)
    for (b,m,d) in mel: add(bell(note(m),max(.8,d*beat*1.6),.22),t+b*beat); add(bell(note(m+12),.5,.05),t+b*beat+.01)
    for k in range(64):  # cascabel en corcheas
        n=int(.06*SR);s=rng.standard_normal(n);s=np.diff(np.concatenate([[0],s]))*np.exp(-np.arange(n)/SR*60)*(.05 if k%2 else .09)
        add(s,t+k*beat/2)
    t+=bar
out=out[:N]; out/=np.abs(out).max()/0.85
wavfile.write(sys.argv[1],SR,(np.stack([out,out],1)*32767).astype(np.int16))
