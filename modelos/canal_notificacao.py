from abc import ABC, abstractmethod
import os
import logging
import smtplib
from email.message import EmailMessage
import requests
from dotenv import load_dotenv

load_dotenv()  # carrega as variáveis do .env para o os.getenv

"""
rf10 notificações desacopladas

CanalNotificacao é uma classe abstrata.
CanalEmail e CanalPush implementam, cada um do seu jeito, o método enviar.
Para adicionar um canal novo (ex.: SMS) basta criar outra classe aqui,
sem mexer no Notificador nem na detecção de atraso.
"""


class CanalNotificacao(ABC):
    @abstractmethod
    def enviar(self, destinatario: str, mensagem: str) -> None:
        raise NotImplementedError


class CanalEmail(CanalNotificacao):
    # herança + polimorfismo: implementa o enviar da classe base, agora enviando de verdade
    def __init__(self):
        self.servidor_smtp = "smtp.gmail.com"
        self.porta = 587  # porta com STARTTLS (a 465 não conectava no seu computador)
        self.remetente = os.getenv("EMAIL_REMETENTE")
        self.senha_app = os.getenv("EMAIL_SENHA_APP")  # senha de app do Gmail, NÃO a senha normal

    def enviar(self, destinatario: str, mensagem: str) -> None:
        # sem credenciais no .env não dá pra enviar: avisa e segue sem travar o painel
        if not self.remetente or not self.senha_app:
            logging.warning("Credenciais de e-mail não configuradas no .env")
            return

        # monta a mensagem
        email = EmailMessage()
        email["Subject"] = "Painel de Transportes - Aviso de atraso"
        email["From"] = self.remetente
        email["To"] = destinatario
        email.set_content(mensagem)  # corpo em texto simples

        try:
            # o 'with' fecha a conexão sozinho no final, mesmo se der erro
            with smtplib.SMTP(self.servidor_smtp, self.porta, timeout=10) as servidor:
                servidor.starttls()  # liga a criptografia depois de conectar
                servidor.login(self.remetente, self.senha_app)
                servidor.send_message(email)
            print(f"[E-mail enviado para {destinatario}]")
        except (smtplib.SMTPException, OSError) as erro:
            # falha de rede ou de login não pode derrubar o sistema (rf8)
            logging.warning(f"Não foi possível enviar e-mail para {destinatario}: {erro}")


class CanalPush(CanalNotificacao):
    """
    Push de verdade usando o ntfy (https://ntfy.sh): serviço gratuito, sem conta e sem chave.
    Como funciona: a pessoa instala o app "ntfy" no celular e assina um TÓPICO (um nome).
    Quando o programa faz um POST para https://ntfy.sh/<topico>, o app recebe a notificação.
    Aqui, o 'destinatario' é o nome do tópico.
    """
    def __init__(self):
        # dá para trocar de servidor no .env (ex.: um ntfy próprio); o padrão é o público
        self.servidor = os.getenv("NTFY_SERVIDOR", "https://ntfy.sh").rstrip("/")

    def enviar(self, destinatario: str, mensagem: str) -> None:
        # o ntfy limita o tamanho da mensagem (~4 KB); corta para não ser recusada
        if len(mensagem) > 1500:
            mensagem = mensagem[:1500] + "\n(...)"

        try:
            resposta = requests.post(
                f"{self.servidor}/{destinatario}",
                data=mensagem.encode("utf-8"),  # corpo da notificação
                headers={
                    "Title": "Painel de Transportes",  # título (cabeçalho: só caracteres simples)
                    "Priority": "high",                # prioridade alta faz o celular vibrar/tocar
                    "Tags": "warning",                 # mostra um ícone de alerta
                },
                timeout=10,  # nunca espera para sempre
            )
            resposta.raise_for_status()  # transforma erro HTTP (404, 500...) em exceção
            print(f"[Push enviado para o tópico {destinatario}]")
        except requests.RequestException as erro:
            # sem internet ou servidor fora do ar: avisa e segue (rf8)
            logging.warning(f"Não foi possível enviar push para {destinatario}: {erro}")