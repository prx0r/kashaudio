# Handover — chant fulls to YouTube + next work (2026-11-01 evening)

## Where everything stands

Audio lane (`kashmir_audio`): 30 works, 1219 wavs/clips, 44046 syls, registry clean.
All 28 chant fulls exist locally in `cards/*_full.mp4` and byte-identical on
R2 `ets/finals-20261101-noen` (28/28 match, zero missing). Per-clip: 253 local
(first 10 works) all present on R2; 508 newer per-clip live only on R2
`kashaudio-backup/cards-noen-20261101-noen` (local pruned by design).

Reader lane (`/tmp/svread`, `svread.pages.dev`): 9 works at 90–100% syllable
sweep via compiled `align/*.json` + `baseline.json` ratchet, validator shipped
as `ac866f8`. 11 works blocked by evidence gate (site verse text ≠ chanted
text — data-lane fix, not matcher). Rest translation-only, correctly reported
as no-chant.

Site lane (`/tmp/ipvv`): 47 recite pages live, all mp3s on R2, cumulative
highlight matching video cards.

Kaggle: token in `~/.kaggle/access_token` (600), `vagdhenu-chant-gpu` COMPLETE.

## YouTube — done today

Studio pack: `/tmp/ytpack/studio/` — 28 mp4s renamed in English
(`01 Hymn to Bhairava.mp4` … `28 Aphorisms of Śiva.mp4`), 28 thumbnails
(1280×720, white, red rule, Devanagari + IAST only, zero English — owner
correction applied), `TITLES.txt` (English-first titles ≤100ch) +
`upload-sheet.json` (titles/descriptions/tags). Title map:
`/tmp/ytpack/titles.json`. Thumb builder: `/tmp/ytpack/make_thumbs.py`
(needs `/tmp/ytmcp` venv for PIL).

Shipped link (public R2, verified 200, 199MB):
https://pub-87169194562a44fcb8279a799d626c62.r2.dev/ytpack/ytpack-studio.zip
Owner is manual-uploading from this. No API upload has happened.

Direct uploader ready but UNUSED: `/tmp/ytpack/upload.py` (resumable 8MB
chunks, unlisted default, receipts to `upload-log.json`, deps in `/tmp/ytmcp`
venv). `--auth-status` correctly returns AUTH MISSING. Needs trio at
`/tmp/ytpack/.yt-auth.json` (600) `{client_id, client_secret, refresh_token}`.

## To get the trio (one human click, in owner's Cloud Shell, project deft-condition-510214-s7)

```
gcloud services enable youtube.googleapis.com
# Console → Auth Platform Clients → Desktop app `chant-upload` → download JSON to ~/client-id-file.json
gcloud auth application-default login --client-id-file="$HOME/client-id-file.json" --scopes="https://www.googleapis.com/auth/youtube.upload,https://www.googleapis.com/auth/youtube"
cat ~/.config/gcloud/application_default_credentials.json
```
Paste client_id/secret/refresh_token here → write `.yt-auth.json` →
`upload.py --auth-status` must print AUTH OK → flip Audience to In production
(removes 7-day testing expiry) → upload unlisted 5–6/day (1600 quota units
each, 10k/day default, reset midnight Pacific).

Dead ends learned: `youtube-connector-mcp` PyPI package is read-only +
broken entrypoint (do not retry); `pauling-ai/youtube-mcp-server` not
installed (unneeded — direct script covers it); gcloud SDK NOT installed on
this box (disk 99%, only 1.6G free — do not apt-install without pruning);
service accounts CANNOT upload to YouTube (`youtubeSignupRequired`); Internal
user type BLOCKS Brand Accounts (channels) — must be External + Production.

## Next todos, in order

1. **YouTube follow-through.** Once trio lands: test one unlisted upload
   (shortest: `saktavijnana` 2.2MB), verify thumbnail + description render,
   then 5/day in numeric order. Record video IDs in `upload-log.json`.
   Quota extension via audit form only if owner wants faster than 6/day.
2. **Parapravesika re-render.** Only work not truly done: 11 clips rendered
   from pre-fix shard, impossible ~7 syl/s on 4 clips. Re-render from current
   `stotras/parapravesika.json` (~5 min GPU on existing kernel), align,
   rebuild cards + full, re-upload that single video + refresh studio zip.
3. **Evidence-gate 11.** `ajadapramatrsiddhi, bodhavilasa, isvarasiddhi,
   kramastotra, phrdaya, ptvmadhyama, saktavijnana, sambandhasiddhi,
   sivasutra, spanda, svabodhasiddhi` — verse field must equal root verse
   only (commentary prose leaking in, e.g. sambandhasiddhi 1151 unmatched
   words). Fix in ipvv lane, then `build_align.py` compiles immediately.
4. **Tongue diagram prototype.** Agreed path: pose swap on same `tickAU`
   clock in `/tmp/svread/app.js`, stills from CC0 Wright/McCloy sagittals
   first, fluid SVG rig after. Phoneme→pose map ~15 rows; anusvara/visarga =
   hold-previous; retroflex needs real poses. Gate like everything else.
5. **Shivastotravali 2–20 per-stotra fulls.** 19 fulls per CATALOG, likely
   only on opencode2 volume — confirm location, back up to R2 if missing.

## Secrets hygiene

API key the owner pasted (`AIza…`) is read-only, exposed in chat — rotate
when convenient, restrict to YouTube Data API v3. OAuth trio must never touch
git. Owner's Cloud Shell project: `deft-condition-510214-s7`. R2 public base:
`https://pub-87169194562a44fcb8279a799d626c62.r2.dev`.
