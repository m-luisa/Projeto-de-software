from servicos.gtfs_usuario import GtfsUsuario

cliente = GtfsUsuario("http://realtime4.mobilibus.com/web/4ch6j/trip-updates?accesskey=982a57efd77a9462bf1665696fb25984")
posicoes = cliente.buscar_posicoes()
print(len(posicoes), "posições encontradas")
if posicoes:
    primeiro_id = list(posicoes.keys())[0]
    print(primeiro_id, "->", posicoes[primeiro_id])