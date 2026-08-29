import requests
from google.transit import gtfs_realtime_pb2


class GtfsUsuario:
    def __init__(self, feed_url: str):
        self.feed_url = feed_url

    def buscar_atualizacoes(self) -> list[dict]:
        resposta = requests.get(self.feed_url, timeout=10)
        resposta.raise_for_status()

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(resposta.content)

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
                                "departure": {"time": stu.departure.time} if stu.HasField("departure") else None,
                                "arrival": {"time": stu.arrival.time} if stu.HasField("arrival") else None,
                            }
                            for stu in tu.stop_time_update
                        ]
                    }
                })

        return atualizacoes
    
    def buscar_posicoes(self) -> dict:
        resposta = requests.get(self.feed_url, timeout=10)
        resposta.raise_for_status()

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(resposta.content)

        posicoes = {}
        for entidade in feed.entity:
            if entidade.HasField("vehicle"):
                v = entidade.vehicle
                posicoes[v.trip.trip_id] = (v.position.latitude, v.position.longitude)

        return posicoes
