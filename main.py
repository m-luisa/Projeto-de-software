from datetime import datetime
from modelos.localizacao import Localizacao
from modelos.retrato_horario import Retrato_horario
from modelos.transporte import Voo, Onibus, Trem

retrato_voo = Retrato_horario("10:00", "10:20")

print("Horário programado:", retrato_voo.horario_programado)
print("Horário real:", retrato_voo.horario_real)
print("Atraso:", retrato_voo.calcular_atraso, "minutos")

retrato_voo = Retrato_horario("10:00", "10:15")
retrato_onibus = Retrato_horario("10:30", "10:40")
retrato_trem = Retrato_horario("11:00", "11:00")


voo = Voo(
    "Maceió",
    "Recife",
    retrato_voo,
    "Atrasado",
    "AB123"
)

onibus = Onibus(
    "Centro",
    "Ponta Verde",
    retrato_onibus,
    "Atrasado",
    "101"
)

trem = Trem(
    "Maceió",
    "Lourdes",
    retrato_trem,
    "No horário",
    "Linha 1"
)


print("Voo:", voo.calcular_atraso(), "minutos")
print("Ônibus:", onibus.calcular_atraso(), "minutos")
print("Trem:", trem.calcular_atraso(), "minutos")