import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

from db import obtener_cliente

load_dotenv()

_embeddings = None


def _obtener_embeddings():
    """Crea el modelo de embeddings la primera vez y lo reutiliza."""
    global _embeddings
    if _embeddings is None:
        _embeddings = OpenAIEmbeddings(
            model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        )
    return _embeddings


def buscar_fragmentos(pregunta: str, cantidad: int = 3):
    """Devuelve los fragmentos de apuntes más parecidos a la pregunta."""
    vector = _obtener_embeddings().embed_query(pregunta)
    respuesta = obtener_cliente().rpc(
        "buscar_apuntes",
        {"embedding_consulta": vector, "cantidad": cantidad},
    ).execute()
    return respuesta.data


# Prueba rápida: python -m services.rag_service
if __name__ == "__main__":
    for f in buscar_fragmentos("¿Cómo repito algo varias veces?"):
        print(round(f["similitud"], 3), f["archivo"], "|", f["contenido"][:60])