from datetime import datetime

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
    
    #mudei calcular_atraso para calcular_diferenca pq esse nome fica mais claro o que o método de fato faz e criei em transportes.py o metodo que de fato vai calcular o atraso com base na diferença de horarios
    def calcular_diferenca(self): 
        diferenca = self.__horario_real - self.__horario_programado
        return diferenca.total_seconds() / 60
