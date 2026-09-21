from modelos import registro_transportes
from datetime import timedelta
from datetime import datetime
import logging

"""
rf5: reconhece o formato de resposta de aviationstack e do feed gtfs-realtime, vai receber os dados brutos e devolver objetos de domínio simples
"""

#rf7 - dados incompletos da api
class DadosIncompletosError(ValueError):
    pass

#estruturaa de dominio cruas dessa camada - ainda nao sao objetos finais, mas ja escondem o json
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
    #rf3 - a api trilhos informa o status por linha, então "identificador" aqui é o código da linha
    def __init__(self, identificador: str, linha: str, empresa: str, origem: str, destino: str, status_operadora: str, operacao_normal: bool, atualizado_em: datetime):
        self.identificador = identificador
        self.linha = linha
        self.empresa = empresa
        self.origem = origem
        self.destino = destino
        self.status_operadora = status_operadora
        self.operacao_normal = operacao_normal
        self.atualizado_em = atualizado_em
 
    def __str__(self) -> str:
        momento = self.atualizado_em.strftime("%H:%M")
        return f"[TREM {self.linha}] ({self.empresa}) {self.origem} -> {self.destino}: {self.status_operadora} (atualizado {momento})"
 
#rf5 - toda a estrutura do json de aviationstack fica nessa classe, que devolve apenas o abjeto de dominio voo, ja limpo
class AviationStackService: 
    @staticmethod # métpdp estático não precisa instanciar a classe
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
            #se a api ainda não tem uma estimativa atualizada usa o horário programado
            str_estimado = info_partida.get("estimated") or str_programado
 
            horario_programado_dt = datetime.fromisoformat(str_programado)
            horario_estimado_dt = datetime.fromisoformat(str_estimado)
 
            return Voo(
                codigo=codigo_voo, origem=aero_origem, destino=aero_destino,
                horario_programado=horario_programado_dt, horario_estimado=horario_estimado_dt,
            )
        #tratamento de erro
        except DadosIncompletosError:
            raise
        except (KeyError, TypeError, ValueError) as erro:
            raise ValueError(f"Formato JSON inválido ou inexistente: {erro}")
 
#rf5 - mesmo painel de isolamento para o feed gtfs-realtime: quem usa o gtfsservice so recebe onibus trem no formato de dominio, nao no dicionario bruto
class GtfsService:
    @staticmethod 
    def criar_onibus_gtfs(gtfs_json: dict) -> Onibus:
        try:
            info_viagem = gtfs_json["trip_update"]
            veiculo = info_viagem["trip"]["trip_id"]
            nome_linha = info_viagem["trip"]["route_id"]
 
            paradas = info_viagem["stop_time_update"]
 
            #rf7 dados incompletos caso esteja com paradas vazias
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
 
            #o horario programado vem do proprio delay que a operadora informa no feed gtfs, ja que ele nao manda o horario programado diretamente
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
 


"""
pequenas tabelas de referência estáticas - a página raspada só dá número, nome e situação da linha; operador e estações extremas são metadados praticamente fixos, então preenchemos por uma tabela local em vez de depender da página pra isso
"""
OPERADORA_POR_LINHA = {
    "1": "Metrô", "2": "Metrô", "3": "Metrô", "15": "Metrô",
    "4": "ViaQuatro", "5": "ViaMobilidade", "8": "ViaMobilidade", "9": "ViaMobilidade",
    "7": "TIC Trens", "10": "CPTM", "11": "CPTM", "12": "CPTM", "13": "CPTM",
}
TERMINAIS_POR_LINHA = {
    "1": ("Jabaquara", "Tucuruvi"),
    "2": ("Vila Prudente", "Vila Madalena"),
    "3": ("Palmeiras-Barra Funda", "Corinthians-Itaquera"),
    "4": ("Vila Sônia", "Luz"),
    "5": ("Capão Redondo", "Chácara Klabin"),
    "15": ("Vila Prudente", "Jardim Colonial"),
}
 
 
#rf5- o html bruto da página do Metrô-SP nunca aparece fora dessa camada, o restante do sistema só enxerga objetos Trem já limpos.
class MetroSPService:
    @staticmethod
    def criar_trens_json(linhas_raspadas: list) -> list[Trem]:
        #recebe a lista de dicts já extraída pelo MetroSPScraper e devolve só os trens que puderam ser montados; entradas com dados incompletos são descartadas e avisadas pela rf7
        trens = []
        for linha_raspada in linhas_raspadas:
            try:
                trens.append(MetroSPService._montar_trem(linha_raspada))
            except DadosIncompletosError as erro:
                logging.warning(str(erro))
                continue
            except (KeyError, TypeError, ValueError) as erro:
                logging.warning(f"Formato da página do Metrô-SP inválido: {erro}")
                continue
        return trens
 
    @staticmethod
    def _montar_trem(linha_raspada: dict) -> Trem:
        try:
            codigo_linha = linha_raspada["numero"]
            nome_linha = linha_raspada.get("nome") or f"Linha {codigo_linha}"
 
            #rf7 sem a situação informada não dá pra saber se está atrasado ou não
            situacao = linha_raspada.get("situacao")
            if not situacao:
                raise DadosIncompletosError(f"Linha {nome_linha}: sem situação informada")
 
            #quando esta tudo certo, a palavra que usamos é "normal"
            operacao_normal = "normal" in situacao.lower()
 
            empresa = OPERADORA_POR_LINHA.get(codigo_linha, "Operadora desconhecida")
            origem, destino = TERMINAIS_POR_LINHA.get(codigo_linha, (nome_linha, nome_linha))
 
            return Trem(
                identificador=codigo_linha, linha=nome_linha, empresa=empresa,
                origem=origem, destino=destino,
                status_operadora=situacao, operacao_normal=operacao_normal,
                atualizado_em=datetime.now(),#a página não expõe o horário da operadora
            )
        except DadosIncompletosError:
            raise
        except (KeyError, TypeError, ValueError) as erro:
            raise ValueError(f"Formato da página do Metrô-SP inválido: {erro}")