from servicos.aviationstack_usuario import AviationStack
from api_oculta import AviationStackService

cliente = AviationStack()
json_cru = cliente.buscar_voo("SQ8451")

voo_limpo = AviationStackService.criar_voo_json(json_cru)
print(voo_limpo.codigo, voo_limpo.origem, voo_limpo.destino, voo_limpo.horario_estimado)

