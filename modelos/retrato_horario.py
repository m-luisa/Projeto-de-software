from dotenv import parser
from datetime import datetime

""" 
rf2 - retratos imutáveis de horário

o retrato vai representar uma foto fixa do horário programado e real do transporte. Depois de criado o objeto nõ pode ser modificado
se o transporte atrasar será criado um novo objeto no lugar de mudar o que já existe, para ser possível comparar o retrato de agora com o de antes
"""
class Retrato_horario(): 
    def __init__(self, horario_programado, horario_real):
        #tratamento de erro para caso de horarios fora do formato
        try:
            self.__horario_programado = datetime.strptime(horario_programado, "%H:%M")
            self.__horario_real = datetime.strptime(horario_real, "%H:%M")
        except(ValueError, TypeError) as erro:
            raise ValueError(
                f"Horários inválidos (esperado 'HH:MM'): programado={horario_programado!r}, "
                f"real={horario_real!r} -> {erro}"
            ) from erro
    #encapsulamento
    @property
    def horario_programado(self):
        return self.__horario_programado
    @property
    def horario_real(self):
        return self.__horario_real
    
    #calcula a diferença em minutos do horario real e programado desse retrato específico, não altera os atributos
    def calcular_diferenca(self): 
        diferenca = self.__horario_real - self.__horario_programado
        return diferenca.total_seconds() / 60
