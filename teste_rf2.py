from modelos.retrato_horario import Retrato_horario 

#cria um retrato
retrato = Retrato_horario("08:00", "08:05")
print("Diferença:", retrato.calcular_diferenca(), "minutos")

#tenta mudar o horário (não pode, é imutável)
try:
    retrato.horario_programado = "09:00"
    print("Conseguiu muda)")
except AttributeError:
    print("O retrato é imutável.")

#se atrasar, cria um retrato NOVO, o antigo continua igual
novo_retrato = Retrato_horario("08:00", "08:15")
print("Retrato antigo continua com diferença:", retrato.calcular_diferenca())
print("Retrato novo tem diferença:", novo_retrato.calcular_diferenca())