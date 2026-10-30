"""CPU-only stotra validation (no GPU, no torch weights needed).
Checks: shard JSON loads, padas normalize via prep_text, meter detection.
Usage: python3 check_text.py stotra_shard.json
"""
import json, sys
sys.path.insert(0, "/home/ubuntu/vagdhenu/src")
import prep_text as PT
from render_core import detect_meter_key

path = sys.argv[1] if len(sys.argv) > 1 else "/home/ubuntu/stotras/stotra_shard.json"
clips = json.load(open(path, encoding="utf-8"))
print(f"{len(clips)} clips")
for c in clips:
    print(f"\n== {c['id']} (declared meter: {c.get('meter')}) ==")
    full = " ".join(c["padas"])
    try:
        det = detect_meter_key(full)
        print(f"  detected: {det} {'OK' if det == c.get('meter') else '-> will fallback to '+c.get('meter')}")
    except Exception as e:
        print(f"  meter detect FAIL: {e}")
    for i, p in enumerate(c["padas"]):
        try:
            norm = PT.model_text_sandhi(p)
            print(f"  pada{i}: {norm[:80]}")
        except Exception as e:
            print(f"  pada{i} FAIL: {e}")
print("\nCPU text check done. GPU render happens on Kaggle.")
