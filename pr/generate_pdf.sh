#!/bin/bash
# Script to generate PDF with Marp CLI using Docker.
# The container is run with the host user's UID:GID so generated files
# keep correct ownership on the host filesystem.

set -euox pipefail

INPUT_FILE=${1:-"pr_generated.md"}
OUTPUT_FILE=${2:-"pr_slides.pdf"}
DOCKER_IMAGE="marpteam/marp-cli:latest"

echo "📄 Generating PDF from slides using Marp CLI (Docker image: $DOCKER_IMAGE)..."

# Ensure docker is available
if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker not found. Please install Docker or run Marp locally."
    exit 1
fi

# Use current directory as workdir inside container so relative paths work
WORKDIR_HOST="$PWD"

# Run Marp CLI in container as root and chown the output to the host user (same pattern as generate_html.sh)
docker run --rm \
    --user root \
    -v "$WORKDIR_HOST":/workspace \
    -w /workspace \
    --entrypoint sh \
    "$DOCKER_IMAGE" \
    -c "node /home/marp/.cli/marp-cli.js --pdf --allow-local-files $INPUT_FILE --output $OUTPUT_FILE && chown $(id -u):$(id -g) $OUTPUT_FILE"

if [ -f "$OUTPUT_FILE" ]; then
    echo "✅ PDF generated successfully: $OUTPUT_FILE"
else
    echo "❌ Failed to generate PDF"
    exit 1
fi
