"""
Folder Todo Generator

A Python package that automatically reads any folder's structure 
and generates markdown to-do lists for all levels of the directory hierarchy.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .generator import FolderTodoGenerator

__all__ = ["FolderTodoGenerator"]