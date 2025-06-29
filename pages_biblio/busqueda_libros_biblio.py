import streamlit as st
from functions import execute_query, get_libro_by_id, update_numero_copias_disponibles

def busqueda_libros_biblio():
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
        }
        
        .logo-title {
            font-size: 3rem;
            font-weight: 700;
            margin: 0;
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

    user_type = st.session_state.get("user_type", "")
    nombre = st.session_state.get("nombre", "Usuario")
    email = st.session_state.get("email", "")
    user_dni = st.session_state.get("dni", "")

    import pandas as pd

    # Barra de búsqueda
    search_query = st.text_input("🔎 Buscar por título, autor o editorial", "")
    st.title("Catálogo de Libros")
    

    # Inicializar session state
    if "selected_book" not in st.session_state:
        st.session_state.selected_book = None
    if "show_details" not in st.session_state:
        st.session_state.show_details = False

    # Obtener todos los libros (con cache para evitar recargas)
    @st.cache_data
    def get_books():
        query = "SELECT * FROM libros ORDER BY titulo"
        return execute_query(query, params=None, is_select=True)

    df = get_books()

    # Filtrar según búsqueda
    if search_query:
        df = df[
            df['titulo'].str.contains(search_query, case=False, na=False) |
            df['autor'].str.contains(search_query, case=False, na=False) |
            df['editoria_edicion'].str.contains(search_query, case=False, na=False)
        ]

    if not df.empty:
        st.write(f"*{len(df)} libros disponibles*")
        st.markdown("---")
        
        libros = df.to_dict("records")
        n = 3  # libros por fila

        for i in range(0, len(libros), n):
            fila = libros[i:i+n]
            cols = st.columns(n)
            for j, libro in enumerate(fila):
                with cols[j]:
                    #st.image("https://via.placeholder.com/150x200/cccccc/666666?text=Sin+Portada", width=150)
                    st.markdown(f"*{libro['titulo']}*")
                    st.markdown(f"por {libro['autor']}")
                    if libro['disponibilidad']:
                        st.success("✅ Disponible")
                    else:
                        st.error("❌ No disponible")
                    if st.button(f"Ver detalles", key=f"btn_{libro['id_libro']}"):
                        st.session_state.selected_book = libro['id_libro']
                        st.session_state.show_details = True
                        st.rerun()
            # Mostrar detalles si el libro seleccionado está en esta fila
            if (
                st.session_state.get("show_details", False)
                and any(libro['id_libro'] == st.session_state.get("selected_book") for libro in fila)
            ):
                libro_detalle = next(libro for libro in fila if libro['id_libro'] == st.session_state.get("selected_book"))
                # Obtener datos actualizados del libro
                libro_db = get_libro_by_id(libro_detalle['id_libro'])
                if libro_db is not None and not libro_db.empty:
                    libro_detalle = libro_db.iloc[0]
                st.markdown("---")
                with st.container():
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        url_portada = libro_detalle.get("url_portada") if isinstance(libro_detalle, dict) else libro_detalle["url_portada"]
                        if not url_portada or str(url_portada).lower() == "null":
                            url_portada = "https://via.placeholder.com/200x300/cccccc/666666?text=Sin+Portada"
                        st.image(url_portada, width=200)
                    with col2:
                        st.markdown(f"### {libro_detalle['titulo']}")
                        st.markdown(f"*Autor:* {libro_detalle['autor']}")
                        st.markdown(f"*Editorial/Edición:* {libro_detalle['editoria_edicion']}")
                        st.markdown(f"*Biblioteca:* {libro_detalle['biblioteca']}")
                        st.markdown(f"*Ubicación:* {libro_detalle['ubicacion']}")
                        st.markdown(f"*ID:* {libro_detalle['id_libro']}")
                        st.markdown(f"**Número de copias:** {libro_detalle['numero_de_copias']}")
                        st.markdown(f"**Copias disponibles:** {libro_detalle['numero_de_copias_disponibles']}")
                        st.markdown(f"**Disponibilidad:** {'✅ Disponible' if libro_detalle['disponibilidad'] else '❌ No disponible'}")
                    if st.button("⬅️ Volver al catálogo", key=f"volver_{libro_detalle['id_libro']}"):
                        st.session_state.selected_book = None
                        st.session_state.show_details = False
                        st.rerun()
                st.markdown("---")
    else:
        st.warning("No se ha encontrado ningún libro con esa búsqueda.")
