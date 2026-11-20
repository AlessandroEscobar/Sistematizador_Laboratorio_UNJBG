#!/usr/bin/env python3
"""
Script opcional en Python para convertir un archivo proyecto_*.json
a un documento Microsoft Word (.docx) nativo bajo normativa APA 7.ª edición,
insertando el escudo oficial de la UNJBG centrado inmediatamente después
de Escuela Profesional.

Uso:
    python generar_informe_docx.py proyecto_informe.json salida_apa7.docx
"""

import json
import os
import sys
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls


def agregar_numero_pagina_apa7(section):
    header = section.header
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run()
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)


def aplicar_bordes_tabla_apa7(table):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        '<w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
        '<w:left w:val="none"/>'
        '<w:right w:val="none"/>'
        '<w:insideH w:val="none"/>'
        '<w:insideV w:val="none"/>'
        '</w:tblBorders>'
    )
    tblPr.append(borders)
    if len(table.rows) > 0:
        for cell in table.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
                '</w:tcBorders>'
            )
            tcPr.append(tcBorders)


def crear_informe_docx(ruta_json: str, ruta_salida: str = "Informe_Laboratorio_UNJBG_APA7.docx"):
    with open(ruta_json, "r", encoding="utf-8") as f:
        datos = json.load(f)

    doc = Document()
    for section in doc.sections:
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.54)
        section.right_margin = Cm(2.54)
        agregar_numero_pagina_apa7(section)

    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    style.paragraph_format.line_spacing = 2.0
    style.paragraph_format.space_after = Pt(0)

    c = datos.get("caratula", {})

    # Carátula Institucional UNJBG
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_uni.paragraph_format.line_spacing = 1.5
    run_uni = p_uni.add_run("UNIVERSIDAD NACIONAL JORGE BASADRE GROHMANN")
    run_uni.bold = True
    run_uni.font.size = Pt(14)

    p_fac = doc.add_paragraph()
    p_fac.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fac.paragraph_format.line_spacing = 1.5
    p_fac.add_run("Facultad: ").bold = True
    p_fac.add_run(f"{c.get('facultad', '[Facultad correspondiente]')}\n")
    p_fac.add_run("Escuela Profesional: ").bold = True
    p_fac.add_run(f"{c.get('escuela', '[Ingeniería Ambiental / Física / etc.]')}")

    # Logo UNJBG centrado inmediatamente después de Escuela Profesional
    ruta_logo = os.path.join(os.path.dirname(__file__), "..", "assets", "logo-unjbg.png")
    if os.path.exists(ruta_logo):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(6)
        p_logo.paragraph_format.space_after = Pt(6)
        p_logo.add_run().add_picture(ruta_logo, width=Cm(3.1))

    p_lab = doc.add_paragraph()
    p_lab.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lab.paragraph_format.line_spacing = 1.5
    p_lab.add_run("Laboratorio de: ").bold = True
    p_lab.add_run(f"{c.get('laboratorio', 'FÍSICA')}")

    p_tit_doc = doc.add_paragraph()
    p_tit_doc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_tit_doc = p_tit_doc.add_run("\nINFORME DE LABORATORIO\n")
    r_tit_doc.bold = True
    r_tit_doc.font.size = Pt(15)

    p_prac = doc.add_paragraph()
    p_prac.add_run("Título de la práctica: ").bold = True
    p_prac.add_run(c.get("tituloPractica", "[Nombre de la práctica]"))

    doc.add_paragraph().add_run("Autores:").bold = True
    for autor in datos.get("autores", []):
        doc.add_paragraph(autor, style="List Bullet")

    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.line_spacing = 1.5
    p_meta.add_run("Grupo: ").bold = True
    p_meta.add_run(f"{c.get('grupo', '[ ]')}    ")
    p_meta.add_run("Horario: ").bold = True
    p_meta.add_run(f"{c.get('horario', '[ ]')}\n")
    p_meta.add_run("Docente: ").bold = True
    p_meta.add_run(f"{c.get('docente', '[Grado y Nombre]')}\n")
    p_meta.add_run("Fecha de ejecución: ").bold = True
    p_meta.add_run(f"{c.get('fechaEjecucion', '[ ]')}\n")
    p_meta.add_run("Fecha de entrega: ").bold = True
    p_meta.add_run(
        f"Tacna, {c.get('diaEntrega', '[ ]')} de "
        f"{c.get('mesEntrega', '[ ]')} de {c.get('anioEntrega', '2026')}"
    )

    doc.add_page_break()

    def add_apa_level1(texto):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(texto)
        r.bold = True
        return p

    def add_apa_body(texto, sangria=True):
        p = doc.add_paragraph(texto)
        if sangria:
            p.paragraph_format.first_line_indent = Cm(1.27)
        return p

    add_apa_level1("1. Resumen")
    add_apa_body(datos.get("resumen", ""), sangria=False)

    add_apa_level1("2. Introducción")
    add_apa_body(datos.get("introduccionTeoria", ""), sangria=True)

    add_apa_level1("3. Materiales y Desarrollo Experimental")
    p_31 = doc.add_paragraph()
    p_31.add_run("3.1 Materiales").bold = True
    add_apa_body(datos.get("materialesTexto", ""), sangria=True)

    p_t1_num = doc.add_paragraph()
    p_t1_num.add_run("Tabla 1").bold = True
    p_t1_tit = doc.add_paragraph()
    p_t1_tit.add_run(datos.get("tituloTablaMateriales", "Características técnicas de equipos")).italic = True

    mat_rows = datos.get("materialesTabla", [])
    tbl = doc.add_table(rows=len(mat_rows) + 1, cols=6)
    headers = ["N°", "Equipo / Material", "Marca / Modelo", "Rango", "Apreciación", "Cant."]
    for j, h in enumerate(headers):
        tbl.rows[0].cells[j].text = h
    for i, m in enumerate(mat_rows, start=1):
        tbl.rows[i].cells[0].text = str(i)
        tbl.rows[i].cells[1].text = m.get("nombre", "")
        tbl.rows[i].cells[2].text = m.get("marca", "")
        tbl.rows[i].cells[3].text = m.get("rango", "")
        tbl.rows[i].cells[4].text = m.get("apreciacion", "")
        tbl.rows[i].cells[5].text = m.get("cantidad", "")
    aplicar_bordes_tabla_apa7(tbl)

    p_32 = doc.add_paragraph()
    p_32.add_run("3.2 Procedimiento").bold = True
    add_apa_body(datos.get("procedimientoTexto", ""), sangria=True)

    add_apa_level1("4. Resultados y Discusión")
    add_apa_body(datos.get("discusionTexto", ""), sangria=True)

    add_apa_level1("5. Conclusiones")
    for con in datos.get("conclusiones", []):
        doc.add_paragraph(con, style="List Number")
    add_apa_body(f"Fuentes de error y aproximaciones: {datos.get('fuentesError', '')}", sangria=True)

    add_apa_level1("6. Reflexión Argumentada")
    add_apa_body(datos.get("reflexionTexto", ""), sangria=True)

    add_apa_level1("7. Referencias")
    for ref in datos.get("referencias", []):
        p_ref = doc.add_paragraph(ref)
        p_ref.paragraph_format.left_indent = Cm(1.27)
        p_ref.paragraph_format.first_line_indent = Cm(-1.27)

    add_apa_level1("8. Cuestionario")
    for idx, item in enumerate(datos.get("cuestionario", []), start=1):
        p = doc.add_paragraph()
        p.add_run(f"Pregunta {idx}: ").bold = True
        p.add_run(item.get("pregunta", ""))
        add_apa_body(item.get("respuesta", ""), sangria=True)

    add_apa_level1("9. Apéndices")
    add_apa_body(datos.get("apendicesTexto", ""), sangria=True)

    doc.save(ruta_salida)
    print(f"Documento APA 7 generado exitosamente: {ruta_salida}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python generar_informe_docx.py proyecto.json [salida_apa7.docx]")
        sys.exit(1)
    salida = sys.argv[2] if len(sys.argv) > 2 else "Informe_Laboratorio_UNJBG_APA7.docx"
    crear_informe_docx(sys.argv[1], salida)
