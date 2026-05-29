import streamlit as st
from pathlib import Path
from evaluador import evaluar_sentido_global

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Sentido Global del Texto",
    page_icon="📖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ── Estilos CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Source+Sans+3:wght@300;400;600&display=swap');

/* ── Variables de tema ── */
:root {
    --sg-bg-card: #FEFDF8;
    --sg-bg-card-hover: #EEF6EE;
    --sg-border: #dde8d9;
    --sg-text: #2d2d2d;
    --sg-text-muted: #6b8f6e;
    --sg-green: #2C5F2E;
    --sg-green-dark: #1a3d1c;
    --sg-green-light: #EEF6EE;
    --sg-resultado-bg: #f7f9f4;
    --sg-barra-bg: #e0e8df;
    --sg-shadow: rgba(0,0,0,0.07);
    --sg-puntaje-color: #2C5F2E;
}

@media (prefers-color-scheme: dark) {
    :root {
        --sg-bg-card: #1a2420;
        --sg-bg-card-hover: #243029;
        --sg-border: #2e4a35;
        --sg-text: #d4ddd6;
        --sg-text-muted: #7faa82;
        --sg-green: #4a9e50;
        --sg-green-dark: #3d8a42;
        --sg-green-light: #1e3028;
        --sg-resultado-bg: #1a2420;
        --sg-barra-bg: #2a3a2d;
        --sg-shadow: rgba(0,0,0,0.3);
        --sg-puntaje-color: #6bc270;
    }
}

html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }
h1, h2, h3 { font-family: 'Lora', serif; }

/* ── Botones de selección de texto ── */
.texto-btn {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    border: 2px solid var(--sg-border);
    background: var(--sg-bg-card);
    cursor: pointer;
    transition: all 0.15s ease;
    text-align: left;
    width: 100%;
    font-family: 'Source Sans 3', sans-serif;
}

.texto-btn:hover {
    border-color: var(--sg-green);
    background: var(--sg-bg-card-hover);
}

.texto-btn.activo {
    border-color: var(--sg-green);
    background: var(--sg-bg-card-hover);
    box-shadow: 0 0 0 3px rgba(74,158,80,0.15);
}

.texto-btn .num {
    min-width: 2rem;
    height: 2rem;
    border-radius: 50%;
    background: var(--sg-green);
    color: white;
    font-weight: 700;
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.texto-btn.activo .num { background: var(--sg-green-dark); }

.texto-btn .titulo-btn {
    font-size: 0.97rem;
    color: var(--sg-text);
    font-weight: 500;
    line-height: 1.3;
}

.texto-btn.activo .titulo-btn {
    color: var(--sg-puntaje-color);
    font-weight: 600;
}

/* ── Tarjeta del texto ── */
.texto-card {
    background: var(--sg-bg-card);
    border-left: 4px solid var(--sg-green);
    border-radius: 4px 8px 8px 4px;
    padding: 1.5rem 1.8rem;
    margin: 1rem 0;
    line-height: 1.8;
    color: var(--sg-text);
    font-size: 1.02rem;
    box-shadow: 0 2px 8px var(--sg-shadow);
}

/* ── Resultado ── */
.puntaje-badge {
    display: inline-block;
    font-size: 3rem;
    font-family: 'Lora', serif;
    font-weight: 600;
    color: var(--sg-puntaje-color);
    line-height: 1;
}

.nivel-badge {
    display: inline-block;
    padding: 0.3rem 1rem;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.95rem;
    margin-left: 0.8rem;
    vertical-align: middle;
}

.resultado-bloque {
    background: var(--sg-resultado-bg);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    border: 1px solid var(--sg-border);
}

.resultado-bloque .etiqueta {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--sg-text-muted);
    margin-bottom: 0.3rem;
}

.resultado-bloque .contenido {
    color: var(--sg-text);
    font-size: 0.97rem;
    line-height: 1.6;
}

.ejemplo-ideal {
    background: var(--sg-green-light);
    border: 1px solid var(--sg-green);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    font-style: italic;
    color: var(--sg-puntaje-color);
}

.motivador {
    background: linear-gradient(135deg, #2C5F2E 0%, #4a8c4d 100%);
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    color: white;
    text-align: center;
    font-size: 1rem;
    line-height: 1.6;
    margin-top: 1rem;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] { background: #1e3d20; }
section[data-testid="stSidebar"] * { color: #d4e8d5 !important; }

/* ── Barra de puntaje ── */
.barra-contenedor {
    background: var(--sg-barra-bg);
    border-radius: 10px;
    height: 12px;
    margin: 0.5rem 0 1rem 0;
    overflow: hidden;
}
.barra-relleno { height: 100%; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)


# ── Utilidades ───────────────────────────────────────────────────────────────

def cargar_textos(carpeta: str = "TEXTOS") -> list[dict]:
    """Carga todos los .md de la carpeta TEXTOS, retorna lista ordenada."""
    textos = []
    ruta = Path(carpeta)
    if not ruta.exists():
        return textos
    for i, archivo in enumerate(sorted(ruta.glob("*.md")), start=1):
        contenido = archivo.read_text(encoding="utf-8")
        lineas = contenido.strip().splitlines()
        titulo = archivo.stem.replace("_", " ").title()
        cuerpo = contenido
        if lineas and lineas[0].startswith("# "):
            titulo = lineas[0][2:].strip()
            cuerpo = "\n".join(lineas[1:]).strip()
        textos.append({
            "num": i,
            "archivo": archivo.name,
            "titulo": titulo,
            "cuerpo": cuerpo,
        })
    return textos


def color_nivel(nivel: str) -> tuple[str, str]:
    colores = {
        "Excelente":    ("#2C5F2E", "white"),
        "Bueno":        ("#4a8c4d", "white"),
        "Regular":      ("#e8a020", "white"),
        "Insuficiente": ("#c0392b", "white"),
    }
    return colores.get(nivel, ("#888", "white"))


def barra_puntaje(puntaje: int):
    porcentaje = puntaje * 10
    color = "#2C5F2E" if puntaje >= 8 else "#4a8c4d" if puntaje >= 6 else "#e8a020" if puntaje >= 4 else "#c0392b"
    st.markdown(f"""
    <div class="barra-contenedor">
      <div class="barra-relleno" style="width:{porcentaje}%; background:{color};"></div>
    </div>
    """, unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 📖 Sentido Global")
    st.markdown("---")
    st.markdown("### ¿Qué es el Sentido Global del Texto?")
    st.markdown(
        "Es la habilidad de **resumir en una sola oración** la idea central de un texto, "
        "capturando su esencia de manera precisa y concisa. No se trata de copiar una frase "
        "del texto, sino de expresar con tus propias palabras de qué trata en su totalidad."
    )
    st.markdown("---")
    st.markdown("### Criterios de evaluación")
    st.markdown("""
- 🎯 **Precisión temática** (3 pts)
- 🌐 **Globalidad** (3 pts)
- ✏️ **Concisión y claridad** (2 pts)
- 📚 **Vocabulario adecuado** (2 pts)
    """)
    st.markdown("---")
    st.markdown("### Consejos")
    st.markdown("""
1. Lee el texto completo antes de escribir.
2. Pregúntate: *¿De qué trata este texto en general?*
3. Escribe una sola oración, no un resumen.
4. Usa tus propias palabras.
    """)


# ── Cuerpo principal ─────────────────────────────────────────────────────────

st.markdown("# Sentido Global del Texto")
st.markdown("Practica la habilidad de captar la idea central de un texto en **una sola oración.**")
st.markdown("---")

# Cargar textos
textos = cargar_textos("TEXTOS")

if not textos:
    st.warning("⚠️ No se encontraron textos. Crea archivos `.md` dentro de la carpeta `TEXTOS/`.")
    st.stop()

# ── Estado: texto seleccionado ────────────────────────────────────────────────
if "texto_idx" not in st.session_state:
    st.session_state.texto_idx = 0

st.markdown("### 📚 Textos disponibles")

# Grid de 3 columnas
filas = [textos[i:i+3] for i in range(0, len(textos), 3)]
for fila in filas:
    cols = st.columns(3)
    for col, t in zip(cols, fila):
        i = t["num"] - 1
        activo = "activo" if i == st.session_state.texto_idx else ""
        with col:
            st.markdown(f"""
            <div class="texto-btn {activo}">
              <div class="num">{t['num']}</div>
              <div class="titulo-btn">{t['titulo']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Seleccionar texto {t['num']}", key=f"btn_texto_{i}",
                         use_container_width=True):
                st.session_state.texto_idx = i
                st.rerun()

# Texto activo
texto_data = textos[st.session_state.texto_idx]

st.markdown("---")
st.markdown(f"### 📄 Texto {texto_data['num']}: {texto_data['titulo']}")
st.markdown(
    f"""<div class="texto-card">{texto_data['cuerpo'].replace(chr(10), '<br>')}</div>""",
    unsafe_allow_html=True
)

st.markdown("---")

# ── Respuesta del estudiante ──────────────────────────────────────────────────
st.markdown("### ✍️ Tu respuesta")
st.markdown(
    "Lee el texto con atención y escribe en **una sola oración** cuál es su idea central. "
    "No copies frases del texto: exprésalo con tus propias palabras."
)

respuesta = st.text_area(
    "Escribe aquí el sentido global del texto:",
    placeholder="El texto trata sobre...",
    height=100,
    max_chars=400,
    key=f"respuesta_{st.session_state.texto_idx}"
)

if respuesta.strip():
    n_palabras = len(respuesta.split())
    color_cont = "#2C5F2E" if 10 <= n_palabras <= 40 else "#e8a020"
    rango_ok = "✓ rango adecuado" if 10 <= n_palabras <= 40 else "— intenta entre 10 y 40 palabras"
    st.markdown(
        f"<span style='font-size:0.85rem; color:{color_cont};'>📊 {n_palabras} palabras {rango_ok}</span>",
        unsafe_allow_html=True
    )

st.markdown("")
col1, col2 = st.columns([2, 1])
with col1:
    evaluar_btn = st.button("🤖 Evaluar mi respuesta", type="primary", use_container_width=True)
with col2:
    limpiar_btn = st.button("🔄 Nuevo intento", use_container_width=True)

if limpiar_btn:
    st.rerun()

# ── Evaluación ───────────────────────────────────────────────────────────────
if evaluar_btn:
    if not respuesta.strip():
        st.warning("✏️ Escribe tu respuesta antes de evaluar.")
    elif len(respuesta.split()) < 5:
        st.warning("Tu respuesta es muy corta. Intenta expresar la idea completa del texto.")
    else:
        with st.spinner("El profesor IA está revisando tu respuesta..."):
            resultado = evaluar_sentido_global(
                texto=texto_data["cuerpo"],
                respuesta_estudiante=respuesta,
                nombre_estudiante=None
            )

        if "error" in resultado:
            st.error(f"❌ {resultado['error']}")
        else:
            st.markdown("---")
            st.markdown("## 📊 Resultado de tu evaluación")

            puntaje = resultado.get("puntaje", 0)
            nivel   = resultado.get("nivel", "—")
            fondo_nivel, texto_nivel = color_nivel(nivel)

            st.markdown(
                f"<span class='puntaje-badge'>{puntaje}/10</span>"
                f"<span class='nivel-badge' style='background:{fondo_nivel}; color:{texto_nivel};'>"
                f"{nivel}</span>",
                unsafe_allow_html=True
            )
            barra_puntaje(puntaje)

            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"""
                <div class="resultado-bloque">
                  <div class="etiqueta">✅ Fortalezas</div>
                  <div class="contenido">{resultado.get('fortalezas', '—')}</div>
                </div>""", unsafe_allow_html=True)
            with col_b:
                st.markdown(f"""
                <div class="resultado-bloque">
                  <div class="etiqueta">📈 Por mejorar</div>
                  <div class="contenido">{resultado.get('aspectos_mejorar', '—')}</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("**💡 Oración ideal para este texto:**")
            st.markdown(f"""
            <div class="ejemplo-ideal">"{resultado.get('ejemplo_ideal', '—')}"</div>
            """, unsafe_allow_html=True)

            st.markdown("**Tu respuesta:**")
            st.markdown(f"""
            <div class="resultado-bloque">
              <div class="contenido" style="font-style:italic;">"{respuesta}"</div>
            </div>""", unsafe_allow_html=True)

            st.markdown(f"""
            <div class="motivador">🌱 {resultado.get('mensaje_motivador', '¡Sigue practicando!')}</div>
            """, unsafe_allow_html=True)
