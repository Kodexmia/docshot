# Contributing to DocShot

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

Before submitting a bug report:
1. Check existing issues to avoid duplicates
2. Collect information:
   - Operating system and version
   - Python version
   - Steps to reproduce
   - Expected vs actual behavior
   - Log files from `~/overlay_annotator_logs/`

Submit bug reports as GitHub issues with the "bug" label.

### Suggesting Features

Feature requests are welcome! Please:
1. Check if the feature has already been requested
2. Describe the use case clearly
3. Explain why it would be useful
4. Consider implementation complexity

Submit feature requests as GitHub issues with the "enhancement" label.

### Code Contributions

#### Setup Development Environment

```bash
# Fork and clone your fork
git clone https://github.com/YOUR_USERNAME/docshot.git
cd docshot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Making Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the coding standards below

3. Test your changes thoroughly

4. Commit with clear messages:
   ```bash
   git commit -m "Add feature: description of your feature"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Open a Pull Request

## Coding Standards

### Python Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use descriptive variable names

### Documentation
- Add docstrings to all functions/classes
- Use type hints where appropriate
- Update README.md if adding features
- Include inline comments for complex logic

### Example
```python
def calculate_duration(self, start_iso: str, end_iso: str) -> str:
    """Calculate duration between two ISO timestamps.
    
    Args:
        start_iso: ISO format timestamp string
        end_iso: ISO format timestamp string
        
    Returns:
        Human-readable duration string (e.g., "2h 30m")
    """
    # Implementation here
    pass
```

## Testing

Before submitting a PR:
1. Test on your platform (Windows/macOS/Linux)
2. Verify all existing features still work
3. Test edge cases
4. Check for error messages in logs

## Pull Request Process

1. Update README.md with details of changes if needed
2. Update version number if applicable
3. Ensure your code follows the style guide
4. Add yourself to contributors list (if first contribution)
5. Request review from maintainers

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- How did you test?
- What platforms were tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No new warnings or errors
- [ ] Tested on [OS]
```

## Project Structure

```
overlay_annotator/
├── app/
│   ├── core/           # Data models, storage, templates
│   └── ui/             # User interface components
├── README.md           # Main documentation
├── INSTALL.md          # Installation guide
├── CONTRIBUTING.md     # This file
└── requirements.txt    # Dependencies
```

## Areas Needing Help

### High Priority
- [ ] Multi-monitor support
- [ ] Integrated toolbar (not floating)
- [ ] Undo/redo for individual annotations

### Medium Priority
- [ ] Dark mode support
- [ ] Keyboard shortcut customization
- [ ] Export to PDF

### Low Priority
- [ ] Cloud sync integration
- [ ] Annotation templates
- [ ] Video annotation support

## Questions?

Feel free to:
- Open a discussion on GitHub
- Comment on related issues
- Reach out to maintainers

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism gracefully
- Focus on what's best for the project
- Show empathy towards other contributors

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing others' private information
- Other unprofessional conduct

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to DocShot! 🎉
