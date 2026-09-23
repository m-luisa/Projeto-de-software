from copy import error
import requests
import os
from dotenv import load_dotenv

load_dotenv() #abre o .env 

"""
rf5 - cliente http da api

essa classe eu cuida apenas do transporte http, devolve o json quase bruto mas gaarante que a resposta é valida
"""

class AviationStack:
    URL = "http://api.aviationstack.com/v1/flights"
    
    def __init__(self, api_key: str = None):
        #encapsulamento: a chave da api é guardada em atributo privado, inacessível fora da classe
        try:#tratamento de erro
            self.__api_key = api_key or os.environ["AVIATIONSTACK_KEY"]
        except KeyError as erro:
            raise KeyError(
            "Variável de 'AVIATIONSTACK_KEY' não encontrada. "
            "Defina-a no arquivo .env."
            ) from erro

    def buscar_voo(self, iata_code: str) -> dict:
        paramd = {"access_key": self.__api_key, "flight_iata": iata_code}
        try:#tratamento de erro
            resposta = requests.get(self.URL, params=paramd, timeout=10)
            resposta.raise_for_status()
            dados = resposta.json()
        except requests.RequestsException as erro:
            raise requests.RequestException(f"Resposta de AviationStack é um JSON inválido: {erro}") from erro
    
        #tratamento de erro  - respostaa com json valido porem com formato inesperado
        try:
            if not dados["data"]:
                raise ValueError(f"Voo {iata_code} não encontrado")
            return dados["data"][0]
        except KeyError as erro:
            raise KeyError(f"Resposta da AviationStack em formato inesperado: {erro}") from erro

    def buscar_voos(self, dep_iata: str = None, quantidade: int = 10) -> list[dict]:
    #rf5 - devolve uma lista de dicionarios ainda no formato da aviationstack, a api_oculta quem vai transformar cada um em um objeto de dominio voo
        paramd = {"access_key": self.__api_key, "limit": quantidade}
        if dep_iata:
            paramd["dep_iata"] = dep_iata
        try:
            resposta = requests.get(self.URL, params=paramd, timeout=10)
            resposta.raise_for_status()
            dados = resposta.json()
        except requests.RequestException as erro:
            raise requests.RequestException(f"Resposta de AviationStack é um JSON inválido: {erro}") from erro

        try:
            return dados["data"] or []
        except KeyError as erro:
            raise KeyError(f"Resposta da AviationStack em formato inesperado: {erro}") from erro