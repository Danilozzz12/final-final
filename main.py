
import os
import requests
from requests.auth import HTTPBasicAuth

from keep_alive import keep_alive

PINNACLE_USERNAME = os.getenv("danilocarreira05@gmail.com")
PINNACLE_PASSWORD = os.getenv("PN11pn12")

def test_pinnacle_api():
    url = "https://api.pinnacle.com/v1/sports"
    response = requests.get(url, auth=HTTPBasicAuth(PINNACLE_USERNAME, PINNACLE_PASSWORD))
    if response.status_code == 200:
        print("✅ Conexão bem-sucedida com a API da Pinnacle")
        print(response.json())
    else:
        print("❌ Erro na conexão:", response.status_code, response.text)

if __name__ == "__main__":
    keep_alive()
    test_pinnacle_api()
