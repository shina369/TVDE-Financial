import requests

# URL correta do serviço FastAPI
url = "https://tvde-financial-production.up.railway.app/upgrade"

# Dados de teste
data = {
    "email": "flavioalmeidamata@gmail.com",  # seu email cadastrado
    "purchaseToken": "serverVerificationData"        # substitua pelo token real do Flutter
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print("Resposta do backend:", response.json())
except Exception as e:
    print("Erro ao chamar o backend:", e)
