import requests
import os
from dotenv import load_dotenv

load_dotenv()

params = {"access_key": os.environ["AVIATIONSTACK_KEY"], "limit": 5}
resposta = requests.get("http://api.aviationstack.com/v1/flights", params=params, timeout=10)
resposta.raise_for_status()
dados = resposta.json()

for voo in dados["data"]:
    print(voo["flight"]["iata"], "-", voo["airline"]["name"])