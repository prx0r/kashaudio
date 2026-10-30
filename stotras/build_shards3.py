#!/usr/bin/env python3
"""Build shards for Stavacintāmaṇi (120), Dehastha (16), Bodhapañcadaśikā (15).
Sources: stotras/src/{stavacintamani.htm, dehastha.itx, bodha.htm}
Writes stotras/{stavacintamani,dehastha,bodhapanadasika}.json then runs the
CPU meter check per verse (check_text logic inline) and reports meter table.
Unknown metres get 'gadya' bank ref (like bhairava phala).
Usage: python3 build_shards3.py
"""
import json, re, html as htmlmod, sys
from pathlib import Path
from indic_transliteration import sanscript

SRC = Path("/home/ubuntu/stotras/src")
OUT = Path("/home/ubuntu/stotras")
sys.path.insert(0, "/home/ubuntu/vagdhenu/src")
from render_core import detect_meter_key

def to_deva_iast(s):
    return sanscript.transliterate(s, sanscript.IAST, sanscript.DEVANAGARI)

def to_deva_itrans(s):
    return sanscript.transliterate(s, sanscript.ITRANS, sanscript.DEVANAGARI)

def strip_paren(s):
    return re.sub(r"\([^)]*\)", "", s)

def make_clip(cid, l1, l2, meter):
    def clean(s):
        s = s.strip()
        s = s.lstrip("|/").rstrip("|/")
        s = s.replace("//", "").strip().rstrip("|").strip()
        return s
    l1 = clean(l1) + " ।"
    l2 = clean(l2)
    if not l2.endswith("॥"):
        l2 = l2 + " ॥"
    return {"id": cid, "meter": meter, "padas": [l1, l2],
            "seed": 60, "no_sandhi": False, "out": f"out/{cid}.wav"}

def report(name, clips):
    from collections import Counter
    cnt = Counter()
    fixed = []
    for c in clips:
        det = detect_meter_key(" ".join(c["padas"]))
        cnt[det or "unknown"] += 1
        if not det:
            c["meter"] = "gadya"
        elif det != c["meter"]:
            c["meter"] = det
        fixed.append(c)
    print(f"[{name}] {len(clips)} verses, meters: {dict(cnt)}")
    return fixed

# ── Stavacintāmaṇi (GRETIL html, IAST; verses inside <p id="BhStc_N">...</p>) ──
def parse_stc():
    h = (SRC / "stavacintamani.htm").read_text(encoding="utf-8")
    seen = {}
    for m in re.finditer(r'<p id="BhStc_(\d+)">(.*?)</p>', h, re.S):
        n = int(m.group(1))
        if n in seen:
            continue
        inner = re.sub(r"<span[^>]*>.*?</span>", "", m.group(2), flags=re.S)
        inner = inner.replace("<br />", "\n").replace("<br>", "\n")
        inner = htmlmod.unescape(re.sub("<[^>]+>", "", inner))
        lines = [ln.strip() for ln in inner.splitlines() if len(ln.strip()) > 15]
        if len(lines) < 2:
            print(f"  WARN stc_{n}: {len(lines)} lines: {lines[:3]}")
            continue
        seen[n] = (lines[0], lines[1])
    clips = []
    for n in sorted(seen):
        if not (1 <= n <= 120):
            continue
        l1, l2 = seen[n]
        clips.append(make_clip(f"stc_{n:03d}", to_deva_iast(l1), to_deva_iast(l2), "anushtubh"))
    return clips

# ── Dehastha (itx, ITRANS) ──
def parse_dhs():
    raw = (SRC / "dehastha.itx").read_text(encoding="utf-8")
    body = raw.split("\\begin{document}")[1]
    body = body.split("iti shrI")[0]
    body = strip_paren(body)
    body = re.sub(r"\\\\engtitle.*?##|\\\\itxtitle.*?##|\\\\endtitles ##", "", body, flags=re.S)
    verses = re.split(r"\|\|\s*\d+\s*\|\|", body)
    clips = []
    n = 0
    for v in verses:
        v = v.strip()
        if not v:
            continue
        v = re.sub(r"\s*%.*", "", v)
        lines = [ln.strip() for ln in v.splitlines() if ln.strip() and not ln.strip().startswith("\\")]
        if len(lines) < 2:
            # single blob: split at first |
            if "|" in v:
                a, b = v.split("|", 1)
                lines = [a.strip(), b.strip()]
            else:
                print("  WARN dhs skip:", v[:60])
                continue
        n += 1
        l1 = lines[0].rstrip("|").strip()
        l2 = lines[1].rstrip("|").strip()
        clips.append(make_clip(f"dhs_{n:02d}", to_deva_itrans(l1), to_deva_itrans(l2), "anushtubh"))
    return clips

# ── Bodhapañcadaśikā (GRETIL html, IAST) ──
def parse_bpc():
    h = (SRC / "bodha.htm").read_text(encoding="utf-8")
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", h, flags=re.S)
    t = re.sub("<[^>]+>", "\n", t)
    t = htmlmod.unescape(t)
    # verses: two lines then || N ||
    pat = re.compile(r"([^\n|]+?)\s*\|\s*\n\s*([^\n]+?)\s*\|\|\s*(\d+)\s*\|\|", re.S)
    clips = []
    for m in pat.finditer(t):
        n = int(m.group(3))
        if not (1 <= n <= 15):
            continue
        l1, l2 = m.group(1).strip(), m.group(2).strip()
        clips.append(make_clip(f"bpc_{n:02d}", to_deva_iast(l1), to_deva_iast(l2), "anushtubh"))
    return clips

def main():
    jobs = [("stavacintamani", parse_stc), ("dehastha", parse_dhs),
            ("bodhapanadasika", parse_bpc)]
    for name, fn in jobs:
        clips = fn()
        clips = report(name, clips)
        json.dump(clips, open(OUT / f"{name}.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        # sample sanity
        if clips:
            c = clips[0]
            print(f"  first: {c['id']} meter={c['meter']}")
            print(f"    {c['padas'][0][:70]}")
            print(f"    {c['padas'][1][:70]}")

main()
