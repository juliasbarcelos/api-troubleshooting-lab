# Database — Estrutura e Gestão da Base de Dados MySQL

## Sobre Esta Pasta

Esta pasta contém os scripts SQL utilizados para criar e preparar a base de dados do projeto **API Troubleshooting Lab**.

O laboratório simula uma aplicação de gestão de pedidos de comércio eletrónico, desenvolvida com Python, FastAPI e MySQL.

A base de dados é responsável pelo armazenamento dos pedidos e permite validar operações realizadas através da API REST.

O objetivo desta documentação é apresentar a estrutura da base de dados, os procedimentos de configuração, as operações SQL utilizadas e as validações realizadas durante o laboratório.

---

## 1. Tecnologias Utilizadas

| Tecnologia | Finalidade |
|---|---|
| MySQL 8.0 | Sistema de gestão de base de dados |
| MySQL Workbench | Administração e execução de consultas SQL |
| SQL | Criação de estruturas e manipulação de dados |
| Python | Comunicação entre a aplicação e a base de dados |
| MySQL Connector/Python | Integração Python–MySQL |
| FastAPI | API responsável pelas operações HTTP |

---

## 2. Estrutura da Pasta

A pasta `database` contém os seguintes ficheiros:

| Ficheiro | Finalidade |
|---|---|
| `01_criar_estrutura.sql` | Criar a base de dados e a tabela de pedidos |
| `02_inserir_dados.sql` | Inserir os pedidos fictícios iniciais |

Os scripts estão organizados pela ordem prevista de execução.

### 01_criar_estrutura.sql

Este script define a estrutura da base de dados utilizada pela aplicação.

Inclui a criação da base de dados e da tabela responsável pelo armazenamento dos pedidos.

### 02_inserir_dados.sql

Este script prepara os dados fictícios iniciais utilizados nos testes da aplicação.

Os registos permitem validar consultas SQL, respostas HTTP e operações realizadas através do Postman.

---

## 3. Identificação da Base de Dados

**Nome da base de dados:**

`api_troubleshooting_lab`

**Tabela principal:**

`pedidos`

A tabela armazena informações sobre pedidos fictícios de clientes.

---

## 4. Estrutura da Tabela Pedidos

| Campo | Tipo de dados | Descrição |
|---|---|---|
| id | INT | Identificador único do pedido |
| cliente | VARCHAR(100) | Nome do cliente |
| produto | VARCHAR(100) | Produto solicitado |
| quantidade | INT | Quantidade de unidades |
| estado | VARCHAR(30) | Estado do pedido |
| data_criacao | TIMESTAMP | Data e hora de criação |

### Regras de Integridade

A estrutura utiliza mecanismos de integridade para controlar os dados armazenados.

- `PRIMARY KEY`: identifica cada pedido de forma única.
- `AUTO_INCREMENT`: gera automaticamente os identificadores.
- `NOT NULL`: impede valores nulos em campos obrigatórios.
- `DEFAULT`: define valores padrão quando aplicável.
- `CHECK`: impede quantidades inferiores ou iguais a zero.

### Validação da Quantidade

A tabela utiliza a restrição:

    CHECK (quantidade > 0)

Esta regra complementa a validação realizada pela aplicação através do Pydantic.

Desta forma, a quantidade é controlada tanto na aplicação como na base de dados.

---

## 5. Dados Fictícios Iniciais

O script `02_inserir_dados.sql` insere cinco pedidos fictícios para utilização nos testes.

| ID | Cliente | Produto | Quantidade | Estado |
|---|---|---|---|---|
| 1 | Cliente Teste | Notebook | 1 | pendente |
| 2 | Maria Silva | Monitor | 2 | enviado |
| 3 | Joao Santos | Teclado | 3 | entregue |
| 4 | Ana Costa | Rato Wireless | 1 | pendente |
| 5 | Pedro Almeida | Impressora | 1 | cancelado |

Estes registos foram utilizados para validar o funcionamento inicial da API.

### Pedidos Criados Posteriormente

Durante os testes HTTP POST, foram criados dois pedidos adicionais.

| ID | Cliente | Produto | Quantidade | Estado |
|---|---|---|---|---|
| 6 | Cliente API | Webcam | 1 | pendente |
| 7 | Cliente API | Webcam | 1 | pendente |

**Pedido 6:** criado durante um teste manual de inserção através da API.

**Pedido 7:** criado durante um teste automático realizado no Postman.

A persistência destes pedidos foi confirmada no MySQL Workbench.

**Total de pedidos após os testes documentados:** 7.

Os identificadores podem variar se a base de dados for recriada ou se forem realizadas novas inserções.

---

## 6. Como Preparar a Base de Dados

### Passo 1 — Abrir o MySQL Workbench

Iniciar o MySQL Workbench e estabelecer uma ligação ao servidor MySQL.

A ligação utilizada para a configuração inicial deve possuir permissões suficientes para criar a base de dados e a tabela.

### Passo 2 — Executar o Script de Estrutura

Abrir o ficheiro:

`01_criar_estrutura.sql`

Executar as instruções SQL para criar a estrutura necessária.

### Passo 3 — Inserir os Dados Iniciais

Abrir o ficheiro:

`02_inserir_dados.sql`

Executar as instruções para inserir os cinco pedidos fictícios.

**Atenção:** este script destina-se à preparação inicial do laboratório.

Não deve ser executado repetidamente numa base já preenchida sem verificar os dados existentes, para evitar duplicações ou conflitos de identificadores.

### Passo 4 — Confirmar os Registos

Executar:

    USE api_troubleshooting_lab;

    SELECT *
    FROM pedidos
    ORDER BY id;

Numa base recém-preparada, deverão aparecer os cinco pedidos iniciais.

---

## 7. Consultas SQL Utilizadas

Durante o laboratório foram realizadas consultas para validar a integridade dos dados e a comunicação com a aplicação.

### Consultar Todos os Pedidos

    SELECT *
    FROM pedidos
    ORDER BY id;

Permite visualizar todos os registos armazenados.

### Consultar um Pedido por Identificador

    SELECT *
    FROM pedidos
    WHERE id = 2;

Permite localizar um pedido específico.

### Contar os Pedidos

    SELECT COUNT(*) AS total_pedidos
    FROM pedidos;

Esta consulta foi utilizada para verificar a quantidade de registos existentes.

### Validar uma Inserção Realizada pela API

    SELECT *
    FROM pedidos
    WHERE id = 7;

Durante o laboratório, esta consulta permitiu confirmar a persistência do pedido criado pelo Postman.

### Consultar os Pedidos Mais Recentes

    SELECT *
    FROM pedidos
    ORDER BY id DESC;

Permite identificar os registos com os identificadores mais elevados.

---

## 8. Integração com a API REST

A base de dados MySQL é utilizada pela aplicação FastAPI para consultar e armazenar pedidos.

### Fluxo de Comunicação

    Postman
       |
       | Requisição HTTP
       v
    FastAPI
       |
       | Operação SQL
       v
    MySQL
       |
       | Resultado
       v
    FastAPI
       |
       | Resposta JSON
       v
    Postman

### Operações Implementadas

| Operação HTTP | Operação SQL | Finalidade |
|---|---|---|
| GET /pedidos | SELECT | Consultar todos os pedidos |
| GET /pedidos/{id} | SELECT + WHERE | Consultar pedido específico |
| POST /pedidos | INSERT | Criar novo pedido |

A API utiliza consultas parametrizadas para enviar valores ao MySQL.

### Exemplo de Inserção

    INSERT INTO pedidos
        (cliente, produto, quantidade, estado)
    VALUES (%s, %s, %s, %s);

Os parâmetros são fornecidos separadamente pelo MySQL Connector/Python.

Esta abordagem reduz riscos de injeção SQL associados à concatenação direta de valores nas instruções.

---

## 9. Configuração de Acesso

Durante o laboratório, foi criado um utilizador específico para a aplicação.

**Utilizador:** `api_suporte@localhost`

As permissões atribuídas foram limitadas às operações necessárias.

    GRANT SELECT, INSERT, UPDATE
    ON api_troubleshooting_lab.*
    TO 'api_suporte'@'localhost';

### Princípio do Menor Privilégio

A utilização de uma conta específica para a aplicação permite evitar o acesso permanente com o utilizador administrativo `root`.

A aplicação utiliza credenciais configuradas localmente através de variáveis de ambiente.

### Variáveis Utilizadas

    DB_HOST
    DB_PORT
    DB_NAME
    DB_USER
    DB_PASSWORD

Os valores reais são armazenados no ficheiro `.env`, localizado na raiz do projeto.

**O ficheiro `.env` não deve ser publicado no GitHub.**

O repositório disponibiliza apenas um exemplo de configuração:

[.env.example](../.env.example)

---

## 10. Investigação de Incidentes MySQL

A base de dados foi utilizada na investigação de dois incidentes técnicos.

### INC-API-001 — Falha de Autenticação

Durante a configuração da integração Python–MySQL, foi identificado um erro de autenticação.

**Erro:**

- MySQL 1045
- SQLSTATE 28000
- Acesso recusado

**Resolução:**

Criação e configuração de um utilizador específico para a aplicação, com permissões limitadas.

A ligação foi posteriormente validada através de uma consulta SQL.

**Relatório:** [INC-API-001.md](../Relatorios/INC-API-001.md)

### INC-API-002 — Indisponibilidade da Base de Dados

Foi realizada uma simulação controlada de falha de conectividade.

A porta MySQL foi temporariamente alterada de `3306` para `3399`.

O teste direto de ligação identificou o erro MySQL 2003, correspondente à impossibilidade de estabelecer comunicação com o servidor na porta configurada.

A aplicação devolveu HTTP 503 Service Unavailable.

Durante a recuperação, também foi identificado um conflito adicional relacionado com um processo Uvicorn na porta HTTP 8000.

Após a restauração das configurações e a resolução do conflito, a aplicação voltou a funcionar normalmente.

**Resultado final:**

- HTTP 200 OK.
- 3/3 testes automáticos aprovados.
- 7 pedidos preservados.

**Relatório:** [INC-API-002.md](../Relatorios/INC-API-002.md)

---

## 11. Validação da Integridade dos Dados

Durante os testes, foram realizadas verificações cruzadas entre a API e o MySQL Workbench.

### Inserção Válida

Uma requisição HTTP POST com dados válidos devolveu HTTP 201.

A consulta SQL posterior confirmou que o registo tinha sido armazenado.

### Inserção Inválida

Foi enviada uma requisição com quantidade igual a `-2`.

A validação Pydantic rejeitou a requisição com HTTP 422.

A consulta SQL confirmou que o pedido inválido não tinha sido inserido.

### Recuperação Após Incidente

Após a simulação de indisponibilidade, a ligação foi restabelecida e os pedidos continuaram disponíveis.

Estas verificações demonstraram:

- Validação de dados antes da inserção.
- Persistência de operações válidas.
- Preservação dos dados durante a simulação.
- Consistência entre respostas HTTP e registos MySQL.

---

## 12. Evidências

As capturas de ecrã produzidas durante o laboratório encontram-se na pasta:

[Evidencias](../Evidencias)

Incluem:

- Criação da estrutura da base de dados.
- Inserção dos pedidos fictícios iniciais.
- Consultas SQL de validação.
- Confirmação de pedidos criados através da API.
- Verificação de rejeição de dados inválidos.
- Testes de conectividade e recuperação de incidentes.

Os resultados também estão documentados nos relatórios técnicos disponíveis em:

[Relatorios](../Relatorios)

---

## 13. Competências Demonstradas

O trabalho desenvolvido nesta componente demonstra competências em:

- Modelação básica de bases de dados relacionais.
- Criação de tabelas MySQL.
- Definição de chaves primárias e restrições.
- Utilização de SELECT, WHERE, COUNT e ORDER BY.
- Inserção de registos através de SQL e APIs.
- Validação da integridade dos dados.
- Integração entre Python e MySQL.
- Utilização de consultas parametrizadas.
- Gestão de permissões de acesso.
- Diagnóstico de erros de autenticação.
- Investigação de problemas de conectividade.
- Validação da recuperação de serviços.
- Documentação técnica.

---

## Documentação Relacionada

- [README principal do projeto](../README.md)
- [Código-fonte da API](../api)
- [Coleção Postman](../Postman)
- [Relatórios técnicos](../Relatorios)
- [Evidências](../Evidencias)

---

## Nota

Esta base de dados foi desenvolvida exclusivamente para um laboratório educativo, utilizando dados fictícios.

O objetivo é demonstrar competências práticas em SQL, integração de aplicações e resolução de incidentes relevantes.
