# Targets — Kashmir Shaiva chant collection (updated 2026-10-31)

> **CATALOG.md is now the source of truth.** This file kept for history.

Priority: short, high-impact, chant-meant Trika works. Abhinavagupta →
Kṣemarāja → Utpaladeva. Audio = AI (Vagdhenu); trad = ear-ref only.
Lane split: audio/render = this repo, translations = prx0r/ipvv,
cards/alignment = separate agent.

## Completed (render + align done; cards/finals pending for v10)

| # | Text | Author | Verses | Status |
|---|---|---|---|---|
| 1 | Bhairavastava (+phala) | Abhinavagupta | 10 | FULLY DONE (v8) |
| 2 | Anuttarāṣṭikā | Abhinavagupta | 8 | FULLY DONE (v8) |
| 3 | Stavacintāmaṇi | Bhaṭṭa Nārāyaṇa | 120 | FULLY DONE (v9) |
| 4 | Dehasthadevatācakra | anon (Krama) | 16 | FULLY DONE (v9) |
| 5 | Bodhapañcadaśikā | Abhinavagupta | 15 | FULLY DONE (v9) |
| 6 | Mahopadeśaviṃśatikā | Abhinavagupta | 20 | render+align ✅ (v10) |
| 7 | Rahasyapañcadaśikā | Abhinavagupta | 15+colophon | render+align ✅ (v10) |
| 8 | Paramārthadvādaśikā | Abhinavagupta | 12+phala | render+align ✅ (v10) |
| 9 | Pañcaślokī | Abhinavagupta | 5 | render+align ✅ (v10) |
| 10 | Kramastotra | Abhinavagupta | 29+dating | render+align ✅ (v10) — long-metre test passed |
| 11 | Śivastotrāvalī Stotra 1 rest | Utpaladeva | 25 | render+align ✅ (v10); translations pending |

## In flight (v11 running)

| # | Text | Author | Verses | State |
|---|---|---|---|---|
| 12 | Anubhavanivedana | Abhinavagupta | 4, śārdūla | rendering |
| 13 | Bodhavilāsa | Kṣemarāja | 42, anuṣṭubh | rendering |
| 14 | Bhairavānukaraṇastotra | Kṣemarāja | 48, mixed | rendering |
| 15 | Ajadapramātṛsiddhi | Utpaladeva | 27 kārikās | rendering |

## Next queue (after v11)

| # | Text | Author | Verses | Notes |
|---|---|---|---|---|
| 16 | Pratyabhijñāhṛdayam | Kṣemarāja | 20 sūtras | FORMAT FLAG: prose, pilot 2–3 gadya first |
| 17 | Parāprāveśikā | Kṣemarāja | 1 aphorism | same pilot as Hṛdayam |
| 18 | Paryantapañcāśikā | Abhinavagupta | 50 | need text source |
| 19 | Paramārthacarcā | Abhinavagupta | TBD | need text source |
| 20 | Īśvara/Sambandha-siddhis | Utpaladeva | TBD | need text source |
| 21 | Paramārthasāra | Abhinavagupta | 105 | capstone — next Stavacintamani-scale |
| 22 | Tattvasandoha | Kṣemarāja | verify | Tier 2 if short |

## Long-term / parked

- Śivastotrāvalī Stotras 2–20 (Utpaladeva): SING phase, not chant.
- Pañcastavī, Sāmbapañcāśikā: non-trio, only if the well runs dry.
- Kramastotra: DONE (was parked for long-metre test, v10 passed).

## Pipeline state

- render: Kaggle GPU v11 in flight (v10 = 109/109 clean)
- alignment: MMS sa-IN → syllable MMS → matra rhythm; means 0.92–0.94
- cards: approved ruby-rows layout, stills-first, overflow guard
- quota: ~8h of 30h/week used
