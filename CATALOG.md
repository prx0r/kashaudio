# Catalog — Kashmir Shaiva chant collection (2026-10-30)

Single source of truth for what's done and what's next. Supersedes the
pre-v9 snapshots in `STATUS.md` / `targets.md` (kept for history).
"Audio" = AI (Vagdhenu) is the deliverable voice; traditional recordings
are ear-references only unless the owner says otherwise.

## Completed — AI chant + karaoke cards + full recitation

| # | Text | Author | Verses | Metre | Text src | AI chant | Cards | Full recitation | Trad audio (ear-ref only) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Bhairavastava (+ phala) | Abhinavagupta | 10 | mixed, 11-syll rathoddhata bank; colophon gadya | GRETIL | 10/10 wav ✅ | 10/10 ✅ (`bhairava_*`) | `bhairavastava_full.mp4` (3,963,738 B) | Dyczkowski recitation (browser) + YT (user pulls) |
| 2 | Anuttarāṣṭikā | Abhinavagupta | 8 | long-metre, regular | GRETIL | 8/8 wav ✅ | 8/8 AI ✅ (`anuttara_*`) + 8 trad parked (`cards/trad/`) | `anuttarashtika_full.mp4` (6,093,238 B) | Lakshmanjoo 14min chant+talk → segmented to 8, MMS 0.93–0.96; `ref/anuttarashtika-trad.mp3` |
| 3 | Stavacintāmaṇi | Bhaṭṭa Nārāyaṇa | 120 | anuṣṭubh throughout | GRETIL | 120/120 wav ✅ (v9) | 120/120 ✅ (`stc_001–120`) | `stavacintamani_full.mp4` (37,260,625 B) | Lakshmanjoo 6h set (user checkout) — ref only |
| 4 | Dehasthadevatācakrastotra | anonymous Krama (Pandey prints it among Abhinavagupta's; verify from colophon) | 16 | mixed / anuṣṭubh-ish | SanskritDocs | 16/16 wav ✅ (v9) | 16/16 ✅ (`dhs_01–16`) | `dehastha_full.mp4` (5,124,299 B) | 53s sample ✅; full set = $24 (not pulled) |
| 5 | Bodhapañcadaśikā | Abhinavagupta | 15 | anuṣṭubh-ish | GRETIL | 15/15 wav ✅ (v9) | 15/15 ✅ (`bpc_01–15`) | `bodhapanadasika_full.mp4` (4,603,612 B) | YT Ishaivite (user pulls) — ref only |
| 6 | Śivastotrāvalī 1.1 (pilot) | Utpaladeva | 1 | — (pilot) | — | demo spot ✅ | — (user has better audio) | — | user-sourced |

Totals: 169 AI verses + 5 fulls (174 mp4s in `cards/`). All fulls rebuilt
2026-10-30 on the fixed join code (stale-frame bug, see PROCESS.md) and
re-scanned single-cut. Finals verified byte-identical at
`r2:ets/finals-20261030/`; working tree backed up at
`r2:kashaudio-backup/kashmir_audio-20261030/`. Gofile spot links from
earlier tonight predate the fix and are superseded.

## Canonical trio catalog — every work, with its delivery (researched 2026-10-31)

The vibe, stated plainly: CHANT is mantra-recitation — short doctrinal or
direct-address verse in regular metre, the Vagdhenu syllable pipeline as
built. SING is melodic devotional song — the Śivastotrāvalī, still sung in
Kashmir today, which deserves a singing voice in a later phase, not this
chant engine. STUDY is treatises and commentaries — never audio targets.

### Abhinavagupta — stotras (all CHANT; Pandey's appendix lists 11)

| Work | Verses | Status |
|---|---|---|
| Bhairavastava (+ phala) | 10 | DONE |
| Anuttarāṣṭikā | 8 | DONE |
| Bodhapañcadaśikā | 15 | DONE |
| Dehasthadevatācakra (attribution fn. above) | 16 | DONE |
| Rahasyapañcadaśikā | 15 + colophon (shard `rahasyapanchadashika.json`: rhs_01–16 ✅, Vol-8 PDF OCR) | NEXT — same shape as Bodhapañcadaśikā (proven); long metres like Krama family |
| Paramārthadvādaśikā | 12 + phala (shard `paramadvayadvadashika.json`: dvd_01–13 ✅, Vol-8 PDF OCR) | QUEUED — mixed śārdūla/anuṣṭubh |
| Mahopadeśaviṃśatikā | 20 (shard `mahopadeshavimshatika.json` ✅, 16 anuṣṭubh; clean itx) | QUEUED — still one GPU run |
| Pañcaślokī | 5, śārdūla (shard `pancashloki.json` ✅, Vol-8 PDF OCR) | QUEUED — 5-verse sprint after the shorts |
| Kramastotra | 29 + dating v30 (shard `kramastotra.json` ✅, GRETIL TEI) | QUEUED — long metres make it the tolerance test, after the short ones |
| Paryantapañcāśikā | 50 | Tier 2 |
| Anubhavanivedana | 4, śārdūla (shard `anubhavanivedana.json` ✅, clean itx) | Tier 2 — tiny gem, ready |
| Paramārthacarcā | count TBD — verify text | Tier 2 |

Abhinavagupta kārikā-treatise, CHANT as recitation: Paramārthasāra (105 —
the next Stavacintamani-scale capstone, jīvanmukti theme), Tier 2.
Prose/massive works (Tantrāloka, Tantrasāra, commentaries): STUDY, never
targets.

### Kṣemarāja — original works only (commentaries are STUDY, never targets)

| Work | Size | Delivery / status |
|---|---|---|
| Pratyabhijñāhṛdayam (sūtras + auto-vṛtti) | 20 sūtras (GRETIL TEI ✅) | CHANT* — the densest Trika essence ("Vedāntasāra of Trika"); FORMAT FLAG: prose sūtras, pilot 2–3 as gadya lines first |
| Parāprāveśikā | 1 aphorism + short gloss | CHANT* — tiny tattva primer; same pilot covers it |
| Bodhavilāsa | 42 anuṣṭubh (yogaśāstra; GRETIL TEI ✅) | CHANT, Tier 2 — Kṣemarāja's own short treatise, ready |
| Bhairavānukaraṇastotra | 48 mixed (GRETIL TEI ✅) | CHANT, Tier 2 — Kṣemarāja stotra, medium length |
| Tattvasandoha | verify size | Tier 2 if short |
| Spandanirṇaya (long prose), Spandasandoha, Uddyotas, Śivasūtravimarśinī, Stavacintāmaṇiṭīkā | — | STUDY — commentaries on others' texts |

### Utpaladeva — songs vs philosophy, split by delivery

| Work | Size | Delivery / status |
|---|---|---|
| Śivastotrāvalī, Stotra 1 rest (Bhaktivilāsa) | 25 (shard `shivastotravali_1.json` ✅, 24 anuṣṭubh; local full text) | SING exception — finish the pilot song now, then STOP; Stotras 2–20 wait for the singing phase |
| Śivastotrāvalī, Stotras 2–20 | 19 songs (Bailly/Rhodes translation; Kṣemarāja commented) | SING — lower priority NOW by owner rule; needs melodic voice, not chant engine |
| Siddhitrayī: Ajadapramātṛsiddhi | 27 kārikās + Vṛtti (GRETIL TEI ✅) | CHANT as recitation, Tier 2 — ready |
| Siddhitrayī: Īśvara/Sambandha-siddhis | counts TBD | CHANT as recitation, Tier 2 |
| Īśvarapratyabhijñākārikā (~199 kārikās) | foundation stone of Pratyabhijñā | STUDY — dense polemical philosophy, not chant material |
| Śivadṛṣṭivṛtti | commentary | STUDY |

### Chant run order (the actual queue)

Rahasyapañcadaśikā → Paramārthadvādaśikā → Mahopadeśaviṃśatikā →
Pañcaślokī → Kramastotra → Stotra 1 completion → Hṛdayam/Parāprāveśikā
pilot → full sūtras → Tier 2 (Paryantapañcāśikā, Anubhavanivedana,
Bodhavilāsa, Bhairavānukaraṇastotra, Ajadapramātṛsiddhi,
Paramārthacarcā, Paramārthasāra, remaining Siddhis).

Text sources IN HAND 2026-10-31: all 7 next-queue shards built and
meter-checked (`stotras/*.json` via `build_shards4.py`); GRETIL TEI for
Kramastotra/Hṛdayam/Bodhavilāsa/Bhairavānukaraṇa/Ajaḍapramātṛsiddhi.
Still to verify: Paramārthacarcā text + count, Īśvara/Sambandha-siddhis,
Tattvasandoha size. OCR-uncertain verses flagged gadya (rhs_09 l2).
Non-trio only if the well runs dry: Pañcastavī, Sāmbapañcāśikā.

## Pipeline state (see PROCESS.md for laws)

- Render: Kaggle GPU kernel v9 — 151 verses in 1h56m, 0 errors.
- Align: word MMS sa-IN → syllable MMS (authority) → matra rhythm.
- Cards: approved ruby-rows Essay-0 look, stills-first, per-frame overflow guard.
- Quota: ~6h of 30h/week Kaggle GPU used. Demo API reserved for spot checks.
