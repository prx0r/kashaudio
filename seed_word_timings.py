#!/usr/bin/env python3
"""Seed word_timings.json for a NEW work after its wavs exist on disk:
shard -> words (danda-stripped, pada-indexed) with proportional placeholder
spans + real clip durations. Follow with regen_syls then align_sylls.
Usage: python3 seed_word_timings.py <work> [<work>...]
"""
import json, subprocess, sys
from pathlib import Path

ST = Path("/home/ubuntu/stotras")
AUD = Path("/home/ubuntu/kashmir_audio")

def dur_of(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(p)],
        capture_output=True, text=True).stdout.strip())

def main():
    for work in sys.argv[1:]:
        shard = json.load(open(ST / f"{work}.json", encoding="utf-8"))
        out = []
        for c in shard:
            wav = AUD / work / f"{c['id']}.wav"
            if not wav.exists():
                print(f"  MISSING {wav}")
                continue
            dur = dur_of(wav)
            words = []
            for pi, pada in enumerate(c["padas"]):
                toks = [w for w in pada.split() if not set(w) <= set("।॥")]
                for w in toks:
                    words.append({"w": w, "t_on": 0.0, "t_off": 0.0, "pada": pi})
            # proportional placeholder by akshara-ish length across [0.02, dur-0.05]
            spans = [max(len(w["w"]), 2) for w in words]
            total = sum(spans) or 1
            t = 0.02
            usable = dur - 0.10
            for w, s in zip(words, spans):
                d = usable * s / total
                w["t_on"] = round(t, 3)
                w["t_off"] = round(t + d, 3)
                t += d
            out.append({"id": c["id"], "meter": c.get("meter", ""),
                        "dur": round(dur, 3), "words": words})
        (AUD / work).mkdir(exist_ok=True)
        json.dump(out, open(AUD / work / "word_timings.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        n = sum(len(c["words"]) for c in out)
        print(f"{work}: seeded {len(out)} clips, {n} words")

main()
