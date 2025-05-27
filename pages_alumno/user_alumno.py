import streamlit as st

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


