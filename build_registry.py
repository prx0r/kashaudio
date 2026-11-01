#!/usr/bin/env python3
"""Build validated registry of all chanted works on the box.
Usage: python3 /tmp/build_registry.py
Writes: /home/ubuntu/kashmir_audio/registry.json
"""
import json, re, glob
from pathlib import Path
from datetime import datetime, timezone

AUD = Path(__file__).resolve().parent
CARDS = AUD / "cards"
TR = json.load(open(AUD / "translations.json", encoding="utf-8"))

META = {
    # dir: (title, author, expected_clips, kind)
    "bhairavastava": ("Bhairavastava (+phala)", "Abhinavagupta", 10, "chant"),
    "anuttarashtika": ("Anuttarastika", "Abhinavagupta", 8, "chant"),
    "stavacintamani": ("Stavacintamani", "Bhatta Narayana", 120, "chant"),
    "dehastha": ("Dehasthadevatacakra", "anon (Krama)", 16, "chant"),
    "bodhapanadasika": ("Bodhapanadasika", "Abhinavagupta", 15, "chant"),
    "mahopadeshavimshatika": ("Mahopadeshavimshatika", "Abhinavagupta", 20, "chant"),
    "rahasyapanchadashika": ("Rahasyapanchadashika", "Abhinavagupta", 16, "chant"),
    "paramadvayadvadashika": ("Paramarthadvadashika (+phala)", "Abhinavagupta", 13, "chant"),
    "pancashloki": ("Pancashloki", "Abhinavagupta", 5, "chant"),
    "kramastotra": ("Kramastotra (+dating)", "Abhinavagupta", 30, "chant"),
    "shivastotravali_1": ("Sivastotravali Stotra 1 rest", "Utpaladeva", 25, "chant"),
    "anubhavanivedana": ("Anubhavanivedana", "Abhinavagupta", 4, "chant"),
    "bodhavilasa": ("Bodhavilasa", "Ksemaraja", 42, "chant"),
    "bhairavanukarana": ("Bhairavanukaranastotra", "Ksemaraja", 48, "chant"),
    "ajadapramatrsiddhi": ("Ajadapramatrsiddhi", "Utpaladeva", 27, "chant"),
    "paryantapancasika": ("Paryantapancasika", "Abhinavagupta", 53, "chant"),
    "pratyabhijnahrdaya": ("Pratyabhijnahrdayam", "Ksemaraja", 20, "chant"),
    "paramarthasara": ("Paramarthasara", "Abhinavagupta", 105, "chant"),
    "sambandhasiddhi": ("Sambandhasiddhi", "Utpaladeva", 9, "chant"),
    "isvarasiddhi": ("Isvarasiddhi", "Utpaladeva", 17, "chant"),
    "ptvmadhyama": ("PTV Madhyama", "Abhinavagupta", 12, "chant"),
    "paramarthacarca": ("Paramarthacarca", "Abhinavagupta", 8, "chant"),
    "parapravesika": ("Parapravesika", "Ksemaraja", 11, "chant"),
    "tattvasandoha": ("Tattvasandoha", "Ksemaraja", 21, "chant"),
    "svabodhasiddhi": ("Svabodhasiddhi", "Bhutiraja", 8, "chant"),
    "saktavijnana": ("Saktavijnana", "Somananda", 10, "chant"),
    "spandakarika": ("Spandakarika", "Vasugupta", 13, "chant"),
    "sivasutra": ("Sivasutra", "Vasugupta", 75, "chant"),
    "anuttarashtika_trad": ("Anuttarastika (traditional cuts)", "Abhinavagupta/trad", 8, "trad"),
    "shivastotravali": ("Sivastotravali Stotras 1-20 (fish audio)", "Utpaladeva", 450, "sing"),
}

FULL_MAP = {}
for _d in list(META):
    _fn = f"{_d}_full.mp4"
    if (AUD / "cards" / _fn).exists():
        FULL_MAP[_d] = _fn
FULLNAME = FULL_MAP

# Works whose per-clip cards were rendered, byte-verified and relayed to
# R2/volume (2026-11-01), then pruned locally. Local file counts cannot
# prove this; the delivery runs can.
SHIPPED_CARDS = {
 "bhairavastava","anuttarashtika","stavacintamani","dehastha","bodhapanadasika",
 "mahopadeshavimshatika","rahasyapanchadashika","paramadvayadvadashika",
 "pancashloki","kramastotra","shivastotravali_1","anubhavanivedana","bodhavilasa",
 "bhairavanukarana","ajadapramatrsiddhi","paryantapancasika","pratyabhijnahrdaya",
 "paramarthasara","sambandhasiddhi","isvarasiddhi","ptvmadhyama","paramarthacarca",
 "parapravesika","tattvasandoha","svabodhasiddhi","saktavijnana","spandakarika",
 "sivasutra",
}

DEVA_RE = re.compile(r"^[ऀ-ॿ\s।॥]+$")

works = []
tot_wavs = tot_clips = tot_syls = tot_cards = 0
tot_bad = tot_mono = tot_zero = 0

for d, (title, author, exp, kind) in META.items():
    wdir = AUD / d
    e = {"dir": d, "title": title, "author": author, "kind": kind,
         "expected_clips": exp, "issues": []}
    wavs = sorted(wdir.glob("*.wav")) if wdir.exists() else []
    e["wavs_on_disk"] = len(wavs)
    e["wavs_empty"] = sum(1 for p in wavs if p.stat().st_size == 0)
    e["wav_bytes_total"] = sum(p.stat().st_size for p in wavs)
    if not wdir.exists():
        e["issues"].append("missing dir (symlink target?)")
    if len(wavs) != exp:
        e["issues"].append(f"wav count {len(wavs)} != expected {exp}")
    tot_wavs += len(wavs)

    wt_path = wdir / "word_timings.json"
    res_files = sorted(wdir.glob("res_*.json"))
    e["res_file"] = res_files[0].name if res_files else None
    if not wt_path.exists():
        e["clips"] = 0
        e["issues"].append("missing word_timings.json")
        works.append(e)
        continue
    try:
        clips = json.load(open(wt_path, encoding="utf-8"))
    except Exception as ex:
        e["clips"] = 0
        e["issues"].append(f"word_timings unreadable: {ex}")
        works.append(e)
        continue
    e["clips"] = len(clips)
    tot_clips += len(clips)
    if len(clips) != exp and d != "parapravesika":
        # parapravesika expected 11 vs catalog 12, known
        e["issues"].append(f"clip count {len(clips)} != expected {exp}")
    ids = [c.get("id") for c in clips]
    # wav <-> id match
    wav_ids = {p.stem for p in wavs}
    missing_wav = [i for i in ids if i not in wav_ids]
    orphan_wav = sorted(wav_ids - set(ids))
    e["clips_missing_wav"] = missing_wav
    e["orphan_wavs"] = orphan_wav
    if missing_wav:
        e["issues"].append(f"{len(missing_wav)} clip ids lack wav: {missing_wav[:3]}")
    if orphan_wav:
        e["issues"].append(f"{len(orphan_wav)} orphan wavs: {orphan_wav[:3]}")

    bad = mono = zero = overlap = 0
    syls_n = 0
    scores = []
    dur_tot = 0.0
    for c in clips:
        dur_tot += float(c.get("dur", 0) or 0)
        prev = -1e-9
        for s in c.get("syls", []):
            syls_n += 1
            if not DEVA_RE.match(s.get("d", "")):
                bad += 1
            t_on, t_off = float(s["t_on"]), float(s["t_off"])
            if t_off <= t_on:
                zero += 1
            if t_on < prev - 1e-9:
                mono += 1
            prev = s["t_off"] if isinstance(s["t_off"], (int, float)) else prev
            if "mms" in s and isinstance(s["mms"], (int, float)):
                scores.append(float(s["mms"]))
    # cross-pada overlap: check sorted syls per clip
    for c in clips:
        ss = sorted(c.get("syls", []), key=lambda s: float(s["t_on"]))
        for a, b in zip(ss, ss[1:]):
            if float(b["t_on"]) < float(a["t_off"]) - 0.001 and a.get("pada") != b.get("pada"):
                overlap += 1
                break
    e["syls_total"] = syls_n
    e["badchars"] = bad
    e["nonmono"] = mono
    e["zerodur"] = zero
    e["cross_pada_overlaps"] = overlap
    e["mms_mean"] = round(sum(scores) / len(scores), 4) if scores else None
    e["mms_min"] = round(min(scores), 4) if scores else None
    e["mms_n"] = len(scores)
    e["dur_total_sec"] = round(dur_tot, 1)
    tot_syls += syls_n
    tot_bad += bad
    tot_mono += mono
    tot_zero += zero
    if bad:
        e["issues"].append(f"{bad} badchars")
    if zero:
        e["issues"].append(f"{zero} zero-dur syls")
    if mono:
        e["issues"].append(f"{mono} nonmono syls")
    if e["mms_mean"] is not None and e["mms_mean"] < 0.7:
        e["issues"].append(f"low mms mean {e['mms_mean']}")
    # NOTE: mms_min is per-syllable and routinely tiny (silent consonants,
    # cluster onsets). It is reported for triage but is NOT a defect signal.

    # cards
    have_mp4 = sum(1 for i in ids if (CARDS / f"{i}.mp4").exists())
    have_mid = sum(1 for i in ids if (CARDS / f"{i}_mid.png").exists())
    have_held = sum(1 for i in ids if (CARDS / f"{i}_held.png").exists())
    e["cards_mp4"] = have_mp4
    e["cards_mid"] = have_mid
    e["cards_held"] = have_held
    tot_cards += have_mp4
    orphan_cards = []
    # orphan card check only for s1 (known _1_1)
    if d == "shivastotravali_1" and (CARDS / "shivastotravali_1_1.mp4").exists() and "shivastotravali_1_1" not in ids:
        orphan_cards.append("shivastotravali_1_1.mp4 (no timing)")
    e["orphan_cards"] = orphan_cards
    if orphan_cards:
        e["issues"].append("orphan card: shivastotravali_1_1.mp4")

    # full
    fn = FULLNAME.get(d)
    if fn and (CARDS / fn).exists():
        sz = (CARDS / fn).stat().st_size
        e["full_mp4"] = fn
        e["full_bytes"] = sz
        if sz < 400_000:
            e["issues"].append(f"full {fn} suspiciously small ({sz}B) — broken?")
    else:
        e["full_mp4"] = None
        e["full_bytes"] = 0

    # translations
    have_tr = sum(1 for i in ids if i in TR)
    e["translations_have"] = have_tr
    e["translations_missing"] = len(ids) - have_tr

    # status
    if kind == "trad":
        e["status"] = "trad-ref"
    elif kind == "sing":
        e["status"] = "sing-audio-only"
    elif d in SHIPPED_CARDS and e["clips"] and not e["issues"]:
        e["status"] = "shipped" if d != "parapravesika" else "needs-rerender"
    elif have_mp4 == 0:
        e["status"] = "audio-done"
    elif have_mp4 < len(ids):
        e["status"] = "cards-partial"
    else:
        e["status"] = "cards-done-no-full"
    works.append(e)

reg = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "audio_root": str(AUD),
    "cards_dir": str(CARDS),
    "translations_file": str(AUD / "translations.json"),
    "cards_location": "r2:kashaudio-backup/cards-noen-20261101-noen + opencode2 volume kashmir-video-20261101/ (local per-clip mp4s + stills pruned after byte verification)",
    "fulls_location": "opencode2 volume kashmir-video-20261101/fulls + r2:ets/finals-*",
    "translations_keys_total": len(TR),
    "works_total": len(works),
    "wavs_total": tot_wavs,
    "clips_total": tot_clips,
    "syls_total": tot_syls,
    "cards_mp4_total": tot_cards,
    "badchars_total": tot_bad,
    "nonmono_total": tot_mono,
    "zerodur_total": tot_zero,
    "works": works,
}
out = AUD / "registry.json"
json.dump(reg, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"wrote {out}")
print(f"works={len(works)} wavs={tot_wavs} clips={tot_clips} syls={tot_syls} cards={tot_cards} bad={tot_bad} mono={tot_mono} zero={tot_zero}")
for w in works:
    flag = "" if not w["issues"] else "  ISSUES: " + "; ".join(w["issues"][:3])
    print(f"{w['dir']:25} clips={w.get('clips',0):3} wav={w['wavs_on_disk']:3} cards={w.get('cards_mp4',0):3}/{w.get('clips',0)} tr={w.get('translations_have',0)}/{w.get('clips',0)} mms={w.get('mms_mean')} status={w.get('status')}{flag}")
