from gtfs_usuario import GtfsUsuario

cliente = GtfsUsuario("http://realtime4.mobilibus.com/web/4ch6j/trip-updates?accesskey=982a57efd77a9462bf1665696fb25984")
atualizacoes = cliente.buscar_atualizacoes()
print(len(atualizacoes), "atualizações encontradas")
print(atualizacoes[0] if atualizacoes else "nenhuma")