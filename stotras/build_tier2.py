#!/usr/bin/env python3
"""Build shards for Tier 2 batch: Anubhavanivedana 4, Bodhavilasa 42,
BhairavAnukaranaStotra 48, Ajadapramatrsiddhi 27.
Sources: sanskritdocuments itx (anubhava), GRETIL TEI (bodhavilasa,
bhairavanukarana, ajadapramatra). Usage: python3 build_tier2.py
"""
import json, re, sys
import xml.etree.ElementTree as ET
from pathlib import Path

SRC = Path("/home/ubuntu/kashmir_audio/stotras/src")
OUT = Path("/home/ubuntu/kashmir_audio/stotras")
GRETL = Path("/tmp/gretil")
sys.path.insert(0, "/home/ubuntu/vagdhenu/src")
from render_core import detect_meter_key
from indic_transliteration import sanscript

def to_deva_iast(s):
    return sanscript.transliterate(s, sanscript.IAST, sanscript.DEVANAGARI)

def to_deva_itrans(s):
    return sanscript.transliterate(s, sanscript.ITRANS, sanscript.DEVANAGARI)

def make_clip(cid, l1, l2, seed=60):
    def clean(s):
        s = s.strip()
        s = re.sub(r'[।॥|/\s\d०-९]+$', '', s).strip()
        s = s.replace(":", "ः").replace(";", "ः")
        return s
    l1 = clean(l1) + " ।"
    l2 = clean(l2)
    if not l2.endswith("॥"):
        l2 = l2 + " ॥"
    return {"id": cid, "meter": "", "padas": [l1, l2],
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

def parse_teI(fname, prefix, seed=60):
    """Parse GRETIL TEI for paired-l works (bodhavilasa, bhairavanukarana)."""
    r = ET.parse(GRETL / fname).getroot()
    ns = "{http://www.tei-c.org/ns/1.0}"
    body = r.find(f".//{ns}body")
    L = ["".join(e.itertext()).strip()
         for e in body.iter() if e.tag == f"{ns}l"]
    L = [re.sub(r"[$%@]", "", s).strip() for s in L]
    L = [s for s in L if s and not s.startswith("[") and not s.startswith("Vṛ")]
    clips = []
    n = 0
    for i in range(0, len(L) - 1, 2):
        n += 1
        l1, l2 = L[i], L[i + 1]
        cid = f"{prefix}_{n:02d}"
        clips.append(make_clip(cid, to_deva_iast(l1), to_deva_iast(l2), seed))
    print(f"  {prefix}: {len(L)} L-lines -> {clips[-1]['id'] if clips else '?'}")
    return clips

def parse_teI_ajs(fname, prefix, seed=60):
    """Parse Ajadapramatrsiddhi TEI: each verse is a [p] line with
    line1 & line2 % structure; [l] line is a redundant second-half
    with UtAjp_N marker. Vṛ: lines are commentary."""
    r = ET.parse(GRETL / fname).getroot()
    ns = "{http://www.tei-c.org/ns/1.0}"
    body = r.find(f".//{ns}body")
    clips = []
    n = 0
    for e in body.iter():
        if e.tag != f"{ns}p":
            continue
        t = "".join(e.itertext()).strip()
        if not t or t.startswith("Vṛ:") or t.startswith("[Pūrvapakṣaḥ:]"):
            continue
        # full verse: line1 & line2 % ...
        m = re.match(r"(.*?)\s*&\s*\n?\s*(.*?)\s*%(.*)$", t, re.S)
        if not m:
            continue
        l1 = re.sub(r"[$%@]", "", m.group(1)).strip()
        l2 = re.sub(r"[$%@]", "", m.group(2)).strip()
        n += 1
        clips.append(make_clip(f"{prefix}_{n:02d}",
                               to_deva_iast(l1), to_deva_iast(l2), seed))
    print(f"  {prefix}: {n} verses from [p] lines")
    # verse 1 fallback: both halves in [l] lines (no [p] counterpart)
    if n < 27:
        L = ["".join(e.itertext()).strip()
             for e in body.iter() if e.tag == f"{ns}l"]
        L = [re.sub(r"[$%@&]", "", s).strip() for s in L]
        L = [s for s in L if s and "UtAjp_01" in s or
             (s and s.startswith("yathā"))]
        # pair first (yathā) + second (jadājaḍānām...UtAjp_01)
        L2 = ["".join(e.itertext()).strip()
              for e in body.iter() if e.tag == f"{ns}l"]
        L2 = [re.sub(r"[$%@&]", "", s).strip() for s in L2]
        L2 = [s for s in L2 if s and not s.startswith("[Pūrvapakṣaḥ:]") and "पूर्वपक्ष" not in s]
        # first [l] line is verse 1 first half, second [l] line is verse 1 second half
        if len(L2) >= 2:
            l1 = to_deva_iast(L2[0])
            l2 = to_deva_iast(re.sub(r"//\s*UtAjp_\d+\s*//", "", L2[1]).strip())
            clips.insert(0, make_clip(f"{prefix}_01", l1, l2, seed))
            # renumber all clips
            for i, c in enumerate(clips, 1):
                c["id"] = f"{prefix}_{i:02d}"
                c["out"] = f"out/{c['id']}.wav"
            n = len(clips)
            print(f"  {prefix}: added verse 1 from [l] fallback, now {n} total")
    return clips

def parse_itx(fname, prefix, seed=60):
    raw = (SRC / fname).read_text(encoding="utf-8")
    body = raw.split("\\begin{document}")[1].split("\\end{document}")[0]
    body = re.sub(r"%.*", "", body)
    body = re.sub(r"\\[a-zA-Z]+(\[.*?\])?(\{.*?\})?", "", body)
    body = body.replace("##", "")
    chunks = re.split(r'\|\|\s*(\d+)\s*\|\|', body)
    clips, nums = [], []
    pending = []
    for k, ch in enumerate(chunks):
        if k % 2 == 1:
            nums.append(int(ch))
            continue
        lines = [ln.strip() for ln in ch.splitlines()
                 if ln.strip() and not ln.strip().startswith("(")]
        lines = [re.sub(r"\(.*?\)", "", ln).strip() for ln in lines]
        lines = [to_deva_itrans(ln) for ln in lines if ln]
        if lines:
            pending.append(lines)
    blocks = pending[:len(nums)]
    for lines, n in zip(blocks, nums):
        if len(lines) == 2:
            l1, l2 = lines
        elif len(lines) >= 4:
            l1, l2 = " ".join(lines[:2]), " ".join(lines[2:4])
        elif len(lines) == 1:
            l1, l2 = lines[0], lines[0]
        else:
            l1, l2 = lines[0], " ".join(lines[1:])
        clips.append(make_clip(f"{prefix}_{n:02d}", l1, l2, seed))
    print(f"  {prefix}: {len(clips)} verses from {fname}")
    return clips

def main():
    jobs = [
        ("anubhavanivedana", lambda: parse_itx("anubhavanivedanam.itx", "anb")),
        ("bodhavilasa", lambda: parse_teI("sa_kSemarAja-bodhavilAsa.xml", "bvl")),
        ("bhairavanukarana", lambda: parse_teI("sa_kSemarAja-bhairavAnukaraNastotra.xml", "bna")),
        ("ajadapramatrsiddhi", lambda: parse_teI_ajs("sa_utpaladeva-ajaDapramAtRsiddhi.xml", "ajs")),
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
