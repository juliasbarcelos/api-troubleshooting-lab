# Postman — Testes Automatizados da API

## Sobre Esta Pasta

Esta pasta contém a coleção Postman desenvolvida para testar e validar a API REST do projeto **API Troubleshooting Lab**.

O laboratório utiliza Python, FastAPI e MySQL para simular uma aplicação de gestão de pedidos de comércio eletrónico.

A coleção permite executar requisições HTTP e verificar automaticamente o comportamento da API através de scripts JavaScript.

O objetivo é demonstrar competências em testes de APIs, validação de respostas HTTP, análise de JSON e investigação de problemas aplicacionais.

---

## 1. Ficheiro da Coleção

**Nome:** `API_Gestao_de_Pedidos.postman_collection.json`

**Formato:** Postman Collection v2.1

**Ficheiro disponível:**

[API de Gestão de Pedidos — Coleção Postman](API_Gestao_de_Pedidos.postman_collection.json)

### Conteúdo

A coleção inclui:

- 6 requisições HTTP.
- 18 verificações automáticas em JavaScript.
- Testes de respostas HTTP 200, 201, 404 e 422.
- Validação da estrutura dos dados JSON.
- Verificação de dados de pedidos.
- Testes de criação de registos.
- Testes de rejeição de dados inválidos.

---

## 2. Ambiente de Testes

| Componente | Tecnologia |
|---|---|
| API REST | FastAPI |
| Linguagem da API | Python |
| Base de dados | MySQL |
| Cliente HTTP | Postman |
| Scripts de teste | JavaScript |
| Servidor | Uvicorn |
| Ambiente | Local |

### Endereço da API

`http://127.0.0.1:8000`

Todas as requisições da coleção utilizam este endereço.

A API precisa de estar em execução para que os testes possam ser realizados.

---

## 3. Requisições e Testes Automatizados

| Requisição | Método | HTTP esperado | Testes |
|---|---|---|---|
| Health Check | GET | 200 | 2 |
| Listar Pedidos | GET | 200 | 3 |
| Consultar Pedido por ID | GET | 200 | 3 |
| Pedido Inexistente | GET | 404 | 3 |
| Criar Pedido | POST | 201 | 4 |
| Quantidade Inválida | POST | 422 | 3 |
| **Total** | | | **18** |

Os testes foram implementados com `pm.test()` e `pm.expect()`.

### 3.1 GET — Health Check

**Endpoint:** `GET /health`

**HTTP esperado:** 200 OK

**Verificações automáticas:**

1. A API devolve HTTP 200.
2. O campo `status` da resposta possui o valor `ok`.

Exemplo de resposta:

    {
      "status": "ok",
      "message": "API em funcionamento"
    }

Este teste permite verificar se o serviço HTTP está disponível.

**Nota:** O Health Check não confirma, por si só, a ligação ao MySQL.

### 3.2 GET — Listar Pedidos

**Endpoint:** `GET /pedidos`

**HTTP esperado:** 200 OK

**Verificações automáticas:**

1. A API devolve HTTP 200.
2. A resposta JSON contém uma lista.
3. A lista contém pelo menos seis pedidos.

O script verifica o número mínimo de elementos:

    pm.expect(resposta.length).to.be.at.least(6);

A verificação depende da existência de pelo menos seis pedidos na base de dados.

### 3.3 GET — Consultar Pedido por ID

**Endpoint:** `GET /pedidos/2`

**HTTP esperado:** 200 OK

**Verificações automáticas:**

1. A API devolve HTTP 200.
2. O identificador do pedido é igual a 2.
3. Os dados do pedido correspondem aos valores esperados.

### Dados esperados

| Campo | Valor |
|---|---|
| id | 2 |
| cliente | Maria Silva |
| produto | Monitor |
| quantidade | 2 |
| estado | enviado |

Este teste valida a consulta de um recurso específico e a consistência dos dados devolvidos.

### 3.4 GET — Pedido Inexistente

**Endpoint:** `GET /pedidos/999`

**HTTP esperado:** 404 Not Found

**Verificações automáticas:**

1. A API devolve HTTP 404.
2. A mensagem de erro é `Pedido não encontrado`.
3. A resposta JSON é um objeto.

Exemplo:

    {
      "detail": "Pedido não encontrado"
    }

O teste demonstra o tratamento de uma consulta cujo recurso não existe.

### 3.5 POST — Criar Pedido

**Endpoint:** `POST /pedidos`

**HTTP esperado:** 201 Created

### Corpo da Requisição

    {
      "cliente": "Cliente API",
      "produto": "Webcam",
      "quantidade": 1,
      "estado": "pendente"
    }

**Verificações automáticas:**

1. A API devolve HTTP 201.
2. O pedido recebe um identificador numérico válido e superior a zero.
3. A resposta contém a mensagem `Pedido criado com sucesso`.
4. Os dados devolvidos correspondem aos dados enviados.

### Validação da Persistência

Durante o laboratório, o teste automático criou o pedido de ID 7.

A gravação foi confirmada através de uma consulta no MySQL Workbench.

**Importante:** Cada execução bem-sucedida desta requisição cria um novo pedido na base de dados.

O identificador gerado poderá ser diferente de 7 em execuções futuras.

### 3.6 POST — Quantidade Inválida

**Endpoint:** `POST /pedidos`

**HTTP esperado:** 422 Unprocessable Entity

### Corpo da Requisição

    {
      "cliente": "Cliente Teste Invalido",
      "produto": "Webcam",
      "quantidade": -2,
      "estado": "pendente"
    }

**Verificações automáticas:**

1. A API devolve HTTP 422.
2. A resposta contém um erro de validação associado ao campo `quantidade`, do tipo `greater_than`.
3. O valor inválido identificado na resposta é `-2`.

A regra de validação implementada no FastAPI exige uma quantidade superior a zero.

A requisição inválida é rejeitada antes da operação de inserção na base de dados.

---

## 4. Resultados dos Testes

Durante a execução individual das seis requisições, foram obtidos os seguintes resultados:

| Cenário | Resultado |
|---|---|
| Health Check | 2/2 aprovados |
| Listar Pedidos | 3/3 aprovados |
| Consultar Pedido por ID | 3/3 aprovados |
| Pedido Inexistente | 3/3 aprovados |
| Criar Pedido | 4/4 aprovados |
| Quantidade Inválida | 3/3 aprovados |
| **Total** | **18/18 aprovados** |

Os resultados foram documentados através de capturas de ecrã e de um relatório técnico.

**Relatório:** [TESTES-AUTOMATICOS-001.md](../Relatorios/TESTES-AUTOMATICOS-001.md)

**Evidências:** [Pasta Evidencias](../Evidencias)

---

## 5. Como Importar a Coleção

### Passo 1 — Preparar o Ambiente

Antes de executar os testes:

1. Instalar as dependências Python do projeto.
2. Configurar a base de dados MySQL.
3. Preparar os pedidos fictícios necessários.
4. Confirmar as variáveis de ambiente da aplicação.
5. Iniciar o servidor FastAPI.

A configuração completa encontra-se no [README principal](../README.md).

### Passo 2 — Iniciar a API

Na pasta principal do projeto, com o ambiente virtual ativo, executar:

    python -m uvicorn api.main:app --host 127.0.0.1 --port 8000

A aplicação ficará disponível em:

`http://127.0.0.1:8000`

### Passo 3 — Importar no Postman

1. Abrir o Postman.
2. Clicar em **Import**.
3. Selecionar o ficheiro `API_Gestao_de_Pedidos.postman_collection.json`.
4. Confirmar a importação.
5. Abrir a coleção **API de Gestão de Pedidos**.

### Passo 4 — Executar os Testes

1. Selecionar a requisição pretendida.
2. Confirmar o método HTTP e o endereço.
3. Consultar os scripts de teste, se necessário.
4. Clicar em **Send**.
5. Verificar o código HTTP.
6. Consultar os resultados dos testes na resposta do Postman.

As requisições podem ser executadas individualmente.

---

## 6. Pré-requisitos dos Dados

Alguns scripts dependem de dados específicos da base MySQL.

| Requisição | Pré-requisito |
|---|---|
| GET /health | API em execução |
| GET /pedidos | Pelo menos seis pedidos existentes |
| GET /pedidos/2 | Pedido 2 com os dados esperados |
| GET /pedidos/999 | Pedido 999 inexistente |
| POST /pedidos válido | Ligação MySQL e permissões de INSERT |
| POST /pedidos inválido | Validação Pydantic ativa |

### Reprodutibilidade

Os scripts SQL fornecidos no projeto criam a estrutura da base e inserem os cinco pedidos iniciais.

Os pedidos adicionais utilizados nos testes originais foram criados posteriormente através da API.

Por este motivo, uma base recém-preparada com apenas os cinco pedidos iniciais não satisfaz imediatamente a verificação de pelo menos seis pedidos.

Para reproduzir o resultado esperado, é necessário preparar os dados adicionais antes de executar essa validação.

**Atenção:** Não executar repetidamente o POST válido sem considerar que novos registos serão armazenados.

---

## 7. Limitações Conhecidas

A coleção documenta os testes realizados no ambiente original do laboratório.

Atualmente:

- As 18 verificações foram aprovadas em execuções individuais.
- A coleção utiliza endereços locais fixos.
- Os testes dependem de dados previamente preparados.
- Não existe limpeza automática dos pedidos criados.
- Não foi executada uma validação completa através do Postman Collection Runner.
- Não estão implementados testes de autenticação HTTP 401 ou autorização HTTP 403.

Estas limitações foram identificadas e podem ser abordadas em futuras melhorias do laboratório.

---

## 8. Melhorias Futuras

- Substituir o endereço fixo por uma variável de ambiente Postman, como `{{base_url}}`.
- Automatizar a preparação e limpeza de dados.
- Tornar os testes independentes de identificadores fixos.
- Executar a coleção através do Postman Collection Runner.
- Integrar a coleção numa pipeline de testes automatizados.
- Adicionar cenários de autenticação e autorização quando implementados na API.

---

## 9. Competências Demonstradas

A coleção evidencia conhecimentos práticos em:

- Testes de APIs REST.
- Configuração de requisições HTTP.
- Utilização do Postman.
- Escrita de testes automatizados em JavaScript.
- Utilização de `pm.test()` e `pm.expect()`.
- Interpretação de respostas JSON.
- Validação de códigos HTTP.
- Verificação de regras de negócio.
- Testes de persistência em MySQL.
- Tratamento de erros e dados inválidos.
- Documentação de resultados de testes.

---

## Documentação Relacionada

- [README principal do projeto](../README.md)
- [Relatório dos testes automáticos](../Relatorios/TESTES-AUTOMATICOS-001.md)
- [Evidências dos testes](../Evidencias)
- [Código-fonte da API](../api/main.py)
- [Scripts da base de dados](../database)

---

## Nota

Este laboratório foi desenvolvido com dados fictícios e num ambiente local controlado.

A coleção Postman integra o portfólio técnico, demonstrando práticas de teste, diagnóstico e validação de aplicações.
