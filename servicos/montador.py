from modelos.retrato_horario import Retrato_horario
from modelos.transporte import Voo as VooDominio, Onibus as OnibusDominio, Trem as TremDominio

"""
rf5 - ponte entre a api oculta, gtfs_usuario e o dominio final usado no painel. cada função vai receber um on=bjeto e devolve o respectivo objeto de dominio com retrto_horario validado (rf2)
"""
def montar_voo_dominio(voo_api) -> VooDominio: 
    #tratamento de erro
    try:
        retrato = Retrato_horario(
            voo_api.horario_programado.strftime("%H:%M"),
            voo_api.horario_estimado.strftime("%H:%M"),
        )
    except (ValueError, AttributeError) as erro:
        raise ValueError(f"Não foi possível montar o voo '{getattr(voo_api, 'codigo', '?')}': {erro}") from erro

    return VooDominio(voo_api.origem, voo_api.destino, retrato, voo_api.codigo)

def montar_onibus_dominio(onibus_api) -> OnibusDominio:
    try:
        retrato = Retrato_horario(
            onibus_api.horario_programado.strftime("%H:%M"),
            onibus_api.horario_chegada.strftime("%H:%M"),
        )
    except (ValueError, AttributeError) as erro:
        raise ValueError(
            f"Não foi possível montar o ônibus '{getattr(onibus_api, 'identificador', '?')}': {erro}"
        ) from erro
    #rf9 - passa o indentificador do veiculo para o objeto de dominio, que vai garantir que a deduolicação no registrotransportes seja feita
    return OnibusDominio(
        onibus_api.origem, onibus_api.destino, retrato, onibus_api.linha,
        identificador=onibus_api.identificador,
    )

def montar_trem_dominio(trem_api) -> TremDominio:
    try:
        #RF2 - a api Trilhos não informa um horário programado por viagem
        #(só o status da linha), então o retrato registra o momento da
        #consulta; a cada nova busca um retrato novo e imutável é criado,
        #o que já basta pra comparar "o que mudou desde então?" (histórico)
        momento_str = trem_api.atualizado_em.strftime("%H:%M")
        retrato = Retrato_horario(momento_str, momento_str)
    except (ValueError, AttributeError) as erro:
        raise ValueError(f"Não foi possível montar o trem '{getattr(trem_api, 'identificador', '?')}': {erro}") from erro
    #rf3 - o trem usa o status informado pela operadora, não um cálculo de atraso
    return TremDominio(
        trem_api.origem, trem_api.destino, retrato, trem_api.linha,
        trem_api.status_operadora, operacao_normal=trem_api.operacao_normal,
        identificador=trem_api.identificador,
    )