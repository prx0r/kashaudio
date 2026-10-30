#!/usr/bin/env bash
# Render cards for the three new works; frame dirs deleted per text (disk law).
set -e
cd /home/ubuntu
render_dir() {
  local dir=$1
  local ids
  ids=$(python3 -c "
import json
for c in json.load(open('/home/ubuntu/kashmir_audio/$dir/word_timings.json')):
    print(c['id'])")
  local n=0
  for id in $ids; do
    python3 kashmir_audio/make_card.py "$id" "$dir" --render
    n=$((n+1))
  done
  rm -rf /home/ubuntu/kashmir_audio/cards/*_frames
  echo "== $dir: $n cards done, frames cleaned =="
}
for d in "$@"; do render_dir "$d"; done
echo ALL_REQUESTED_DONE
ls /home/ubuntu/kashmir_audio/cards/*.mp4 | wc -l
