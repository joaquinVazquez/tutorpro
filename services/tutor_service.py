import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

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
        # Sin "temperature": algunos modelos solo aceptan el valor por defecto
        _llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        )
    return _llm


def responder_pregunta(pregunta: str) -> str:
    """Envía la pregunta al modelo y devuelve el texto de la respuesta."""
    mensajes = [
        SystemMessage(content=INSTRUCCIONES),
        HumanMessage(content=pregunta),
    ]
    return _obtener_llm().invoke(mensajes).content