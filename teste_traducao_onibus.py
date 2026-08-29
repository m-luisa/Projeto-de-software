from servicos.gtfs_usuario import GtfsUsuario
from api_oculta import GtfsService

cliente = GtfsUsuario("http://realtime4.mobilibus.com/web/4ch6j/trip-updates?accesskey=982a57efd77a9462bf1665696fb25984")
atualizacoes = cliente.buscar_atualizacoes()

atualizacao_valida = None
for a in atualizacoes:
    paradas = a["trip_update"]["stop_time_update"]
    if paradas[0]["departure"] and (paradas[-1]["arrival"] or paradas[-1]["departure"]):
        atualizacao_valida = a
        break

if atualizacao_valida:
    onibus_limpo = GtfsService.criar_onibus_gtfs(atualizacao_valida)
    print(onibus_limpo)
else:
    print("Nenhuma atualização com partida e chegada completas encontrada — tenta rodar de novo.")
