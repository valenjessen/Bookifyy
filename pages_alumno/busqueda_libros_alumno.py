
import streamlit as st


st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');
    
    :root {
        --color-primary: #75510e;
        --color-secondary: #b9985a;
        --color-light: #f5e0b9;
        --color-lightest: #fef8ee;
    }
    
    .stApp {
        background-color: var(--color-lightest);
        color: var(--color-primary);
        font-family: 'Libre Baskerville', serif;
    }
    
    /* Sidebar Navigation */
    .sidebar-nav {
        background-color: var(--color-light);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .nav-item {
        display: block;
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        color: var(--color-primary);
        text-decoration: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .nav-item:hover, .nav-item.active {
        background-color: var(--color-primary);
        color: white;
    }
    
    /* Header */
    .page-header {
        background-color: var(--color-primary);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Search Box */
    .search-container {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(117, 81, 14, 0.1);
        margin-bottom: 2rem;
    }
    
    /* Book Cards */
    .book-card {
        background-color: white;
        border: 2px solid var(--color-light);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .book-card:hover {
        box-shadow: 0 8px 25px rgba(117, 81, 14, 0.15);
        transform: translateY(-2px);
    }
    
    .book-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--color-primary);
        margin-bottom: 0.5rem;
    }
    
    .book-info {
        color: var(--color-secondary);
        margin: 0.25rem 0;
    }
    
    .availability-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.5rem 0.5rem 0.5rem 0;
    }
    
    .available {
        background-color: #d4edda;
        color: #155724;
    }
    
    .unavailable {
        background-color: #f8d7da;
        color: #721c24;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: var(--color-primary);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-family: 'Libre Baskerville', serif;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: var(--color-secondary);
    }
    
    .secondary-btn {
        background-color: var(--color-light) !important;
        color: var(--color-primary) !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)
st.title("Mi titulo nuevo")
user_type = st.session_state.get("user_type", "")
nombre = st.session_state.get("nombre", "Usuario")
