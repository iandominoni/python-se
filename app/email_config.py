"""
Configuração de email para envio de prontuários.
Lê credenciais de variáveis de ambiente para não expor dados sensíveis no Git.
"""

import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env (se existir)
load_dotenv()

# Configuração de Email - Dados sensíveis vêm de variáveis de ambiente
EMAIL_CONFIG = {
    "provider": os.getenv("EMAIL_PROVIDER", "gmail"),
    "sender_email": os.getenv("EMAIL_SENDER"),
    "sender_password": os.getenv("EMAIL_PASSWORD"),
    "sender_name": "Sistema de Avaliação",
    "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    "smtp_port": int(os.getenv("SMTP_PORT", "587")),
}

# Validar se credenciais estão configuradas
if not EMAIL_CONFIG["sender_email"] or not EMAIL_CONFIG["sender_password"]:
    raise EnvironmentError(
        "\nCredenciais de email não configuradas!\n\n"
        "Para usar o envio de emails, configure as variáveis de ambiente:\n"
        "  - EMAIL_SENDER: seu.email@gmail.com\n"
        "  - EMAIL_PASSWORD: sua_senha_de_app\n"
        "\nOpções:\n"
        "  1. Criar arquivo .env na pasta do app (NÃO FAZER COMMIT)\n"
        "  2. Definir variáveis de ambiente do sistema\n"
        "  3. Ver arquivo .env.example para referência\n"
    )
