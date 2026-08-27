import requests
import os
from dotenv import load_dotenv

load_dotenv() #abre o .env 

class AviationStack:
    URL = "http://api.aviationstack.com/v1/flights"
    
    def __init__(self, api_key: str = None):
        self.__api_key = api_key or os.environ["AVIATIONSTACK_KEY"] #pega a cgave 

    def buscar_voo(self, iata_code: str) -> dict:
        paramd = {"access_key": self.__api_key, "flight_iata": iata_code}
        resposta = requests.get(self.URL, params=paramd, timeout=10) #vai ate o endereço e pega os dados
        resposta.raise_for_status() #ve se nao deu erro
        dados = resposta.json() #transforma em dicionario

        if not dados["data"]:
            raise ValueError(f"Voo {iata_code} não encontrado") #se nao achar da erro

        return dados["data"][0]
