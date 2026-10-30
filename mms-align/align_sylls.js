// Syllable-level MMS forced alignment — EXACT karaoke timing.
// Each display syllable is its own token; CTC Viterbi gives per-syllable
// boundaries against the actual audio (replaces matra estimates entirely).
// Word spans recompute from their syllables. Usage:
//   node align_sylls.js bhairavastava anuttarashtika [anuttarashtika_trad]
const fs = require("fs");
const { execSync } = require("child_process");
const { createAligner, alignNative } = require("mms-forced-align");

const AUD = "/home/ubuntu/kashmir_audio";

async function main() {
  const dirs = process.argv.slice(2);
  if (!dirs.length) { console.error("dirs required"); process.exit(1); }
  console.error("creating aligner (fp32)...");
  const aligner = await createAligner({ quantized: false });
  for (const dir of dirs) {
    const path = `${AUD}/${dir}/word_timings.json`;
    const clips = JSON.parse(fs.readFileSync(path, "utf8"));
    for (const c of clips) {
      const wav = `${AUD}/${dir}/${c.id}.wav`;
      const f32 = `/tmp/${dir}_${c.id}_syl.f32`;
      if (!fs.existsSync(f32)) {
        execSync(`ffmpeg -y -v error -i "${wav}" -ar 16000 -ac 1 -f f32le "${f32}"`);
      }
      const buf = fs.readFileSync(f32);
      const wf = new Float32Array(buf.buffer, buf.byteOffset, buf.byteLength / 4);
      const syls = [...c.syls].sort((a, b) => a.pada - b.pada || a.t_on - b.t_on);
      const toks = syls.map(s => s.d);
      const t0 = Date.now();
      const T = await alignNative(aligner, wf, 16000, toks, "sa-IN");
      let prev = 0, minScore = 1, sum = 0;
      for (let i = 0; i < syls.length; i++) {
        let a = Math.max(T[i].start, prev);
        let b = Math.min(Math.max(T[i].end, a + 0.05), c.dur);
        syls[i].t_on = +a.toFixed(3);
        syls[i].t_off = +b.toFixed(3);
        syls[i].mms = T[i].score;
        sum += T[i].score;
        if (T[i].score < minScore) minScore = T[i].score;
        prev = b;
      }
      c.syls = syls;   // word spans untouched: cards light syls only; word-level MMS stays as metadata
      const mean = sum / T.length;
      console.error(`${dir}/${c.id}: ${toks.length} syls mean=${mean.toFixed(3)} min=${minScore.toFixed(3)} ${((Date.now() - t0) / 1000).toFixed(1)}s`);
    }
    fs.writeFileSync(path, JSON.stringify(clips, null, 1));
    console.error("wrote", path);
  }
  await aligner.dispose();
  console.error("DONE");
}
main().catch(e => { console.error(e); process.exit(1); });
