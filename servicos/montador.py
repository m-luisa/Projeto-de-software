from modelos.retrato_horario import Retrato_horario
from modelos.transporte import Voo as VooDominio, Onibus as OnibusDominio, Trem as TremDominio

#mudança para tratamento de erro
def montar_voo_dominio(voo_api) -> VooDominio: #essa função converte os daddos brutos da api em objeto de dominio
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
    #rf9 - garante que a deduplicação seja por veiculo e nao por linha
    return OnibusDominio(
        onibus_api.origem, onibus_api.destino, retrato, onibus_api.linha,
        identificador=onibus_api.identificador,
    )

def montar_trem_dominio (trem_api, horario_programado_str: str, status_operadora: str) -> TremDominio:
    try:
        retrato = Retrato_horario(
            horario_programado_str, trem_api.horario_chegada.strftime("%H:%M"))
    except (ValueError, AttributeError) as erro:
        raise ValueError(f"Não foi possível montar o trem '{getattr(trem_api, 'identificador', '?')}': {erro}") from erro
    return TremDominio (trem_api.origem, trem_api.destino, retrato, trem_api.linha, status_operadora)
    
