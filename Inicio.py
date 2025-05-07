import streamlit as st
from supabase import create_client, Client
from functions import add_persona

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

# --- Main Application ---
st.title("Sign Up")

# Check if the user is already logged in (using session state)
if not st.session_state.get("logged_in", False):
    # If not logged in, show the login form
    with st.form("login_form"):
        mail_institucional = st.text_input("Mail institucional (@austral.edu.ar)")
        nombre = st.text_input("Nombre y Apellido")
        sexo = st.selectbox("Sexo", ["-", "Masculino", "Femenino"])
        dni = st.text_input("DNI")
        user_type = st.selectbox("Tipo de usuario", ["-", "Estudiante", "Docente", "Bibliotecario"])
        contrasena = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Login")
        stay_signed_in = st.checkbox("Mantener sesión iniciada")
        if submitted:
            # For this demo, any username/password is accepted
            if mail_institucional and contrasena and nombre and dni and user_type != "-":
                st.session_state["logged_in"] = True
                st.session_state["mail_institucional"] = mail_institucional  # Optional: store username
                st.session_state["nombre"] = nombre  # Store the user's name
                st.session_state["sexo"] = sexo
                if sexo == "Masculino":
                    st.session_state["welcome_message"] = f"Bienvenido, {nombre}"
                elif sexo == "Femenino":
                    st.session_state["welcome_message"] = f"Bienvenida, {nombre}"
                st.success(f"¡Usuario creado con exito!")  # Mostrar el mensaje de bienvenida
            else:
                st.error("Por favor completar todos los campos.")
    add_persona(dni, user_type, nombre, contrasena, mail_institucional)  # Call the function to add the user to the database
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