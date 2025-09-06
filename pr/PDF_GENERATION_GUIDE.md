# PDF Generation Setup for Marp Slides

You now have **two approaches** to generate PDFs and other formats from your Marp slides using Docker:

## 🔧 Approach 1: Makefile (Recommended)

### Quick Start:
```bash
# Generate slides and PDF in one command
make quick

# Or step by step:
make slides    # Generate markdown from template
make pdf       # Generate PDF using Docker
```

### All Available Targets:

| Target | Description |
|--------|-------------|
| `make slides` | Generate markdown slides from Jinja2 template |
| `make pdf` | Generate PDF using Marp CLI Docker |
| `make pptx` | Generate PowerPoint presentation |
| `make html` | Generate HTML slides |
| `make all-formats` | Generate all formats (MD, PDF, PPTX, HTML) |
| `make watch` | Watch template for changes and auto-regenerate |
| `make clean` | Remove all generated files |
| `make quick` | Quick build: slides + PDF |
| `make help` | Show all available targets |

### Example Workflow:
```bash
# Complete workflow
make clean           # Clean previous files
make all-formats     # Generate everything
ls -la *.pdf *.pptx *.html  # Check outputs

# Development workflow
make watch          # Watch for changes (Ctrl+C to stop)
```

## 🐳 Approach 2: Docker Compose

### Quick Start:
```bash
# Generate slides template first
docker-compose --profile generate up slides-generator

# Generate PDF
docker-compose --profile pdf up pdf-generator

# Generate all formats
docker-compose --profile all-formats up
```

### Available Profiles:

| Profile | Command | Description |
|---------|---------|-------------|
| `generate` | `docker-compose --profile generate up` | Generate markdown from template |
| `pdf` | `docker-compose --profile pdf up` | Generate PDF |
| `pptx` | `docker-compose --profile pptx up` | Generate PowerPoint |
| `html` | `docker-compose --profile html up` | Generate HTML |
| `all-formats` | `docker-compose --profile all-formats up` | Generate all formats |
| `watch` | `docker-compose --profile watch up` | File watcher mode |
| `dev` | `docker-compose --profile dev up` | Development server with HTTP |

### Example Workflow:
```bash
# Generate everything
docker-compose --profile all-formats up

# Development mode with file watcher
docker-compose --profile watch up

# Development server (serves files on http://localhost:8080)
docker-compose --profile dev up
```

## 📋 Comparison

| Feature | Makefile | Docker Compose |
|---------|----------|----------------|
| **Simplicity** | ⭐⭐⭐ Simple commands | ⭐⭐ More verbose |
| **Dependencies** | Docker + Make | Docker + Docker Compose |
| **File watching** | ✅ `make watch` | ✅ `--profile watch` |
| **Parallel execution** | ❌ Sequential | ✅ Can run in parallel |
| **Development server** | ❌ Not included | ✅ HTTP server included |
| **Caching** | ✅ Make dependency tracking | ⭐ Docker layer caching |

## 🚀 Recommended Usage

### For Daily Development:
```bash
# Use Makefile for simplicity
make slides    # Generate from template
make pdf       # Quick PDF generation
```

### For CI/CD or Complex Workflows:
```bash
# Use Docker Compose for containerized environments
docker-compose --profile all-formats up
```

### For Presentation Preparation:
```bash
# Generate all formats for different scenarios
make all-formats

# Files generated:
# - pr_generated.md (for VS Code preview)
# - pr_slides.pdf (for sharing/printing)
# - pr_slides.pptx (for PowerPoint editing)
# - pr_slides.html (for web presentation)
```

## 🔧 Requirements

### For Makefile:
- Docker installed and running
- Make utility (usually pre-installed on Linux/macOS)
- Python 3.x for template generation

### For Docker Compose:
- Docker installed and running
- Docker Compose (usually included with Docker Desktop)

## 📁 Generated Files

Both approaches generate the same output files:

```
pr_generated.md    # Markdown slides (Marp compatible)
pr_slides.pdf      # PDF presentation
pr_slides.pptx     # PowerPoint presentation
pr_slides.html     # HTML slides (self-contained)
```

## 🛠️ Customization

### Modify Output Names:
Edit the variables in `Makefile`:
```makefile
PDF_OUTPUT = my_custom_slides.pdf
PPTX_OUTPUT = my_custom_slides.pptx
```

### Add Custom Marp Options:
Modify the Docker commands in either `Makefile` or `docker-compose.yml`:
```bash
# Add theme or other options
docker run --rm -v $(PWD):/home/marp/app -w /home/marp/app marpteam/marp-cli:latest \
    --pdf --theme custom_theme --allow-local-files \
    pr_generated.md --output pr_slides.pdf
```

## 🎯 Integration with VS Code

The auto-generation setup works perfectly with both approaches:

1. **Edit** `pr_corrected.md.j2` in VS Code
2. **Save** → Auto-generates `pr_generated.md`
3. **Run** `make pdf` or Docker Compose to generate final outputs
4. **Preview** the PDF or other formats

The **Makefile approach** is recommended for most users due to its simplicity and integration with development workflows!
