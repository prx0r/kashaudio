# Catalog — Kashmir Shaiva chant collection (2026-10-31)

Single source of truth. Supersedes `STATUS.md` / `targets.md` (kept for history).
"Audio" = AI (Vagdhenu) is the deliverable voice; traditional = ear-ref only.
**Lane split: audio (render+align) = this repo. Translations = prx0r/ipvv. Cards + fulls = alignment agent.**

## Fully shipped — render + align + cards + fulls (10 works, 362 verses)

| # | Text | Author | Verses |
|---|---|---|---|
| 1 | Bhairavastava (+ phala) | Abhinavagupta | 10 |
| 2 | Anuttarāṣṭikā | Abhinavagupta | 8 |
| 3 | Stavacintāmaṇi | Bhaṭṭa Nārāyaṇa | 120 |
| 4 | Dehasthadevatācakra | anon (Krama) | 16 |
| 5 | Bodhapañcadaśikā | Abhinavagupta | 15 |
| 6 | Mahopadeśaviṃśatikā | Abhinavagupta | 20 |
| 7 | Rahasyapañcadaśikā | Abhinavagupta | 15+colophon |
| 8 | Paramārthadvādaśikā | Abhinavagupta | 12+phala |
| 9 | Pañcaślokī | Abhinavagupta | 5 |
| 10 | Kramastotra | Abhinavagupta | 29+dating |

10 fulls on disk + R2 (`publish_r2.sh`).

## Render + align done — cards waiting on translations (18 works, 399 verses)

| # | Text | Author | Verses |
|---|---|---|---|
| 11 | Śivastotrāvalī Stotra 1 rest | Utpaladeva | 25 |
| 12 | Anubhavanivedana | Abhinavagupta | 4 |
| 13 | Bodhavilāsa | Kṣemarāja | 42 |
| 14 | Bhairavānukaraṇastotra | Kṣemarāja | 48 |
| 15 | Ajadapramātṛsiddhi | Utpaladeva | 27 |
| 16 | Paryantapañcāśikā | Abhinavagupta | 53 |
| 17 | Pratyabhijñāhṛdayam | Kṣemarāja | 20 sūtras |
| 18 | Paramārthasāra | Abhinavagupta | 105 |
| 19 | Sambandhasiddhi | Utpaladeva | 9 |
| 20 | Īśvarasiddhi | Utpaladeva | 17 |
| 21 | PTV Madhyama | Abhinavagupta | 12 |
| 22 | Paramārthacarcā | Abhinavagupta | 8 |
| 23 | Parāprāveśikā | Kṣemarāja | 12 |
| 24 | Tattvasandoha | Kṣemarāja | 21 |
| 25 | Svabodhasiddhi | Bhūtirāja | 8 |
| 26 | Śaktavijñāna | Somānanda | 10 |
| 27 | Spandakārikā | Vasugupta | 13 |
| 28 | Śivasūtra | Vasugupta | 75 |

**Grand total: 761 verses across 28 works rendered + aligned. 0 errors, 0 badchars.**

## Recitation gold remaining in prx0r/ipvv

Filter: verse/kārikā/stotra type (not commentary), text held or sourceable.

| Work | Author | Size | ipvv status | Text | Priority |
|---|---|---|---|---|---|
| **Anuttaraśataka** | Abhinavagupta | 100 vv | STOCKPILE | need source | HIGH — short century |
| **Prakaraṇastotra** | Abhinavagupta | ? | STOCKPILE | need source | HIGH |
| **Paramārthasaṃgraha** | Abhinavagupta | ? | STOCKPILE | need source | MED |
| **Tantravaṭadhānikā** | Abhinavagupta | verse | STOCKPILE | need source | MED — "Seed of Tantra" |
| **Tattvādhvaprakāśikā** | Abhinavagupta | ? | STOCKPILE | need source | MED |
| **Spandasandoha** | Kṣemarāja | short | SOURCE_HELD | `spandasandoha.txt` ✅ | HIGH — text in hand |
| **Śivastotrāvalī Stotras 2–20** | Utpaladeva | 19 songs | SOURCE_HELD | full shard exists ✅ | SING phase (not chant) |
| **IPK** | Utpaladeva | 4 adhikāras | SOURCE_HELD | `ipk.txt` ✅ | LOW — dense philosophy, STUDY |
| **Venisamhara** | Bhaṭṭa Nārāyaṇa | 6 acts | SOURCE_HELD | drama, not chant | SKIP |
| **Spandanirṇaya** | Kṣemarāja | 53 comm. | SOURCE_HELD | commentary | STUDY |
| **Śivasūtravimarśinī** | Kṣemarāja | 77 comm. | SOURCE_HELD | commentary | STUDY |

**Immediate next:** Spandasandoha (text in hand) + Anuttaraśataka (source hunt).

## Delivery rules

- **CHANT** = mantra-recitation, Vagdhenu syllable pipeline.
- **SING** = melodic bhakti — Stotrāvalī Stotras 2–20 wait for singing phase.
- **STUDY** = treatises, commentaries — never audio targets.

## Pipeline state (see PROCESS.md for laws)

- Render: v10–v17 complete, 761 clips, 0 env failures across 592 session clips.
  Env law: numpy 2.2.x, IndicF5 pinned to live HEAD, verify cell RAISES.
- Align: word MMS → syllable MMS authority → matra rhythm. Means 0.87–0.94.
- Cards: stills-first law, per-frame overflow guard, LEAD=0.28 locked.
  10 works shipped; 18 works waiting on translations.
- R2: `publish_r2.sh` = 3 targets (R2 backup + R2 finals + opencode2 volume).
- Quota: ~15h of 30h/week used (v8–v17). Disk: ~2.4G free.
- Translations: 278/761 done (Qwen + canonical). 483 pending — prx0r/ipvv lane.
