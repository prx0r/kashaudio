#!/usr/bin/env python3
"""Rhythm-correct syllable timing: distribute within each PADA proportional
to syllable weight (guru=2 matras, laghu=1), spanning the MMS word window.
This is how the chant actually moves — matra-proportional, not uniform.
Usage: python3 regen_syls.py
"""
import json, sys
from indic_transliteration import sanscript
sys.path.insert(0, "/home/ubuntu/vagdhenu/src")
from tts_normalize import normalize
from tts_g2p import to_slp1
from tts_syllabify import syllabify
from tts_weight import tag_weights

AUD = "/home/ubuntu/kashmir_audio"

def pada_syllables(pada_text):
    # normalize() emits jihvāmūlīya/upadhmānīya (ᳵᳶ) before k/p; SLP1 maps them
    # to Z/z which the display path renders as literal ASCII — restore plain visarga
    # (matches source Devanagari and fixes the guru-via-visarga weight rule too).
    t = normalize(pada_text).replace("ᳵ", "ः").replace("ᳶ", "ः")
    syls = syllabify(to_slp1(t))
    tag_weights(syls)
    return syls

subs = sys.argv[1:] or ["bhairavastava", "anuttarashtika"]
for sub in subs:
    clips = json.load(open(f"{AUD}/{sub}/word_timings.json", encoding="utf-8"))
    for c in clips:
        by_pada = {}
        for w in c["words"]:
            by_pada.setdefault(w["pada"], []).append(w)
        syls_out = []
        for pi in sorted(by_pada):
            pw = by_pada[pi]
            pada_text = " ".join(w["w"] for w in pw)
            syls = pada_syllables(pada_text)
            # pada span = first word t_on .. last word t_off (MMS-correct)
            span0 = pw[0]["t_on"]
            span1 = pw[-1]["t_off"]
            total_matras = sum(2 if s["weight"] == "G" else 1 for s in syls)
            matra = (span1 - span0) / total_matras if total_matras else 0
            # walk syllables, tracking which word each belongs to
            t = span0
            wi = 0
            for s in syls:
                d = 2 * matra if s["weight"] == "G" else matra
                syls_out.append({
                    "d": str(sanscript.transliterate(s["text"], sanscript.SLP1, sanscript.DEVANAGARI)),
                    "r": str(sanscript.transliterate(s["text"], sanscript.SLP1, sanscript.IAST)),
                    "t_on": round(t, 3), "t_off": round(t + d, 3),
                    "pada": pi, "w": s["weight"], "word": pw[wi]["w"] if wi < len(pw) else pw[-1]["w"]})
                t += d
                # advance word pointer when syllable count within word is exhausted
                # (word boundary: s.is_word_final)
                if s.get("is_word_final"):
                    wi += 1
        c["syls"] = sorted(syls_out, key=lambda s: s["t_on"])
    json.dump(clips, open(f"{AUD}/{sub}/word_timings.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    tot = sum(len(c["syls"]) for c in clips)
    print(sub, "clips:", len(clips), "syls:", tot)
