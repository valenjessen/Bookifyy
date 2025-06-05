import streamlit as st
import os
import sys

# Inserta en sys.path la carpeta padre de pages_alumno,
# es decir: …\CDpM1\Bookifyy
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from functions import update_user_academic_info, get_user_complete_info

facultad_actual='Facultad de Ingeniería'
carrera_actual='Ingeniería Informática'
mail_usuario='vjessen@mail.austral.edu.ar'

st.title("Prueba Form")



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