#!/usr/bin/env python3
"""Transition-early diagnostic: for every page start, compare MMS-claimed
syllable onset vs the measured acoustic onset in the audio. Also join rhythm
for full recitations (prev clip trailing + next lead-in).
Usage: python3 diag_transitions.py
"""
import json
import numpy as np
import soundfile as sf
import librosa

AUD = "/home/ubuntu/kashmir_audio"
STOPS = set("kKgGcCjJtTdDpPbB")  # SLP1 voiceless/voiced stops (page-start suspects)

def onsets(y, sr):
    hop = 128  # fine hop for onset precision (~5ms at 24k)
    o = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop, aggregate=np.median)
    return sorted(float(t) for t in librosa.onset.onset_detect(
        onset_envelope=o, sr=sr, hop_length=hop, units="time", backtrack=True,
        pre_max=3, post_max=3, pre_avg=6, post_avg=6, delta=0.04, wait=4))

def first_phon_class(r):
    # crude: first char of roman -> stop?
    return "STOP" if r[:1].lower() in "kgcjtdpb" else "other"

print("=== PAGE-START: MMS claim vs acoustic onset (delta<0 = light EARLY) ===")
rows = []
for sub in ["bhairavastava", "anuttarashtika"]:
    for c in json.load(open(f"{AUD}/{sub}/word_timings.json")):
        y, sr = sf.read(f"{AUD}/{sub}/{c['id']}.wav")
        if y.ndim > 1:
            y = y.mean(axis=1)
        ons = onsets(y, sr)
        padas = sorted({s["pada"] for s in c["syls"]})
        prev_end = 0.0
        for p in padas:
            ps = [s for s in c["syls"] if s["pada"] == p]
            first = ps[0]
            # search acoustic onset in [prev_end, claim+0.4]
            lo, hi = max(0.0, prev_end - 0.05), first["t_on"] + 0.4
            cand = [t for t in ons if lo <= t <= hi]
            tac = cand[0] if cand else float("nan")
            delta = first["t_on"] - tac if cand else float("nan")
            cls = first_phon_class(first["r"])
            gap = first["t_on"] - prev_end
            rows.append((sub, c["id"], p, first["t_on"], tac, delta, gap, cls, first["r"]))
            prev_end = ps[-1]["t_off"]
for r in rows:
    sub, cid, p, tc, ta, dl, gap, cls, rom = r
    flag = "  <<< EARLY" if dl == dl and dl < -0.12 else ("  << earlyish" if dl == dl and dl < -0.06 else "")
    print(f"{cid:>18} p{p} claim={tc:7.3f} acoustic={'nan' if ta!=ta else format(ta,'7.3f')} "
          f"delta={'na' if dl!=dl else format(dl,'+6.3f')} gap={gap:5.2f} {cls:5s} {rom[:14]:14s}{flag}")

early = [r for r in rows if r[5] == r[5] and r[5] < -0.12]
print(f"\npage starts: {len(rows)}, early(<-120ms): {len(early)}")
from collections import Counter
print("early by phoneme class:", Counter(r[7] for r in early), "| all by class:", Counter(r[7] for r in rows))

print("\n=== FULL-VIDEO JOINS: prev trailing + next lead-in vs in-clip pattern (LEAD 0.28) ===")
for sub in ["bhairavastava", "anuttarashtika"]:
    clips = sorted(json.load(open(f"{AUD}/{sub}/word_timings.json")), key=lambda c: c["id"])
    for i in range(len(clips) - 1):
        a, b = clips[i], clips[i + 1]
        trail = a["dur"] - max(s["t_off"] for s in a["syls"])
        lead = b["syls"][0]["t_on"] if b["syls"][0]["pada"] == 0 else min(s["t_on"] for s in b["syls"])
        # pale time at join in full video = lead (page appears at clip start)
        pale = lead
        flag = "  <<< RUSHED join" if pale < 0.22 else ""
        print(f"{a['id']}->{b['id']}: trail={trail:5.2f} next_pale={pale:5.2f}{flag}")
