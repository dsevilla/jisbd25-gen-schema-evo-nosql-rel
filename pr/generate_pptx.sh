#!/bin/bash
# Script to generate PowerPoint with Marp CLI Docker while handling permissions correctly

set -e

INPUT_FILE=${1:-"pr_generated.md"}
OUTPUT_FILE=${2:-"pr_slides.pptx"}

echo "📊 Generating PowerPoint from slides using Marp CLI..."

# Run Marp CLI Docker as root and fix permissions afterwards
marp --pptx --allow-local-files $INPUT_FILE --output $OUTPUT_FILE

if [ -f "$OUTPUT_FILE" ]; then
    echo "✅ PowerPoint generated successfully: $OUTPUT_FILE"
else
    echo "❌ Failed to generate PowerPoint"
    exit 1
fi
