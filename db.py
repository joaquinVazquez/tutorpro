import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carga las variables del archivo .env
load_dotenv()


def obtener_cliente() -> Client:
    """Crea y devuelve el cliente de Supabase."""
    url = os.getenv("SUPABASE_URL")
    llave = os.getenv("SUPABASE_KEY")

    if not url or not llave:
        raise RuntimeError("Faltan SUPABASE_URL o SUPABASE_KEY en el archivo .env")

    return create_client(url, llave)


# Prueba rápida: se ejecuta solo con "python db.py"
if __name__ == "__main__":
    cliente = obtener_cliente()
    try:
        # Consultamos una tabla que aún no existe, solo para probar la conexión
        cliente.table("tabla_que_no_existe").select("*").limit(1).execute()
        print("Conexión correcta.")
    except Exception as error:
        print("Respuesta de Supabase:", error)