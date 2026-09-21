from abc import ABC, abstractmethod
"""
rf10 notificações desacopladas

CanaalNotificacao é uma classe abstrata 
CanalEmail e CanalPush implementam de acordo com suas proprias maneiras o metodo da CanalNotificacao

"""
class CanalNotificacao(ABC):
    @abstractmethod
    def enviar(self, destinatario: str, mensagem: str) -> None:
        raise NotImplementedError


class CanalEmail(CanalNotificacao):
    #herança + polimorfismo: implementa o enviar da classe
    def enviar(self, destinatario: str, mensagem: str) -> None:
        print(f"[E-mail para {destinatario}] {mensagem}")


class CanalPush(CanalNotificacao):
    def enviar(self, destinatario: str, mensagem: str) -> None:
        print(f"[Push para {destinatario}] {mensagem}")