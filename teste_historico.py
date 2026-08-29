from modelos.retrato_horario import Retrato_horario
from modelos.historico_retratos import HistoricoRetratos

historico = HistoricoRetratos()

#simula a primeira coleta c voo no horário
retrato_14h = Retrato_horario("14:00", "14:00")
historico.registrar("AZ1234", retrato_14h)
print(historico.mudou("AZ1234"))  # deve dizer "nada a comparar ainda"

#simula uma coleta nova c 20 minutos de atraso
retrato_14h20 = Retrato_horario("14:00", "14:20")
historico.registrar("AZ1234", retrato_14h20)
print(historico.mudou("AZ1234"))  # deve mostrar a mudança de 0 pra 20 min

#confirma que o retrato das 14:00 continua o mwsmo
print("Retrato antigo continua mostrando:", historico.penultimo("AZ1234").calcular_diferenca(), "min")