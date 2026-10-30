#!/usr/bin/env python3
"""Segment the traditional Anuttarashtika recitation into 8 per-verse chant
blocks (thr=0.025 1s-RMS, merge gaps <25s), extract 24k wavs + 16k f32,
keep pada word structure for the card pipeline.
Usage: python3 segment_trad.py
"""
import json, os, subprocess
import numpy as np
import soundfile as sf

AUD = "/home/ubuntu/kashmir_audio"
SRC = f"{AUD}/ref/anuttarashtika-trad.mp3"
WORK = f"{AUD}/anuttarashtika_trad"

def loud_regions(y, sr, thr=0.025, merge=25.0, mins=8.0):
    dur = len(y) / sr
    win = int(1.0 * sr)
    rms = np.sqrt(np.convolve(y ** 2, np.ones(win) / win, mode="same"))
    loud = rms > thr
    out, s = [], None
    for i, v in enumerate(loud):
        if v and s is None:
            s = i
        if not v and s is not None:
            if (i - s) / sr >= mins:
                out.append((s / sr, i / sr))
            s = None
    if s is not None and (len(y) - s) / sr >= mins:
        out.append((s / sr, dur))
    m = []
    for a, b in out:
        if m and a - m[-1][1] < merge:
            m[-1] = (m[-1][0], b)
        else:
            m.append((a, b))
    return m

def main():
    p22 = "/tmp/anu_trad_22k.wav"
    y, sr = sf.read(p22)
    if y.ndim > 1:
        y = y.mean(axis=1)
    dur = len(y) / sr
    regions = loud_regions(y, sr)
    print(f"duration {dur:.1f}s, {len(regions)} chant regions")
    for i, (a, b) in enumerate(regions):
        print(f"  r{i}: {a:.1f}-{b:.1f} ({b-a:.1f}s)")

    shard = json.load(open("/home/ubuntu/stotras/anuttarashtika.json", encoding="utf-8"))
    shard.sort(key=lambda c: c["id"])
    if len(regions) != len(shard):
        print(f"ERROR: {len(regions)} regions vs {len(shard)} verses")
        return

    os.makedirs(WORK, exist_ok=True)
    verses = []
    for c, (a, b) in zip(shard, regions):
        lead, tail = 0.3, 1.0
        a0, b0 = max(0.0, a - lead), min(dur, b + tail)
        out = f"{WORK}/{c['id']}.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", SRC,
                        "-ss", f"{a0:.3f}", "-to", f"{b0:.3f}",
                        "-ar", "24000", "-ac", "1", out], check=True)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", out,
                        "-ar", "16000", "-ac", "1", "-f", "f32le",
                        f"/tmp/{c['id']}_trad.f32"], check=True)
        padas_words = [[w for w in p.split() if not set(w) <= set("।॥")]
                       for p in c["padas"]]
        words = [w for pw in padas_words for w in pw]
        pada_of = [pi for pi, pw in enumerate(padas_words) for _ in pw]
        verses.append({"id": c["id"], "meter": c.get("meter", ""),
                       "words": words, "pada_of": pada_of,
                       "src": [round(a0, 3), round(b0, 3)]})
        d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "default=noprint_wrappers=1:nokey=1", out],
                           capture_output=True, text=True).stdout.strip()
        print(f"  {c['id']}: src {a0:.1f}-{b0:.1f} -> wav {float(d):.1f}s, {len(words)} words")
    json.dump(verses, open(f"{WORK}/verses.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", f"{WORK}/verses.json")

main()
