"""
MÓDULO DE EXPORTACIÓN APA 7.ª EDICIÓN - UNJBG
Genera:
  1. Documento Word (.docx) nativo con formato APA 7.ª edición y el escudo UNJBG
     centrado inmediatamente después de Escuela Profesional.
  2. Código fuente LaTeX (.tex) listo para Overleaf con paquete apa7/geometry.
  3. Documento Markdown (.md) listo para GitHub.
  4. Archivo de proyecto editable (.json) para guardar y actualizar luego.
"""

import io
import os
import json
import base64
from docx import Document
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls


def _agregar_numero_pagina_apa7(section):
    """Agrega numeración de página en la esquina superior derecha (APA 7)."""
    header = section.header
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run()
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls("w"))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls("w"))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls("w"))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls("w"))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)


def _aplicar_bordes_tabla_apa7(table):
    """Aplica bordes estilo APA 7: solo líneas horizontales superior, bajo encabezado e inferior."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        '<w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
        '<w:left w:val="none"/>'
        '<w:right w:val="none"/>'
        '<w:insideH w:val="none"/>'
        '<w:insideV w:val="none"/>'
        "</w:tblBorders>"
    )
    tblPr.append(borders)
    if len(table.rows) > 0:
        for cell in table.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
                "</w:tcBorders>"
            )
            tcPr.append(tcBorders)


def _insertar_tabla_apa7(doc, numero_tabla: int, titulo_cursiva: str, headers: list, rows: list, nota_pie: str):
    """Inserta una tabla completa siguiendo las reglas de APA 7.ª edición."""
    p_num = doc.add_paragraph()
    p_num.paragraph_format.space_before = Pt(8)
    p_num.paragraph_format.space_after = Pt(0)
    p_num.paragraph_format.line_spacing = 1.15
    r_num = p_num.add_run(f"Tabla {numero_tabla}")
    r_num.bold = True

    p_tit = doc.add_paragraph()
    p_tit.paragraph_format.space_before = Pt(0)
    p_tit.paragraph_format.space_after = Pt(4)
    p_tit.paragraph_format.line_spacing = 1.15
    r_tit = p_tit.add_run(titulo_cursiva or f"Datos correspondientes a la Tabla {numero_tabla}")
    r_tit.italic = True

    if not headers:
        headers = ["Columna 1"]
    if not rows:
        rows = [["" for _ in headers]]

    tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    for j, h in enumerate(headers):
        cell = tbl.rows[0].cells[j]
        cell.text = str(h)
        for p in cell.paragraphs:
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                r.bold = True
                r.font.name = "Times New Roman"
                r.font.size = Pt(11)

    for i, row_data in enumerate(rows, start=1):
        for j in range(len(headers)):
            val = row_data[j] if j < len(row_data) else ""
            cell = tbl.rows[i].cells[j]
            cell.text = str(val if val is not None else "")
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing = 1.15
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(11)

    _aplicar_bordes_tabla_apa7(tbl)

    if nota_pie and nota_pie.strip():
        p_nota = doc.add_paragraph()
        p_nota.paragraph_format.space_before = Pt(4)
        p_nota.paragraph_format.space_after = Pt(10)
        p_nota.paragraph_format.line_spacing = 1.15
        r_nota = p_nota.add_run(nota_pie.strip())
        r_nota.italic = True
        r_nota.font.size = Pt(10)


def _insertar_imagen_base64(doc, img_b64: str, ancho_cm: float = 11.5):
    if not img_b64:
        return
    try:
        if "," in img_b64:
            img_b64 = img_b64.split(",", 1)[1]
        img_bytes = base64.b64decode(img_b64)
        stream = io.BytesIO(img_bytes)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(stream, width=Cm(ancho_cm))
    except Exception:
        pass


def generar_docx_bytes(datos: dict, logo_path: str = "assets/logo-unjbg.png") -> bytes:
    """Genera el archivo Word (.docx) en memoria cumpliendo APA 7.ª edición."""
    doc = Document()

    for section in doc.sections:
        # Márgenes oficiales APA 7: 2.54 cm (1 pulgada) en todos los lados
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.54)
        section.right_margin = Cm(2.54)
        _agregar_numero_pagina_apa7(section)

    normal_style = doc.styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(12)
    normal_style.paragraph_format.line_spacing = 2.0
    normal_style.paragraph_format.space_after = Pt(0)
    normal_style.paragraph_format.space_before = Pt(0)

    c = datos.get("caratula", {})

    # --- CARÁTULA OFICIAL UNJBG ---
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_uni.paragraph_format.line_spacing = 1.5
    r_uni = p_uni.add_run("UNIVERSIDAD NACIONAL JORGE BASADRE GROHMANN")
    r_uni.bold = True
    r_uni.font.size = Pt(14)

    p_fac = doc.add_paragraph()
    p_fac.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fac.paragraph_format.line_spacing = 1.5
    p_fac.add_run("Facultad: ").bold = True
    p_fac.add_run(f"{c.get('facultad') or '[Facultad correspondiente]'}\n")
    p_fac.add_run("Escuela Profesional: ").bold = True
    p_fac.add_run(f"{c.get('escuela') or '[Ingeniería Ambiental / Física / etc.]'}")

    # LOGO OFICIAL UNJBG JUSTO DESPUÉS DE ESCUELA PROFESIONAL EN EL CENTRO
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(8)
        p_logo.paragraph_format.space_after = Pt(8)
        p_logo.add_run().add_picture(logo_path, width=Cm(3.2))

    p_lab = doc.add_paragraph()
    p_lab.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lab.paragraph_format.line_spacing = 1.5
    p_lab.add_run("Laboratorio de: ").bold = True
    p_lab.add_run(f"{c.get('laboratorio') or 'FÍSICA'}")

    p_banner = doc.add_paragraph()
    p_banner.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_banner.paragraph_format.space_before = Pt(12)
    p_banner.paragraph_format.space_after = Pt(12)
    r_banner = p_banner.add_run("INFORME DE LABORATORIO")
    r_banner.bold = True
    r_banner.font.size = Pt(15)

    p_tit = doc.add_paragraph()
    p_tit.paragraph_format.line_spacing = 1.5
    p_tit.add_run("Título de la práctica: ").bold = True
    p_tit.add_run(c.get("tituloPractica") or "[Nombre de la práctica]")

    p_aut_lbl = doc.add_paragraph()
    p_aut_lbl.paragraph_format.space_before = Pt(8)
    p_aut_lbl.paragraph_format.line_spacing = 1.5
    p_aut_lbl.add_run("Autores:").bold = True

    for autor in datos.get("autores", []):
        if autor.strip():
            p_a = doc.add_paragraph(autor.strip(), style="List Bullet")
            p_a.paragraph_format.line_spacing = 1.5

    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(10)
    p_meta.paragraph_format.line_spacing = 1.5
    p_meta.add_run("Grupo: ").bold = True
    p_meta.add_run(f"{c.get('grupo') or '[ ]'}        ")
    p_meta.add_run("Horario: ").bold = True
    p_meta.add_run(f"{c.get('horario') or '[ ]'}\n")
    p_meta.add_run("Docente: ").bold = True
    p_meta.add_run(f"{c.get('docente') or '[Grado y Nombre]'}\n")
    p_meta.add_run("Fecha de ejecución: ").bold = True
    p_meta.add_run(f"{c.get('fechaEjecucion') or '[ ]'}\n")
    p_meta.add_run("Fecha de entrega: ").bold = True
    p_meta.add_run(
        f"Tacna, {c.get('diaEntrega') or '[ ]'} de "
        f"{c.get('mesEntrega') or '[ ]'} de {c.get('anioEntrega') or '2026'}"
    )

    doc.add_page_break()

    # Helpers APA 7
    def add_apa_h1(texto: str):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(texto)
        r.bold = True
        return p

    def add_apa_h2(texto: str):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(texto)
        r.bold = True
        return p

    def add_apa_parrafos(texto: str, sangria: bool = True):
        for bloque in (texto or "").split("\n"):
            p = doc.add_paragraph(bloque)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            if sangria and bloque.strip():
                p.paragraph_format.first_line_indent = Cm(1.27)

    # 1. Resumen (En APA 7: título centrado en negrita y párrafo único sin sangría inicial)
    add_apa_h1("1. Resumen")
    add_apa_parrafos(datos.get("resumen", ""), sangria=False)

    # 2. Introducción
    add_apa_h1("2. Introducción")
    add_apa_parrafos(datos.get("introduccionTeoria", ""), sangria=True)

    add_apa_h2("Objetivos")
    p_og = doc.add_paragraph()
    p_og.paragraph_format.first_line_indent = Cm(1.27)
    p_og.add_run("Objetivo General: ").bold = True
    p_og.add_run(datos.get("objetivoGeneral", ""))

    p_oe = doc.add_paragraph()
    p_oe.add_run("Objetivos Específicos:").bold = True
    for obj in datos.get("objetivosEspecificos", []):
        if obj.strip():
            doc.add_paragraph(obj.strip(), style="List Bullet")

    # 3. Materiales y Desarrollo Experimental
    add_apa_h1("3. Materiales y Desarrollo Experimental")
    add_apa_h2("3.1 Materiales")
    add_apa_parrafos(datos.get("materialesTexto", ""), sangria=True)

    mat_rows = [
        [
            idx + 1,
            m.get("nombre", ""),
            m.get("marca", ""),
            m.get("rango", ""),
            m.get("apreciacion", ""),
            m.get("cantidad", ""),
        ]
        for idx, m in enumerate(datos.get("materialesTabla", []))
    ]
    _insertar_tabla_apa7(
        doc,
        numero_tabla=1,
        titulo_cursiva=datos.get("tituloTablaMateriales", ""),
        headers=["N°", "Equipo / Material", "Marca / Modelo", "Rango", "Apreciación", "Cant."],
        rows=mat_rows,
        nota_pie=datos.get("notaTablaMateriales", ""),
    )

    add_apa_h2("3.2 Procedimiento")
    add_apa_parrafos(datos.get("procedimientoTexto", ""), sangria=True)

    # Figura 1 APA 7
    p_f1 = doc.add_paragraph()
    p_f1.add_run("Figura 1").bold = True
    p_f1_t = doc.add_paragraph()
    p_f1_t.add_run(datos.get("figura1Desc", "")).italic = True
    _insertar_imagen_base64(doc, datos.get("figura1Img", ""))
    if datos.get("figura1Nota", "").strip():
        p_f1_n = doc.add_paragraph()
        r_f1_n = p_f1_n.add_run(datos.get("figura1Nota", "").strip())
        r_f1_n.italic = True
        r_f1_n.font.size = Pt(10)

    # Tabla 2 APA 7
    tc = datos.get("tablaCruda", {"headers": [], "rows": []})
    _insertar_tabla_apa7(
        doc,
        numero_tabla=2,
        titulo_cursiva=datos.get("tituloTablaCruda", ""),
        headers=tc.get("headers", []),
        rows=tc.get("rows", []),
        nota_pie=datos.get("notaTablaCruda", ""),
    )

    # 4. Resultados y Discusión
    add_apa_h1("4. Resultados y Discusión")
    tr = datos.get("tablaResultados", {"headers": [], "rows": []})
    _insertar_tabla_apa7(
        doc,
        numero_tabla=3,
        titulo_cursiva=datos.get("tituloTablaResultados", ""),
        headers=tr.get("headers", []),
        rows=tr.get("rows", []),
        nota_pie=datos.get("notaTablaResultados", ""),
    )

    # Figura 2 APA 7
    p_f2 = doc.add_paragraph()
    p_f2.add_run("Figura 2").bold = True
    p_f2_t = doc.add_paragraph()
    p_f2_t.add_run(datos.get("figura2Desc", "")).italic = True
    _insertar_imagen_base64(doc, datos.get("figura2Img", ""))
    if datos.get("figura2Nota", "").strip():
        p_f2_n = doc.add_paragraph()
        r_f2_n = p_f2_n.add_run(datos.get("figura2Nota", "").strip())
        r_f2_n.italic = True
        r_f2_n.font.size = Pt(10)

    add_apa_parrafos(datos.get("discusionTexto", ""), sangria=True)

    # 5. Conclusiones
    add_apa_h1("5. Conclusiones")
    for con in datos.get("conclusiones", []):
        if con.strip():
            doc.add_paragraph(con.strip(), style="List Number")
    p_err = doc.add_paragraph()
    p_err.paragraph_format.first_line_indent = Cm(1.27)
    p_err.add_run("Fuentes de error y aproximaciones: ").bold = True
    p_err.add_run(datos.get("fuentesError", ""))

    # 6. Reflexión Argumentada
    add_apa_h1("6. Reflexión Argumentada")
    add_apa_parrafos(datos.get("reflexionTexto", ""), sangria=True)

    # 7. Referencias (Sangría francesa APA 7 de 1.27 cm)
    add_apa_h1("7. Referencias")
    for ref in datos.get("referencias", []):
        if ref.strip():
            p_ref = doc.add_paragraph(ref.strip())
            p_ref.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p_ref.paragraph_format.left_indent = Cm(1.27)
            p_ref.paragraph_format.first_line_indent = Cm(-1.27)

    # 8. Cuestionario
    add_apa_h1("8. Cuestionario")
    for idx, item in enumerate(datos.get("cuestionario", []), start=1):
        p_q = doc.add_paragraph()
        p_q.add_run(f"Pregunta {idx}: ").bold = True
        p_q.add_run(item.get("pregunta", ""))
        add_apa_parrafos(item.get("respuesta", ""), sangria=True)

    # 9. Apéndices
    add_apa_h1("9. Apéndices")
    add_apa_parrafos(datos.get("apendicesTexto", ""), sangria=True)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()


def generar_markdown_str(datos: dict) -> str:
    """Genera el informe en formato Markdown con estructura APA 7 y logo centrado."""
    c = datos.get("caratula", {})
    autores_md = "\n".join([f"- {a}" for a in datos.get("autores", []) if a.strip()]) or "- [Autores]"
    obj_esp_md = "\n".join([f"- {o}" for o in datos.get("objetivosEspecificos", []) if o.strip()]) or "- [Objetivo]"
    concl_md = "\n".join([f"{i+1}. {x}" for i, x in enumerate(datos.get("conclusiones", [])) if x.strip()]) or "1. [Conclusión]"
    refs_md = "\n\n".join([r for r in datos.get("referencias", []) if r.strip()])
    cuest_md = "\n\n".join(
        [f"**Pregunta {i+1}:** {q.get('pregunta','')}\n\n**Respuesta:** {q.get('respuesta','')}" for i, q in enumerate(datos.get("cuestionario", []))]
    )

    def tabla_md(headers, rows):
        if not headers:
            return ""
        h_line = "| " + " | ".join(str(h) for h in headers) + " |"
        s_line = "| " + " | ".join("---" for _ in headers) + " |"
        r_lines = ["| " + " | ".join(str(cell) for cell in r) + " |" for r in rows]
        return "\n".join([h_line, s_line] + r_lines)

    mat_rows = [
        [i + 1, m.get("nombre", ""), m.get("marca", ""), m.get("rango", ""), m.get("apreciacion", ""), m.get("cantidad", "")]
        for i, m in enumerate(datos.get("materialesTabla", []))
    ]
    t1_md = tabla_md(["N°", "Equipo / Material", "Marca / Modelo", "Rango", "Apreciación", "Cant."], mat_rows)
    tc = datos.get("tablaCruda", {"headers": [], "rows": []})
    t2_md = tabla_md(tc.get("headers", []), tc.get("rows", []))
    tr = datos.get("tablaResultados", {"headers": [], "rows": []})
    t3_md = tabla_md(tr.get("headers", []), tr.get("rows", []))

    return f"""<div align="center">

# UNIVERSIDAD NACIONAL JORGE BASADRE GROHMANN

**Facultad:** {c.get('facultad') or '[Facultad correspondiente]'}  
**Escuela Profesional:** {c.get('escuela') or '[Ingeniería Ambiental / Física / etc.]'}  

<img src="assets/logo-unjbg.png" alt="Escudo UNJBG" width="115" />

**Laboratorio de:** {c.get('laboratorio') or 'FÍSICA'}  

---

## INFORME DE LABORATORIO

</div>

**Título de la práctica:** {c.get('tituloPractica') or '[Nombre de la práctica]'}  

**Autores:**  
{autores_md}

**Grupo:** {c.get('grupo') or '[ ]'} | **Horario:** {c.get('horario') or '[ ]'}  
**Docente:** {c.get('docente') or '[Grado y Nombre]'}  
**Fecha de ejecución:** {c.get('fechaEjecucion') or '[ ]'}  
**Fecha de entrega:** Tacna, {c.get('diaEntrega') or '[ ]'} de {c.get('mesEntrega') or '[ ]'} de {c.get('anioEntrega') or '2026'}  

---

## 1. Resumen
{datos.get('resumen', '')}

## 2. Introducción
{datos.get('introduccionTeoria', '')}

### Objetivos
**Objetivo General:**  
{datos.get('objetivoGeneral', '')}

**Objetivos Específicos:**  
{obj_esp_md}

## 3. Materiales y Desarrollo Experimental
### 3.1 Materiales
{datos.get('materialesTexto', '')}

**Tabla 1**  
*{datos.get('tituloTablaMateriales', '')}*

{t1_md}

*{datos.get('notaTablaMateriales', '')}*

### 3.2 Procedimiento
{datos.get('procedimientoTexto', '')}

**Figura 1**  
*{datos.get('figura1Desc', '')}*  
*{datos.get('figura1Nota', '')}*

**Tabla 2**  
*{datos.get('tituloTablaCruda', '')}*

{t2_md}

*{datos.get('notaTablaCruda', '')}*

## 4. Resultados y Discusión
**Tabla 3**  
*{datos.get('tituloTablaResultados', '')}*

{t3_md}

*{datos.get('notaTablaResultados', '')}*

**Figura 2**  
*{datos.get('figura2Desc', '')}*  
*{datos.get('figura2Nota', '')}*

{datos.get('discusionTexto', '')}

## 5. Conclusiones
{concl_md}

**Fuentes de error y aproximaciones:**  
{datos.get('fuentesError', '')}

## 6. Reflexión Argumentada
{datos.get('reflexionTexto', '')}

## 7. Referencias
{refs_md}

## 8. Cuestionario
{cuest_md}

## 9. Apéndices
{datos.get('apendicesTexto', '')}
"""


def generar_latex_str(datos: dict) -> str:
    """Genera el código fuente LaTeX (.tex) con formato APA 7 y logo centrado."""
    c = datos.get("caratula", {})
    autores_tex = "\n".join([f"  \\item {a}" for a in datos.get("autores", []) if a.strip()]) or "  \\item Apellidos y Nombres - Código"
    obj_esp_tex = "\n".join([f"  \\item {o}" for o in datos.get("objetivosEspecificos", []) if o.strip()]) or "  \\item Objetivo específico"
    concl_tex = "\n".join([f"  \\item {x}" for x in datos.get("conclusiones", []) if x.strip()]) or "  \\item Conclusión experimental"
    refs_tex = "\n".join([f"\\noindent\\hangindent=1.27cm\\hangafter=1 {r}\n" for r in datos.get("referencias", []) if r.strip()])

    return f"""\\documentclass[12pt,letterpaper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[spanish]{{babel}}
\\usepackage{{times}}
\\usepackage{{amsmath,amssymb}}
\\usepackage{{graphicx}}
\\usepackage{{booktabs}}
\\usepackage{{setspace}}
\\usepackage{{geometry}}
\\usepackage{{fancyhdr}}

% Márgenes APA 7.ª edición (2.54 cm = 1 pulgada)
\\geometry{{margin=2.54cm}}
\\doublespacing
\\setlength{{\\parindent}}{{1.27cm}}

\\pagestyle{{fancy}}
\\fancyhf{{}}
\\fancyhead[R]{{\\thepage}}
\\renewcommand{{\\headrulewidth}}{{0pt}}

\\begin{{document}}

\\begin{{titlepage}}
  \\centering
  \\thispagestyle{{fancy}}
  {{\\Large \\textbf{{UNIVERSIDAD NACIONAL JORGE BASADRE GROHMANN}}}}\\[0.3cm]
  \\textbf{{Facultad:}} {c.get('facultad') or '[Facultad correspondiente]'}\\
  \\textbf{{Escuela Profesional:}} {c.get('escuela') or '[Ingeniería Ambiental / Física / etc.]'}\\[0.4cm]

  % Escudo oficial UNJBG centrado inmediatamente después de Escuela Profesional
  \\includegraphics[width=3.2cm]{{assets/logo-unjbg.png}}\\[0.4cm]

  \\textbf{{Laboratorio de:}} {c.get('laboratorio') or 'FÍSICA'}\\[0.8cm]

  {{\\LARGE \\textbf{{INFORME DE LABORATORIO}}}}\\[0.7cm]
  {{\\large \\textbf{{Título de la práctica:}} {c.get('tituloPractica') or '[Nombre de la práctica]'}}}\\[0.9cm]

  \\begin{{flushleft}}
    \\textbf{{Autores:}}
    \\begin{{itemize}}
{autores_tex}
    \\end{{itemize}}
    \\textbf{{Grupo:}} {c.get('grupo') or '[ ]'} \\quad \\textbf{{Horario:}} {c.get('horario') or '[ ]'}\\
    \\textbf{{Docente:}} {c.get('docente') or '[Grado y Nombre]'}\\
    \\textbf{{Fecha de ejecución:}} {c.get('fechaEjecucion') or '[ ]'}\\
    \\textbf{{Fecha de entrega:}} Tacna, {c.get('diaEntrega') or '[ ]'} de {c.get('mesEntrega') or '[ ]'} de {c.get('anioEntrega') or '2026'}
  \\end{{flushleft}}
\\end{{titlepage}}

\\section*{{1. Resumen}}
\\noindent {datos.get('resumen', '')}

\\section*{{2. Introducción}}
{datos.get('introduccionTeoria', '')}

\\subsection*{{Objetivos}}
\\noindent\\textbf{{Objetivo General:}} {datos.get('objetivoGeneral', '')}

\\noindent\\textbf{{Objetivos Específicos:}}
\\begin{{itemize}}
{obj_esp_tex}
\\end{{itemize}}

\\section*{{3. Materiales y Desarrollo Experimental}}
\\subsection*{{3.1 Materiales}}
{datos.get('materialesTexto', '')}

\\subsection*{{3.2 Procedimiento}}
{datos.get('procedimientoTexto', '')}

\\section*{{4. Resultados y Discusión}}
{datos.get('discusionTexto', '')}

\\section*{{5. Conclusiones}}
\\begin{{enumerate}}
{concl_tex}
\\end{{enumerate}}
\\textbf{{Fuentes de error y aproximaciones:}} {datos.get('fuentesError', '')}

\\section*{{6. Reflexión Argumentada}}
{datos.get('reflexionTexto', '')}

\\section*{{7. Referencias}}
{refs_tex}

\\section*{{8. Cuestionario}}
{chr(10).join([f"\\noindent\\textbf{{Pregunta {i+1}:}} {q.get('pregunta','')}\\ {q.get('respuesta','')}" for i, q in enumerate(datos.get('cuestionario', []))])}

\\section*{{9. Apéndices}}
{datos.get('apendicesTexto', '')}

\\end{{document}}
"""


def generar_json_str(datos: dict) -> str:
    return json.dumps(datos, indent=2, ensure_ascii=False)
