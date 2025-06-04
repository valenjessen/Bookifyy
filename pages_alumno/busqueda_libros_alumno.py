import streamlit as st

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

st.title("Mi titulo nuevo")
user_type = st.session_state.get("user_type", "")
nombre = st.session_state.get("nombre", "Usuario")


import pandas as pd
import streamlit as st
from functions import execute_query

st.title("Catálogo de Libros")

# Inicializar session state
if "selected_book" not in st.session_state:
    st.session_state.selected_book = None

# Obtener todos los libros (con cache para evitar recargas)
@st.cache_data
def get_books():
    query = "SELECT * FROM libros ORDER BY titulo"
    return execute_query(query, params=None, is_select=True)

df = get_books()

if not df.empty:
    st.write(f"**{len(df)} libros disponibles**")
    st.markdown("---")
    
    # Crear columnas para el layout de tarjetas
    cols = st.columns(3)  # 3 libros por fila
    
    for index, row in df.iterrows():
        col = cols[index % 3]  # Alternar entre las 3 columnas
        
        with col:
            # Crear una tarjeta para cada libro
            with st.container():
                # Imagen de portada (placeholder por ahora)
                st.image("https://via.placeholder.com/150x200/cccccc/666666?text=Sin+Portada", 
                        width=150)
                
                # Título del libro
                st.markdown(f"**{row['titulo']}**")
                
                # Autor
                st.markdown(f"*por {row['autor']}*")
                
                # Estado de disponibilidad
                if row['disponibilidad']:
                    st.success("✅ Disponible")
                else:
                    st.error("❌ No disponible")
                
                # Botón para ver detalles
                if st.button(f"Ver detalles", key=f"btn_{row['numero_de_id']}"):
                    st.session_state.selected_book = row['numero_de_id']
                    st.rerun()
                
                st.markdown("---")
    
    # Mostrar detalles del libro seleccionado
    if st.session_state.selected_book is not None:
        book_id = st.session_state.selected_book
        
        # Buscar el libro seleccionado
        selected_book = df[df['numero_de_id'] == book_id].iloc[0]
        
        st.markdown("## 📖 Detalles del Libro")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Portada más grande
            st.image("https://via.placeholder.com/200x300/cccccc/666666?text=Sin+Portada", 
                    width=200)
        
        with col2:
            st.markdown(f"### {selected_book['titulo']}")
            st.markdown(f"**Autor:** {selected_book['autor']}")
            st.markdown(f"**Editorial/Edición:** {selected_book['editoria_edicion']}")
            st.markdown(f"**Biblioteca:** {selected_book['biblioteca']}")
            st.markdown(f"**Ubicación:** {selected_book['ubicacion']}")
            st.markdown(f"**ID:** {selected_book['numero_de_id']}")
            
            # Estado
            if selected_book['disponibilidad']:
                st.success("✅ Libro disponible para préstamo")
                if st.button("📚 Solicitar préstamo"):
                    st.info("Funcionalidad de préstamo en desarrollo")
            else:
                st.error("❌ Libro no disponible")
                if st.button("⏰ Agregar a lista de espera"):
                    st.info("Funcionalidad de lista de espera en desarrollo")
        
        # Botón para volver
        if st.button("⬅️ Volver al catálogo"):
            st.session_state.selected_book = None
            st.rerun()

else:
    st.warning("No hay libros en la base de datos")