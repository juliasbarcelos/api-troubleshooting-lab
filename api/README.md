# API — Implementação e Integração com MySQL

## Sobre Esta Pasta

Esta pasta contém o código-fonte da API REST desenvolvida para o projeto **API Troubleshooting Lab**.

A aplicação foi implementada em Python, utilizando FastAPI para disponibilizar endpoints HTTP e MySQL para armazenar pedidos fictícios de uma plataforma de comércio eletrónico.

O objetivo é demonstrar competências práticas em desenvolvimento, integração de sistemas, validação de dados e diagnóstico de incidentes aplicacionais.

---

## 1. Estrutura dos Ficheiros

| Ficheiro | Responsabilidade |
|---|---|
| `main.py` | Implementação dos endpoints REST e tratamento das requisições |
| `database.py` | Configuração e estabelecimento da ligação ao MySQL |
| `testar_ligacao.py` | Teste independente de conectividade com a base de dados |

### main.py

Contém a aplicação FastAPI e as funcionalidades principais:

- Verificação do funcionamento básico da API.
- Listagem dos pedidos armazenados.
- Consulta de pedidos por identificador.
- Criação de novos pedidos.
- Validação dos dados através de Pydantic.
- Tratamento de erros HTTP.
- Execução de operações SQL.

### database.py

Centraliza a configuração da ligação ao MySQL.

As informações de ligação são carregadas através de variáveis de ambiente definidas num ficheiro `.env`, localizado na raiz do projeto.

Esta separação evita a necessidade de incluir diretamente as credenciais no código-fonte.

### testar_ligacao.py

Permite validar a conectividade entre Python e MySQL sem utilizar o Postman.

O script foi utilizado durante a configuração inicial e a investigação de incidentes.

---

## 2. Tecnologias Utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Linguagem de programação |
| FastAPI | Desenvolvimento da API REST |
| Pydantic | Validação dos dados |
| Uvicorn | Servidor ASGI |
| MySQL | Persistência dos pedidos |
| MySQL Connector/Python | Comunicação Python–MySQL |
| python-dotenv | Carregamento de variáveis de ambiente |

---

## 3. Arquitetura da Aplicação

O fluxo principal de comunicação é:

    Cliente HTTP (Postman)
             |
             v
        FastAPI
        main.py
             |
             v
     Validação Pydantic
             |
             v
        database.py
             |
             v
           MySQL
             |
             v
      Resposta HTTP/JSON

A aplicação recebe requisições HTTP, valida os dados necessários, executa operações na base de dados e devolve respostas JSON.

---

## 4. Endpoints Implementados

| Método | Endpoint | Descrição | HTTP esperado |
|---|---|---|---|
| GET | `/health` | Verificação básica da API | 200 |
| GET | `/pedidos` | Listagem dos pedidos | 200 |
| GET | `/pedidos/{pedido_id}` | Consulta de um pedido específico | 200 ou 404 |
| POST | `/pedidos` | Criação de um pedido | 201 ou 422 |

### GET /health

Permite confirmar que a aplicação HTTP está operacional.

Exemplo de resposta:

    {
      "status": "ok",
      "message": "API em funcionamento"
    }

Este endpoint não realiza necessariamente uma verificação da conectividade com a base de dados.

### GET /pedidos

Consulta os pedidos armazenados no MySQL e devolve uma lista JSON.

A implementação utiliza uma consulta SQL para recuperar os registos existentes.

### GET /pedidos/{pedido_id}

Permite consultar um pedido através do seu identificador.

Quando o pedido é encontrado, a API devolve HTTP 200.

Quando o identificador não corresponde a um pedido existente, devolve HTTP 404.

Exemplo:

    {
      "detail": "Pedido não encontrado"
    }

### POST /pedidos

Recebe dados JSON, valida os campos e cria um pedido na tabela MySQL.

Exemplo:

    {
      "cliente": "Cliente API",
      "produto": "Webcam",
      "quantidade": 1,
      "estado": "pendente"
    }

Após a inserção e confirmação da transação, a API devolve HTTP 201 Created.

---

## 5. Validação dos Dados

O projeto utiliza Pydantic para validar o conteúdo enviado nas requisições POST.

### Modelo NovoPedido

| Campo | Tipo | Regra |
|---|---|---|
| cliente | string | Entre 1 e 100 caracteres |
| produto | string | Entre 1 e 100 caracteres |
| quantidade | integer | Valor superior a zero |
| estado | string | Entre 1 e 30 caracteres; padrão `pendente` |

Quando uma requisição contém dados que não satisfazem as regras, o FastAPI devolve HTTP 422.

Por exemplo, uma quantidade igual a `-2` é rejeitada antes da execução do INSERT.

---

## 6. Integração com MySQL

A comunicação com a base de dados utiliza o MySQL Connector/Python.

As informações de ligação são configuradas através das seguintes variáveis:

    DB_HOST
    DB_PORT
    DB_NAME
    DB_USER
    DB_PASSWORD

O ficheiro `.env` contém os valores utilizados no ambiente local e não deve ser publicado.

### Operações Implementadas

- SELECT para consultar pedidos.
- INSERT para criar pedidos.
- Consultas parametrizadas para reduzir riscos de injeção SQL.
- `commit()` para confirmar inserções.
- Encerramento das ligações e cursores após as operações.

### Segurança

Foi criado um utilizador específico para o laboratório, com permissões limitadas sobre a base de dados da aplicação.

A utilização de credenciais próprias permite separar o acesso da aplicação das contas administrativas do MySQL.

---

## 7. Tratamento de Erros

A aplicação implementa tratamentos básicos para diferentes situações:

| HTTP | Situação |
|---|---|
| 200 | Consulta realizada com sucesso |
| 201 | Pedido criado com sucesso |
| 404 | Pedido não encontrado |
| 422 | Dados inválidos enviados na requisição |
| 503 | Indisponibilidade ou falha de acesso à base de dados |

### Exemplo de HTTP 503

Quando ocorre uma falha de comunicação com o MySQL, a aplicação pode devolver:

    {
      "detail": "Serviço de base de dados indisponível"
    }

O tratamento de erros evita expor diretamente ao cliente os detalhes internos da ligação à base de dados.

O laboratório ainda poderá ser melhorado com a implementação de logs estruturados e mecanismos adicionais de monitorização.

---

## 8. Execução da Aplicação

Os comandos devem ser executados na raiz do projeto, onde se encontram as pastas `api` e `database`.

### Instalar Dependências

Com o ambiente virtual ativado:

    python -m pip install -r requirements.txt

### Testar a Ligação MySQL

    python -m api.testar_ligacao

Este comando valida a comunicação com a base de dados e permite consultar o número de pedidos disponíveis.

### Iniciar a API

    python -m uvicorn api.main:app --host 127.0.0.1 --port 8000

Após a inicialização, a API fica disponível em:

`http://127.0.0.1:8000`

### Documentação Interativa

O FastAPI disponibiliza documentação Swagger UI em:

`http://127.0.0.1:8000/docs`

### Encerrar a Aplicação

No terminal onde o Uvicorn está em execução, pressionar:

    Ctrl + C

---

## 9. Investigação de Incidentes

O código desta pasta foi utilizado em dois incidentes técnicos documentados.

### INC-API-001 — Falha de Autenticação MySQL

Durante a configuração inicial, ocorreu um erro MySQL 1045 relacionado com autenticação.

A correção incluiu a criação de um utilizador específico para a aplicação e a atualização das configurações de ligação.

**Relatório:** [INC-API-001.md](../Relatorios/INC-API-001.md)

### INC-API-002 — Indisponibilidade da Base de Dados

Foi simulada uma falha de conectividade MySQL através da configuração temporária de uma porta incorreta.

A investigação envolveu:

- Diagnóstico do erro MySQL 2003.
- Reprodução de HTTP 503.
- Verificação das variáveis de ambiente.
- Identificação de conflito na porta HTTP 8000.
- Recuperação do serviço.
- Validação final com HTTP 200 e três testes automáticos aprovados.

**Relatório:** [INC-API-002.md](../Relatorios/INC-API-002.md)

---

## 10. Testes e Validação

A aplicação foi testada através de requisições manuais e scripts automáticos no Postman.

Os testes verificaram:

- Disponibilidade do serviço HTTP.
- Consulta de pedidos.
- Pesquisa por identificador.
- Tratamento de pedidos inexistentes.
- Criação e persistência de registos.
- Rejeição de dados inválidos.
- Comportamento em situações de indisponibilidade do MySQL.

### Resultados

- 8 testes HTTP manuais documentados.
- 18 verificações automáticas aprovadas individualmente.
- 2 incidentes investigados e resolvidos.

**Coleção Postman:** [API de Gestão de Pedidos](../Postman/API_Gestao_de_Pedidos.postman_collection.json)

**Evidências:** [Pasta Evidencias](../Evidencias)

---

## 11. Competências Demonstradas

Este módulo do projeto demonstra competências em:

- Desenvolvimento de APIs REST.
- Python e FastAPI.
- Validação de dados com Pydantic.
- Integração entre aplicações e bases de dados.
- Operações SQL parametrizadas.
- Gestão de ligações MySQL.
- Tratamento básico de erros HTTP.
- Diagnóstico de conectividade.
- Investigação de incidentes aplicacionais.
- Testes de APIs através do Postman.

---

## Documentação Relacionada

- [README principal do projeto](../README.md)
- [Scripts SQL](../database)
- [Coleção Postman](../Postman)
- [Relatórios técnicos](../Relatorios)
- [Evidências](../Evidencias)

---

## Nota

Este código foi desenvolvido num ambiente local e controlado, utilizando dados fictícios, para fins educativos e de demonstração de competências.
