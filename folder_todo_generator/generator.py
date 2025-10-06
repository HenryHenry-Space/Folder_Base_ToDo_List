"""
Folder structure to markdown todo list generator.
"""

import re
from pathlib import Path
from typing import List, Optional, Set


class FolderTodoGenerator:
    """Generate markdown todo lists from folder structures."""
    
    def __init__(self, max_depth: Optional[int] = 4, 
                 exclude_dirs: Optional[List[str]] = None,
                 tag_filter: Optional[List[str]] = None):
        """
        Initialize the generator.
        
        Args:
            max_depth: Maximum directory depth to traverse (default 4)
            exclude_dirs: List of directory names to exclude
            tag_filter: List of tags to filter by (only show todos with these tags)
        """
        self.max_depth = max_depth or 4
        self.exclude_dirs = exclude_dirs or []
        self.tag_filter = tag_filter or []
    
    def _extract_tags_from_name(self, name: str) -> Set[str]:
        """
        Extract tags from directory or file names.
        Tags are in the format #tagname
        
        Args:
            name: Directory or file name
            
        Returns:
            Set of extracted tags
        """
        # Find all hashtag patterns in the name
        tag_pattern = r'#(\w+)'
        matches = re.findall(tag_pattern, name, re.IGNORECASE)
        return set(matches)
    
    def _check_tag_file(self, directory: Path) -> Set[str]:
        """
        Check for a .tags file in the directory that contains tags.
        
        Args:
            directory: Directory to check
            
        Returns:
            Set of tags from the .tags file
        """
        tags = set()
        tag_file = directory / '.tags'
        if tag_file.exists() and tag_file.is_file():
            try:
                content = tag_file.read_text(encoding='utf-8').strip()
                # Extract tags from the file content
                tag_pattern = r'#(\w+)'
                matches = re.findall(tag_pattern, content, re.IGNORECASE)
                tags.update(matches)
            except Exception:
                # Ignore errors reading tag file
                pass
        return tags
    
    def _should_include_item(self, tags: Set[str]) -> bool:
        """
        Check if an item should be included based on tag filtering.
        
        Args:
            tags: Set of tags for the item
            
        Returns:
            True if item should be included
        """
        if not self.tag_filter:
            return True
        
        # Check if any of the filter tags match
        return bool(set(self.tag_filter).intersection(tags))
    
    def _format_tags(self, tags: Set[str]) -> str:
        """
        Format tags for display in markdown.
        
        Args:
            tags: Set of tags
            
        Returns:
            Formatted tag string
        """
        if not tags:
            return ""
        
        sorted_tags = sorted(tags)
        tag_str = " ".join(f"`#{tag}`" for tag in sorted_tags)
        return f" {tag_str}"
    
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
            ""
        ]
        
        # Add tag filter info if applicable
        if self.tag_filter:
            tag_list = ", ".join(f"`#{tag}`" for tag in self.tag_filter)
            markdown_lines.extend([
                f"*Filtered by tags: {tag_list}*",
                ""
            ])
        
        markdown_lines.extend([
            "## Directory Structure Tasks",
            ""
        ])
        
        # Generate todo items
        todo_items = self._generate_todo_items(root)
        
        if not todo_items and self.tag_filter:
            markdown_lines.append("*No directories found matching the specified tags.*")
        else:
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
                # Extract tags from directory name and .tags file
                name_tags = self._extract_tags_from_name(dir_item.name)
                file_tags = self._check_tag_file(dir_item)
                all_tags = name_tags.union(file_tags)
                
                # Check if this directory should be included based on tag filter
                if not self._should_include_item(all_tags):
                    continue
                
                # Create indentation based on depth
                indent = "  " * current_depth
                
                # Format tags for display
                tag_display = self._format_tags(all_tags)
                
                # Add directory as todo item
                items.append(f"{indent}- [ ] **{dir_item.name}/**{tag_display}")
                
                # Recursively add subdirectory contents
                sub_items = self._generate_todo_items(dir_item, current_depth + 1)
                items.extend(sub_items)
        
        except PermissionError:
            indent = "  " * current_depth
            items.append(f"{indent}- [ ] *Permission denied*")
        
        return items