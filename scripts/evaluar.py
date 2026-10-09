from services.rag_service import buscar_fragmentos
from services.tutor_service import responder_pregunta, UMBRAL_SIMILITUD

# Cada caso: pregunta, archivo que debería encontrarse (None si es ajena
# al curso) y palabras de las que la respuesta debe incluir al menos una.
CASOS = [
    ("¿Qué es una variable?", "variables.md", ["valor", "nombre"]),
    ("¿Cómo sé de qué tipo es una variable?", "variables.md", ["type("]),
    ("¿Qué diferencia hay entre = y ==?", "condicionales.md", ["==", "compar"]),
    ("¿Para qué sirve elif?", "condicionales.md", ["elif"]),
    ("¿Cómo uso and y or en una condición?", "condicionales.md", ["and", "or"]),
    ("¿Cómo repito algo varias veces?", "bucles.md", ["for", "while"]),
    ("¿Qué es un bucle infinito?", "bucles.md", ["infinito"]),
    ("¿Para qué sirve break?", "bucles.md", ["break"]),
    ("¿Qué diferencia hay entre print y return?", "funciones.md", ["return"]),
    ("¿Cómo le pongo un valor por defecto a un parámetro?", "funciones.md", ["defecto"]),
    # Preguntas ajenas: el tutor debe decir que solo ayuda con los 4 temas
    ("¿Quién ganó el mundial de 2022?", None, ["solo", "sólo"]),
    ("Dame una receta de pozole", None, ["solo", "sólo"]),
]


def evaluar_busqueda(pregunta, archivo_esperado):
    """Revisa si la búsqueda trae el archivo correcto. Devuelve (ok, detalle)."""
    fragmentos = buscar_fragmentos(pregunta)
    archivos = [f["archivo"] for f in fragmentos]

    if archivo_esperado is None:
        # Pregunta ajena: ningún fragmento debería superar el umbral
        pasan = [f for f in fragmentos if f["similitud"] >= UMBRAL_SIMILITUD]
        return len(pasan) == 0, f"{len(pasan)} fragmentos sobre el umbral"

    ok = bool(archivos) and archivos[0] == archivo_esperado
    return ok, f"primero: {archivos[0] if archivos else 'nada'}"


def evaluar_respuesta(pregunta, palabras):
    """Revisa si la respuesta contiene alguna palabra esperada."""
    respuesta = responder_pregunta(pregunta).lower()
    ok = any(p.lower() in respuesta for p in palabras)
    return ok, respuesta


def main():
    aciertos_busqueda = 0
    aciertos_respuesta = 0
    fallos = []

    for pregunta, archivo, palabras in CASOS:
        try:
            ok_b, detalle_b = evaluar_busqueda(pregunta, archivo)
            ok_r, respuesta = evaluar_respuesta(pregunta, palabras)
        except Exception as e:
            print(f"ERROR  {pregunta} -> {e}")
            fallos.append((pregunta, f"Error: {e}"))
            continue

        aciertos_busqueda += ok_b
        aciertos_respuesta += ok_r
        print(f"busqueda={'OK ' if ok_b else 'MAL'} respuesta={'OK ' if ok_r else 'MAL'} | {pregunta}")

        if not ok_b or not ok_r:
            fallos.append((pregunta, f"{detalle_b} | respuesta: {respuesta[:200]}"))

    total = len(CASOS)
    print("\n--- Resumen ---")
    print(f"Búsqueda correcta: {aciertos_busqueda}/{total}")
    print(f"Respuesta correcta: {aciertos_respuesta}/{total}")

    if fallos:
        print("\n--- Casos a revisar ---")
        for pregunta, detalle in fallos:
            print(f"* {pregunta}\n  {detalle}")


if __name__ == "__main__":
    main()