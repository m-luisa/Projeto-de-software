from modelos.retrato_horario import Retrato_horario
from modelos.transporte import Voo, Onibus, Trem

#atualização da main para atender o RF4
#vms mudar para fazer um menu de interação com o usuário, usando o que já temos de código 

#horarios - programado e real
retrato_voo = Retrato_horario("10:00", "10:20")
retrato_onibus = Retrato_horario("10:30", "10:42")
retrato_trem = Retrato_horario("11:00", "11:00")


#transportes
voo = Voo(
    "Maceió",
    "Recife",
    retrato_voo,
    "AZ1234"
)

onibus = Onibus(
    "Centro",
    "Ponta Verde",
    retrato_onibus,
    "032"
)

trem = Trem(
    "Maceió",
    "Lourdes",
    retrato_trem,
    "R1"
)


#painel - rf4 - polimorfismo
transportes = [voo, onibus, trem]

for transporte in transportes:
    print(transporte.exibir_status())