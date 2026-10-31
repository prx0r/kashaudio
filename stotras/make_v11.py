#!/usr/bin/env python3
"""Generate v11 Kaggle kernel: render Tier 2 batch (121 clips).
Order: anb (proven sardula) -> bvl (proven anushtubh) -> bna (gadya mixed) -> ajs (gadya).
Env cell = exact v11-proven install (fixed IndicF5 pin + indic-transliteration).
Usage: python3 make_v11.py
"""
import json
from pathlib import Path

ST = Path("/home/ubuntu/kashmir_audio/stotras")
PUSH = Path("/home/ubuntu/vagdhenu-kaggle-push")

def py_literal(obj):
    s = json.dumps(obj, ensure_ascii=False)
    return s.replace("false", "False").replace("true", "True").replace("null", "None")

works = [
    ("anubhavanivedana", "anb", "Anubhavanivedana 4 (sardula, itx)"),
    ("bodhavilasa", "bvl", "Bodhavilasa 42 (40 anushtubh, GRETIL)"),
    ("bhairavanukarana", "bna", "BhairavanukaranaStotra 48 (mixed, GRETIL)"),
    ("ajadapramatrsiddhi", "ajs", "Ajadapramatrsiddhi 27 (GRETIL)"),
]

nb = {
 "cells": [
  {"cell_type": "markdown", "metadata": {}, "source": [
    "# Vagdhenu batch v11: Tier 2, 121 clips\n",
    "Anubhavanivedana 4, Bodhavilasa 42, Bhairavanukarana 48, Ajadapramatrsiddhi 27.\n",
    "Settings: Accelerator=GPU (T4), Internet=ON. Est ~3h.\n"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [
    "!nvidia-smi | head -n 12\n", "!python3 --version\n", "!df -h /kaggle/working | tail -n 2\n"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [
    "# 1. Code\n",
    "!if [ ! -d /kaggle/working/vagdhenu ]; then git clone https://github.com/prathoshap/vagdhenu.git /kaggle/working/vagdhenu; fi\n"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [
    "# 2. Deps (exact v11-proven env law)\n",
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
src = ["# 4. Write the four shards\n", "import json\n"]
for name, _, _ in works:
    data = json.load(open(ST / f"{name}.json", encoding="utf-8"))
    src.append(f"{name} = " + py_literal(data) + "\n")
    src.append(f"json.dump({name}, open('/kaggle/working/{name}.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)\n")
src.append("print(" + "+".join(f"'{p}:'+str(len({n}))" for n, p, _ in works) + ")")
nb["cells"].append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": src})

# render cells
for name, prefix, label in works:
    nb["cells"].append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [
        f"# 5. Render {label}\n",
        f"!mkdir -p /kaggle/working/out_{name}\n",
        f"!cd /kaggle/working/vagdhenu && PYTHONPATH=/kaggle/working/BigVGAN:$PYTHONPATH python3 src/render.py --shard /kaggle/working/{name}.json --results /kaggle/working/res_{name}.json --outdir /kaggle/working/out_{name}\n",
        f"!ls /kaggle/working/out_{name}/ | wc -l && cat /kaggle/working/res_{name}.json | python3 -c \"import json,sys; r=json.load(sys.stdin); print('DONE', sum(1 for x in r if 'error' not in x), '/', len(r))\"\n"]})

# verify cell (RAISES on failure)
nb["cells"].append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [
    "# 6. Verify (RAISES on failure)\n",
    "import json, pathlib\n",
    "expected = {'anubhavanivedana': 4, 'bodhavilasa': 42, 'bhairavanukarana': 48, 'ajadapramatrsiddhi': 27}\n",
    "for name, n in expected.items():\n",
    "    r = json.load(open(f'/kaggle/working/res_{name}.json', encoding='utf-8'))\n",
    "    errs = [x for x in r if 'error' in x]\n",
    "    wavs = list(pathlib.Path(f'/kaggle/working/out_{name}').glob('*.wav'))\n",
    "    print(f'{name}: {len(r)}/{n} results, {len(errs)} errors, {len(wavs)} wavs')\n",
    "    assert len(r) == n and not errs and len(wavs) == n, f'FAILED: {name}'\n",
    "print('V11_ALL_OK')\n"]})

json.dump(nb, open(PUSH / "vagdhenu-chant-gpu.ipynb", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote v11 notebook,", len(nb["cells"]), "cells")
