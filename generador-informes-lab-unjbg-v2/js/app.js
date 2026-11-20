/**
 * LÓGICA PRINCIPAL DE LA APLICACIÓN - GENERADOR DE INFORMES UNJBG (APA 7.ª EDICIÓN)
 */

const STORAGE_KEY = "unjbg_informe_lab_apa7_v2";

let estado = {
  caratula: {
    facultad: "",
    escuela: "",
    laboratorio: "FÍSICA",
    tituloPractica: "",
    grupo: "",
    horario: "",
    docente: "",
    fechaEjecucion: "",
    diaEntrega: "",
    mesEntrega: "",
    anioEntrega: "2026"
  },
  autores: ["Apellidos y Nombres - Código Universitario"],
  resumen: "",
  introduccionTeoria: "",
  objetivoGeneral: "",
  objetivosEspecificos: [""],
  materialesTexto: "",
  tituloTablaMateriales: "Características técnicas de los dispositivos y equipos de medición empleados",
  materialesTabla: [
    { nombre: "", marca: "", rango: "", apreciacion: "", cantidad: "1" }
  ],
  notaTablaMateriales: "Nota. Elaboración propia a partir de las especificaciones técnicas del laboratorio.",
  procedimientoTexto: "",
  figura1Desc: "Esquema del dispositivo experimental empleado en la práctica",
  figura1Nota: "Nota. Montaje experimental realizado en el Laboratorio de Física de la UNJBG.",
  figura1Img: "",
  tituloTablaCruda: "Datos experimentales registrados directamente durante la medición",
  tablaCruda: {
    headers: ["Medición N°", "Magnitud X [unidad]", "Magnitud Y [unidad]"],
    rows: [
      ["1", "", ""],
      ["2", "", ""],
      ["3", "", ""]
    ]
  },
  notaTablaCruda: "Nota. Mediciones directas obtenidas sin procesamiento matemático.",
  tituloTablaResultados: "Valores procesados, incertezas experimentales y comparación con el modelo teórico",
  tablaResultados: {
    headers: ["Ensayo", "Resultado ± Incerteza", "Valor Teórico", "Error Relativo (%)"],
    rows: [
      ["1", "", "", ""],
      ["2", "", "", ""]
    ]
  },
  notaTablaResultados: "Nota. Las incertezas fueron calculadas mediante propagación de errores.",
  figura2Desc: "Relación experimental entre [Magnitud Y (unidad)] y [Magnitud X (unidad)]",
  figura2Nota: "Nota. Ajuste lineal por mínimos cuadrados y = mx + b, R² = ...",
  figura2Img: "",
  discusionTexto: "",
  conclusiones: [""],
  fuentesError: "",
  reflexionTexto: "",
  referencias: [
    "Alonso, M., & Finn, E. J. (1986). Física: Vol. I. Mecánica. Fondo Educativo Interamericano."
  ],
  cuestionario: [
    { pregunta: "", respuesta: "" }
  ],
  apendicesTexto: ""
};

document.addEventListener("DOMContentLoaded", () => {
  cargarListasSugeridas();
  inyectarGuiasDesdePlantilla();
  cargarDesdeLocalStorage();
  renderizarTodo();
  enlazarEventos();
});

function cargarListasSugeridas() {
  const dlFac = document.getElementById("listaFacultades");
  const dlEsc = document.getElementById("listaEscuelas");
  PLANTILLA_UNJBG.institucion.facultadesSugeridas.forEach(f => {
    const opt = document.createElement("option");
    opt.value = f;
    dlFac.appendChild(opt);
  });
  PLANTILLA_UNJBG.institucion.escuelasSugeridas.forEach(e => {
    const opt = document.createElement("option");
    opt.value = e;
    dlEsc.appendChild(opt);
  });
}

function inyectarGuiasDesdePlantilla() {
  const mapaGuias = {};
  PLANTILLA_UNJBG.secciones.forEach(sec => {
    if (sec.guia) mapaGuias[sec.id] = sec.guia;
  });

  document.querySelectorAll(".guia-box").forEach(box => {
    const key = box.getAttribute("data-guia");
    if (mapaGuias[key]) {
      box.innerHTML = `<strong>Guía APA 7.ª Ed.:</strong> ${mapaGuias[key]}`;
    }
  });
}

function guardarEnLocalStorage() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(estado));
    const ind = document.getElementById("estadoGuardado");
    if (ind) {
      const hora = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
      ind.textContent = `Guardado automático (${hora})`;
    }
  } catch (e) {
    console.warn("No se pudo guardar en localStorage:", e);
  }
}

function cargarDesdeLocalStorage() {
  try {
    const guardado = localStorage.getItem(STORAGE_KEY);
    if (guardado) {
      const parsed = JSON.parse(guardado);
      estado = { ...estado, ...parsed };
    }
  } catch (e) {
    console.warn("Error leyendo respaldo local:", e);
  }
}

function renderizarTodo() {
  Object.keys(estado.caratula).forEach(k => {
    const el = document.getElementById(k);
    if (el) el.value = estado.caratula[k] || "";
  });

  const camposTexto = [
    "resumen", "introduccionTeoria", "objetivoGeneral",
    "materialesTexto", "tituloTablaMateriales", "notaTablaMateriales",
    "procedimientoTexto", "figura1Desc", "figura1Nota",
    "tituloTablaCruda", "notaTablaCruda",
    "tituloTablaResultados", "notaTablaResultados",
    "figura2Desc", "figura2Nota",
    "discusionTexto", "fuentesError",
    "reflexionTexto", "apendicesTexto"
  ];
  camposTexto.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = estado[id] || "";
  });

  actualizarContadorResumen();
  renderAutores();
  renderObjetivos();
  renderTablaMateriales();
  renderTablaDinamica("tablaDatosCrudos", estado.tablaCruda);
  renderTablaDinamica("tablaResultados", estado.tablaResultados);
  renderConclusiones();
  renderReferencias();
  renderCuestionario();
  renderPreviewsImagenes();
}

function actualizarContadorResumen() {
  const texto = estado.resumen || "";
  const lineasAprox = texto.trim() ? Math.ceil(texto.length / 85) : 0;
  const pill = document.getElementById("contadorResumen");
  pill.textContent = `${lineasAprox} líneas aprox. (Meta: ~15 líneas)`;
  if (lineasAprox >= 12 && lineasAprox <= 18) {
    pill.classList.add("ok");
  } else {
    pill.classList.remove("ok");
  }
}

function renderAutores() {
  const cont = document.getElementById("listaAutores");
  cont.innerHTML = "";
  estado.autores.forEach((autor, idx) => {
    const row = document.createElement("div");
    row.className = "dynamic-row";
    row.innerHTML = `
      <input type="text" value="${escapeAttr(autor)}" placeholder="Apellidos y Nombres - Código Universitario" />
      ${estado.autores.length > 1 ? `<button type="button" class="btn-danger-icon no-print" title="Eliminar">×</button>` : ""}
    `;
    row.querySelector("input").addEventListener("input", e => {
      estado.autores[idx] = e.target.value;
      guardarEnLocalStorage();
    });
    const btnDel = row.querySelector("button");
    if (btnDel) {
      btnDel.addEventListener("click", () => {
        estado.autores.splice(idx, 1);
        renderAutores();
        guardarEnLocalStorage();
      });
    }
    cont.appendChild(row);
  });
}

function renderObjetivos() {
  const cont = document.getElementById("listaObjetivos");
  cont.innerHTML = "";
  estado.objetivosEspecificos.forEach((obj, idx) => {
    const row = document.createElement("div");
    row.className = "dynamic-row";
    row.innerHTML = `
      <input type="text" value="${escapeAttr(obj)}" placeholder="Objetivo específico ${idx + 1}..." />
      ${estado.objetivosEspecificos.length > 1 ? `<button type="button" class="btn-danger-icon no-print">×</button>` : ""}
    `;
    row.querySelector("input").addEventListener("input", e => {
      estado.objetivosEspecificos[idx] = e.target.value;
      guardarEnLocalStorage();
    });
    const btnDel = row.querySelector("button");
    if (btnDel) {
      btnDel.addEventListener("click", () => {
        estado.objetivosEspecificos.splice(idx, 1);
        renderObjetivos();
        guardarEnLocalStorage();
      });
    }
    cont.appendChild(row);
  });
}

function renderTablaMateriales() {
  const tbody = document.querySelector("#tablaMateriales tbody");
  tbody.innerHTML = "";
  estado.materialesTabla.forEach((item, idx) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${idx + 1}</td>
      <td><input type="text" data-field="nombre" value="${escapeAttr(item.nombre)}" placeholder="Ej. Cronómetro digital" /></td>
      <td><input type="text" data-field="marca" value="${escapeAttr(item.marca)}" placeholder="Casio" /></td>
      <td><input type="text" data-field="rango" value="${escapeAttr(item.rango)}" placeholder="0 - 999 s" /></td>
      <td><input type="text" data-field="apreciacion" value="${escapeAttr(item.apreciacion)}" placeholder="0.01 s" /></td>
      <td><input type="text" data-field="cantidad" value="${escapeAttr(item.cantidad)}" placeholder="1" /></td>
      <td class="no-print"><button type="button" class="btn-danger-icon">×</button></td>
    `;
    tr.querySelectorAll("input").forEach(inp => {
      inp.addEventListener("input", e => {
        estado.materialesTabla[idx][e.target.dataset.field] = e.target.value;
        guardarEnLocalStorage();
      });
    });
    tr.querySelector("button").addEventListener("click", () => {
      if (estado.materialesTabla.length > 1) {
        estado.materialesTabla.splice(idx, 1);
        renderTablaMateriales();
        guardarEnLocalStorage();
      }
    });
    tbody.appendChild(tr);
  });
}

function renderTablaDinamica(tableId, tablaData) {
  const table = document.getElementById(tableId);
  const thead = table.querySelector("thead");
  const tbody = table.querySelector("tbody");

  thead.innerHTML = "";
  const trHead = document.createElement("tr");
  tablaData.headers.forEach((h, colIdx) => {
    const th = document.createElement("th");
    th.innerHTML = `<input type="text" value="${escapeAttr(h)}" placeholder="Columna ${colIdx + 1}" />`;
    th.querySelector("input").addEventListener("input", e => {
      tablaData.headers[colIdx] = e.target.value;
      guardarEnLocalStorage();
    });
    trHead.appendChild(th);
  });
  const thAction = document.createElement("th");
  thAction.className = "no-print";
  thAction.style.width = "45px";
  trHead.appendChild(thAction);
  thead.appendChild(trHead);

  tbody.innerHTML = "";
  tablaData.rows.forEach((rowArr, rowIdx) => {
    const tr = document.createElement("tr");
    rowArr.forEach((val, colIdx) => {
      const td = document.createElement("td");
      td.innerHTML = `<input type="text" value="${escapeAttr(val)}" />`;
      td.querySelector("input").addEventListener("input", e => {
        tablaData.rows[rowIdx][colIdx] = e.target.value;
        guardarEnLocalStorage();
      });
      tr.appendChild(td);
    });
    const tdDel = document.createElement("td");
    tdDel.className = "no-print";
    tdDel.innerHTML = `<button type="button" class="btn-danger-icon">×</button>`;
    tdDel.querySelector("button").addEventListener("click", () => {
      if (tablaData.rows.length > 1) {
        tablaData.rows.splice(rowIdx, 1);
        renderTablaDinamica(tableId, tablaData);
        guardarEnLocalStorage();
      }
    });
    tr.appendChild(tdDel);
    tbody.appendChild(tr);
  });
}

function renderConclusiones() {
  const cont = document.getElementById("listaConclusiones");
  cont.innerHTML = "";
  estado.conclusiones.forEach((c, idx) => {
    const row = document.createElement("div");
    row.className = "dynamic-row";
    row.innerHTML = `
      <textarea rows="2" placeholder="Conclusión ${idx + 1} sustentada en los datos experimentales...">${escapeHtml(c)}</textarea>
      ${estado.conclusiones.length > 1 ? `<button type="button" class="btn-danger-icon no-print">×</button>` : ""}
    `;
    row.querySelector("textarea").addEventListener("input", e => {
      estado.conclusiones[idx] = e.target.value;
      guardarEnLocalStorage();
    });
    const btnDel = row.querySelector("button");
    if (btnDel) {
      btnDel.addEventListener("click", () => {
        estado.conclusiones.splice(idx, 1);
        renderConclusiones();
        guardarEnLocalStorage();
      });
    }
    cont.appendChild(row);
  });
}

function renderReferencias() {
  const cont = document.getElementById("listaReferencias");
  cont.innerHTML = "";
  estado.referencias.forEach((ref, idx) => {
    const row = document.createElement("div");
    row.className = "dynamic-row";
    row.innerHTML = `
      <input type="text" value="${escapeAttr(ref)}" placeholder="Apellido, N. (Año). Título en cursiva. Editorial." />
      ${estado.referencias.length > 1 ? `<button type="button" class="btn-danger-icon no-print">×</button>` : ""}
    `;
    row.querySelector("input").addEventListener("input", e => {
      estado.referencias[idx] = e.target.value;
      guardarEnLocalStorage();
    });
    const btnDel = row.querySelector("button");
    if (btnDel) {
      btnDel.addEventListener("click", () => {
        estado.referencias.splice(idx, 1);
        renderReferencias();
        guardarEnLocalStorage();
      });
    }
    cont.appendChild(row);
  });
}

function renderCuestionario() {
  const cont = document.getElementById("listaCuestionario");
  cont.innerHTML = "";
  estado.cuestionario.forEach((item, idx) => {
    const box = document.createElement("div");
    box.className = "cuestionario-item";
    box.innerHTML = `
      <div class="block-header">
        <strong>Pregunta ${idx + 1}</strong>
        ${estado.cuestionario.length > 1 ? `<button type="button" class="btn-danger-icon no-print">Eliminar</button>` : ""}
      </div>
      <input type="text" class="q-preg" value="${escapeAttr(item.pregunta)}" placeholder="Enunciado de la pregunta del docente..." />
      <textarea rows="3" class="q-resp" placeholder="Desarrollo y respuesta fundamentada con citas APA 7 (Autor, Año)...">${escapeHtml(item.respuesta)}</textarea>
    `;
    box.querySelector(".q-preg").addEventListener("input", e => {
      estado.cuestionario[idx].pregunta = e.target.value;
      guardarEnLocalStorage();
    });
    box.querySelector(".q-resp").addEventListener("input", e => {
      estado.cuestionario[idx].respuesta = e.target.value;
      guardarEnLocalStorage();
    });
    const btnDel = box.querySelector("button");
    if (btnDel) {
      btnDel.addEventListener("click", () => {
        estado.cuestionario.splice(idx, 1);
        renderCuestionario();
        guardarEnLocalStorage();
      });
    }
    cont.appendChild(box);
  });
}

function renderPreviewsImagenes() {
  const p1 = document.getElementById("previewFigura1");
  const p2 = document.getElementById("previewFigura2");
  p1.innerHTML = estado.figura1Img ? `<img src="${estado.figura1Img}" alt="Figura 1" />` : "";
  p2.innerHTML = estado.figura2Img ? `<img src="${estado.figura2Img}" alt="Figura 2" />` : "";
}

function enlazarEventos() {
  Object.keys(estado.caratula).forEach(k => {
    const el = document.getElementById(k);
    if (el) {
      el.addEventListener("input", e => {
        estado.caratula[k] = e.target.value;
        guardarEnLocalStorage();
      });
    }
  });

  const camposTexto = [
    "resumen", "introduccionTeoria", "objetivoGeneral",
    "materialesTexto", "tituloTablaMateriales", "notaTablaMateriales",
    "procedimientoTexto", "figura1Desc", "figura1Nota",
    "tituloTablaCruda", "notaTablaCruda",
    "tituloTablaResultados", "notaTablaResultados",
    "figura2Desc", "figura2Nota",
    "discusionTexto", "fuentesError",
    "reflexionTexto", "apendicesTexto"
  ];
  camposTexto.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener("input", e => {
        estado[id] = e.target.value;
        if (id === "resumen") actualizarContadorResumen();
        guardarEnLocalStorage();
      });
    }
  });

  document.getElementById("btnAgregarAutor").addEventListener("click", () => {
    estado.autores.push("");
    renderAutores();
    guardarEnLocalStorage();
  });

  document.getElementById("btnAgregarObjetivo").addEventListener("click", () => {
    estado.objetivosEspecificos.push("");
    renderObjetivos();
    guardarEnLocalStorage();
  });

  document.getElementById("btnAgregarMaterial").addEventListener("click", () => {
    estado.materialesTabla.push({ nombre: "", marca: "", rango: "", apreciacion: "", cantidad: "1" });
    renderTablaMateriales();
    guardarEnLocalStorage();
  });

  document.getElementById("btnAgregarColCruda").addEventListener("click", () => {
    estado.tablaCruda.headers.push(`Magnitud ${estado.tablaCruda.headers.length + 1}`);
    estado.tablaCruda.rows.forEach(r => r.push(""));
    renderTablaDinamica("tablaDatosCrudos", estado.tablaCruda);
    guardarEnLocalStorage();
  });

  document.getElementById("btnAgregarFilaCruda").addEventListener("click", () => {
    const nueva = estado.tablaCruda.headers.map((_, i) => i === 0 ? String(estado.tablaCruda.rows.length + 1) : "");
    estado.tablaCruda.rows.push(nueva);
    renderTablaDinamica("tablaDatosCrudos", estado.tablaCruda);
    guardarEnLocalStorage();
  });

  document.getElementById("btnAgregarColRes").addEventListener("click", () => {
    estado.tablaResultados.headers.push(`Columna ${estado.tablaResultados.headers.length + 1}`);
    estado.tablaResultados.rows.forEach(r => r.push(""));
    renderTablaDinamica("tablaResultados", estado.tablaResultados);
    guardarEnLocalStorage();
  });

  document.getElementById("btnAgregarFilaRes").addEventListener("click", () => {
    const nueva = estado.tablaResultados.headers.map((_, i) => i === 0 ? String(estado.tablaResultados.rows.length + 1) : "");
    estado.tablaResultados.rows.push(nueva);
    renderTablaDinamica("tablaResultados", estado.tablaResultados);
    guardarEnLocalStorage();
  });

  document.getElementById("btnAgregarConclusion").addEventListener("click", () => {
    estado.conclusiones.push("");
    renderConclusiones();
    guardarEnLocalStorage();
  });

  document.getElementById("btnAgregarReferencia").addEventListener("click", () => {
    estado.referencias.push("");
    renderReferencias();
    guardarEnLocalStorage();
  });

  document.getElementById("btnOrdenarAPA").addEventListener("click", () => {
    estado.referencias = estado.referencias
      .filter(r => r.trim() !== "")
      .sort((a, b) => a.localeCompare(b, "es", { sensitivity: "base" }));
    if (estado.referencias.length === 0) estado.referencias.push("");
    renderReferencias();
    guardarEnLocalStorage();
  });

  document.getElementById("btnInsertarAPA").addEventListener("click", () => {
    const tipo = document.getElementById("apaTipoFuente").value;
    const autor = document.getElementById("apaAutor").value.trim() || "Autor, A.";
    const anio = document.getElementById("apaAnio").value.trim() || "2026";
    const titulo = document.getElementById("apaTitulo").value.trim() || "Título de la obra";
    const fuente = document.getElementById("apaFuente").value.trim() || "Editorial / Fuente";

    let citaFormateada = "";
    if (tipo === "libro") {
      citaFormateada = `${autor} (${anio}). ${titulo}. ${fuente}.`;
    } else if (tipo === "articulo") {
      citaFormateada = `${autor} (${anio}). ${titulo}. ${fuente}.`;
    } else {
      citaFormateada = `${autor} (${anio}). ${titulo}. ${fuente}`;
    }

    if (estado.referencias.length === 1 && estado.referencias[0].trim() === "") {
      estado.referencias[0] = citaFormateada;
    } else {
      estado.referencias.push(citaFormateada);
    }
    estado.referencias.sort((a, b) => a.localeCompare(b, "es", { sensitivity: "base" }));

    document.getElementById("apaAutor").value = "";
    document.getElementById("apaAnio").value = "";
    document.getElementById("apaTitulo").value = "";
    document.getElementById("apaFuente").value = "";

    renderReferencias();
    guardarEnLocalStorage();
  });

  document.getElementById("btnAgregarPregunta").addEventListener("click", () => {
    estado.cuestionario.push({ pregunta: "", respuesta: "" });
    renderCuestionario();
    guardarEnLocalStorage();
  });

  document.getElementById("inputFigura1").addEventListener("change", e => leerImagen(e, "figura1Img"));
  document.getElementById("inputFigura2").addEventListener("change", e => leerImagen(e, "figura2Img"));

  document.getElementById("btnToggleGuias").addEventListener("click", e => {
    document.body.classList.toggle("ocultar-guias");
    e.target.textContent = document.body.classList.contains("ocultar-guias") ? "Mostrar Guías" : "Ocultar Guías";
  });

  document.getElementById("btnExportarJSON").addEventListener("click", () => Exportadores.aJSON(estado));
  document.getElementById("btnExportarMD").addEventListener("click", () => Exportadores.aMarkdown(estado));
  document.getElementById("btnExportarTEX").addEventListener("click", () => Exportadores.aLaTeX(estado));
  document.getElementById("btnExportarDOC").addEventListener("click", () => Exportadores.aWord(estado));

  document.getElementById("inputImportarJSON").addEventListener("change", e => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = ev => {
      try {
        const data = JSON.parse(ev.target.result);
        estado = { ...estado, ...data };
        renderizarTodo();
        guardarEnLocalStorage();
        alert("Proyecto cargado correctamente.");
      } catch (err) {
        alert("El archivo seleccionado no es un JSON válido.");
      }
    };
    reader.readAsText(file);
  });

  document.getElementById("btnCargarEjemplo").addEventListener("click", () => {
    cargarDatosDeEjemplo();
    renderizarTodo();
    guardarEnLocalStorage();
  });

  document.getElementById("btnLimpiarTodo").addEventListener("click", () => {
    if (confirm("¿Seguro que deseas borrar todos los campos del informe actual?")) {
      localStorage.removeItem(STORAGE_KEY);
      location.reload();
    }
  });
}

function leerImagen(event, campoDestino) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    estado[campoDestino] = e.target.result;
    renderPreviewsImagenes();
    guardarEnLocalStorage();
  };
  reader.readAsDataURL(file);
}

function cargarDatosDeEjemplo() {
  estado.caratula = {
    facultad: "Facultad de Ingeniería (FAIN)",
    escuela: "Ingeniería Ambiental",
    laboratorio: "FÍSICA",
    tituloPractica: "Determinación de la Aceleración de la Gravedad mediante el Péndulo Simple",
    grupo: "A",
    horario: "Lunes 14:00 - 16:00",
    docente: "Dr. Juan Pérez Mamani",
    fechaEjecucion: "12/11/2026",
    diaEntrega: "19",
    mesEntrega: "noviembre",
    anioEntrega: "2026"
  };
  estado.autores = [
    "Quispe Flores, María Elena - 2025-119042",
    "Condori Mamani, Carlos Alberto - 2025-119058"
  ];
  estado.resumen = "Se determinó experimentalmente la aceleración de la gravedad local en la ciudad de Tacna mediante el análisis del movimiento armónico simple de un péndulo ideal para oscilaciones de pequeña amplitud. Se midió el periodo de oscilación T para cinco longitudes de cuerda comprendidas entre 0.200 m y 1.000 m, registrando el tiempo de 20 oscilaciones completas con un cronómetro digital de 0.01 s de apreciación. Mediante ajuste lineal por mínimos cuadrados de T² en función de la longitud L, se obtuvo una pendiente de (4.03 ± 0.04) s²/m, de la cual se calculó una aceleración gravitacional experimental de g = (9.79 ± 0.10) m/s². Al comparar este resultado con el valor referencial teórico de 9.78 m/s², se determinó un error relativo porcentual de 0.10 %, verificando la validez de la relación cuadrática entre el periodo y la longitud del péndulo.";
  estado.introduccionTeoria = "El estudio del movimiento oscilatorio constituye uno de los fundamentos de la mecánica clásica (Alonso & Finn, 1986). Un péndulo simple consiste en una masa puntual suspendida de un hilo inextensible y de masa despreciable. Según Serway y Jewett (2018), para desplazamientos angulares pequeños (θ < 10°), el movimiento se aproxima a un Movimiento Armónico Simple cuyo periodo T está dado por:

T = 2π √(L / g)   (1)

Elevando al cuadrado la ecuación (1), se obtiene la relación lineal:

T² = (4π² / g) L   (2)";
  estado.objetivoGeneral = "Determinar experimentalmente el valor de la aceleración de la gravedad (g) mediante el estudio del periodo de oscilación de un péndulo simple.";
  estado.objetivosEspecificos = [
    "Verificar la dependencia lineal entre el cuadrado del periodo (T²) y la longitud del péndulo (L).",
    "Evaluar las incertezas experimentales asociadas a las mediciones directas e indirectas."
  ];
  estado.referencias = [
    "Alonso, M., & Finn, E. J. (1986). Física: Vol. I. Mecánica. Fondo Educativo Interamericano.",
    "Serway, R. A., & Jewett, J. W. (2018). Física para ciencias e ingeniería (10.ª ed., Vol. 1). Cengage Learning."
  ];
}

function escapeAttr(str) {
  return String(str || "").replace(/"/g, "&quot;");
}

function escapeHtml(str) {
  return String(str || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
