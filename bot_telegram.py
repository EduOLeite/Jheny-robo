import os
import requests
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_mensagem(texto):
    """Envia uma mensagem de texto simples para o grupo do Telegram."""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown"
    }
    resposta = requests.post(url, json=payload)
    return resposta.json()

if __name__ == "__main__":
    print("Enviando mensagem de teste para o Telegram...")
    resultado = enviar_mensagem("🚀 *Robô Jheny Achadinhos conectado com sucesso!*")
    print(resultado)