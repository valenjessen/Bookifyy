import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from functions import get_waiting_list

def display_waiting_lists():
    """
    Display all waiting lists.
    """
    waiting_lists = get_waiting_list()
    # Format and display waiting lists
    # Group by book title