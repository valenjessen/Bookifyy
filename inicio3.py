import streamlit as st
from supabase import create_client, Client
from functions import add_person
from functions import verify_credentials
from functions import get_user_info
from pages_alumno import busqueda_libros_alumno, mis_prestamos_alumno, user_alumno
from pages_biblio import busqueda_libros_biblio, prestamos_biblio

# --- Page Configuration ---
st.set_page_config(
    page_title="Bookify - Sistema de gestión bibliotecaria",
    page_icon="📚",
    layout="centered"
)

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
    }
    
    .logo-subtitle {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    
    /* Botones personalizados */
    .stButton > button {
        background-color: var(--color-primary);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-family: 'Libre Baskerville', serif;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: var(--color-secondary);
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
    
    /* Ocultar elementos innecesarios */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div class="header-container">
        <h1 class="logo-title">bookify</h1>
        <p class="logo-subtitle">Sistema de gestión bibliotecaria</p>
        <p style="margin-top: 1rem; font-size: 1rem;">Universidad Austral</p>
    </div>
""", unsafe_allow_html=True)

# Check if the user is already logged in
if not st.session_state.get("logged_in", True):
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Option to login or register
    login_option = st.radio("", ["Crear nueva cuenta", "Ya tengo una cuenta"], horizontal=True)
    
    if login_option == "Crear nueva cuenta":
        st.subheader("Sign Up")
        
        with st.form("signup_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                mail = st.text_input("Mail institucional", placeholder="you@mail.austral.edu.ar")
                name = st.text_input("Nombre y Apellido")
                gender = st.selectbox("Sexo", ["-", "Masculino", "Femenino"])
            
            with col2:
                dni = st.text_input("DNI")
                user_type = st.selectbox("Rol", ["-", "Alumno/Profesor", "Bibliotecario"])
                password = st.text_input("Contraseña", type="password")
            
            submitted = st.form_submit_button("Sign up")
            
            if submitted:
                if mail and password and name and dni and user_type != "-":
                    st.session_state["logged_in"] = True
                    st.session_state["mail_institucional"] = mail
                    st.session_state["nombre"] = name
                    st.session_state["sexo"] = gender
                    st.session_state["user_type"] = user_type
                    st.session_state["dni"] = dni
                    
                    if gender == "Masculino":
                        st.session_state["welcome_message"] = f"Bienvenido, {name}"
                    elif gender == "Femenino":
                        st.session_state["welcome_message"] = f"Bienvenida, {name}"
                    else:
                        st.session_state["welcome_message"] = f"Bienvenido/a, {name}"
                    
                    st.success("¡Usuario creado con éxito!")
                    add_person(dni, user_type, name, password, mail, gender)
                    st.rerun()
                else:
                    st.error("Por favor completar todos los campos.")
    
    else:  # "Ya tengo una cuenta"
        st.subheader("Log In")
        
        with st.form("login_form"):
            login_mail = st.text_input("DNI o mail", placeholder="DNI o you@mail.austral.edu.ar")
            login_password = st.text_input("Contraseña", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Clasificación**")
            with col2:
                user_classification = st.selectbox("", ["Alumno/Profesor", "Bibliotecario"], label_visibility="collapsed")
            
            login_submitted = st.form_submit_button("Log in")
            
            if login_submitted:
                if login_mail and login_password:
                    if verify_credentials(login_mail, login_password):
                        user_info = get_user_info(login_mail)
                        
                        st.session_state["logged_in"] = True
                        st.session_state["mail_institucional"] = login_mail
                        st.session_state["nombre"] = user_info.get("nombre", "Usuario")
                        st.session_state["sexo"] = user_info.get("sexo", "")
                        st.session_state["user_type"] = user_classification
                        
                        if user_info.get("sexo") == "Masculino":
                            st.session_state["welcome_message"] = f"Bienvenido, {user_info.get('nombre')}"
                        elif user_info.get("sexo") == "Femenino":
                            st.session_state["welcome_message"] = f"Bienvenida, {user_info.get('nombre')}"
                        else:
                            st.session_state["welcome_message"] = f"Bienvenido/a, {user_info.get('nombre')}"
                        
                        st.success("¡Inicio de sesión exitoso!")
                        st.rerun()
                    else:
                        st.error("Credenciales incorretas. Por favor, intente nuevamente.")
                else:
                    st.error("Por favor ingrese sus credenciales.")
        
    st.markdown('</div>', unsafe_allow_html=True)

else:

    user_type = st.session_state.get("user_type", "")
    if user_type == "Bibliotecario":
        st.success(st.session_state.get("welcome_message", "¡Bienvenido/a!"))
        st.subheader("welcome message")
        with st.sidebar:
            st.markdown("### Menú Principal")
            if st.button("🏠 Inicio", use_container_width=True): current_page="home"
            if st.button("📚 Buscar libros", use_container_width=True): busqueda_libros_biblio.mostrar()
            if st.button("🤝 Préstamos", use_container_width=True): prestamos_biblio.mostrar()
            st.markdown("---")
            if st.button("🔓 Log Out", use_container_width=True):
                st.session_state.clear()
                st.rerun()
    else:
        st.success(st.session_state.get("welcome_message", "¡Bienvenido/a!"))
        st.subheader("welcome message")
        with st.sidebar:
            st.markdown("### Menú Principal")
            if st.button("🏠 Inicio", use_container_width=True): current_page="home"
            if st.button("📚 Buscar libros", use_container_width=True): busqueda_libros_alumno.mostrar()
            if st.button("🤝 Préstamos", use_container_width=True): mis_prestamos_alumno.mostrar()
            st.markdown("---")
            if st.button("🔓 Log Out", use_container_width=True):
                st.session_state.clear()
                st.rerun()
    
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("Logout", type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()





# else:
#     # If logged in, redirect based on user type
#     st.success(st.session_state.get("welcome_message", "¡Bienvenido/a!"))
    
#     user_type = st.session_state.get("user_type", "")
    
#     if user_type == "Bibliotecario":
#         st.info("Redirigiendo al panel de bibliotecario...")
#         st.markdown("**Funciones disponibles:**")
#         st.markdown("- Gestión de libros")
#         st.markdown("- Ver préstamos activos")
#         st.markdown("- Administrar listas de espera")
#     else:
#         st.info("Redirigiendo al panel de estudiante/profesor...")
#         st.markdown("**Funciones disponibles:**")
#         st.markdown("- Buscar libros")
#         st.markdown("- Solicitar préstamos")
#         st.markdown("- Ver mis préstamos")

#     with st.sidebar:
#             st.markdown("### Menú Principal")
#             if st.button("🏠 Inicio", use_container_width=True): st.session_state.current_page='home'
#             if st.button("📚 Buscar libros", use_container_width=True): st.session_state.current_page='search'
#             if st.button("🤝 Préstamos", use_container_width=True): st.session_state.current_page='loans'
#             st.markdown("---")
#             if st.button("🔓 Log Out", use_container_width=True):
#                 st.session_state.clear()
#                 st.rerun()

#     page = st.session_state.get('current_page','home')
#     user_type = st.session_state.get('user_type','')
    
#     if page == 'home':
#         st.markdown(f"<div style='display:flex;justify-content:center;align-items:center;height:70vh;'><h2>{st.session_state.get('welcome_message')}</h2></div>", unsafe_allow_html=True)
#     elif page == 'search':
#         if user_type == "Bibliotecario": busqueda_libros_biblio.mostrar()
#         else: busqueda_libros_alumno.mostrar()
#     elif page == 'loans':
#         if user_type == "Bibliotecario": prestamos_biblio.mostrar()
#         else: mis_prestamos_alumno.mostrar()
    
