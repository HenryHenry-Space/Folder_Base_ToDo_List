#!/usr/bin/env python3
"""
Folder Structure to Markdown Todo Generator

This program reads any folder's structure and automatically generates
a markdown to-do list for all levels of the directory hierarchy.
"""

import os
import argparse
from pathlib import Path
from typing import List, Set


class FolderTodoGenerator:
    """Generate markdown todo lists from folder structures."""
    
    def __init__(self, exclude_dirs: Set[str] = None, exclude_files: Set[str] = None):
        """
        Initialize the generator.
        
        Args:
            exclude_dirs: Set of directory names to exclude (e.g., {'.git', '__pycache__'})
            exclude_files: Set of file patterns to exclude (e.g., {'.DS_Store', '*.pyc'})
        """
        self.exclude_dirs = exclude_dirs or {'.git', '__pycache__', '.vscode', 'node_modules', '.idea'}
        self.exclude_files = exclude_files or {'.DS_Store', '.gitignore', 'Thumbs.db'}
    
    def should_exclude_dir(self, dir_name: str) -> bool:
        """Check if directory should be excluded."""
        return dir_name in self.exclude_dirs or dir_name.startswith('.')
    
    def should_exclude_file(self, file_name: str) -> bool:
        """Check if file should be excluded."""
        return file_name in self.exclude_files or file_name.startswith('.')
    
    def generate_todo_markdown(self, root_path: str, include_files: bool = True) -> str:
        """
        Generate markdown todo list from folder structure.
        
        Args:
            root_path: Root directory path to scan
            include_files: Whether to include files in the todo list
            
        Returns:
            Formatted markdown string
        """
        root_path = Path(root_path).resolve()
        
        if not root_path.exists():
            raise FileNotFoundError(f"Path does not exist: {root_path}")
        
        if not root_path.is_dir():
            raise ValueError(f"Path is not a directory: {root_path}")
        
        markdown_lines = [
            f"# Todo List for: {root_path.name}",
            "",
            f"*Generated from folder structure: `{root_path}`*",
            "",
            "## Directory Structure Tasks",
            ""
        ]
        
        # Generate the todo items
        todo_items = self._generate_todo_items(root_path, include_files)
        markdown_lines.extend(todo_items)
        
        return "\n".join(markdown_lines)
    
    def _generate_todo_items(self, root_path: Path, include_files: bool, level: int = 0) -> List[str]:
        """
        Recursively generate todo items for directory structure.
        
        Args:
            root_path: Current directory path
            include_files: Whether to include files
            level: Current nesting level for indentation
            
        Returns:
            List of markdown todo lines
        """
        items = []
        indent = "  " * level
        
        try:
            # Get all items in the directory
            dir_items = sorted(root_path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
            
            for item in dir_items:
                if item.is_dir():
                    # Skip excluded directories
                    if self.should_exclude_dir(item.name):
                        continue
                    
                    # Add directory as todo item
                    items.append(f"{indent}- [ ] **{item.name}/** (directory)")
                    
                    # Recursively process subdirectory
                    sub_items = self._generate_todo_items(item, include_files, level + 1)
                    items.extend(sub_items)
                
                elif item.is_file() and include_files:
                    # Skip excluded files
                    if self.should_exclude_file(item.name):
                        continue
                    
                    # Add file as todo item
                    file_size = self._format_file_size(item.stat().st_size)
                    items.append(f"{indent}- [ ] {item.name} `({file_size})`")
        
        except PermissionError:
            items.append(f"{indent}- [ ] *[Permission Denied]*")
        
        return items
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format."""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        size = float(size_bytes)
        i = 0
        
        while size >= 1024.0 and i < len(size_names) - 1:
            size /= 1024.0
            i += 1
        
        return f"{size:.1f} {size_names[i]}"
    
    def save_to_file(self, markdown_content: str, output_path: str) -> None:
        """Save markdown content to file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"Todo list saved to: {output_path}")


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(
        description="Generate markdown todo lists from folder structures",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python folder_todo_generator.py /path/to/project
  python folder_todo_generator.py . --output todo.md
  python folder_todo_generator.py /home/user/docs --no-files
  python folder_todo_generator.py . --exclude-dirs build dist --exclude-files "*.log"
        """
    )
    
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Path to directory to scan (default: current directory)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: print to stdout)'
    )
    
    parser.add_argument(
        '--no-files',
        action='store_true',
        help='Exclude files from todo list (directories only)'
    )
    
    parser.add_argument(
        '--exclude-dirs',
        nargs='*',
        default=[],
        help='Additional directory names to exclude'
    )
    
    parser.add_argument(
        '--exclude-files',
        nargs='*',
        default=[],
        help='Additional file names/patterns to exclude'
    )
    
    args = parser.parse_args()
    
    # Create generator with custom exclusions
    default_exclude_dirs = {'.git', '__pycache__', '.vscode', 'node_modules', '.idea'}
    default_exclude_files = {'.DS_Store', '.gitignore', 'Thumbs.db'}
    
    exclude_dirs = default_exclude_dirs.union(set(args.exclude_dirs))
    exclude_files = default_exclude_files.union(set(args.exclude_files))
    
    generator = FolderTodoGenerator(exclude_dirs=exclude_dirs, exclude_files=exclude_files)
    
    try:
        # Generate the markdown todo list
        markdown_content = generator.generate_todo_markdown(
            args.path,
            include_files=not args.no_files
        )
        
        if args.output:
            generator.save_to_file(markdown_content, args.output)
        else:
            print(markdown_content)
    
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())