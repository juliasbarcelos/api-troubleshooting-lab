# API Troubleshooting Lab

## Sobre o Projeto

Este projeto apresenta um laboratório prático de testes, diagnóstico e investigação de incidentes em APIs REST, desenvolvido com foco nas atividades de Suporte Aplicacional Júnior.

O laboratório combina testes HTTP realizados no Postman, desenvolvimento de uma API REST em Python com FastAPI e utilização de uma base de dados relacional MySQL.

O objetivo é desenvolver e demonstrar competências de diagnóstico técnico, interpretação de respostas HTTP, análise de erros, consultas SQL, identificação de causas, resolução de problemas e documentação de incidentes aplicacionais.

O projeto utiliza um cenário fictício de comércio eletrónico, permitindo reproduzir e investigar falhas num ambiente local e controlado.

**Estado do projeto:** Em desenvolvimento.

---

## Objetivos

- Executar e analisar requisições HTTP GET e POST.
- Interpretar códigos de estado HTTP e respostas JSON.
- Desenvolver uma API REST utilizando Python e FastAPI.
- Implementar uma base de dados relacional MySQL.
- Integrar uma aplicação Python com o MySQL.
- Executar consultas SQL para verificar dados.
- Diagnosticar falhas de autenticação e ligação à base de dados.
- Aplicar o princípio do menor privilégio.
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

O laboratório simula uma aplicação de comércio eletrónico que utiliza uma API REST para consultar e registar pedidos fictícios de clientes.

A arquitetura é composta por três componentes principais:

1. **Postman:** ferramenta utilizada para enviar requisições HTTP, analisar respostas e organizar testes.
2. **FastAPI:** aplicação Python responsável por receber e processar requisições HTTP.
3. **MySQL:** sistema de gestão de base de dados responsável pelo armazenamento dos pedidos.

A ligação Python–MySQL já foi implementada e validada através de um script de diagnóstico.

A integração das consultas SQL com os endpoints HTTP da API será realizada nas próximas etapas.

---

## Desenvolvimento da API

Foi criada uma API REST em Python utilizando FastAPI e o servidor Uvicorn.

### Funcionalidades Implementadas

- Inicialização da aplicação FastAPI.
- Configuração do servidor Uvicorn.
- Implementação do endpoint GET `/health`.
- Respostas estruturadas em JSON.
- Testes de comunicação HTTP através do Postman.
- Configuração da ligação Python–MySQL.
- Consulta de validação à base de dados MySQL.

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

O endpoint permite verificar se a aplicação está a responder corretamente a requisições HTTP.

Esta verificação confirma a disponibilidade básica da aplicação, mas não valida automaticamente a conectividade com a base de dados.

**Código-fonte:** [api/main.py](api/main.py)

---

## Integração Python + MySQL

Foi implementada e validada a comunicação entre Python e a base de dados `api_troubleshooting_lab`.

A integração utiliza a biblioteca `mysql-connector-python` e configurações carregadas através de `python-dotenv`.

### Ficheiros de Integração

- [database.py](api/database.py) — estabelece a ligação ao MySQL.
- [testar_ligacao.py](api/testar_ligacao.py) — executa o teste de ligação e a consulta SQL.
- [requirements.txt](requirements.txt) — regista as dependências Python.
- [.env.example](.env.example) — apresenta as variáveis de configuração necessárias.
- [.gitignore](.gitignore) — define os ficheiros que não devem ser incluídos no Git.

### Segurança da Ligação

Foi criado um utilizador MySQL específico para a aplicação:

`api_suporte@localhost`

Foram atribuídas permissões limitadas à base de dados do laboratório:

```sql
GRANT SELECT, INSERT, UPDATE
ON api_troubleshooting_lab.*
TO 'api_suporte'@'localhost';
```

Esta configuração permite realizar as operações necessárias sem utilizar permanentemente a conta administrativa `root`.

As credenciais são guardadas localmente no ficheiro `.env`, que não é publicado no GitHub.

O ficheiro `.env.example` contém apenas valores demonstrativos.

### Teste de Integração

Para validar a ligação entre Python e MySQL, foi executado:

```powershell
python -m api.testar_ligacao
```

**Resultado obtido:**

```text
Ligação ao MySQL estabelecida com sucesso.
Total de pedidos encontrados: 5
```

O resultado confirmou que o Python conseguiu autenticar-se no MySQL, executar uma consulta SQL e obter o total de pedidos armazenados.

**Estado:** Ligação Python–MySQL validada.

A utilização desta ligação nos endpoints HTTP da API será implementada na próxima etapa.

---

## Base de Dados MySQL

O laboratório utiliza uma base de dados MySQL para armazenar pedidos fictícios de uma aplicação de comércio eletrónico.

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

### Implementação

A base de dados e a tabela `pedidos` foram criadas e validadas no MySQL Workbench.

Foram inseridos cinco pedidos fictícios, com diferentes produtos, quantidades e estados.

### Dados de Teste

| ID | Cliente | Produto | Quantidade | Estado |
|---|---|---|---|---|
| 1 | Cliente Teste | Notebook | 1 | pendente |
| 2 | Maria Silva | Monitor | 2 | enviado |
| 3 | Joao Santos | Teclado | 3 | entregue |
| 4 | Ana Costa | Rato Wireless | 1 | pendente |
| 5 | Pedro Almeida | Impressora | 1 | cancelado |

Todos os registos são fictícios e utilizados exclusivamente para testes e simulação de incidentes.

### Validação SQL

Após a inserção dos dados, foi executada a seguinte consulta:

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

**Resultado:** Foram devolvidos os cinco pedidos esperados.

### Scripts SQL

- [01_criar_estrutura.sql](database/01_criar_estrutura.sql) — criação da base de dados e da tabela.
- [02_inserir_dados.sql](database/02_inserir_dados.sql) — inserção e consulta dos pedidos fictícios.

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

A investigação incluiu a verificação da conta autenticada no MySQL Workbench, análise da configuração Python e identificação do código de erro.

#### Correção Aplicada

Foi criado o utilizador `api_suporte`, com credenciais próprias e permissões limitadas de `SELECT`, `INSERT` e `UPDATE` na base de dados do laboratório.

As configurações locais foram atualizadas para utilizar a nova conta.

#### Validação

Após a correção, a execução do teste devolveu:

```text
Ligação ao MySQL estabelecida com sucesso.
Total de pedidos encontrados: 5
```

A consulta confirmou que a aplicação Python conseguiu autenticar-se e aceder aos dados.

**Conclusão:** Incidente resolvido e correção validada.

**Relatório:** [INC-API-001.md](Relatorios/INC-API-001.md)

**Evidência:** [Erro MySQL 1045 e correção](Evidencias/MYSQL_ERRO_1045_CORRECAO.png)

### Incidentes Planeados

Os próximos cenários serão simulados num ambiente controlado.

| Cenário | Falha a investigar | Código HTTP previsto |
|---|---|---|
| Consulta de pedido inexistente | Recurso não encontrado | 404 |
| Envio de dados inválidos | Erro de validação | 400/422 |
| Falha de autenticação na API | Credenciais inválidas | 401 |
| Permissão insuficiente | Acesso proibido | 403 |
| Falha de comunicação com MySQL | Erro interno ou indisponibilidade | 500/503 |

Os códigos dependerão do tratamento de erros implementado.

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

```text
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
|   |-- MYSQL_CRIACAO_TABELA_PEDIDOS.png
|   |-- MYSQL_INSERCAO_PEDIDOS.png
|   |-- MYSQL_ERRO_1045_CORRECAO.png
|
|-- Relatorios/
|   |-- TESTE-GET-001.md
|   |-- TESTE-POST-002.md
|   |-- TESTE-GET-003.md
|   |-- INC-API-001.md
|
|-- .env.example
|-- .gitignore
|-- requirements.txt
|-- README.md
```

O ficheiro `.env` verdadeiro e o ambiente virtual `.venv` permanecem locais e não fazem parte do repositório.

A estrutura será ampliada à medida que forem implementadas novas funcionalidades e investigações.

---

## Configuração do Ambiente

### Requisitos

- Python compatível com as dependências do projeto.
- MySQL Server 8.0.
- MySQL Workbench, opcional para administração.
- Postman para testes HTTP.

### 1. Criar o Ambiente Virtual

Na pasta principal do projeto:

```powershell
python -m venv .venv
```

Ativar o ambiente no Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar as Dependências

```powershell
python -m pip install -r requirements.txt
```

As dependências incluem FastAPI, Uvicorn, MySQL Connector/Python e python-dotenv.

### 3. Preparar a Base de Dados

No MySQL Workbench:

1. Estabelecer ligação ao MySQL Server.
2. Executar `database/01_criar_estrutura.sql`.
3. Numa base inicialmente vazia, executar `database/02_inserir_dados.sql`.
4. Confirmar a existência dos cinco pedidos fictícios.

### 4. Configurar as Variáveis de Ambiente

Criar um ficheiro `.env` na pasta principal com base em `.env.example`.

Configurar os valores de ligação ao MySQL:

```dotenv
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=api_troubleshooting_lab
DB_USER=seu_utilizador_mysql
DB_PASSWORD=sua_palavra_passe
```

O utilizador configurado deve ter permissões adequadas sobre a base de dados do laboratório.

Não publicar o ficheiro `.env` com credenciais reais.

### 5. Testar a Ligação ao MySQL

Executar:

```powershell
python -m api.testar_ligacao
```

Numa base com os cinco registos de teste, o resultado esperado é:

```text
Ligação ao MySQL estabelecida com sucesso.
Total de pedidos encontrados: 5
```

### 6. Executar a API

Na pasta principal do projeto:

```powershell
python -m uvicorn api.main:app --reload
```

A aplicação ficará disponível em:

`http://127.0.0.1:8000`

Endpoint Health Check:

`http://127.0.0.1:8000/health`

Documentação interativa:

`http://127.0.0.1:8000/docs`

Para interromper o servidor, pressionar `Ctrl + C` no terminal.

**Nota:** a ligação Python–MySQL está validada através de um script independente. A utilização da base de dados nos endpoints HTTP ainda será desenvolvida.

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
- [x] Implementação das restrições de integridade.
- [x] Inserção de cinco pedidos fictícios.
- [x] Validação dos registos através de SQL.
- [x] Publicação dos scripts SQL.
- [x] Instalação do MySQL Connector/Python.
- [x] Configuração das variáveis de ambiente.
- [x] Criação de utilizador MySQL com permissões limitadas.
- [x] Validação da ligação Python–MySQL.
- [x] Diagnóstico do erro MySQL 1045.
- [x] Resolução e validação do incidente INC-API-001.
- [x] Publicação do código de integração Python.
- [x] Documentação dos testes e do incidente.
- [x] Organização das evidências técnicas.

### Próximas Etapas

- [ ] Implementar GET `/pedidos` com consulta ao MySQL.
- [ ] Implementar GET `/pedidos/{id}`.
- [ ] Implementar POST `/pedidos`.
- [ ] Validar a persistência de dados através da API.
- [ ] Criar testes automáticos no Postman.
- [ ] Implementar tratamento estruturado de erros.
- [ ] Simular incidentes HTTP 400, 401, 403, 404 e 500.
- [ ] Investigar falhas de comunicação com MySQL.
- [ ] Documentar causas, correções e validações.
- [ ] Exportar e publicar a coleção Postman.
- [ ] Rever a documentação e as instruções de execução.
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
- Diagnóstico de erros de autenticação.
- Interpretação de códigos MySQL e SQLSTATE.
- Gestão básica de utilizadores e permissões.
- Aplicação do princípio do menor privilégio.
- Utilização de variáveis de ambiente.
- Validação de correções técnicas.
- Elaboração de relatórios de incidentes.
- Organização de código e evidências no GitHub.

---

## Nota

Este projeto utiliza exclusivamente dados fictícios e foi desenvolvido para fins educativos e de demonstração de competências técnicas em Suporte Aplicacional Júnior.

Os resultados correspondem a testes realizados num ambiente local e controlado e não representam um sistema empresarial em produção.
