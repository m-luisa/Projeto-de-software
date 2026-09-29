import logging

from modelos.usuario import UsuarioInscrito

"""
rf10- polimorfismo- notificações de atraso desacopladas da detecção
o notificador nao sabe quais canais existem, aqui ele apenas chama canal.enviar em cada canal da lista de inscrições
adicionar novo canal nao altera esse arquivo

Funcionamento em duas etapas:
  1) notificar_atraso  -> DETECTA o atraso e guarda a mensagem numa fila (não envia nada)
  2) enviar_pendentes  -> junta a fila em UMA mensagem e envia uma vez por canal
Assim o painel não fica lento e ninguém recebe 30 e-mails seguidos.
"""
class Notificador:
    def __init__(self):
        self._inscritos: list[UsuarioInscrito] = []
        self._avisos_enviados: set = set()   # guarda (id_transporte, atraso) que já foram avisados
        self._pendentes: list[str] = []      # mensagens esperando para serem enviadas juntas

    def inscrever(self, usuario: UsuarioInscrito) -> None:
        self._inscritos.append(usuario)

    def notificar_atraso(self, transporte) -> None:
        # rf10 - usa o calculo de atraso do transporte para decidir se notifica
        atraso = transporte.calcular_atraso()
        if atraso <= 0:
            return

        # se já avisamos exatamente esse atraso desse transporte, não repete
        # (se o atraso mudar, ex.: de 12 para 20 min, a chave muda e avisa de novo)
        chave = (transporte.id_transporte, atraso)
        if chave in self._avisos_enviados:
            return

        self._avisos_enviados.add(chave)
        self._pendentes.append(f"- {transporte.exibir_status()}")

    def enviar_pendentes(self) -> None:
        # nada novo para avisar: não faz nada
        if not self._pendentes:
            return

        # junta todos os atrasos novos em UM texto só
        mensagem = f"{len(self._pendentes)} atraso(s) detectado(s):\n" + "\n".join(self._pendentes)
        self._pendentes = []  # limpa a fila antes de enviar

        # rf10 - dispara os canais de cada usuário, sem saber qual canal é qual
        for usuario in self._inscritos:
            for canal, destinatario in usuario.inscricoes:
                try:
                    canal.enviar(destinatario, mensagem)
                except Exception as erro:
                    # um canal com problema não pode impedir os outros de receberem o aviso
                    logging.warning(f"Falha no canal {type(canal).__name__}: {erro}")