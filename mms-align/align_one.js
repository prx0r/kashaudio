// MMS forced-align one clip: read Devanagari words from word_timings.json,
// align against raw f32le 16k audio, print WordTiming[].
const fs = require("fs");
const { createAligner, alignNative } = require("mms-forced-align");

async function main() {
  const wtPath = process.argv[2];   // word_timings.json
  const f32Path = process.argv[3];  // raw f32le 16k mono
  const id = process.argv[4];       // clip id

  const clips = JSON.parse(fs.readFileSync(wtPath, "utf8"));
  const clip = clips.find(c => c.id === id);
  if (!clip) throw new Error("clip not found: " + id);
  const words = clip.words.map(w => w.w);   // Devanagari

  const buf = fs.readFileSync(f32Path);
  const waveform = new Float32Array(buf.buffer, buf.byteOffset, buf.byteLength / 4);

  console.error("creating aligner (fp32)...");
  const aligner = await createAligner({ quantized: false });
  console.error("aligning", words.length, "words,", (waveform.length / 16000).toFixed(2), "s...");
  const t0 = Date.now();
  const timings = await alignNative(aligner, waveform, 16000, words, "sa-IN");
  console.error("aligned in", ((Date.now() - t0) / 1000).toFixed(1), "s");

  const out = timings.map((t, i) => ({
    w: t.word,
    t_on: +t.start.toFixed(3),
    t_off: +t.end.toFixed(3),
    score: t.score !== undefined ? +t.score.toFixed(3) : undefined,
    old_on: clip.words[i]?.t_on,
  }));
  console.log(JSON.stringify(out, null, 1));
  await aligner.dispose();
}
main().catch(e => { console.error(e); process.exit(1); });
