import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions import get_all_loans

def display_all_loans(filter_state=None):
    """
    Display all loans, optionally filtered by state.
    """
    loans = get_all_loans(filter_state)
    # Format and display loans
    # Group by status (overdue, active, requested)
    
def create_new_loan_form():
    """
    Display form for creating a new loan.
    """
    # Form logic for creating new loan
    # Should call create_loan() when submitted
    
def send_reminder(dni, numero_de_id):
    """
    Send reminder to user about overdue book.
    """
    # Reminder logic here
    # Could involve email or notification system
