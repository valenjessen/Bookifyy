import sys
import os
import streamlit as st

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
    
    import streamlit as st
from PIL import Image
import io

# Configuración de la página
st.set_page_config(
    page_title="Perfil de Usuario",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para el estilo
st.markdown("""
<style>
    /* Estilo general */
    .main {
        padding-top: 2rem;
    }
    
    /* Contenedor del botón de usuario en la esquina superior derecha */
    .user-button-container {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 999;
    }
    
    /* Estilo del perfil de usuario */
    .user-profile {
        background-color: #f8f6f0;
        padding: 2rem;
        border-radius: 10px;
        margin: 2rem 0;
    }
    
    /* Avatar del usuario */
    .user-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background-color: #d4c5a0;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
        font-size: 2rem;
        color: white;
    }
    
    /* Información del usuario */
    .user-info h2 {
        color: #8b7355;
        margin: 0.5rem 0;
        font-size: 1.5rem;
    }
    
    .user-info p {
        color: #8b7355;
        margin: 0.2rem 0;
        font-size: 1rem;
    }
    
    /* Formularios */
    .form-section {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
    }
    
    .form-title {
        color: #8b7355;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    /* Estilo para inputs */
    .stTextInput > div > div > input {
        border-radius: 20px;
        border: 2px solid #d4c5a0;
        padding: 0.5rem 1rem;
    }
    
    /* Botones */
    .stButton > button {
        background-color: #c4a772;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background-color: #b89660;
    }
</style>
""", unsafe_allow_html=True)

# Función para crear el botón de usuario en la esquina superior derecha
def create_user_button():
    # Aquí puedes usar tu propia imagen
    # Por ahora uso un emoji, pero puedes reemplazarlo con:
    # user_image = Image.open("path/to/your/user-button-image.png")
    # st.image(user_image, width=40)
    
    with st.container():
        col1, col2, col3 = st.columns([8, 1, 1])
        with col3:
            if st.button("👤", key="user_button", help="Perfil de Usuario"):
                st.session_state.show_profile = True

# Inicializar estados de sesión
if 'show_profile' not in st.session_state:
    st.session_state.show_profile = False


# Crear el botón de usuario
create_user_button()

# Sidebar (ya tienes esto implementado)
with st.sidebar:
    st.markdown("### Menú Principal")
    if st.button("🏠 Inicio", use_container_width=True):
        st.session_state.show_profile = False
        st.session_state.show_change_password = False
    
    if st.button("📚 Buscar libros", use_container_width=True):
        st.session_state.show_profile = False
        st.session_state.show_change_password = False
    
    if st.button("🤝 Préstamos", use_container_width=True):
        st.session_state.show_profile = False
        st.session_state.show_change_password = False
    
    st.markdown("---")
    if st.button("🔓 Log Out", use_container_width=True):
        st.session_state.clear()

# Contenido principal
if st.session_state.show_profile:
    st.title("Perfil de Usuario")
    
    # Perfil del usuario
    with st.container():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Avatar (puedes reemplazar con una imagen real)
            st.markdown("""
            <div class="user-avatar">
                👤
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="user-info">
                <h2>{st.session_state.user_name}</h2>
                <p>{st.session_state.user_type}</p>
                <p>{st.session_state.user_email}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Botón para cambiar contraseña
    col1, col2, col3 = st.columns([6, 2, 2])
    with col3:
        if st.button("Cambiar contraseña", key="change_password_btn"):
            st.session_state.show_change_password = not st.session_state.show_change_password
    
    st.markdown("---")
    
    # Formulario de información personal
    if not st.session_state.show_change_password:
        st.markdown('<div class="form-title">Información Personal</div>', unsafe_allow_html=True)
        
        with st.form("personal_info_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                facultad = st.text_input("Facultad", value="", placeholder="Ingrese su facultad")
            
            with col2:
                carrera = st.text_input("Carrera", value="", placeholder="Ingrese su carrera")
            
            submitted = st.form_submit_button("Guardar Cambios")
            
            if submitted:
                st.success("✅ Información actualizada correctamente")
    
    # Formulario de cambio de contraseña
    else:
        st.markdown('<div class="form-title">Cambiar Contraseña</div>', unsafe_allow_html=True)
        
        with st.form("change_password_form"):
            current_password = st.text_input("Contraseña actual", type="password", placeholder="Ingrese su contraseña actual")
            new_password = st.text_input("Nueva contraseña", type="password", placeholder="Ingrese su nueva contraseña")
            confirm_password = st.text_input("Repetir nueva contraseña", type="password", placeholder="Confirme su nueva contraseña")
            
            col1, col2, col3 = st.columns([6, 2, 2])
            with col2:
                submitted = st.form_submit_button("Cambiar contraseña")
            
            if submitted:
                if new_password != confirm_password:
                    st.error("❌ Las contraseñas no coinciden")
                elif len(new_password) < 6:
                    st.error("❌ La contraseña debe tener al menos 6 caracteres")
                else:
                    st.success("✅ Contraseña cambiada correctamente")
                    st.session_state.show_change_password = False

else:
    st.title("Bienvenido a la Biblioteca")
    st.write("Selecciona una opción del menú lateral para comenzar.")

# Información adicional sobre cómo usar tu propia imagen
st.markdown("""
---
### 📝 Notas para personalizar:

1. **Para usar tu propia imagen de botón de usuario:**
   ```python
   # Reemplaza la línea del botón emoji por:
   user_image = Image.open("ruta/a/tu/imagen.png")
   if st.button("", key="user_button", help="Perfil"):
       # Tu lógica aquí
   ```

2. **Para cambiar el avatar del usuario:**
   ```python
   # En lugar del emoji, usa:
   user_avatar = Image.open("ruta/a/avatar.png")
   st.image(user_avatar, width=80)
   ```

3. **El botón de usuario está fijo en la esquina superior derecha** y aparece en todas las vistas.

4. **Los estilos CSS** están configurados para que coincidan con el diseño mostrado en las imágenes.
""")