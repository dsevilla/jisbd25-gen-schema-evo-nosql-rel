"""
Code block generation functions for Marp slides using Jinja2.
This module provides functions to generate properly formatted code blocks
that are compatible with Marp's syntax highlighting and auto-scaling features.

IMPORTANT: Current implementation provides basic HTML structure.
For advanced syntax highlighting requirements (hljs-string, hljs-keyword, etc.),
see SYNTAX_HIGHLIGHTING_REQUIREMENTS.md for enhancement specifications.
"""

import html
import shutil
import subprocess
from subprocess import CompletedProcess
import tempfile
import os
from pathlib import Path
import base64
import zlib
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

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


def generate_mermaid_diagram(diagram_name: str,
                             diagram_code: str,
                             width: int = 800, height: int = -1,
                             diagram_type: str = "erDiagram",
                             output_format: str = "svg") -> str:
    """
    Generate a Mermaid diagram using Docker and return the SVG content inline.

    Args:
        diagram_name (str): Name of the diagram (used for saving the file in img/ folder)
        diagram_code (str): The Mermaid diagram code (without the diagram type declaration)
        diagram_type (str): Type of diagram ('erDiagram', 'flowchart', 'sequenceDiagram', etc.)
        output_format (str): Output format ('svg', 'png', 'pdf')
        width (int): Diagram width in pixels
        height (int): Diagram height in pixels

    Returns:
        str: HTML string with inline SVG or image tag
    """
    # Complete Mermaid diagram code
    full_diagram: str = f"{diagram_type}\n{diagram_code}"
    mmd_path = None
    output_path = None

    # Set height to -1 if not specified
    if height == -1:
        height = width * 16 // 9  # Default to 16:9 aspect ratio

    # Create temporary files in current directory instead of /tmp
    current_dir: str = os.getcwd()

    try:
        # Create temporary files in current working directory
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, dir=current_dir) as mmd_file:
            mmd_file.write(full_diagram)
            mmd_path: str = mmd_file.name

        output_path = mmd_path.replace('.mmd', f'.{output_format}')

        # Run Mermaid CLI in Docker
        # Mount current directory to /data for better compatibility
        # Add user mapping to fix permission issues
        current_user: int = os.getuid() if hasattr(os, 'getuid') else 1000
        current_group: int = os.getgid() if hasattr(os, 'getgid') else 1000

        docker_cmd: list[str] = [
            'docker', 'run', '--rm',
            '--user', f'{current_user}:{current_group}',
            '-v', f'{current_dir}:/data:rw',
            'minlag/mermaid-cli',
            '-i', f'/data/{os.path.basename(mmd_path)}',
            '-o', f'/data/{os.path.basename(output_path)}',
            '-w', str(width),
            '-H', str(height)
        ]

        result: CompletedProcess[str] = subprocess.run(docker_cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            error_msg: str = f"Mermaid generation failed: {result.stderr}"
            print(f"Warning: {error_msg}")
            return f'<div class="error">Error generating diagram: {error_msg}</div>'

        # If diagram_name is not none, take this as the name of a file in the img folder
        if diagram_name:
            output_path: str = os.path.join(current_dir, 'img', f'{diagram_name}.{output_format}')
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            # Copy the generated file to the target location
            shutil.copy(mmd_path.replace('.mmd', f'.{output_format}'), output_path)
            # Optionally, remove the temporary files
            os.remove(mmd_path.replace('.mmd', f'.{output_format}'))

            # Output the image tag pointing to the saved file
            rel_path: str = os.path.relpath(output_path, '.')
            output_path = None
            return f'<p><img src="{rel_path}" alt="center" style="width:{width}px;" /></p>'

        # Read the generated file
        # Embed the generated file inline as a base64 data URI
        try:
            with open(output_path, 'rb') as bf:
                raw: bytes = bf.read()
            b64: str = base64.b64encode(raw).decode('ascii')
            fmt: str = output_format.lower()
            if fmt == 'svg':
                # Try to remove hard-coded width/height from the SVG so it can scale
                try:
                    svg_text = raw.decode('utf-8')
                    # Parse SVG and adjust attributes
                    try:
                        root = ET.fromstring(svg_text)
                        # Namespaces: handle common svg namespace
                        # Get width/height if present
                        w = root.attrib.pop('width', None)
                        h = root.attrib.pop('height', None)
                        vb = root.attrib.get('viewBox')
                        if not vb and w and h:
                            # Strip 'px' if present and try to build a viewBox
                            try:
                                wn = float(str(w).replace('px', ''))
                                hn = float(str(h).replace('px', ''))
                                root.set('viewBox', f'0 0 {int(wn)} {int(hn)}')
                            except Exception:
                                # ignore if parsing fails
                                pass
                        # Ensure preserveAspectRatio exists so scaling behaves
                        if 'preserveAspectRatio' not in root.attrib:
                            root.set('preserveAspectRatio', 'xMidYMid meet')

                        # Serialize back to string
                        svg_text = ET.tostring(root, encoding='unicode')
                    except Exception:
                        # If parsing fails, fall back to a regex-like removal
                        import re
                        svg_text = re.sub(r'\swidth="[^"]+"', '', svg_text)
                        svg_text = re.sub(r'\sheight="[^"]+"', '', svg_text)

                    # Encode cleaned svg
                    cleaned_b64 = base64.b64encode(svg_text.encode('utf-8')).decode('ascii')
                    data_uri = f'data:image/svg+xml;base64,{cleaned_b64}'
                    # Return responsive image tag so CSS width/height control applies
                    style = f"max-width:{width}px; height:auto; display:block; margin:0 auto;"
                    return f'<p><img src="{data_uri}" alt="center" style="{style}" /></p>'
                except Exception:
                    # Fallback to previous behavior if anything goes wrong
                    data_uri = f'data:image/svg+xml;base64,{b64}'
                    return f'<p><img src="{data_uri}" alt="center" style="width:{width}px;" /></p>'
            elif fmt == 'png':
                mime = 'image/png'
                data_uri = f'data:{mime};base64,{b64}'
                return f'<p><img src="{data_uri}" alt="center" style="width:{width}px;" /></p>'
            elif fmt in ('jpg', 'jpeg'):
                mime = 'image/jpeg'
                data_uri = f'data:{mime};base64,{b64}'
                return f'<p><img src="{data_uri}" alt="center" style="width:{width}px;" /></p>'
            elif fmt == 'pdf':
                # Embed PDF using <embed> so it can be viewed in supporting viewers
                data_uri = f'data:application/pdf;base64,{b64}'
                return f'<p><embed src="{data_uri}" type="application/pdf" width="100%" height="600px" /></p>'
            else:
                # Unknown format: fall back to a relative path
                rel_path = os.path.relpath(output_path, '.')
                return f'<p><img src="{rel_path}" alt="center" style="width:{width}px;" /></p>'
        except Exception as e:
            print(f"Warning: embedding image failed: {e}")
            rel_path = os.path.relpath(output_path, '.')
            return f'<p><img src="{rel_path}" alt="center" style="width:{width}px;" /></p>'

    except Exception as e:
        error_msg = f"Error generating Mermaid diagram: {str(e)}"
        print(f"Warning: {error_msg}")
        return f'<div class="error">{error_msg}</div>'
    finally:
        # Cleanup temporary files
        try:
            if mmd_path and os.path.exists(mmd_path):
                os.unlink(mmd_path)
            if output_path and os.path.exists(output_path):
                os.unlink(output_path)
        except Exception:
            pass


def generate_er_diagram(entities_and_relationships: str, **kwargs) -> str:
    """
    Shorthand for ER diagrams specifically.

    Args:
        entities_and_relationships (str): The ER diagram definition
        **kwargs: Additional arguments passed to generate_mermaid_diagram

    Returns:
        str: HTML string with the ER diagram
    """
    return generate_mermaid_diagram(entities_and_relationships, "erDiagram", **kwargs)


def generate_mermaid_kroki(diagram_code: str, diagram_type: str = "erDiagram",
                          kroki_url: str = "https://kroki.io") -> str:
    """
    Generate a Mermaid diagram using Kroki web service (simpler alternative to Docker).

    Args:
        diagram_code (str): The Mermaid diagram code (without the diagram type declaration)
        diagram_type (str): Type of diagram ('erDiagram', 'flowchart', 'sequenceDiagram', etc.)
        kroki_url (str): Kroki service URL (default: https://kroki.io)

    Returns:
        str: HTML string with inline SVG
    """
    # Complete Mermaid diagram code
    full_diagram = f"{diagram_type}\n{diagram_code}"

    try:
        # Encode the diagram for Kroki
        diagram_bytes = full_diagram.encode('utf-8')
        compressed = zlib.compress(diagram_bytes)
        encoded = base64.urlsafe_b64encode(compressed).decode('ascii')

        # Build Kroki URL
        kroki_svg_url = f"{kroki_url}/mermaid/svg/{encoded}"

        # Fetch the SVG
        with urllib.request.urlopen(kroki_svg_url, timeout=10) as response:
            svg_content = response.read().decode('utf-8')

        return f'<div class="mermaid-diagram">{svg_content}</div>'

    except Exception as e:
        error_msg = f"Error generating Mermaid diagram via Kroki: {str(e)}"
        print(f"Warning: {error_msg}")
        return f'<div class="error">{error_msg}</div>'


def generate_er_diagram_kroki(entities_and_relationships: str, **kwargs) -> str:
    """
    Shorthand for ER diagrams using Kroki service.

    Args:
        entities_and_relationships (str): The ER diagram definition
        **kwargs: Additional arguments passed to generate_mermaid_kroki

    Returns:
        str: HTML string with the ER diagram
    """
    return generate_mermaid_kroki(entities_and_relationships, "erDiagram", **kwargs)


def generate_mermaid_local_kroki(diagram_code: str, diagram_type: str = "erDiagram",
                                kroki_url: str = "http://localhost:8000") -> str:
    """
    Generate a Mermaid diagram using local Kroki service (via docker-compose).

    Args:
        diagram_code (str): The Mermaid diagram code (without the diagram type declaration)
        diagram_type (str): Type of diagram ('erDiagram', 'flowchart', 'sequenceDiagram', etc.)
        kroki_url (str): Local Kroki service URL (default: http://localhost:8000)

    Returns:
        str: HTML string with inline SVG
    """
    return generate_mermaid_kroki(diagram_code, diagram_type, kroki_url)


def generate_mermaid_placeholder(diagram_code: str, diagram_type: str = "erDiagram") -> str:
    """
    Generate a placeholder for Mermaid diagrams when external services are not available.
    This creates a simple HTML representation of the diagram code.

    Args:
        diagram_code (str): The Mermaid diagram code
        diagram_type (str): Type of diagram

    Returns:
        str: HTML string with styled placeholder
    """
    # Clean up the diagram code for display
    cleaned_code = diagram_code.strip()

    # Create a simple SVG placeholder
    svg_content = f'''
    <svg width="400" height="300" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
        <rect x="10" y="10" width="380" height="280" fill="#f9f9f9" stroke="#ddd" stroke-width="2" rx="5"/>
        <text x="200" y="40" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" font-weight="bold">{diagram_type}</text>
        <text x="200" y="60" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#666">Diagram Placeholder</text>
        <foreignObject x="20" y="80" width="360" height="200">
            <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: monospace; font-size: 11px; white-space: pre-wrap; overflow: hidden;">
{html.escape(cleaned_code)}
            </div>
        </foreignObject>
    </svg>
    '''

    return f'<div class="mermaid-placeholder" style="text-align: center; margin: 20px 0;">{svg_content}</div>'


def generate_er_diagram_safe(entities_and_relationships: str, fallback_to_placeholder: bool = True) -> str:
    """
    Generate an ER diagram with automatic fallback to placeholder if external services fail.

    Args:
        entities_and_relationships (str): The ER diagram definition
        fallback_to_placeholder (bool): Whether to fall back to placeholder on failure

    Returns:
        str: HTML string with the ER diagram or placeholder
    """
    # Try Docker method first (usually more reliable than Kroki)
    try:
        result = generate_mermaid_diagram(entities_and_relationships, "erDiagram")
        # Check if it's a real SVG result (not an error div)
        if result.startswith('<div class="mermaid-diagram">') and '<svg' in result:
            return result
    except Exception:
        pass

    try:
        # Try Kroki as fallback
        result = generate_mermaid_kroki(entities_and_relationships, "erDiagram")
        # Check if it's a real SVG result (not an error div)
        if result.startswith('<div class="mermaid-diagram">') and '<svg' in result:
            return result
    except Exception:
        pass

    # Fallback to placeholder if enabled
    if fallback_to_placeholder:
        return generate_mermaid_placeholder(entities_and_relationships, "erDiagram")

    return '<div class="error">Unable to generate ER diagram</div>'


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
