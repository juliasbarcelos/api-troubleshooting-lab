from fastapi import FastAPI, HTTPException
from mysql.connector import Error

from api.database import obter_ligacao


app = FastAPI(
    title="API de Gestão de Pedidos",
    description="Laboratório de investigação de incidentes em APIs REST",
    version="1.0.0"
)


@app.get("/health")
def verificar_estado():
    return {
        "status": "ok",
        "message": "API em funcionamento"
    }


@app.get("/pedidos")
def listar_pedidos():
    ligacao = None
    cursor = None

    try:
        # Estabelecer ligação à base de dados
        ligacao = obter_ligacao()

        # Consultar os pedidos e devolver os campos por nome
        cursor = ligacao.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, cliente, produto, quantidade,
                   estado, data_criacao
            FROM pedidos
            ORDER BY id
        """)

        pedidos = cursor.fetchall()

        return pedidos

    except Error:
        # Não divulgar detalhes internos da base de dados na API
        raise HTTPException(
            status_code=503,
            detail="Serviço de base de dados indisponível"
        )

    finally:
        # Libertar os recursos utilizados
        if cursor is not None:
            cursor.close()

        if ligacao is not None and ligacao.is_connected():
            ligacao.close()
