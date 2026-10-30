import json
bhai = json.load(open('/home/ubuntu/stotras/bhairavastava.json', encoding='utf-8'))
anut = json.load(open('/home/ubuntu/stotras/anuttarashtika.json', encoding='utf-8'))
shiv = json.load(open('/home/ubuntu/stotras/shivastotravali_1_1.json', encoding='utf-8'))
kashmir = bhai + anut  # 10 + 8 = 18 (Shivastotravali excluded per owner)
for c in kashmir:
    c['out'] = 'out/' + c['id'] + '.wav'

nb = {
 "cells": [
  {"cell_type": "markdown", "metadata": {}, "source": ["# Vagdhenu Kashmir Shaiva set (GPU) v8\n", "Bhairavastava 10 (9+phala) + Anuttarashtika 8 = 18 clips.\n", "Env: numpy 2.2.x + FULL f5 infer deps (pypinyin/jieba/pydub/safetensors/ema_pytorch/...); IndicF5 --no-deps.\n", "Settings: Accelerator=GPU (T4 x2), Internet=ON."]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": ["!nvidia-smi\n", "!python3 --version\n", "!df -h /kaggle/working | tail -n 5"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": ["# 1. Code\n", "!if [ ! -d /kaggle/working/vagdhenu ]; then git clone https://github.com/prathoshap/vagdhenu.git /kaggle/working/vagdhenu; fi\n", "!ls /kaggle/working/vagdhenu/src/"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": ["# 2. Deps (run FIRST while internet available)\n", "# numpy 2.2.x: jax needs >=2.1, numba (via librosa) needs <2.3. Installed LAST so nothing downgrades it.\n", "# IndicF5 --no-deps (its numpy<=1.26 pin breaks Kaggle jax); all f5 infer deps installed explicitly\n", "# (full list from IndicF5 setup.py + utils_infer.py imports; minus torch/datasets/wandb).\n", "!pip -q install transformers==4.46.3 accelerate==0.34.2 vocos==0.1.0 x-transformers==2.19.7 librosa==0.11.0 soundfile huggingface_hub indic-transliteration scipy torchdiffeq einops pypinyin jieba pydub safetensors ema_pytorch cached_path click tomli tqdm transformers_stream_generator unidecode inflect hydra-core\n", "!pip -q install --no-deps \"git+https://github.com/ai4bharat/IndicF5.git@13f7c4d627cc10111aea8fe9c0039462cacacdc7\"\n", "!pip -q install \"numpy==2.2.*\"\n", "!if [ ! -d /kaggle/working/BigVGAN ]; then git clone --depth 1 https://github.com/NVIDIA/BigVGAN.git /kaggle/working/BigVGAN; fi\n", "import sys\n", "sys.path.insert(0,\"/kaggle/working/BigVGAN\")\n", "sys.path.insert(0,\"/kaggle/working/vagdhenu/src\")\n", "!python3 -c \"import numpy; v=tuple(map(int, numpy.__version__.split('.')[:2])); print('numpy', numpy.__version__); assert (2,1) <= v < (2,3), 'need numpy 2.1-2.2'\"\n", "!python3 -c \"from transformers import pipeline; print('pipeline ok')\"\n", "!python3 -c \"import torchdiffeq, librosa; print('diffeq+librosa ok')\"\n", "!python3 -c \"from f5_tts.infer.utils_infer import load_model; print('f5 ok')\"\n"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": ["# 3. Weights\n", "!VAGDHENU_HF=prathoshap/vagdhenu python3 /kaggle/working/vagdhenu/scripts/download_weights.py\n", "!ls -lh /kaggle/working/vagdhenu/models/ 2>/dev/null || find /kaggle/working -maxdepth 4 -name \"*.pt\" -exec ls -lh {} \\;"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": ["# placeholder"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": ["# placeholder test"]},
 ],
 "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3.10.0"}},
 "nbformat": 4, "nbformat_minor": 4
}

def py_literal(obj):
    # json.dumps gives true/false/null - Python needs True/False/None
    s = json.dumps(obj, ensure_ascii=False)
    return s.replace('false', 'False').replace('true', 'True').replace('null', 'None')

kashmir_src = "kashmir = " + py_literal(kashmir) + "\n"
nb["cells"][5]["source"] = [
    "# 4. Write shards (all 18 + per-text)\n",
    "import json\n",
    kashmir_src,
    "bhai = [c for c in kashmir if c['id'].startswith('bhairava')]\n",
    "anut = [c for c in kashmir if c['id'].startswith('anuttara')]\n",
    "json.dump(kashmir, open('/kaggle/working/kashmir.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)\n",
    "json.dump(bhai, open('/kaggle/working/bhairavastava.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)\n",
    "json.dump(anut, open('/kaggle/working/anuttarashtika.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)\n",
    "print('bhairava', len(bhai), '| anuttara', len(anut))\n",
]
nb["cells"][6]["source"] = [
    "# 5a. Bhairavastava 10 (9 + phala)\n",
    "!mkdir -p /kaggle/working/out_bhairava && cd /kaggle/working/vagdhenu && PYTHONPATH=/kaggle/working/BigVGAN:$PYTHONPATH python3 src/render.py --shard /kaggle/working/bhairavastava.json --results /kaggle/working/res_bhairava.json --outdir /kaggle/working/out_bhairava\n",
    "!ls -lh /kaggle/working/out_bhairava/ && cat /kaggle/working/res_bhairava.json",
]
nb["cells"].append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [
    "# 5b. Anuttarashtika 8\n",
    "!mkdir -p /kaggle/working/out_anuttara && cd /kaggle/working/vagdhenu && PYTHONPATH=/kaggle/working/BigVGAN:$PYTHONPATH python3 src/render.py --shard /kaggle/working/anuttarashtika.json --results /kaggle/working/res_anuttara.json --outdir /kaggle/working/out_anuttara\n",
    "!ls -lh /kaggle/working/out_anuttara/ && cat /kaggle/working/res_anuttara.json",
]})
nb["cells"].append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [
    "# 6. Listen\n",
    "from IPython.display import Audio\n",
    "import glob\n",
    "wavs=sorted(glob.glob('/kaggle/working/out_bhairava/*.wav')+glob.glob('/kaggle/working/out_anuttara/*.wav'))\n",
    "print(len(wavs), 'wavs')\n",
    "Audio(wavs[0]) if wavs else print('no wav yet')",
]})
json.dump(nb, open('/home/ubuntu/vagdhenu-kaggle-push/vagdhenu-chant-gpu.ipynb', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote v4 notebook, cells:', len(nb['cells']))
