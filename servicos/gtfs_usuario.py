from requests import exceptions
from google.protobuf import internal
from modelos import retrato_horario
from modelos.localizacao import Localizacao
import logging
import requests
from google.transit import gtfs_realtime_pb2
from google.protobuf.message import DecodeError #biblioteca para quando o programa tenta ler uma mensagem em binario corrompida


class GtfsUsuario:
    def __init__(self, feed_url: str):
        self.feed_url = feed_url
    
    #tratamento de erro quando o feed do gtfs corrompido nao é tratado
    def _buscar_feed(self) -> gtfs_realtime_pb2.FeedMessage:
        try:
            resposta = requests.get(self.feed_url, timeout=10)
            resposta.raise_for_status()
        except requests.RequestException as erro:
            raise requests.RequestException(
                f"Falha ao buscar feed GTFS em '{self.feed_url}': {erro}"
            ) from erro

        feed = gtfs_realtime_pb2.FeedMessage()
        try:
            feed.ParseFromString(resposta.content)
        except DecodeError as erro:
            raise ValueError(f"Feed GTFS retornado em formato inválido: {erro}") from erro

        return feed

    def buscar_atualizacoes(self) -> list[dict]:
        resposta = requests.get(self.feed_url, timeout=10)
        resposta.raise_for_status()

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(resposta.content)


        #o feed nao manda o horario, so o delay (atraso em segundos) vms usar isso como referencia 
        timestamp_feed = feed.header.timestamp if feed.header.HasField("timestamp") else None

        def _evento(stu_evento, tem_campo):
            #extrai {"time":..., "delay":...} de um StopTimeEvent do GTFS-realtime.
            #'delay' (em segundos) é o próprio atraso informado pela operadora.
            if not tem_campo:
                return None

            tem_time = stu_evento.HasField("time") and stu_evento.time != 0
            tem_delay = stu_evento.HasField("delay")

            #RF7: sem 'time' válido E sem 'delay', não há como saber o
            #horário de jeito nenhum — dado incompleto, descartado aqui.
            if not tem_time and not (tem_delay and timestamp_feed):
                return None

            if tem_time:
                #caso ideal: o feed manda o horário absoluto de verdade.
                return {
                    "time": stu_evento.time,
                    "delay": stu_evento.delay if tem_delay else None,
                }

            #sem 'time', mas com 'delay': usa o timestamp do feed como
            #horário real observado, e o delay é usado depois (em
            #api_oculta.py) pra derivar o horário programado.
            return {
                "time": timestamp_feed,
                "delay": stu_evento.delay,
            }

        atualizacoes = []
        for entidade in feed.entity:
            if entidade.HasField("trip_update"):
                tu = entidade.trip_update
                atualizacoes.append({
                    "trip_update": {
                        "trip": {
                            "trip_id": tu.trip.trip_id,
                            "route_id": tu.trip.route_id,
                        },
                        "stop_time_update": [
                            {
                                "stop_id": stu.stop_id,
                                "departure": _evento(stu.departure, stu.HasField("departure")),
                                "arrival": _evento(stu.arrival, stu.HasField("arrival")),
                            }
                            for stu in tu.stop_time_update
                        ]
                    }
                })

        return atualizacoes
    
    def buscar_posicoes(self) -> dict:
        #rf1 entrega so posicoes vlaidas
        resposta = requests.get(self.feed_url, timeout=10)
        resposta.raise_for_status()

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(resposta.content)

        posicoes = {}
        for entidade in feed.entity:
            if entidade.HasField("vehicle"):
                v = entidade.vehicle
                trip_id = v.trip.trip_id
                try:
                    posicoes[trip_id] = Localizacao(v.position.latitude, v.position.longitude)
                except (ValueError, TypeError) as erro:
                    logging.warning(
                        f"Posição inválida descartada para o veículo '{trip_id}': {erro}"
                    )
                    continue

        return posicoes