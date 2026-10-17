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
- Validar a persistência dos dados na base de dados.
- Diagnosticar falhas de autenticação e ligação ao MySQL.
- Aplicar o princípio do menor privilégio.
- Validar consultas de recursos existentes e inexistentes.
- Investigar erros HTTP 400, 401, 403, 404, 422 e 500.
- Analisar logs e identificar causas de falhas.
- Validar correções através de novos testes.
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

O laboratório simula uma aplicação de comércio eletrónico que utiliza uma API REST para consultar e criar pedidos fictícios de clientes.

A arquitetura é composta por três componentes principais:

1. **Postman:** envia requisições HTTP, analisa respostas e organiza testes.
2. **FastAPI:** recebe as requisições, valida dados e executa a lógica da aplicação.
3. **MySQL:** armazena e disponibiliza os pedidos através de operações SQL.

### Fluxo de Comunicação

    Postman
       |
       | Requisição HTTP
       v
    FastAPI (Python)
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

A integração foi validada através de consultas GET e da criação de um pedido através do método POST.

---

## Desenvolvimento da API

Foi desenvolvida uma API REST em Python utilizando FastAPI e o servidor Uvicorn.

### Funcionalidades Implementadas

- Inicialização da aplicação FastAPI.
- Configuração do servidor local Uvicorn.
- Implementação do endpoint GET `/health`.
- Implementação do endpoint GET `/pedidos`.
- Implementação do endpoint GET `/pedidos/{pedido_id}`.
- Implementação do endpoint POST `/pedidos`.
- Validação de dados recebidos através do Pydantic.
- Respostas estruturadas em JSON.
- Ligação à base de dados MySQL.
- Consultas SQL através da aplicação Python.
- Utilização de consultas SQL parametrizadas.
- Inserção de novos pedidos no MySQL.
- Confirmação de transações através de `commit()`.
- Recuperação de identificadores gerados automaticamente.
- Tratamento de pedidos inexistentes com HTTP 404.
- Tratamento básico de erros MySQL com HTTP 503.
- Testes HTTP realizados através do Postman.

### Endpoints Disponíveis

| Método | Endpoint | Descrição | Estado |
|---|---|---|---|
| GET | `/health` | Verificação básica da API | Implementado |
| GET | `/pedidos` | Consulta de todos os pedidos | Implementado |
| GET | `/pedidos/{pedido_id}` | Consulta de um pedido pelo identificador | Implementado |
| POST | `/pedidos` | Criação de novo pedido no MySQL | Implementado |

### Endpoint GET /health

**Endereço:** `http://127.0.0.1:8000/health`

**Resposta esperada:**

    {
      "status": "ok",
      "message": "API em funcionamento"
    }

O endpoint confirma que a aplicação está a responder a requisições HTTP, mas não verifica automaticamente a conectividade com a base de dados.

### Endpoint GET /pedidos

**Endereço:** `http://127.0.0.1:8000/pedidos`

Este endpoint estabelece ligação ao MySQL e consulta os pedidos armazenados na tabela `pedidos`.

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

Os registos são devolvidos em formato JSON.

### Endpoint GET /pedidos/{pedido_id}

**Exemplo:** `http://127.0.0.1:8000/pedidos/2`

Este endpoint permite consultar um pedido específico através do seu identificador.

Utiliza uma consulta SQL parametrizada:

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

Quando o pedido não existe, devolve HTTP 404 Not Found:

    {
      "detail": "Pedido não encontrado"
    }

O comportamento foi validado através dos testes TESTE-GET-005 e TESTE-GET-006.

### Endpoint POST /pedidos

**Endereço:** `http://127.0.0.1:8000/pedidos`

Este endpoint permite criar novos pedidos através de uma requisição HTTP POST.

A API recebe dados em formato JSON e utiliza um modelo Pydantic para validar os campos antes da inserção.

#### Exemplo de Requisição

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

Após a execução da instrução SQL, a aplicação confirma a transação através de `commit()`.

O identificador gerado pelo MySQL é recuperado através de `lastrowid`.

#### Exemplo de Resposta

**HTTP 201 Created**

    {
      "id": 6,
      "cliente": "Cliente API",
      "produto": "Webcam",
      "quantidade": 1,
      "estado": "pendente",
      "message": "Pedido criado com sucesso"
    }

O comportamento foi validado através do TESTE-POST-007.

A persistência do registo foi posteriormente confirmada no MySQL Workbench.

### Validação de Dados

O modelo Pydantic utilizado no endpoint POST define:

- `cliente`: texto obrigatório, com 1 a 100 caracteres.
- `produto`: texto obrigatório, com 1 a 100 caracteres.
- `quantidade`: número inteiro superior a zero.
- `estado`: texto com 1 a 30 caracteres, cujo valor padrão é `pendente`.

As regras serão testadas em cenários de dados inválidos nas próximas etapas do laboratório.

**Código-fonte:** [api/main.py](api/main.py)

---

## Integração Python + MySQL

Foi implementada e validada a comunicação entre Python e a base de dados `api_troubleshooting_lab`.

A integração utiliza `mysql-connector-python` e configurações carregadas através de `python-dotenv`.

### Ficheiros de Integração

- [database.py](api/database.py) — estabelece a ligação ao MySQL.
- [testar_ligacao.py](api/testar_ligacao.py) — testa a ligação e executa uma consulta SQL.
- [main.py](api/main.py) — disponibiliza os endpoints HTTP.
- [requirements.txt](requirements.txt) — regista as dependências Python.
- [.env.example](.env.example) — apresenta as variáveis necessárias à configuração.
- [.gitignore](.gitignore) — define ficheiros excluídos do controlo de versões.

### Segurança da Ligação

Foi criado um utilizador MySQL específico para a aplicação:

`api_suporte@localhost`

Foram atribuídas permissões limitadas à base de dados do laboratório:

    GRANT SELECT, INSERT, UPDATE
    ON api_troubleshooting_lab.*
    TO 'api_suporte'@'localhost';

Esta configuração permite executar operações autorizadas sem utilizar permanentemente a conta administrativa `root`.

As credenciais são guardadas no ficheiro `.env`, mantido fora do repositório público.

### Validação da Ligação

Foi executado o comando:

    python -m api.testar_ligacao

**Resultado obtido na validação inicial:**

    Ligação ao MySQL estabelecida com sucesso.
    Total de pedidos encontrados: 5

Posteriormente, a ligação foi utilizada nos endpoints GET e POST da API.

### Validação de Escrita

A API executou uma operação INSERT através do endpoint POST `/pedidos`.

O pedido recebeu o identificador 6 e a operação foi confirmada através de `commit()`.

A consulta posterior ao MySQL confirmou que o registo foi armazenado.

**Estado:** Integração de leitura e escrita funcional e validada.

---

## Base de Dados MySQL

O laboratório utiliza uma base de dados relacional MySQL para armazenar pedidos fictícios.

### Estrutura

- **Base de dados:** `api_troubleshooting_lab`
- **Tabela:** `pedidos`
- **SGBD:** MySQL 8.0
- **Ferramenta de administração:** MySQL Workbench

### Tabela pedidos

| Campo | Tipo | Descrição |
|---|---|---|
| id | INT | Identificador único do pedido |
| cliente | VARCHAR(100) | Nome fictício do cliente |
| produto | VARCHAR(100) | Produto associado ao pedido |
| quantidade | INT | Quantidade de unidades |
| estado | VARCHAR(30) | Estado do pedido |
| data_criacao | TIMESTAMP | Data e hora de criação |

### Regras de Integridade

- Chave primária no campo `id`.
- Identificador com incremento automático.
- Campos obrigatórios definidos com `NOT NULL`.
- Estado inicial padrão `pendente`.
- Restrição `CHECK` para impedir quantidades inferiores ou iguais a zero.
- Registo automático da data de criação.

### Dados de Teste

Foram inseridos inicialmente cinco pedidos fictícios através de SQL.

| ID | Cliente | Produto | Quantidade | Estado |
|---|---|---|---|---|
| 1 | Cliente Teste | Notebook | 1 | pendente |
| 2 | Maria Silva | Monitor | 2 | enviado |
| 3 | Joao Santos | Teclado | 3 | entregue |
| 4 | Ana Costa | Rato Wireless | 1 | pendente |
| 5 | Pedro Almeida | Impressora | 1 | cancelado |

Posteriormente, foi criado um sexto pedido através da API.

| ID | Cliente | Produto | Quantidade | Estado |
|---|---|---|---|---|
| 6 | Cliente API | Webcam | 1 | pendente |

**Total de pedidos após o TESTE-POST-007:** 6.

### Scripts SQL

- [01_criar_estrutura.sql](database/01_criar_estrutura.sql) — criação da base de dados e da tabela.
- [02_inserir_dados.sql](database/02_inserir_dados.sql) — inserção dos cinco pedidos iniciais.

**Nota:** o script de inserção inicial não deve ser repetido numa base já preenchida, para evitar duplicações.

### Evidências MySQL

- [Criação da tabela pedidos](Evidencias/MYSQL_CRIACAO_TABELA_PEDIDOS.png)
- [Inserção dos cinco pedidos iniciais](Evidencias/MYSQL_INSERCAO_PEDIDOS.png)
- [Validação do pedido criado via API](Evidencias/MYSQL_VALIDACAO_POST_PEDIDO_ID_6.png)

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

O teste confirmou o envio e a receção de dados JSON numa API pública.

Não houve armazenamento dos dados numa base de dados.

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

O teste confirmou a consulta dos pedidos inicialmente armazenados no MySQL através da API.

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
- **Pedido devolvido:** ID 2 — Maria Silva
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

O teste confirmou que a API devolve a resposta adequada quando um pedido não existe.

O código HTTP 404 representa o comportamento esperado neste cenário.

**Relatório:** [TESTE-GET-006.md](Relatorios/TESTE-GET-006.md)

**Evidência:** [GET_PEDIDO_INEXISTENTE_404.png](Evidencias/GET_PEDIDO_INEXISTENTE_404.png)

### TESTE-POST-007 — Criação de Pedido com Persistência MySQL

- **Método:** POST
- **Endpoint:** `http://127.0.0.1:8000/pedidos`
- **Resultado:** HTTP 201 Created
- **Tempo:** 488 ms
- **Tamanho:** 257 B
- **Novo identificador:** 6
- **Cliente:** Cliente API
- **Produto:** Webcam
- **Quantidade:** 1
- **Estado do pedido:** pendente
- **Estado do teste:** Aprovado

O teste confirmou que a API recebeu os dados JSON, executou uma operação SQL INSERT e criou um novo pedido na base MySQL.

A gravação foi validada através de uma consulta SQL posterior no MySQL Workbench.

O processo demonstrou a integração entre Postman, FastAPI e MySQL para operações de escrita.

**Relatório:** [TESTE-POST-007.md](Relatorios/TESTE-POST-007.md)

**Evidências:**

- [POST_PEDIDO_201_CREATED.png](Evidencias/POST_PEDIDO_201_CREATED.png)
- [MYSQL_VALIDACAO_POST_PEDIDO_ID_6.png](Evidencias/MYSQL_VALIDACAO_POST_PEDIDO_ID_6.png)

---

## Investigação de Incidentes

### INC-API-001 — Falha de Autenticação MySQL

**Categoria:** Autenticação na base de dados

**Estado:** Resolvido e validado.

#### Descrição

Durante a configuração da ligação entre Python e MySQL, foi identificada uma falha de autenticação que impedia o acesso à base `api_troubleshooting_lab`.

#### Erro Identificado

- **Tipo:** ProgrammingError
- **Código MySQL:** 1045
- **SQLSTATE:** 28000
- **Significado:** Acesso recusado pelo servidor MySQL.

#### Diagnóstico

A configuração inicial utilizava a conta administrativa `root`, sem uma palavra-passe definida no ficheiro `.env`.

As credenciais utilizadas não foram aceites pelo servidor.

A investigação incluiu a verificação da conta autenticada no MySQL Workbench, a análise da configuração Python e a identificação do código de erro.

#### Correção Aplicada

Foi criado o utilizador `api_suporte`, com credenciais próprias e permissões limitadas de SELECT, INSERT e UPDATE.

As configurações locais foram atualizadas para utilizar a nova conta.

#### Validação

Após a correção, o teste devolveu:

    Ligação ao MySQL estabelecida com sucesso.
    Total de pedidos encontrados: 5

A consulta confirmou que a aplicação conseguiu autenticar-se e aceder aos dados.

**Conclusão:** Incidente resolvido e correção validada.

**Relatório:** [INC-API-001.md](Relatorios/INC-API-001.md)

**Evidência:** [MYSQL_ERRO_1045_CORRECAO.png](Evidencias/MYSQL_ERRO_1045_CORRECAO.png)

### Validação do Comportamento HTTP 404

O teste TESTE-GET-006 demonstrou que a ausência de um pedido pode originar uma resposta HTTP 404 legítima.

O comportamento foi previsto na aplicação e não foi classificado como incidente.

**Relatório:** [TESTE-GET-006.md](Relatorios/TESTE-GET-006.md)

### Cenários Planeados

| Cenário | Comportamento a investigar | HTTP previsto |
|---|---|---|
| Quantidade inválida | Erro de validação | 422 |
| Dados obrigatórios ausentes | Erro de validação | 422 |
| Falha de autenticação na API | Credenciais inválidas | 401 |
| Permissão insuficiente | Acesso proibido | 403 |
| Falha de comunicação com MySQL | Serviço indisponível | 503 |
| Erro interno não tratado | Falha de processamento | 500 |

Os códigos dependerão dos mecanismos de validação e tratamento de erros implementados.

Cada investigação incluirá o registo do problema, os resultados esperados e observados, a análise técnica, a causa identificada, a correção e a validação.

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
    |   |-- MYSQL_CRIACAO_TABELA_PEDIDOS.png
    |   |-- MYSQL_INSERCAO_PEDIDOS.png
    |   |-- MYSQL_ERRO_1045_CORRECAO.png
    |   |-- MYSQL_VALIDACAO_POST_PEDIDO_ID_6.png
    |
    |-- Relatorios/
    |   |-- TESTE-GET-001.md
    |   |-- TESTE-POST-002.md
    |   |-- TESTE-GET-003.md
    |   |-- TESTE-GET-004.md
    |   |-- TESTE-GET-005.md
    |   |-- TESTE-GET-006.md
    |   |-- TESTE-POST-007.md
    |   |-- INC-API-001.md
    |
    |-- .env.example
    |-- .gitignore
    |-- requirements.txt
    |-- README.md

O ficheiro `.env` verdadeiro e o ambiente virtual `.venv` permanecem locais e não fazem parte do repositório.

---

## Configuração do Ambiente

### Requisitos

- Python compatível com as dependências do projeto.
- MySQL Server 8.0.
- MySQL Workbench para administração.
- Postman para testes HTTP.

### 1. Criar o Ambiente Virtual

Na pasta principal do projeto:

    python -m venv .venv

Ativar no Windows PowerShell:

    .\.venv\Scripts\Activate.ps1

### 2. Instalar as Dependências

    python -m pip install -r requirements.txt

### 3. Preparar a Base de Dados

No MySQL Workbench:

1. Estabelecer ligação ao MySQL.
2. Executar `database/01_criar_estrutura.sql`.
3. Numa base inicialmente vazia, executar `database/02_inserir_dados.sql`.
4. Confirmar a existência dos cinco pedidos iniciais.
5. Configurar um utilizador com as permissões necessárias.

O sexto pedido foi criado posteriormente através do endpoint POST e não está incluído no script inicial.

### 4. Configurar as Variáveis de Ambiente

Criar um ficheiro `.env` na pasta principal com base em `.env.example`.

Exemplo:

    DB_HOST=127.0.0.1
    DB_PORT=3306
    DB_NAME=api_troubleshooting_lab
    DB_USER=seu_utilizador_mysql
    DB_PASSWORD=sua_palavra_passe

Não publicar credenciais reais.

### 5. Testar a Ligação

    python -m api.testar_ligacao

O número de pedidos apresentado dependerá dos registos existentes na base de dados.

### 6. Executar a API

    python -m uvicorn api.main:app --reload

A aplicação ficará disponível em:

`http://127.0.0.1:8000`

### Endpoints

- `GET http://127.0.0.1:8000/health`
- `GET http://127.0.0.1:8000/pedidos`
- `GET http://127.0.0.1:8000/pedidos/2`
- `GET http://127.0.0.1:8000/pedidos/999`
- `POST http://127.0.0.1:8000/pedidos`

Documentação interativa:

`http://127.0.0.1:8000/docs`

Para interromper o servidor, pressionar `Ctrl + C` no terminal.

**Nota:** cada POST bem-sucedido cria um novo registo. Evitar executar repetidamente os testes de criação sem necessidade.

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
- [x] Validação do Health Check no Postman.
- [x] Criação da base de dados MySQL.
- [x] Criação da tabela `pedidos`.
- [x] Implementação de restrições de integridade.
- [x] Inserção de cinco pedidos fictícios.
- [x] Validação dos registos através de SQL.
- [x] Publicação dos scripts SQL.
- [x] Instalação do MySQL Connector/Python.
- [x] Configuração das variáveis de ambiente.
- [x] Criação de utilizador MySQL com permissões limitadas.
- [x] Validação da ligação Python–MySQL.
- [x] Diagnóstico e resolução do incidente INC-API-001.
- [x] Implementação do endpoint GET `/pedidos`.
- [x] Validação da consulta dos pedidos no Postman.
- [x] Implementação do endpoint GET `/pedidos/{pedido_id}`.
- [x] Validação da consulta de pedido existente.
- [x] Validação da resposta HTTP 404.
- [x] Implementação do endpoint POST `/pedidos`.
- [x] Validação da criação do pedido com HTTP 201.
- [x] Confirmação da persistência do pedido no MySQL.
- [x] Documentação do TESTE-POST-007.
- [x] Publicação do código e das evidências no GitHub.
- [x] Organização dos relatórios no Google Drive e no Notion.

### Próximas Etapas

- [ ] Testar validações HTTP 422 com dados inválidos.
- [ ] Confirmar que pedidos inválidos não são gravados no MySQL.
- [ ] Criar testes automáticos no Postman.
- [ ] Implementar tratamento estruturado de erros e logs.
- [ ] Simular cenários HTTP 401 e 403.
- [ ] Investigar falhas de comunicação com MySQL.
- [ ] Documentar causas, correções e validações.
- [ ] Exportar e publicar a coleção Postman.
- [ ] Rever as instruções de execução.
- [ ] Realizar a revisão final do portfólio.

---

## Competências Trabalhadas

- Testes de APIs REST com Postman.
- Comunicação HTTP e interpretação de JSON.
- Desenvolvimento de APIs com FastAPI.
- Modelação e validação de dados com Pydantic.
- Execução de aplicações Python com Uvicorn.
- Criação e configuração de bases de dados MySQL.
- Inserção e consulta de dados relacionais.
- Integração Python–MySQL.
- Desenvolvimento de endpoints GET e POST.
- Utilização de consultas SQL parametrizadas.
- Criação e confirmação de transações.
- Validação da persistência de dados.
- Interpretação de respostas HTTP 200, 201 e 404.
- Diagnóstico de erros de autenticação MySQL.
- Gestão básica de utilizadores e permissões.
- Aplicação do princípio do menor privilégio.
- Utilização de variáveis de ambiente.
- Elaboração de relatórios de testes e incidentes.
- Organização de código e evidências no GitHub.

---

## Nota

Este projeto utiliza exclusivamente dados fictícios e foi desenvolvido para fins educativos e de demonstração de competências técnicas em Suporte Aplicacional Júnior.

Os resultados correspondem a testes realizados num ambiente local e controlado e não representam um sistema empresarial em produção.
