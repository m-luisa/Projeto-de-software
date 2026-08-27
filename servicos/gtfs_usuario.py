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
                    "trip_id": tu.trip.trip_id,
                    "route_id": tu.trip.route_id,
                    "paradas": [
                        {
                            "stop_id": stu.stop_id,
                            "chegada": stu.arrival.time if stu.HasField("arrival") else None,
                        }
                        for stu in tu.stop_time_update
                    ]
                })

        return atualizacoes