import streamlit as st
import inicio2

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

with st.sidebar:
    st.markdown("### Menú Principal")
    if st.button("🏠 Inicio", use_container_width=True):
        inicio2.py.mostrar()
        
    
    if st.button("📚 Buscar libros", use_container_width=True):
        st.session_state.vista="busqueda_libros_alumno.py"
    
    if st.button("🤝 Préstamos", use_container_width=True):
        st.session_state.vista="mis_prestamos_alumno.py"
    
    st.markdown("---")
    if st.button("🔓 Log Out", use_container_width=True):
        st.session_state.clear()

with st.container():
    col1, col2, col3 = st.columns([8, 1, 1])
    with col3:
        if st.button("👤", key="user_button", help="Perfil de Usuario"):
            st.session_state.show_profile = True