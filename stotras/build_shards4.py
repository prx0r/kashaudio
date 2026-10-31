#!/usr/bin/env python3
"""Build shards for the next queue: Rahasya 15, Dvadashika 12+phala,
Mahopadesha 20, Anubhavanivedana 4, Pancashloki 5, Kramastotra 30,
Sivastotravali Stotra-1 rest (25). Sources: Vol-8 PDF OCR (rahasya,
dvadashika, pancashloki), sanskritdocuments itx (mahopadesha, anubhava),
GRETIL TEI (kramastotra), local full.json (stotra1 rest).
Writes stotras/*.json then CPU meter check per verse; unknown -> gadya.
Usage: python3 build_shards4.py
"""
import json, re, sys, html as htmlmod
import xml.etree.ElementTree as ET
from pathlib import Path

SRC = Path("/home/ubuntu/kashmir_audio/stotras/src")
OUT = Path("/home/ubuntu/kashmir_audio/stotras")
sys.path.insert(0, "/home/ubuntu/vagdhenu/src")
from render_core import detect_meter_key
try:
    from indic_transliteration import sanscript
    def to_deva_iast(s):
        return sanscript.transliterate(s, sanscript.IAST, sanscript.DEVANAGARI)
    def to_deva_itrans(s):
        return sanscript.transliterate(s, sanscript.ITRANS, sanscript.DEVANAGARI)
except ImportError:
    to_deva_iast = None
    to_deva_itrans = None

def norm_line(s):
    # OCR writes visarga as ASCII : or ; — restore ः (never legit ASCII here)
    s = s.replace(" :", "ः").replace(" ;", "ः").replace(":", "ः").replace(";", "ः")
    s = s.replace("हदयगगनोदभासि", "हृदयगगनोद्भासि")
    return s

def make_clip(cid, l1, l2, meter, seed=60):
    def clean(s):
        s = norm_line(s)
        s = re.sub(r'[।॥|/\s\d०-९!‰¡."\'॰]+$', '', s.strip()).strip()
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
        if not det:
            c["meter"] = "gadya"
        elif det != c["meter"]:
            c["meter"] = det
    print(f"[{name}] {len(clips)} verses, meters: {dict(cnt)}")
    return clips

# ── OCR helper: keep Devanagari verse lines, drop English/translit garbage ──
def ocr_verses(paths):
    lines = []
    for p in paths:
        for ln in (SRC / p).read_text(encoding="utf-8").splitlines():
            s = ln.strip()
            deva = len(re.findall(r'[\u0900-\u097F]', s))
            if deva < 10 or re.search(r'[A-Za-z€{}$\[\]()A-Za-z]', s):
                continue
            if len(re.findall(r'\d', s)) > 4:
                continue  # OCR garbage rows carry many digits; verse nos are 1-2
            if len(re.findall(r'\d+', s)) >= 2:
                continue  # verse lines carry at most one digit group (their number)
            if "सम्पूर्ण" in s:
                continue  # closer line, never chanted
            lines.append(s)
    # group into verses at trailing number markers (। N। / | N |); order = rank
    verses, cur = [], []
    for s in lines:
        cur.append(s)
        if re.search(r'[।|]\s*[०-९0-9]+\s*[।|][।|\s]*$', s):
            verses.append(cur)
            cur = []
    if cur:
        verses.append(cur)
    # drop trailing closer ("iti ...") block: short, marker-less, contains इति
    if verses and len(verses[-1]) <= 2 and any("इति" in s for s in verses[-1]) \
            and not re.search(r'[।|]\s*[०-९0-9‰]+\s*[।|]', " ".join(verses[-1])):
        verses.pop()
    return verses

def split_at(verses, marker):
    """Split any over-long block at the verse starting with marker."""
    out = []
    for v in verses:
        idx = next((k for k, s in enumerate(v) if s.startswith(marker)), None)
        if idx is not None and idx > 0:
            out += [v[:idx], v[idx:]]
        else:
            out.append(v)
    return out

def verses_to_clips(verses, prefix, seed=60, note=""):
    clips = []
    for i, v in enumerate(verses, 1):
        if len(v) == 2:
            l1, l2 = v
        elif len(v) == 4:
            l1, l2 = v[0] + " " + v[1], v[2] + " " + v[3]
        elif len(v) == 1:
            l1, l2 = v[0], v[0]
        else:
            sys.exit(f"FATAL {prefix} block {i} has {len(v)} lines (garbage?): {v}")
        clips.append(make_clip(f"{prefix}_{i:02d}", l1, l2, "", seed))
    return clips

RAH_FIX = {
    "ततोऽन्यसत्र": "ततोऽन्यत्र",
    "कल्पवुमा :": "कल्पवृक्षाः",
    "कल्पवुमाः": "कल्पवृक्षाः",
    "तस परस्यै": "तस्यै परस्यै",
    "शिवेशिवस्य": "शिवे शिवस्य",
    "त्वमेवदेवता": "त्वमेव देवता",
    "मासमेदो": "मांसमेदो",
    "दुमेऽभिनवगुप्तेन": "मयाऽभिनवगुप्तेन",
    "कराक्षि:": "कराक्षैः",
    "कराक्षि :": "कराक्षैः",
    "भगवत्म्रपत्ति:": "भगवत्प्रपत्तिः",
    "भगवत्म्रपत्ति :": "भगवत्प्रपत्तिः",
    "शृड्वल": "शृङ्खल",
}
def apply_fixes(s, fixes):
    for a, b in fixes.items():
        s = s.replace(a, b)
    return s

def parse_rahasya():
    verses = ocr_verses([f"ocr/u-{p}.txt" for p in (234, 235, 236, 237, 238)])
    print(f"  rahasya OCR verse blocks: {len(verses)} (expect 16: 15 + colophon)")
    verses = [[apply_fixes(s, RAH_FIX) for s in v] for v in verses]
    return verses_to_clips(verses, "rhs")

DVD_FIX = {
    "स्तत्संहारक्रमे": "तत्संहारक्रमे",
    "जडाद्िशेष": "जडाद्विशेष",
    "वजञ्चनेयम्": "वञ्चनेयम्",
    "प्रोदयदिभम": "प्रोदयद्भ्रम",
    "स्वतच्र": "स्वतन्त्र",
    "परतच्रतामुपगतो": "परतन्त्रतामुपगतो",
    "मथ्यनातु": "मथ्नातु",
    "मनमथः": "मन्मथः",
    "निडनि": "निगिरामि",
    "भोंऽहं": "भोऽहं",
    "परवबोधधाम": "परमबोधधाम",
    "त्ुटयद्विभमनित्यतुप्िमहिमा": "त्रुट्यद्विभ्रमनित्यतृप्तमहिमा",
}
def parse_dvadashika():
    verses = ocr_verses([f"ocr/y-{p}.txt" for p in (208, 209, 210, 211, 212)])
    verses = split_at(verses, "कः कोऽत्र भोऽहं कवलीकरोमि")  # v11/v12 merged (no marker)
    print(f"  dvadashika OCR verse blocks: {len(verses)} (expect 13: 12 + phala)")
    verses = [[apply_fixes(s, DVD_FIX) for s in v] for v in verses]
    return verses_to_clips(verses, "dvd")

def parse_pancasloki():
    verses = ocr_verses(["ocr/y-206.txt", "ocr/y-207.txt"])
    # y-206 opens with Dehastha v16 + colophon: find the Pancashloki start
    start = next(i for i, v in enumerate(verses)
                 if any("यत्सत्यं तु मया कृतं" in s for s in v))
    verses = verses[start:start + 5]
    verses = split_at(verses, "यातस्त्वत्सहवासतो")  # v4/v5 merged (‰ misread)
    print(f"  pancashloki OCR verse blocks used: {len(verses)} (expect 5)")
    return verses_to_clips(verses, "psl")

# ── itx (ITRANS, sanskritdocuments) ──
def parse_itx(fname, prefix, seed=60):
    raw = (SRC / fname).read_text(encoding="utf-8")
    body = raw.split("\\begin{document}")[1].split("\\end{document}")[0]
    body = re.sub(r"%.*", "", body)
    body = re.sub(r"\\[a-zA-Z]+(\[.*?\])?(\{.*?\})?", "", body)
    body = body.replace("##", "")
    # colophon line starting with || iti ... || kept as trailing block
    assert to_deva_itrans, "indic_transliteration needed for itx"
    chunks = re.split(r'\|\|\s*(\d+)\s*\|\|', body)
    clips, pending = [], []
    nums = []
    for k, ch in enumerate(chunks):
        if k % 2 == 1:
            nums.append(int(ch))
            continue
        lines = [ln.strip() for ln in ch.splitlines()
                 if ln.strip() and not ln.strip().startswith("(")]
        lines = [re.sub(r"\(.*?\)", "", ln).strip() for ln in lines]
        lines = [ln for ln in lines if ln]
        lines = [to_deva_itrans(ln) for ln in lines]
        if lines:
            pending.append(lines)
    # pair pending blocks with numbers: pending[i] belongs to nums[i]
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
        clips.append(make_clip(f"{prefix}_{n:02d}", l1, l2, "", seed))
    print(f"  {prefix}: {len(clips)} verses from {fname}")
    return clips

# ── Kramastotra (GRETIL TEI, IAST) ──
def parse_kramastotra():
    assert to_deva_iast, "indic_transliteration needed"
    r = ET.parse(SRC / "sa_abhinavagupta-kramastotra.xml").getroot()
    ns = "{http://www.tei-c.org/ns/1.0}"
    body = r.find(f".//{ns}body")
    L = ["".join(e.itertext()).strip()
         for e in body.iter() if e.tag == f"{ns}l"]
    L = [re.sub(r"[$%@]", "", s).strip() for s in L]
    L = [s for s in L if s]
    # GRETIL typo: kra_23 "mārta.ṅdasya" for mārtāṇḍasya (sun); "." never legit
    L = [s.replace("mārta.ṅdasya", "mārtāṇḍasya").replace(".", "") for s in L]
    assert len(L) % 2 == 0, f"odd L count {len(L)}"
    clips = []
    for i in range(0, len(L), 2):
        n = i // 2 + 1
        clips.append(make_clip(f"kra_{n:02d}",
                               to_deva_iast(L[i]), to_deva_iast(L[i + 1]), "", 60))
    print(f"  kramastotra: {len(L)} L-lines -> {len(clips)} verses")
    return clips

# ── Stotra 1 rest (local full.json) ──
def parse_stotra1():
    full = json.load(open(OUT / "shivastotravali_full.json", encoding="utf-8"))
    clips = []
    for c in full:
        m = re.fullmatch(r"shivastotravali_1_(\d+)", c["id"])
        if m and int(m.group(1)) >= 2:
            d = dict(c)
            d["seed"] = 34
            clips.append(d)
    clips.sort(key=lambda c: int(c["id"].rsplit("_", 1)[1]))
    print(f"  stotra1 rest: {len(clips)} verses")
    return clips

def main():
    jobs = [  # noqa: keep order stable; each writes stotras/<name>.json

        ("rahasyapanchadashika", parse_rahasya),
        ("paramadvayadvadashika", parse_dvadashika),
        ("mahopadeshavimshatika", lambda: parse_itx("mahopadeshavimshatikam.itx", "mhu")),
        ("anubhavanivedana", lambda: parse_itx("anubhavanivedanam.itx", "anb")),
        ("pancashloki", parse_pancasloki),
        ("kramastotra", parse_kramastotra),
        ("shivastotravali_1", parse_stotra1),
    ]
    for name, fn in jobs:
        clips = fn()
        clips = report(name, clips)
        json.dump(clips, open(OUT / f"{name}.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        if clips:
            print(f"    first: {clips[0]['id']} meter={clips[0]['meter']}")
            print(f"      {clips[0]['padas'][0][:70]}")
        # junk scan: no ASCII/symbol debris may reach cards
        for c in clips:
            for p in c["padas"]:
                if re.search(r'[A-Za-z€{}$\[\]()!‰¡;:,."0-9]', p):
                    print(f"    JUNK? {c['id']}: {p[:80]}")

if __name__ == "__main__":
    main()
