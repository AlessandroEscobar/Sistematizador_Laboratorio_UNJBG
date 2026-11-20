# Generador de Informes de Laboratorio - UNJBG (Streamlit + APA 7.ª Edición)

Aplicación web interactiva desarrollada en **Python y Streamlit** para redactar y exportar informes de **Laboratorio de Física** de la **Universidad Nacional Jorge Basadre Grohmann (UNJBG)** siguiendo las normas **APA 7.ª Edición**.

---

## Características Principales

- **100 % Compatible con Streamlit Community Cloud:** Incluye `streamlit_app.py`, `app.py`, `requirements.txt` y `.streamlit/config.toml` directamente en la raíz del repositorio.
- **Carátula Oficial UNJBG:** Incorpora el escudo institucional (`assets/logo-unjbg.png`) centrado inmediatamente después de **Escuela Profesional** y antes de **Laboratorio de: FÍSICA**.
- **Normativa APA 7.ª Edición:**
  - Exportación nativa a **Microsoft Word (`.docx`)** con fuente *Times New Roman* 12 pt, interlineado doble (`2.0`), márgenes de `2.54 cm`, tablas solo con bordes horizontales, figuras con título en cursiva y *Nota.* al pie, y referencias ordenadas alfabéticamente con **sangría francesa** (`1.27 cm`).
  - Exportación también disponible en **LaTeX (`.tex`)**, **Markdown (`.md`)** y respaldo editable **JSON (`.json`)**.
- **Fácil de Actualizar:** Edita `modulos/plantilla_unjbg.py` para añadir facultades, escuelas profesionales o modificar las guías de las 9 secciones.

---

## Cómo Desplegar en Streamlit Community Cloud

1. Sube todos los archivos de este `.zip` directamente a la **raíz** de tu repositorio en GitHub.
2. Ingresa a [share.streamlit.io](https://share.streamlit.io/), selecciona tu repositorio y elige como archivo principal `streamlit_app.py` (o `app.py`).
3. Haz clic en **Deploy** y la aplicación cargará lista para usar.

## Ejecución Local

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
