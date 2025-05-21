import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions import get_user_loans
from functions import extend_loan


def display_user_loans(dni):
    """
    Display all loans for the current user.
    """
    loans = get_user_loans(dni)
    # Format and display loans
    # Group by status (overdue, active, requested)
    
def request_extension(dni, numero_de_id):
    """
    Request an extension for a loan.
    """
    success, message = extend_loan(dni, numero_de_id)
    # Display success or error message