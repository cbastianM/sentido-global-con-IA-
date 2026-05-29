import json
import re
import requests
import streamlit as st
from typing import Optional

DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"
DEEPSEEK_MODEL = "deepseek-v4-flash"

SYSTEM_PROMPT = """Eres un profesor experto en comprensión lectora y habilidades comunicativas.
Tu tarea es evaluar la habilidad llamada SENTIDO GLOBAL DEL TEXTO de un estudiante.

El SENTIDO GLOBAL DEL TEXTO consiste en resumir en UNA SOLA frase u oración la idea central de un texto,
captando su esencia de manera precisa, coherente y concisa.

Criterios de evaluación:
1. **Precisión temática** (0-3 pts): ¿La frase refleja correctamente el tema central del texto?
2. **Globalidad** (0-3 pts): ¿Captura la idea global y no solo un detalle o idea secundaria?
3. **Concisión y claridad** (0-2 pts): ¿Está expresada en una sola oración clara y bien redactada?
4. **Vocabulario adecuado** (0-2 pts): ¿Usa palabras apropiadas al texto leído?

Total: 10 puntos.

Responde ÚNICAMENTE con un JSON válido, sin markdown, sin backticks, sin texto antes ni después:
{"puntaje": 7, "nivel": "Bueno", "fortalezas": "...", "aspectos_mejorar": "...", "ejemplo_ideal": "...", "mensaje_motivador": "..."}"""


def _extraer_json(texto: str) -> dict:
    """Extrae JSON de la respuesta, limpiando markdown si es necesario."""
    # Limpiar backticks de markdown
    limpio = re.sub(r"```(?:json)?\s*", "", texto).strip()
    limpio = limpio.rstrip("`").strip()

    # Intentar parsear directo
    try:
        return json.loads(limpio)
    except json.JSONDecodeError:
        pass

    # Buscar el primer { ... } en el texto
    match = re.search(r"\{.*\}", limpio, re.DOTALL)
    if match:
        return json.loads(match.group())

    raise ValueError(f"No se pudo extraer JSON de la respuesta: {texto[:200]}")


def evaluar_sentido_global(
    texto: str,
    respuesta_estudiante: str,
    nombre_estudiante: Optional[str] = None
) -> dict:
    nombre = nombre_estudiante or "el estudiante"

    user_message = f"""TEXTO LEÍDO:
---
{texto}
---

SENTIDO GLOBAL ESCRITO POR {nombre.upper()}:
"{respuesta_estudiante}"

Evalúa la respuesta según los criterios establecidos. Responde SOLO con el JSON, nada más."""

    headers = {
        "Authorization": f"Bearer {st.secrets['DEEPSEEK_API_KEY']}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.3,
        "max_tokens": 600
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return _extraer_json(content)

    except requests.exceptions.Timeout:
        return {"error": "La evaluación tardó demasiado. Intenta de nuevo."}
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            return {"error": "API Key inválida. Verifica tu clave en secrets.toml."}
        return {"error": f"Error del servidor: {e.response.status_code}"}
    except Exception as e:
        return {"error": f"Error inesperado: {str(e)}"}
