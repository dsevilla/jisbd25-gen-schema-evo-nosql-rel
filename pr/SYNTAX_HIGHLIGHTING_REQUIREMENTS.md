# Syntax Highlighting Requirements for Marp Code Blocks

## Overview

When generating code blocks for Marp slides, the HTML output must include proper syntax highlighting spans for optimal presentation. This document specifies the required HTML structure for syntax highlighting elements.

## Required Syntax Highlighting Elements

The generated `<pre><code>` blocks must include the following special span elements for syntax highlighting:

### String Literals
```html
<span class="hljs-string">"example string"</span>
<span class="hljs-string">'single quoted'</span>
```

### Numbers
```html
<span class="hljs-number">42</span>
<span class="hljs-number">3.14</span>
<span class="hljs-number">0xFF</span>
```

### Keywords
```html
<span class="hljs-keyword">import</span>
<span class="hljs-keyword">def</span>
<span class="hljs-keyword">class</span>
<span class="hljs-keyword">if</span>
<span class="hljs-keyword">return</span>
```

### Literals (Boolean, None, etc.)
```html
<span class="hljs-literal">True</span>
<span class="hljs-literal">False</span>
<span class="hljs-literal">None</span>
<span class="hljs-literal">null</span>
```

### Comments
```html
<span class="hljs-comment"># This is a comment</span>
<span class="hljs-comment">// JavaScript comment</span>
```

### Built-in Functions/Types
```html
<span class="hljs-built_in">print</span>
<span class="hljs-built_in">len</span>
<span class="hljs-built_in">str</span>
```

## Complete Example

Here's an example of properly highlighted Python code:

```html
<pre is="marp-pre" data-auto-scaling="downscale-only">
<code class="language-python">
<span class="hljs-keyword">import</span> <span class="hljs-title">boto3</span>

<span class="hljs-keyword">def</span> <span class="hljs-title function_">upload_file</span>():
    <span class="hljs-comment"># Create S3 client</span>
    client = boto3.client(<span class="hljs-string">"s3"</span>)

    <span class="hljs-comment"># Configuration</span>
    bucket_name = <span class="hljs-string">"my-bucket"</span>
    file_size = <span class="hljs-number">1024</span>
    is_public = <span class="hljs-literal">True</span>

    <span class="hljs-keyword">if</span> is_public:
        <span class="hljs-built_in">print</span>(<span class="hljs-string">"Uploading public file"</span>)
        <span class="hljs-keyword">return</span> <span class="hljs-literal">True</span>

    <span class="hljs-keyword">return</span> <span class="hljs-literal">False</span>
</code>
</pre>
```

## Implementation Requirements

### Current Implementation Status
The current `code_generator.py` provides basic HTML escaping and Marp-compatible structure, but **does not include syntax highlighting spans**.

### Required Enhancement
The code generation functions need to be enhanced to:

1. **Parse the input code** based on the specified language
2. **Identify syntax elements** (strings, keywords, numbers, etc.)
3. **Wrap elements** in appropriate `<span class="hljs-*">` tags
4. **Maintain Marp compatibility** with the existing `<pre is="marp-pre">` structure

### Language Support Priority
1. **Python** - Primary language used in slides
2. **YAML** - For CloudFormation templates
3. **JSON** - For configuration examples
4. **JavaScript** - For web examples
5. **Bash** - For command line examples

## Future Implementation

To implement proper syntax highlighting, consider these approaches:

### Option 1: Server-side Highlighting (Recommended)
- Use a Python syntax highlighting library (e.g., `pygments`)
- Generate highlighted HTML during template rendering
- Ensures consistent highlighting across all environments

### Option 2: Client-side Highlighting
- Generate basic HTML structure
- Rely on Marp's built-in highlighting (highlight.js/Prism.js)
- May have inconsistent results

### Option 3: Hybrid Approach
- Generate basic highlighting for critical elements (strings, keywords)
- Let Marp handle detailed highlighting
- Balance between control and simplicity

## Integration with Current System

This enhancement should be integrated into:

1. **`code_generator.py`** - Add syntax highlighting functions
2. **Template rendering** - Apply highlighting during generation
3. **Custom syntax function** - The user's planned custom syntax processor
4. **Documentation** - Update guides with highlighted examples

## Testing Requirements

Any implementation should be tested with:

- Multiple programming languages
- Complex code examples
- Nested syntax elements
- Special characters and escaping
- Marp preview compatibility
- PDF generation compatibility

## Notes

- The `hljs-*` classes are part of the highlight.js naming convention
- Marp uses these classes for consistent styling across themes
- Proper highlighting improves presentation quality and readability
- This is especially important for technical presentations with code examples
