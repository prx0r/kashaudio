#!/usr/bin/env python3
"""Canonical karaoke card — ONE word per line; each Devanagari syllable with
its romanization directly beneath (ruby). Matra-rhythm timing (MMS +
tts_weight). Per-slide type sizing (big when few words, shrink to fit when
many). Sanskrit centered/lower, English full-width near bottom.
One pada per slide. Usage: python3 make_card.py bhairava_01
"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
LIGHT, INK, INK50, FADE, FADE50 = (255, 255, 255), (23, 20, 15), (118, 115, 110), (207, 201, 190), (216, 210, 198)
FD = "/home/ubuntu/.fonts/TiroDevanagariSanskrit-Regular.ttf"
FR = "/home/ubuntu/.fonts/CormorantGaramond-Italic.ttf"
FE = "/home/ubuntu/.fonts/CormorantGaramond-Medium.ttf"
AUD = Path("/home/ubuntu/kashmir_audio")
OUT = AUD / "cards"
TOP, BOT = 150, 850
EN_Y, EN_W = 878, W - 360

def main():
    id_ = sys.argv[1] if len(sys.argv) > 1 else "bhairava_01"
    textdir = sys.argv[2] if len(sys.argv) > 2 else (
        "bhairavastava" if id_.startswith("bhairava") else "anuttarashtika")
    wt = {c["id"]: c for c in json.load(open(AUD / textdir / "word_timings.json"))}[id_]
    en = json.load(open(AUD / "translations.json", encoding="utf-8"))[id_]
    outd = OUT / "trad" if "_trad" in textdir else OUT
    syls = wt["syls"]
    dur = wt["dur"]
    padas = sorted({s["pada"] for s in syls})

    fe = ImageFont.truetype(FE, 48)
    lh_e = int(48 * 1.4)
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

    # per-pada word groups + font size (biggest that fits)
    avail = BOT - TOP
    pdata = {}
    for p in padas:
        cur = [s for s in syls if s["pada"] == p]
        wmap, order = {}, []
        for s in cur:
            if s["word"] not in wmap:
                wmap[s["word"]] = []; order.append(s["word"])
            wmap[s["word"]].append(s)
        n = len(order)
        for ds, rs in [(96, 40), (84, 36), (74, 32), (64, 28), (56, 25), (48, 21)]:
            word_h = int(ds * 1.4) + int(rs * 1.5) + 26
            if n * word_h <= avail:
                break
        pdata[p] = dict(order=order, wmap=wmap, n=n,
                        fd=ImageFont.truetype(FD, ds), fr=ImageFont.truetype(FR, rs),
                        lh_d=int(ds * 1.4), lh_r=int(rs * 1.5), word_h=word_h)

    def ctext(d, s, ft, y, fill=INK, cx=W / 2):
        d.text((cx - ft.getlength(s) / 2, y), s, font=ft, fill=fill)

    def slide(t):
        api = 0
        for p in padas:
            first = next(s for s in syls if s["pada"] == p)
            if first["t_on"] <= t:
                api = p
        P = pdata[api]
        n, word_h = P["n"], P["word_h"]
        y0 = TOP + (avail - n * word_h) / 2
        im = Image.new("RGB", (W, H), LIGHT)
        d = ImageDraw.Draw(im)
        lit = []
        y = y0
        for wtext in P["order"]:
            wsyls = P["wmap"][wtext]
            fd, fr, lh_d = P["fd"], P["fr"], P["lh_d"]
            dw = [tmp.textlength(s["d"], font=fd) for s in wsyls]
            rw = [tmp.textlength(s["r"], font=fr) for s in wsyls]
            total_w = sum(dw) + 8 * (len(wsyls) - 1)
            x0 = (W - total_w) / 2
            for i, s in enumerate(wsyls):
                on = t >= s["t_on"]
                if on:
                    lit.append(s["d"])
                cx = x0 + dw[i] / 2
                d.text((cx - dw[i] / 2, y), s["d"], font=fd, fill=INK if on else FADE)
                d.text((cx - rw[i] / 2, y + lh_d), s["r"], font=fr, fill=INK50 if on else FADE50)
                x0 += dw[i] + 8
            y += word_h
        yy = EN_Y
        for ln in en_txt:
            ctext(d, " ".join(ln), fe, yy)
            yy += lh_e
        return im, api, lit

    bounds = sorted({0.0, dur} | {s["t_on"] for s in syls})
    outd.mkdir(parents=True, exist_ok=True)
    fdir = outd / f"{id_}_frames"
    import shutil
    shutil.rmtree(fdir, ignore_errors=True); fdir.mkdir(parents=True)
    entries, idx = [], 0
    for t0, t1 in zip(bounds, bounds[1:]):
        if t1 - t0 < 1e-3:
            continue
        t = (t0 + t1) / 2
        im, api, lit = slide(t)
        print(f"t={t:6.2f} pada={api} lit={len(lit)}")
        im.save(fdir / f"{idx:06d}.png")
        entries.append((idx, t1 - t0)); idx += 1
    slide(dur - 0.2)[0].save(outd / f"{id_}_held.png")
    slide(2.0 if dur > 4 else dur * 0.3)[0].save(outd / f"{id_}_mid.png")
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
