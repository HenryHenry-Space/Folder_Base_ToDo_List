# Folder Todo Generator

A Python package that automatically reads any folder's structure and generates markdown to-do lists for all levels of the directory hierarchy.

## Features

- 📁 Recursively scans directory structures
- 📝 Generates markdown-formatted todo lists
- 🎯 Hierarchical organization with proper indentation
- 📊 Includes file sizes in human-readable format
- 🚫 Smart exclusion of common system/build directories
- ⚙️ Customizable exclusion patterns
- 💾 Save to file or print to stdout
- 🔧 Easy installation via pip
- 📂 Collapsible folder structure support

## Installation

### From PyPI (when published)

```bash
pip install folder-todo-generator
```

### Local Installation

Clone or download this repository and install:

```bash
# Install in development mode
pip install -e .

# Or install normally
pip install .
```

## Usage

After installation, you can use the tool from anywhere with the `folder-todo-gen` command:

### Basic Usage

```bash
# Generate todo list for current directory
folder-todo-gen

# Generate todo list for specific directory
folder-todo-gen /path/to/your/project

# Save output to file
folder-todo-gen . --output project_todo.md

# Only include directories (exclude files)
folder-todo-gen . --no-files

# Create collapsible folder structure
folder-todo-gen . --collapsible --output collapsible_todo.md
```

### Advanced Options

```bash
# Exclude additional directories
folder-todo-gen . --exclude-dirs build dist temp

# Exclude additional files
folder-todo-gen . --exclude-files "*.log" "*.tmp"

# Combine options
folder-todo-gen /my/project --output todo.md --no-files --exclude-dirs venv

# Show version
folder-todo-gen --version

# Show help
folder-todo-gen --help
```

### Alternative Command

You can also use the shorter `ftg` command:

```bash
ftg .
ftg /path/to/project --output todo.md
```

## Programmatic Usage

You can also use the package in your Python code:

```python
from folder_todo_generator import FolderTodoGenerator

# Create generator instance
generator = FolderTodoGenerator()

# Generate todo markdown
todo_content = generator.generate_todo_markdown("/path/to/project")
print(todo_content)

# Save to file
generator.save_to_file(todo_content, "project_todo.md")

# Custom exclusions
custom_generator = FolderTodoGenerator(
    exclude_dirs={'build', 'dist', '__pycache__'},
    exclude_files={'*.pyc', '*.log'}
)
custom_todo = custom_generator.generate_todo_markdown(".")

# Generate collapsible structure
collapsible_generator = FolderTodoGenerator()
collapsible_todo = collapsible_generator.generate_todo_markdown(".", collapsible=True)
```

## Example Output

### Regular Output

```markdown
# Todo List for: my_project

*Generated from folder structure: `/home/user/my_project`*

## Directory Structure Tasks

- [ ] **src/** (directory)
  - [ ] main.py `(2.3 KB)`
  - [ ] **utils/** (directory)
    - [ ] helpers.py `(1.1 KB)`
- [ ] **tests/** (directory)
  - [ ] test_main.py `(856 B)`
- [ ] README.md `(1.5 KB)`
```

### Collapsible Output

```markdown
# Todo List for: my_project

*Generated from folder structure: `/home/user/my_project`*

## Directory Structure Tasks

<details>
<summary>- [ ] **src/** (directory)</summary>

  - [ ] main.py `(2.3 KB)`
  <details>
  <summary>- [ ] **utils/** (directory)</summary>

    - [ ] helpers.py `(1.1 KB)`
  </details>

</details>

<details>
<summary>- [ ] **tests/** (directory)</summary>

  - [ ] test_main.py `(856 B)`
</details>

- [ ] README.md `(1.5 KB)`
```

The collapsible format allows users to expand/collapse folder sections in markdown viewers that support HTML.

## Example Output

```markdown
# Todo List for: my_project

*Generated from folder structure: `/home/user/my_project`*

## Directory Structure Tasks

- [ ] **src/** (directory)
  - [ ] main.py `(2.3 KB)`
  - [ ] **utils/** (directory)
    - [ ] helpers.py `(1.1 KB)`
- [ ] **tests/** (directory)
  - [ ] test_main.py `(856 B)`
- [ ] README.md `(1.5 KB)`
```

## Default Exclusions

The program automatically excludes common system and build directories:
- `.git`, `__pycache__`, `.vscode`, `node_modules`, `.idea`
- Hidden files starting with `.`
- Common system files like `.DS_Store`, `Thumbs.db`

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)