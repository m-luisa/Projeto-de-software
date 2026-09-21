from modelos.usuario import UsuarioInscrito

"""
rf10- polimorfismo- notificações de atraso desacopladas da detecção
o notificador nao sabe quais canais existem, aqui ele apenas chama canal.enviar em cada canal da lista de inscrições
adicionar novo canal nao altera esse arquivo
"""
class Notificador:
    def __init__(self):
        self._inscritos: list[UsuarioInscrito] = []
    
    def inscrever(self, usuario: UsuarioInscrito) -> None:
        self._inscritos.append(usuario)
    def notificar_atraso(self, transporte) ->None:
    #rf10 - usa o calculo de atraso do transporte para decidir se notifica
        atraso = transporte.calcular_atraso()
        if atraso <= 0:
            return

        mensagem = f"Atraso detectado - {transporte.exibir_status()}"

        #rf10 - dispra os canais do usuario
        for usuario in self._inscritos:
            for canal, destinatario in usuario.inscricoes:
                canal.enviar(destinatario, mensagem)