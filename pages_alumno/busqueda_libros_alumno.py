###PARTE INICIAL DE CODIGO      

# import sys
# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from functions import search_books
# from functions import get_book_details

# def display_search_results(search_term):
#     """
#     Display search results based on search term.
#     """
#     results = search_books(search_term)
#     # Format and display results
#     # Display availability, location, etc.

# def display_book_details(numero_de_id):
#     """
#     Display detailed information about a book.
#     """
#     book = get_book_details(numero_de_id)
#     # Format and display book details
#     # Include buttons for requesting loan or joining waiting list

###PARTE FRONT CLAUDE

import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Bookify - Buscar Libros",
    page_icon="🔍",
    layout="wide"
)

# --- CSS Styling ---
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

# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
    
    # Logo small
    st.markdown("### bookify")
    st.markdown("*Sistema de gestión bibliotecaria*")
    
    st.markdown("---")
    
    # User info
    user_name = st.session_state.get("nombre", "Usuario")
    st.markdown(f"**{user_name}**")
    st.markdown("Alumno")
    
    st.markdown("---")
    
    # Navigation
    if st.button("🏠 Inicio", use_container_width=True):
        st.switch_page("app.py")
    
    if st.button("🔍 Buscar libros", use_container_width=True, type="primary"):
        pass  # Already on this page
    
    if st.button("📚 Préstamos", use_container_width=True):
        st.switch_page("pages/mis_prestamos_alumno.py")
    
    st.markdown("---")
    
    if st.button("👤 Perfil", use_container_width=True):
        st.switch_page("pages/usuario_alumno.py")
    
    if st.button("🚪 Log Out", use_container_width=True, type="secondary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("app.py")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Main Content ---
# Header
st.markdown(f"""
    <div class="page-header">
        <div>
            <h2 style="margin: 0;">Buscar libros</h2>
            <p style="margin: 0; opacity: 0.9;">Encuentra el libro que necesitas</p>
        </div>
        <div>
            <p style="margin: 0;">Bienvenido/a</p>
            <h3 style="margin: 0;">{user_name}</h3>
        </div>
    </div>
""", unsafe_allow_html=True)

# Search Section
st.markdown('<div class="search-container">', unsafe_allow_html=True)

search_query = st.text_input("", placeholder="Busque su título o autor aquí", label_visibility="collapsed")

col1, col2 = st.columns([1, 4])
with col1:
    search_button = st.button("🔍 Buscar", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Mock search results - Replace with actual database query
if search_query or st.session_state.get("show_results", False):
    if search_query:
        st.session_state["show_results"] = True
        st.session_state["current_search"] = search_query
    
    current_search = st.session_state.get("current_search", "")
    
    if current_search:
        st.markdown(f"**Mostrando resultados para \"{current_search}\"**")
        
        # Mock books data
        books = [
            {
                "titulo": "La Odisea",
                "autor": "Homero",
                "editorial": "La estación",
                "año": "2005",
                "sede": "Sede Pilar, biblioteca del edificio de grado",
                "ubicacion": "Estante A-2",
                "copias_disponibles": 3,
                "copias_totales": 5
            },
            {
                "titulo": "La Odisea",
                "autor": "Homero", 
                "editorial": "Bibliok 1",
                "año": "2010",
                "sede": "Sede Pilar, biblioteca del edificio de grado",
                "ubicacion": "Estante A-3",
                "copias_disponibles": 0,
                "copias_totales": 2
            }
        ]
        
        for book in books:
            st.markdown('<div class="book-card">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f'<div class="book-title">{book["titulo"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="book-info"><strong>Autor:</strong> {book["autor"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="book-info"><strong>Editorial:</strong> {book["editorial"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="book-info"><strong>Año:</strong> {book["año"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="book-info"><strong>Ubicación:</strong> {book["sede"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="book-info"><strong>Estante:</strong> {book["ubicacion"]}</div>', unsafe_allow_html=True)
            
            with col2:
                if book["copias_disponibles"] > 0:
                    st.markdown(f'<div class="availability-badge available">Copias disponibles: {book["copias_disponibles"]}</div>', 
                              unsafe_allow_html=True)
                    if st.button(f"📖 Solicitar préstamo", key=f"request_{book['titulo']}_{book['editorial']}"):
                        st.success(f"Préstamo solicitado para: {book['titulo']}")
                        st.info("Se te notificará cuando esté listo para retirar.")
                else:
                    st.markdown('<div class="availability-badge unavailable">Copias disponibles: 0</div>', 
                              unsafe_allow_html=True)
                    if st.button(f"⏳ Lista de espera", key=f"waitlist_{book['titulo']}_{book['editorial']}"):
                        st.success(f"Agregado a lista de espera para: {book['titulo']}")
                        st.info("Se te avisará cuando hayan copias disponibles")
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("---")
    
    else:
        st.info("Ingresa un término de búsqueda para encontrar libros.")

else:
    # Welcome message when no search
    st.markdown("""
        ### 👋 ¡Bienvenido al sistema de búsqueda!
        
        Utiliza la barra de búsqueda para encontrar libros por:
        - **Título del libro**
        - **Nombre del autor**
        - **Editorial**
        
        Una vez que encuentres el libro que buscas, podrás:
        - ✅ Solicitar un préstamo si hay copias disponibles
        - ⏳ Unirte a la lista de espera si no hay copias disponibles
        - 📍 Ver la ubicación exacta del libro en la biblioteca
    """)
    
    # Show some featured books
    st.markdown("### 📚 Libros populares")
    
    featured_books = [
        "La Odisea - Homero",
        "Rayuela - Julio Cortázar", 
        "A buen fin no hay mal principio - W. Shakespeare",
        "A la deriva - Horacio Quiroga"
    ]
    
    for book in featured_books:
        st.markdown(f"• {book}")

# Check if user is logged in
if not st.session_state.get("logged_in", False):
    st.error("Debes iniciar sesión para acceder a esta página.")
    st.stop()