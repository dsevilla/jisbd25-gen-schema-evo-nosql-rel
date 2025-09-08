#!/usr/bin/env python3
"""
Example script showing how to use the template system for Marp slides.
"""

from render_template import render_template

def main():
    """Generate the Marp slides from the Jinja2 template."""
    print("Rendering Marp slides from Jinja2 template...")

    # Render the template with any additional variables you might need
    template_vars = {
        # You can add any variables here that you want to use in your template
        # For example:
        # 'course_year': '2024-25',
        # 'author': 'Your Name',
    }

    try:
        render_template('pr.md', 'pr_generated.md', **template_vars)
        print("✅ Successfully generated pr_generated.md from pr.md")
        print("You can now open pr_generated.md in VS Code with the Marp extension to preview your slides!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
