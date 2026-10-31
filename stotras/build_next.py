#!/usr/bin/env python3
"""Build shards for next batch: Pratyabhijnahrdaya 20 sutras + Paryantapancasika 52.
Sources: GRETIL TEI. Hrdajam = prose sutras (gadya format flag).
Usage: python3 build_next.py
"""
import json, re, sys
import xml.etree.ElementTree as ET
from pathlib import Path

GRETL = Path("/tmp/gretil")
OUT = Path("/home/ubuntu/kashmir_audio/stotras")
sys.path.insert(0, "/home/ubuntu/vagdhenu/src")
from render_core import detect_meter_key
from indic_transliteration import sanscript

def to_deva_iast(s):
    return sanscript.transliterate(s, sanscript.IAST, sanscript.DEVANAGARI)

def make_clip(cid, l1, l2, meter="", seed=60):
    def clean(s):
        s = s.strip()
        s = re.sub(r'[।॥|/\s\d०-९]+$', '', s).strip()
        return s
    l1 = clean(l1) + " ।"
    l2 = clean(l2)
    if not l2.endswith("॥"):
        l2 = l2 + " ॥"
    return {"id": cid, "meter": meter, "padas": [l1, l2],
            "seed": seed, "no_sandhi": False, "out": f"out/{cid}.wav"}

def report(name, clips):
    from collections import Counter
    cnt = Counter()
    for c in clips:
        det = detect_meter_key(" ".join(c["padas"]))
        cnt[det or "unknown"] += 1
        c["meter"] = det or "gadya"
    print(f"[{name}] {len(clips)} verses, meters: {dict(cnt)}")
    return clips

def parse_hrdayam():
    """20 sutras: prose, each is one pad (too short for 2-pad split)."""
    r = ET.parse(GRETL / "sa_kSemarAja-pratyabhijJAhRdaya.xml").getroot()
    ns = "{http://www.tei-c.org/ns/1.0}"
    L = [''.join(e.itertext()).strip()
         for e in r.find(f".//{ns}body").iter() if e.tag == f"{ns}l"]
    L = [re.sub(r'\[\d+\]', '', s).strip() for s in L]
    L = [s for s in L if s]
    clips = []
    for s in L:
        m = re.search(r'\|\|\s*(\d+)\s*\|\|\s*$', s)
        if not m:
            continue
        n = int(m.group(1))
        text = re.sub(r'\|\|\s*\d+\s*\|\|\s*$', '', s).strip()
        if not text:
            continue
        # short sutra: both pads = same text (one-pad verse)
        cid = f"hrd_{n:02d}"
        deva = to_deva_iast(text)
        clips.append(make_clip(cid, deva, deva, "gadya"))
    print(f"  hrd: {len(clips)} sutras extracted")
    return clips

def parse_paryanta():
    """52 verses: 2-line anustubh, || N || markers."""
    r = ET.parse(GRETL / "sa_abhinavagupta-paryantapaJcAzikA.xml").getroot()
    ns = "{http://www.tei-c.org/ns/1.0}"
    L = [''.join(e.itertext()).strip()
         for e in r.find(f".//{ns}body").iter() if e.tag == f"{ns}l"]
    L = [re.sub(r'[$%@]', '', s).strip() for s in L]
    L = [s for s in L if s]
    # pair into 2-line verses
    clips = []
    n = 0
    for i in range(0, len(L) - 1, 2):
        n += 1
        l1 = re.sub(r'\|\|\s*\d+\s*\|\|\s*$', '', L[i]).strip()
        l2 = re.sub(r'\|\|\s*\d+\s*\|\|\s*$', '', L[i + 1]).strip()
        if not l1 or not l2:
            continue
        cid = f"prc_{n:02d}"
        clips.append(make_clip(cid, to_deva_iast(l1), to_deva_iast(l2)))
    print(f"  prc: {len(L)} L-lines -> {clips[-1]['id'] if clips else '?'}")
    return clips

def main():
    jobs = [
        ("pratyabhijnahrdaya", parse_hrdayam),
        ("paryantapancasika", parse_paryanta),
    ]
    for name, fn in jobs:
        clips = fn()
        clips = report(name, clips)
        json.dump(clips, open(OUT / f"{name}.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        if clips:
            print(f"    first: {clips[0]['id']} meter={clips[0]['meter']}")
            print(f"      {clips[0]['padas'][0][:70]}")

if __name__ == "__main__":
    main()
