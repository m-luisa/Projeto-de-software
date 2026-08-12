from datetime import datetime

#implementação do requisito funcional de encapsulamento
class Retrato_horario():
    def __init__(self, horario_programado, horario_real):
        self.__horario_programado = datetime.strptime(horario_programado,"%H:%M")
        self.__horario_real = datetime.strptime(horario_real,"%H:%M")

    @property
    def horario_programado(self):
        return self.__horario_programado
    @property
    def horario_real(self):
        return self.__horario_real
    @property
    def calcular_atraso(self):
        atraso = self.__horario_real - self.__horario_programado

        return atraso.total_seconds() / 60
