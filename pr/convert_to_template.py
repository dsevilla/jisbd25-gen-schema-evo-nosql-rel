#!/usr/bin/env python3
"""
Create a corrected Jinja2 template by reading the original markdown
and converting code blocks to use proper template syntax.
"""

import re
from pathlib import Path

def convert_code_blocks_to_template(content):
    """Convert standard markdown code blocks to Jinja2 template calls."""

    # Pattern to match code blocks with language specification
    pattern = r'```(\w+)\n(.*?)\n```'

    def replace_code_block(match):
        language = match.group(1)
        code = match.group(2)
        # Escape single quotes in the code
        escaped_code = code.replace("'", "\\'")
        return f"{{{{ generate_code_block('{language}', '{escaped_code}') }}}}"

    # Replace all code blocks
    converted = re.sub(pattern, replace_code_block, content, flags=re.DOTALL)
    return converted

def main():
    # Read the original markdown file
    original_file = Path('/home/dsevilla/svn/tesis/jisbd25/pr/pr.md')

    if not original_file.exists():
        print("Original pr.md file not found")
        return

    with open(original_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Convert code blocks
    converted_content = convert_code_blocks_to_template(content)

    # Write to template file
    template_file = Path('/home/dsevilla/svn/tesis/jisbd25/pr/pr_corrected.md.j2')
    with open(template_file, 'w', encoding='utf-8') as f:
        f.write(converted_content)

    print(f"Created corrected template: {template_file}")

if __name__ == "__main__":
    main()
