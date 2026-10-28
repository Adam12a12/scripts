#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $(basename "$0") <input.webm>" >&2
  exit 1
}

[[ $# -ne 1 ]] && usage
[[ $1 == -h || $1 == --help ]] && usage

input=$1
output="${input%.*}.mp4"

[[ -f $input ]] || { echo "Input not found: $input" >&2; exit 1; }

count=1
while [[ -e $output ]]; do
  ((count++))
  output="${input%.*}-${count}.mp4"
  exit 1
done

echo "Processing:  $input"
echo "Writing to: $output"

ffmpeg -hide_banner -i "$input" -c:v libx264 -preset veryfast -crf 20 -c:a aac -b:a 128k -movflags +faststart "$output"

echo "Done: $output"
