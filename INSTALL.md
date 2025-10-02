# Installation and Build Guide

## For Users

### Option 1: Install from Source (Recommended)

```bash
# Clone or download the repository
git clone <repository-url>
cd folder-todo-generator

# Install the package
pip install .
```

### Option 2: Development Installation

```bash
# For developers who want to modify the code
pip install -e .
```

### Option 3: Install from PyPI (when published)

```bash
# Once published to PyPI
pip install folder-todo-generator
```

## For Developers

### Setting up Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd folder-todo-generator

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Building the Package

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# The built packages will be in the dist/ directory
```

### Publishing to PyPI

```bash
# Test on TestPyPI first
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

### Testing

```bash
# Test the command line tool
folder-todo-gen --help
ftg --version

# Test the Python library
python -c "from folder_todo_generator import FolderTodoGenerator; print('Import successful!')"
```

## Package Structure

```
folder-todo-generator/
├── folder_todo_generator/          # Main package
│   ├── __init__.py                 # Package initialization
│   ├── generator.py                # Core functionality
│   └── cli.py                      # Command-line interface
├── pyproject.toml                  # Modern Python packaging config
├── setup.py                       # Backward compatibility
├── MANIFEST.in                     # Package manifest
├── LICENSE                         # MIT License
├── README.md                       # Documentation
└── example_usage.py               # Usage examples
```

## Entry Points

The package provides two command-line tools:
- `folder-todo-gen`: Full command name
- `ftg`: Short alias

Both commands are equivalent and provide the same functionality.