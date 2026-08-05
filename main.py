from datetime import datetime, timedelta
from core import Localizacao, VooSnapshot, OnibusSnapshot, TremSnapshot, Viagem
from api import AviationStackClient

agora = datetime.now()

local_terminal = Localizacao(latitude=-23.55, longitude=-46.63, nome_local="Terminal Tietê")
L
CHAVE_API = "67cd9cbcb038a09e2f3a0a941181599b"
cliente = AviationStackClient(api_key=CHAVE_API)

voo = cliente.buscar_voo("LA3467")

if not voo:
    voo = VooSnapshot(
        id_trecho="LA3467",
        programado=agora,
        estimado=agora + timedelta(minutes=20),
        captura=agora,
        localizacao=local_terminal
    )

onibus = OnibusSnapshot(
    id_trecho="BUS-100", 
    programado=agora + timedelta(hours=2), 
    estimado=agora + timedelta(hours=2, minutes=5), 
    captura=agora, 
    localizacao=local_terminal
) 

trem = TremSnapshot(
    id_trecho="TREM-01", 
    programado=agora + timedelta(hours=4), 
    estimado=agora + timedelta(hours=4), 
    captura=agora, 
    status_operadora="EM_DIA"
)

minha_viagem = Viagem(id_viagem="SP-RJ-001", trechos=[voo, onibus, trem])
minha_viagem.exibir_painel()

print("\nTESTANDO VALIDAÇÃO DE COORDENADAS")
try:
    coordenada_errada = Localizacao(latitude=950.0, longitude=-46.63)
except ValueError as erro:
    print(f"O sistema rejeitou a coordenada inválida: {erro}")