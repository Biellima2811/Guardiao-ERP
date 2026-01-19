import logging
import os
from datetime import datetime

# Garante que a pasta logs existe
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configuração do Logger
arquivo_log = f"logs/sistema_{datetime.now().strftime('%Y-%m-%d')}.log"

logging.basicConfig(
    filename=arquivo_log,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S'
)

# Função auxiliar para usar no sistema
def log_info(mensagem):
    logging.info(mensagem)
    print(f"[INFO] {mensagem}") # Mostra no terminal também

def log_erro(mensagem, erro):
    logging.error(f"{mensagem}: {erro}")
    print(f"[ERRO] {mensagem}: {erro}")