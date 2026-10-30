# Kashmir Shaiva chant collection — status (2026-10-30)

## Done (AI + cards pipeline proven end-to-end)

| Text | Verses | AI chant | Cards | Trad audio |
|---|---|---|---|---|
| Bhairavastava (+phala) | 10 | 10/10 wav ✅ | 1/10 (bhairava_01) | Dyczkowski recitation (browser) + YT (user pulls) |
| Anuttarāṣṭikā | 8 | 8/8 wav ✅ | 0/8 | 14min chant+talk ✅ `ref/anuttarashtika-trad.mp3` |
| Śivastotrāvalī 1.1 | 1 (test) | demo spot ✅ | — (user has better audio) | user-sourced |

## Targets (in batch order)

| # | Text | Verses | Metre | Text src | Trad audio | State |
|---|---|---|---|---|---|---|
| 1 | Stavacintāmaṇi (Bhaṭṭa Nārāyaṇa) | ~120 | anuṣṭubh | GRETIL ✅ | Lakshmanjoo 6h, $0 checkout (user) | TODO shard → v9 kernel |
| 2 | Dehasthadevatācakra (anon Krama) | 16 | mixed/anuṣṭubh-ish | SanskritDocs ✅ | 53s sample ✅, full = $24 set | TODO shard → v9 kernel |
| 3 | Bodhapañcadaśikā | 15 | anuṣṭubh-ish | GRETIL ✅ | YT Ishaivite (user pulls) | TODO shard → v9 kernel |
| 4 | Kramastotra | 29+dating | śikharinī/mālinī/śārdūla/vasanta | GRETIL ✅ | none (Dyczkowski vol = user's) | TODO, long-metre tolerance test |

## Quotas / limits to respect

- Kaggle GPU: 30h/week. Used ~4h so far (v1–v8). Stavacintāmaṇi 120 verses ≈ 3h — fits.
- Demo API: 10 chants/day/IP. Spent 1. Reserve for spot checks only.
- tmpfiles/gofile links expire — Kaggle dataset is the permanent home.
- Traditional recordings are study/reference only, not for redistribution.
