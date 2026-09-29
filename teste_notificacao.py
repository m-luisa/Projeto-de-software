"""
Teste do rf10: força atrasos com transportes FALSOS e dispara as notificações de verdade.
Não depende de nenhuma API externa nem de haver atraso real no momento.

Rode com:  python3 teste_notificacao.py
"""
from modelos.canal_notificacao import CanalEmail, CanalPush
from modelos.usuario import UsuarioInscrito
from servicos.notificador import Notificador


class TransporteFalso:
    # imita só o que o Notificador usa: id_transporte, calcular_atraso e exibir_status
    def __init__(self, id_transporte: str, atraso_min: int):
        self.id_transporte = id_transporte
        self._atraso_min = atraso_min

    def calcular_atraso(self) -> int:
        return self._atraso_min

    def exibir_status(self) -> str:
        if self._atraso_min > 0:
            return f"{self.id_transporte} -> ATRASADO {self._atraso_min} min"
        return f"{self.id_transporte} -> NO HORARIO"


# --- monta o usuário com os canais que você quiser testar (Enter = pular) ---
inscricoes = []

email = input("E-mail para teste (Enter para pular): ").strip()
if email:
    inscricoes.append((CanalEmail(), email))

topico = input("Tópico do ntfy para teste (Enter para pular): ").strip()
if topico:
    inscricoes.append((CanalPush(), topico))

if not inscricoes:
    print("Nenhum canal escolhido, nada para testar.")
    raise SystemExit

notificador = Notificador()
notificador.inscrever(UsuarioInscrito("Teste", inscricoes))

voo = TransporteFalso("AZ 1234", 20)
onibus = TransporteFalso("Onibus 032", 12)
trem = TransporteFalso("Trem R1", 0)  # sem atraso: NÃO deve aparecer na mensagem

# --- rodada 1: deve enviar UMA mensagem por canal, com 2 atrasos ---
print("\n--- Rodada 1 (deve enviar: voo e ônibus) ---")
for t in (voo, onibus, trem):
    notificador.notificar_atraso(t)
notificador.enviar_pendentes()

# --- rodada 2: mesmos atrasos, NÃO deve enviar nada ---
print("\n--- Rodada 2 (mesmos atrasos: não deve enviar nada) ---")
for t in (voo, onibus, trem):
    notificador.notificar_atraso(t)
notificador.enviar_pendentes()

# --- rodada 3: o ônibus piorou, deve avisar só ele ---
print("\n--- Rodada 3 (ônibus piorou para 25 min: deve enviar só ele) ---")
onibus = TransporteFalso("Onibus 032", 25)
for t in (voo, onibus, trem):
    notificador.notificar_atraso(t)
notificador.enviar_pendentes()