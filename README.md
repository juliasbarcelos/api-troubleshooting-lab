# API Troubleshooting Lab

## Sobre o Projeto

Este projeto apresenta um laboratório prático de testes, diagnóstico e investigação de incidentes em APIs REST, desenvolvido com foco nas atividades de Suporte Aplicacional Júnior.

O laboratório integra o desenvolvimento de uma API REST em Python com FastAPI, uma base de dados MySQL, testes manuais e automáticos no Postman e investigação de problemas de conectividade.

O objetivo é demonstrar competências de suporte técnico a aplicações, análise de respostas HTTP, consultas SQL, diagnóstico de incidentes, validação de dados e recuperação de serviços.

O projeto utiliza um cenário fictício de comércio eletrónico, com pedidos de clientes armazenados numa base de dados local.

**Estado:** Em desenvolvimento — funcionalidades e investigações principais concluídas.

---

## Objetivos

- Desenvolver uma API REST utilizando Python e FastAPI.
- Integrar a API com uma base de dados MySQL.
- Implementar operações de consulta e criação de pedidos.
- Executar testes HTTP com Postman.
- Interpretar respostas JSON e códigos HTTP.
- Implementar testes automáticos em JavaScript.
- Validar a persistência e integridade dos dados.
- Investigar falhas de autenticação e conectividade MySQL.
- Diagnosticar problemas de configuração e processos.
- Simular falhas HTTP 503 em ambiente controlado.
- Validar a recuperação da aplicação.
- Produzir relatórios e evidências técnicas.

---

## Tecnologias e Ferramentas

| Tecnologia | Utilização |
|---|---|
| Python | Desenvolvimento da aplicação |
| FastAPI | Implementação da API REST |
| Pydantic | Validação de dados |
| Uvicorn | Servidor ASGI |
| MySQL 8.0 | Base de dados relacional |
| MySQL Workbench | Administração e consultas SQL |
| MySQL Connector/Python | Integração Python–MySQL |
| python-dotenv | Configuração por variáveis de ambiente |
| Postman | Testes manuais e automáticos |
| JavaScript | Scripts de validação no Postman |
| PowerShell | Diagnóstico de processos e portas |
| Visual Studio Code | Desenvolvimento e execução |
| GitHub | Versionamento e documentação |

---

## Arquitetura

O laboratório é composto por três componentes principais:

1. **Postman:** envia requisições e valida respostas HTTP.
2. **FastAPI:** processa requisições, valida dados e executa operações SQL.
3. **MySQL:** armazena os pedidos fictícios.

### Fluxo de Comunicação

    Postman
       |
       | HTTP GET / POST
       v
    FastAPI + Pydantic
       |
       | SELECT / INSERT
       v
    MySQL
       |
       | Resultados
       v
    FastAPI
       |
       | HTTP + JSON
       v
    Postman
       |
       | Testes JavaScript
       v
    Resultados de validação

---

## Funcionalidades Implementadas

- Verificação básica do funcionamento da API.
- Consulta de todos os pedidos.
- Consulta de pedidos por identificador.
- Criação de pedidos com persistência MySQL.
- Validação de dados recebidos através de Pydantic.
- Tratamento de recursos inexistentes com HTTP 404.
- Rejeição de dados inválidos com HTTP 422.
- Tratamento básico de falhas MySQL com HTTP 503.
- Consultas SQL parametrizadas.
- Confirmação de transações com `commit()`.
- Utilização de variáveis de ambiente.
- Testes manuais e automáticos.

### Endpoints

| Método | Endpoint | Função |
|---|---|---|
| GET | `/health` | Verificar o funcionamento básico da API |
| GET | `/pedidos` | Listar pedidos existentes |
| GET | `/pedidos/{pedido_id}` | Consultar pedido específico |
| POST | `/pedidos` | Criar novo pedido |

### GET /health

**URL:** `http://127.0.0.1:8000/health`

Resposta:

    {
      "status": "ok",
      "message": "API em funcionamento"
    }

Este endpoint verifica a disponibilidade básica da aplicação, mas não confirma automaticamente a ligação ao MySQL.

### GET /pedidos

**URL:** `http://127.0.0.1:8000/pedidos`

Consulta SQL:

    SELECT
        id,
        cliente,
        produto,
        quantidade,
        estado,
        data_criacao
    FROM pedidos
    ORDER BY id;

A resposta apresenta os pedidos armazenados em formato JSON.

### GET /pedidos/{pedido_id}

Exemplo:

`http://127.0.0.1:8000/pedidos/2`

Utiliza uma consulta SQL parametrizada para procurar o identificador solicitado.

Quando o pedido existe, devolve HTTP 200.

Quando não existe, devolve HTTP 404:

    {
      "detail": "Pedido não encontrado"
    }

### POST /pedidos

**URL:** `http://127.0.0.1:8000/pedidos`

Recebe dados JSON e cria um novo pedido na base MySQL.

Exemplo:

    {
      "cliente": "Cliente API",
      "produto": "Webcam",
      "quantidade": 1,
      "estado": "pendente"
    }

A aplicação valida os campos através do Pydantic e executa uma operação SQL parametrizada:

    INSERT INTO pedidos
        (cliente, produto, quantidade, estado)
    VALUES (%s, %s, %s, %s);

Após a execução do INSERT, confirma a transação através de `commit()`.

A resposta apresenta HTTP 201 Created e o identificador gerado pelo MySQL.

### Regras de Validação

| Campo | Regra |
|---|---|
| cliente | Texto obrigatório, 1 a 100 caracteres |
| produto | Texto obrigatório, 1 a 100 caracteres |
| quantidade | Número inteiro superior a zero |
| estado | Texto entre 1 e 30 caracteres; padrão `pendente` |

Uma quantidade negativa é rejeitada com HTTP 422 antes da operação de inserção.

**Código-fonte:** [api/main.py](api/main.py)

---

## Base de Dados MySQL

### Estrutura

- **Base de dados:** `api_troubleshooting_lab`
- **Tabela:** `pedidos`
- **SGBD:** MySQL 8.0

### Campos

| Campo | Tipo | Descrição |
|---|---|---|
| id | INT | Identificador automático |
| cliente | VARCHAR(100) | Cliente fictício |
| produto | VARCHAR(100) | Produto |
| quantidade | INT | Quantidade |
| estado | VARCHAR(30) | Estado do pedido |
| data_criacao | TIMESTAMP | Data de criação |

### Restrições

- Chave primária no identificador.
- Incremento automático.
- Campos obrigatórios definidos com `NOT NULL`.
- Estado padrão `pendente`.
- Restrição `CHECK (quantidade > 0)`.
- Data de criação automática.

### Dados de Teste

| ID | Cliente | Produto | Quantidade | Estado |
|---|---|---|---|---|
| 1 | Cliente Teste | Notebook | 1 | pendente |
| 2 | Maria Silva | Monitor | 2 | enviado |
| 3 | Joao Santos | Teclado | 3 | entregue |
| 4 | Ana Costa | Rato Wireless | 1 | pendente |
| 5 | Pedro Almeida | Impressora | 1 | cancelado |
| 6 | Cliente API | Webcam | 1 | pendente |
| 7 | Cliente API | Webcam | 1 | pendente |

Os cinco primeiros pedidos foram inseridos através de SQL.

O pedido 6 foi criado num teste manual HTTP POST.

O pedido 7 foi criado durante a validação automática HTTP 201.

**Total após as validações realizadas:** 7 pedidos.

### Scripts SQL

- [01_criar_estrutura.sql](database/01_criar_estrutura.sql)
- [02_inserir_dados.sql](database/02_inserir_dados.sql)

O script de inserção inicial não deve ser repetido numa base já preenchida, para evitar duplicações.

---

## Integração Python–MySQL

A aplicação utiliza o módulo `api/database.py` para estabelecer ligações à base de dados.

A configuração é carregada através do ficheiro local `.env`, utilizando `python-dotenv`.

### Segurança

Foi criado um utilizador específico para o laboratório:

`api_suporte@localhost`

Com permissões limitadas:

    GRANT SELECT, INSERT, UPDATE
    ON api_troubleshooting_lab.*
    TO 'api_suporte'@'localhost';

A aplicação não necessita de utilizar permanentemente a conta administrativa `root`.

As credenciais são mantidas no ficheiro `.env`, não publicado no GitHub.

### Teste Direto da Ligação

Comando:

    python -m api.testar_ligacao

A consulta permite confirmar a conectividade e contar os pedidos armazenados.

O teste foi utilizado durante a investigação e a recuperação dos incidentes MySQL.

**Ficheiros relacionados:**

- [api/database.py](api/database.py)
- [api/testar_ligacao.py](api/testar_ligacao.py)
- [.env.example](.env.example)
- [.gitignore](.gitignore)

---

## Testes HTTP Manuais

Foram realizados oito testes manuais, identificados e documentados individualmente.

| Teste | Cenário | HTTP | Resultado |
|---|---|---|---|
| TESTE-GET-001 | GET numa API pública | 200 | Aprovado |
| TESTE-POST-002 | POST numa API pública | 200 | Aprovado |
| TESTE-GET-003 | Health Check local | 200 | Aprovado |
| TESTE-GET-004 | Listagem de pedidos MySQL | 200 | Aprovado |
| TESTE-GET-005 | Consulta de pedido por ID | 200 | Aprovado |
| TESTE-GET-006 | Pedido inexistente | 404 | Aprovado |
| TESTE-POST-007 | Criação com persistência MySQL | 201 | Aprovado |
| TESTE-POST-008 | Quantidade inválida | 422 | Aprovado |

### Relatórios

- [TESTE-GET-001.md](Relatorios/TESTE-GET-001.md)
- [TESTE-POST-002.md](Relatorios/TESTE-POST-002.md)
- [TESTE-GET-003.md](Relatorios/TESTE-GET-003.md)
- [TESTE-GET-004.md](Relatorios/TESTE-GET-004.md)
- [TESTE-GET-005.md](Relatorios/TESTE-GET-005.md)
- [TESTE-GET-006.md](Relatorios/TESTE-GET-006.md)
- [TESTE-POST-007.md](Relatorios/TESTE-POST-007.md)
- [TESTE-POST-008.md](Relatorios/TESTE-POST-008.md)

### Validação da Persistência

No TESTE-POST-007, a API criou o pedido 6 com HTTP 201.

A gravação foi confirmada no MySQL Workbench.

### Validação da Rejeição

No TESTE-POST-008, foi enviada uma quantidade negativa.

O FastAPI respondeu com HTTP 422.

Uma consulta posterior confirmou que o pedido inválido não tinha sido armazenado.

---

## Testes Automáticos no Postman

Foram implementadas verificações automáticas em JavaScript através de `pm.test()` e `pm.expect()`.

Os scripts estão configurados em `Scripts > After response` no Postman.

### Resultados

| Requisição | HTTP | Testes aprovados |
|---|---|---|
| GET /health | 200 | 2/2 |
| GET /pedidos | 200 | 3/3 |
| GET /pedidos/2 | 200 | 3/3 |
| GET /pedidos/999 | 404 | 3/3 |
| POST /pedidos — quantidade inválida | 422 | 3/3 |
| POST /pedidos — criação válida | 201 | 4/4 |
| **Total** | | **18/18** |

**Estado:** Aprovado nas execuções individuais.

### Validações Automatizadas

- Códigos HTTP esperados.
- Estrutura das respostas JSON.
- Identificadores devolvidos.
- Dados de pedidos existentes.
- Mensagem de pedido inexistente.
- Rejeição de quantidade negativa.
- Criação de um pedido válido.
- Comparação dos dados enviados e recebidos.

Durante o teste HTTP 201 foi criado o pedido 7.

A persistência foi confirmada diretamente no MySQL Workbench.

### Limitações

Os testes foram executados individualmente.

Ainda não foi realizada uma execução completa através do Postman Collection Runner.

Os testes POST válidos modificam a base de dados e precisam de ser executados de forma controlada.

**Relatório completo:** [TESTES-AUTOMATICOS-001.md](Relatorios/TESTES-AUTOMATICOS-001.md)

### Evidências

- [AUTO_GET_HEALTH_200.png](Evidencias/AUTO_GET_HEALTH_200.png)
- [AUTO_GET_PEDIDOS_200.png](Evidencias/AUTO_GET_PEDIDOS_200.png)
- [AUTO_GET_PEDIDO_ID_200.png](Evidencias/AUTO_GET_PEDIDO_ID_200.png)
- [AUTO_GET_PEDIDO_404.png](Evidencias/AUTO_GET_PEDIDO_404.png)
- [AUTO_POST_INVALIDO_422_01.png](Evidencias/AUTO_POST_INVALIDO_422_01.png)
- [AUTO_POST_INVALIDO_422_02.png](Evidencias/AUTO_POST_INVALIDO_422_02.png)
- [AUTO_POST_CRIACAO_201_01.png](Evidencias/AUTO_POST_CRIACAO_201_01.png)
- [AUTO_POST_CRIACAO_201_02.png](Evidencias/AUTO_POST_CRIACAO_201_02.png)
- [AUTO_MYSQL_PEDIDO_ID_7.png](Evidencias/AUTO_MYSQL_PEDIDO_ID_7.png)

---

## Investigação de Incidentes

Foram investigados e resolvidos dois incidentes técnicos relacionados com a integração entre Python, FastAPI e MySQL.

### INC-API-001 — Falha de Autenticação MySQL

**Categoria:** Autenticação na base de dados

**Estado:** Resolvido e validado

#### Descrição

Durante a configuração da integração Python–MySQL, foi identificada uma falha de autenticação.

#### Erro Identificado

- **Tipo:** ProgrammingError
- **Código MySQL:** 1045
- **SQLSTATE:** 28000
- **Significado:** Acesso recusado pelo servidor MySQL.

#### Diagnóstico

A configuração inicial utilizava a conta administrativa `root` com credenciais que não foram aceites pelo servidor.

#### Correção

Foi criado um utilizador específico para a aplicação, com credenciais próprias e permissões limitadas.

A configuração local foi atualizada para utilizar essa conta.

#### Validação

Após a correção, a ligação Python–MySQL foi estabelecida com sucesso e a consulta encontrou os cinco pedidos iniciais.

**Relatório:** [INC-API-001.md](Relatorios/INC-API-001.md)

**Evidência:** [MYSQL_ERRO_1045_CORRECAO.png](Evidencias/MYSQL_ERRO_1045_CORRECAO.png)

---

### INC-API-002 — Indisponibilidade da Base de Dados MySQL

**Data:** 19/10/2026

**Categoria:** Conectividade / Base de dados

**Estado:** Resolvido e validado

#### Objetivo

Simular uma falha de comunicação entre FastAPI e MySQL, verificar a resposta HTTP 503 e recuperar o serviço.

#### Estado Inicial

Antes da simulação:

- Endpoint: GET `/pedidos`
- HTTP: 200 OK
- Tempo de resposta: 129 ms
- Testes automáticos: 3/3 aprovados
- Pedidos disponíveis: 7

#### Simulação da Falha

Foi alterada temporariamente a porta MySQL no ficheiro `.env`.

**Configuração original:**

    DB_PORT=3306

**Configuração simulada:**

    DB_PORT=3399

O objetivo era provocar uma falha de comunicação sem interromper o servidor MySQL e sem modificar os dados.

#### Erro MySQL Identificado

O teste direto de ligação apresentou:

- **Tipo:** InterfaceError
- **Código MySQL:** 2003
- **SQLSTATE:** None

O erro indicou que o cliente não conseguiu estabelecer ligação ao servidor MySQL na porta configurada.

#### Diagnóstico das Variáveis de Ambiente

Durante a investigação, verificou-se o carregamento das configurações pelo `python-dotenv`.

Foi testada temporariamente a opção:

    load_dotenv(BASE_DIR / ".env", override=True)

Esta opção faz com que os valores do `.env` tenham prioridade sobre variáveis de ambiente já existentes.

Após a alteração, foi possível reproduzir o HTTP 503.

Posteriormente, o ficheiro `database.py` foi restaurado à configuração original.

A origem exata da diferença inicial de configuração entre processos não foi estabelecida de forma conclusiva.

#### Resposta HTTP 503

O Postman apresentou:

- **HTTP:** 503 Service Unavailable
- **Tempo de resposta:** 2,26 s
- **Tamanho:** 196 B
- **Testes automáticos:** 0/3 aprovados

Resposta JSON:

    {
      "detail": "Serviço de base de dados indisponível"
    }

Os testes automáticos reprovaram porque esperavam uma lista de pedidos e HTTP 200.

O comportamento confirmou que a API possuía tratamento básico para a falha de comunicação com a base de dados.

#### Restauração da Configuração MySQL

A porta original foi restaurada:

    DB_PORT=3306

O teste de ligação Python–MySQL voltou a apresentar:

    Ligação ao MySQL estabelecida com sucesso.
    Total de pedidos encontrados: 7

Contudo, o endpoint HTTP continuou temporariamente a devolver HTTP 503.

A investigação prosseguiu com a análise dos processos Uvicorn.

#### Conflito na Porta HTTP 8000

Durante o reinício do servidor, foi identificado:

    [Errno 10048] error while attempting to bind
    on address ('127.0.0.1', 8000)

O erro indicava que a porta HTTP 8000 estava ocupada.

Foram utilizados comandos PowerShell para investigar processos e ligações TCP:

    netstat -ano | findstr :8000

    Get-NetTCPConnection -LocalPort 8000 -State Listen

    Get-CimInstance Win32_Process

A porta 8000 encontrava-se associada ao PID 13080.

Posteriormente, foi identificado o processo Python 31000, cujo processo pai era o PID 13080.

#### Recuperação Temporária

Para contornar o conflito, a API foi iniciada na porta HTTP 8001:

    python -m uvicorn api.main:app --host 127.0.0.1 --port 8001

O endpoint GET `/pedidos` voltou a funcionar.

**Resultados:**

- HTTP 200 OK
- Tempo de resposta: 108 ms
- Testes automáticos: 3/3 aprovados
- Pedidos preservados: 7

#### Resolução do Conflito

Foi encerrado o processo Python residual identificado durante a investigação:

    Stop-Process -Id 31000

Após o encerramento, a porta 8000 deixou de apresentar ligações em estado LISTENING.

#### Recuperação Definitiva

A API foi iniciada novamente na porta original:

    python -m uvicorn api.main:app --host 127.0.0.1 --port 8000

O Postman confirmou:

- **HTTP:** 200 OK
- **Tempo de resposta:** 338 ms
- **Tamanho:** 1014 B
- **Testes automáticos:** 3/3 aprovados
- **Pedidos preservados:** 7

A instância temporária da porta 8001 foi encerrada após a recuperação.

#### Análise das Causas

Foram identificados dois problemas distintos:

**1. Falha simulada de conectividade MySQL**

A alteração da porta MySQL de 3306 para 3399 provocou a impossibilidade de estabelecer ligação, originando o erro MySQL 2003 e a resposta HTTP 503.

**2. Conflito na porta HTTP 8000**

Durante a recuperação, foi identificado um processo Python associado à execução anterior do servidor que impedia a utilização normal da porta 8000.

Após o encerramento do processo identificado, a porta ficou disponível e a API pôde ser iniciada novamente no endereço original.

A investigação demonstrou a importância de distinguir erros de conectividade à base de dados de problemas de gestão dos processos que executam a aplicação.

#### Evidências

- [INC-API-002_01_ESTADO_INICIAL_200.png](Evidencias/INC-API-002_01_ESTADO_INICIAL_200.png)
- [INC-API-002_02_FALHA_MYSQL_503.png](Evidencias/INC-API-002_02_FALHA_MYSQL_503.png)
- [INC-API-002_04_RECUPERACAO_FINAL_8000.png](Evidencias/INC-API-002_04_RECUPERACAO_FINAL_8000.png)

#### Conclusão

O incidente simulado foi resolvido e a recuperação da API foi validada na porta original 8000.

A aplicação voltou a responder com HTTP 200 OK e os três testes automáticos foram aprovados.

Os sete pedidos permaneceram armazenados no MySQL.

**Relatório completo:** [INC-API-002.md](Relatorios/INC-API-002.md)

**Estado final:** Resolvido e validado.

---

## Lições Aprendidas

As investigações permitiram desenvolver conhecimentos práticos sobre:

- Distinção entre erros de autenticação e conectividade.
- Interpretação dos códigos MySQL 1045 e 2003.
- Tratamento de indisponibilidade através de HTTP 503.
- Importância das variáveis de ambiente.
- Diagnóstico de processos Python.
- Identificação de conflitos de portas TCP.
- Recuperação de serviços através de validações sucessivas.
- Preservação de dados durante uma investigação.
- Utilização de testes automáticos para verificar a recuperação.

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
    |   |-- INC-API-002_01_ESTADO_INICIAL_200.png
    |   |-- INC-API-002_02_FALHA_MYSQL_503.png
    |   |-- INC-API-002_04_RECUPERACAO_FINAL_8000.png
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
    |   |-- INC-API-002.md
    |
    |-- .env.example
    |-- .gitignore
    |-- requirements.txt
    |-- README.md

O ficheiro `.env` verdadeiro e o ambiente virtual `.venv` permanecem locais e não devem ser publicados.

---

## Configuração e Execução

### Requisitos

- Python compatível com as dependências do projeto.
- MySQL Server 8.0.
- MySQL Workbench.
- Postman.

### 1. Criar o Ambiente Virtual

Na pasta principal:

    python -m venv .venv

Ativar no PowerShell:

    .\.venv\Scripts\Activate.ps1

### 2. Instalar as Dependências

    python -m pip install -r requirements.txt

### 3. Preparar a Base de Dados

No MySQL Workbench:

1. Executar `database/01_criar_estrutura.sql`.
2. Numa base inicialmente vazia, executar `database/02_inserir_dados.sql`.
3. Confirmar os cinco pedidos iniciais.
4. Configurar um utilizador com as permissões necessárias.

Os pedidos de ID 6 e 7 foram criados posteriormente através da API e não fazem parte do script de inserção inicial.

### 4. Configurar as Variáveis de Ambiente

Criar um ficheiro `.env` com base em `.env.example`.

Exemplo:

    DB_HOST=127.0.0.1
    DB_PORT=3306
    DB_NAME=api_troubleshooting_lab
    DB_USER=seu_utilizador_mysql
    DB_PASSWORD=sua_palavra_passe

Não publicar credenciais reais no GitHub.

### 5. Validar a Ligação MySQL

Executar:

    python -m api.testar_ligacao

O total apresentado depende dos dados existentes na base de dados local.

### 6. Iniciar a API

Executar:

    python -m uvicorn api.main:app --host 127.0.0.1 --port 8000

A aplicação ficará disponível em:

`http://127.0.0.1:8000`

Documentação interativa:

`http://127.0.0.1:8000/docs`

### Endpoints para Teste

- `GET http://127.0.0.1:8000/health`
- `GET http://127.0.0.1:8000/pedidos`
- `GET http://127.0.0.1:8000/pedidos/2`
- `GET http://127.0.0.1:8000/pedidos/999`
- `POST http://127.0.0.1:8000/pedidos`

Cada POST válido e bem-sucedido cria um novo pedido.

### Encerrar a Aplicação

Pressionar `Ctrl + C` no terminal onde o Uvicorn está em execução.

Evitar iniciar várias instâncias simultâneas na mesma porta.

---

## Estado do Projeto

### Atividades Concluídas

- [x] Configuração do ambiente Python.
- [x] Criação da API com FastAPI.
- [x] Configuração do Uvicorn.
- [x] Criação da base de dados MySQL.
- [x] Criação da tabela `pedidos`.
- [x] Inserção dos dados fictícios iniciais.
- [x] Integração Python–MySQL.
- [x] Configuração das variáveis de ambiente.
- [x] Criação de utilizador MySQL com permissões limitadas.
- [x] Implementação de GET `/health`.
- [x] Implementação de GET `/pedidos`.
- [x] Implementação de GET `/pedidos/{pedido_id}`.
- [x] Implementação de POST `/pedidos`.
- [x] Validação de HTTP 200.
- [x] Validação de HTTP 201.
- [x] Validação de HTTP 404.
- [x] Validação de HTTP 422.
- [x] Verificação da persistência de pedidos.
- [x] Verificação da rejeição de dados inválidos.
- [x] Documentação dos oito testes HTTP manuais.
- [x] Implementação de 18 verificações automáticas.
- [x] Validação das 18 verificações automáticas no Postman.
- [x] Investigação e resolução do INC-API-001.
- [x] Investigação e resolução do INC-API-002.
- [x] Simulação controlada de HTTP 503.
- [x] Diagnóstico do erro MySQL 2003.
- [x] Diagnóstico do conflito da porta HTTP 8000.
- [x] Recuperação da aplicação na porta original.
- [x] Confirmação de HTTP 200 e 3/3 testes após a recuperação.
- [x] Publicação dos relatórios e evidências no GitHub.
- [x] Organização da documentação no Google Drive e no Notion.

### Próximas Etapas

- [ ] Exportar e publicar a coleção Postman.
- [ ] Rever a configuração dos testes para facilitar a sua reprodução.
- [ ] Verificar os links e as evidências do repositório.
- [ ] Realizar a revisão final do README e do código.
- [ ] Concluir a apresentação do projeto no Notion.

### Melhorias Opcionais

- [ ] Testar outros campos obrigatórios e dados inválidos.
- [ ] Implementar logs estruturados.
- [ ] Implementar autenticação e autorização.
- [ ] Simular cenários HTTP 401 e 403.
- [ ] Criar preparação e limpeza automatizada de dados de teste.
- [ ] Executar a coleção através do Postman Collection Runner.

---

## Competências Demonstradas

### Desenvolvimento e Integração

- Python e FastAPI.
- Desenvolvimento de endpoints REST.
- Validação com Pydantic.
- Integração Python–MySQL.
- Consultas SQL parametrizadas.
- Criação e confirmação de transações.

### Testes e Qualidade

- Testes HTTP manuais.
- Testes automáticos com JavaScript no Postman.
- Interpretação de respostas JSON.
- Validação da persistência de dados.
- Verificação da rejeição de dados inválidos.

### Diagnóstico e Suporte Aplicacional

- Interpretação de erros MySQL 1045 e 2003.
- Análise de HTTP 404, 422 e 503.
- Diagnóstico de variáveis de ambiente.
- Investigação de problemas de conectividade.
- Identificação de processos Python.
- Análise de portas TCP através do PowerShell.
- Recuperação de serviços Uvicorn.
- Validação de correções através de testes.

### Documentação Técnica

- Elaboração de relatórios de incidentes.
- Registo de resultados esperados e obtidos.
- Organização de capturas de ecrã.
- Documentação de procedimentos de diagnóstico.
- Publicação de evidências técnicas no GitHub.

---

## Nota

Este projeto utiliza exclusivamente dados fictícios e foi desenvolvido para fins educativos e de demonstração de competências técnicas.

Os resultados correspondem a testes realizados num ambiente local e controlado e não representam um sistema empresarial em produção.
