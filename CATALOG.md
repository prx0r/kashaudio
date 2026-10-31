# Catalog — Kashmir Shaiva chant collection (2026-10-31)

Single source of truth. Supersedes `STATUS.md` / `targets.md` (kept for history).
"Audio" = AI (Vagdhenu) is the deliverable voice; traditional = ear-ref only.
**My lane: audio (render + align).** Translations = prx0r/ipvv. Cards + fulls = alignment agent.

## Completed — AI chant rendered + aligned

| # | Text | Author | Verses | AI chant | Aligned | Cards | Full | Translations | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Bhairavastava (+ phala) | Abhinavagupta | 10 | ✅ | ✅ | ✅ | ✅ | ✅ | v8 |
| 2 | Anuttarāṣṭikā | Abhinavagupta | 8 | ✅ | ✅ | ✅ | ✅ | ✅ | v8; trad parked in `cards/trad/` |
| 3 | Stavacintāmaṇi | Bhaṭṭa Nārāyaṇa | 120 | ✅ | ✅ | ✅ | ✅ | ✅ | v9 |
| 4 | Dehasthadevatācakra | anon (Krama; Pandey attrs Abhinavagupta) | 16 | ✅ | ✅ | ✅ | ✅ | ✅ | v9 |
| 5 | Bodhapañcadaśikā | Abhinavagupta | 15 | ✅ | ✅ | ✅ | ✅ | ✅ | v9 |
| 6 | Mahopadeśaviṃśatikā | Abhinavagupta | 20 | ✅ | ✅ | pending | pending | ✅ | v10; 16 anuṣṭubh |
| 7 | Rahasyapañcadaśikā | Abhinavagupta | 15 + colophon | ✅ | ✅ | pending | pending | ✅ | v10; OCR source |
| 8 | Paramārthadvādaśikā | Abhinavagupta | 12 + phala | ✅ | ✅ | pending | pending | ✅ | v10; OCR source |
| 9 | Pañcaślokī | Abhinavagupta | 5, śārdūla | ✅ | ✅ | pending | pending | ✅ (canonical) | v10; OCR source |
| 10 | Kramastotra | Abhinavagupta | 29 + dating v30 | ✅ | ✅ | pending | pending | ✅ (Singh/Maheshvarananda) | v10; long-metre test passed |
| 11 | Śivastotrāvalī Stotra 1 rest | Utpaladeva | 25 (v2–26) | ✅ | ✅ | pending | pending | **pending ipvv** | v10; SING exception |

**Totals: 278 AI verses rendered + aligned. 5 fulls shipped (v8/v9). 6 new fulls pending cards.**

R2 backup: `r2:kashaudio-backup/kashmir_audio-20261030/` (pre-v10; re-publish after cards).
Finals: `r2:ets/finals-20261030/` (v8/v9 fulls only; v10 fulls pending).

## Canonical delivery — CHANT vs SING vs STUDY

- **CHANT** = mantra-recitation, Vagdhenu pipeline as built.
- **SING** = melodic bhakti song — Stotrāvalī Stotras 2–20 wait for singing phase.
- **STUDY** = treatises, commentaries — never audio.

## Next targets (Tier 2 — all CHANT, ready to render)

| # | Text | Author | Verses | Text src | Status |
|---|---|---|---|---|---|
| 1 | Anubhavanivedana | Abhinavagupta | 4, śārdūla | clean itx | shard built; render next |
| 2 | Pratyabhijñāhṛdayam | Kṣemarāja | 20 sūtras | GRETIL TEI | FORMAT FLAG: prose sūtras, pilot 2–3 gadya first |
| 3 | Parāprāveśikā | Kṣemarāja | 1 aphorism | GRETIL | tiny; same pilot as Hṛdayam |
| 4 | Bodhavilāsa | Kṣemarāja | 42 anuṣṭubh | GRETIL TEI | ready |
| 5 | Bhairavānukaraṇastotra | Kṣemarāja | 48 mixed | GRETIL TEI | ready |
| 6 | Ajadapramātṛsiddhi | Utpaladeva | 27 kārikās | GRETIL TEI | ready |
| 7 | Paryantapañcāśikā | Abhinavagupta | 50 | verify text | need source |
| 8 | Paramārthacarcā | Abhinavagupta | count TBD | verify text | need source |
| 9 | Īśvara/Sambandha-siddhis | Utpaladeva | counts TBD | verify text | need source |
| 10 | Paramārthasāra | Abhinavagupta | 105 | GRETIL | capstone; Tier 2 |
| 11 | Kramastotra | Abhinavagupta | 29+dating | GRETIL TEI | **DONE (v10)** |
| 12 | Tattvasandoha | Kṣemarāja | verify size | need source | Tier 2 if short |

## Pipeline state (see PROCESS.md)

- Render: Kaggle GPU v10 — 109 clips, ~2h, 0 errors. Env law: numpy 2.2.x, IndicF5 pinned to live HEAD, `indic-transliteration` explicit.
- Align: word MMS → syllable MMS authority → matra rhythm. All v10 means 0.92–0.94.
- Cards: pending for v10 works (translations blocking for stotra-1; rest ready).
- Quota: ~8h of 30h/week used.
- Disk: 4.1G free — watch /tmp on f32 caches.
