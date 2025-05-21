import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions import search_books

def display_all_books():
    """
    Display all books in the library.
    """
    books = search_books("")  # Empty search returns all books
    # Format and display books
    
