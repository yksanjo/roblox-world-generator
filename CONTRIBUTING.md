# Contributing to Roblox World Generator

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/roblox-world-generator/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)

### Suggesting Features

1. Check existing feature requests
2. Create a new issue with:
   - Clear description of the feature
   - Use case and benefits
   - Possible implementation approach (if you have ideas)

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes:**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed
4. **Test your changes:**
   - Test locally
   - Ensure no breaking changes
5. **Commit your changes:**
   ```bash
   git commit -m "Add: description of your feature"
   ```
6. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request:**
   - Provide clear description
   - Reference related issues
   - Add screenshots if UI changes

## Code Style

### Python
- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions/classes
- Maximum line length: 100 characters

### JavaScript/React
- Use ES6+ features
- Follow React best practices
- Use functional components with hooks
- Consistent indentation (2 spaces)

### Lua (Roblox Plugin)
- Follow Roblox Lua style guide
- Use descriptive variable names
- Comment complex logic

## Development Setup

1. Clone your fork:
```bash
git clone https://github.com/yourusername/roblox-world-generator.git
cd roblox-world-generator
```

2. Set up backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up frontend:
```bash
cd frontend
npm install
```

4. Create `.env` file:
```bash
cd backend
cp env.example .env
# Add your API keys
```

## Testing

Before submitting:
- Test all new features
- Test error cases
- Ensure backward compatibility
- Check for linting errors

## Questions?

Feel free to open an issue for questions or discussions!



