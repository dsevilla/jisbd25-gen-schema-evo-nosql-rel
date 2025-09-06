# Marp Slides with Jinja2 Templates

This project converts Marp slides to use Jinja2 templates while maintaining compatibility with Markdown preview. The system allows you to generate code blocks with proper Marp-compatible HTML structure using Jinja2 syntax.

## Files

- `pr.md` - The original Marp slides
- `pr_corrected.md.j2` - The Jinja2 template version (auto-generated)
- `pr_generated.md` - The final generated Markdown file (compatible with Marp)
- `code_generator.py` - Python functions for generating code blocks
- `render_template.py` - Template rendering script
- `generate_slides.py` - Script to generate slides from template
- `convert_to_template.py` - Script to convert original markdown to template
- `example_custom.md.j2` - Example showing custom syntax usage
- `requirements.txt` - Python dependencies

### Documentation Files
- `README.md` - This file - main system overview
- `AUTO_GENERATION_SETUP.md` - VS Code auto-generation configuration
- `PDF_GENERATION_GUIDE.md` - Complete PDF/PPTX/HTML generation guide
- `COMPLETE_SETUP_SUMMARY.md` - Final comprehensive summary
- `SYNTAX_HIGHLIGHTING_REQUIREMENTS.md` - Syntax highlighting specifications

### Generated Output Files
- `pr_slides.pdf` - PDF presentation
- `pr_slides.pptx` - PowerPoint presentation
- `pr_slides.html` - HTML slides

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure you have the Marp extension installed in VS Code for preview.

## Usage

### Basic Usage

Generate the slides from the template:

```bash
python generate_slides.py
```

Or use the render script directly:

```bash
python render_template.py pr.md.j2 pr.md
```

### Template Syntax

In your Jinja2 template (`pr.md.j2`), you can use the following functions to generate code blocks:

#### Basic Code Block

```jinja2
{{ generate_code_block('python', '''
import boto3
client = boto3.client('s3')
''') }}
```

This generates:
```html
<pre is="marp-pre" data-auto-scaling="downscale-only"><code class="language-python">import boto3
client = boto3.client('s3')</code></pre>
```

#### Language-Specific Shortcuts

```jinja2
{{ python_code('''
print("Hello, World!")
''') }}

{{ yaml_code('''
apiVersion: v1
kind: Service
''') }}

{{ json_code('''
{
  "name": "example",
  "version": "1.0.0"
}
''') }}

{{ bash_code('''
ls -la
cd /home/user
''') }}
```

#### Advanced Options

```jinja2
{{ generate_code_block('python', code, auto_scaling='both', additional_classes='custom-class') }}

{{ generate_highlighted_code_block('python', code, highlight_lines=[1, 3, 5]) }}

{{ generate_terminal_block('ls -la', 'total 4\ndrwxr-xr-x 2 user user 4096 Jan 1 12:00 .') }}

{{ generate_diff_block('''
- old line
+ new line
''') }}
```

## Features

- **Marp Compatibility**: Generated code blocks include proper `is="marp-pre"` and `data-auto-scaling` attributes
- **Syntax Highlighting**: Supports all languages that Marp/Prism.js supports
- **HTML Escaping**: Automatically escapes HTML special characters in code
- **Auto-scaling**: Configurable auto-scaling behavior for code blocks
- **Preview Compatibility**: The template syntax is designed to be as unobtrusive as possible for Markdown preview

## Template Functions

### `generate_code_block(language, code, auto_scaling='downscale-only', additional_classes=None)`

Generates a basic code block with Marp-compatible structure.

- `language`: Programming language for syntax highlighting
- `code`: The code content
- `auto_scaling`: Auto-scaling behavior ('downscale-only', 'both', 'disabled')
- `additional_classes`: Additional CSS classes for the code element

### `generate_highlighted_code_block(language, code, highlight_lines=None, auto_scaling='downscale-only')`

Generates a code block with specific lines highlighted.

### `generate_terminal_block(command, output='', auto_scaling='downscale-only')`

Generates a terminal session with command and output.

### `generate_diff_block(diff_content, auto_scaling='downscale-only')`

Generates a diff-formatted code block.

### Language-specific shortcuts

- `python_code(code, **kwargs)`
- `yaml_code(code, **kwargs)`
- `json_code(code, **kwargs)`
- `bash_code(code, **kwargs)`
- `javascript_code(code, **kwargs)`

## Workflow

1. Edit your slides in `pr.md.j2` using Jinja2 syntax for code blocks
2. Run `python generate_slides.py` to generate `pr.md`
3. Open `pr.md` in VS Code with Marp extension to preview
4. Present using Marp

## Extending the System

To add new code generation functions:

1. Add your function to `code_generator.py`
2. Import and register it in `render_template.py` in the `env.globals.update()` call
3. Use it in your templates with `{{ your_function(...) }}`

## Benefits

- **Separation of Content and Presentation**: Code generation logic is separate from content
- **Reusability**: Code generation functions can be reused across multiple slide decks
- **Maintainability**: Changes to code block formatting only need to be made in one place
- **Consistency**: All code blocks follow the same Marp-compatible structure
- **Extensibility**: Easy to add new code generation patterns
