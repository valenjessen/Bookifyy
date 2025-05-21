import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions import search_books
from functions import get_book_details

def display_search_results(search_term):
    """
    Display search results based on search term.
    """
    results = search_books(search_term)
    # Format and display results
    # Display availability, location, etc.

def display_book_details(numero_de_id):
    """
    Display detailed information about a book.
    """
    book = get_book_details(numero_de_id)
    # Format and display book details
    # Include buttons for requesting loan or joining waiting list