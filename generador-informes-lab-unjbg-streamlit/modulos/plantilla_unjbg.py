"""
PLANTILLA OFICIAL DE INFORME DE LABORATORIO - UNJBG (APA 7.ª EDICIÓN)
Archivo modular de configuración institucional, reglas APA 7 y guías académicas.

CÓMO ACTUALIZAR ESTE ARCHIVO EN EL FUTURO:
- Para agregar facultades o escuelas: edita FACULTADES_SUGERIDAS y ESCUELAS_SUGERIDAS.
- Para cambiar el logotipo institucional: reemplaza assets/logo-unjbg.png.
- Para modificar las instrucciones de cada sección: edita GUIAS_SECCIONES.
"""

INSTITUCION = {
    "universidad": "UNIVERSIDAD NACIONAL JORGE BASADRE GROHMANN",
    "ciudad": "Tacna",
    "anio_defecto": "2026",
    "laboratorio_defecto": "FÍSICA",
    "logo_path": "assets/logo-unjbg.png",
}

FACULTADES_SUGERIDAS = [
    "Facultad de Ingeniería (FAIN)",
    "Facultad de Ingeniería Civil, Arquitectura y Geotecnia (FIAG)",
    "Facultad de Ciencias (FACI)",
    "Facultad de Ciencias Agropecuarias (FCAG)",
    "Facultad de Ciencias de la Salud (FACS)",
    "Facultad de Ciencias Jurídicas y Empresariales (FCJE)",
    "Facultad de Educación, Comunicación y Humanidades (FECH)",
]

ESCUELAS_SUGERIDAS = [
    "Ingeniería Ambiental",
    "Física Aplicada",
    "Ingeniería Civil",
    "Ingeniería de Minas",
    "Ingeniería Geológica - Geotecnia",
    "Ingeniería Metalúrgica",
    "Ingeniería Mecánica",
    "Ingeniería en Informática y Sistemas",
    "Ingeniería Química",
    "Biología - Microbiología",
    "Matemática",
]

REGLAS_APA7 = {
    "fuente": "Times New Roman, 12 pt",
    "interlineado": "Doble (2.0)",
    "margenes": "2.54 cm (1 pulgada) en todos los lados",
    "alineacion": "Alineado a la izquierda (sin justificar)",
    "sangria_parrafo": "1.27 cm (0.5 pulgadas) en la primera línea de cada párrafo",
    "sangria_referencias": "Sangría francesa de 1.27 cm (0.5 pulgadas) y orden alfabético",
    "citas": "Sistema Autor-Fecha: (Apellido, Año) o Apellido (Año)",
    "tablas": "Número en negrita arriba (Tabla 1), título en cursiva debajo, solo bordes horizontales (sin líneas verticales) y Nota. al pie.",
    "figuras": "Número en negrita arriba (Figura 1), título en cursiva debajo, imagen centrada y Nota. al pie.",
}

GUIAS_SECCIONES = {
    "resumen": (
        "Redactado en tercera persona, tiempo pasado, vocabulario formal y con una extensión "
        "aproximada de 15 líneas (en APA 7: párrafo único sin sangría inicial, interlineado doble). "
        "Deberá comprender una visión integral del trabajo: breve fundamentación teórica, metodología "
        "empleada, resultados más relevantes con valores numéricos y su incerteza, y conclusiones "
        "principales. Se elabora al final del informe."
    ),
    "introduccion": (
        "Exposición de las motivaciones del trabajo experimental. Debe incluir la mínima base teórica "
        "que permita la comprensión del fenómeno estudiado, las ecuaciones debidamente numeradas en "
        "orden correlativo (1), (2)..., y las citas bibliográficas en formato APA 7.ª edición (Autor, Año). "
        "Al final del apartado se indican claramente los objetivos de la práctica: magnitudes a determinar, "
        "leyes a verificar y fenómenos a estudiar. No debe incluir resultados ni conclusiones."
    ),
    "materiales": (
        "Descripción de los dispositivos, reactivos y equipos de medición, especificando características "
        "técnicas relevantes como apreciación, rango de medición y marca. En APA 7, la Tabla 1 lleva el "
        "número en negrita arriba, título en cursiva debajo y únicamente bordes horizontales."
    ),
    "procedimiento": (
        "Descripción del método de medición en tiempo pasado. Se recomienda la presentación de un esquema "
        "del dispositivo experimental empleado (Figura 1, con número en negrita arriba, título en cursiva "
        "y Nota. al pie). Las tablas deben contener los datos tomados directamente en el experimento. "
        "No se incluyen resultados procesados."
    ),
    "resultados": (
        "Presentación de las mediciones realizadas en forma de tablas y gráficos bajo normativa APA 7.ª "
        "edición (número en negrita + título en cursiva + Nota. al pie). Toda gráfica debe contener: título, "
        "nombre de cada eje con sus unidades, escalas y nota al pie. Se debe incluir la evaluación de "
        "incertezas, ajustes de curvas y cálculo de pendientes cuando corresponda. Se discute la validez, "
        "precisión e interpretación de los resultados frente al modelo teórico existente citando (Autor, Año)."
    ),
    "conclusiones": (
        "Contiene la argumentación de cómo, a partir de los resultados obtenidos, se demuestra aquello "
        "planteado como objetivo. Todas las conclusiones deben estar sustentadas exclusivamente en los "
        "datos experimentales. Se debe incluir el análisis de las posibles fuentes de error y las "
        "aproximaciones respecto al caso ideal."
    ),
    "reflexion": (
        "Comentario fundamentado que permite relacionar la teoría evaluada experimentalmente con el "
        "campo de acción profesional."
    ),
    "referencias": (
        "Relación ordenada alfabéticamente de la bibliografía citada durante el desarrollo del informe, "
        "bajo formato normado APA 7.ª edición (sangría francesa de 1.27 cm, sin corchetes ni viñetas). "
        "Ejemplo: Alonso, M., & Finn, E. J. (1986). Física: Vol. I. Mecánica. Fondo Educativo Interamericano."
    ),
    "cuestionario": (
        "Preguntas que deja el docente en la práctica de laboratorio de física para resolverlo, "
        "fundamentando con citas APA 7 (Autor, Año) cuando corresponda."
    ),
    "apendices": (
        "Información complementaria que ayuda a clarificar el contenido, como cálculos detallados para "
        "la obtención de resultados o estimación de incertezas, que en el cuerpo principal distraerían "
        "la atención del lector."
    ),
}
