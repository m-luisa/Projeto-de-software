import requests
from datetime import datetime
from core import VooSnapshot, Localizacao

class AviationStackClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "http://api.aviationstack.com/v1/flights"

    def buscar_voo(self, codigo_voo: str):
        parametros ={
            'access_key': self.api_key,
            'flight_iata': codigo_voo
        }
        
        try:
            resposta = requests.get(self.url, params=parametros, timeout=5)
            dados_json = resposta.json()
            
            voos = dados_json.get('data', [])
                
            if not voos:
                print(f"Voo {codigo_voo} não encontrado na API.")
                return None
            voo_info = voos[0]
            
            texto_programado = voo_info['departure']['scheduled']
            programado = datetime.fromisoformat(texto_programado)
            
            texto_estimado = voo_info['departure'].get('estimated') or texto_programado
            estimado = datetime.fromisoformat(texto_estimado)

            localizacao_objeto = None
            if voo_info.get('live'):
                lat = voo_info['live']['latitude']
                lon = voo_info['live']['longitude']
                localizacao_objeto = Localizacao(latitude=lat, longitude=lon, nome_local="Em trânsito")

            return VooSnapshot(
                id_trecho=codigo_voo,
                programado=programado,
                estimado=estimado,
                captura=datetime.now(),
                localizacao=localizacao_objeto
            )

        except Exception as erro:
            print(f"Aviso: Não foi possível conectar à API do AviationStack. Erro: {erro}")
            return None