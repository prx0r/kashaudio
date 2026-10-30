#!/usr/bin/env python3
"""One-shot qwen-omni review: karaoke sync (esp. hrdi/vande tail) + centered layout taste."""
import base64, json, subprocess, sys, urllib.request
from pathlib import Path

KEY = Path("/tmp/opencode/qwen/key").read_text().strip()
URL = ("https://ws-h6o7g3oq9mc7u24u.ap-southeast-1.maas.aliyuncs.com"
       "/compatible-mode/v1/chat/completions")
MODEL = "qwen3.8-omni-flash"
AUD = Path("/home/ubuntu/kashmir_audio")
ID = sys.argv[1] if len(sys.argv) > 1 else "bhairava_01"

def media_part(path: Path):
    ext = path.suffix.lower().lstrip(".")
    mime = {"mp4": "video/mp4", "png": "image/png"}[ext]
    b64 = base64.b64encode(path.read_bytes()).decode()
    if ext == "mp4":
        return {"type": "video_url", "video_url": {"url": f"data:{mime};base64,{b64}"}}
    return {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}}

# stills at the disputed tail + mid
stills = []
for tag, t in [("hrdi", 11.6), ("vande", 12.15)]:
    p = AUD / "cards" / f"{ID}_{tag}.png"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i",
                    str(AUD / "cards" / f"{ID}.mp4"), "-frames:v", "1", str(p)], check=True)
    stills.append(p)

BRIEF = """You are reviewing a Sanskrit chant karaoke card. The video (12.37s, with audio) shows ONE pada per slide: centered Devanagari verse, IAST romanization below it, English translation full-width at the bottom. The currently-sung word lights in dark ink exactly at its onset; upcoming words stay pale gray.

AUDIO-LYRICS MAP (verse 2, the slide from 6.2s): bhairavanatham-anathasharanyam (6.24s) / tvanmayacittataya (9.27s) / hrdi (11.56s) / vande (12.08s, clip ends 12.37s).

TASKS:
1. SYNC: listen carefully to the LAST TWO WORDS (hrdi ~11.6s, vande ~12.1s). Is each word's highlight early, late, or correct relative to when it is SUNG? Estimate the error in ms and give corrected t_on values. Also flag any other word you hear as off.
2. LAYOUT: does this match Essay-0 centered-couplet taste (white ground, centered Devanagari, IAST below, full-width English bottom, no rules/dots/decoration)? One-line taste verdict.

Return STRICT JSON ONLY:
{"pass": true/false, "score": 1-5,
 "sync": [{"word": "hrdi", "verdict": "early|late|ok", "off_ms": 0, "corrected_t_on": 0.0}, ...],
 "layout": "one line",
 "defects": ["worst first"]}"""

mp4 = AUD / "cards" / f"{ID}.mp4"
parts = [media_part(mp4)] + [media_part(p) for p in stills]
parts.append({"type": "text", "text": BRIEF})
body = json.dumps({"model": MODEL, "modalities": ["text"],
                   "messages": [{"role": "user", "content": parts}]}).encode()
req = urllib.request.Request(URL, data=body,
                             headers={"Authorization": f"Bearer {KEY}",
                                      "Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=300) as r:
    data = json.load(r)
txt = ((data.get("choices") or [{}])[0].get("message", {}).get("content")) or ""
print(txt)
