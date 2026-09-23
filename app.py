import streamlit as st
import pandas as pd
import os

# Configuración de la pestaña del navegador
st.set_page_config(
    page_title="Verificación y Certificación de Egresados - FOAL-MEC-2026",
    page_icon="🎓",
    layout="centered"
)

# --- ESTILOS VISUALES PARA LA INTERFAZ ---
st.markdown("""
    <html lang="es" class="notranslate" translate="no">
    <head>
        <meta name="google" content="notranslate" />
    </head>
    <style>
    .main-title {
        color: #0F172A;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle {
        color: #475569;
        font-size: 15px;
        text-align: center;
        margin-bottom: 25px;
    }
    .footer {
        text-align: center;
        color: #94A3B8;
        font-size: 12px;
        margin-top: 15px;
    }
    /* Tarjeta de datos para copiar */
    .datos-box {
        background-color: #F1F5F9;
        border: 1px dashed #64748B;
        padding: 15px;
        border-radius: 6px;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    /* Estilo personalizado: Letra Roja, Calibri, Tamaño Aumentado (24px) */
    .stCheckbox > label > div[data-testid="stMarkdownContainer"] > p {
        font-family: 'Calibri', sans-serif !important;
        color: #DC2626 !important;
        font-size: 24px !important;
        font-weight: bold !important;
        line-height: 1.3 !important;
    }
    /* Estilo para el botón verde de WhatsApp */
    .btn-whatsapp {
        display: inline-block;
        background-color: #25D366;
        color: white !important;
        font-weight: bold;
        text-decoration: none;
        padding: 14px 28px;
        border-radius: 8px;
        text-align: center;
        font-size: 16px;
        margin-top: 10px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        transition: background-color 0.3s ease;
    }
    .btn-whatsapp:hover {
        background-color: #128C7E;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado visual actualizado para el curso FOAL-MEC-2026
st.markdown('<div class="main-title">🎓 Curso FOAL-MEC-2026: Consulta de Nómina y Solicitud de Certificado</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ingrese su número de cédula para verificar su condición de egreso y gestionar su certificado</div>', unsafe_allow_html=True)

# --- CONFIGURACIÓN DEL ARCHIVO EXCEL ---
EXCEL_FILE = "nomina_egresados.xlsx"

@st.cache_data
def cargar_datos(ruta_archivo):
    try:
        # Se asegura la lectura de la cédula como texto limpio
        df = pd.read_excel(ruta_archivo, dtype={'Cédula de identidad': str})
        df['Cédula de identidad'] = df['Cédula de identidad'].astype(str).str.strip()
        return df, None
    except Exception as e:
        return None, str(e)

# Control de existencia del archivo Excel
if not os.path.exists(EXCEL_FILE):
    st.info(f"💡 Configuración Inicial: Asegúrate de guardar tu archivo Excel con el nombre '{EXCEL_FILE}' en la misma carpeta.")
    st.stop()

# Carga automática del archivo
df_egresados, error_carga = cargar_datos(EXCEL_FILE)

if error_carga:
    st.error(f"❌ Error al abrir el archivo de datos: {error_carga}")
    st.stop()

# Validación de las columnas requeridas
columnas_requeridas = ['Nombres', 'Apellidos', 'Cédula de identidad', 'Fecha de culminación']
columnas_faltantes = [col for col in columnas_requeridas if col not in df_egresados.columns]

if columnas_faltantes:
    st.error(f"❌ Al archivo Excel le faltan las siguientes columnas obligatorias: {', '.join(columnas_faltantes)}")
    st.stop()

# --- INTERFAZ DE BÚSQUEDA ---
with st.form(key="formulario_egresados"):
    cedula_usuario = st.text_input(
        "Número de Cédula de Identidad:",
        placeholder="Ej: 1004944 (ingrese solo números)",
        help="Introduzca su número de documento sin puntos, comas ni guiones."
    )
    
    boton_consultar = st.form_submit_button(label="🔍 Verificar Egreso")

# --- PROCESAMIENTO DE LA CONSULTA ---
if boton_consultar or st.session_state.get('verificado', False):
    cedula_limpia = cedula_usuario.strip().replace(".", "").replace("-", "")
    
    if not cedula_limpia:
        st.warning("⚠️ Por favor, digite un número de cédula válido para realizar la verificación.")
    else:
        resultado = df_egresados[df_egresados['Cédula de identidad'] == cedula_limpia]
        
        if not resultado.empty:
            st.session_state['verificado'] = True
            
            datos_alumno = resultado.iloc[0]
            nombres_alumno = datos_alumno['Nombres']
            apellidos_alumno = datos_alumno['Apellidos']
            cedula_alumno = datos_alumno['Cédula de identidad']
            
            # Formateo visual de la fecha de culminación
            fecha_culminacion = datos_alumno['Fecha de culminación']
            if pd.notnull(fecha_culminacion):
                if isinstance(fecha_culminacion, pd.Timestamp):
                    fecha_str = fecha_culminacion.strftime('%d/%m/%Y')
                else:
                    fecha_str = str(fecha_culminacion).split()[0]
            else:
                fecha_str = "No registrada"
            
            st.success("✅ ¡Estudiante Verificado! Usted figura correctamente en el registro oficial de egresados.")
            
            # Cuadro de visualización de datos institucional
            st.markdown("### 📋 Información Registrada del Egresado:")
            st.write(f"**Nombres:** {nombres_alumno}")
            st.write(f"**Apellidos:** {apellidos_alumno}")
            st.write(f"**Cédula de Identidad:** {cedula_alumno}")
            st.write(f"**Fecha de Culminación:** {fecha_str}")
            
            st.markdown("---")
            
            # --- PASOS NUMERADOS PARA LA SOLICITUD DE CERTIFICADO ---
            st.markdown("### 📜 Pasos a seguir:")
            
            st.markdown("""
            1. **Confirmar la exactitud de datos** (verifique que sus nombres, apellidos, cédula y fecha de culminación sean correctos).
            2. **Copiar el texto de los datos** (no hacer captura de pantalla).
            3. **Ingresar a la Comunidad de Aprendizaje** (WhatsApp).
            4. **Pegar en el chat de la comunidad los datos** (únicamente texto).
            5. **Esperar que el equipo de soporte reporte** que ya está matriculado/a en el aula.
            6. **Ingresar a M360° + Clic en MIS CURSOS + Completar encuesta + Descargar certificado**.
            7. **Agradecer y abandonar la Comunidad de Aprendizaje**.
            """)
            
            # Bloque de texto listo para copiar
            texto_copiar = (
                f"SOLICITUD DE CERTIFICADO DE EGRESO:\n"
                f"• Curso: FOAL-MEC-2026\n"
                f"• Nombres: {nombres_alumno}\n"
                f"• Apellidos: {apellidos_alumno}\n"
                f"• Cédula: {cedula_alumno}\n"
                f"• Culminación: {fecha_str}\n"
                f"• Estado: VERIFICADO Y CONFIRMADO"
            )
            st.markdown(f'<div class="datos-box"><code style="color: #0F172A; font-weight: bold; white-space: pre-wrap;">{texto_copiar}</code></div>', unsafe_allow_html=True)
            
            # Casilla de confirmación con tipografía ampliada
            confirmado = st.checkbox("👉 RECONOZCO QUE MIS DATOS ESTÁN CORRECTOS Y DESEO DESCARGAR EL CERTIFICADO.")
            
            # Enlace a la comunidad de WhatsApp
            ENLACE_GRUPO_WHATSAPP = "https://chat.whatsapp.com/LguFT9oElAHAv6wrSsTD4P"

            if confirmado:
                st.success("🎉 Datos confirmados con éxito. Puede unirse a la Comunidad de Aprendizaje.")
                st.markdown(f'<a href="{ENLACE_GRUPO_WHATSAPP}" target="_blank" class="btn-whatsapp">💬 Ingresar a la Comunidad de Aprendizaje (WhatsApp)</a>', unsafe_allow_html=True)
            else:
                st.warning("🔒 El botón de acceso a la comunidad permanecerá bloqueado hasta que marque la casilla roja de confirmación.")
            
        else:
            st.session_state['verificado'] = False
            st.error("❌ El número de cédula ingresado NO se encuentra en la nómina oficial de egresados.")
            
            # Aviso actualizado con la fecha de corte
            st.info("ℹ️ El presente reporte contempla a los estudiantes que han concluido satisfactoriamente sus estudios hasta el **05 de agosto de 2026**. Si culminó posteriormente, sus datos se procesarán en la próxima emisión. Para consultas adicionales, contacte al soporte de M360°.")

# Pie de página institucional
st.markdown("---")
st.markdown('<div class="footer">Sistema Seguro de Validación y Certificación de Egresados © 2026</div>', unsafe_allow_html=True)
