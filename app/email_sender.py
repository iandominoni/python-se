"""
Módulo para envio de prontuários por email via SMTP.
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from pathlib import Path
from email_config import EMAIL_CONFIG


class EmailSender:
    """Gerenciador de envio de emails com prontuários PDF."""

    def __init__(self):
        self.config = EMAIL_CONFIG
        self.smtp_server = self.config["smtp_server"]
        self.smtp_port = int(self.config["smtp_port"])
        self.sender_email = self.config["sender_email"]
        self.sender_password = self.config["sender_password"]
        self.sender_name = self.config["sender_name"]

    def send_prontuario(self, recipient_email, recipient_name, pdf_path):
        """
        Envia prontuário em PDF por email.

        Args:
            recipient_email: Email do destinatário
            recipient_name: Nome do destinatário
            pdf_path: Caminho completo do arquivo PDF

        Returns:
            Tupla (sucesso: bool, mensagem: str)
        """
        try:
            # Validar arquivo
            if not Path(pdf_path).exists():
                return False, f"Arquivo não encontrado: {pdf_path}"

            # Criar mensagem
            msg = MIMEMultipart()
            msg["From"] = f"{self.sender_name} <{self.sender_email}>"
            msg["To"] = recipient_email
            msg["Date"] = formatdate(localtime=True)
            msg["Subject"] = "Prontuário de Avaliação - Sistema de Avaliação"

            # Corpo do email
            body = f"""
Prezado(a) {recipient_name},

Segue anexado o prontuário de sua avaliação realizada através do Sistema de Avaliação de Risco.

IMPORTANTE - DOCUMENTO ACADÊMICO 

Este é um PROJETO ACADÊMICO/EDUCACIONAL desenvolvido para fins de aprendizagem e pesquisa.
Este sistema E SEUS RESULTADOS NÃO DEVEM SER UTILIZADOS PARA DIAGNÓSTICO OU TRATAMENTO CLÍNICO REAL.

Este documento contém:
• Resultado geral da avaliação
• Detalhamento por eixo temático
• Recomendações baseadas no resultado
• Data e hora da avaliação

AVISO CRÍTICO:
Esta avaliação é uma ferramenta acadêmica de triagem e os resultados podem apresentar variações significativas.
A interpretação clínica deve considerar idade, contexto e histórico individual.
Este instrumento NÃO substitui JAMAIS a avaliação de um profissional de saúde qualificado e credenciado.
Use apenas para fins educacionais e de pesquisa.

---
Sistema de Avaliação de Risco para Transtornos Alimentares
Projeto Acadêmico - Apenas para fins educacionais

"""

            msg.attach(MIMEText(body, "plain"))

            # Anexar PDF
            with open(pdf_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)
            filename = Path(pdf_path).name
            part.add_header("Content-Disposition", f"attachment; filename= {filename}")
            msg.attach(part)

            # Enviar email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Criptografia
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            return True, f"Email enviado com sucesso para {recipient_email}"

        except smtplib.SMTPAuthenticationError:
            return False, "Erro de autenticação. Verifique email e senha."
        except smtplib.SMTPException as e:
            return False, f"Erro ao enviar email: {str(e)}"
        except Exception as e:
            return False, f"Erro inesperado: {str(e)}"
