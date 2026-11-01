# Catalog — Kashmir Shaiva chant collection (2026-11-01)

Single source of truth. Supersedes `STATUS.md` / `targets.md` (kept for history).
`registry.json` holds machine-readable verified state; this file explains it.

"Audio" = AI (Vagdhenu) is the deliverable voice; traditional = ear-ref only.
**Lane split: audio (render+align) = this repo. Translations = prx0r/ipvv.
Cards + fulls = this repo. Site (recite pages, syllable karaoke) = prx0r/ipvv.**

## State at a glance

- **769 chant verses across 28 works** rendered + aligned: 0 badchars,
  0 non-monotonic, 0 zero-duration. Plus 450 Śivastotrāvalī SING verses
  (stotras 1–20) and 8 traditional ear-ref cuts.
- **All 28 chant works have cards + fulls.** No work is waiting on English
  any more — the approved Sanskrit-only centred layout unblocked them.
- **All 769 are live on the ipvv site** as verse-by-verse recite pages with
  syllable-exact highlighting (words conjoined). 1193 mp3s.
- **English: 286/769.** 483 still missing (prx0r/ipvv lane). Cards render
  Sanskrit-only and are complete without it.

## Shipped — render + align + cards + fulls (28 works, 769 verses)

| # | Text | Author | Verses | Align |
|---|---|---|---|---|
| 1 | Bhairavastava (+phala) | Abhinavagupta | 10 | 0.92 |
| 2 | Anuttarāṣṭikā | Abhinavagupta | 8 | 0.94 |
| 3 | Stavacintāmaṇi | Bhaṭṭa Nārāyaṇa | 120 | 0.93 |
| 4 | Dehasthadevatācakra | anon (Krama) | 16 | 0.93 |
| 5 | Bodhapañcadaśikā | Abhinavagupta | 15 | 0.93 |
| 6 | Mahopadeśaviṃśatikā | Abhinavagupta | 20 | 0.93 |
| 7 | Rahasyapañcadaśikā | Abhinavagupta | 16 | 0.92 |
| 8 | Paramārthadvādaśikā | Abhinavagupta | 13 | 0.94 |
| 9 | Pañcaślokī | Abhinavagupta | 5 | 0.92 |
| 10 | Kramastotra (+dating) | Abhinavagupta | 30 | 0.93 |
| 11 | Anubhavanivedana | Abhinavagupta | 4 | 0.94 |
| 12 | Bodhavilāsa | Kṣemarāja | 42 | 0.93 |
| 13 | Bhairavānukaraṇastotra | Kṣemarāja | 48 | 0.92 |
| 14 | Ajadapramātṛsiddhi | Utpaladeva | 27 | 0.89 |
| 15 | Paryantapañcāśikā | Abhinavagupta | 53 | 0.93 |
| 16 | Pratyabhijñāhṛdayam | Kṣemarāja | 20 | 0.87 |
| 17 | Paramārthasāra | Abhinavagupta | 105 | 0.93 |
| 18 | Sambandhasiddhi | Utpaladeva | 9 | 0.92 |
| 19 | Īśvarasiddhi | Utpaladeva | 17 | 0.92 |
| 20 | PTV Madhyama | Abhinavagupta | 12 | 0.93 |
| 21 | Paramārthacarcā | Abhinavagupta | 8 | 0.94 |
| 22 | Parāprāveśikā | Kṣemarāja | 11 | **needs re-render** |
| 23 | Tattvasandoha | Kṣemarāja | 21 | 0.91 |
| 24 | Svabodhasiddhi | Bhūtirāja | 8 | 0.92 |
| 25 | Śaktavijñāna | Somānanda | 10 | 0.91 |
| 26 | Spandakārikā | Vasugupta | 13 | 0.92 |
| 27 | Śivasūtra | Vasugupta | 75 | 0.87 |
| 28 | Śivastotrāvalī 1 (rest) | Utpaladeva | 25 | 0.93 |

Plus **Śivastotrāvalī stotras 2–20** as SING-source audio: 424 verses,
0.88 mean, cards + 19 per-stotra fulls built.

**Parāprāveśikā is the one work not truly done.** Re-aligning (2026-11-01)
moved it 0.58 → 0.57, which proved alignment was never the problem: the
audio was rendered from the *pre-fix* shard and the shard was rebuilt
afterwards (commit `f809cd1`), so text and audio disagree. Four clips
demand up to 7.05 syllables/second — impossible for chant. **Fix is a
re-render from the current shard, then align** (11 clips, ~5 min GPU).

Other alignment outliers, audited and accepted:
`Śivasūtra` 0.87 and
`Pratyabhijñāhṛdayam` 0.87 are prose sūtras — short clips score low by
nature (median 3.4 syl/s means the audio is fine). `hrd_11` (0.65s, one word) renders silent — Vagdhenu limit on
ultra-short input, accepted.

## Site state (prx0r/ipvv)

- 47 recite pages, 1193 mp3s, syllable-level karaoke verified on all.
- Audio relayed to `r2:svread-audio/audio/<work>/<id>.mp3`, byte-verified
  (1193/1193). Public URL not yet enabled — blocker for trimming git.
- Highlight fidelity note: videos are cumulative (a syllable stays lit
  once its onset passes; `t_off` unused for display). The site engine
  un-lights at `t_off`, so a sustained final syllable goes dark early.
  Open design decision.

## Recitation targets — what is actually recitable

Filter that matters: **is the text a hymn (stotra/kārikā/stava) or a
treatise?** Treatises and commentaries are never audio targets, no matter
how famous.

### Yes — recitable, source pending

| Work | Author | Size | Text | Note |
|---|---|---|---|---|
| **Anuttaraśataka** | Abhinavagupta | 100 vv | need source | ipvv: `category: stotra`. HIGH — the big one left |
| **Prakaraṇastotra** | Abhinavagupta | ? | need source | stotra; HIGH |
| **Paramārthasaṃgraha** | Abhinavagupta | ? | need source | MED |
| **Tantravaṭadhānikā** | Abhinavagupta | verse | need source | MED — "Seed of Tantra" |
| **Tattvādhvaprakāśikā** | Abhinavagupta | ? | need source | MED |
| **Sixteen Amṛtas** | ? | 16 vv | Wisdom appendix | unknown category — confirm before promising |

### No — NOT recitation texts (removed from chant queue)

| Work | Why not |
|---|---|
| **Spandasandoha** | ipvv: `category: spanda`. Kṣemarāja's prose treatise, ~81 verse markers embedded in dense commentary. Root kārikās already done as Spandakārikā. STUDY. |
| **Spandanirṇaya** | commentary on 53 kārikās. STUDY. |
| **Śivasūtravimarśinī** | commentary on 77 sūtras. STUDY. |
| **IPK** | 4 adhikāras of dense Pratyabhijñā argument. STUDY. |
| **Venisamhara** | drama in 6 acts. Not chant. |
| Śivastotrāvalī 2–20 | recitable but SING material — done as source audio, not chant. |

**Next action:** source Anuttaraśataka (100 vv, stotra). Then Sixteen Amṛtas
needs its category confirmed from the Wisdom appendix before any work.

## Delivery rules

- **CHANT** = mantra-recitation, Vagdhenu syllable pipeline.
- **SING** = melodic bhakti — recitable lyrics, sung not chanted.
- **STUDY** = treatises, commentaries — never audio targets.
- Sanskrit-only cards are complete deliverables; English is an enhancement.
  **Never** block a card on translation.

## Pipeline state (see PROCESS.md for laws)

- Render: v8–v17 + session 2026-11-01, 769 chant clips, 0 env failures.
  Env law: numpy 2.2.x, IndicF5 pinned to live HEAD, verify cell RAISES.
- Align: word MMS → syllable MMS authority → matra rhythm. Means 0.87–0.94.
- Cards: stills-first law, per-frame overflow guard, LEAD=0.28 locked.
  `--no-en` (centred, deva 84 / roman 40) is the shipped layout;
  `--no-en-small` (70/33) auto-fallback for dense padas.
- Fulls: gap 1.05 / pale 0.28 target. Long natural speech tails push gap
  past target on some joins — pale is the invariant that matters.
- Storage: R2 backup + R2 finals + opencode2 volume (`publish_r2.sh`).
  Per-clip mp4s and stills live on `r2:kashaudio-backup/cards-noen-*` and
  the volume; local copies pruned after byte verification.
- Disk law: purge `*.f32` after align, `_join_tmp` after fulls.
- Translations: 286/769 done. 483 pending — prx0r/ipvv lane.
