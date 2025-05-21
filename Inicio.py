import streamlit as st
from supabase import create_client, Client
from functions import add_person
from functions import verify_credentials
from functions import get_user_info

##COSAS DE ANTES DE EL ARCHIVO APP
# Configurar conexión a Supabase
# url="https://adudbqxlncpmkaphctho.supabase.co"
# key= "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFkdWRicXhsbmNwbWthcGhjdGhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ4MjU1NzAsImV4cCI6MjA2MDQwMTU3MH0.3N9v48CgDMtqBUw268vIp5ZhiAop-ceofPIYpvhCneE"
# supabase: Client = create_client(url, key)

# Ejemplo: mostrar datos de una tabla
#def cargar_datos():
    # response = supabase.table("nombre_de_tu_tabla").select("*").execute()
    # return response.data

# Streamlit UI
# st.title("Mi App con Supabase")
# datos = cargar_datos()
# st.write(datos)


#PARTE NUEVA
# --- Page Configuration (Optional but Recommended) ---
st.set_page_config(
    page_title="Bookify - Login",
    page_icon="🛒",
    layout="centered" # "wide" or "centered"
)
import streamlit as st
from streamlit_option_menu import option_menu

import streamlit as st

import streamlit as st

st.markdown("""
    <style>
    /* Cambiar color del texto general de la app */
    .stApp {
        color: #75510e !important;
    }

    /* Personalizar el ícono de hamburguesa */
    [data-testid="collapsedControl"]::before {
        content: "\\2261";  /* Unicode para ≡ */
        font-size: 24px;
        color: #31333F;
        position: relative;
        top: 2px;
        left: 2px;
        font-weight: bold;
    }

    /* Cambiar fondo y texto del sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f5e0b9;
        color: #75510e !important;
    }
    </style>
""", unsafe_allow_html=True)


# --- Main Application ---
st.title("Sign Up")

# Check if the user is already logged in (using session state)
if not st.session_state.get("logged_in", False):
    # Option to login or register
    login_option = st.radio("", ["Crear nueva cuenta", "Ya tengo una cuenta"], horizontal=True)
    
    if login_option == "Crear nueva cuenta":
        # If not logged in, show the signup form
        with st.form("signup_form"):
            mail = st.text_input("Mail institucional (@austral.edu.ar)")
            name = st.text_input("Nombre y Apellido")
            gender= st.selectbox("Sexo", ["-", "Masculino", "Femenino"])
            dni = st.text_input("DNI")
            user_type = st.selectbox("Tipo de usuario", ["-", "Estudiante", "Docente", "Bibliotecario"])
            password = st.text_input("Contraseña", type="password")
            submitted = st.form_submit_button("Sign up")
            stay_signed_in = st.checkbox("Mantener sesión iniciada")
            if submitted:
                # For this demo, any username/password is accepted
                if mail and password and name and dni and user_type != "-":
                    st.session_state["logged_in"] = True
                    st.session_state["mail_institucional"] = mail  # Optional: store username
                    st.session_state["nombre"] = name  # Store the user's name
                    st.session_state["sexo"] = gender
                    if gender == "Masculino":
                        st.session_state["welcome_message"] = f"Bienvenido, {name}"
                    elif gender == "Femenino":
                        st.session_state["welcome_message"] = f"Bienvenida, {name}"
                    st.success(f"¡Usuario creado con exito!")  # Mostrar el mensaje de bienvenida
                else:
                    st.error("Por favor completar todos los campos.")
        add_person(dni, user_type, name, password, mail, gender)  # Call the function to add the user to the database
    
    else:  # "Ya tengo una cuenta"
        # Show login form for existing users
        with st.form("login_form"):
            login_mail = st.text_input("Mail institucional (@austral.edu.ar)")
            login_password = st.text_input("Contraseña", type="password")
            login_submitted = st.form_submit_button("Iniciar sesión")
            stay_signed_in = st.checkbox("Mantener sesión iniciada")
            
            if login_submitted:
                if login_mail and login_password:
                    # Aquí verificarías las credenciales contra tu base de datos
                    if verify_credentials(login_mail, login_password):  # Función que deberás implementar
                        # Obtener datos del usuario
                        user_info = get_user_info(login_mail)  # Función que deberás implementar
                        
                        st.session_state["logged_in"] = True
                        st.session_state["mail_institucional"] = login_mail
                        st.session_state["nombre"] = user_info.get("nombre", "Usuario")
                        st.session_state["sexo"] = user_info.get("sexo", "")
                        
                        # Establecer mensaje de bienvenida según género
                        if user_info.get("sexo") == "Masculino":
                            st.session_state["welcome_message"] = f"Bienvenido, {user_info.get('nombre')}"
                        elif user_info.get("sexo") == "Femenino":
                            st.session_state["welcome_message"] = f"Bienvenida, {user_info.get('nombre')}"
                        else:
                            st.session_state["welcome_message"] = f"Bienvenido/a, {user_info.get('nombre')}"
                            
                        st.success("¡Inicio de sesión exitoso!")
                    else:
                        st.error("Credenciales incorrectas. Por favor, intente nuevamente.")
                else:
                    st.error("Por favor ingrese su mail y contraseña.")
else:
    # If logged in, show a welcome message
    st.success(st.session_state.get("welcome_message", "¡Bienvenido/a!"))
    st.info("Navega utilizando el menú lateral.")
    #st.balloons() # Fun little animation

    # Optional: Add a logout button
    if st.button("Logout"):
        del st.session_state["logged_in"]
        if "mail_institucional" in st.session_state:
            del st.session_state["mail_institucional"]