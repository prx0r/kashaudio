#!/usr/bin/env python3
"""Generate v10 Kaggle kernel: render the next queue (109 clips).
Order: mhu + st1 first (proven anustubh path), then rhs/dvd/psl/kra.
Env cell = exact v8-proven install. Usage: python3 make_v10.py
"""
import json
from pathlib import Path

ST = Path("/home/ubuntu/kashmir_audio/stotras")
PUSH = Path("/home/ubuntu/vagdhenu-kaggle-push")

def py_literal(obj):
    s = json.dumps(obj, ensure_ascii=False)
    return s.replace("false", "False").replace("true", "True").replace("null", "None")

works = [
    ("mahopadeshavimshatika", "mhu", "Mahopadesha 20 (16 anustubh, clean itx)"),
    ("shivastotravali_1", "st1", "Stotra-1 rest 25 (24 anustubh)"),
    ("rahasyapanchadashika", "rhs", "Rahasya 15+colophon (long metres, OCR)"),
    ("paramadvayadvadashika", "dvd", "Dvadashika 12+phala (mixed, OCR)"),
    ("pancashloki", "psl", "Pancashloki 5 (shardula, OCR)"),
    ("kramastotra", "kra", "Kramastotra 29+dating (long metres, GRETIL TEI)"),
]

nb = {
 "cells": [
  {"cell_type": "markdown", "metadata": {}, "source": [
    "# Vagdhenu batch v10: next queue, 109 clips\n",
    "Rahasya 15+colophon, Dvadashika 12+phala, Mahopadesha 20, Pancashloki 5, Kramastotra 30, Stotra-1 rest 25.\n",
    "Settings: Accelerator=GPU (T4), Internet=ON. Est ~1.5h.\n"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [
    "!nvidia-smi | head -n 12\n", "!python3 --version\n", "!df -h /kaggle/working | tail -n 2\n"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [
    "# 1. Code\n",
    "!if [ ! -d /kaggle/working/vagdhenu ]; then git clone https://github.com/prathoshap/vagdhenu.git /kaggle/working/vagdhenu; fi\n"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [
    "# 2. Deps (exact v8-proven env law)\n",
    "!pip -q install transformers==4.46.3 accelerate==0.34.2 vocos==0.1.0 x-transformers==2.19.7 librosa==0.11.0 soundfile huggingface_hub scipy torchdiffeq einops pypinyin jieba pydub safetensors ema_pytorch cached_path click tomli tqdm transformers_stream_generator unidecode inflect hydra-core indic-transliteration\n",
    "!pip -q install --no-deps \"git+https://github.com/ai4bharat/IndicF5.git@13f7c4d627cc10111aea8fe9c0039462cacacdc7\"\n",
    "!pip -q install \"numpy==2.2.*\"\n",
    "!if [ ! -d /kaggle/working/BigVGAN ]; then git clone --depth 1 https://github.com/NVIDIA/BigVGAN.git /kaggle/working/BigVGAN; fi\n",
    "import sys\n", "sys.path.insert(0,\"/kaggle/working/BigVGAN\")\n",
    "sys.path.insert(0,\"/kaggle/working/vagdhenu/src\")\n",
    "!python3 -c \"import numpy; v=tuple(map(int, numpy.__version__.split('.')[:2])); print('numpy', numpy.__version__); assert (2,1) <= v < (2,3)\"\n",
    "!python3 -c \"from transformers import pipeline; print('pipeline ok')\"\n",
    "!python3 -c \"import torchdiffeq, librosa; print('diffeq+librosa ok')\"\n",
    "!python3 -c \"from f5_tts.infer.utils_infer import load_model; print('f5 ok')\"\n"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [
    "# 3. Weights\n",
    "!VAGDHENU_HF=prathoshap/vagdhenu python3 /kaggle/working/vagdhenu/scripts/download_weights.py\n",
    "!ls -lh /kaggle/working/vagdhenu/models/\n"]},
 ],
 "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
              "language_info": {"version": "3.10.0"}},
 "nbformat": 4, "nbformat_minor": 4,
}

# shard-write cell
src = ["# 4. Write the six shards\n", "import json\n"]
for name, _, _ in works:
    data = json.load(open(ST / f"{name}.json", encoding="utf-8"))
    src.append(f"{name} = " + py_literal(data) + "\n")
    src.append(f"json.dump({name}, open('/kaggle/working/{name}.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)\n")
src.append("print(" + "+".join(f"'{p}:'+str(len({n}))" for n, p, _ in works) + ")")
nb["cells"].append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": src})

# render cells (safe anustubh first, long-metre tolerance last)
for name, prefix, label in works:
    nb["cells"].append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [
        f"# 5. Render {label}\n",
        f"!mkdir -p /kaggle/working/out_{name}\n",
        f"!cd /kaggle/working/vagdhenu && PYTHONPATH=/kaggle/working/BigVGAN:$PYTHONPATH python3 src/render.py --shard /kaggle/working/{name}.json --results /kaggle/working/res_{name}.json --outdir /kaggle/working/out_{name}\n",
        f"!ls /kaggle/working/out_{name}/ | wc -l && cat /kaggle/working/res_{name}.json | python3 -c \"import json,sys; r=json.load(sys.stdin); print('DONE', sum(1 for x in r if 'error' not in x), '/', len(r))\"\n"]})

nb["cells"].append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [
    "# 6. Verify (RAISES on failure — never ship a false-COMPLETE again)\n",
    "import json, pathlib\n",
    "expected = {'mahopadeshavimshatika': 20, 'shivastotravali_1': 25, 'rahasyapanchadashika': 16, 'paramadvayadvadashika': 13, 'pancashloki': 5, 'kramastotra': 30}\n",
    "for name, n in expected.items():\n",
    "    r = json.load(open(f'/kaggle/working/res_{name}.json', encoding='utf-8'))\n",
    "    errs = [x for x in r if 'error' in x]\n",
    "    wavs = list(pathlib.Path(f'/kaggle/working/out_{name}').glob('*.wav'))\n",
    "    print(f'{name}: {len(r)}/{n} results, {len(errs)} errors, {len(wavs)} wavs')\n",
    "    assert len(r) == n and not errs and len(wavs) == n, f'FAILED: {name}'\n",
    "print('V10_ALL_OK')\n"]})

json.dump(nb, open(PUSH / "vagdhenu-chant-gpu.ipynb", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote v10 notebook,", len(nb["cells"]), "cells")
