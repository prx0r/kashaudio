// MMS-align traditional Anuttarashtika verse segments -> word_timings.json
const fs = require("fs");
const { createAligner, alignNative } = require("mms-forced-align");

const WORK = "/home/ubuntu/kashmir_audio/anuttarashtika_trad";

async function main() {
  const verses = JSON.parse(fs.readFileSync(`${WORK}/verses.json`, "utf8"));
  console.error("creating aligner (fp32)...");
  const aligner = await createAligner({ quantized: false });
  const out = [];
  for (const v of verses) {
    const buf = fs.readFileSync(`/tmp/${v.id}_trad.f32`);
    const waveform = new Float32Array(buf.buffer, buf.byteOffset, buf.byteLength / 4);
    const t0 = Date.now();
    const timings = await alignNative(aligner, waveform, 16000, v.words, "sa-IN");
    const words = timings.map((t, i) => ({
      w: t.word,
      t_on: +t.start.toFixed(3),
      t_off: +t.end.toFixed(3),
      mms: t.score !== undefined ? +t.score.toFixed(3) : null,
      pada: v.pada_of[i],
    }));
    for (let i = 1; i < words.length; i++) {
      if (words[i].t_on < words[i - 1].t_on) words[i].t_on = words[i - 1].t_on;
    }
    const mean = (words.reduce((s, w) => s + (w.mms || 0), 0) / words.length).toFixed(3);
    const dur = waveform.length / 16000;
    console.error(`${v.id}: ${words.length} words, mean score ${mean}, align ${((Date.now() - t0) / 1000).toFixed(1)}s, dur ${dur.toFixed(1)}s, last word ends ${words[words.length - 1].t_off.toFixed(1)}`);
    out.push({ id: v.id, meter: v.meter, dur: +dur.toFixed(3), words });
  }
  fs.writeFileSync(`${WORK}/word_timings.json`, JSON.stringify(out, null, 1));
  await aligner.dispose();
  console.error("wrote", `${WORK}/word_timings.json`);
}
main().catch(e => { console.error(e); process.exit(1); });
