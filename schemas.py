# Validación sencilla de lo que llega desde el navegador
MAX_CARACTERES = 500


def validar_pregunta(datos):
    """Devuelve (pregunta, error). Si todo está bien, error es None."""
    if not isinstance(datos, dict):
        return None, "El cuerpo de la petición debe ser JSON."

    pregunta = (datos.get("pregunta") or "").strip()

    if not pregunta:
        return None, "Escribe una pregunta."
    if len(pregunta) > MAX_CARACTERES:
        return None, f"La pregunta no puede pasar de {MAX_CARACTERES} caracteres."

    return pregunta, None