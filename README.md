# API Troubleshooting Lab

## Sobre o Projeto

Este projeto apresenta um laboratório prático de testes, diagnóstico e investigação de incidentes em APIs REST, desenvolvido com foco nas atividades de Suporte Aplicacional Júnior.

O laboratório combina testes HTTP realizados no Postman, desenvolvimento de uma API REST em Python com FastAPI e utilização de uma base de dados relacional MySQL.

O objetivo é desenvolver competências de diagnóstico técnico, interpretação de respostas HTTP, análise de erros, consultas SQL, identificação de causas, resolução de problemas e documentação de incidentes aplicacionais.

O projeto utiliza um cenário fictício de comércio eletrónico, permitindo reproduzir e investigar falhas num ambiente local e controlado.

**Estado do projeto:** Em desenvolvimento.

---

## Objetivos

- Executar e analisar requisições HTTP GET e POST.
- Interpretar códigos de estado HTTP e respostas JSON.
- Desenvolver uma API REST utilizando Python e FastAPI.
- Implementar e consultar uma base de dados MySQL.
- Integrar endpoints HTTP com consultas SQL.
- Criar novos registos através de uma API.
- Validar a persistência de dados.
- Verificar a rejeição de dados inválidos.
- Diagnosticar falhas de autenticação e ligação ao MySQL.
- Aplicar o princípio do menor privilégio.
- Investigar respostas HTTP 400, 401, 403, 404, 422, 500 e 503.
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
- SQL
- HTTP e APIs REST
- JSON
- Visual Studio Code
- GitHub

---

## Cenário do Laboratório

O laboratório simula uma aplicação de comércio eletrónico que utiliza uma API REST para consultar e criar pedidos fictícios.

A arquitetura é composta por três componentes:

1. **Postman:** envia requisições HTTP e analisa respostas.
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

Quando os dados recebidos não respeitam as regras de validação, o FastAPI pode rejeitar a requisição com HTTP 422 antes de executar operações na base de dados.

---

## Desenvolvimento da API

Foi desenvolvida uma API REST em Python utilizando FastAPI e Uvicorn.

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
- Testes HTTP realizados através do Postman.

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

Quando o identificador não corresponde a um pedido existente, devolve HTTP 404:

    {
      "detail": "Pedido não encontrado"
    }

Este comportamento foi validado através dos testes TESTE-GET-005 e TESTE-GET-006.

### POST /pedidos

**Endpoint:** `http://127.0.0.1:8000/pedidos`

Permite criar pedidos através de requisições HTTP POST.

A API recebe dados JSON, valida os campos e executa uma inserção na tabela MySQL.

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

A restrição utilizada para a quantidade é `gt=0`.

#### Exemplo de Requisição Inválida

    {
      "cliente": "Cliente Teste Invalido",
      "produto": "Webcam",
      "quantidade": -2,
      "estado": "pendente"
    }

O valor `-2` viola a regra que exige uma quantidade superior a zero.

#### Resposta — HTTP 422

O FastAPI rejeitou a requisição com HTTP 422.

A resposta identificou:

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

As credenciais são mantidas no ficheiro `.env`, que não é publicado no GitHub.

### Validação da Ligação

Comando executado:

    python -m api.testar_ligacao

Resultado obtido inicialmente:

    Ligação ao MySQL estabelecida com sucesso.
    Total de pedidos encontrados: 5

Posteriormente, a integração foi validada através de operações GET e POST.

### Validação da Escrita

O POST `/pedidos` criou um pedido com ID 6.

A gravação foi confirmada diretamente no MySQL Workbench.

### Validação da Rejeição

O teste com quantidade negativa devolveu HTTP 422.

A consulta posterior ao MySQL não encontrou o pedido inválido.

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

### Pedido Criado Através da API

| ID | Cliente | Produto | Quantidade | Estado |
|---|---|---|---|---|
| 6 | Cliente API | Webcam | 1 | pendente |

**Total após o TESTE-POST-007:** 6 pedidos.

O TESTE-POST-008 não criou novos registos.

### Scripts SQL

- [01_criar_estrutura.sql](database/01_criar_estrutura.sql)
- [02_inserir_dados.sql](database/02_inserir_dados.sql)

O script de inserção inicial não deve ser executado repetidamente numa base já preenchida.

### Evidências

- [Criação da tabela](Evidencias/MYSQL_CRIACAO_TABELA_PEDIDOS.png)
- [Inserção dos pedidos iniciais](Evidencias/MYSQL_INSERCAO_PEDIDOS.png)
- [Persistência do pedido ID 6](Evidencias/MYSQL_VALIDACAO_POST_PEDIDO_ID_6.png)
- [Validação sem inserção de pedido inválido](Evidencias/MYSQL_VALIDACAO_SEM_INSERCAO_422.png)

---

## Testes HTTP Realizados

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

### TESTE-POST-008 — Validação de Quantidade Inválida (HTTP 422)

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

O teste confirmou que a API rejeita uma quantidade negativa através da validação Pydantic.

A resposta HTTP 422 identificou o campo inválido e a regra violada.

Uma consulta posterior no MySQL Workbench confirmou que o pedido rejeitado não foi armazenado.

O resultado corresponde ao comportamento esperado.

**Relatório:** [TESTE-POST-008.md](Relatorios/TESTE-POST-008.md)

**Evidências:**

- [POST_QUANTIDADE_INVALIDA_422.png](Evidencias/POST_QUANTIDADE_INVALIDA_422.png)
- [MYSQL_VALIDACAO_SEM_INSERCAO_422.png](Evidencias/MYSQL_VALIDACAO_SEM_INSERCAO_422.png)

---

## Investigação de Incidentes

### INC-API-001 — Falha de Autenticação MySQL

**Categoria:** Autenticação na base de dados

**Estado:** Resolvido e validado.

#### Descrição

Durante a configuração da ligação Python–MySQL, foi identificada uma falha de autenticação.

#### Erro Identificado

- Tipo: ProgrammingError
- Código MySQL: 1045
- SQLSTATE: 28000
- Significado: Acesso recusado pelo servidor MySQL.

#### Diagnóstico

A configuração inicial utilizava a conta `root` sem uma palavra-passe definida no ficheiro `.env`.

As credenciais utilizadas não foram aceites.

#### Correção

Foi criado o utilizador `api_suporte`, com credenciais próprias e permissões limitadas.

A configuração local foi atualizada para utilizar essa conta.

#### Validação

A ligação passou a funcionar e a consulta SQL devolveu os cinco pedidos inicialmente inseridos.

**Relatório:** [INC-API-001.md](Relatorios/INC-API-001.md)

**Evidência:** [MYSQL_ERRO_1045_CORRECAO.png](Evidencias/MYSQL_ERRO_1045_CORRECAO.png)

### Respostas HTTP Esperadas

Os testes também permitiram validar respostas HTTP que não representam incidentes:

- **404 Not Found:** pedido inexistente.
- **422 Unprocessable Entity:** dados inválidos.

Ambos os comportamentos foram previstos na aplicação e validados através do Postman.

### Cenários Planeados

| Cenário | Código HTTP previsto |
|---|---|
| Campos obrigatórios ausentes | 422 |
| Outros dados inválidos | 422 |
| Falha de autenticação na API | 401 |
| Permissões insuficientes | 403 |
| Base de dados indisponível | 503 |
| Erro interno não tratado | 500 |

Estes cenários ainda serão desenvolvidos e investigados nas próximas etapas.

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

Na pasta principal:

    python -m venv .venv

Ativar no Windows PowerShell:

    .\.venv\Scripts\Activate.ps1

### 2. Instalar as Dependências

    python -m pip install -r requirements.txt

### 3. Preparar a Base de Dados

No MySQL Workbench:

1. Executar `database/01_criar_estrutura.sql`.
2. Numa base inicialmente vazia, executar `database/02_inserir_dados.sql`.
3. Verificar os cinco pedidos fictícios iniciais.
4. Configurar um utilizador com permissões adequadas.

O pedido de ID 6 foi criado posteriormente através da API.

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
- [x] Implementação do endpoint GET `/health`.
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
- [x] Confirmação da persistência do pedido no MySQL.
- [x] Validação de quantidade inválida com HTTP 422.
- [x] Confirmação de que o pedido inválido não foi armazenado.
- [x] Documentação do TESTE-POST-008.
- [x] Publicação dos relatórios e evidências no GitHub.
- [x] Organização dos relatórios no Google Drive e no Notion.

### Próximas Etapas

- [ ] Testar outros campos obrigatórios e valores inválidos.
- [ ] Criar testes automáticos no Postman.
- [ ] Implementar tratamento estruturado de erros e logs.
- [ ] Simular cenários HTTP 401 e 403.
- [ ] Investigar indisponibilidade do MySQL.
- [ ] Documentar novos incidentes e validações.
- [ ] Exportar e publicar a coleção Postman.
- [ ] Rever as instruções de execução.
- [ ] Realizar a revisão final do portfólio.

---

## Competências Trabalhadas

- Testes de APIs REST com Postman.
- Interpretação de respostas HTTP e JSON.
- Desenvolvimento básico de APIs com FastAPI.
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
