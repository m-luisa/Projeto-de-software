from datetime import datetime, timedelta

#Requisito 1
class Localizacao:
    def __init__(self, latitude: float, longitude: float, nome_local: str = ""):
        self.nome_local = nome_local
        self.latitude = latitude
        self.longitude = longitude

    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, valor: float):
        if valor < -90.0 or valor > 90.0:
            raise ValueError(f"Latitude inválida: {valor}")
        self._latitude = valor

    @property
    def longitude(self) -> float:
        return self._longitude

    @longitude.setter
    def longitude(self, valor: float):
        if valor < -180.0 or valor > 180.0:
            raise ValueError(f"Longitude inválida: {valor}")
        self._longitude = valor   

#Requisito 2 e 3
class SnapshotTrecho:
    def __init__(self, id_trecho: str, programado: datetime, estimado: datetime, captura: datetime, localizacao: Localizacao = None):
        self._id_trecho = id_trecho
        self._programado = programado
        self._estimado = estimado
        self._timestamp_captura = captura 
        self._localizacao = localizacao

    @property
    def id_trecho(self): 
        return self._id_trecho

    @property
    def programado(self): 
        return self._programado
    
    @property
    def estimado(self): 
        return self._estimado
    
    @property
    def timestamp_captura(self): 
        return self._timestamp_captura

    @property
    def localizacao(self): 
        return self._localizacao
    
    def calcular_atraso_minutos(self) -> float:
        diferenca = self._estimado - self._programado
        minutos = diferenca.total_seconds() / 60.0
        if minutos < 0:
            return 0.0
        return minutos

    def esta_atrasado(self) -> bool:
        return False


class VooSnapshot(SnapshotTrecho):
    def esta_atrasado(self) -> bool:
        return self.calcular_atraso_minutos() >= 15.0


class OnibusSnapshot(SnapshotTrecho):
    def esta_atrasado(self) -> bool:
        return self.calcular_atraso_minutos() >= 10.0


class TremSnapshot(SnapshotTrecho):
    def __init__(self, id_trecho: str, programado: datetime, estimado: datetime, captura: datetime, status_operadora: str, localizacao: Localizacao = None):
        super().__init__(id_trecho, programado, estimado, captura, localizacao)
        self.status_operadora = status_operadora

    def esta_atrasado(self) -> bool:
        if self.status_operadora.upper() == "ATRASADO":
            return True
        return self.calcular_atraso_minutos() >= 5.0


class Viagem:
    def __init__(self, id_viagem: str, trechos: list):
        self.id_viagem = id_viagem
        self.trechos = trechos

    def calcular_chegada_final(self) -> datetime:
        if not self.trechos:
            return datetime.now()

        horario_final = self.trechos[-1].estimado
        atraso_total = timedelta()

        for trecho in self.trechos:
            if trecho.esta_atrasado():
                minutos = trecho.calcular_atraso_minutos()
                atraso_total += timedelta(minutes=minutos)

        return horario_final + atraso_total

    def exibir_painel(self):
        print(f"\n  PAINEL DA VIAGEM: {self.id_viagem}")
        for t in self.trechos:
            status = "ATRASADO" if t.esta_atrasado() else "NO HORÁRIO"
            print(f"Trecho {t.id_trecho} - Status: {status}")

        chegada_recalculada = self.calcular_chegada_final()
        print(f"Chegada final prevista: {chegada_recalculada.strftime('%d/%m/%Y %H:%M')}")