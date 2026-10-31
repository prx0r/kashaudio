#!/usr/bin/env bash
# R2 publish: backup working tree + ship final fulls. Repeatable, no Kaggle needed.
# Usage: bash publish_r2.sh [label]   (default label = today YYYYMMDD)
# Requires: rclone remote `r2` (Cloudflare R2, see ~/.config/rclone/rclone.conf)
set -e
LABEL=${1:-$(date +%Y%m%d)}
AUD=/home/ubuntu/kashmir_audio

echo "== backup working tree -> r2:kashaudio-backup/kashmir_audio-$LABEL =="
rclone sync "$AUD" "r2:kashaudio-backup/kashmir_audio-$LABEL" \
  --exclude ".git/**" --exclude "__pycache__/**" --exclude "*_frames/**" \
  --exclude "*.f32" --exclude "node_modules/**" -v 2>&1 | tail -n 5

echo "== finals -> r2:ets/finals-$LABEL =="
rclone copy "$AUD/cards/" "r2:ets/finals-$LABEL/" --include "*_full.mp4" -v 2>&1 | tail -n 5

echo "== verify =="
rclone ls "r2:ets/finals-$LABEL/" 2>&1
echo "--- local sizes (bytes) ---"
ls -l "$AUD"/cards/*_full.mp4 | awk '{print $5, $9}'
echo "PUBLISH_R2_DONE label=$LABEL"
