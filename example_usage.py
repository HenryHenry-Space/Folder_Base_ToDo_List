#!/usr/bin/env python3
"""
Example usage of FolderTodoGenerator as a module
"""

from folder_todo_generator import FolderTodoGenerator

def main():
    """Example of using the FolderTodoGenerator class directly."""
    
    # Create a generator instance
    generator = FolderTodoGenerator()
    
    # Generate todo list for current directory
    current_dir_todo = generator.generate_todo_markdown(".", include_files=True)
    print("=== Current Directory Todo ===")
    print(current_dir_todo)
    print("\n" + "="*50 + "\n")
    
    # Generate todo list excluding files
    dirs_only_todo = generator.generate_todo_markdown(".", include_files=False)
    print("=== Directories Only Todo ===")
    print(dirs_only_todo)
    print("\n" + "="*50 + "\n")
    
    # Custom exclusions
    custom_generator = FolderTodoGenerator(
        exclude_dirs={'build', 'dist', '__pycache__'},
        exclude_files={'*.pyc', '*.log'}
    )
    
    custom_todo = custom_generator.generate_todo_markdown(".")
    print("=== Custom Exclusions Todo ===")
    print(custom_todo)
    print("\n" + "="*50 + "\n")
    
    # Collapsible structure
    collapsible_todo = generator.generate_todo_markdown(".", collapsible=True)
    print("=== Collapsible Todo ===")
    print(collapsible_todo)


if __name__ == "__main__":
    main()