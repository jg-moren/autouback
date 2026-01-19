import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("--- MODELOS DISPONÍVEIS ---")

try:
    # Vamos apenas imprimir o objeto inteiro ou o nome direto
    for model in client.models.list():
        # Tenta pegar o nome, se não der, imprime o objeto para lermos
        if hasattr(model, 'name'):
            print(f"ID: {model.name}")
        else:
            print(f"Modelo encontrado: {model}")

except Exception as e:
    print(f"Erro fatal: {e}")