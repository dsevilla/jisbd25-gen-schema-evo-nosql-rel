# Auto-Generation Setup for Marp Slides

You now have **multiple options** to automatically generate your slides when you save the template file:

## Option 1: VS Code Extension (Recommended) ✅

The **"Run on Save"** extension has been installed and configured.

### How it works:
- Every time you save `pr_corrected.md.j2`, it automatically runs the generation script
- The generated `pr_generated.md` file updates automatically
- You can keep the preview of `pr_generated.md` open to see changes in real-time

### Usage:
1. Open `pr_corrected.md.j2` in one tab
2. Open `pr_generated.md` in another tab with Marp preview (Ctrl+Shift+V)
3. Edit the template file
4. Save (Ctrl+S) → slides regenerate automatically
5. The preview updates automatically

### Configuration:
The extension is configured in `.vscode/settings.json` to:
- Watch for changes to `pr_corrected.md.j2`
- Run the generation script automatically
- Show minimal output in the terminal

## Option 2: VS Code Tasks

You can manually trigger generation using VS Code tasks:

### Usage:
1. Press `Ctrl+Shift+P`
2. Type "Tasks: Run Task"
3. Select "Generate Marp Slides"

### Or create a keyboard shortcut:
Add to your VS Code keybindings.json:
```json
{
    "key": "ctrl+alt+g",
    "command": "workbench.action.tasks.runTask",
    "args": "Generate Marp Slides"
}
```

## Option 3: File Watcher Script

For users who prefer a standalone solution:

### Setup:
```bash
pip install -r requirements.txt
```

### Usage:
```bash
python watch_template.py
```

This runs a background process that watches for file changes.

## Option 4: Manual Generation

Simple manual approach:

```bash
python generate_slides.py
```

## Recommended Workflow

1. **Setup**: Use Option 1 (VS Code Extension)
2. **Editing**:
   - Keep `pr_corrected.md.j2` open for editing
   - Keep `pr_generated.md` open with Marp preview
3. **Preview**: Changes appear automatically when you save

## Troubleshooting

### Extension not working?
- Check the Output panel (View → Output → "Run on Save")
- Ensure Python is in your PATH
- Check the terminal for error messages

### Preview not updating?
- Make sure you're previewing `pr_generated.md` (not the template)
- Try refreshing the preview (Ctrl+Shift+V)
- Check if the generation was successful in the terminal

### File permissions?
- Ensure the scripts are executable
- Check that Python can write to the directory

## Benefits of Auto-Generation

- **Real-time feedback**: See changes immediately
- **No manual steps**: Save and preview updates automatically
- **Efficient workflow**: Focus on content, not process
- **Error catching**: Immediate feedback if template has issues

The VS Code extension approach (Option 1) provides the smoothest experience for slide development!
