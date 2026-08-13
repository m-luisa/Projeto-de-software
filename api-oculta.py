from datetime import datetime
# não sabemos do JSON e nem da API
class Voo: 
    def __init__(self, codigo: str, origem: str, destino: str, horario_estimado: datetime):
        self.codigo = codigo
        self.origem = origem
        self.destino = destino
        self.horario_estimado = horario_estimado

    def __str__(self) -> str:
        hora_formatada = self.horario_estimado.strftime("%H:%M")
        return f"[VOO {self.codigo}] {self.origem} -> {self.destino} - Horário estimado: {hora_formatada}"
    

class Onibus:
    def __init__(self, identificador: str, linha: str, origem: str, destino: str, horario_partida: datetime, horario_chegada: datetime):
        self.identificador = identificador
        self.linha = linha
        self.origem = origem
        self.destino = destino
        self.horario_partida = horario_partida
        self.horario_chegada = horario_chegada

    def __str__(self) -> str:
        partida = self.horario_partida.strftime("%H:%M")
        chegada = self.horario_chegada.strftime("%H:%M")
        return f"[ÔNIBUS linha {self.linha}] ID: {self.identificador} {self.origem} ({partida}) -> {self.destino} ({chegada})"


class Trem:
    def __init__(self, identificador: str, linha: str, origem: str, destino: str, horario_partida: datetime, horario_chegada: datetime):
        self.identificador = identificador
        self.linha = linha
        self.origem = origem
        self.destino = destino
        self.horario_partida = horario_partida
        self.horario_chegada = horario_chegada

    def __str__(self) -> str:
        partida = self.horario_partida.strftime("%H:%M")
        chegada = self.horario_chegada.strftime("%H:%M")
        return f"[TREM linha {self.linha}] ID: {self.identificador} {self.origem} ({partida}) -> {self.destino} ({chegada})"

#aqui,nós vms passar pelas APIs e o JSON vai passar aqui 
class AviationStackService: # nome da api, p facilitar
    @staticmethod # p nn precisar instanciar a classe
    def criar_voo_json(json_sem_tratar: dict) -> Voo:
        try:
            codigo_voo = json_sem_tratar["flight"]["iata"] 
            aero_origem = json_sem_tratar["departure"]["airport"] 
            aero_destino = json_sem_tratar["arrival"]["airport"] 
            info_partida = json_sem_tratar["departure"]
            str_horario = info_partida.get("estimated") or info_partida["scheduled"]
            horario_datetime = datetime.fromisoformat(str_horario) 

            return Voo(codigo=codigo_voo, origem=aero_origem, destino=aero_destino, horario_estimado=horario_datetime)

        except (KeyError, TypeError, ValueError) as erro:
            raise ValueError(f"Formato JSON inválido ou inexistente: {erro}")


class GtfsService:
    @staticmethod 
    def criar_onibus_gtfs(gtfs_json: dict) -> Onibus:
        try:
            info_viagem = gtfs_json["trip_update"]
            veiculo = info_viagem["trip"]["trip_id"]
            nome_linha = info_viagem["trip"]["route_id"]

            paradas = info_viagem["stop_time_update"]
            est_origem = paradas[0]["stop_id"]
            est_destino = paradas[-1]["stop_id"]

            tempo_partida = paradas[0]["departure"]["time"]
            partida_dt = datetime.fromtimestamp(tempo_partida)

            info_chegada = paradas[-1].get("arrival") or paradas[-1].get("departure")
            tempo_chegada = info_chegada["time"]
            chegada_dt = datetime.fromtimestamp(tempo_chegada)

            return Onibus(identificador=veiculo, linha=nome_linha, origem=est_origem, destino=est_destino, horario_partida=partida_dt, horario_chegada=chegada_dt)
        except (KeyError, TypeError, ValueError, IndexError) as erro:
            raise ValueError(f"Formato GTFS inválido ou inexistente: {erro}")

    @staticmethod
    def criar_trem_gtfs(gtfs_json: dict) -> Trem:
        try:
            info_viagem = gtfs_json["trip_update"]
            veiculo = info_viagem["trip"]["trip_id"]
            nome_linha = info_viagem["trip"]["route_id"]

            paradas = info_viagem["stop_time_update"]
            est_origem = paradas[0]["stop_id"]
            est_destino = paradas[-1]["stop_id"]

            tempo_partida = paradas[0]["departure"]["time"]
            partida_dt = datetime.fromtimestamp(tempo_partida)

            info_chegada = paradas[-1].get("arrival") or paradas[-1].get("departure")
            tempo_chegada = info_chegada["time"]
            chegada_dt = datetime.fromtimestamp(tempo_chegada)

            return Trem(identificador=veiculo, linha=nome_linha, origem=est_origem, destino=est_destino, horario_partida=partida_dt, horario_chegada=chegada_dt)
        except (KeyError, TypeError, ValueError, IndexError) as erro:
            raise ValueError(f"Formato GTFS inválido ou inexistente: {erro}")

if __name__ == "__main__": #aqui a gnt vai printar os resultados dos voos, trens e onibus
    agora_timestamp = int(datetime.now().timestamp())
    
    json_voo = {
        "flight": {"iata": "AB1234"},
        "departure": {"airport": "Aeroporto A", "estimated": "2026-08-12T13:00:00", "scheduled": "2026-08-12T12:50:00"},
        "arrival": {"airport": "Aeroporto B"},
    }

    meu_voo = AviationStackService.criar_voo_json(json_voo)
    print(f"Voo: {meu_voo}\n")

    json_onibus = {
        "trip_update": {
            "trip": {"trip_id": "BUS-001", "route_id": "001 - A/Z"},
            "stop_time_update": [
                {"stop_id": "Estação A", "departure": {"time": agora_timestamp}},
                {"stop_id": "Estação B", "arrival": {"time": agora_timestamp + 3600}}
            ]
        }
    }
    meu_onibus = GtfsService.criar_onibus_gtfs(json_onibus)
    print(f"Onibus: {meu_onibus}\n")

    json_trem = {
        "trip_update": {
            "trip": {"trip_id": "TRM-01", "route_id": "VLT - Linha 001"},
            "stop_time_update": [
                {"stop_id": "Estação A", "departure": {"time": agora_timestamp}},
                {"stop_id": "Estação B", "arrival": {"time": agora_timestamp + 3600}}
            ]
        }
    }
    meu_trem = GtfsService.criar_trem_gtfs(json_trem)
    print(f"Trem: {meu_trem}\n")
