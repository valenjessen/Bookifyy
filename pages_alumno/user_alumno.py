#FUNCIONA EN EL TEST, ACA NO, ARREGLAR (asumo que no esta bien definido para ingresar la info, porque devuelve vacio, osea no entiende)
#CHEQUEAR EL CAMBIADO DE CONTRASENA

import streamlit as st
from functions import get_user_complete_info, update_user_password, update_user_academic_info

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

            with st.form("academic_info_form"):
                col1, col2 = st.columns(2)

                with col1:
                    facultad_input = st.text_input("Facultad", value=facultad_actual, placeholder="Ej: Facultad de Ingeniería")

                with col2:
                    carrera_input = st.text_input("Carrera", value=carrera_actual, placeholder="Ej: Ingeniería Informática")

                submitted_academic = st.form_submit_button("Guardar información académica")

                if submitted_academic:
                    
                    if facultad_input and carrera_input:
                        try:
                            success = update_user_academic_info(facultad_input, carrera_input, mail_usuario)
                            if success:
                                st.success("✅ Información académica actualizada correctamente")
                                st.session_state["facultad"] = facultad_input
                                st.session_state["carrera"] = carrera_input
                                st.rerun()
                            else:
                                st.error("❌ No se pudo actualizar la información académica.")
                        except Exception as e:
                            st.error(f"❌ Error al actualizar la información: {str(e)}")
                    else:
                        st.error("Por favor completa ambos campos")

        st.markdown("---")

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
                                success = update_user_password(mail_usuario, new_password)
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