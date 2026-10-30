#!/usr/bin/env bash
# Render all 18 AI cards (approved layout; stills already approved 2026-10-30).
set -e
cd /home/ubuntu
for c in bhairava_01 bhairava_02 bhairava_03 bhairava_04 bhairava_05 bhairava_06 bhairava_07 bhairava_08 bhairava_09 bhairava_10_phala; do
  python3 kashmir_audio/make_card.py "$c" --render
done
for c in anuttara_01 anuttara_02 anuttara_03 anuttara_04 anuttara_05 anuttara_06 anuttara_07 anuttara_08; do
  python3 kashmir_audio/make_card.py "$c" --render
done
echo "ALL 18 DONE"; ls kashmir_audio/cards/*.mp4 | wc -l
