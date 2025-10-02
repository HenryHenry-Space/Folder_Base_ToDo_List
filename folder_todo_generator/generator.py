"""
Folder structure to markdown todo list generator.
"""

from pathlib import Path
from typing import List, Optional


class FolderTodoGenerator:
    """Generate markdown todo lists from folder structures."""
    
    def __init__(self, max_depth: Optional[int] = 4, 
                 exclude_dirs: Optional[List[str]] = None):
        """
        Initialize the generator.
        
        Args:
            max_depth: Maximum directory depth to traverse (default 4)
            exclude_dirs: List of directory names to exclude
        """
        self.max_depth = max_depth or 4
        self.exclude_dirs = exclude_dirs or []
    
    def generate_todo_markdown(self, root_path: str, collapsible: bool = False) -> str:
        """
        Generate a markdown todo list from a folder structure.
        
        Args:
            root_path: Path to the root directory
            collapsible: Ignored - kept for compatibility
            
        Returns:
            Markdown formatted todo list
        """
        root = Path(root_path).resolve()
        if not root.exists():
            raise FileNotFoundError(f"Path does not exist: {root}")
        
        if not root.is_dir():
            raise ValueError(f"Path is not a directory: {root}")
        
        # Generate header
        markdown_lines = [
            f"# Todo List for: {root.name}",
            "",
            f"*Generated from folder structure: `{root}`*",
            "",
            "## Directory Structure Tasks",
            ""
        ]
        
        # Generate todo items
        todo_items = self._generate_todo_items(root)
        markdown_lines.extend(todo_items)
        
        return "\n".join(markdown_lines)
    
    def _generate_todo_items(self, directory: Path, current_depth: int = 0) -> List[str]:
        """
        Recursively generate todo items for directory contents.
        
        Args:
            directory: Directory to process
            current_depth: Current recursion depth
            
        Returns:
            List of markdown lines
        """
        items = []
        
        # Stop if we've reached max depth
        if current_depth >= self.max_depth:
            return items
        
        try:
            # Get all directories in current directory
            all_items = list(directory.iterdir())
            directories = [item for item in all_items if item.is_dir() and item.name not in self.exclude_dirs]
            
            # Sort directories
            directories.sort(key=lambda x: x.name.lower())
            
            # Process directories
            for dir_item in directories:
                # Create indentation based on depth
                indent = "  " * current_depth
                
                # Add directory as todo item
                items.append(f"{indent}- [ ] **{dir_item.name}/**")
                
                # Recursively add subdirectory contents
                sub_items = self._generate_todo_items(dir_item, current_depth + 1)
                items.extend(sub_items)
        
        except PermissionError:
            indent = "  " * current_depth
            items.append(f"{indent}- [ ] *Permission denied*")
        
        return items