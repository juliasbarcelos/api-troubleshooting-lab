from api.database import obter_ligacao


def testar_ligacao():
    ligacao = None
    cursor = None

    try:
        # Estabelecer ligação ao MySQL
        ligacao = obter_ligacao()

        # Criar cursor para executar consultas SQL
        cursor = ligacao.cursor()

        # Consultar o total de pedidos existentes
        cursor.execute("SELECT COUNT(*) FROM pedidos")

        # Obter o resultado da consulta
        total = cursor.fetchone()[0]

        # Apresentar o resultado
        print("Ligação ao MySQL estabelecida com sucesso.")
        print(f"Total de pedidos encontrados: {total}")

    except Exception as erro:
        # Apresentar informações para diagnóstico
        print("Falha na ligação ou consulta MySQL.")
        print(f"Tipo de erro: {type(erro).__name__}")
        print(f"Código MySQL: {getattr(erro, 'errno', 'Não disponível')}")
        print(f"SQLSTATE: {getattr(erro, 'sqlstate', 'Não disponível')}")
        print("Consulta não concluída. Verificar configuração e logs.")

    finally:
        # Fechar o cursor
        if cursor is not None:
            cursor.close()

        # Fechar a ligação com o MySQL
        if ligacao is not None and ligacao.is_connected():
            ligacao.close()


if __name__ == "__main__":
    testar_ligacao()