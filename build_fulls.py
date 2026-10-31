#!/usr/bin/env python3
"""Full recitation builder with JOIN RHYTHM (fixes the every-4th bug).

Intra-clip page cuts: page arrives LEAD (0.28s) before the first beat — perfect.
Inter-clip joins were rushed (new page pale only 0.02-0.14s, some prev-trails
as short as 0.16s). Fix per join, target total gap G=1.05s (intra median) and
pale exactly LEAD:
  A = prev clip's LAST frame held S1 + silence   (old page keeps holding)
  B = next clip's FIRST frame (pale) S2 + silence (pale window to exactly 0.28)
  S1 = max(0, G - trail - LEAD);  S2 = max(0, LEAD - next_first_light)

Usage: python3 build_fulls.py [bhairavastava anuttarashtika]
"""
import json, subprocess, sys
from pathlib import Path

AUD = Path("/home/ubuntu/kashmir_audio")
G, LEAD, FPS = 1.05, 0.28, 30

def ff(*args):
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True)

def dur_of(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(p)],
        capture_output=True, text=True).stdout.strip())

def still_seg(png, secs, out):
    """Silent video: PNG held `secs` at 30fps + silence."""
    if secs <= 0.01:
        return False
    ff("-loop", "1", "-framerate", str(FPS), "-t", f"{secs:.3f}", "-i", str(png),
       "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", f"{secs:.3f}",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "16",
       "-c:a", "aac", "-b:a", "192k", "-shortest", str(out))
    return True

def build(work):
    cards = AUD / "cards"
    clips = sorted(json.load(open(AUD / work / "word_timings.json")), key=lambda c: c["id"])
    files, seginfo = [], []
    tmp = AUD / "cards" / "_join_tmp"; tmp.mkdir(exist_ok=True)
    for i, c in enumerate(clips):
        mp4 = cards / f"{c['id']}.mp4"
        if i > 0:
            prev = clips[i - 1]
            prev_mp4 = cards / f"{prev['id']}.mp4"
            trail = prev["dur"] - max(s["t_off"] for s in prev["syls"])
            nlight = min(s["t_on"] for s in c["syls"])
            s1 = max(0.0, G - trail - LEAD)
            s2 = max(0.0, LEAD - nlight)
            # Robust last-frame grab (2026-10-30 fix): `-sseof -0.05`
            # silently produced EMPTY output on ~72/169 clips (exit 0,
            # no error), leaving a STALE tmp/last.png from the previous
            # join -> A held the WRONG page -> double-cut feel. Fix:
            # unique names per join + seek to dur-0.2 (safely inside the
            # trailing last-page hold) + verify non-empty, fail loudly.
            last_png, first_png = tmp / f"last{i}.png", tmp / f"first{i}.png"
            for p in (last_png, first_png):
                if p.exists():
                    p.unlink()
            prev_dur = dur_of(prev_mp4)
            ff("-ss", f"{max(0.0, prev_dur - 0.2):.3f}", "-i", str(prev_mp4),
               "-frames:v", "1", str(last_png))
            ff("-i", str(mp4), "-frames:v", "1", str(first_png))
            for p in (last_png, first_png):
                if not p.exists() or p.stat().st_size == 0:
                    sys.exit(f"FRAME GRAB FAILED for {p} (prev={prev['id']}) — refusing to build with stale frame")
            a = tmp / f"A{i}.mp4"; b = tmp / f"B{i}.mp4"
            if a.exists(): a.unlink()
            if b.exists(): b.unlink()
            if still_seg(last_png, s1, a):
                files.append(a)
            if still_seg(first_png, s2, b):
                files.append(b)
            gap = trail + s1 + s2 + nlight
            pale = s2 + nlight
            seginfo.append((prev["id"], c["id"], trail, s1, s2, nlight, gap, pale))
        files.append(mp4)
    # concat list + re-encode (uniform params)
    lst = tmp / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in files))
    out = cards / f"{work}_full.mp4"
    ff("-f", "concat", "-safe", "0", "-i", str(lst),
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "16",
       "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "24000", "-ac", "1",
       str(out))
    print(f"\n{work}: joins (gap target {G}s, pale target {LEAD}s):")
    ok = True
    for pi, ni, trail, s1, s2, nlight, gap, pale in seginfo:
        flag = "" if (G - 0.05 <= gap <= G + 0.35 and pale >= LEAD - 0.02) else "  <<< CHECK"
        if flag: ok = False
        print(f"  {ni}: trail={trail:.2f} +A{s1:.2f} +B{s2:.2f} +lead{nlight:.2f}"
              f" -> gap={gap:.2f} pale={pale:.2f}{flag}")
    print("  ->", out, f"({dur_of(out):.1f}s)", "PATTERN OK" if ok else "PATTERN OFF")

def main():
    for work in (sys.argv[1:] or ["bhairavastava", "anuttarashtika"]):
        build(work)

main()
