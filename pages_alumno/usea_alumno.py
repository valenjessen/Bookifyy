import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions import get_user_info
from functions import verify_credentials

def display_user_profile(email):
    """
    Display user profile information.
    """
    user_info = get_user_info(email)
    # Format and display user information
    
def change_password(email, current_password, new_password):
    """
    Change user password.
    """
    # Verify current password
    if verify_credentials(email, current_password):
        # Update password logic here
        # ...
        return True, "Password changed successfully"
    else:
        return False, "Current password is incorrect"