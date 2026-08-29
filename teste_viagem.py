from modelos.retrato_horario import Retrato_horario
from modelos.transporte import Voo, Onibus
from modelos.viagem import Viagem

#voo que atrasou 30 minutos
retrato_voo = Retrato_horario("13:00", "13:30")
voo = Voo("GRU", "MCZ", retrato_voo, "AZ1234")

#ônibus que atrasou 12 minutos
retrato_onibus = Retrato_horario("14:35", "14:47")
onibus = Onibus("Aeroporto", "Centro", retrato_onibus, "032")

viagem = Viagem([voo, onibus])
print(viagem.exibir_status())