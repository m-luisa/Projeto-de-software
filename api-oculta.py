# primeiro a gnt vai criar uma classe de domínio q vai guardar os dados de fato essenciais ao sistema
from datetime import datetime

class Voo: #nn sabemos da JSON e nem da API
    def __init__(self, codigo: str, origem: str, destino: str, horario_estimado: datetime):
        self.codigo = codigo
        self.origem = origem
        self.destino = destino
        self.horario_estimado = horario_estimado

    def __str__(self) -> str:
        hora_formatada = self.horario_estimado.strftime("%H:%M")
        return f"[VOO {self.codigo}] {self.origem} -> {self.destino} - Horário estimado: {hora_formatada}"
    
# vms ver a criação da camada da api oculta -> a gnt vai encapsular tudo e navegar pelo dicionario associado a api oculta e vms criar uma classe q vai saber lidar c o dicionário da api externa

class AviationStackService: # nome da api, p facilitar
    @staticmethod # p nn precisar instanciar a classe
    def criar_voo_json(json_sem_tratar: dict) -> Voo: # o parametro json vai vir bruto, sem tratamento e esse dict quer dzr q é parte do dicionario
        try: #tentar executar esses dados do json
            codigo_voo = json_sem_tratar["flight"]["iata"] 
            aero_origem = json_sem_tratar["departure"]["airport"] 
            aero_destino = json_sem_tratar["arrival"]["airport"] 
            info_partida = json_sem_tratar["departure"]
            str_horario = info_partida.get("estimated") or info_partida["scheduled"]
            horario_datetime = datetime.fromisoformat(str_horario) 

            return Voo(codigo=codigo_voo, origem=aero_origem, destino=aero_destino, horario_estimado=horario_datetime) #retorna o voo criado

        except (KeyError, TypeError, ValueError) as erro:
            raise ValueError(f"Formato JSON inválido ou inexistente: {erro}")


if __name__ == "__main__": # aqui vms fzr um teste
    json_teste_api = { # criando um dicionario do jeito q a API mandaria
        "flight": {"iata": "AB1234"},
        "departure": {"airport": "Aeroporto A", "estimated": "2026-08-12T13:00:00", "scheduled": "2026-08-12T12:50:00"},
        "arrival": {"airport": "Aeroporto B"},
    }

    #print("=== TESTANDO REQUISITO 5 ===")

    meu_voo_teste = AviationStackService.criar_voo_json(json_teste_api) #testa criar um voo limpo

    print(meu_voo_teste)
    #print(f"\nCódigo isolado: {meu_voo_teste.codigo}")
    #print(f"Destino isolado: {meu_voo_teste.destino}")
