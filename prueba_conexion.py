import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from supabase import create_client

# 1. Cargar las variables del archivo .env
load_dotenv()

# 2. Verificar que cada variable tenga valor (sin mostrar la llave)
variables = ["OPENAI_API_KEY", "OPENAI_MODEL", "SUPABASE_URL", "SUPABASE_KEY", "FLASK_SECRET_KEY"]
for nombre in variables:
    estado = "OK" if os.getenv(nombre) else "FALTA"
    print(f"{nombre}: {estado}")

# 3. Probar OpenAI
llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
respuesta = llm.invoke("Responde solo con la palabra: listo")
print("OpenAI respondió:", respuesta.content)

# 4. Crear el cliente de Supabase
cliente = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
print("Cliente de Supabase creado")
