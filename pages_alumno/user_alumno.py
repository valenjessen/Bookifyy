#no cambia la contrasena en la base de datos

import streamlit as st
from functions import get_user_complete_info, update_user_password, update_user_academic_info, get_facultades, get_carreras_por_facultad

def user_alumno():
    """Página de perfil para alumnos"""

    # Obtener información del usuario actual
    mail_usuario = st.session_state.get("mail_institucional", "")
    nombre_usuario = st.session_state.get("nombre", "Usuario")
    sexo_usuario = st.session_state.get("sexo", "")
    user_type = st.session_state.get("user_type", "Alumno")

    # Validar que el mail esté presente
    if not mail_usuario:
        st.error("No se encontró el correo institucional del usuario en la sesión.")
        return

    # Obtener datos del usuario
    user_data = get_user_complete_info(mail_usuario)

    if user_data is not None and not user_data.empty:
        user_info = user_data.iloc[0]

        # Contenedor principal con el avatar
        col1, col2 = st.columns([1, 3])

        with col1:
            st.markdown("""
                <div style="
                    width: 120px; 
                    height: 120px; 
                    border-radius: 50%; 
                    background: linear-gradient(135deg, #b9985a, #75510e);
                    display: flex; 
                    align-items: center; 
                    justify-content: center; 
                    margin: 20px auto;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                ">
                    <div style="
                        color: white; 
                        font-size: 48px; 
                        font-weight: bold;
                        font-family: 'Libre Baskerville', serif;
                    ">👤</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div style="margin-top: 20px;">
                    <h2 style="color: #75510e; margin-bottom: 5px; font-family: 'Libre Baskerville', serif;">
                        {nombre_usuario}
                    </h2>
                    <p style="color: #b9985a; font-size: 1.1rem; margin-bottom: 5px;">
                        {user_type}
                    </p>
                    <p style="color: #75510e; font-size: 1rem; opacity: 0.8;">
                        {mail_usuario}
                    </p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Información académica
        facultad_actual = user_info['facultad'] if 'facultad' in user_info else ""
        carrera_actual = user_info['carrera'] if 'carrera' in user_info else ""

        if facultad_actual and carrera_actual:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                    <div style="
                        background-color: #f5e0b9; 
                        padding: 15px; 
                        border-radius: 10px; 
                        margin-bottom: 10px;
                    ">
                        <h4 style="color: #75510e; margin-bottom: 5px;">Facultad</h4>
                        <p style="color: #75510e; font-size: 1.1rem; margin: 0;">{facultad_actual}</p>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                    <div style="
                        background-color: #f5e0b9; 
                        padding: 15px; 
                        border-radius: 10px; 
                        margin-bottom: 10px;
                    ">
                        <h4 style="color: #75510e; margin-bottom: 5px;">Carrera</h4>
                        <p style="color: #75510e; font-size: 1.1rem; margin: 0;">{carrera_actual}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:

            st.markdown("**Completa tu información académica:**")

            facultades_df = get_facultades()
            facultades = facultades_df["facultad"].tolist() if not facultades_df.empty else []

            facultad_guardada = st.session_state.get("facultad_guardada", facultad_actual)
            carrera_guardada = st.session_state.get("carrera_guardada", carrera_actual)

            colf, colc = st.columns(2)

            with colf:
                facultad_select = st.selectbox(
                    "Facultad",
                    facultades,
                    index=facultades.index(facultad_guardada) if facultad_guardada in facultades else 0,
                    key="facultad_select"
                )
                guardar_facultad = st.button("Guardar facultad")
                if guardar_facultad:
                    st.session_state["facultad_guardada"] = facultad_select
                    st.session_state["carrera_guardada"] = ""  # Reset carrera al cambiar facultad
                    st.success("Facultad guardada. Ahora seleccioná tu carrera.")

            with colc:
                facultad_elegida = st.session_state.get("facultad_guardada", "")
                if facultad_elegida:
                    carreras_df = get_carreras_por_facultad(facultad_elegida)
                    carreras = carreras_df["carrera"].tolist() if not carreras_df.empty else []
                else:
                    carreras = []
                carrera_select = st.selectbox(
                    "Carrera",
                    carreras,
                    index=carreras.index(carrera_guardada) if carrera_guardada in carreras else 0,
                    key="carrera_select",
                    disabled=not facultad_elegida
                )
                guardar_carrera = st.button("Guardar carrera", disabled=not facultad_elegida)
                if guardar_carrera and facultad_elegida:
                    if carrera_select:
                        try:
                            success = update_user_academic_info(facultad_elegida, carrera_select, mail_usuario)
                            if success:
                                st.success("✅ Información académica actualizada correctamente")
                                st.session_state["carrera_guardada"] = carrera_select
                                st.session_state["facultad"] = facultad_elegida
                                st.session_state["carrera"] = carrera_select
                                st.rerun()
                            else:
                                st.error("❌ No se pudo actualizar la información académica.")
                        except Exception as e:
                            st.error(f"❌ Error al actualizar la información: {str(e)}")
                    else:
                        st.error("Por favor seleccioná una carrera")

        # Cambio de contraseña
        st.markdown("### 🔐 Cambiar Contraseña")

        if st.button("Cambiar contraseña", key="change_password_btn"):
            st.session_state.show_password_form = True

        if st.session_state.get("show_password_form", False):
            with st.form("password_change_form"):
                st.markdown("**Cambiar contraseña:**")

                current_password = st.text_input("Contraseña actual", type="password")
                new_password = st.text_input("Nueva contraseña", type="password")
                confirm_password = st.text_input("Repetir nueva contraseña", type="password")

                col1, col2 = st.columns(2)

                with col1:
                    submitted_password = st.form_submit_button("Cambiar contraseña")

                with col2:
                    if st.form_submit_button("Cancelar"):
                        st.session_state.show_password_form = False
                        st.rerun()

                if submitted_password:
                    if current_password and new_password and confirm_password:
                        current_user_password = user_info['contrasena'] if 'contrasena' in user_info else ''

                        if current_password != current_user_password:
                            st.error("❌ La contraseña actual no es correcta")
                        elif new_password != confirm_password:
                            st.error("❌ Las nuevas contraseñas no coinciden")
                        elif len(new_password) < 4:
                            st.error("❌ La nueva contraseña debe tener al menos 4 caracteres")
                        else:
                            try:
                                # CORRECCIÓN: el orden de los argumentos es (new_password, email)
                                success = update_user_password(new_password, mail_usuario)
                                if success:
                                    st.success("✅ Contraseña cambiada correctamente")
                                    st.session_state.show_password_form = False
                                    st.rerun()
                                else:
                                    st.error("❌ No se pudo cambiar la contraseña.")
                            except Exception as e:
                                st.error(f"❌ Error al cambiar la contraseña: {str(e)}")
                    else:
                        st.error("Por favor completa todos los campos")

    else:
        st.error("No se pudo cargar la información del usuario")

# Ejecutar la función
pass