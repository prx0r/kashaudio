#!/usr/bin/env python3
"""APPROVED layout restored (owner: "OMG ITS PERFECT" 2026-10-30): ruby-syllable
karaoke — each Devanagari syllable with its romanization directly underneath,
pairs flow left-to-right in centered rows. One pada per slide. Hard cuts at
syllable onsets. Matra-rhythm timing from MMS word_timings.json.

Tweaks staged for still-approval (owner asks): Sanskrit block lowered/central,
Sanskrit +1 size, English 1 step nearer bottom BUT hard-clamped inside frame
(never off-page). English size unchanged from approved version.

STILLS ONLY by default: python3 make_card.py <id> [textdir] [--stills]
  --stills (or default when arg missing? no: explicit) -> PNGs only, no ffmpeg.
Render: ... <id> [textdir] --render
"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

W, H = 1920, 1080
LIGHT, INK, INK50, FADE, FADE50 = (255, 255, 255), (23, 20, 15), (118, 115, 110), (207, 201, 190), (216, 210, 198)
FD = "/home/ubuntu/.fonts/TiroDevanagariSanskrit-Regular.ttf"
FR = "/home/ubuntu/.fonts/CormorantGaramond-Italic.ttf"
FE = "/home/ubuntu/.fonts/CormorantGaramond-Medium.ttf"
AUD = Path("/home/ubuntu/kashmir_audio")
OUT = AUD / "cards"
EN_Y = 790        # English base, 1 step lower than approved 760
EN_W = W - 400
GAP = 34          # gap between ruby syllable pairs
SK_TOP, SK_SPAN = 90, 670   # Sanskrit block centers within [90, 760]
LEAD = 0.28       # transition pattern: new page cuts in 0.28s BEFORE its first
                  # syllable's voice beat (page pale -> word lights ON the beat)

def bounds_check(im, tag):
    """Mistake-log rule: no dark pixels may touch frame edges."""
    g = np.array(im.convert("L"))
    ys = np.where((g < 150).any(axis=1))[0]
    xs = np.where((g < 150).any(axis=0))[0]
    ok = ys.max() < H - 8 and xs.min() > 8 and xs.max() < W - 8
    print(f"  bounds[{tag}]: y {ys.min()}-{ys.max()} x {xs.min()}-{xs.max()} -> {'OK' if ok else 'OVERFLOW!'}")
    return ok

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    do_render = "--render" in sys.argv
    id_ = args[0] if args else "bhairava_01"
    textdir = args[1] if len(args) > 1 else (
        "bhairavastava" if id_.startswith("bhairava") else "anuttarashtika")
    wt = {c["id"]: c for c in json.load(open(AUD / textdir / "word_timings.json"))}[id_]
    en = json.load(open(AUD / "translations.json", encoding="utf-8"))[id_]
    syls = wt["syls"]
    dur = wt["dur"]
    padas = sorted({s["pada"] for s in syls})

    # approved sizes, Sanskrit +1: deva 64->70, roman 30->33, English unchanged 46
    fd, fr, fe = ImageFont.truetype(FD, 70), ImageFont.truetype(FR, 33), ImageFont.truetype(FE, 46)
    lh_d, lh_r, lh_e = int(70 * 1.35), int(33 * 1.35), int(46 * 1.4)
    tmp = ImageDraw.Draw(Image.new("RGB", (W, H)))
    enw, en_lines, cur, curw = en.split(), [], [], 0
    sp = tmp.textlength(" ", font=fe)
    for i, w in enumerate(enw):
        ww = tmp.textlength(w, font=fe)
        if cur and curw + sp + ww > EN_W:
            en_lines.append(cur); cur, curw = [], 0
        if cur:
            curw += sp
        cur.append(i); curw += ww
    if cur:
        en_lines.append(cur)
    en_txt = [" ".join(enw[i] for i in ln) for ln in en_lines]
    # HARD CLAMP: English block bottom never crosses H-36 (mistake-log rule)
    en_h = len(en_txt) * lh_e
    en_y = min(EN_Y, H - en_h - 36)
    assert en_y >= 700, f"English block too tall for frame: {en_h}px (id={id_})"

    # ── transition pattern: page cuts in LEAD before its first voice beat,
    # so every page boundary is identical: new page PALE -> word ON at beat.
    firsts = {p: next(s for s in syls if s["pada"] == p)["t_on"] for p in padas}
    switches = {p: max(0.0, firsts[p] - LEAD) for p in padas}
    print(f"[{id_}] rhythm pattern ({len(padas)} pages, lead={LEAD}s):")
    for i in range(1, len(padas)):
        pp, np_ = padas[i - 1], padas[i]
        prev_end = max(s["t_off"] for s in syls if s["pada"] == pp)
        warn = "  !!PREV STILL LIT AT CUT" if prev_end > switches[np_] else ""
        print(f"  p{pp}->p{np_}: cut@{switches[np_]:.2f} | pale->lit beat {firsts[np_]:.2f}"
              f" | prev ends {prev_end:.2f}{warn}")

    def ctext(d, s, ft, y, fill=INK):
        d.text(((W - ft.getlength(s)) / 2, y), s, font=ft, fill=fill)

    def pair_w(s):
        return max(tmp.textlength(s["d"], font=fd), tmp.textlength(s["r"], font=fr))

    def slide(t):
        api = padas[0]
        for p in padas:
            if switches[p] <= t:
                api = p
        cur_s = [s for s in syls if s["pada"] == api]
        rows, row, roww = [], [], 0
        for s in cur_s:
            w = pair_w(s) + GAP
            if row and roww + w - GAP > 1500:
                rows.append(row); row, roww = [], 0
            row.append(s); roww += w
        if row:
            rows.append(row)
        block_h = len(rows) * (lh_d + lh_r + 26) - 26
        y0 = SK_TOP + (SK_SPAN - block_h) / 2
        im = Image.new("RGB", (W, H), LIGHT)
        d = ImageDraw.Draw(im)
        lit = []
        y = y0
        for r in rows:
            total = sum(pair_w(s) + GAP for s in r) - GAP
            x = (W - total) / 2
            for s in r:
                on = t >= s["t_on"]
                if on:
                    lit.append(s["d"])
                dw = tmp.textlength(s["d"], font=fd)
                rw = tmp.textlength(s["r"], font=fr)
                d.text((x + (pair_w(s) - dw) / 2, y), s["d"], font=fd, fill=INK if on else FADE)
                d.text((x + (pair_w(s) - rw) / 2, y + lh_d), s["r"], font=fr,
                       fill=INK50 if on else FADE50)
                x += pair_w(s) + GAP
            y += lh_d + lh_r + 26
        yy = en_y
        for ln in en_txt:
            ctext(d, ln, fe, yy)
            yy += lh_e
        return im, api, lit

    # ── STILLS (default): mid + held, bounds-checked, NO video ──
    outd = OUT / "trad" if "_trad" in textdir else OUT
    outd.mkdir(parents=True, exist_ok=True)
    still_t = [(f"{id_}_mid", dur * 0.4), (f"{id_}_held", dur - 0.2)]
    allok = True
    for tag, t in still_t:
        im, api, lit = slide(t)
        im.save(outd / f"{tag}.png")
        allok &= bounds_check(im, tag)
    # ── STORYBOARD (transitions reviewed before any render) ──
    if "--storyboard" in sys.argv and not do_render:
        cells = []
        for i in range(1, len(padas)):
            pp, np_ = padas[i - 1], padas[i]
            sw, fo = switches[np_], firsts[np_]
            cells.append((f"t={sw-0.06:.2f} cut-0.06 · p{pp} FULL LIT", sw - 0.06))
            cells.append((f"t={sw+0.06:.2f} cut+0.06 · p{np_} PALE (page in)", sw + 0.06))
            cells.append((f"t={fo+0.10:.2f} beat+0.10 · p{np_} 1st word LIT", fo + 0.10))
        cells.append((f"t={dur*0.4:.2f} reference · mid-frame", dur * 0.4))
        try:
            capf = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 19)
        except OSError:
            capf = ImageFont.load_default()
        cw, chh, cap, cols = 640, 360, 30, 3
        rn = (len(cells) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * cw, rn * (chh + cap)), (250, 250, 250))
        dr = ImageDraw.Draw(sheet)
        allok = True
        for k, (label, t) in enumerate(cells):
            im, _, _ = slide(t)
            allok &= bounds_check(im, f"{id_}#{k}")
            sheet.paste(im.resize((cw, chh)), ((k % cols) * cw, (k // cols) * (chh + cap) + cap))
            dr.text(((k % cols) * cw + 8, (k // cols) * (chh + cap) + 5), label, font=capf, fill=INK)
        sp = outd / f"{id_}_storyboard.png"
        sheet.save(sp)
        print("STORYBOARD:", sp, "->", "ALL OK" if allok else "BOUNDS FAIL — DO NOT RENDER")
        if not allok:
            sys.exit(2)
        return

    if not do_render:
        print("STILLS ONLY (no video):", [str(outd / f"{t[0]}.png") for t in still_t])
        if not allok:
            sys.exit("BOUNDs FAILED — do not render")
        return

    # ── RENDER (explicit --render, only after stills approved) ──
    bounds = sorted({0.0, dur} | set(switches.values()) | {s["t_on"] for s in syls})
    fdir = outd / f"{id_}_frames"
    import shutil
    shutil.rmtree(fdir, ignore_errors=True); fdir.mkdir(parents=True)
    entries, idx = [], 0
    for t0, t1 in zip(bounds, bounds[1:]):
        if t1 - t0 < 1e-3:
            continue
        im, api, lit = slide((t0 + t1) / 2)
        g = np.array(im.convert("L"))
        ymax = int(np.where((g < 150).any(axis=1))[0].max())
        if ymax >= H - 8:
            sys.exit(f"FRAME OVERFLOW at t={t0:.2f} (ymax={ymax}) — refusing to render {id_}")
        im.save(fdir / f"{idx:06d}.png")
        entries.append((idx, t1 - t0)); idx += 1
    lines = []
    for i, du in entries:
        lines += [f"file '{fdir / f'{i:06d}.png'}'", f"duration {du:.4f}"]
    lines.append(f"file '{fdir / f'{entries[-1][0]:06d}.png'}'")
    (fdir / "concat.txt").write_text("\n".join(lines) + "\n")
    wav = AUD / textdir / f"{id_}.wav"
    mp4 = outd / f"{id_}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(fdir / "concat.txt"),
                    "-i", str(wav), "-map", "0:v", "-map", "1:a", "-vf", "fps=30,format=yuv420p",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", str(mp4)], check=True)
    print("OK:", mp4, f"({dur}s, {len(entries)} cuts)")

main()
