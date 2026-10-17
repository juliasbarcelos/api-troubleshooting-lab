# API Troubleshooting Lab

## Sobre o Projeto

Este projeto apresenta um laboratório prático de testes, diagnóstico e investigação de incidentes em APIs REST, desenvolvido com foco nas atividades de Suporte Aplicacional Júnior.

O laboratório combina testes HTTP realizados no Postman, desenvolvimento de uma API REST em Python com FastAPI, integração com MySQL e validações automáticas com JavaScript.

O objetivo é desenvolver competências de diagnóstico técnico, interpretação de respostas HTTP, análise de erros, consultas SQL, identificação de causas, resolução de problemas e documentação de incidentes aplicacionais.

O projeto utiliza um cenário fictício de comércio eletrónico, permitindo reproduzir e investigar falhas num ambiente local e controlado.

**Estado do projeto:** Em desenvolvimento.

---

## Objetivos

- Executar e analisar requisições HTTP GET e POST.
- Interpretar códigos de estado HTTP e respostas JSON.
- Desenvolver uma API REST utilizando Python e FastAPI.
- Implementar e consultar uma base de dados MySQL.
- Integrar endpoints HTTP com operações SQL.
- Criar novos pedidos e validar a persistência dos dados.
- Verificar a rejeição de dados inválidos.
- Implementar testes automáticos com JavaScript no Postman.
- Validar respostas HTTP 200, 201, 404 e 422.
- Diagnosticar falhas de autenticação e ligação ao MySQL.
- Aplicar o princípio do menor privilégio.
- Investigar cenários de indisponibilidade e erros aplicacionais.
- Analisar logs e identificar causas de falhas.
- Documentar procedimentos, resultados e evidências técnicas.

---

## Tecnologias e Ferramentas

- Python
- FastAPI
- Pydantic
- Uvicorn
- MySQL 8.0
- MySQL Workbench
- MySQL Connector/Python
- python-dotenv
- Postman
- JavaScript
- SQL
- HTTP e APIs REST
- JSON
- Visual Studio Code
- GitHub

---

## Cenário do Laboratório

O laboratório simula uma aplicação de comércio eletrónico que utiliza uma API REST para consultar e criar pedidos fictícios.

A arquitetura é composta por três componentes principais:

1. **Postman:** envia requisições HTTP, analisa respostas e executa testes automáticos.
2. **FastAPI:** recebe as requisições, valida dados e executa a lógica da aplicação.
3. **MySQL:** armazena e disponibiliza os pedidos através de operações SQL.

### Fluxo de Comunicação

    Postman
       |
       | Requisição HTTP
       v
    FastAPI (Python + Pydantic)
       |
       | SELECT / INSERT
       v
    MySQL
       |
       | Resultados
       v
    FastAPI
       |
       | Resposta HTTP / JSON
       v
    Postman
       |
       | Testes automáticos JavaScript
       v
    Resultados de validação

Quando os dados recebidos não respeitam as regras definidas, o FastAPI pode rejeitar a requisição antes de executar operações na base de dados.

---

## Desenvolvimento da API

Foi desenvolvida uma API REST em Python utilizando FastAPI e o servidor Uvicorn.

### Funcionalidades Implementadas

- Inicialização da aplicação FastAPI.
- Configuração do servidor Uvicorn.
- Endpoint GET `/health`.
- Endpoint GET `/pedidos`.
- Endpoint GET `/pedidos/{pedido_id}`.
- Endpoint POST `/pedidos`.
- Validação de dados através do Pydantic.
- Respostas estruturadas em JSON.
- Ligação à base de dados MySQL.
- Consultas e inserções SQL parametrizadas.
- Confirmação de transações através de `commit()`.
- Recuperação de identificadores gerados pelo MySQL.
- Tratamento de pedidos inexistentes com HTTP 404.
- Rejeição de dados inválidos com HTTP 422.
- Tratamento básico de erros MySQL com HTTP 503.
- Testes HTTP manuais e automáticos através do Postman.

### Endpoints Disponíveis

| Método | Endpoint | Descrição | Estado |
|---|---|---|---|
| GET | `/health` | Verificação básica da API | Implementado |
| GET | `/pedidos` | Consulta de todos os pedidos | Implementado |
| GET | `/pedidos/{pedido_id}` | Consulta de um pedido por ID | Implementado |
| POST | `/pedidos` | Criação de um pedido no MySQL | Implementado |

### GET /health

**Endpoint:** `http://127.0.0.1:8000/health`

Resposta esperada:

    {
      "status": "ok",
      "message": "API em funcionamento"
    }

Este endpoint verifica a disponibilidade básica da aplicação, mas não confirma automaticamente a conectividade com o MySQL.

### GET /pedidos

**Endpoint:** `http://127.0.0.1:8000/pedidos`

Consulta SQL utilizada:

    SELECT
        id,
        cliente,
        produto,
        quantidade,
        estado,
        data_criacao
    FROM pedidos
    ORDER BY id;

Os pedidos armazenados no MySQL são devolvidos em formato JSON.

### GET /pedidos/{pedido_id}

**Exemplo:** `http://127.0.0.1:8000/pedidos/2`

Consulta SQL parametrizada:

    SELECT
        id,
        cliente,
        produto,
        quantidade,
        estado,
        data_criacao
    FROM pedidos
    WHERE id = %s;

Quando o pedido existe, a API devolve HTTP 200 OK.

Quando não existe, devolve HTTP 404 Not Found:

    {
      "detail": "Pedido não encontrado"
    }

Este comportamento foi validado através dos testes TESTE-GET-005 e TESTE-GET-006.

### POST /pedidos

**Endpoint:** `http://127.0.0.1:8000/pedidos`

Permite criar pedidos através de requisições HTTP POST.

A API recebe dados JSON, valida os campos através do Pydantic e executa uma inserção na tabela MySQL.

#### Exemplo de Requisição Válida

    {
      "cliente": "Cliente API",
      "produto": "Webcam",
      "quantidade": 1,
      "estado": "pendente"
    }

#### Operação SQL

    INSERT INTO pedidos
        (cliente, produto, quantidade, estado)
    VALUES (%s, %s, %s, %s);

Após o INSERT, a aplicação executa `commit()` e recupera o identificador gerado através de `lastrowid`.

#### Exemplo de Resposta — HTTP 201 Created

    {
      "id": 6,
      "cliente": "Cliente API",
      "produto": "Webcam",
      "quantidade": 1,
      "estado": "pendente",
      "message": "Pedido criado com sucesso"
    }

A persistência do pedido foi confirmada no MySQL Workbench durante o TESTE-POST-007.

### Validação de Dados com Pydantic

O endpoint POST utiliza um modelo Pydantic para definir regras de validação:

| Campo | Regra |
|---|---|
| cliente | Texto obrigatório, entre 1 e 100 caracteres |
| produto | Texto obrigatório, entre 1 e 100 caracteres |
| quantidade | Número inteiro superior a zero |
| estado | Texto de 1 a 30 caracteres; padrão `pendente` |

A quantidade utiliza a restrição `gt=0`.

#### Exemplo de Requisição Inválida

    {
      "cliente": "Cliente Teste Invalido",
      "produto": "Webcam",
      "quantidade": -2,
      "estado": "pendente"
    }

O valor `-2` viola a regra de validação.

#### Resposta HTTP 422

O FastAPI rejeitou a requisição e identificou:

- Tipo de erro: `greater_than`.
- Campo inválido: `body → quantidade`.
- Valor recebido: `-2`.
- Mensagem: `Input should be greater than 0`.

A validação ocorreu antes da execução da função responsável pelo INSERT.

Uma consulta posterior ao MySQL confirmou que o pedido inválido não foi armazenado.

**Código-fonte:** [api/main.py](api/main.py)

---

## Integração Python + MySQL

Foi implementada a comunicação entre Python e a base de dados `api_troubleshooting_lab`.

A integração utiliza `mysql-connector-python` e configurações carregadas através de `python-dotenv`.

### Ficheiros

- [database.py](api/database.py) — ligação ao MySQL.
- [testar_ligacao.py](api/testar_ligacao.py) — teste de conectividade e consulta SQL.
- [main.py](api/main.py) — endpoints da API.
- [requirements.txt](requirements.txt) — dependências Python.
- [.env.example](.env.example) — exemplo de configuração.
- [.gitignore](.gitignore) — ficheiros excluídos do controlo de versões.

### Segurança

Foi criado o utilizador MySQL:

`api_suporte@localhost`

Com permissões limitadas:

    GRANT SELECT, INSERT, UPDATE
    ON api_troubleshooting_lab.*
    TO 'api_suporte'@'localhost';

As credenciais são mantidas no ficheiro `.env`, que não deve ser publicado no GitHub.

Esta configuração evita a utilização da conta administrativa `root` pela aplicação.

### Validação Inicial da Ligação

Comando executado:

    python -m api.testar_ligacao

Resultado inicial:

    Ligação ao MySQL estabelecida com sucesso.
    Total de pedidos encontrados: 5

Posteriormente, a integração foi validada através dos endpoints GET e POST.

### Validação da Escrita

O TESTE-POST-007 criou o pedido de ID 6.

A gravação foi confirmada no MySQL Workbench.

### Validação da Rejeição

O TESTE-POST-008 enviou uma quantidade negativa.

O FastAPI devolveu HTTP 422 e a consulta posterior ao MySQL não encontrou o pedido inválido.

### Validação Automatizada

Durante os testes automáticos do POST, foi criado o pedido de ID 7.

Uma consulta posterior ao MySQL confirmou a persistência do registo.

**Estado:** Integração de leitura, escrita e validação funcional.

---

## Base de Dados MySQL

### Estrutura

- **Base:** `api_troubleshooting_lab`
- **Tabela:** `pedidos`
- **SGBD:** MySQL 8.0
- **Administração:** MySQL Workbench

### Tabela pedidos

| Campo | Tipo | Descrição |
|---|---|---|
| id | INT | Identificador único |
| cliente | VARCHAR(100) | Nome fictício do cliente |
| produto | VARCHAR(100) | Produto |
| quantidade | INT | Quantidade |
| estado | VARCHAR(30) | Estado do pedido |
| data_criacao | TIMESTAMP | Data e hora de criação |

### Regras de Integridade

- Chave primária.
- Identificador automático.
- Campos obrigatórios com `NOT NULL`.
- Estado padrão `pendente`.
- Restrição `CHECK (quantidade > 0)`.
- Data de criação automática.

### Dados Iniciais

| ID | Cliente | Produto | Quantidade | Estado |
|---|---|---|---|---|
| 1 | Cliente Teste | Notebook | 1 | pendente |
| 2 | Maria Silva | Monitor | 2 | enviado |
| 3 | Joao Santos | Teclado | 3 | entregue |
| 4 | Ana Costa | Rato Wireless | 1 | pendente |
| 5 | Pedro Almeida | Impressora | 1 | cancelado |

### Pedidos Criados Através da API

| ID | Cliente | Produto | Quantidade | Estado | Origem |
|---|---|---|---|---|---|
| 6 | Cliente API | Webcam | 1 | pendente | Teste manual |
| 7 | Cliente API | Webcam | 1 | pendente | Teste automático |

**Total de pedidos após os testes de criação:** 7.

A quantidade negativa utilizada no TESTE-POST-008 não originou novos registos.

### Scripts SQL

- [01_criar_estrutura.sql](database/01_criar_estrutura.sql)
- [02_inserir_dados.sql](database/02_inserir_dados.sql)

O script de inserção inicial não deve ser executado repetidamente numa base já preenchida.

### Evidências

- [Criação da tabela](Evidencias/MYSQL_CRIACAO_TABELA_PEDIDOS.png)
- [Inserção dos pedidos iniciais](Evidencias/MYSQL_INSERCAO_PEDIDOS.png)
- [Persistência do pedido ID 6](Evidencias/MYSQL_VALIDACAO_POST_PEDIDO_ID_6.png)
- [Ausência de inserção inválida](Evidencias/MYSQL_VALIDACAO_SEM_INSERCAO_422.png)
- [Persistência do pedido ID 7](Evidencias/AUTO_MYSQL_PEDIDO_ID_7.png)

---

## Testes HTTP Manuais Realizados

### TESTE-GET-001 — Verificação de Comunicação HTTP

- **Método:** GET
- **Endpoint:** `https://postman-echo.com/get`
- **Resultado:** HTTP 200 OK
- **Tempo:** 384 ms
- **Estado:** Aprovado

**Relatório:** [TESTE-GET-001.md](Relatorios/TESTE-GET-001.md)

**Evidência:** [GET_200_OK.png](Evidencias/GET_200_OK.png)

### TESTE-POST-002 — Envio de Dados HTTP

- **Método:** POST
- **Endpoint:** `https://postman-echo.com/post`
- **Resultado:** HTTP 200 OK
- **Tempo:** 433 ms
- **Estado:** Aprovado

O Postman Echo recebeu e devolveu os dados JSON, sem os armazenar numa base de dados.

**Relatório:** [TESTE-POST-002.md](Relatorios/TESTE-POST-002.md)

**Evidência:** [POST_200_OK.png](Evidencias/POST_200_OK.png)

### TESTE-GET-003 — Health Check da API

- **Método:** GET
- **Endpoint:** `http://127.0.0.1:8000/health`
- **Resultado:** HTTP 200 OK
- **Tempo:** 5 ms
- **Estado:** Aprovado

**Relatório:** [TESTE-GET-003.md](Relatorios/TESTE-GET-003.md)

**Evidência:** [GET_HEALTH_200_OK.png](Evidencias/GET_HEALTH_200_OK.png)

### TESTE-GET-004 — Consulta de Pedidos no MySQL

- **Método:** GET
- **Endpoint:** `http://127.0.0.1:8000/pedidos`
- **Resultado:** HTTP 200 OK
- **Tempo:** 54 ms
- **Tamanho:** 766 B
- **Pedidos devolvidos:** 5
- **Estado:** Aprovado

**Relatório:** [TESTE-GET-004.md](Relatorios/TESTE-GET-004.md)

**Evidências:**

- [GET_PEDIDOS_MYSQL_200_OK_01.png](Evidencias/GET_PEDIDOS_MYSQL_200_OK_01.png)
- [GET_PEDIDOS_MYSQL_200_OK_02.png](Evidencias/GET_PEDIDOS_MYSQL_200_OK_02.png)

### TESTE-GET-005 — Consulta de Pedido por ID

- **Método:** GET
- **Endpoint:** `http://127.0.0.1:8000/pedidos/2`
- **Resultado:** HTTP 200 OK
- **Tempo:** 109 ms
- **Tamanho:** 251 B
- **Pedido:** ID 2 — Maria Silva
- **Estado:** Aprovado

**Relatório:** [TESTE-GET-005.md](Relatorios/TESTE-GET-005.md)

**Evidência:** [GET_PEDIDO_ID_200_OK.png](Evidencias/GET_PEDIDO_ID_200_OK.png)

### TESTE-GET-006 — Pedido Inexistente

- **Método:** GET
- **Endpoint:** `http://127.0.0.1:8000/pedidos/999`
- **Resultado:** HTTP 404 Not Found
- **Tempo:** 116 ms
- **Tamanho:** 169 B
- **Mensagem:** Pedido não encontrado
- **Estado:** Aprovado

**Relatório:** [TESTE-GET-006.md](Relatorios/TESTE-GET-006.md)

**Evidência:** [GET_PEDIDO_INEXISTENTE_404.png](Evidencias/GET_PEDIDO_INEXISTENTE_404.png)

### TESTE-POST-007 — Criação de Pedido com Persistência MySQL

- **Método:** POST
- **Endpoint:** `http://127.0.0.1:8000/pedidos`
- **Resultado:** HTTP 201 Created
- **Tempo:** 488 ms
- **Tamanho:** 257 B
- **ID criado:** 6
- **Cliente:** Cliente API
- **Produto:** Webcam
- **Estado:** Aprovado

A API criou um novo pedido e a sua persistência foi confirmada no MySQL.

**Relatório:** [TESTE-POST-007.md](Relatorios/TESTE-POST-007.md)

**Evidências:**

- [POST_PEDIDO_201_CREATED.png](Evidencias/POST_PEDIDO_201_CREATED.png)
- [MYSQL_VALIDACAO_POST_PEDIDO_ID_6.png](Evidencias/MYSQL_VALIDACAO_POST_PEDIDO_ID_6.png)

### TESTE-POST-008 — Validação de Quantidade Inválida

- **Método:** POST
- **Endpoint:** `http://127.0.0.1:8000/pedidos`
- **Resultado:** HTTP 422 Unprocessable Entity
- **Tempo:** 12 ms
- **Tamanho:** 276 B
- **Quantidade enviada:** -2
- **Tipo de erro:** `greater_than`
- **Campo inválido:** `quantidade`
- **Registos encontrados no MySQL:** 0
- **Estado:** Aprovado

O teste confirmou que a API rejeitou uma quantidade negativa através do Pydantic.

Uma consulta posterior ao MySQL confirmou que o pedido inválido não foi armazenado.

**Relatório:** [TESTE-POST-008.md](Relatorios/TESTE-POST-008.md)

**Evidências:**

- [POST_QUANTIDADE_INVALIDA_422.png](Evidencias/POST_QUANTIDADE_INVALIDA_422.png)
- [MYSQL_VALIDACAO_SEM_INSERCAO_422.png](Evidencias/MYSQL_VALIDACAO_SEM_INSERCAO_422.png)

---

## Testes Automáticos no Postman

Foram implementados testes automáticos em JavaScript para validar os principais comportamentos da API de Gestão de Pedidos.

Os scripts foram configurados na secção `Scripts > After response` do Postman, utilizando `pm.test()` e `pm.expect()`.

### Metodologia

Os testes foram adicionados às requisições da coleção `API de Gestão de Pedidos`.

Cada script verifica automaticamente condições específicas da resposta recebida.

Foram realizadas execuções individuais das requisições e analisados os resultados apresentados no separador `Test Results`.

### Resumo dos Resultados

| Requisição | HTTP | Testes aprovados |
|---|---|---|
| GET /health | 200 OK | 2/2 |
| GET /pedidos | 200 OK | 3/3 |
| GET /pedidos/2 | 200 OK | 3/3 |
| GET /pedidos/999 | 404 Not Found | 3/3 |
| POST /pedidos — quantidade inválida | 422 | 3/3 |
| POST /pedidos — criação válida | 201 Created | 4/4 |
| **Total** | | **18/18** |

**Resultado:** 18 verificações automáticas aprovadas nas execuções individuais.

### GET /health — HTTP 200

**Testes:** 2/2 aprovados.

Validações:

- Confirmar HTTP 200.
- Confirmar que o campo `status` apresenta `ok`.

**Tempo observado:** 8 ms.

**Evidência:** [AUTO_GET_HEALTH_200.png](Evidencias/AUTO_GET_HEALTH_200.png)

### GET /pedidos — HTTP 200

**Testes:** 3/3 aprovados.

Validações:

- Confirmar HTTP 200.
- Confirmar que a resposta é uma lista JSON.
- Confirmar que existem pelo menos seis pedidos.

**Tempo observado:** 119 ms.

**Evidência:** [AUTO_GET_PEDIDOS_200.png](Evidencias/AUTO_GET_PEDIDOS_200.png)

### GET /pedidos/2 — HTTP 200

**Testes:** 3/3 aprovados.

Validações:

- Confirmar HTTP 200.
- Confirmar que o ID devolvido é 2.
- Confirmar os dados de Maria Silva, produto Monitor, quantidade 2 e estado enviado.

**Tempo observado:** 124 ms.

**Evidência:** [AUTO_GET_PEDIDO_ID_200.png](Evidencias/AUTO_GET_PEDIDO_ID_200.png)

### GET /pedidos/999 — HTTP 404

**Testes:** 3/3 aprovados.

Validações:

- Confirmar HTTP 404.
- Confirmar a mensagem `Pedido não encontrado`.
- Confirmar que a resposta é um objeto JSON.

**Tempo observado:** 117 ms.

**Evidência:** [AUTO_GET_PEDIDO_404.png](Evidencias/AUTO_GET_PEDIDO_404.png)

O código HTTP 404 foi considerado um resultado aprovado porque corresponde ao comportamento esperado.

### POST /pedidos — Quantidade Inválida (HTTP 422)

**Testes:** 3/3 aprovados.

Validações:

- Confirmar HTTP 422.
- Confirmar que o erro está relacionado com o campo `quantidade`.
- Confirmar que o valor inválido identificado é `-2`.

**Tempo observado:** 5 ms.

**Evidências:**

- [AUTO_POST_INVALIDO_422_01.png](Evidencias/AUTO_POST_INVALIDO_422_01.png)
- [AUTO_POST_INVALIDO_422_02.png](Evidencias/AUTO_POST_INVALIDO_422_02.png)

O Pydantic rejeitou os dados inválidos antes da execução da função responsável pela inserção.

### POST /pedidos — Criação Válida (HTTP 201)

**Testes:** 4/4 aprovados.

Validações:

- Confirmar HTTP 201 Created.
- Confirmar que o pedido recebeu um identificador numérico positivo.
- Confirmar a mensagem `Pedido criado com sucesso`.
- Confirmar que os dados devolvidos correspondem aos enviados.

**Tempo observado:** 110 ms.

O teste criou um pedido com os seguintes dados:

| Campo | Valor |
|---|---|
| ID | 7 |
| Cliente | Cliente API |
| Produto | Webcam |
| Quantidade | 1 |
| Estado | pendente |

A gravação foi posteriormente confirmada no MySQL Workbench.

**Evidências:**

- [AUTO_POST_CRIACAO_201_01.png](Evidencias/AUTO_POST_CRIACAO_201_01.png)
- [AUTO_POST_CRIACAO_201_02.png](Evidencias/AUTO_POST_CRIACAO_201_02.png)
- [AUTO_MYSQL_PEDIDO_ID_7.png](Evidencias/AUTO_MYSQL_PEDIDO_ID_7.png)

### Análise Técnica

Os testes automáticos validaram:

- Códigos HTTP esperados.
- Estrutura das respostas JSON.
- Conteúdo e valores devolvidos.
- Consulta de pedidos existentes.
- Tratamento de pedidos inexistentes.
- Validação de quantidades inválidas.
- Criação de pedidos.
- Persistência de dados no MySQL.

As respostas HTTP 404 e 422 foram consideradas aprovadas porque representam comportamentos esperados nos respetivos cenários.

O POST válido foi executado de forma controlada, uma vez que cada requisição bem-sucedida cria um novo registo.

### Limitações

Os testes foram executados individualmente.

Ainda não foi realizada uma execução automatizada de toda a coleção através do Collection Runner.

A validação de quantidade mínima de pedidos depende dos dados existentes na base local.

Os testes de criação modificam a base de dados e devem ser executados de forma controlada.

### Conclusão

Foram implementadas e aprovadas 18 verificações automáticas distribuídas por seis requisições HTTP.

**Estado:** Aprovado nas execuções individuais.

**Relatório técnico:** [TESTES-AUTOMATICOS-001.md](Relatorios/TESTES-AUTOMATICOS-001.md)

---

## Investigação de Incidentes

### INC-API-001 — Falha de Autenticação MySQL

**Categoria:** Autenticação na base de dados.

**Estado:** Resolvido e validado.

#### Descrição

Durante a configuração da ligação Python–MySQL, foi identificada uma falha de autenticação que impedia o acesso à base de dados do laboratório.

#### Erro Identificado

- **Tipo:** ProgrammingError
- **Código MySQL:** 1045
- **SQLSTATE:** 28000
- **Significado:** Acesso recusado pelo servidor MySQL.

#### Diagnóstico

A configuração inicial utilizava a conta `root` sem uma palavra-passe definida no ficheiro `.env`.

As credenciais utilizadas não foram aceites pelo servidor.

A investigação incluiu a verificação da conta autenticada no MySQL Workbench, a análise da configuração Python e a identificação do código de erro.

#### Correção

Foi criado o utilizador `api_suporte`, com credenciais próprias e permissões limitadas.

A configuração local foi atualizada para utilizar essa conta.

#### Validação

A ligação passou a funcionar e a consulta SQL devolveu os cinco pedidos inicialmente inseridos.

**Conclusão:** Incidente resolvido e correção validada.

**Relatório:** [INC-API-001.md](Relatorios/INC-API-001.md)

**Evidência:** [MYSQL_ERRO_1045_CORRECAO.png](Evidencias/MYSQL_ERRO_1045_CORRECAO.png)

### Respostas HTTP Esperadas

Os testes também permitiram validar respostas HTTP que não representam incidentes técnicos:

- **404 Not Found:** pedido inexistente.
- **422 Unprocessable Entity:** dados inválidos.

Ambos os comportamentos foram previstos na aplicação e validados no Postman.

### Cenários Planeados

| Cenário | Código HTTP previsto |
|---|---|
| Campos obrigatórios ausentes | 422 |
| Outros dados inválidos | 422 |
| Falha de autenticação na API | 401 |
| Permissões insuficientes | 403 |
| Base de dados indisponível | 503 |
| Erro interno não tratado | 500 |

Os cenários ainda não executados serão desenvolvidos e investigados nas próximas etapas.

---

## Estrutura do Repositório

    api-troubleshooting-lab/
    |
    |-- api/
    |   |-- main.py
    |   |-- database.py
    |   |-- testar_ligacao.py
    |
    |-- database/
    |   |-- 01_criar_estrutura.sql
    |   |-- 02_inserir_dados.sql
    |
    |-- Evidencias/
    |   |-- GET_200_OK.png
    |   |-- POST_200_OK.png
    |   |-- GET_HEALTH_200_OK.png
    |   |-- GET_PEDIDOS_MYSQL_200_OK_01.png
    |   |-- GET_PEDIDOS_MYSQL_200_OK_02.png
    |   |-- GET_PEDIDO_ID_200_OK.png
    |   |-- GET_PEDIDO_INEXISTENTE_404.png
    |   |-- POST_PEDIDO_201_CREATED.png
    |   |-- POST_QUANTIDADE_INVALIDA_422.png
    |   |-- MYSQL_CRIACAO_TABELA_PEDIDOS.png
    |   |-- MYSQL_INSERCAO_PEDIDOS.png
    |   |-- MYSQL_ERRO_1045_CORRECAO.png
    |   |-- MYSQL_VALIDACAO_POST_PEDIDO_ID_6.png
    |   |-- MYSQL_VALIDACAO_SEM_INSERCAO_422.png
    |   |-- AUTO_GET_HEALTH_200.png
    |   |-- AUTO_GET_PEDIDOS_200.png
    |   |-- AUTO_GET_PEDIDO_ID_200.png
    |   |-- AUTO_GET_PEDIDO_404.png
    |   |-- AUTO_POST_INVALIDO_422_01.png
    |   |-- AUTO_POST_INVALIDO_422_02.png
    |   |-- AUTO_POST_CRIACAO_201_01.png
    |   |-- AUTO_POST_CRIACAO_201_02.png
    |   |-- AUTO_MYSQL_PEDIDO_ID_7.png
    |
    |-- Relatorios/
    |   |-- TESTE-GET-001.md
    |   |-- TESTE-POST-002.md
    |   |-- TESTE-GET-003.md
    |   |-- TESTE-GET-004.md
    |   |-- TESTE-GET-005.md
    |   |-- TESTE-GET-006.md
    |   |-- TESTE-POST-007.md
    |   |-- TESTE-POST-008.md
    |   |-- TESTES-AUTOMATICOS-001.md
    |   |-- INC-API-001.md
    |
    |-- .env.example
    |-- .gitignore
    |-- requirements.txt
    |-- README.md

O ficheiro `.env` verdadeiro e o ambiente virtual `.venv` permanecem locais e não devem ser publicados.

---

## Configuração do Ambiente

### Requisitos

- Python compatível com as dependências do projeto.
- MySQL Server 8.0.
- MySQL Workbench.
- Postman.

### 1. Criar o Ambiente Virtual

Na pasta principal do projeto:

    python -m venv .venv

Ativar no Windows PowerShell:

    .\.venv\Scripts\Activate.ps1

### 2. Instalar as Dependências

    python -m pip install -r requirements.txt

### 3. Preparar a Base de Dados

No MySQL Workbench:

1. Executar `database/01_criar_estrutura.sql`.
2. Numa base inicialmente vazia, executar `database/02_inserir_dados.sql`.
3. Confirmar os cinco pedidos fictícios iniciais.
4. Configurar um utilizador com as permissões necessárias.

Os pedidos de ID 6 e 7 foram criados posteriormente através da API.

### 4. Configurar o Ficheiro .env

Criar o ficheiro `.env` com base em `.env.example`.

Exemplo:

    DB_HOST=127.0.0.1
    DB_PORT=3306
    DB_NAME=api_troubleshooting_lab
    DB_USER=seu_utilizador_mysql
    DB_PASSWORD=sua_palavra_passe

Não publicar credenciais reais no GitHub.

### 5. Testar a Ligação

    python -m api.testar_ligacao

O número de pedidos apresentado dependerá dos registos existentes na base de dados.

### 6. Iniciar a API

    python -m uvicorn api.main:app --reload

A API ficará disponível em:

`http://127.0.0.1:8000`

Documentação interativa:

`http://127.0.0.1:8000/docs`

### Endpoints para Teste

- `GET http://127.0.0.1:8000/health`
- `GET http://127.0.0.1:8000/pedidos`
- `GET http://127.0.0.1:8000/pedidos/2`
- `GET http://127.0.0.1:8000/pedidos/999`
- `POST http://127.0.0.1:8000/pedidos`

Cada requisição POST válida e bem-sucedida cria um novo pedido.

---

## Estado do Projeto

### Atividades Concluídas

- [x] Configuração do Postman.
- [x] Teste HTTP GET numa API pública.
- [x] Teste HTTP POST numa API pública.
- [x] Criação da API Python com FastAPI.
- [x] Configuração do ambiente virtual.
- [x] Instalação das dependências.
- [x] Implementação de GET `/health`.
- [x] Validação do Health Check.
- [x] Criação da base de dados MySQL.
- [x] Criação da tabela `pedidos`.
- [x] Implementação de restrições de integridade.
- [x] Inserção de cinco pedidos fictícios.
- [x] Validação dos registos através de SQL.
- [x] Publicação dos scripts SQL.
- [x] Configuração da integração Python–MySQL.
- [x] Criação de utilizador MySQL com permissões limitadas.
- [x] Diagnóstico e resolução do incidente INC-API-001.
- [x] Implementação de GET `/pedidos`.
- [x] Implementação de GET `/pedidos/{pedido_id}`.
- [x] Validação da resposta HTTP 404.
- [x] Implementação de POST `/pedidos`.
- [x] Validação da criação de pedido com HTTP 201.
- [x] Confirmação da persistência no MySQL.
- [x] Validação de quantidade inválida com HTTP 422.
- [x] Confirmação de que o pedido inválido não foi armazenado.
- [x] Documentação dos testes HTTP manuais.
- [x] Implementação de testes automáticos no Postman.
- [x] Aprovação das 18 verificações automáticas.
- [x] Validação automática dos cenários HTTP 200, 201, 404 e 422.
- [x] Confirmação da persistência do pedido criado no teste automático.
- [x] Documentação dos testes em TESTES-AUTOMATICOS-001.md.
- [x] Publicação dos relatórios e evidências no GitHub.
- [x] Organização dos relatórios no Google Drive e no Notion.

### Próximas Etapas

- [ ] Testar outros campos obrigatórios e valores inválidos.
- [ ] Implementar tratamento estruturado de erros e logs.
- [ ] Investigar a indisponibilidade do MySQL e a resposta HTTP 503.
- [ ] Validar a recuperação da API após a correção.
- [ ] Documentar o novo incidente e as respetivas evidências.
- [ ] Exportar e publicar a coleção Postman.
- [ ] Preparar execuções repetíveis dos testes.
- [ ] Rever as instruções de execução.
- [ ] Realizar a revisão final do portfólio.

### Melhorias Opcionais

- [ ] Implementar autenticação e autorização na API.
- [ ] Investigar cenários HTTP 401 e 403.
- [ ] Criar uma estratégia automática de preparação e limpeza de dados de teste.
- [ ] Executar a coleção através do Postman Collection Runner.

---

## Competências Trabalhadas

- Testes manuais de APIs REST com Postman.
- Testes automáticos em JavaScript no Postman.
- Utilização de `pm.test()` e `pm.expect()`.
- Interpretação de respostas HTTP e JSON.
- Desenvolvimento de APIs com FastAPI.
- Validação de dados com Pydantic.
- Execução de aplicações Python com Uvicorn.
- Criação e configuração de bases de dados MySQL.
- Consultas e inserções SQL.
- Integração Python–MySQL.
- Desenvolvimento de endpoints GET e POST.
- Utilização de SQL parametrizado.
- Criação e confirmação de transações.
- Validação da persistência de dados.
- Verificação da rejeição de dados inválidos.
- Interpretação de códigos HTTP 200, 201, 404 e 422.
- Diagnóstico de erros de autenticação MySQL.
- Aplicação do princípio do menor privilégio.
- Utilização de variáveis de ambiente.
- Elaboração de relatórios técnicos.
- Organização de código e evidências no GitHub.

---

## Nota

Este projeto utiliza exclusivamente dados fictícios e foi desenvolvido para fins educativos e de demonstração de competências técnicas em Suporte Aplicacional Júnior.

Os resultados correspondem a testes realizados num ambiente local e controlado e não representam um sistema empresarial em produção.
