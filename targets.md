# Targets — Kashmir Shaiva chant collection (chosen 2026-10-30)

Priority order. "Audio" = AI (Vagdhenu) is the deliverable voice; traditional
recordings are ear-references only unless owner says otherwise.

| # | Text | Verses | Status | Notes |
|---|---|---|---|---|
| 1 | **Bhairavastava** (Abhinavagupta) | 9 + phala | AI wavs ✅, cards pending layout approval | render first — short, complete, test vehicle |
| 2 | **Stavacintāmaṇi** (Bhaṭṭa Nārāyaṇa) | ~120 | text (GRETIL) ready, no shard yet | the scale pick — anuṣṭubh throughout, nightly recitation library for stages 7–8 |
| 3 | **Dehasthadevatācakrastotra** | 16 | text (SanskritDocs) ready | body-as-circle-of-deities pairs with install stages 1–6 |
| 4 | **Bodhapañcadaśikā** (Abhinavagupta) | 15 | text (GRETIL) ready | anuṣṭubh-suited rhythm test, stage 7 material |
| 5 | **Anuttarāṣṭikā** (Abhinavagupta) | 8 | AI wavs ✅ + cards rendered (old layout, redo after approval) | long-metre but regular; Lakshmanjoo recitation = EAR-REFERENCE only (`ref/anuttarashtika-trad.mp3`, trad cards parked in `cards/trad/`) |
| 6 | **Śivastotrāvalī** (Utpaladeva) | 1.1 pilot ✅, full 20 stotras long-term | long-term project once pipeline proven |
| 7 | **Kramastotra** (Abhinavagupta) | 29+dating | parked until Krama layer, or listening-only render |

## Pipeline state (per PROCESS.md)
- render: Kaggle GPU kernel (v8 proven, 18/18)
- alignment: MMS sa-IN (`mms-align/`) + matra rhythm (`regen_syls.py`)
- cards: layout under still-approval loop — see PROCESS.md Mistakes
- quota: ~4h of 30h/week Kaggle GPU used; Stavacintāmaṇi 120 ≈ 3h
