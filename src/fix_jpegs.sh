#!/bin/bash

INPUT_DIR="."
OUTPUT_DIR="./fixed"

mkdir -p "$OUTPUT_DIR"

for img in *.jpg *.jpeg; do
    [ -e "$img" ] || continue  # skip if no matching files
    echo "Fixing: $img"
    magick "$img" -strip -interlace JPEG -quality 95 "$OUTPUT_DIR/$img"
done

echo "Done! Fixed images saved in: $OUTPUT_DIR"
