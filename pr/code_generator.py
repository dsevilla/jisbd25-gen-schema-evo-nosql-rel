"""
Code block generation functions for Marp slides using Jinja2.
This module provides functions to generate properly formatted code blocks
that are compatible with Marp's syntax highlighting and auto-scaling features.

IMPORTANT: Current implementation provides basic HTML structure.
For advanced syntax highlighting requirements (hljs-string, hljs-keyword, etc.),
see SYNTAX_HIGHLIGHTING_REQUIREMENTS.md for enhancement specifications.
"""

import html

def generate_code_block(language: str, code: str, auto_scaling: str = "downscale-only",
                       additional_classes: str | None = None) -> str:
    """
    Generate a Marp-compatible code block with proper HTML structure.

    Args:
        language (str): The programming language for syntax highlighting (e.g., 'python', 'yaml', 'json')
        code (str): The code content to be displayed
        auto_scaling (str): Auto-scaling behavior for Marp ('downscale-only', 'both', 'disabled')
        additional_classes (str, optional): Additional CSS classes to add to the code element

    Returns:
        str: HTML string with properly formatted pre and code elements for Marp
    """
    # Escape HTML special characters in the code
    escaped_code: str = html.escape(code.strip())

    # Build the class attribute for the code element
    code_classes: str = f"language-{language}"
    if additional_classes:
        code_classes += f" {additional_classes}"

    # Generate the complete HTML structure
    html_output: str = f'<pre is="marp-pre" data-auto-scaling="{auto_scaling}"><code class="{code_classes}">{escaped_code}</code></pre>'

    return html_output


def generate_highlighted_code_block(language: str, code: str, highlight_lines: list | None = None,
                                  auto_scaling: str = "downscale-only") -> str:
    """
    Generate a code block with specific lines highlighted.

    Args:
        language (str): The programming language for syntax highlighting
        code (str): The code content to be displayed
        highlight_lines (list, optional): List of line numbers to highlight (1-indexed)
        auto_scaling (str): Auto-scaling behavior for Marp

    Returns:
        str: HTML string with highlighted code block
    """
    additional_classes = ""
    if highlight_lines:
        # Convert line numbers to a format that Marp can understand
        highlight_str = ",".join(str(line) for line in highlight_lines)
        additional_classes = f"highlight-lines-{highlight_str}"

    return generate_code_block(language, code, auto_scaling, additional_classes)


def generate_terminal_block(command: str, output: str = "", auto_scaling: str = "downscale-only") -> str:
    """
    Generate a terminal/bash code block with command and optional output.

    Args:
        command (str): The terminal command
        output (str, optional): The command output
        auto_scaling (str): Auto-scaling behavior for Marp

    Returns:
        str: HTML string formatted as a terminal session
    """
    terminal_content = f"$ {command}"
    if output:
        terminal_content += f"\n{output}"

    return generate_code_block("bash", terminal_content, auto_scaling)


def generate_diff_block(diff_content: str, auto_scaling: str = "downscale-only") -> str:
    """
    Generate a diff code block for showing code changes.

    Args:
        diff_content (str): The diff content
        auto_scaling (str): Auto-scaling behavior for Marp

    Returns:
        str: HTML string formatted as a diff
    """
    return generate_code_block("diff", diff_content, auto_scaling)


# Additional helper functions for common code block patterns

def python_code(code: str, **kwargs) -> str:
    """Shorthand for Python code blocks."""
    return generate_code_block("python", code, **kwargs)


def yaml_code(code: str, **kwargs) -> str:
    """Shorthand for YAML code blocks."""
    return generate_code_block("yaml", code, **kwargs)


def json_code(code: str, **kwargs) -> str:
    """Shorthand for JSON code blocks."""
    return generate_code_block("json", code, **kwargs)


def bash_code(code: str, **kwargs) -> str:
    """Shorthand for Bash/shell code blocks."""
    return generate_code_block("bash", code, **kwargs)


def javascript_code(code: str, **kwargs) -> str:
    """Shorthand for JavaScript code blocks."""
    return generate_code_block("javascript", code, **kwargs)


# Enhanced syntax highlighting function (placeholder for future implementation)
def generate_enhanced_code_block(language: str, code: str, auto_scaling: str = "downscale-only") -> str:
    """
    Generate a code block with enhanced syntax highlighting using hljs-* classes.

    This is a placeholder for future implementation. When implemented, this function
    should generate code blocks with proper syntax highlighting spans:
    - <span class="hljs-string"> for strings
    - <span class="hljs-keyword"> for keywords
    - <span class="hljs-number"> for numbers
    - <span class="hljs-literal"> for literals (True, False, None)
    - <span class="hljs-comment"> for comments
    - <span class="hljs-built_in"> for built-in functions

    See SYNTAX_HIGHLIGHTING_REQUIREMENTS.md for complete specifications.

    Args:
        language (str): The programming language for syntax highlighting
        code (str): The code content to be highlighted
        auto_scaling (str): Auto-scaling behavior for Marp

    Returns:
        str: HTML string with enhanced syntax highlighting

    TODO: Implement using pygments or similar syntax highlighting library
    """
    # For now, fall back to basic code block generation
    # TODO: Replace with proper syntax highlighting implementation
    return generate_code_block(language, code, auto_scaling)


# Example of what the enhanced function should generate (for documentation)
def _example_enhanced_output():
    """
    Example of the expected output from generate_enhanced_code_block.
    This is for documentation purposes only.
    """
    return '''<pre is="marp-pre" data-auto-scaling="downscale-only"><code class="language-python"><span class="hljs-keyword">import</span> <span class="hljs-title">boto3</span>

<span class="hljs-keyword">def</span> <span class="hljs-title function_">upload_file</span>():
    <span class="hljs-comment"># Create S3 client</span>
    client = boto3.client(<span class="hljs-string">"s3"</span>)
    bucket_name = <span class="hljs-string">"my-bucket"</span>
    is_public = <span class="hljs-literal">True</span>

    <span class="hljs-keyword">if</span> is_public:
        <span class="hljs-built_in">print</span>(<span class="hljs-string">"Uploading file"</span>)
        <span class="hljs-keyword">return</span> <span class="hljs-literal">True</span>
</code></pre>'''
