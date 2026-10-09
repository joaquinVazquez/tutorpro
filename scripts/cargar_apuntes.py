import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

from db import obtener_cliente

load_dotenv()

CARPETA_APUNTES = Path("apuntes")


def dividir_en_fragmentos(texto):
    """Separa un apunte en fragmentos; cada título '## ' inicia uno nuevo."""
    fragmentos = []
    for parte in texto.split("## "):
        parte = parte.strip()
        if parte:
            fragmentos.append("## " + parte)
    return fragmentos


def main():
    cliente = obtener_cliente()
    embeddings = OpenAIEmbeddings(
        model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    )

    # Juntamos todos los fragmentos de todos los archivos .md
    filas = []
    for ruta in sorted(CARPETA_APUNTES.glob("*.md")):
        texto = ruta.read_text(encoding="utf-8")
        for fragmento in dividir_en_fragmentos(texto):
            filas.append({"archivo": ruta.name, "contenido": fragmento})

    if not filas:
        print("No encontré archivos .md en la carpeta apuntes/")
        return

    # Un solo llamado a OpenAI para convertir todo a vectores
    vectores = embeddings.embed_documents([f["contenido"] for f in filas])
    for fila, vector in zip(filas, vectores):
        fila["embedding"] = vector

    # Limpiamos la tabla para no duplicar si corres el script varias veces
    cliente.table("apuntes").delete().neq("id", 0).execute()
    cliente.table("apuntes").insert(filas).execute()

    print(f"Se cargaron {len(filas)} fragmentos.")


if __name__ == "__main__":
    main()