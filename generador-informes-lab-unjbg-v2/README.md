# Generador de Informes de Laboratorio - UNJBG (v2.0 - APA 7.ª Edición)

Software web modular diseñado para redactar, estructurar y exportar informes de **Laboratorio de Física** de la **Universidad Nacional Jorge Basadre Grohmann (UNJBG)** cumpliendo con la normativa **APA 7.ª Edición (7th Edition)**.

---

## Novedades de la Versión 2.0

1. **Escudo Oficial UNJBG en Carátula:** El logotipo institucional (`assets/logo-unjbg.png`) aparece centrado automáticamente inmediatamente después de **Escuela Profesional** y antes de **Laboratorio de: FÍSICA**, tanto en la vista web como en las exportaciones a **Word (`.doc` / `.docx`)**, **LaTeX (`.tex`)**, **Markdown (`.md`)** e **Impresión / PDF**.
2. **Normativa APA 7.ª Edición Integrada:**
   - **Tipografía y Márgenes:** Times New Roman 12 pt, interlineado doble (2.0), márgenes de 2.54 cm (1 pulgada), alineación a la izquierda y sangría de primera línea de 1.27 cm (0.5 in).
   - **Tablas Estilo APA 7:** Número en **negrita** (`Tabla 1`) en la línea superior, título en *cursiva* debajo, bordes exclusivamente horizontales (sin líneas verticales) y *Nota.* al pie.
   - **Figuras Estilo APA 7:** Número en **negrita** (`Figura 1`), título en *cursiva*, imagen centrada y *Nota.* descriptiva al pie.
   - **Citas y Referencias APA 7:** Sistema Autor-Fecha `(Apellido, Año)`, asistente rápido para generar referencias de libros, artículos o guías, ordenamiento alfabético automático (A-Z) y **sangría francesa** (`1.27 cm`).

---

## Estructura del Repositorio

```text
generador-informes-lab-unjbg-v2/
├── assets/
│   └── logo-unjbg.png                   # Escudo oficial UNJBG
├── index.html                           # Interfaz principal del editor
├── css/
│   └── styles.css                       # Estilos académicos y reglas de impresión APA 7
├── js/
│   ├── plantilla-unjbg.js               # Configuración modular de la plantilla UNJBG y APA 7
│   ├── app.js                           # Lógica de tablas, asistente APA 7 y autoguardado
│   └── exportadores.js                  # Exportación a Word APA 7 (.doc), LaTeX (.tex), MD y JSON
├── python/
│   ├── generar_informe_docx.py          # Conversor CLI a .docx nativo con formato APA 7 y logo
│   └── requirements.txt                 # Dependencias Python
└── .github/workflows/
    └── deploy-pages.yml                 # Publicación automática en GitHub Pages
```

---

## Cómo Actualizar en el Futuro

- **Cambiar logotipo institucional:** Reemplaza `assets/logo-unjbg.png` y actualiza el campo `logo` en `js/plantilla-unjbg.js`.
- **Editar secciones o guías:** Modifica `js/plantilla-unjbg.js`.
- **Continuar un informe guardado:** Usa el botón **Guardar Proyecto (`.json`)** y vuelve a cargarlo con **Abrir Proyecto (`.json`)**.
