import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#from functions import get_user_loans
#from functions import extend_loan

def mis_prestamos_alumno():
    """Página para mostrar los préstamos del alumno"""
    
    # Verificar si el usuario está autenticado
    if 'mail_institucional' not in st.session_state:
        st.error("Por favor, inicia sesión para ver tus préstamos.")
        return
    
    mail_usuario = st.session_state['mail_institucional']
    nombre_usuario = st.session_state.get('nombre', 'Usuario')
    

    # Contenedor de bienvenida
    st.markdown("""
        <div class="welcome-container">
            <div class="welcome-message">Tus Préstamos Actuales</div>
            <div class="welcome-subtitle">Aquí puedes ver y gestionar tus préstamos.</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Botón de usuario en la esquina superior derecha
    st.markdown("""
        <div class="user-button-container">
            <button class="user-button">👤</button>
        </div>
    """, unsafe_allow_html=True)
    
    # Mostrar los préstamos del usuario
    display_user_loans(mail_usuario)

    # --- CSS Styling ---
    st.markdown("""
        <style>
        /* Importar Libre Baskerville */
        @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');
    
        /* Colores de la marca */
        :root {
          --color-primary: #75510e;
         --color-secondary: #b9985a;
         --color-light: #f5e0b9;
         --color-lightest: #fef8ee;
        }
    
        /* Aplicar fuente y colores generales */
        .stApp {
            background-color: var(--color-lightest);
            color: var(--color-primary);
            font-family: 'Libre Baskerville', serif;
        }
    
        .logo-title {
            font-size: 3rem;
            font-weight: 700;
            margin: 0;
            font-family: 'Libre Baskerville', serif;
            text-align: center;
        }
        .logo-subtitle {
            font-size: 1.2rem;
            margin: 0.5rem 0 0 0;
            opacity: 0.9;
            text-align: center;
        }
    
        .welcome-container {
            display: flex;
            justify-content: center;
            align-items: center;
                height: 60vh;
            text-align: center;
        }
    
        .welcome-message {
            font-size: 2.5rem;
            font-weight: 700;
            color: white;
            margin-bottom: 1rem;
        }
    
        .welcome-subtitle {
            font-size: 1.2rem;
            opacity: 0.8;
            color: white;
        }
    
    
        /* Botones personalizados */
        .stButton > button {
            background-color: #b9985a;   /* fixed */
            color: white;                /* for contrast */
            border: none;
            border-radius: 8px;
            padding: 0.75rem 2rem;
            font-family: 'Libre Baskerville', serif;
            font-weight: 600;
            width: 100%;
            transition: all 0.3s ease;
        }
    
        .stButton > button:hover {
        background-color: #75510e;   /* fixed */
        color: white;
        transform: translateY(-2px);
        }
    
        /* Inputs personalizados */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select {
            border: 2px solid var(--color-light);
            border-radius: 8px;
            padding: 0.75rem;
            font-family: 'Libre Baskerville', serif;
        }
    
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {
            border-color: var(--color-primary);
            box-shadow: 0 0 0 3px rgba(117, 81, 14, 0.1);
        }
    
        /* Radio buttons */
        .stRadio > div {
            background-color: var(--color-light);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
    
        /* Formulario */
        .stForm {
            background-color: var(--color-lightest);
            padding: 2rem;
            border-radius: 10px;
            border: 1px solid var(--color-light);
        }
    
        /* Mensajes de éxito y error */
        .stSuccess {
            background-color: #d4edda;
            border-color: #c3e6cb;
            color: #155724;
        }
    
        .stError {
            background-color: #f8d7da;
            border-color: #f5c6cb;
            color: #721c24;
        }

        /* Sidebar personalizado */
        section[data-testid="stSidebar"] {
            background-color: #b9985a !important;
        }
    
        /* Ocultar elementos innecesarios */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    
        .sidebar-greeting {
            color: white !important;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

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