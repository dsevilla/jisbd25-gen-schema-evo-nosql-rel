#!/bin/bash
# Script to generate PDF with Marp CLI Docker while handling permissions correctly

set -e

INPUT_FILE=${1:-"pr_generated.md"}
OUTPUT_FILE=${2:-"pr_slides.pdf"}

echo "📄 Generating PDF from slides using Marp CLI..."

marp --pdf --allow-local-files $INPUT_FILE --output $OUTPUT_FILE

if [ -f "$OUTPUT_FILE" ]; then
    echo "✅ PDF generated successfully: $OUTPUT_FILE"
else
    echo "❌ Failed to generate PDF"
    exit 1
fi
