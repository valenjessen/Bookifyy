import streamlit as st

# Importar solo las funciones necesarias inicialmente
from functions import add_person, verify_credentials, get_user_info, verify_credentials_with_type

# NO importar las páginas aquí - las importaremos dinámicamente cuando sea necesario

# --- Page Configuration ---
st.set_page_config(
    page_title="Bookify - Sistema de gestión bibliotecaria",
    page_icon="📚",
    layout="centered"
)

# IMPORTANTE: Limpiar completamente la sesión si hay inconsistencias
if st.button("🔄 Reiniciar Página", key="reset_app"):
    st.session_state.clear()
    st.rerun()

# Inicializar variables de sesión FORZANDO valores por defecto
if "logged_in" not in st.session_state or st.session_state.logged_in is None:
    st.session_state.logged_in = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# DEBUG: Mostrar estado actual (comentar en producción)
# st.sidebar.write("DEBUG - Estado actual:", st.session_state)


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
        color: var(--color-primary);
        margin-bottom: 1rem;
    }
    
    .welcome-subtitle {
        font-size: 1.2rem;
        opacity: 0.8;
        color: var(--color-secondary);
    }
    
    /* Botón de usuario en la esquina superior derecha */
    .user-button-container {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 999;
    }
    
    .user-button {
        background-color: #b9985a;
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        font-size: 1.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .user-button:hover {
        background-color: #75510e;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
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
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# LÓGICA PRINCIPAL DE LA APLICACIÓN
# =============================================================================

# Verificar explícitamente el estado de login
print(f"Estado de login: {st.session_state.logged_in}")  # Para debug en consola

if not st.session_state.logged_in:
    # --- PÁGINA DE LOGIN/SIGNUP ---
    
    # Header
    st.markdown("""
        <div class="header-container">
            <h1 class="logo-title"> bookify</h1>
            <p class="logo-subtitle">Sistema de gestión bibliotecaria</p>
            <p style="margin-top: 1rem; font-size: 1rem; text-align: center;">Universidad Austral</p>
        </div>
    """, unsafe_allow_html=True)
    
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
                    try:
                        # Primero crear el usuario en la base de datos
                        add_person(dni, user_type, name, password, mail, gender)
                        
                        # Configurar sesión EXPLÍCITAMENTE
                        st.session_state.logged_in = True
                        st.session_state.mail_institucional = mail
                        st.session_state.nombre = name
                        st.session_state.sexo = gender
                        st.session_state.user_type = user_type
                        st.session_state.dni = dni
                        st.session_state.current_page = "home"
                        
                        if gender == "Masculino":
                            st.session_state.welcome_message = f"Bienvenido, {name}"
                        elif gender == "Femenino":
                            st.session_state.welcome_message = f"Bienvenida, {name}"
                        else:
                            st.session_state.welcome_message = f"Bienvenido/a, {name}"
                        
                        st.success("¡Usuario creado con éxito! Redirigiendo...")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al crear el usuario: {str(e)}")
                else:
                    st.error("Por favor completar todos los campos.")
    
    else:  # "Ya tengo una cuenta"
        st.subheader("Log In")
        
        with st.form("login_form"):
            login_mail = st.text_input("mail", placeholder="you@mail.austral.edu.ar")
            login_password = st.text_input("Contraseña", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Clasificación**")
            with col2:
                user_classification = st.selectbox("", ["Alumno/Profesor", "Bibliotecario"], label_visibility="collapsed")
            
            login_submitted = st.form_submit_button("Log in")
            
            if login_submitted:
                if login_mail and login_password:
                    try:
                        if verify_credentials_with_type(login_mail, login_password, user_classification):
                            user_info = get_user_info(login_mail)
                            
                            # Configurar sesión EXPLÍCITAMENTE
                            st.session_state.logged_in = True
                            st.session_state.mail_institucional = login_mail
                            st.session_state.nombre = user_info.get("nombre", "Usuario")
                            st.session_state.sexo = user_info.get("sexo", "")
                            st.session_state.user_type = user_classification
                            st.session_state.current_page = "home"
                            
                            if user_info.get("sexo") == "Masculino":
                                st.session_state.welcome_message = f"Bienvenido, {user_info.get('nombre')}"
                            elif user_info.get("sexo") == "Femenino":
                                st.session_state.welcome_message = f"Bienvenida, {user_info.get('nombre')}"
                            else:
                                st.session_state.welcome_message = f"Bienvenido/a, {user_info.get('nombre')}"
                            
                            st.success("¡Inicio de sesión exitoso! Redirigiendo...")
                            st.rerun()
                        else:
                            st.error("Credenciales incorrectas. Por favor, intente nuevamente.")
                    except Exception as e:
                        st.error(f"Error al iniciar sesión: {str(e)}")
                else:
                    st.error("Por favor ingrese sus credenciales.")
        
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- USUARIO LOGUEADO ---
    
    user_type = st.session_state.get("user_type", "")
    nombre = st.session_state.get("nombre", "Usuario")
    
    # Botón de usuario en la esquina superior derecha (se mantiene en todas las páginas)
    st.markdown("""
        <div class="user-button-container">
    """, unsafe_allow_html=True)
    
    if st.button("👤", key="user_profile_btn", help="Mi perfil"):
        st.session_state.current_page = "user"
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #f5e0b9; /* Cambia este color a gusto */
        }
    </style>
    """,
    unsafe_allow_html=True
)

    # Sidebar con navegación
    with st.sidebar:
        st.markdown(f"### Hola, {nombre}")
        st.markdown("---")
        
        if st.button("🏠 Inicio", use_container_width=True, key="nav_home"):
            st.session_state.current_page = "home"
            st.rerun()
        
        if st.button("📚 Buscar libros", use_container_width=True, key="nav_search"):
            st.session_state.current_page = "search"
            st.rerun()
            
        if st.button("🤝 Préstamos", use_container_width=True, key="nav_loans"):
            st.session_state.current_page = "loans"
            st.rerun()
            
        st.markdown("---")
        
        if st.button("🔓 Log Out", use_container_width=True, key="nav_logout"):
            # Limpiar TODAS las variables de sesión
            st.session_state.clear()
            st.rerun()
    
    # Contenido principal basado en la página actual
    current_page = st.session_state.get("current_page", "home")
    
    if current_page == "home":
        # --- PÁGINA DE INICIO ---
        st.markdown(f"""
            <div class="welcome-container">
                <div>
                    <h2 class="welcome-message">{st.session_state.get('welcome_message', '¡Bienvenido/a!')}</h2>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Mostrar información del usuario (aquí no cambia nada)
        col1, col2, col3 = st.columns([1, 2, 1])
    
    elif current_page == "search":
        # --- PÁGINA DE BÚSQUEDA ---
        st.title("📚 Buscar libros")
        st.markdown("Encuentra el libro que necesitas")
        
        try:
            if user_type == "Bibliotecario":
                # Importar y ejecutar la vista de búsqueda para bibliotecario
                from pages_biblio.busqueda_libros_biblio import busqueda_libros_biblio
                busqueda_libros_biblio()
            else:
                # Importar y ejecutar la vista de búsqueda para alumno
                from pages_alumno.busqueda_libros_alumno import busqueda_libros_alumno
                busqueda_libros_alumno()
        except Exception as e:
            st.error("Error al cargar la página de búsqueda")
            st.error(f"Detalle del error: {str(e)}")
            st.session_state.current_page = "home"
            if st.button("Volver al inicio"):
                st.rerun()
    
    elif current_page == "loans":
        # --- PÁGINA DE PRÉSTAMOS ---
        st.title("🤝 Préstamos")
        
        try:
            if user_type == "Bibliotecario":
                st.markdown("Gestión de préstamos")
                # Importar y ejecutar la vista de préstamos (bibliotecario)
                from pages_biblio.prestamos_biblio import prestamos_biblio
                prestamos_biblio()
            else:
                
                # Importar y ejecutar la vista de préstamos (alumno)
                from pages_alumno.mis_prestamos_alumno import mis_prestamos_alumno
                mis_prestamos_alumno()
        except Exception as e:
            st.error("Error al cargar la página de préstamos")
            st.error(f"Detalle del error: {str(e)}")
            st.session_state.current_page = "home"
            if st.button("Volver al inicio"):
                st.rerun()
    
    elif current_page == "user":
        # --- PÁGINA DE USUARIO ---
        try:
            if user_type == "Bibliotecario":
                from pages_biblio.user_biblio import user_biblio
                user_biblio()
            else:
                from pages_alumno.user_alumno import user_alumno
                user_alumno()
        except Exception as e:
            st.error("Error al cargar la página de usuario")
            st.error(f"Detalle del error: {str(e)}")
            st.session_state.current_page = "home"
            if st.button("Volver al inicio"):
                st.rerun()
