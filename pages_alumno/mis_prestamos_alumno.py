import sys
import os
import streamlit as st
from datetime import datetime
from functions import get_user_loans, get_user_requested_loans_with_order, get_user_complete_info, execute_query

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def mis_prestamos_alumno():
    """Página para mostrar los préstamos del alumno"""

    # Usar la clave correcta para el email
    email_usuario = st.session_state.get('mail_institucional', None)
    if not email_usuario:
        st.error("No se encontró el email del usuario en la sesión. Por favor, vuelve a iniciar sesión.")
        st.stop()

    # Obtener el dni a partir del email usando la función de functions.py
    user_info = get_user_complete_info(email_usuario)
    if user_info is not None and not user_info.empty:
        dni_usuario = user_info.iloc[0]['dni']
        nombre_usuario = user_info.iloc[0].get('nombre', 'Usuario')
    else:
        st.error("No se pudo obtener la información del usuario.")
        st.stop()

    # --- NUEVO: Actualizar préstamos vencidos antes de mostrar ---
    from functions import marcar_prestamos_vencidos  # Asegúrate de tener esta función en functions.py
    marcar_prestamos_vencidos(dni_usuario)
    # --- FIN NUEVO ---

    # Mensajes informativos más chicos y con menos espacio
    st.markdown(
        "<div style='font-size:1.1rem; margin-bottom:0.1em; font-weight:600;'>Tus Préstamos Actuales</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div style='font-size:0.95rem; margin-bottom:0.5em; margin-top:0em;'>Aquí puedes ver y gestionar tus préstamos.</div>",
        unsafe_allow_html=True
    )

    # Mostrar los préstamos del usuario en columnas por estado
    loans = get_user_loans(dni_usuario)
    if loans is not None and not loans.empty:
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
                    # Cambiar a warning (amarillo) para solicitados
                    st.warning(f"### {titulos[idx]}")
                
                if estado != "solicitado":
                    prestamos_estado = loans[loans['estado'].str.lower() == estado]
                    if not prestamos_estado.empty:
                        for i, row in prestamos_estado.iterrows():
                            # Contenedor enmarcado para cada préstamo
                            st.markdown(f"""
                                <div class="prestamo-card">
                                    <div class="prestamo-content">
                                        <p><strong>Título:</strong> {row['titulo']}</p>
                                        {'<p><strong>Autor:</strong> ' + str(row['autor']) + '</p>' if 'autor' in row else ''}
                                        <p><strong>Fecha de préstamo:</strong> {row['fecha_prestamo']}</p>
                                        <p><strong>Fecha de devolución:</strong> {row['fecha_devolucion']}</p>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            # --- Botón pedir extensión ---
                            key_ext = f"ext_{row['id_libro']}_{dni_usuario}_{estado}"
                            if st.button("Pedir extensión", key=key_ext):
                                # Chequear si hay algún préstamo solicitado para este libro
                                query_check = "SELECT COUNT(*) as cantidad FROM prestamo WHERE id_libro = %s AND LOWER(estado) = 'solicitado'"
                                result = execute_query(query_check, (row['id_libro'],), is_select=True)
                                if result is not None and not result.empty and int(result.iloc[0]['cantidad']) > 0:
                                    st.warning("No se puede extender el préstamo: hay solicitudes pendientes para este libro.")
                                else:
                                    from datetime import datetime, timedelta
                                    nueva_fecha = datetime.now().date() + timedelta(days=7)
                                    query_update = "UPDATE prestamo SET fecha_devolucion = %s, estado = 'activo' WHERE id_libro = %s AND dni = %s AND (LOWER(estado) = 'activo' OR LOWER(estado) = 'vencido')"
                                    execute_query(query_update, (nueva_fecha, row['id_libro'], dni_usuario), is_select=False)
                                    st.success("¡Préstamo extendido exitosamente!")
                else:
                    # Mostrar solicitados con orden_de_llegada
                    solicitados = get_user_requested_loans_with_order(dni_usuario)
                    if solicitados is not None and not solicitados.empty:
                        for i, row in solicitados.iterrows():
                            # Contenedor enmarcado para cada préstamo solicitado
                            st.markdown(f"""
                                <div class="prestamo-card">
                                    <div class="prestamo-content">
                                        <p><strong>Título:</strong> {row['titulo']}</p>
                                        {'<p><strong>Autor:</strong> ' + str(row['autor']) + '</p>' if 'autor' in row else ''}
                                        <p><strong>Orden en lista de espera:</strong> {row['orden_de_llegada']}</p>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                           
                    else:
                        st.info("No tienes préstamos solicitados.")
    else:
        st.info("No tienes préstamos registrados.")

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
            min-height: 120px;
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
    """, unsafe_allow_html=True)