from fastapi import FastAPI, HTTPException
from mysql.connector import Error

from api.database import obter_ligacao


# Configuração da aplicação
app = FastAPI(
    title="API de Gestão de Pedidos",
    description="Laboratório de investigação de incidentes em APIs REST",
    version="1.0.0"
)


# Endpoint 1 — Verificar o funcionamento da API
@app.get("/health")
def verificar_estado():
    return {
        "status": "ok",
        "message": "API em funcionamento"
    }


# Endpoint 2 — Consultar todos os pedidos
@app.get("/pedidos")
def listar_pedidos():
    ligacao = None
    cursor = None

    try:
        # Estabelecer ligação à base de dados
        ligacao = obter_ligacao()

        # Preparar a consulta
        cursor = ligacao.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, cliente, produto, quantidade,
                   estado, data_criacao
            FROM pedidos
            ORDER BY id
        """)

        # Recuperar todos os pedidos
        pedidos = cursor.fetchall()

        return pedidos

    except Error:
        raise HTTPException(
            status_code=503,
            detail="Serviço de base de dados indisponível"
        )

    finally:
        # Fechar cursor e ligação
        if cursor is not None:
            cursor.close()

        if ligacao is not None and ligacao.is_connected():
            ligacao.close()


# Endpoint 3 — Consultar um pedido pelo ID
@app.get("/pedidos/{pedido_id}")
def consultar_pedido(pedido_id: int):
    ligacao = None
    cursor = None

    try:
        # Estabelecer ligação à base de dados
        ligacao = obter_ligacao()

        # Preparar a consulta
        cursor = ligacao.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, cliente, produto, quantidade,
                   estado, data_criacao
            FROM pedidos
            WHERE id = %s
        """, (pedido_id,))

        # Recuperar apenas um pedido
        pedido = cursor.fetchone()

        # Verificar se o pedido existe
        if pedido is None:
            raise HTTPException(
                status_code=404,
                detail="Pedido não encontrado"
            )

        return pedido

    except Error:
        raise HTTPException(
            status_code=503,
            detail="Serviço de base de dados indisponível"
        )

    finally:
        # Fechar cursor e ligação
        if cursor is not None:
            cursor.close()

        if ligacao is not None and ligacao.is_connected():
            ligacao.close()
