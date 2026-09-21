#rf10 - representa o usuario que deve se inscrever para receber as notificações de atraso

#inscricoes é uma lista que pode misturar CanalEmail e CanalPush 

class UsuarioInscrito:
    def __init__(self, nome: str, inscricoes: list):
        #tratamento de erro
        if not inscricoes:
            raise ValueError(
                f"Usuário '{nome}' precisa de pelo menos um canal de notificação."
            )
        self.nome = nome
        self.inscricoes = inscricoes