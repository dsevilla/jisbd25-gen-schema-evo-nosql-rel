# Makefile for Marp Slides Generation
# This file provides convenient targets for generating slides and PDFs

# Variables
TEMPLATE_FILE = pr.md.j2
GENERATED_FILE = pr_generated.md
PDF_OUTPUT = pr_slides.pdf
PPTX_OUTPUT = pr_slides.pptx
HTML_OUTPUT = pr_slides.html

# Python command (can be overridden)
PYTHON = python3

# Default target
.PHONY: all
all: slides

# Generate markdown slides from Jinja2 template
.PHONY: slides
slides: $(GENERATED_FILE)

$(GENERATED_FILE): $(TEMPLATE_FILE) code_generator.py render_template.py generate_slides.py
	@echo "🔄 Generating slides from template..."
	$(PYTHON) generate_slides.py
	@echo "✅ Slides generated: $(GENERATED_FILE)"

# Generate PDF using Marp CLI Docker container
.PHONY: pdf
pdf: $(PDF_OUTPUT)

$(PDF_OUTPUT): $(GENERATED_FILE)
	@echo "📄 Generating PDF from slides..."
	@./generate_pdf.sh

# Generate PowerPoint presentation using Marp CLI Docker container
.PHONY: pptx
pptx: $(PPTX_OUTPUT)

$(PPTX_OUTPUT): $(GENERATED_FILE)
	@echo "📊 Generating PowerPoint from slides..."
	@./generate_pptx.sh

# Generate HTML using Marp CLI Docker container
.PHONY: html
html: $(HTML_OUTPUT)

$(HTML_OUTPUT): $(GENERATED_FILE)
	@echo "🌐 Generating HTML from slides..."
	@./generate_html.sh

# Generate all formats
.PHONY: all-formats
all-formats: slides pdf pptx html
	@echo "✅ All formats generated!"

# Watch mode - automatically regenerate on template changes
.PHONY: watch
watch:
	@echo "👀 Watching for template changes..."
	$(PYTHON) watch_template.py

# Install Python dependencies
.PHONY: install
install:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed!"


# Clean generated files
.PHONY: clean
clean:
	@echo "🧹 Cleaning generated files..."
	rm -f $(GENERATED_FILE) $(PDF_OUTPUT) $(PPTX_OUTPUT) $(HTML_OUTPUT)
	@echo "✅ Cleaned!"

# Show help
.PHONY: help
help:
	@echo "📋 Available targets:"
	@echo "  slides      - Generate markdown slides from Jinja2 template"
	@echo "  pdf         - Generate PDF using Marp CLI Docker"
	@echo "  pptx        - Generate PowerPoint using Marp CLI Docker"
	@echo "  html        - Generate HTML using Marp CLI Docker"
	@echo "  all-formats - Generate all formats (markdown, PDF, PPTX, HTML)"
	@echo "  watch       - Watch template for changes and auto-regenerate"
	@echo "  install     - Install Python dependencies"
	@echo "  clean       - Remove generated files"
	@echo "  help        - Show this help message"
	@echo ""
	@echo "📝 Usage examples:"
	@echo "  make slides    # Generate markdown slides"
	@echo "  make pdf       # Generate PDF (requires Docker)"
	@echo "  make all-formats # Generate all output formats"
	@echo "  make clean && make all-formats # Clean rebuild"

# Development targets
.PHONY: dev
dev: install slides
	@echo "🚀 Development setup complete!"

# Quick build - generate slides and PDF
.PHONY: quick
quick: slides pdf
	@echo "🚀 Quick build complete: slides + PDF generated!"
