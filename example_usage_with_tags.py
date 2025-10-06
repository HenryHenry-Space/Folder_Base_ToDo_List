#!/usr/bin/env python3
"""
Example usage of FolderTodoGenerator with tag support
"""

from folder_todo_generator import FolderTodoGenerator

def main():
    """Example of using the FolderTodoGenerator class with tag functionality."""
    
    # Create a generator instance with no tag filtering
    generator = FolderTodoGenerator()
    
    # Generate todo list for test directory (shows all tags)
    print("=== All Directories with Tags ===")
    todo_all = generator.generate_todo_markdown("test_dirs")
    print(todo_all)
    print("\n" + "="*50 + "\n")
    
    # Filter by specific tags
    ui_generator = FolderTodoGenerator(tag_filter=["ui", "frontend"])
    print("=== Frontend/UI Only ===")
    todo_ui = ui_generator.generate_todo_markdown("test_dirs")
    print(todo_ui)
    print("\n" + "="*50 + "\n")
    
    # Filter by urgent items
    urgent_generator = FolderTodoGenerator(tag_filter=["urgent"])
    print("=== Urgent Items Only ===")
    todo_urgent = urgent_generator.generate_todo_markdown("test_dirs")
    print(todo_urgent)
    print("\n" + "="*50 + "\n")
    
    # Combine with other options
    custom_generator = FolderTodoGenerator(
        max_depth=2,
        exclude_dirs=['node_modules', '.git'],
        tag_filter=["api", "documentation"]
    )
    print("=== API and Documentation (Max Depth 2) ===")
    todo_custom = custom_generator.generate_todo_markdown("test_dirs")
    print(todo_custom)


if __name__ == "__main__":
    main()