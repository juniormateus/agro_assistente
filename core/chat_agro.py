import requests
import time
from fastapi import Request

API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_TOKEN = "GROK_API" 

# Controle de chamadas por IP: armazena timestamps das chamadas recentes
calls_by_ip = {}

LIMIT_CALLS_PER_MINUTE = 50
WINDOW_SECONDS = 108000

def pode_fazer_chamada(ip: str) -> bool:
    agora = time.time()
    chamadas = calls_by_ip.get(ip, [])
    chamadas = [ts for ts in chamadas if agora - ts < WINDOW_SECONDS]
    if len(chamadas) >= LIMIT_CALLS_PER_MINUTE:
        return False
    chamadas.append(agora)
    calls_by_ip[ip] = chamadas
    return True

def perguntar_agronomo(pergunta_usuario: str, ip: str) -> str:
    if not pode_fazer_chamada(ip):
        return "Você atingiu o limite de perguntas por minuto. Por favor, aguarde alguns instantes antes de tentar novamente."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}",
    }
    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Você é um ai agronomica experiente em agricultura brasileira, "
                    "responda as dúvidas de produtores rurais de forma clara e prática."
                )
            },
            {
                "role": "user",
                "content": pergunta_usuario
            }
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        return f"Erro {response.status_code}: {response.text}"
