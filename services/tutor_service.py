import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from services.rag_service import buscar_fragmentos

load_dotenv()

# Fragmentos con menos similitud que esto se descartan (se puede ajustar)
UMBRAL_SIMILITUD = 0.3

# Instrucciones que definen cómo se comporta el tutor
INSTRUCCIONES = """Eres un tutor de programación básica para principiantes.
Solo respondes dudas sobre variables, condicionales, bucles y funciones.
Usa Python en tus ejemplos, explica con palabras sencillas y en español.
Da respuestas cortas, con un ejemplo de código pequeño cuando ayude.
Si la pregunta no trata de esos temas, di amablemente que solo puedes
ayudar con ellos."""

_llm = None


def _obtener_llm():
    """Crea el modelo la primera vez y lo reutiliza después."""
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        )
    return _llm


def _armar_instrucciones(fragmentos):
    """Agrega los apuntes encontrados a las instrucciones del tutor."""
    if not fragmentos:
        return INSTRUCCIONES + (
            "\n\nNo se encontraron apuntes relacionados con esta pregunta. "
            "Si la duda es de los temas permitidos, responde con cuidado y "
            "aclara que no está en los apuntes del curso."
        )

    apuntes = "\n\n".join(f["contenido"] for f in fragmentos)
    return INSTRUCCIONES + (
        "\n\nBasa tu respuesta en estos apuntes del curso:\n\n" + apuntes
    )


def responder_pregunta(pregunta: str) -> str:
    """Busca apuntes, se los pasa al modelo y devuelve la respuesta."""
    encontrados = buscar_fragmentos(pregunta)
    fragmentos = [f for f in encontrados if f["similitud"] >= UMBRAL_SIMILITUD]

    # Se ve en la terminal para entender qué apuntes se usaron
    print("Apuntes usados:", [(f["archivo"], round(f["similitud"], 2)) for f in fragmentos])

    mensajes = [
        SystemMessage(content=_armar_instrucciones(fragmentos)),
        HumanMessage(content=pregunta),
    ]
    return _obtener_llm().invoke(mensajes).content