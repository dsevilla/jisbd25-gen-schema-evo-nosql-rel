#!/bin/bash
# Script to generate PowerPoint with Marp CLI using Docker.
# The container runs with the host user's UID:GID so generated files
# keep correct ownership on the host filesystem.

set -euo pipefail

INPUT_FILE=${1:-"pr_generated.md"}
OUTPUT_FILE=${2:-"pr_slides.pptx"}
DOCKER_IMAGE="marpteam/marp-cli:latest"

echo "📊 Generating PowerPoint from slides using Marp CLI (Docker image: $DOCKER_IMAGE)..."

# Ensure docker is available
if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker not found. Please install Docker or run Marp locally."
    exit 1
fi

WORKDIR_HOST="$PWD"

docker run --rm \
    --user root \
    -v "$(pwd):/workspace" \
    -w /workspace \
    --entrypoint sh \
    "$DOCKER_IMAGE" \
    -c "node /home/marp/.cli/marp-cli.js --pptx --allow-local-files $INPUT_FILE --output $OUTPUT_FILE && chown $(id -u):$(id -g) $OUTPUT_FILE"

if [ -f "$OUTPUT_FILE" ]; then
    echo "✅ PowerPoint generated successfully: $OUTPUT_FILE"
else
    echo "❌ Failed to generate PowerPoint"
    exit 1
fi
