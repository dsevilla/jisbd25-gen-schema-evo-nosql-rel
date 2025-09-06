#!/bin/bash
# Script to generate HTML with Marp CLI Docker while handling permissions correctly

set -e

INPUT_FILE="pr_generated.md"
OUTPUT_FILE="pr_slides.html"

echo "🌐 Generating HTML from slides using Marp CLI..."

# Run Marp CLI Docker as root and fix permissions afterwards
docker run --rm \
    --user root \
    -v "$(pwd):/workspace" \
    -w /workspace \
    --entrypoint sh \
    marpteam/marp-cli:latest \
    -c "node /home/marp/.cli/marp-cli.js --html --allow-local-files $INPUT_FILE --output $OUTPUT_FILE && chown $(id -u):$(id -g) $OUTPUT_FILE"

if [ -f "$OUTPUT_FILE" ]; then
    echo "✅ HTML generated successfully: $OUTPUT_FILE"
else
    echo "❌ Failed to generate HTML"
    exit 1
fi
