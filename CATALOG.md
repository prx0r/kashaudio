# Catalog — Kashmir Shaiva chant collection (2026-10-31)

Single source of truth. Supersedes `STATUS.md` / `targets.md` (kept for history).
"Audio" = AI (Vagdhenu) is the deliverable voice; traditional = ear-ref only.
**My lane: audio (render + align).** Translations = prx0r/ipvv. Cards + fulls = alignment agent.

## Fully shipped — render + align + cards + fulls

| # | Text | Author | Verses | Cards | Full | Translations |
|---|---|---|---|---|---|---|
| 1 | Bhairavastava (+ phala) | Abhinavagupta | 10 | ✅ 10/10 | ✅ | ✅ |
| 2 | Anuttarāṣṭikā | Abhinavagupta | 8 | ✅ 8/8 | ✅ | ✅ |
| 3 | Stavacintāmaṇi | Bhaṭṭa Nārāyaṇa | 120 | ✅ 120/120 | ✅ | ✅ |
| 4 | Dehasthadevatācakra | anon (Krama) | 16 | ✅ 16/16 | ✅ | ✅ |
| 5 | Bodhapañcadaśikā | Abhinavagupta | 15 | ✅ 15/15 | ✅ | ✅ |
| 6 | Mahopadeśaviṃśatikā | Abhinavagupta | 20 | ✅ 20/20 | ✅ | ✅ |
| 7 | Rahasyapañcadaśikā | Abhinavagupta | 15+colophon | ✅ 16/16 | ✅ | ✅ |
| 8 | Paramārthadvādaśikā | Abhinavagupta | 12+phala | ✅ 13/13 | ✅ | ✅ |
| 9 | Pañcaślokī | Abhinavagupta | 5 | ✅ 5/5 | ✅ | ✅ (canonical) |
| 10 | Kramastotra | Abhinavagupta | 29+dating | ✅ 30/30 | ✅ | ✅ (Singh/Maheshvarananda) |

**Totals: 362 verses fully shipped across 10 works. 10 fulls on disk + R2.**

## Render + align done, cards pending

| # | Text | Author | Verses | Wavs | Aligned | Cards | Blocker |
|---|---|---|---|---|---|---|---|
| 11 | Śivastotrāvalī Stotra 1 rest | Utpaladeva | 25 | ✅ | ✅ | 3/25 | ipvv translations (25 verses) |

## In flight (v11 on Kaggle, ~1h left)

| # | Text | Author | Verses | State |
|---|---|---|---|---|
| 12 | Anubhavanivedana | Abhinavagupta | 4 | rendering |
| 13 | Bodhavilāsa | Kṣemarāja | 42 | rendering |
| 14 | Bhairavānukaraṇastotra | Kṣemarāja | 48 | rendering |
| 15 | Ajadapramātṛsiddhi | Utpaladeva | 27 | rendering |

## Shards built, awaiting kernel (v12)

| # | Text | Author | Verses | Format | Status |
|---|---|---|---|---|---|
| 16 | Pratyabhijñāhṛdayam | Kṣemarāja | 20 sūtras | **gadya** (prose) | FORMAT FLAG: pilot 2–3 first |
| 17 | Paryantapañcāśikā | Abhinavagupta | 53 | anuṣṭubh | ready |

## Need text source (not on GRETIL)

| # | Text | Author | Verses | Note |
|---|---|---|---|---|
| 18 | Parāprāveśikā | Kṣemarāja | 1 aphorism | not on GRETIL; try Muktabodha |
| 19 | Paramārthacarcā | Abhinavagupta | TBD | not on GRETIL; Pandey appendix |
| 20 | Īśvara/Sambandha-siddhis | Utpaladeva | TBD | Ajadapramātṛsiddhi done; others need source |
| 21 | Tattvasandoha | Kṣemarāja | verify | Tier 2 if short |
| 22 | Paramārthasāra | Abhinavagupta | 105 | GRETIL ✅; next capstone |

## Out of scope — huge targets for Fish Audio / other agent

These are too large for our Kaggle quota + Vagdhenu pipeline (100+ verses
each), but Fish Audio's S2.1-Pro has a **free API** (`s2.1-pro-free`) and
voice-clone from 10–30s reference audio. Another agent with a Fish key
could render these:

| Target | Author | Size | Why out of scope | Source |
|---|---|---|---|---|
| **Paramārthasāra** | Abhinavagupta | 105 verses | fits but it's our next capstone — do with Vagdhenu | GRETIL TEI ✅ |
| **Tantrasāra** | Abhinavagupta | ~268p, mostly prose | STUDY by our rule; but verse portions could be chanted | GRETIL TEI ✅ |
| **Tantrāloka** | Abhinavagupta | 37+ chapters, thousands of verses | massive; STUDY; verse insertions only if desired | GRETIL TEI ✅ |
| **Vijñāna Bhairava Tantra** | tradition | 162 verses | not trio; but hugely popular for chanting | multiple sources |
| **Śivadṛṣṭi** | Somānanda | ~30 verses | non-trio (pre-Utpaladeva); short enough for anyone | need source |
| **Spandakārikā** | Vasugupta | ~33 verses | non-trio; foundational; short | GRETIL TEI ✅ |
| **Śivasūtra** | Vasugupta | 77 sūtras | non-trio; gadya format like Hṛdayam | GRETIL TEI ✅ |
| **Bhagavad Gītā** | tradition | 700 | huge; universal chanting target | multiple |
| **Śrīmad Bhāgavatam** | tradition | 16,017 | Vagdhenu already did this (per README) | already done |

## Delivery rules

- **CHANT** = mantra-recitation, Vagdhenu syllable pipeline.
- **SING** = melodic bhakti — Stotrāvalī Stotras 2–20 wait for singing phase.
- **STUDY** = treatises, commentaries — never audio targets.

## Pipeline state (see PROCESS.md)

- Render: v10 = 109/109 clean; v11 running. Env law: numpy 2.2.x, IndicF5
  pinned to live HEAD `13f7c4d...cacacdc7`, `indic-transliteration` explicit.
  Verify cell RAISES on failure (v10 false-COMPLETE incident).
- Align: word MMS → syllable MMS authority → matra rhythm. Means 0.92–0.94.
- Cards: stills-first law, per-frame overflow guard, LEAD=0.28 locked.
- R2: `publish_r2.sh` backs up working tree + finals. Latest: `v10-cards`.
- Quota: ~9h of 30h/week used. Disk: ~2.9G free — watch /tmp.
