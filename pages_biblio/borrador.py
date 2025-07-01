import sys
import os
import streamlit as st
from datetime import datetime
from functions import get_loans, get_requested_loans_with_order, marcar_todos_prestamos_vencidos
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def prestamos_biblio():
    """Página para mostrar TODOS los préstamos de la biblioteca"""

    # --- NUEVO: Actualizar préstamos vencidos antes de mostrar ---
    marcar_todos_prestamos_vencidos()
    # --- FIN NUEVO ---

    # Inicializar session state para el botón de modificar
    if "modificar_prestamo_id" not in st.session_state:
        st.session_state.modificar_prestamo_id = None

    # Barra de búsqueda
    search_query = st.text_input("🔎 Buscar por título, ID libro o nombre de usuario", "")


    # Obtener todos los préstamos
    loans = get_loans()

    if loans is not None and not loans.empty:
        # Filtrar según búsqueda si hay texto de búsqueda
        if search_query:
            loans_filtered = loans[
                loans['titulo'].str.contains(search_query, case=False, na=False) |
                loans['id_libro'].astype(str).str.contains(search_query, case=False, na=False) |
                loans['nombre'].str.contains(search_query, case=False, na=False)
            ]
        else:
            loans_filtered = loans
        
        if loans_filtered.empty and search_query:
            st.warning("No se encontraron préstamos que coincidan con la búsqueda.")
            return

        # Mostrar cantidad total de préstamos
        st.markdown(f"<div style='font-size:1.1rem; margin-bottom:0.5em;'><strong>Cantidad total de préstamos: {len(loans_filtered)}</strong></div>", unsafe_allow_html=True)

        estados = ["activo", "vencido", "solicitado"]
        titulos = ["Activos", "Vencidos", "Solicitados"]
        col1, col2, col3 = st.columns(3)
        columnas = [col1, col2, col3]

        for idx, estado in enumerate(estados):
            with columnas[idx]:
                # Título de columna con color según estado
                if estado == "activo":
                    st.success(f"### {titulos[idx]}")
                elif estado == "vencido":
                    st.error(f"### {titulos[idx]}")
                else:
                    st.warning(f"### {titulos[idx]}")
                # Mostrar cantidad de préstamos de este estado
                if estado != "solicitado":
                    prestamos_estado = loans_filtered[loans_filtered['estado'].str.lower() == estado]
                    st.markdown(f"Cantidad: <strong>{len(prestamos_estado)}</strong>", unsafe_allow_html=True)
                    if not prestamos_estado.empty:
                        for i, row in prestamos_estado.iterrows():
                            st.markdown(
                                "<div class=\"prestamo-card\">"
                                "<div class=\"prestamo-content\">"
                                f"<p><strong>Título:</strong> {row['titulo']}</p>"
                                f"{'<p><strong>Autor:</strong> ' + str(row['autor']) + '</p>' if 'autor' in row and pd.notna(row['autor']) else ''}"
                                f"<p><strong>Usuario:</strong> {row['nombre']} (DNI: {row['dni']})</p>"
                                f"<p><strong>ID Libro:</strong> {row['id_libro']}</p>"
                                f"<p><strong>Fecha de préstamo:</strong> {row['fecha_prestamo']}</p>"
                                f"<p><strong>Fecha de devolución:</strong> {row['fecha_devolucion']}</p>"
                                "</div></div>",
                                unsafe_allow_html=True
                            )
                            
                            # Botones para activos y vencidos
                            if estado in ["activo", "vencido"]:
                                key_dev = f"dev_{row['id_libro']}_{row['dni']}_{estado}"
                                if st.button("Libro devuelto", key=key_dev):
                                    from functions import libro_devuelto_func
                                    exito = libro_devuelto_func(row['id_libro'])
                                    if exito:
                                        st.success("Libro devuelto correctamente. Si había alguien en lista de espera, se activó su préstamo.")
                                    else:
                                        st.error("Error al procesar la devolución del libro.")
                else:
                    # Mostrar solicitados con orden_de_llegada
                    solicitados = get_requested_loans_with_order()
                    if solicitados is not None and not solicitados.empty:
                        # Aplicar filtro de búsqueda también a los solicitados
                        if search_query:
                            solicitados_filtered = solicitados[
                                solicitados['titulo'].str.contains(search_query, case=False, na=False) |
                                solicitados['id_libro'].astype(str).str.contains(search_query, case=False, na=False) |
                                solicitados['nombre'].str.contains(search_query, case=False, na=False)
                            ]
                        else:
                            solicitados_filtered = solicitados
                        st.markdown(f"Cantidad: <strong>{len(solicitados_filtered)}</strong>", unsafe_allow_html=True)
                        if not solicitados_filtered.empty:
                            for i, row in solicitados_filtered.iterrows():
                                orden = ""
                                if 'orden_de_llegada' in row and not pd.isna(row['orden_de_llegada']):
                                    orden = f"<p><strong>Orden en lista de espera:</strong> {row['orden_de_llegada']}</p>"
                                st.markdown(
                                    "<div class=\"prestamo-card\">"
                                    "<div class=\"prestamo-content\">"
                                    f"<p><strong>Título:</strong> {row['titulo']}</p>"
                                    f"{'<p><strong>Autor:</strong> ' + str(row['autor']) + '</p>' if 'autor' in row and pd.notna(row['autor']) else ''}"
                                    f"<p><strong>Usuario:</strong> {row['nombre']} (DNI: {row['dni']})</p>"
                                    f"<p><strong>ID Libro:</strong> {row['id_libro']}</p>"
                                    f"{orden}"
                                    "</div></div>",
                                    unsafe_allow_html=True
                                )
                        else:
                            st.info("No hay préstamos solicitados que coincidan con la búsqueda.")
                    else:
                        st.info("No hay préstamos solicitados.")
    else:
        st.info("No hay préstamos registrados en la biblioteca.")

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
            color: var(--color-primary);
        }

        /* Estilos para las tarjetas de préstamos */
        .prestamo-card {
            background-color: white;
            border: 2px solid var(--color-light);
            border-radius: 10px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(117, 81, 14, 0.1);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            height: auto;
            min-height: 150px;
        }

        .prestamo-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(117, 81, 14, 0.15);
        }

        .prestamo-content {
            padding: 1rem;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .prestamo-content p {
            margin: 0.3rem 0;
            font-size: 0.9rem;
            line-height: 1.4;
        }

        .prestamo-content p:last-child {
            margin-bottom: 0;
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
    """, unsafe_allow_html=True) ##