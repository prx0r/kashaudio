// Batch MMS-align all clips (dirs via argv). reads word_timings; word-level pass.
// NOTE: for NEW works there is no word_timings yet — use seed_word_timings first.
// Batch legacy comment: reads word_timings.json per work, resamples via
// ffmpeg, aligns with sa-IN, merges corrected t_on/t_off back into the JSON.
const fs = require("fs");
const { execSync } = require("child_process");
const { createAligner, alignNative } = require("mms-forced-align");

const AUD = "/home/ubuntu/kashmir_audio";
const WORKS = process.argv.slice(2);

async function main() {
  console.error("creating aligner (fp32)...");
  const aligner = await createAligner({ quantized: false });
  for (const work of WORKS) {
    const path = `${AUD}/${work}/word_timings.json`;
    const clips = JSON.parse(fs.readFileSync(path, "utf8"));
    for (const clip of clips) {
      const wav = `${AUD}/${work}/${clip.id}.wav`;
      const f32 = `/tmp/${clip.id}.f32`;
      execSync(`ffmpeg -y -v error -i "${wav}" -ar 16000 -ac 1 -f f32le "${f32}"`);
      const buf = fs.readFileSync(f32);
      const waveform = new Float32Array(buf.buffer, buf.byteOffset, buf.byteLength / 4);
      const words = clip.words.map(w => w.w);
      const t0 = Date.now();
      const timings = await alignNative(aligner, waveform, 16000, words, "sa-IN");
      let moved = 0;
      for (let i = 0; i < clip.words.length; i++) {
        const t = timings[i];
        const old = clip.words[i].t_on;
        clip.words[i].t_on = +t.start.toFixed(3);
        clip.words[i].t_off = +t.end.toFixed(3);
        clip.words[i].mms = t.score !== undefined ? +t.score.toFixed(3) : null;
        if (Math.abs(old - t.start) > 0.05) moved++;
      }
      // keep monotonic
      for (let i = 1; i < clip.words.length; i++) {
        if (clip.words[i].t_on < clip.words[i - 1].t_on) {
          clip.words[i].t_on = clip.words[i - 1].t_on;
        }
      }
      const avg = (clip.words.reduce((s, w) => s + (w.mms || 0), 0) / clip.words.length).toFixed(3);
      console.error(`${clip.id}: ${clip.words.length} words, ${moved} moved >50ms, mean score ${avg}, ${(Date.now() - t0) / 1000 | 0}s`);
    }
    fs.writeFileSync(path, JSON.stringify(clips, null, 1));
    console.error("wrote", path);
  }
  await aligner.dispose();
  console.error("DONE");
}
main().catch(e => { console.error(e); process.exit(1); });
