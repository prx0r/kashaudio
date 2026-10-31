#!/usr/bin/env python3
"""Batch-translate new verses to English via qwen (card right column).
Usage: python3 translate_batch.py [batch_size]
Writes merged kashmir_audio/translations.json (keeps existing entries).
"""
import json, sys, time, urllib.request
from pathlib import Path

KEY = Path("/tmp/opencode/qwen/key").read_text().strip()
URL = ("https://ws-h6o7g3oq9mc7u24u.ap-southeast-1.maas.aliyuncs.com"
       "/compatible-mode/v1/chat/completions")
MODEL = "qwen3.8-omni-flash"
ST = Path("/home/ubuntu/stotras")
TR = Path("/home/ubuntu/kashmir_audio/translations.json")

def qwen(text, timeout=300):
    body = json.dumps({"model": MODEL, "modalities": ["text"],
                       "messages": [{"role": "user", "content": text}]}).encode()
    req = urllib.request.Request(URL, data=body,
                                 headers={"Authorization": f"Bearer {KEY}",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.load(r)
    return ((data.get("choices") or [{}])[0].get("message", {}).get("content")) or ""

def parse(txt):
    t = txt.strip()
    if t.startswith("```"):
        t = t.split("```")[1]
        t = t[4:] if t.startswith("json") else t
    i, j = t.find("{"), t.rfind("}")
    return json.loads(t[i:j + 1])

def main():
    bs = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    works = sys.argv[2:] or ["bodhapanadasika", "dehastha", "stavacintamani"]
    existing = json.load(open(TR, encoding="utf-8"))
    todo = []
    for name in works:
        for c in json.load(open(ST / f"{name}.json", encoding="utf-8")):
            if c["id"] not in existing:
                todo.append(c)
    print(f"{len(todo)} verses to translate")
    done = 0
    for i in range(0, len(todo), bs):
        batch = todo[i:i + bs]
        lines = "\n".join(f'{c["id"]} :: {" ".join(c["padas"])}' for c in batch)
        prompt = ("Translate these Sanskrit verses (Kashmir Shaiva tradition) to ENGLISH.\n"
                  "One concise prose line per verse, max 40 words, faithful, readable as an "
                  "on-screen subtitle under the original. No notes, no verse numbers.\n"
                  'Return STRICT JSON ONLY: {"id": "...", ...} with ALL ids from the input.\n\n' + lines)
        for attempt in range(3):
            try:
                out = parse(qwen(prompt))
                missing = [c["id"] for c in batch if c["id"] not in out]
                if missing:
                    raise ValueError(f"missing {missing}")
                existing.update({k: str(v) for k, v in out.items()})
                done += len(batch)
                json.dump(existing, open(TR, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                print(f"  {done}/{len(todo)} ok (last: {list(out)[0]})", flush=True)
                time.sleep(0.5)
                break
            except Exception as e:
                print(f"  batch {i} attempt {attempt+1} failed: {e}")
                time.sleep(10)
        else:
            print(f"FATAL batch at {i}, saving partial")
            break
    json.dump(existing, open(TR, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # verify
    need = {c["id"] for name in works
            for c in json.load(open(ST / f"{name}.json", encoding="utf-8"))}
    have = set(existing)
    print(f"done. coverage: {len(need & have)}/{len(need)}; total translations {len(existing)}")

main()
