"""
GENERADOR DE INFORMES DE LABORATORIO - UNJBG (APA 7.ª EDICIÓN)
Aplicación web interactiva construida en Python + Streamlit.
"""

import os
import json
import base64
import math
import pandas as pd
import streamlit as st

from modulos.plantilla_unjbg import (
    INSTITUCION,
    FACULTADES_SUGERIDAS,
    ESCUELAS_SUGERIDAS,
    REGLAS_APA7,
    GUIAS_SECCIONES,
)
from modulos.exportadores import (
    generar_docx_bytes,
    generar_markdown_str,
    generar_latex_str,
    generar_json_str,
)

st.set_page_config(
    page_title="Generador de Informes de Laboratorio - UNJBG (APA 7)",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS personalizados para vista académica y carátula centrada
st.markdown(
    """
    <style>
      .caratula-box {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        font-family: 'Times New Roman', Times, serif;
        margin-bottom: 1.5rem;
      }
      .caratula-uni {
        font-size: 1.45rem;
        font-weight: 800;
        color: #0f294a;
        margin-bottom: 0.4rem;
      }
      .caratula-sub {
        font-size: 1.05rem;
        color: #1e293b;
        margin: 0.2rem 0;
      }
      .caratula-banner {
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: 1px;
        color: #0f294a;
        border-top: 2px solid #0f294a;
        border-bottom: 2px solid #0f294a;
        padding: 0.45rem;
        margin: 1rem auto;
        max-width: 460px;
      }
      .guia-academica {
        background-color: #eff6ff;
        border-left: 4px solid #2563eb;
        padding: 0.7rem 1rem;
        border-radius: 0 6px 6px 0;
        font-size: 0.88rem;
        color: #1e3a8a;
        margin-bottom: 0.8rem;
      }
    </style>
    """,
    unsafe_allow_html=True,
)


def obtener_estado_inicial() -> dict:
    return {
        "caratula": {
            "facultad": "",
            "escuela": "",
            "laboratorio": INSTITUCION["laboratorio_defecto"],
            "tituloPractica": "",
            "grupo": "",
            "horario": "",
            "docente": "",
            "fechaEjecucion": "",
            "diaEntrega": "",
            "mesEntrega": "",
            "anioEntrega": INSTITUCION["anio_defecto"],
        },
        "autores": ["Apellidos y Nombres - Código Universitario"],
        "resumen": "",
        "introduccionTeoria": "",
        "objetivoGeneral": "",
        "objetivosEspecificos": [""],
        "materialesTexto": "",
        "tituloTablaMateriales": "Características técnicas de los dispositivos y equipos de medición empleados",
        "materialesTabla": [
            {"nombre": "", "marca": "", "rango": "", "apreciacion": "", "cantidad": "1"}
        ],
        "notaTablaMateriales": "Nota. Elaboración propia a partir de las especificaciones técnicas del laboratorio.",
        "procedimientoTexto": "",
        "figura1Desc": "Esquema del dispositivo experimental empleado en la práctica",
        "figura1Nota": "Nota. Montaje experimental realizado en el Laboratorio de Física de la UNJBG.",
        "figura1Img": "",
        "tituloTablaCruda": "Datos experimentales registrados directamente durante la medición",
        "tablaCruda": {
            "headers": ["Medición N°", "Magnitud X [unidad]", "Magnitud Y [unidad]"],
            "rows": [["1", "", ""], ["2", "", ""], ["3", "", ""]],
        },
        "notaTablaCruda": "Nota. Mediciones directas obtenidas sin procesamiento matemático.",
        "tituloTablaResultados": "Valores procesados, incertezas experimentales y comparación con el modelo teórico",
        "tablaResultados": {
            "headers": ["Ensayo", "Resultado ± Incerteza", "Valor Teórico", "Error Relativo (%)"],
            "rows": [["1", "", "", ""], ["2", "", "", ""]],
        },
        "notaTablaResultados": "Nota. Las incertezas fueron calculadas mediante propagación de errores.",
        "figura2Desc": "Relación experimental entre [Magnitud Y (unidad)] y [Magnitud X (unidad)]",
        "figura2Nota": "Nota. Ajuste lineal por mínimos cuadrados y = mx + b, R² = ...",
        "figura2Img": "",
        "discusionTexto": "",
        "conclusiones": [""],
        "fuentesError": "",
        "reflexionTexto": "",
        "referencias": [
            "Alonso, M., & Finn, E. J. (1986). Física: Vol. I. Mecánica. Fondo Educativo Interamericano."
        ],
        "cuestionario": [{"pregunta": "", "respuesta": ""}],
        "apendicesTexto": "",
    }


def cargar_ejemplo() -> dict:
    ej = obtener_estado_inicial()
    ej["caratula"] = {
        "facultad": "Facultad de Ingeniería (FAIN)",
        "escuela": "Ingeniería Ambiental",
        "laboratorio": "FÍSICA",
        "tituloPractica": "Determinación de la Aceleración de la Gravedad mediante el Péndulo Simple",
        "grupo": "A",
        "horario": "Lunes 14:00 - 16:00",
        "docente": "Dr. Juan Pérez Mamani",
        "fechaEjecucion": "12/11/2026",
        "diaEntrega": "19",
        "mesEntrega": "noviembre",
        "anioEntrega": "2026",
    }
    ej["autores"] = [
        "Quispe Flores, María Elena - 2025-119042",
        "Condori Mamani, Carlos Alberto - 2025-119058",
    ]
    ej["resumen"] = (
        "Se determinó experimentalmente la aceleración de la gravedad local en la ciudad de Tacna "
        "mediante el análisis del movimiento armónico simple de un péndulo ideal para oscilaciones de "
        "pequeña amplitud. Se midió el periodo de oscilación T para cinco longitudes de cuerda comprendidas "
        "entre 0.200 m y 1.000 m, registrando el tiempo de 20 oscilaciones completas con un cronómetro "
        "digital de 0.01 s de apreciación. Mediante ajuste lineal por mínimos cuadrados de T² en función "
        "de la longitud L, se obtuvo una pendiente de (4.03 ± 0.04) s²/m, de la cual se calculó una "
        "aceleración gravitacional experimental de g = (9.79 ± 0.10) m/s². Al comparar este resultado con "
        "el valor referencial teórico de 9.78 m/s², se determinó un error relativo porcentual de 0.10 %, "
        "verificando la validez de la relación cuadrática entre el periodo y la longitud del péndulo."
    )
    ej["introduccionTeoria"] = (
        "El estudio del movimiento oscilatorio constituye uno de los fundamentos de la mecánica clásica "
        "(Alonso & Finn, 1986). Un péndulo simple consiste en una masa puntual suspendida de un hilo "
        "inextensible y de masa despreciable. Según Serway y Jewett (2018), para desplazamientos angulares "
        "pequeños (θ < 10°), el movimiento se aproxima a un Movimiento Armónico Simple cuyo periodo T está dado por:\n\n"
        "T = 2π √(L / g)   (1)\n\n"
        "Elevando al cuadrado la ecuación (1), se obtiene la relación lineal:\n\n"
        "T² = (4π² / g) L   (2)"
    )
    ej["objetivoGeneral"] = (
        "Determinar experimentalmente el valor de la aceleración de la gravedad (g) mediante el estudio "
        "del periodo de oscilación de un péndulo simple."
    )
    ej["objetivosEspecificos"] = [
        "Verificar la dependencia lineal entre el cuadrado del periodo (T²) y la longitud del péndulo (L).",
        "Evaluar las incertezas experimentales asociadas a las mediciones directas e indirectas.",
    ]
    ej["materialesTabla"] = [
        {"nombre": "Cronómetro digital", "marca": "Casio HS-3", "rango": "0 - 999.99 s", "apreciacion": "0.01 s", "cantidad": "1"},
        {"nombre": "Wincha métrica", "marca": "Stanley", "rango": "0 - 3.000 m", "apreciacion": "0.001 m", "cantidad": "1"},
        {"nombre": "Esfera metálica", "marca": "Pasco", "rango": "50 g", "apreciacion": "0.1 g", "cantidad": "1"},
    ]
    ej["referencias"] = [
        "Alonso, M., & Finn, E. J. (1986). Física: Vol. I. Mecánica. Fondo Educativo Interamericano.",
        "Serway, R. A., & Jewett, J. W. (2018). Física para ciencias e ingeniería (10.ª ed., Vol. 1). Cengage Learning.",
    ]
    return ej


if "informe" not in st.session_state:
    st.session_state["informe"] = obtener_estado_inicial()

datos = st.session_state["informe"]
logo_path = INSTITUCION["logo_path"]

# --- BARRA LATERAL ---
with st.sidebar:
    if os.path.exists(logo_path):
        col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
        with col_l2:
            st.image(logo_path, width=95)

    st.markdown("### UNJBG • Laboratorio de Física")
    st.caption("Normativa: **APA 7.ª Edición**")

    mostrar_guias = st.toggle("Mostrar guías académicas APA 7", value=True)

    st.divider()
    st.markdown("#### Acciones Rápidas")
    if st.button("Cargar Ejemplo Completo", use_container_width=True):
        st.session_state["informe"] = cargar_ejemplo()
        st.rerun()

    if st.button("Limpiar Todo el Formulario", use_container_width=True):
        st.session_state["informe"] = obtener_estado_inicial()
        st.rerun()

    st.divider()
    st.markdown("#### Guardar o Actualizar Proyecto")
    json_str = generar_json_str(datos)
    st.download_button(
        label="Guardar Proyecto (.json)",
        data=json_str.encode("utf-8"),
        file_name="proyecto_informe_unjbg_apa7.json",
        mime="application/json",
        use_container_width=True,
    )

    archivo_json = st.file_uploader("Abrir Proyecto (.json) para actualizar", type=["json"])
    if archivo_json is not None:
        if st.button("Aplicar Proyecto Cargado", use_container_width=True):
            try:
                cargado = json.load(archivo_json)
                base = obtener_estado_inicial()
                base.update(cargado)
                st.session_state["informe"] = base
                st.success("Proyecto cargado correctamente.")
                st.rerun()
            except Exception as e:
                st.error(f"Error al leer el archivo JSON: {e}")

    st.divider()
    with st.expander("Reglas APA 7 Aplicadas"):
        for k, v in REGLAS_APA7.items():
            st.markdown(f"- **{k.replace('_', ' ').capitalize()}:** {v}")


def mostrar_guia(clave: str):
    if mostrar_guias and clave in GUIAS_SECCIONES:
        st.markdown(f'<div class="guia-academica"><strong>Guía APA 7.ª Ed.:</strong> {GUIAS_SECCIONES[clave]}</div>', unsafe_allow_html=True)


# --- ENCABEZADO PRINCIPAL Y DESCARGAS ---
st.title("Generador de Informes de Laboratorio - UNJBG")
st.markdown("Formato oficial de la **Universidad Nacional Jorge Basadre Grohmann** adaptado a **APA 7.ª Edición**.")

# Botones principales de descarga en la parte superior
col_d1, col_d2, col_d3 = st.columns(3)
docx_bytes = generar_docx_bytes(datos, logo_path=logo_path)
md_str = generar_markdown_str(datos)
tex_str = generar_latex_str(datos)

slug_nombre = (datos["caratula"]["tituloPractica"] or "informe_laboratorio_unjbg").strip().lower().replace(" ", "_")[:45]

with col_d1:
    st.download_button(
        label="Descargar Word APA 7 (.docx)",
        data=docx_bytes,
        file_name=f"{slug_nombre}_APA7.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        type="primary",
        use_container_width=True,
    )
with col_d2:
    st.download_button(
        label="Descargar LaTeX APA 7 (.tex)",
        data=tex_str.encode("utf-8"),
        file_name=f"{slug_nombre}_APA7.tex",
        mime="application/x-tex",
        use_container_width=True,
    )
with col_d3:
    st.download_button(
        label="Descargar Markdown (.md)",
        data=md_str.encode("utf-8"),
        file_name=f"{slug_nombre}.md",
        mime="text/markdown",
        use_container_width=True,
    )

st.divider()

# Pestañas organizadas por secciones del informe
tabs = st.tabs([
    "Carátula UNJBG",
    "1. Resumen",
    "2. Introducción",
    "3. Materiales y Método",
    "4. Resultados y Discusión",
    "5. Conclusiones",
    "6. Reflexión",
    "7. Referencias (APA 7)",
    "8. Cuestionario",
    "9. Apéndices",
])

# ==========================================
# TAB 0: CARÁTULA OFICIAL UNJBG
# ==========================================
with tabs[0]:
    st.subheader("Carátula Oficial del Informe de Laboratorio")
    c = datos["caratula"]

    col1, col2 = st.columns(2)
    with col1:
        fac_sel = st.selectbox(
            "Facultad (sugerida o escriba abajo):",
            ["(Personalizada)"] + FACULTADES_SUGERIDAS,
            index=0,
        )
        c["facultad"] = st.text_input(
            "Facultad:",
            value=c["facultad"] if fac_sel == "(Personalizada)" else fac_sel,
            placeholder="[Facultad correspondiente]",
        )

        esc_sel = st.selectbox(
            "Escuela Profesional (sugerida o escriba abajo):",
            ["(Personalizada)"] + ESCUELAS_SUGERIDAS,
            index=0,
        )
        c["escuela"] = st.text_input(
            "Escuela Profesional:",
            value=c["escuela"] if esc_sel == "(Personalizada)" else esc_sel,
            placeholder="[Ingeniería Ambiental / Física / etc.]",
        )

        c["laboratorio"] = st.text_input("Laboratorio de:", value=c["laboratorio"])
        c["tituloPractica"] = st.text_input("Título de la práctica:", value=c["tituloPractica"], placeholder="[Nombre de la práctica]")

    with col2:
        c["grupo"] = st.text_input("Grupo:", value=c["grupo"], placeholder="[ ]")
        c["horario"] = st.text_input("Horario:", value=c["horario"], placeholder="[ ]")
        c["docente"] = st.text_input("Docente:", value=c["docente"], placeholder="[Grado y Nombre]")
        c["fechaEjecucion"] = st.text_input("Fecha de ejecución:", value=c["fechaEjecucion"], placeholder="[dd/mm/2026]")

        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            c["diaEntrega"] = st.text_input("Día entrega:", value=c["diaEntrega"], placeholder="[día]")
        with col_f2:
            c["mesEntrega"] = st.text_input("Mes entrega:", value=c["mesEntrega"], placeholder="[mes]")
        with col_f3:
            c["anioEntrega"] = st.text_input("Año entrega:", value=c["anioEntrega"], placeholder="2026")

    st.markdown("#### Autores (Apellidos y Nombres - Código Universitario)")
    for idx, autor in enumerate(datos["autores"]):
        ca1, ca2 = st.columns([10, 1])
        with ca1:
            datos["autores"][idx] = st.text_input(
                f"Autor {idx + 1}",
                value=autor,
                key=f"autor_{idx}",
                label_visibility="collapsed",
                placeholder="Apellidos y Nombres - Código Universitario",
            )
        with ca2:
            if len(datos["autores"]) > 1 and st.button("✕", key=f"del_autor_{idx}"):
                datos["autores"].pop(idx)
                st.rerun()

    if st.button("+ Agregar Autor"):
        datos["autores"].append("")
        st.rerun()

    # Vista previa visual de la carátula con el logo centrado después de Escuela Profesional
    st.markdown("#### Vista Previa de la Carátula (Logo centrado después de Escuela Profesional)")
    logo_b64_html = ""
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as lf:
            b64 = base64.b64encode(lf.read()).decode("utf-8")
            logo_b64_html = f'<div style="text-align:center; margin: 14px auto;"><img src="data:image/png;base64,{b64}" width="115" alt="Escudo UNJBG" /></div>'

    autores_html = "<br/>".join([a for a in datos["autores"] if a.strip()]) or "Apellidos y Nombres - Código Universitario"
    st.markdown(
        f"""
        <div class="caratula-box">
          <div class="caratula-uni">UNIVERSIDAD NACIONAL JORGE BASADRE GROHMANN</div>
          <div class="caratula-sub"><strong>Facultad:</strong> {c['facultad'] or '[Facultad correspondiente]'}</div>
          <div class="caratula-sub"><strong>Escuela Profesional:</strong> {c['escuela'] or '[Ingeniería Ambiental / Física / etc.]'}</div>
          {logo_b64_html}
          <div class="caratula-sub"><strong>Laboratorio de:</strong> {c['laboratorio'] or 'FÍSICA'}</div>
          <div class="caratula-banner">INFORME DE LABORATORIO</div>
          <div style="text-align:left; max-width:600px; margin: 0 auto; line-height:1.7;">
            <p><strong>Título de la práctica:</strong> {c['tituloPractica'] or '[Nombre de la práctica]'}</p>
            <p><strong>Autores:</strong><br/>{autores_html}</p>
            <p><strong>Grupo:</strong> {c['grupo'] or '[ ]'} &nbsp;&nbsp;&nbsp;&nbsp; <strong>Horario:</strong> {c['horario'] or '[ ]'}</p>
            <p><strong>Docente:</strong> {c['docente'] or '[Grado y Nombre]'}</p>
            <p><strong>Fecha de ejecución:</strong> {c['fechaEjecucion'] or '[ ]'}</p>
            <p><strong>Fecha de entrega:</strong> Tacna, {c['diaEntrega'] or '[ ]'} de {c['mesEntrega'] or '[ ]'} de {c['anioEntrega'] or '2026'}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==========================================
# TAB 1: 1. RESUMEN
# ==========================================
with tabs[1]:
    st.subheader("1. Resumen")
    mostrar_guia("resumen")
    datos["resumen"] = st.text_area(
        "Redacción del Resumen (párrafo único sin sangría en APA 7):",
        value=datos["resumen"],
        height=220,
        placeholder="Redacte en tercera persona y tiempo pasado (~15 líneas). Se elabora al final del informe...",
    )
    lineas_aprox = math.ceil(len(datos["resumen"].strip()) / 85) if datos["resumen"].strip() else 0
    if 12 <= lineas_aprox <= 18:
        st.success(f"Extensión estimada: ~{lineas_aprox} líneas (dentro del rango recomendado de ~15 líneas).")
    else:
        st.info(f"Extensión estimada: ~{lineas_aprox} líneas (Meta recomendada: ~15 líneas).")

# ==========================================
# TAB 2: 2. INTRODUCCIÓN
# ==========================================
with tabs[2]:
    st.subheader("2. Introducción")
    mostrar_guia("introduccion")
    datos["introduccionTeoria"] = st.text_area(
        "Motivación y Base Teórica (ecuaciones numeradas (1), (2)... y citas APA 7 (Autor, Año)):",
        value=datos["introduccionTeoria"],
        height=240,
        placeholder="Exponga las motivaciones, marco teórico, ecuaciones numeradas y citas en formato APA 7...",
    )

    st.markdown("#### Objetivos: Generales y Específicos")
    datos["objetivoGeneral"] = st.text_area(
        "Objetivo General:",
        value=datos["objetivoGeneral"],
        height=80,
        placeholder="Determinar / Verificar / Estudiar...",
    )

    st.markdown("**Objetivos Específicos:**")
    for idx, obj in enumerate(datos["objetivosEspecificos"]):
        co1, co2 = st.columns([10, 1])
        with co1:
            datos["objetivosEspecificos"][idx] = st.text_input(
                f"Obj {idx+1}",
                value=obj,
                key=f"obj_esp_{idx}",
                label_visibility="collapsed",
                placeholder=f"Objetivo específico {idx + 1}...",
            )
        with co2:
            if len(datos["objetivosEspecificos"]) > 1 and st.button("✕", key=f"del_obj_{idx}"):
                datos["objetivosEspecificos"].pop(idx)
                st.rerun()

    if st.button("+ Agregar Objetivo Específico"):
        datos["objetivosEspecificos"].append("")
        st.rerun()

# ==========================================
# TAB 3: 3. MATERIALES Y DESARROLLO EXPERIMENTAL
# ==========================================
with tabs[3]:
    st.subheader("3. Materiales y Desarrollo Experimental")
    st.markdown("### 3.1 Materiales")
    mostrar_guia("materiales")

    datos["materialesTexto"] = st.text_area(
        "Descripción general de dispositivos, reactivos y equipos:",
        value=datos["materialesTexto"],
        height=100,
    )

    st.markdown("**Tabla 1** *(Formato APA 7: Número en negrita arriba, título en cursiva y sin líneas verticales)*")
    datos["tituloTablaMateriales"] = st.text_input("Título en cursiva de la Tabla 1:", value=datos["tituloTablaMateriales"])

    df_mat = pd.DataFrame(datos["materialesTabla"])
    df_mat_edit = st.data_editor(
        df_mat,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "nombre": "Equipo / Material",
            "marca": "Marca / Modelo",
            "rango": "Rango de medición",
            "apreciacion": "Apreciación / Incerteza",
            "cantidad": "Cantidad",
        },
        key="editor_materiales",
    )
    datos["materialesTabla"] = df_mat_edit.fillna("").to_dict(orient="records")
    datos["notaTablaMateriales"] = st.text_input("Nota al pie de Tabla 1 (APA 7):", value=datos["notaTablaMateriales"])

    st.divider()
    st.markdown("### 3.2 Procedimiento")
    mostrar_guia("procedimiento")

    datos["procedimientoTexto"] = st.text_area(
        "Descripción del método de medición en tiempo pasado:",
        value=datos["procedimientoTexto"],
        height=160,
    )

    st.markdown("**Figura 1** *(Esquema del dispositivo experimental - Formato APA 7)*")
    datos["figura1Desc"] = st.text_input("Título en cursiva de la Figura 1:", value=datos["figura1Desc"])
    up_fig1 = st.file_uploader("Subir imagen del esquema experimental (Figura 1)", type=["png", "jpg", "jpeg"], key="up_f1")
    if up_fig1 is not None:
        datos["figura1Img"] = base64.b64encode(up_fig1.read()).decode("utf-8")
    if datos["figura1Img"]:
        st.image(base64.b64decode(datos["figura1Img"]), caption=datos["figura1Desc"], width=360)
    datos["figura1Nota"] = st.text_input("Nota al pie de Figura 1 (APA 7):", value=datos["figura1Nota"])

    st.markdown("**Tabla 2** *(Datos experimentales tomados directamente, sin procesar - Formato APA 7)*")
    datos["tituloTablaCruda"] = st.text_input("Título en cursiva de la Tabla 2:", value=datos["tituloTablaCruda"])

    col_tc1, col_tc2 = st.columns([3, 1])
    with col_tc1:
        nueva_col_cruda = st.text_input("Nombre de nueva columna para Tabla 2 (opcional):", key="new_col_cruda")
    with col_tc2:
        st.write("")
        st.write("")
        if st.button("+ Añadir Columna T2") and nueva_col_cruda.strip():
            datos["tablaCruda"]["headers"].append(nueva_col_cruda.strip())
            for r in datos["tablaCruda"]["rows"]:
                r.append("")
            st.rerun()

    df_cruda = pd.DataFrame(datos["tablaCruda"]["rows"], columns=datos["tablaCruda"]["headers"])
    df_cruda_edit = st.data_editor(df_cruda, num_rows="dynamic", use_container_width=True, key="editor_cruda")
    datos["tablaCruda"]["headers"] = list(df_cruda_edit.columns)
    datos["tablaCruda"]["rows"] = df_cruda_edit.fillna("").values.tolist()
    datos["notaTablaCruda"] = st.text_input("Nota al pie de Tabla 2 (APA 7):", value=datos["notaTablaCruda"])

# ==========================================
# TAB 4: 4. RESULTADOS Y DISCUSIÓN
# ==========================================
with tabs[4]:
    st.subheader("4. Resultados y Discusión")
    mostrar_guia("resultados")

    st.markdown("**Tabla 3** *(Resultados procesados e incertezas - Formato APA 7)*")
    datos["tituloTablaResultados"] = st.text_input("Título en cursiva de la Tabla 3:", value=datos["tituloTablaResultados"])

    col_tr1, col_tr2 = st.columns([3, 1])
    with col_tr1:
        nueva_col_res = st.text_input("Nombre de nueva columna para Tabla 3 (opcional):", key="new_col_res")
    with col_tr2:
        st.write("")
        st.write("")
        if st.button("+ Añadir Columna T3") and nueva_col_res.strip():
            datos["tablaResultados"]["headers"].append(nueva_col_res.strip())
            for r in datos["tablaResultados"]["rows"]:
                r.append("")
            st.rerun()

    df_res = pd.DataFrame(datos["tablaResultados"]["rows"], columns=datos["tablaResultados"]["headers"])
    df_res_edit = st.data_editor(df_res, num_rows="dynamic", use_container_width=True, key="editor_res")
    datos["tablaResultados"]["headers"] = list(df_res_edit.columns)
    datos["tablaResultados"]["rows"] = df_res_edit.fillna("").values.tolist()
    datos["notaTablaResultados"] = st.text_input("Nota al pie de Tabla 3 (APA 7):", value=datos["notaTablaResultados"])

    st.divider()
    st.markdown("**Figura 2** *(Gráfica experimental con título, ejes con unidades, escalas y nota al pie)*")
    datos["figura2Desc"] = st.text_input("Título en cursiva de la Figura 2:", value=datos["figura2Desc"])
    up_fig2 = st.file_uploader("Subir imagen de la gráfica (Figura 2)", type=["png", "jpg", "jpeg"], key="up_f2")
    if up_fig2 is not None:
        datos["figura2Img"] = base64.b64encode(up_fig2.read()).decode("utf-8")
    if datos["figura2Img"]:
        st.image(base64.b64decode(datos["figura2Img"]), caption=datos["figura2Desc"], width=380)
    datos["figura2Nota"] = st.text_input("Nota al pie de Figura 2 (APA 7):", value=datos["figura2Nota"])

    datos["discusionTexto"] = st.text_area(
        "Discusión de resultados, evaluación de incertezas y comparación teórica (cite en APA 7):",
        value=datos["discusionTexto"],
        height=200,
    )

# ==========================================
# TAB 5: 5. CONCLUSIONES
# ==========================================
with tabs[5]:
    st.subheader("5. Conclusiones")
    mostrar_guia("conclusiones")

    for idx, concl in enumerate(datos["conclusiones"]):
        cc1, cc2 = st.columns([10, 1])
        with cc1:
            datos["conclusiones"][idx] = st.text_area(
                f"Conclusión {idx + 1}:",
                value=concl,
                height=80,
                key=f"concl_{idx}",
            )
        with cc2:
            if len(datos["conclusiones"]) > 1 and st.button("✕", key=f"del_concl_{idx}"):
                datos["conclusiones"].pop(idx)
                st.rerun()

    if st.button("+ Agregar Conclusión"):
        datos["conclusiones"].append("")
        st.rerun()

    datos["fuentesError"] = st.text_area(
        "Análisis de posibles fuentes de error y aproximaciones respecto al caso ideal:",
        value=datos["fuentesError"],
        height=120,
    )

# ==========================================
# TAB 6: 6. REFLEXIÓN ARGUMENTADA
# ==========================================
with tabs[6]:
    st.subheader("6. Reflexión Argumentada")
    mostrar_guia("reflexion")
    datos["reflexionTexto"] = st.text_area(
        "Relación de la teoría evaluada experimentalmente con el campo de acción profesional:",
        value=datos["reflexionTexto"],
        height=180,
    )

# ==========================================
# TAB 7: 7. REFERENCIAS (APA 7.ª EDICIÓN)
# ==========================================
with tabs[7]:
    st.subheader("7. Referencias (APA 7.ª Edición)")
    mostrar_guia("referencias")

    with st.expander("Asistente rápido para construir referencias APA 7.ª Edición", expanded=True):
        ca_1, ca_2, ca_3 = st.columns([2, 1, 2])
        with ca_1:
            apa_autor = st.text_input("Autor(es):", placeholder="Serway, R. A., & Jewett, J. W.")
        with ca_2:
            apa_anio = st.text_input("Año:", placeholder="2018")
        with ca_3:
            apa_titulo = st.text_input("Título:", placeholder="Física para ciencias e ingeniería")
        apa_fuente = st.text_input("Editorial / Revista / URL:", placeholder="Cengage Learning.")

        if st.button("Insertar Referencia APA 7 y Ordenar Alfabéticamente"):
            if apa_autor.strip() and apa_titulo.strip():
                nueva_ref = f"{apa_autor.strip()} ({apa_anio.strip() or 's.f.'}). {apa_titulo.strip()}. {apa_fuente.strip()}".strip()
                if len(datos["referencias"]) == 1 and not datos["referencias"][0].strip():
                    datos["referencias"][0] = nueva_ref
                else:
                    datos["referencias"].append(nueva_ref)
                datos["referencias"] = sorted([r for r in datos["referencias"] if r.strip()], key=lambda s: s.lower())
                st.rerun()

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        if st.button("+ Agregar Referencia Manual"):
            datos["referencias"].append("")
            st.rerun()
    with col_r2:
        if st.button("Ordenar Alfabéticamente (A-Z APA 7)"):
            datos["referencias"] = sorted([r for r in datos["referencias"] if r.strip()], key=lambda s: s.lower()) or [""]
            st.rerun()

    for idx, ref in enumerate(datos["referencias"]):
        cr1, cr2 = st.columns([10, 1])
        with cr1:
            datos["referencias"][idx] = st.text_input(
                f"Ref {idx + 1}",
                value=ref,
                key=f"ref_{idx}",
                label_visibility="collapsed",
                placeholder="Apellido, N. (Año). Título. Editorial.",
            )
        with cr2:
            if len(datos["referencias"]) > 1 and st.button("✕", key=f"del_ref_{idx}"):
                datos["referencias"].pop(idx)
                st.rerun()

# ==========================================
# TAB 8: 8. CUESTIONARIO
# ==========================================
with tabs[8]:
    st.subheader("8. Cuestionario")
    mostrar_guia("cuestionario")

    for idx, item in enumerate(datos["cuestionario"]):
        st.markdown(f"**Pregunta {idx + 1}**")
        cq1, cq2 = st.columns([10, 1])
        with cq1:
            item["pregunta"] = st.text_input(
                f"Enunciado {idx+1}",
                value=item.get("pregunta", ""),
                key=f"q_preg_{idx}",
                label_visibility="collapsed",
                placeholder="Escriba la pregunta planteada por el docente...",
            )
        with cq2:
            if len(datos["cuestionario"]) > 1 and st.button("✕", key=f"del_q_{idx}"):
                datos["cuestionario"].pop(idx)
                st.rerun()
        item["respuesta"] = st.text_area(
            f"Respuesta {idx + 1}:",
            value=item.get("respuesta", ""),
            height=100,
            key=f"q_resp_{idx}",
        )

    if st.button("+ Agregar Pregunta"):
        datos["cuestionario"].append({"pregunta": "", "respuesta": ""})
        st.rerun()

# ==========================================
# TAB 9: 9. APÉNDICES
# ==========================================
with tabs[9]:
    st.subheader("9. Apéndices")
    mostrar_guia("apendices")
    datos["apendicesTexto"] = st.text_area(
        "Cálculos detallados, propagación de incertezas y material complementario:",
        value=datos["apendicesTexto"],
        height=240,
    )
