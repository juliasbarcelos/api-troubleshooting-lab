# API Troubleshooting Lab

## Sobre o Projeto

Este projeto apresenta um laboratório prático de testes e investigação de incidentes em APIs REST, desenvolvido com foco nas atividades de Suporte Aplicacional Júnior.

O laboratório combina testes HTTP utilizando o Postman, o desenvolvimento de uma API REST em Python com FastAPI e a utilização de uma base de dados relacional MySQL.

O objetivo é desenvolver competências de diagnóstico técnico, interpretação de respostas HTTP, análise de erros, consultas SQL, identificação de causas e documentação de incidentes aplicacionais.

O projeto utiliza um cenário fictício de comércio eletrónico, permitindo reproduzir e investigar falhas de forma controlada.

**Estado do projeto:** Em desenvolvimento.

---

## Objetivos

- Executar e analisar requisições HTTP GET e POST.
- Interpretar códigos de estado HTTP e respostas JSON.
- Desenvolver uma API REST utilizando Python e FastAPI.
- Implementar uma base de dados relacional MySQL.
- Integrar a API Python com a base de dados.
- Executar consultas SQL para verificar dados.
- Simular e investigar erros HTTP 400, 401, 403, 404 e 500.
- Analisar logs e identificar possíveis causas de falhas.
- Validar correções através de novos testes.
- Documentar procedimentos, resultados e evidências técnicas.

---

## Tecnologias e Ferramentas

- Python
- FastAPI
- Uvicorn
- MySQL 8.0
- MySQL Workbench
- Postman
- SQL
- HTTP e APIs REST
- JSON
- Visual Studio Code
- GitHub

---

## Cenário do Laboratório

O laboratório simula uma aplicação de comércio eletrónico que utiliza uma API REST para consultar e registar pedidos fictícios de clientes.

A arquitetura prevista é composta por três componentes:

1. **Postman:** utilizado para enviar requisições HTTP e analisar respostas.
2. **FastAPI:** responsável por receber e processar as requisições.
3. **MySQL:** responsável pelo armazenamento dos pedidos.

A integração entre FastAPI e MySQL será implementada nas próximas etapas.

Durante o desenvolvimento serão simulados incidentes para reproduzir situações comuns de Suporte Aplicacional.

---

## Desenvolvimento da API

Foi criada uma API REST em Python utilizando o framework FastAPI e o servidor Uvicorn.

### Funcionalidades Implementadas

- Inicialização da aplicação FastAPI.
- Configuração do servidor local Uvicorn.
- Implementação do endpoint GET `/health`.
- Resposta estruturada em JSON.
- Teste de comunicação HTTP através do Postman.

### Endpoint Health Check

**Método:** GET

**Endpoint:** `http://127.0.0.1:8000/health`

**Resposta esperada:**

```json
{
  "status": "ok",
  "message": "API em funcionamento"
}
```

O endpoint permite verificar se a aplicação está a responder a requisições HTTP.

Esta verificação confirma a disponibilidade básica da aplicação, mas não valida, por si só, a conectividade com a base de dados.

**Código-fonte:** [api/main.py](api/main.py)

---

## Base de Dados MySQL

O laboratório utiliza uma base de dados MySQL para armazenar informações de pedidos fictícios.

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

A estrutura da tabela inclui:

- Chave primária no campo `id`.
- Incremento automático do identificador.
- Campos obrigatórios definidos com `NOT NULL`.
- Estado inicial padrão `pendente`.
- Restrição `CHECK` para impedir quantidades inferiores ou iguais a zero.
- Registo automático da data de criação.

### Implementação

A base de dados `api_troubleshooting_lab` e a tabela `pedidos` foram criadas e validadas através do MySQL Workbench.

Foram inseridos cinco pedidos fictícios, com diferentes produtos, quantidades e estados.

A consulta SQL confirmou que os cinco registos foram armazenados corretamente, com identificadores automáticos e datas de criação.

### Dados de Teste Inseridos

| ID | Cliente | Produto | Quantidade | Estado |
|---|---|---|---|---|
| 1 | Cliente Teste | Notebook | 1 | pendente |
| 2 | Maria Silva | Monitor | 2 | enviado |
| 3 | Joao Santos | Teclado | 3 | entregue |
| 4 | Ana Costa | Rato Wireless | 1 | pendente |
| 5 | Pedro Almeida | Impressora | 1 | cancelado |

Todos os registos são fictícios e utilizados exclusivamente para simulação de operações e incidentes.

### Validação SQL

Após a inserção, foi executada uma consulta para verificar os registos armazenados:

```sql
USE api_troubleshooting_lab;

SELECT
    id,
    cliente,
    produto,
    quantidade,
    estado,
    data_criacao
FROM pedidos
ORDER BY id;
```

**Resultado:** Foram devolvidos os cinco pedidos esperados, sem erros na execução.

### Scripts SQL

- [01_criar_estrutura.sql](database/01_criar_estrutura.sql) — criação da base de dados e da tabela.
- [02_inserir_dados.sql](database/02_inserir_dados.sql) — inserção e consulta dos pedidos fictícios.

**Nota:** o script de inserção deve ser executado apenas uma vez numa base inicialmente vazia, pois uma nova execução poderá criar registos duplicados.

### Evidências

- [Criação da tabela pedidos](Evidencias/MYSQL_CRIACAO_TABELA_PEDIDOS.png)
- [Inserção dos cinco pedidos](Evidencias/MYSQL_INSERCAO_PEDIDOS.png)

### Resultado

**Estado:** Concluído — estrutura criada e cinco pedidos fictícios inseridos e validados.

A integração entre FastAPI e MySQL ainda será implementada.

---

## Testes HTTP Realizados

### TESTE-GET-001 — Verificação de Comunicação HTTP

**Ferramenta:** Postman

**Método:** GET

**Endpoint:** `https://postman-echo.com/get`

**Resultado:** HTTP 200 OK

**Tempo de resposta:** 384 ms

**Estado:** Aprovado

O teste confirmou que a API pública respondeu corretamente à requisição GET.

**Relatório:** [TESTE-GET-001.md](Relatorios/TESTE-GET-001.md)

**Evidência:** [GET_200_OK.png](Evidencias/GET_200_OK.png)

### TESTE-POST-002 — Verificação de Envio de Dados HTTP

**Ferramenta:** Postman

**Método:** POST

**Endpoint:** `https://postman-echo.com/post`

**Resultado:** HTTP 200 OK

**Tempo de resposta:** 433 ms

**Estado:** Aprovado

O teste confirmou que a API recebeu e devolveu corretamente os dados JSON enviados.

O Postman Echo não armazenou os dados numa base de dados.

**Relatório:** [TESTE-POST-002.md](Relatorios/TESTE-POST-002.md)

**Evidência:** [POST_200_OK.png](Evidencias/POST_200_OK.png)

### TESTE-GET-003 — Health Check da API Local

**Ferramenta:** Postman

**Método:** GET

**Endpoint:** `http://127.0.0.1:8000/health`

**Resultado:** HTTP 200 OK

**Tempo de resposta:** 5 ms

**Estado:** Aprovado

O teste confirmou que a API desenvolvida em Python estava a responder corretamente no ambiente local.

**Relatório:** [TESTE-GET-003.md](Relatorios/TESTE-GET-003.md)

**Evidência:** [GET_HEALTH_200_OK.png](Evidencias/GET_HEALTH_200_OK.png)

---

## Investigação de Incidentes

O laboratório irá incluir simulações controladas de incidentes relacionados com APIs REST e operações de base de dados.

### Cenários Planeados

| Incidente | Cenário | Categoria |
|---|---|---|
| INC-API-001 | Consulta de pedido inexistente | HTTP 404 |
| INC-API-002 | Envio de dados inválidos | HTTP 400/422 |
| INC-API-003 | Falha de autenticação | HTTP 401 |
| INC-API-004 | Permissão insuficiente | HTTP 403 |
| INC-API-005 | Falha de comunicação com MySQL | HTTP 500/503 |

Os códigos apresentados representam os cenários previstos e dependerão do tratamento de erros implementado.

Cada investigação incluirá:

1. Descrição do incidente.
2. Comportamento esperado e observado.
3. Reprodução da falha.
4. Análise de respostas HTTP e logs.
5. Identificação da causa.
6. Aplicação da correção.
7. Validação através de novos testes.
8. Registo de evidências e conclusão técnica.

**Estado:** Investigações ainda não iniciadas.

---

## Estrutura do Repositório

```text
api-troubleshooting-lab/
|
|-- api/
|   |-- main.py
|
|-- database/
|   |-- 01_criar_estrutura.sql
|   |-- 02_inserir_dados.sql
|
|-- Evidencias/
|   |-- GET_200_OK.png
|   |-- POST_200_OK.png
|   |-- GET_HEALTH_200_OK.png
|   |-- MYSQL_CRIACAO_TABELA_PEDIDOS.png
|   |-- MYSQL_INSERCAO_PEDIDOS.png
|
|-- Relatorios/
|   |-- TESTE-GET-001.md
|   |-- TESTE-POST-002.md
|   |-- TESTE-GET-003.md
|
|-- .gitignore
|-- requirements.txt
|-- README.md
```

A estrutura será ampliada à medida que forem implementadas novas funcionalidades, testes e investigações.

---

## Configuração do Ambiente

### Requisitos

- Python compatível com as dependências do projeto.
- MySQL Server 8.0.
- MySQL Workbench, opcional para administração.
- Postman para execução de testes.

### Instalação das Dependências

Criar e ativar um ambiente virtual Python:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instalar as bibliotecas:

```powershell
python -m pip install -r requirements.txt
```

### Preparar a Base de Dados

No MySQL Workbench:

1. Estabelecer ligação ao servidor MySQL.
2. Executar `database/01_criar_estrutura.sql`.
3. Numa base inicialmente vazia, executar `database/02_inserir_dados.sql`.
4. Confirmar a existência dos cinco pedidos fictícios.

### Executar a API

Na pasta principal do projeto:

```powershell
python -m uvicorn api.main:app --reload
```

A API ficará disponível localmente em:

`http://127.0.0.1:8000`

Documentação interativa automática:

`http://127.0.0.1:8000/docs`

O servidor pode ser interrompido com `Ctrl + C`.

**Nota:** nesta versão, a base de dados e a API funcionam separadamente. A ligação entre FastAPI e MySQL será implementada na próxima etapa.

---

## Estado do Projeto

### Atividades Concluídas

- [x] Configuração do Postman.
- [x] Teste HTTP GET numa API pública.
- [x] Teste HTTP POST com dados JSON.
- [x] Criação da API Python com FastAPI.
- [x] Configuração do ambiente virtual Python.
- [x] Instalação das dependências.
- [x] Implementação do endpoint GET `/health`.
- [x] Validação do Health Check no Postman.
- [x] Criação da base de dados MySQL.
- [x] Criação da tabela `pedidos`.
- [x] Implementação de restrições de integridade.
- [x] Inserção de cinco pedidos fictícios no MySQL.
- [x] Validação dos registos através de consulta SQL.
- [x] Publicação dos scripts de criação e inserção.
- [x] Publicação das evidências técnicas.
- [x] Documentação dos três primeiros testes HTTP.

### Próximas Etapas

- [ ] Integrar FastAPI com MySQL.
- [ ] Configurar a ligação à base de dados de forma segura.
- [ ] Implementar GET `/pedidos`.
- [ ] Implementar GET `/pedidos/{id}`.
- [ ] Implementar POST `/pedidos`.
- [ ] Validar a persistência de dados através da API.
- [ ] Criar testes automáticos no Postman.
- [ ] Simular e investigar incidentes HTTP.
- [ ] Documentar causas, correções e validações.
- [ ] Exportar e publicar a coleção Postman.
- [ ] Realizar a revisão final do portfólio.

---

## Competências Trabalhadas

- Testes de APIs REST.
- Comunicação HTTP.
- Interpretação de respostas JSON.
- Desenvolvimento básico de APIs com Python.
- Utilização do framework FastAPI.
- Administração básica de bases de dados MySQL.
- Criação de tabelas e restrições SQL.
- Inserção e consulta de dados relacionais.
- Verificação da integridade dos dados.
- Análise de resultados técnicos.
- Documentação de testes e evidências.
- Organização de projetos utilizando GitHub.

---

## Nota

Este projeto utiliza exclusivamente dados fictícios e foi desenvolvido para fins educativos e de demonstração de competências técnicas em Suporte Aplicacional.

Os resultados apresentados correspondem a testes realizados num ambiente controlado, não representando um sistema empresarial em produção.
