
from datetime import datetime, timedelta
from core import Localizacao, VooSnapshot, OnibusSnapshot, TremSnapshot, Viagem
from api import AviationStackClient

agora = datetime.now()

loc = Localizacao(latitude=-23.55, longitude=-46.63, nome_local="Terminal")

cliente_api = AviationStackClient(api_key="chave api")
voo = cliente_api.buscar_voo("LA3000")

if not voo:
    print("Usando voo simulado para o teste...")
    voo = VooSnapshot("LA3000", agora, agora + timedelta(minutes=20), agora, loc) 

onibus = OnibusSnapshot("BUS-100", agora + timedelta(hours=2), agora + timedelta(hours=2, minutes=5), agora, loc) 
trem = TremSnapshot("TREM-01", agora + timedelta(hours=4), agora + timedelta(hours=4), agora, "EM_DIA")

minha_viagem = Viagem("SP-RJ-001", [voo, onibus, trem])
minha_viagem.exibir_painel()