"""
Command line interface for folder-todo-generator.
"""

import argparse
import sys
from pathlib import Path
from .generator import FolderTodoGenerator


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate markdown todo lists from folder structures"
    )
    
    parser.add_argument(
        "path",
        help="Path to the directory to process"
    )
    
    parser.add_argument(
        "--max-depth",
        type=int,
        default=4,
        help="Maximum directory depth to traverse (default: 4)"
    )
    
    parser.add_argument(
        "--exclude-dirs",
        nargs="*",
        default=[],
        help="Directory names to exclude"
    )
    
    parser.add_argument(
        "--tags",
        nargs="*",
        default=[],
        help="Filter by tags (e.g., --tags frontend backend)"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path (default: print to stdout)"
    )
    
    args = parser.parse_args()
    
    try:
        # Create generator
        generator = FolderTodoGenerator(
            max_depth=args.max_depth,
            exclude_dirs=args.exclude_dirs,
            tag_filter=args.tags
        )
        
        # Generate markdown
        markdown_content = generator.generate_todo_markdown(args.path)
        
        # Output result
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(markdown_content, encoding='utf-8')
            print(f"Todo list saved to: {output_path}")
        else:
            print(markdown_content)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()