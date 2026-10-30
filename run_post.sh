#!/usr/bin/env bash
# End-to-end post-render chain for the three new works (run AFTER v9 completes
# and wavs are pulled into kashmir_audio/<work>/).
set -e
cd /home/ubuntu
WORKS="bodhapanadasika dehastha stavacintamani"
echo "== 1. seed word timings (from shards + real wav durations) =="
python3 kashmir_audio/seed_word_timings.py $WORKS
echo "== 2. syllable texts + guru/laghu weights (matra placeholder) =="
python3 kashmir_audio/regen_syls.py $WORKS
echo "== 3. SYLLABLE-level MMS exact timing =="
node mms-align/align_sylls.js $WORKS
echo "== 4. integrity scan (non-Devanagari / overlaps) =="
python3 - <<'PY'
import json, re
bad = mono = 0
for sub in ["bodhapanadasika","dehastha","stavacintamani"]:
    for c in json.load(open(f"/home/ubuntu/kashmir_audio/{sub}/word_timings.json")):
        prev = 0
        for s in c["syls"]:
            if not re.fullmatch(r"[ऀ-ॿ\s]+", s["d"]): bad += 1; print("BADCHAR", sub, c["id"], s["d"])
            if s["t_on"] < prev - 1e-9: mono += 1
            if s["t_off"] <= s["t_on"]: print("BAD DUR", sub, c["id"], s)
            prev = s["t_off"]
print(f"scan: badchars={bad} nonmono={mono}")
PY
echo "== 5. storyboards (3, bounds-checked; review before any render) =="
python3 kashmir_audio/make_card.py bpc_01 bodhapanadasika --storyboard
python3 kashmir_audio/make_card.py dhs_01 dehastha --storyboard
python3 kashmir_audio/make_card.py stc_001 stavacintamani --storyboard
echo "POST CHAIN DONE — review storyboards next"
