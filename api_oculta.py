from modelos import registro_transportes
from datetime import timedelta
from datetime import datetime
#rf7 - dados incompletos da api
class DadosIncompletosError(ValueError):
    pass

#não sabemos do JSON e nem da API
class Voo: 
    def __init__(self, codigo: str, origem: str, destino: str, horario_programado: datetime, horario_estimado: datetime):
        self.codigo = codigo
        self.origem = origem
        self.destino = destino
        self.horario_programado = horario_programado
        self.horario_estimado = horario_estimado
 
    def __str__(self) -> str:
        hora_formatada = self.horario_estimado.strftime("%H:%M")
        return f"[VOO {self.codigo}] {self.origem} -> {self.destino} - Horário estimado: {hora_formatada}"
    
 
class Onibus:
    def __init__(self, identificador: str, linha: str, origem: str, destino: str, horario_programado: datetime, horario_partida: datetime, horario_chegada: datetime):
        self.identificador = identificador
        self.linha = linha
        self.origem = origem
        self.destino = destino
        self.horario_programado = horario_programado
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
 
            #rf7 sem horário programado não dá pra saber se o voo está atrasado ou não 
            str_programado = info_partida.get("scheduled")
            if not str_programado:
                raise DadosIncompletosError(
                    f"Voo {codigo_voo}: sem horário programado"
                )
            #se a api ainda não tem uma estimativa atualizada vms usar o horário programado
            str_estimado = info_partida.get("estimated") or str_programado
 
            horario_programado_dt = datetime.fromisoformat(str_programado)
            horario_estimado_dt = datetime.fromisoformat(str_estimado)
 
            return Voo(
                codigo=codigo_voo, origem=aero_origem, destino=aero_destino,
                horario_programado=horario_programado_dt, horario_estimado=horario_estimado_dt,
            )
 
        except DadosIncompletosError:
            raise
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
 
            #ef7 dados incompletos caso esteja com paradas vazias
            if not paradas or not paradas[0].get("departure") or not (
                paradas[-1].get("arrival") or paradas[-1].get("departure")
            ):
                raise DadosIncompletosError(
                    f"Ônibus {veiculo}: horário de partida/chegada incompleto"
                )
 
            est_origem = paradas[0]["stop_id"]
            est_destino = paradas[-1]["stop_id"]
 
            tempo_partida = paradas[0]["departure"]["time"]
            partida_dt = datetime.fromtimestamp(tempo_partida)
 
            info_chegada = paradas[-1].get("arrival") or paradas[-1].get("departure")
            tempo_chegada = info_chegada["time"]
            chegada_dt = datetime.fromtimestamp(tempo_chegada)
 
            #o horario programado vem do proprio delay que a operadora informa no feed gtfs
            delay_segundos = info_chegada.get("delay") or 0
            programado_dt = chegada_dt - timedelta(seconds=delay_segundos)
 
            return Onibus(
                identificador=veiculo, linha=nome_linha, origem=est_origem, destino=est_destino,
                horario_programado=programado_dt, horario_partida=partida_dt, horario_chegada=chegada_dt,
            )
        except DadosIncompletosError:
            raise
        except (KeyError, TypeError, ValueError, IndexError) as erro:
            raise ValueError(f"Formato GTFS inválido ou inexistente: {erro}")
 
    @staticmethod
    def criar_trem_gtfs(gtfs_json: dict) -> Trem:
        try:
            info_viagem = gtfs_json["trip_update"]
            veiculo = info_viagem["trip"]["trip_id"]
            nome_linha = info_viagem["trip"]["route_id"]
 
            paradas = info_viagem["stop_time_update"]
 
            if not paradas or not paradas[0].get("departure") or not (
                paradas[-1].get("arrival") or paradas[-1].get("departure")
            ):
                raise DadosIncompletosError(
                    f"Trem {veiculo}: horário de partida/chegada incompleto"
                )
 
            est_origem = paradas[0]["stop_id"]
            est_destino = paradas[-1]["stop_id"]
 
            tempo_partida = paradas[0]["departure"]["time"]
            partida_dt = datetime.fromtimestamp(tempo_partida)
 
            info_chegada = paradas[-1].get("arrival") or paradas[-1].get("departure")
            tempo_chegada = info_chegada["time"]
            chegada_dt = datetime.fromtimestamp(tempo_chegada)
 
            return Trem(identificador=veiculo, linha=nome_linha, origem=est_origem, destino=est_destino, horario_partida=partida_dt, horario_chegada=chegada_dt)
        except DadosIncompletosError:
            raise
        except (KeyError, TypeError, ValueError, IndexError) as erro:
            raise ValueError(f"Formato GTFS inválido ou inexistente: {erro}")