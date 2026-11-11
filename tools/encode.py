import json, os, subprocess, sys

name = sys.argv[1]
W, H = os.environ.get("OUT_W","1080"), os.environ.get("OUT_H","1920")
d = f"/home/claude/reels/frames_{name}"
meta = json.load(open(f"{d}/frames.json"))
frames, marks = meta["frames"], meta["marks"]
start = marks.get("start", frames[0][1])
end = marks["end"]
frames = [f for f in frames if f[1] >= start - 0.05] or meta["frames"][-1:]
lines = ["ffconcat version 1.0"]
for i, (fn, ts) in enumerate(frames):
    nxt = frames[i + 1][1] if i + 1 < len(frames) else end
    dur = max(0.001, nxt - ts)
    lines += [f"file '{os.path.basename(fn)}'", f"duration {dur:.4f}"]
lines.append(f"file '{os.path.basename(frames[-1][0])}'")
open(f"{d}/list.txt", "w").write("\n".join(lines))
out = f"/home/claude/reels/momelinv_reel_{name}.mp4"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{d}/list.txt",
                "-vf", f"scale={W}:{H}:flags=lanczos,fps=30,format=yuv420p",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-movflags", "+faststart", out], check=True)
print(out, f"{end - start:.1f}s", len(frames), "frames")
