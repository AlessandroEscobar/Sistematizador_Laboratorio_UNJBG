/**
 * MÓDULO DE EXPORTACIÓN APA 7.ª EDICIÓN - INFORME DE LABORATORIO UNJBG
 */

const Exportadores = {
  descargarArchivo(contenido, nombreArchivo, tipoMime) {
    const blob = new Blob([contenido], { type: tipoMime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = nombreArchivo;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  },

  slugify(texto) {
    return (texto || "informe_laboratorio_unjbg_apa7")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[̀-ͯ]/g, "")
      .replace(/[^a-z0-9]+/g, "_")
      .replace(/^_|_$/g, "");
  },

  aJSON(datos) {
    const nombre = `proyecto_${this.slugify(datos.caratula.tituloPractica)}.json`;
    this.descargarArchivo(JSON.stringify(datos, null, 2), nombre, "application/json;charset=utf-8");
  },

  aMarkdown(datos) {
    const c = datos.caratula;
    const autoresMd = datos.autores.map(a => `- ${a}`).join("
") || "- [Apellidos y Nombres - Código Universitario]";
    const objEspMd = datos.objetivosEspecificos.map(o => `- ${o}`).join("
") || "- [Objetivo específico]";
    const conclusionesMd = datos.conclusiones.map((con, i) => `${i + 1}. ${con}`).join("
") || "1. [Conclusión]";
    const refsMd = datos.referencias.map(r => `${r}`).join("

") || "Alonso, M., & Finn, E. J. (1986). *Física: Vol. I. Mecánica*. Fondo Educativo Interamericano.";
    const cuestMd = datos.cuestionario.map((q, i) => `**Pregunta ${i + 1}:** ${q.pregunta}

**Respuesta:** ${q.respuesta}`).join("

") || "[Sin preguntas registradas]";

    const tablaMatMd = [
      "**Tabla 1**  ",
      `*${datos.tituloTablaMateriales || "Características técnicas de los dispositivos y equipos de medición"}*`,
      "",
      "| N° | Equipo / Material | Marca / Modelo | Rango de medición | Apreciación / Incerteza | Cant. |",
      "|---|---|---|---|---|---|",
      ...datos.materialesTabla.map((m, idx) => `| ${idx + 1} | ${m.nombre} | ${m.marca} | ${m.rango} | ${m.apreciacion} | ${m.cantidad} |`),
      "",
      `*${datos.notaTablaMateriales || "Nota. Elaboración propia."}*`
    ].join("
");

    const renderTablaDinamicaMd = (numTabla, titulo, tabla, nota) => {
      if (!tabla || !tabla.headers || tabla.headers.length === 0) return "";
      const head = `| ${tabla.headers.join(" | ")} |`;
      const sep = `| ${tabla.headers.map(() => "---").join(" | ")} |`;
      const rows = tabla.rows.map(r => `| ${r.join(" | ")} |`).join("
");
      return `**Tabla ${numTabla}**  
*${titulo}*

${head}
${sep}
${rows}

*${nota || ""}*`;
    };

    const md = `<div align="center">

# UNIVERSIDAD NACIONAL JORGE BASADRE GROHMANN

**Facultad:** ${c.facultad || "[Facultad correspondiente]"}  
**Escuela Profesional:** ${c.escuela || "[Ingeniería Ambiental / Física / etc.]"}  

<img src="assets/logo-unjbg.png" alt="Escudo UNJBG" width="115" />

**Laboratorio de:** ${c.laboratorio || "FÍSICA"}  

---

## INFORME DE LABORATORIO

</div>

**Título de la práctica:** ${c.tituloPractica || "[Nombre de la práctica]"}  

**Autores:**  
${autoresMd}

**Grupo:** ${c.grupo || "[ ]"} | **Horario:** ${c.horario || "[ ]"}  
**Docente:** ${c.docente || "[Grado y Nombre]"}  
**Fecha de ejecución:** ${c.fechaEjecucion || "[ ]"}  
**Fecha de entrega:** Tacna, ${c.diaEntrega || "[ ]"} de ${c.mesEntrega || "[ ]"} de ${c.anioEntrega || "2026"}  

---

## 1. Resumen
${datos.resumen || ""}

## 2. Introducción
${datos.introduccionTeoria || ""}

### Objetivos
**Objetivo General:**  
${datos.objetivoGeneral || ""}

**Objetivos Específicos:**  
${objEspMd}

## 3. Materiales y Desarrollo Experimental
### 3.1 Materiales
${datos.materialesTexto || ""}

${tablaMatMd}

### 3.2 Procedimiento
${datos.procedimientoTexto || ""}

**Figura 1**  
*${datos.figura1Desc || "Esquema del dispositivo experimental."}*  
*${datos.figura1Nota || "Nota. Elaboración propia."}*

${renderTablaDinamicaMd(2, datos.tituloTablaCruda, datos.tablaCruda, datos.notaTablaCruda)}

## 4. Resultados y Discusión
${renderTablaDinamicaMd(3, datos.tituloTablaResultados, datos.tablaResultados, datos.notaTablaResultados)}

**Figura 2**  
*${datos.figura2Desc || "Gráfica experimental."}*  
*${datos.figura2Nota || "Nota. Elaboración propia."}*

${datos.discusionTexto || ""}

## 5. Conclusiones
${conclusionesMd}

**Fuentes de error y aproximaciones:**  
${datos.fuentesError || ""}

## 6. Reflexión Argumentada
${datos.reflexionTexto || ""}

## 7. Referencias
${refsMd}

## 8. Cuestionario
${cuestMd}

## 9. Apéndices
${datos.apendicesTexto || ""}
`;
    const nombre = `${this.slugify(c.tituloPractica)}.md`;
    this.descargarArchivo(md, nombre, "text/markdown;charset=utf-8");
  },

  aLaTeX(datos) {
    const c = datos.caratula;
    const autoresTex = datos.autores.map(a => `  \item ${a}`).join("
") || "  \item Apellidos y Nombres - Código Universitario";
    const objEspTex = datos.objetivosEspecificos.map(o => `  \item ${o}`).join("
") || "  \item Objetivo específico";
    const conclTex = datos.conclusiones.map(con => `  \item ${con}`).join("
") || "  \item Conclusión experimental";
    const refsTex = datos.referencias.map(r => `\noindent\hangindent=1.27cm\hangafter=1 ${r}
`).join("
") || "\noindent\hangindent=1.27cm\hangafter=1 Alonso, M., \& Finn, E. J. (1986). \textit{Física: Vol. I. Mecánica}. Fondo Educativo Interamericano.";

    const tex = `\documentclass[12pt,letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage[spanish]{babel}
\usepackage{times}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{setspace}
\usepackage{geometry}
\usepackage{fancyhdr}

% Márgenes oficiales APA 7.ª edición (1 pulgada = 2.54 cm)
\geometry{margin=2.54cm}
\doublespacing
\setlength{\parindent}{1.27cm}

% Numeración de página superior derecha según APA 7
\pagestyle{fancy}
\fancyhf{}
\fancyhead[R]{\thepage}
\renewcommand{\headrulewidth}{0pt}

\begin{document}

\begin{titlepage}
  \centering
  \thispagestyle{fancy}
  {\Large \textbf{UNIVERSIDAD NACIONAL JORGE BASADRE GROHMANN}}\\[0.3cm]
  \textbf{Facultad:} ${c.facultad || "[Facultad correspondiente]"}\\
  \textbf{Escuela Profesional:} ${c.escuela || "[Ingeniería Ambiental / Física / etc.]"}\\[0.4cm]

  % Escudo oficial UNJBG centrado inmediatamente después de Escuela Profesional
  \includegraphics[width=3.1cm]{assets/logo-unjbg.png}\\[0.4cm]

  \textbf{Laboratorio de:} ${c.laboratorio || "FÍSICA"}\\[0.8cm]

  {\LARGE \textbf{INFORME DE LABORATORIO}}\\[0.7cm]
  {\large \textbf{Título de la práctica:} ${c.tituloPractica || "[Nombre de la práctica]"}}\\[0.9cm]

  \begin{flushleft}
    \textbf{Autores:}
    \begin{itemize}
${autoresTex}
    \end{itemize}
    \textbf{Grupo:} ${c.grupo || "[ ]"} \quad \textbf{Horario:} ${c.horario || "[ ]"}\\
    \textbf{Docente:} ${c.docente || "[Grado y Nombre]"}\\
    \textbf{Fecha de ejecución:} ${c.fechaEjecucion || "[ ]"}\\
    \textbf{Fecha de entrega:} Tacna, ${c.diaEntrega || "[ ]"} de ${c.mesEntrega || "[ ]"} de ${c.anioEntrega || "2026"}
  \end{flushleft}
\end{titlepage}

\section*{1. Resumen}
\noindent ${datos.resumen || ""}

\section*{2. Introducción}
${datos.introduccionTeoria || ""}

\subsection*{Objetivos}
\noindent\textbf{Objetivo General:} ${datos.objetivoGeneral || ""}

\noindent\textbf{Objetivos Específicos:}
\begin{itemize}
${objEspTex}
\end{itemize}

\section*{3. Materiales y Desarrollo Experimental}
\subsection*{3.1 Materiales}
${datos.materialesTexto || ""}

\subsection*{3.2 Procedimiento}
${datos.procedimientoTexto || ""}

\section*{4. Resultados y Discusión}
${datos.discusionTexto || ""}

\section*{5. Conclusiones}
\begin{enumerate}
${conclTex}
\end{enumerate}
\textbf{Fuentes de error y aproximaciones:} ${datos.fuentesError || ""}

\section*{6. Reflexión Argumentada}
${datos.reflexionTexto || ""}

\section*{7. Referencias}
${refsTex}

\section*{8. Cuestionario}
${datos.cuestionario.map((q, i) => `\noindent\textbf{Pregunta ${i + 1}:} ${q.pregunta}\\ ${q.respuesta}
`).join("
")}

\section*{9. Apéndices}
${datos.apendicesTexto || ""}

\end{document}
`;
    const nombre = `${this.slugify(c.tituloPractica)}.tex`;
    this.descargarArchivo(tex, nombre, "application/x-tex;charset=utf-8");
  },

  aWord(datos) {
    const c = datos.caratula;
    const logoUri = (typeof PLANTILLA_UNJBG !== "undefined" && PLANTILLA_UNJBG.institucion.logo.dataUri)
      ? PLANTILLA_UNJBG.institucion.logo.dataUri
      : "assets/logo-unjbg.png";

    const esc = (str) => String(str || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/
/g, "<br/>");

    // Renderizado de tablas en estricto estilo APA 7.ª edición (sin líneas verticales)
    const renderTablaAPA7 = (numTabla, titulo, headers, rows, nota) => {
      const ths = headers.map(h => `<th style="border-top:1.5pt solid #000;border-bottom:1pt solid #000;border-left:none;border-right:none;padding:6pt 5pt;text-align:left;font-weight:bold;">${esc(h)}</th>`).join("");
      const trs = rows.map((r, rIdx) => {
        const isLast = rIdx === rows.length - 1;
        const borderBot = isLast ? "border-bottom:1.5pt solid #000;" : "border-bottom:none;";
        return `<tr>${r.map(cell => `<td style="${borderBot}border-top:none;border-left:none;border-right:none;padding:5pt;text-align:left;">${esc(cell)}</td>`).join("")}</tr>`;
      }).join("");

      return `
        <p style="margin-bottom:2pt;text-indent:0;font-weight:bold;">Tabla ${numTabla}</p>
        <p style="margin-top:0;margin-bottom:6pt;text-indent:0;font-style:italic;">${esc(titulo)}</p>
        <table style="width:100%;border-collapse:collapse;margin:4pt 0;font-family:'Times New Roman',serif;font-size:11pt;line-height:1.15;">
          <thead><tr>${ths}</tr></thead>
          <tbody>${trs}</tbody>
        </table>
        <p style="margin-top:4pt;margin-bottom:12pt;text-indent:0;font-size:10pt;"><i>${esc(nota || "")}</i></p>
      `;
    };

    const tablaMat = renderTablaAPA7(
      1,
      datos.tituloTablaMateriales || "Características técnicas de los dispositivos y equipos de medición",
      ["N°", "Equipo / Material", "Marca / Modelo", "Rango de medición", "Apreciación / Incerteza", "Cant."],
      datos.materialesTabla.map((m, i) => [i + 1, m.nombre, m.marca, m.rango, m.apreciacion, m.cantidad]),
      datos.notaTablaMateriales
    );

    const htmlWord = `
      <html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
      <head><meta charset='utf-8'><title>Informe de Laboratorio UNJBG - APA 7</title>
      <!--[if gte mso 9]>
      <xml>
        <w:WordDocument>
          <w:View>Print</w:View>
          <w:Zoom>100</w:Zoom>
        </w:WordDocument>
      </xml>
      <![endif]-->
      <style>
        @page {
          size: 21.59cm 27.94cm;
          margin: 2.54cm 2.54cm 2.54cm 2.54cm;
          mso-page-numbers: 1;
        }
        body {
          font-family: 'Times New Roman', Times, serif;
          font-size: 12pt;
          line-height: 200%;
          color: #000000;
          text-align: left;
        }
        p {
          margin-top: 0;
          margin-bottom: 0;
          text-indent: 1.27cm;
        }
        p.no-indent {
          text-indent: 0;
        }
        p.center {
          text-align: center;
          text-indent: 0;
        }
        h2.apa-level1 {
          font-size: 12pt;
          font-weight: bold;
          text-align: center;
          margin-top: 12pt;
          margin-bottom: 6pt;
        }
        h3.apa-level2 {
          font-size: 12pt;
          font-weight: bold;
          text-align: left;
          margin-top: 12pt;
          margin-bottom: 4pt;
        }
        h4.apa-level3 {
          font-size: 12pt;
          font-weight: bold;
          font-style: italic;
          text-align: left;
          margin-top: 10pt;
          margin-bottom: 4pt;
        }
        p.apa-ref {
          padding-left: 1.27cm;
          text-indent: -1.27cm;
          margin-bottom: 0;
        }
        .caratula {
          page-break-after: always;
          line-height: 150%;
        }
      </style>
      </head>
      <body>
        <div class="caratula">
          <p class="center" style="font-size:14pt;font-weight:bold;">UNIVERSIDAD NACIONAL JORGE BASADRE GROHMANN</p>
          <p class="center"><b>Facultad:</b> ${esc(c.facultad || "[Facultad correspondiente]")}</p>
          <p class="center"><b>Escuela Profesional:</b> ${esc(c.escuela || "[Ingeniería Ambiental / Física / etc.]")}</p>

          <!-- LOGO OFICIAL UNJBG JUSTO DESPUÉS DE ESCUELA PROFESIONAL EN EL CENTRO -->
          <p class="center" style="margin-top:10pt;margin-bottom:10pt;">
            <img src="${logoUri}" width="110" height="128" alt="Escudo UNJBG" />
          </p>

          <p class="center"><b>Laboratorio de:</b> ${esc(c.laboratorio || "FÍSICA")}</p>
          <br/>
          <p class="center" style="font-size:15pt;font-weight:bold;border-top:1.5pt solid #000;border-bottom:1.5pt solid #000;padding:6pt;">INFORME DE LABORATORIO</p>
          <br/>
          <p class="no-indent"><b>Título de la práctica:</b> ${esc(c.tituloPractica || "[Nombre de la práctica]")}</p>
          <br/>
          <p class="no-indent"><b>Autores:</b><br/>${datos.autores.map(a => `&bull; ${esc(a)}`).join("<br/>")}</p>
          <br/>
          <p class="no-indent"><b>Grupo:</b> ${esc(c.grupo || "[ ]")} &nbsp;&nbsp;&nbsp;&nbsp; <b>Horario:</b> ${esc(c.horario || "[ ]")}</p>
          <p class="no-indent"><b>Docente:</b> ${esc(c.docente || "[Grado y Nombre]")}</p>
          <p class="no-indent"><b>Fecha de ejecución:</b> ${esc(c.fechaEjecucion || "[ ]")}</p>
          <p class="no-indent"><b>Fecha de entrega:</b> Tacna, ${esc(c.diaEntrega || "[ ]")} de ${esc(c.mesEntrega || "[ ]")} de ${esc(c.anioEntrega || "2026")}</p>
        </div>

        <h2 class="apa-level1">1. Resumen</h2>
        <p class="no-indent">${esc(datos.resumen)}</p>

        <h2 class="apa-level1">2. Introducción</h2>
        <p>${esc(datos.introduccionTeoria)}</p>
        <h3 class="apa-level2">Objetivos</h3>
        <p><b>Objetivo General:</b> ${esc(datos.objetivoGeneral)}</p>
        <p class="no-indent"><b>Objetivos Específicos:</b></p>
        <ul>${datos.objetivosEspecificos.map(o => `<li>${esc(o)}</li>`).join("")}</ul>

        <h2 class="apa-level1">3. Materiales y Desarrollo Experimental</h2>
        <h3 class="apa-level2">3.1 Materiales</h3>
        <p>${esc(datos.materialesTexto)}</p>
        ${tablaMat}

        <h3 class="apa-level2">3.2 Procedimiento</h3>
        <p>${esc(datos.procedimientoTexto)}</p>

        <p class="no-indent" style="font-weight:bold;margin-top:10pt;">Figura 1</p>
        <p class="no-indent" style="font-style:italic;">${esc(datos.figura1Desc)}</p>
        ${datos.figura1Img ? `<p class="center"><img src="${datos.figura1Img}" style="max-width:440px;"/></p>` : ""}
        <p class="no-indent" style="font-size:10pt;"><i>${esc(datos.figura1Nota || "")}</i></p>

        ${renderTablaAPA7(2, datos.tituloTablaCruda, datos.tablaCruda.headers, datos.tablaCruda.rows, datos.notaTablaCruda)}

        <h2 class="apa-level1">4. Resultados y Discusión</h2>
        ${renderTablaAPA7(3, datos.tituloTablaResultados, datos.tablaResultados.headers, datos.tablaResultados.rows, datos.notaTablaResultados)}

        <p class="no-indent" style="font-weight:bold;margin-top:10pt;">Figura 2</p>
        <p class="no-indent" style="font-style:italic;">${esc(datos.figura2Desc)}</p>
        ${datos.figura2Img ? `<p class="center"><img src="${datos.figura2Img}" style="max-width:440px;"/></p>` : ""}
        <p class="no-indent" style="font-size:10pt;"><i>${esc(datos.figura2Nota || "")}</i></p>

        <p>${esc(datos.discusionTexto)}</p>

        <h2 class="apa-level1">5. Conclusiones</h2>
        <ol>${datos.conclusiones.map(con => `<li>${esc(con)}</li>`).join("")}</ol>
        <p><b>Fuentes de error y aproximaciones:</b> ${esc(datos.fuentesError)}</p>

        <h2 class="apa-level1">6. Reflexión Argumentada</h2>
        <p>${esc(datos.reflexionTexto)}</p>

        <h2 class="apa-level1">7. Referencias</h2>
        ${datos.referencias.map(r => `<p class="apa-ref">${esc(r)}</p>`).join("")}

        <h2 class="apa-level1">8. Cuestionario</h2>
        ${datos.cuestionario.map((q, i) => `<p class="no-indent"><b>Pregunta ${i + 1}:</b> ${esc(q.pregunta)}</p><p>${esc(q.respuesta)}</p>`).join("")}

        <h2 class="apa-level1">9. Apéndices</h2>
        <p>${esc(datos.apendicesTexto)}</p>
      </body>
      </html>
    `;
    const nombre = `${this.slugify(c.tituloPractica)}_APA7.doc`;
    this.descargarArchivo("﻿" + htmlWord, nombre, "application/msword;charset=utf-8");
  }
};
