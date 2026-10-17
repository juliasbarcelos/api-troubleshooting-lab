from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from mysql.connector import Error

from api.database import obter_ligacao


# Configuração da aplicação
app = FastAPI(
    title="API de Gestão de Pedidos",
    description="Laboratório de investigação de incidentes em APIs REST",
    version="1.0.0"
)


# Modelo para validar os dados de um novo pedido
class NovoPedido(BaseModel):
    cliente: str = Field(min_length=1, max_length=100)
    produto: str = Field(min_length=1, max_length=100)
    quantidade: int = Field(gt=0)
    estado: str = Field(default="pendente", min_length=1, max_length=30)


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
        ligacao = obter_ligacao()
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
        raise HTTPException(
            status_code=503,
            detail="Serviço de base de dados indisponível"
        )

    finally:
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
        ligacao = obter_ligacao()
        cursor = ligacao.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, cliente, produto, quantidade,
                   estado, data_criacao
            FROM pedidos
            WHERE id = %s
        """, (pedido_id,))

        pedido = cursor.fetchone()

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
        if cursor is not None:
            cursor.close()

        if ligacao is not None and ligacao.is_connected():
            ligacao.close()


# Endpoint 4 — Criar um novo pedido
@app.post("/pedidos", status_code=201)
def criar_pedido(novo_pedido: NovoPedido):
    ligacao = None
    cursor = None

    try:
        # Estabelecer ligação ao MySQL
        ligacao = obter_ligacao()
        cursor = ligacao.cursor()

        # Inserir os dados de forma parametrizada
        cursor.execute("""
            INSERT INTO pedidos
                (cliente, produto, quantidade, estado)
            VALUES (%s, %s, %s, %s)
        """, (
            novo_pedido.cliente,
            novo_pedido.produto,
            novo_pedido.quantidade,
            novo_pedido.estado
        ))

        # Confirmar a gravação na base de dados
        ligacao.commit()

        # Recuperar o identificador criado pelo MySQL
        pedido_id = cursor.lastrowid

        return {
            "id": pedido_id,
            "cliente": novo_pedido.cliente,
            "produto": novo_pedido.produto,
            "quantidade": novo_pedido.quantidade,
            "estado": novo_pedido.estado,
            "message": "Pedido criado com sucesso"
        }

    except Error:
        if ligacao is not None and ligacao.is_connected():
            ligacao.rollback()

        raise HTTPException(
            status_code=503,
            detail="Erro ao guardar o pedido na base de dados"
        )

    finally:
        if cursor is not None:
            cursor.close()

        if ligacao is not None and ligacao.is_connected():
            ligacao.close()
