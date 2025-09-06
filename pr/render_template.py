#!/usr/bin/env python3
"""
Template renderer for Marp slides.
This script processes Jinja2 templates and generates Markdown files compatible with Marp.
"""

import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template

# Import our code generation functions
from code_generator import (
    generate_code_block,
    generate_highlighted_code_block,
    generate_terminal_block,
    generate_diff_block,
    generate_mermaid_diagram,
    generate_er_diagram,
    generate_mermaid_kroki,
    generate_er_diagram_kroki,
    generate_mermaid_local_kroki,
    generate_mermaid_placeholder,
    generate_er_diagram_safe,
    python_code,
    yaml_code,
    json_code,
    bash_code,
    javascript_code
)


def render_template(template_path: str, output_path: str | None = None, **template_vars):
    """
    Render a Jinja2 template with code generation functions available.

    Args:
        template_path (str): Path to the Jinja2 template file
        output_path (str, optional): Output path for the rendered file.
                                   If None, uses template path without .j2 extension
        **template_vars: Additional variables to pass to the template
    """
    template_path_obj = Path(template_path)

    if not template_path_obj.exists():
        print(f"Error: Template file {template_path} does not exist.")
        sys.exit(1)

    # Determine output path
    if output_path is None:
        if template_path_obj.suffix == '.j2':
            output_path_obj: Path = template_path_obj.with_suffix('')
        else:
            output_path_obj: Path = template_path_obj.with_suffix(template_path_obj.suffix + '.rendered')
    else:
        output_path_obj: Path = Path(output_path)

    # Set up Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(template_path_obj.parent),
        trim_blocks=True,
        lstrip_blocks=True
    )

    # Make code generation functions available in templates
    env.globals.update({
        'generate_code_block': generate_code_block,
        'generate_highlighted_code_block': generate_highlighted_code_block,
        'generate_terminal_block': generate_terminal_block,
        'generate_diff_block': generate_diff_block,
        'generate_mermaid_diagram': generate_mermaid_diagram,
        'generate_er_diagram': generate_er_diagram,
        'generate_mermaid_kroki': generate_mermaid_kroki,
        'generate_er_diagram_kroki': generate_er_diagram_kroki,
        'generate_mermaid_local_kroki': generate_mermaid_local_kroki,
        'generate_mermaid_placeholder': generate_mermaid_placeholder,
        'generate_er_diagram_safe': generate_er_diagram_safe,
        'python_code': python_code,
        'yaml_code': yaml_code,
        'json_code': json_code,
        'bash_code': bash_code,
        'javascript_code': javascript_code,
    })

    # Load and render template
    try:
        template: Template = env.get_template(template_path_obj.name)
        rendered_content: str = template.render(**template_vars)

        # Write to output file
        with open(output_path_obj, 'w', encoding='utf-8') as f:
            f.write(rendered_content)

        print(f"Template rendered successfully: {template_path} -> {output_path_obj}")

    except Exception as e:
        print(f"Error rendering template: {e}")
        sys.exit(1)


def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python render_template.py <template_file> [output_file]")
        print("Example: python render_template.py pr.md.j2 pr.md")
        sys.exit(1)

    template_file: str = sys.argv[1]
    output_file: str | None = sys.argv[2] if len(sys.argv) > 2 else None

    render_template(template_file, output_file)


if __name__ == "__main__":
    main()
