from modelos.retrato_horario import Retrato_horario
from modelos.transporte import Voo as VooDominio

def montar_voo_dominio(voo_api, horario_programado_str: str) -> VooDominio:
    retrato = Retrato_horario(
        horario_programado_str, voo_api.horario_estimado.strftime("%H:%M")
    )

    return VooDominio(voo_api.origem, voo_api.destino, retrato, voo_api.codigo)
    