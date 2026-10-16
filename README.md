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
- Diagnosticar falhas de autenticação e ligação à base de dados.
- Aplicar o princípio do menor privilégio.
- Validar consultas de recursos existentes e inexistentes.
- Simular e investigar erros HTTP 400, 401, 403, 404 e 500.
- Analisar logs e identificar causas de falhas.
- Validar correções através de novos testes.
- Documentar procedimentos, resultados e evidências técnicas.

---

## Tecnologias e Ferramentas

- Python
- FastAPI
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

O laboratório simula uma aplicação de comércio eletrónico que utiliza uma API REST para consultar pedidos fictícios de clientes.

A arquitetura é composta por três componentes principais:

1. **Postman:** envia requisições HTTP, analisa respostas e organiza testes.
2. **FastAPI:** recebe as requisições e executa a lógica da aplicação.
3. **MySQL:** armazena os pedidos e permite consultar os dados através de SQL.

### Fluxo de Comunicação

    Postman
       |
       | Requisição HTTP
       v
    FastAPI (Python)
       |
       | Consulta SQL
       v
    MySQL
       |
       | Dados dos pedidos
       v
    FastAPI
       |
       | Resposta HTTP / JSON
       v
    Postman

A integração foi validada através dos endpoints `GET /pedidos` e `GET /pedidos/{pedido_id}`.

---

## Desenvolvimento da API

Foi desenvolvida uma API REST em Python utilizando FastAPI e o servidor Uvicorn.

### Funcionalidades Implementadas

- Inicialização da aplicação FastAPI.
- Configuração do servidor local Uvicorn.
- Implementação do endpoint GET `/health`.
- Implementação do endpoint GET `/pedidos`.
- Implementação do endpoint GET `/pedidos/{pedido_id}`.
- Respostas estruturadas em JSON.
- Ligação à base de dados MySQL.
- Consultas SQL através da aplicação Python.
- Utilização de consultas SQL parametrizadas.
- Tratamento de pedidos inexistentes com HTTP 404.
- Tratamento básico de erros de acesso à base de dados com HTTP 503.
- Testes de comunicação HTTP através do Postman.

### Endpoints Disponíveis

| Método | Endpoint | Descrição | Estado |
|---|---|---|---|
| GET | `/health` | Verificação básica da API | Implementado |
| GET | `/pedidos` | Consulta de todos os pedidos armazenados no MySQL | Implementado |
| GET | `/pedidos/{pedido_id}` | Consulta de um pedido específico por identificador | Implementado |

### Endpoint GET /health

**Endereço:** `http://127.0.0.1:8000/health`

**Resposta esperada:**

    {
      "status": "ok",
      "message": "API em funcionamento"
    }

O endpoint permite verificar se a aplicação está a responder a requisições HTTP.

Esta verificação confirma a disponibilidade básica da aplicação, mas não valida automaticamente a conectividade com a base de dados.

### Endpoint GET /pedidos

**Endereço:** `http://127.0.0.1:8000/pedidos`

Este endpoint estabelece uma ligação ao MySQL e executa uma consulta SQL à tabela `pedidos`.

A consulta utilizada é:

    SELECT
        id,
        cliente,
        produto,
        quantidade,
        estado,
        data_criacao
    FROM pedidos
    ORDER BY id;

Os registos encontrados são devolvidos em formato JSON.

O endpoint inclui tratamento básico de erros do conector MySQL, devolvendo HTTP 503 caso seja detetada uma falha de acesso à base de dados.

### Endpoint GET /pedidos/{pedido_id}

**Exemplo:** `http://127.0.0.1:8000/pedidos/2`

Este endpoint permite consultar um pedido específico através do seu identificador.

A aplicação recebe o parâmetro `pedido_id` e executa uma consulta SQL parametrizada.

Consulta utilizada:

    SELECT
        id,
        cliente,
        produto,
        quantidade,
        estado,
        data_criacao
    FROM pedidos
    WHERE id = %s;

O resultado é obtido através do método `fetchone()`.

#### Pedido Existente

Quando o identificador corresponde a um registo existente, a API devolve HTTP 200 OK e os dados do pedido em formato JSON.

O teste com o ID 2 devolveu o pedido de Maria Silva, produto Monitor, quantidade 2 e estado enviado.

#### Pedido Inexistente

Quando o identificador não corresponde a um registo, a API devolve HTTP 404 Not Found.

**Exemplo:** `GET /pedidos/999`

Resposta:

    {
      "detail": "Pedido não encontrado"
    }

Este comportamento foi validado no Postman.

As consultas SQL parametrizadas ajudam a prevenir ataques de SQL Injection.

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

**Resultado obtido:**

    Ligação ao MySQL estabelecida com sucesso.
    Total de pedidos encontrados: 5

A consulta confirmou que o Python conseguiu autenticar-se no servidor MySQL e consultar os registos armazenados.

Posteriormente, a ligação também foi validada através dos endpoints HTTP `GET /pedidos` e `GET /pedidos/{pedido_id}`.

**Estado:** Integração funcional e validada.

---

## Base de Dados MySQL

O laboratório utiliza uma base de dados relacional MySQL para armazenar pedidos fictícios de uma aplicação de comércio eletrónico.

### Estrutura da Base de Dados

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
| estado | VARCHAR(30) | Estado atual do pedido |
| data_criacao | TIMESTAMP | Data e hora de criação |

### Regras de Integridade

A tabela foi configurada com:

- Chave primária no campo `id`.
- Identificador com incremento automático.
- Campos obrigatórios definidos com `NOT NULL`.
- Estado inicial padrão `pendente`.
- Restrição `CHECK` para impedir quantidades inferiores ou iguais a zero.
- Registo automático da data de criação.

### Dados de Teste

Foram inseridos cinco pedidos fictícios:

| ID | Cliente | Produto | Quantidade | Estado |
|---|---|---|---|---|
| 1 | Cliente Teste | Notebook | 1 | pendente |
| 2 | Maria Silva | Monitor | 2 | enviado |
| 3 | Joao Santos | Teclado | 3 | entregue |
| 4 | Ana Costa | Rato Wireless | 1 | pendente |
| 5 | Pedro Almeida | Impressora | 1 | cancelado |

Os registos foram validados através de consultas SQL no MySQL Workbench e através da API FastAPI.

### Scripts SQL

- [01_criar_estrutura.sql](database/01_criar_estrutura.sql) — criação da base de dados e da tabela.
- [02_inserir_dados.sql](database/02_inserir_dados.sql) — inserção dos pedidos fictícios e consulta de validação.

**Nota:** o script de inserção deve ser executado apenas uma vez numa base inicialmente vazia, para evitar registos duplicados.

### Evidências MySQL

- [Criação da tabela pedidos](Evidencias/MYSQL_CRIACAO_TABELA_PEDIDOS.png)
- [Inserção dos cinco pedidos](Evidencias/MYSQL_INSERCAO_PEDIDOS.png)

**Estado:** Estrutura criada, dados inseridos e consultas validadas.

---

## Testes HTTP Realizados

### TESTE-GET-001 — Verificação de Comunicação HTTP

- **Ferramenta:** Postman
- **Método:** GET
- **Endpoint:** `https://postman-echo.com/get`
- **Resultado:** HTTP 200 OK
- **Tempo de resposta:** 384 ms
- **Estado:** Aprovado

O teste confirmou que a API pública respondeu corretamente à requisição GET.

**Relatório:** [TESTE-GET-001.md](Relatorios/TESTE-GET-001.md)

**Evidência:** [GET_200_OK.png](Evidencias/GET_200_OK.png)

### TESTE-POST-002 — Verificação de Envio de Dados HTTP

- **Ferramenta:** Postman
- **Método:** POST
- **Endpoint:** `https://postman-echo.com/post`
- **Resultado:** HTTP 200 OK
- **Tempo de resposta:** 433 ms
- **Estado:** Aprovado

O teste confirmou que a API pública recebeu e devolveu corretamente os dados JSON enviados.

O Postman Echo não armazenou os dados numa base de dados.

**Relatório:** [TESTE-POST-002.md](Relatorios/TESTE-POST-002.md)

**Evidência:** [POST_200_OK.png](Evidencias/POST_200_OK.png)

### TESTE-GET-003 — Health Check da API Local

- **Ferramenta:** Postman
- **Método:** GET
- **Endpoint:** `http://127.0.0.1:8000/health`
- **Resultado:** HTTP 200 OK
- **Tempo de resposta:** 5 ms
- **Estado:** Aprovado

O teste confirmou que a API Python respondeu corretamente à requisição GET no ambiente local.

**Relatório:** [TESTE-GET-003.md](Relatorios/TESTE-GET-003.md)

**Evidência:** [GET_HEALTH_200_OK.png](Evidencias/GET_HEALTH_200_OK.png)

### TESTE-GET-004 — Consulta de Pedidos na Base MySQL

- **Ferramenta:** Postman
- **Método:** GET
- **Endpoint:** `http://127.0.0.1:8000/pedidos`
- **Base de dados:** MySQL
- **Resultado:** HTTP 200 OK
- **Tempo de resposta:** 54 ms
- **Tamanho da resposta:** 766 B
- **Total de pedidos:** 5
- **Estado:** Aprovado

O teste confirmou o funcionamento da comunicação entre Postman, FastAPI e MySQL.

A API executou uma consulta SQL à tabela `pedidos` e devolveu os cinco registos fictícios em formato JSON.

**Relatório:** [TESTE-GET-004.md](Relatorios/TESTE-GET-004.md)

**Evidências:**

- [GET_PEDIDOS_MYSQL_200_OK_01.png](Evidencias/GET_PEDIDOS_MYSQL_200_OK_01.png)
- [GET_PEDIDOS_MYSQL_200_OK_02.png](Evidencias/GET_PEDIDOS_MYSQL_200_OK_02.png)

### TESTE-GET-005 — Consulta de Pedido por ID

- **Ferramenta:** Postman
- **Método:** GET
- **Endpoint:** `http://127.0.0.1:8000/pedidos/2`
- **Base de dados:** MySQL
- **Resultado:** HTTP 200 OK
- **Tempo de resposta:** 109 ms
- **Tamanho da resposta:** 251 B
- **Pedido devolvido:** ID 2 — Maria Silva
- **Estado:** Aprovado

O teste confirmou que a API consegue consultar um pedido específico através do identificador fornecido na URL.

Foi utilizada uma consulta SQL parametrizada para recuperar o registo de ID 2.

A resposta JSON devolveu os dados correspondentes ao pedido existente no MySQL.

**Relatório:** [TESTE-GET-005.md](Relatorios/TESTE-GET-005.md)

**Evidência:** [GET_PEDIDO_ID_200_OK.png](Evidencias/GET_PEDIDO_ID_200_OK.png)

### TESTE-GET-006 — Consulta de Pedido Inexistente (HTTP 404)

- **Ferramenta:** Postman
- **Método:** GET
- **Endpoint:** `http://127.0.0.1:8000/pedidos/999`
- **Base de dados:** MySQL
- **Resultado:** HTTP 404 Not Found
- **Tempo de resposta:** 116 ms
- **Tamanho da resposta:** 169 B
- **Mensagem:** Pedido não encontrado
- **Estado:** Aprovado

O teste confirmou que a API identifica corretamente a ausência de um pedido na base de dados.

Quando o identificador não corresponde a um registo, o endpoint devolve HTTP 404 e uma mensagem JSON adequada.

Neste cenário, HTTP 404 representa o comportamento esperado da aplicação, e não uma falha técnica.

**Relatório:** [TESTE-GET-006.md](Relatorios/TESTE-GET-006.md)

**Evidência:** [GET_PEDIDO_INEXISTENTE_404.png](Evidencias/GET_PEDIDO_INEXISTENTE_404.png)

---

## Investigação de Incidentes

### INC-API-001 — Falha de Autenticação MySQL

**Categoria:** Autenticação na base de dados

**Ambiente:** Python + MySQL

**Estado:** Resolvido e validado.

#### Descrição

Durante a configuração da ligação entre Python e MySQL, foi identificada uma falha de autenticação que impedia a consulta à base `api_troubleshooting_lab`.

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

Foi criado o utilizador `api_suporte`, com credenciais próprias e permissões limitadas de `SELECT`, `INSERT` e `UPDATE` na base de dados do laboratório.

As configurações locais foram atualizadas para utilizar a nova conta.

#### Validação

Após a correção, o teste devolveu:

    Ligação ao MySQL estabelecida com sucesso.
    Total de pedidos encontrados: 5

A consulta confirmou que a aplicação Python conseguiu autenticar-se e aceder aos dados.

**Conclusão:** Incidente resolvido e correção validada.

**Relatório:** [INC-API-001.md](Relatorios/INC-API-001.md)

**Evidência:** [Erro MySQL 1045 e correção](Evidencias/MYSQL_ERRO_1045_CORRECAO.png)

### Validação do Comportamento HTTP 404

O teste `TESTE-GET-006` demonstrou que a ausência de um pedido pode originar uma resposta HTTP 404 legítima.

O comportamento foi previsto e implementado na aplicação, não sendo classificado como incidente.

**Relatório relacionado:** [TESTE-GET-006.md](Relatorios/TESTE-GET-006.md)

### Incidentes Planeados

Os próximos cenários serão simulados num ambiente controlado.

| Cenário | Falha a investigar | Código HTTP previsto |
|---|---|---|
| Envio de dados inválidos | Erro de validação | 400/422 |
| Falha de autenticação na API | Credenciais inválidas | 401 |
| Permissão insuficiente | Acesso proibido | 403 |
| Falha de comunicação com MySQL | Erro interno ou indisponibilidade | 500/503 |

Os códigos apresentados dependerão do tratamento de erros implementado.

Cada investigação incluirá:

1. Identificação e descrição do incidente.
2. Registo do comportamento esperado e observado.
3. Reprodução da falha.
4. Análise de respostas HTTP, logs e consultas SQL.
5. Identificação da causa.
6. Aplicação da correção.
7. Validação através de novos testes.
8. Registo das evidências e conclusão técnica.

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
    |   |-- MYSQL_CRIACAO_TABELA_PEDIDOS.png
    |   |-- MYSQL_INSERCAO_PEDIDOS.png
    |   |-- MYSQL_ERRO_1045_CORRECAO.png
    |
    |-- Relatorios/
    |   |-- TESTE-GET-001.md
    |   |-- TESTE-POST-002.md
    |   |-- TESTE-GET-003.md
    |   |-- TESTE-GET-004.md
    |   |-- TESTE-GET-005.md
    |   |-- TESTE-GET-006.md
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
- MySQL Workbench, opcional para administração.
- Postman para testes HTTP.

### 1. Criar o Ambiente Virtual

Na pasta principal do projeto:

    python -m venv .venv

Ativar o ambiente no Windows PowerShell:

    .\.venv\Scripts\Activate.ps1

### 2. Instalar as Dependências

    python -m pip install -r requirements.txt

As dependências incluem FastAPI, Uvicorn, MySQL Connector/Python e python-dotenv.

### 3. Preparar a Base de Dados

No MySQL Workbench:

1. Estabelecer ligação ao servidor MySQL.
2. Executar `database/01_criar_estrutura.sql`.
3. Numa base inicialmente vazia, executar `database/02_inserir_dados.sql`.
4. Confirmar a existência dos cinco pedidos fictícios.
5. Configurar um utilizador com as permissões necessárias.

### 4. Configurar as Variáveis de Ambiente

Criar um ficheiro `.env` na pasta principal com base em `.env.example`.

Configurar os valores de ligação ao MySQL:

    DB_HOST=127.0.0.1
    DB_PORT=3306
    DB_NAME=api_troubleshooting_lab
    DB_USER=seu_utilizador_mysql
    DB_PASSWORD=sua_palavra_passe

O utilizador configurado deve ter permissões adequadas sobre a base de dados do laboratório.

Não publicar o ficheiro `.env` com credenciais reais.

### 5. Testar a Ligação ao MySQL

Executar:

    python -m api.testar_ligacao

Numa base com os cinco registos de teste, o resultado esperado é:

    Ligação ao MySQL estabelecida com sucesso.
    Total de pedidos encontrados: 5

### 6. Executar a API

Na pasta principal do projeto:

    python -m uvicorn api.main:app --reload

A aplicação ficará disponível em:

`http://127.0.0.1:8000`

### Endpoints Disponíveis

- `GET http://127.0.0.1:8000/health`
- `GET http://127.0.0.1:8000/pedidos`
- `GET http://127.0.0.1:8000/pedidos/2`
- `GET http://127.0.0.1:8000/pedidos/999`

Os dois últimos endereços permitem testar os cenários HTTP 200 e HTTP 404.

Documentação interativa:

`http://127.0.0.1:8000/docs`

Para interromper o servidor, pressionar `Ctrl + C` no terminal.

---

## Estado do Projeto

### Atividades Concluídas

- [x] Configuração do Postman.
- [x] Teste HTTP GET numa API pública.
- [x] Teste HTTP POST com dados JSON.
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
- [x] Validação da consulta dos cinco pedidos no Postman.
- [x] Documentação do TESTE-GET-004 e respetivas evidências.
- [x] Implementação do endpoint GET `/pedidos/{pedido_id}`.
- [x] Validação da consulta de um pedido existente.
- [x] Validação da resposta HTTP 404 para pedido inexistente.
- [x] Documentação dos testes TESTE-GET-005 e TESTE-GET-006.
- [x] Publicação do código e das evidências no GitHub.
- [x] Organização dos relatórios no Google Drive e no Notion.

### Próximas Etapas

- [ ] Implementar POST `/pedidos`.
- [ ] Validar a persistência de novos pedidos através da API.
- [ ] Criar testes automáticos no Postman.
- [ ] Implementar tratamento estruturado de erros e logs.
- [ ] Simular incidentes HTTP 400, 401, 403 e 500.
- [ ] Investigar falhas de comunicação com MySQL.
- [ ] Documentar causas, correções e validações.
- [ ] Exportar e publicar a coleção Postman.
- [ ] Rever as instruções de execução.
- [ ] Realizar a revisão final do portfólio.

---

## Competências Trabalhadas

- Testes de APIs REST com Postman.
- Comunicação HTTP e interpretação de JSON.
- Desenvolvimento básico de APIs com FastAPI.
- Execução de aplicações Python com Uvicorn.
- Criação e configuração de bases de dados MySQL.
- Inserção e consulta de dados relacionais.
- Integração Python–MySQL.
- Desenvolvimento de endpoints HTTP com consultas SQL.
- Utilização de consultas SQL parametrizadas.
- Tratamento de recursos inexistentes com HTTP 404.
- Diagnóstico de erros de autenticação.
- Interpretação de códigos MySQL e SQLSTATE.
- Gestão básica de utilizadores e permissões.
- Aplicação do princípio do menor privilégio.
- Utilização de variáveis de ambiente.
- Validação de correções técnicas.
- Elaboração de relatórios de testes e incidentes.
- Organização de código e evidências no GitHub.

---

## Nota

Este projeto utiliza exclusivamente dados fictícios e foi desenvolvido para fins educativos e de demonstração de competências técnicas em Suporte Aplicacional Júnior.

Os resultados correspondem a testes realizados num ambiente local e controlado e não representam um sistema empresarial em produção.
