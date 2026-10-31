#!/usr/bin/env bash
# Publish: backup working tree + finals to 3 targets.
#   1. R2 working tree  (rclone -> r2:kashaudio-backup)
#   2. R2 finals         (rclone -> r2:ets/finals-<label>)
#   3. opencode2 volume  (rsync -> root@2.28.50.109:/mnt/HC_Volume_106427611/patala/backup)
# Usage: bash publish_r2.sh [label]   (default label = today YYYYMMDD)
set -e
LABEL=${1:-$(date +%Y%m%d)}
AUD=/home/ubuntu/kashmir_audio
VPS="root@2.28.50.109"
VOL="/mnt/HC_Volume_106427611/patala/backup"
SSH_KEY="$HOME/.ssh/id_ed25519"

echo "== 1. backup working tree -> r2:kashaudio-backup/kashmir_audio-$LABEL =="
rclone sync "$AUD" "r2:kashaudio-backup/kashmir_audio-$LABEL" \
  --exclude ".git/**" --exclude "__pycache__/**" --exclude "*_frames/**" \
  --exclude "*.f32" --exclude "node_modules/**" -v 2>&1 | tail -n 3

echo "== 2. finals -> r2:ets/finals-$LABEL =="
rclone copy "$AUD/cards/" "r2:ets/finals-$LABEL/" --include "*_full.mp4" -v 2>&1 | tail -n 3

echo "== 3. finals -> opencode2 volume =="
rsync -az --progress -e "ssh -i $SSH_KEY -o StrictHostKeyChecking=accept-new" \
  --include="*_full.mp4" --include="*_mid.png" --include="*_held.png" \
  --include="*_storyboard.png" --exclude="*" \
  "$AUD/cards/" "$VPS:$VOL/kashmir-audio-$LABEL/" 2>&1 | tail -n 5

echo "== verify =="
echo "-- R2 finals --"
rclone ls "r2:ets/finals-$LABEL/" 2>&1
echo "-- opencode2 volume --"
ssh -i "$SSH_KEY" -o BatchMode=yes "$VPS" "ls -l $VOL/kashmir-audio-$LABEL/*_full.mp4 2>/dev/null | awk '{print \$5, \$9}'" 2>&1
echo "-- local sizes (bytes) --"
ls -l "$AUD"/cards/*_full.mp4 | awk '{print $5, $9}'
echo "PUBLISH_DONE label=$LABEL targets=[r2-backup, r2-finals, opencode2-volume]"
