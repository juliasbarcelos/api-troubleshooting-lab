import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

# Localizar o ficheiro .env na pasta principal
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def obter_ligacao():
    """Estabelece uma ligação à base de dados MySQL."""

    ligacao = mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        connection_timeout=5
    )

    return ligacao
