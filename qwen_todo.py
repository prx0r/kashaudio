#!/usr/bin/env python3
"""Qwen perfectionist QA: watch rendered karaoke videos, return up to 10
concrete to-dos with timestamps. STRICT JSON. Usage:
  python3 qwen_todo.py bhairava_01 anuttara_01 [more ids...]
"""
import base64, json, sys, urllib.request
from pathlib import Path

KEY = Path("/tmp/opencode/qwen/key").read_text().strip()
URL = ("https://ws-h6o7g3oq9mc7u24u.ap-southeast-1.maas.aliyuncs.com"
       "/compatible-mode/v1/chat/completions")
MODEL = "qwen3.8-omni-flash"
AUD = Path("/home/ubuntu/kashmir_audio")

def media_part(path: Path):
    b64 = base64.b64encode(path.read_bytes()).decode()
    return {"type": "video_url", "video_url": {"url": f"data:video/mp4;base64,{b64}"}}

BRIEF = """You are the PERFECTIONIST QA for Sanskrit karaoke chant videos.
Each video: white slide, ONE pada (verse-line) per page, Devanagari syllables with romanization ruby below, English translation at bottom. The currently-SUNG syllable lights dark; upcoming stays pale gray. Hard page cut 0.28s before a new page's first voice beat.

WATCH CAREFULLY for exactly these classes:
1. KARAOKE SYNC: a syllable lights noticeably before or after you HEAR it (>=200ms off counts; sub-100ms is fine, do NOT report it).
2. PAGE TRANSITION: a cut feels jarring, or page switches on the beat instead of before it, or old page still visible when new voice starts.
3. LAYOUT: text touching/leaving frame edges, collisions between Sanskrit and English, inconsistent sizing between pages, spacing that looks broken.
4. Any other VISIBLE or AUDIBLE defect a picky owner would catch.

Rules: ONLY defects you can actually observe in THESE videos (no speculation from audio alone). Max 10, worst first. If something is clean, do not invent issues.

Return STRICT JSON ONLY (no fences, no prose):
{"pass": true/false, "score": 1-5,
 "todos": [{"video": "<id>", "t": <seconds>, "severity": "high|med|low", "defect": "<terse>", "fix": "<concrete suggested fix>"}]}"""

def qwen(parts, timeout=420):
    body = json.dumps({"model": MODEL, "modalities": ["text"],
                       "messages": [{"role": "user", "content": parts}]}).encode()
    req = urllib.request.Request(URL, data=body,
                                 headers={"Authorization": f"Bearer {KEY}",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.load(r)
    return ((data.get("choices") or [{}])[0].get("message", {}).get("content")) or ""

def main():
    ids = sys.argv[1:] or ["bhairava_01", "anuttara_01", "bhairava_05"]
    parts = []
    names = []
    for i in ids:
        p = AUD / "cards" / f"{i}.mp4"
        parts.append(media_part(p)); names.append(i)
    parts.append({"type": "text", "text": BRIEF + f"\n\nVIDEOS (in order): {names}"})
    txt = qwen(parts)
    t = txt.strip()
    if t.startswith("```"):
        t = t.split("```")[1]
        t = t[4:] if t.startswith("json") else t
    i, j = t.find("{"), t.rfind("}")
    verdict = json.loads(t[i:j + 1])
    print(json.dumps(verdict, indent=1, ensure_ascii=False))

main()
