# INC-API-002 — Indisponibilidade da Base de Dados MySQL

## 1. Identificação do Incidente

- **ID:** INC-API-002
- **Título:** Falha de comunicação entre FastAPI e MySQL
- **Aplicação:** API de Gestão de Pedidos
- **Categoria:** Conectividade / Base de dados
- **Ambiente:** Laboratório local
- **Ferramentas:** Python, FastAPI, MySQL, Postman, VS Code e PowerShell
- **Data:** 19/10/2026
- **Estado:** Resolvido e validado

## 2. Objetivo

Simular uma falha de comunicação com a base de dados MySQL, analisar o comportamento da API e realizar a recuperação do serviço.

Validar que a aplicação devolve HTTP 503 quando não consegue estabelecer ligação ao MySQL e HTTP 200 após o restabelecimento da comunicação.

## 3. Cenário Inicial

A aplicação encontrava-se operacional, com o servidor Uvicorn disponível em:

`http://127.0.0.1:8000`

O endpoint utilizado na investigação foi:

`GET /pedidos`

A base de dados `api_troubleshooting_lab` continha sete pedidos fictícios.

### Validação Inicial

Foi realizada uma requisição no Postman.

**Resultado obtido:**

- Código HTTP: 200 OK
- Tempo de resposta: 129 ms
- Testes automáticos: 3/3 aprovados
- Resposta: Lista JSON de pedidos

A comunicação entre FastAPI e MySQL estava funcional.

## 4. Simulação da Falha

Para reproduzir uma falha de conectividade, foi alterada temporariamente a configuração local da porta MySQL.

### Configuração original

    DB_PORT=3306

### Configuração utilizada na simulação

    DB_PORT=3399

O objetivo era fazer com que a aplicação tentasse estabelecer ligação através de uma porta onde não estava disponível o servidor MySQL.

A simulação não exigiu interromper o serviço MySQL nem modificar os dados armazenados.

## 5. Diagnóstico Inicial

Após a alteração da configuração, o Postman continuou inicialmente a devolver HTTP 200.

Foi necessário investigar a configuração efetivamente utilizada pela aplicação.

### Verificação das Variáveis de Ambiente

Foi executado um comando Python que confirmou:

    Porta MySQL configurada: 3399

### Teste Direto da Ligação

Foi executado:

    python -m api.testar_ligacao

**Resultado:**

    Falha na ligação ou consulta MySQL.
    Tipo de erro: InterfaceError
    Código MySQL: 2003
    SQLSTATE: None
    Consulta não concluída.

### Interpretação

O erro MySQL 2003 indicou que o cliente não conseguiu estabelecer ligação ao servidor no endereço e porta configurados.

A falha foi reproduzida de forma controlada.

## 6. Análise do Carregamento de Configurações

Durante a investigação, foi analisado o carregamento das variáveis de ambiente no ficheiro `api/database.py`.

A configuração utilizava:

    load_dotenv(BASE_DIR / ".env")

Para verificar a hipótese de existirem variáveis de ambiente previamente definidas, foi testada temporariamente a utilização de:

    load_dotenv(BASE_DIR / ".env", override=True)

Esta alteração permite que os valores do ficheiro `.env` substituam variáveis de ambiente já existentes no processo Python.

Após o reinício da aplicação, foi possível reproduzir a resposta HTTP 503.

A configuração original de `database.py` foi posteriormente restaurada.

**Nota:** a investigação não demonstrou de forma conclusiva a origem da diferença inicial de configuração entre os processos. A hipótese de precedência das variáveis de ambiente foi considerada durante o diagnóstico.

## 7. Falha HTTP 503 Confirmada

Foi executada uma nova requisição:

`GET http://127.0.0.1:8000/pedidos`

### Resultado Obtido

- **Código HTTP:** 503 Service Unavailable
- **Tempo de resposta:** 2,26 s
- **Tamanho da resposta:** 196 B
- **Testes automáticos:** 0/3 aprovados

### Resposta JSON

    {
      "detail": "Serviço de base de dados indisponível"
    }

### Análise Técnica

A API recebeu a requisição HTTP, mas não conseguiu estabelecer a ligação necessária ao MySQL.

O tratamento de erros da aplicação devolveu HTTP 503 em vez de uma lista de pedidos.

Os testes automáticos existentes esperavam HTTP 200 e uma lista JSON, pelo que reprovaram durante a simulação.

Este comportamento confirmou que o endpoint distinguia uma consulta bem-sucedida de uma indisponibilidade da base de dados.

## 8. Tentativa de Recuperação

A configuração da porta MySQL foi restaurada:

    DB_PORT=3306

O teste direto de ligação voltou a funcionar:

    Ligação ao MySQL estabelecida com sucesso.
    Total de pedidos encontrados: 7

Contudo, o endpoint HTTP continuou temporariamente a devolver HTTP 503.

Foi necessário prosseguir com a investigação dos processos responsáveis pelo servidor da API.

## 9. Diagnóstico do Conflito da Porta HTTP 8000

Durante as tentativas de reiniciar o Uvicorn, foi identificado o erro:

    [Errno 10048] error while attempting to bind
    on address ('127.0.0.1', 8000)

Este erro indicava que a porta HTTP 8000 já estava ocupada.

### Verificações Realizadas

Foram utilizados comandos PowerShell:

    netstat -ano | findstr :8000

    Get-NetTCPConnection -LocalPort 8000 -State Listen

    Get-CimInstance Win32_Process

### Resultados

Foi identificado o PID 13080 como responsável por uma ligação em estado LISTENING na porta 8000.

Posteriormente, a análise dos processos Python identificou:

- PID 31000 — processo Python associado ao processo pai 13080.
- PID 15420 — processo associado ao Uvicorn na porta 8001.
- PID 30672 — processo associado ao Uvicorn na porta 8001.

O PID 13080 já não podia ser encontrado pelos comandos de encerramento utilizados, apesar de continuar associado à porta 8000.

O processo Python 31000 foi identificado como possível componente residual da execução anterior.

## 10. Recuperação Temporária na Porta 8001

Para isolar o conflito da porta HTTP 8000, foi iniciada uma instância da API numa porta alternativa.

### Comando

    python -m uvicorn api.main:app --host 127.0.0.1 --port 8001

O servidor iniciou corretamente.

### Validação

Foi consultado o endpoint:

`http://127.0.0.1:8001/pedidos`

A API devolveu os sete pedidos armazenados no MySQL.

Posteriormente, o resultado também foi validado no Postman.

**Resultado obtido:**

- Código HTTP: 200 OK
- Tempo de resposta: 108 ms
- Tamanho da resposta: 1014 B
- Testes automáticos: 3/3 aprovados

A recuperação na porta alternativa confirmou que a aplicação e a base de dados estavam operacionais.

## 11. Resolução do Conflito na Porta 8000

A investigação dos processos identificou uma instância Python associada à execução antiga do Uvicorn.

Foi utilizado o comando:

    Stop-Process -Id 31000

Após o encerramento desse processo, a consulta à porta 8000 deixou de apresentar processos no estado LISTENING.

### Validação

Foi executado:

    Get-NetTCPConnection -LocalPort 8000 -State Listen

Não foram devolvidas ligações em estado LISTENING.

A porta HTTP 8000 ficou novamente disponível.

## 12. Recuperação Definitiva

Com a porta 8000 disponível e a configuração MySQL restaurada, foi iniciada uma nova instância da API:

    python -m uvicorn api.main:app --host 127.0.0.1 --port 8000

A aplicação iniciou corretamente.

### Validação Final no Postman

**Endpoint:**

`GET http://127.0.0.1:8000/pedidos`

**Resultado obtido:**

- Código HTTP: 200 OK
- Tempo de resposta: 338 ms
- Tamanho da resposta: 1014 B
- Testes automáticos: 3/3 aprovados
- Pedidos preservados: 7

A comunicação entre Postman, FastAPI e MySQL foi restabelecida na porta original.

A instância temporária da porta 8001 foi encerrada após a recuperação.

**Estado final:** Serviço operacional na porta 8000.

## 13. Análise da Causa

### Causa da Falha Simulada

A falha inicial foi provocada intencionalmente pela alteração da porta MySQL de 3306 para 3399.

A tentativa de ligação à porta incorreta originou o erro MySQL 2003.

O tratamento da exceção na aplicação devolveu HTTP 503.

### Problema Adicional Durante a Recuperação

Durante o restabelecimento do serviço, foi identificado um conflito na porta HTTP 8000.

A investigação encontrou um processo Python residual associado à execução anterior do Uvicorn.

Após o encerramento do processo identificado, a porta 8000 ficou disponível.

### Distinção entre as Falhas

Os problemas tinham naturezas diferentes:

1. **MySQL 2003:** falha de conectividade com a base de dados.
2. **HTTP 503:** resposta da aplicação à indisponibilidade do MySQL.
3. **Windows 10048:** conflito ao tentar iniciar o servidor HTTP numa porta já ocupada.

O conflito da porta 8000 ocorreu durante a investigação e recuperação; não deve ser confundido com a causa original da falha MySQL.

## 14. Impacto e Integridade dos Dados

Durante a simulação:

- Não foram apagados pedidos.
- Não foram executadas operações de alteração da tabela.
- O serviço MySQL não foi interrompido.
- As credenciais da base de dados não foram modificadas.
- Os sete pedidos existentes permaneceram armazenados.

A integridade dos dados foi confirmada através de consultas SQL e da recuperação do endpoint GET `/pedidos`.

## 15. Linha Temporal da Investigação

| Etapa | Ocorrência | Resultado |
|---|---|---|
| 1 | Validação inicial | HTTP 200 |
| 2 | Alteração da porta MySQL | 3306 → 3399 |
| 3 | Teste direto Python–MySQL | Erro 2003 |
| 4 | Reprodução da falha na API | HTTP 503 |
| 5 | Restauração da configuração MySQL | Ligação direta recuperada |
| 6 | Investigação dos processos Uvicorn | Conflito na porta 8000 |
| 7 | Inicialização na porta 8001 | HTTP 200 |
| 8 | Encerramento do processo residual | Porta 8000 libertada |
| 9 | Reinício na porta original | HTTP 200 |
| 10 | Validação final | 3/3 testes aprovados |

## 16. Evidências

### Evidência 1 — Estado Inicial

**Ficheiro:** `INC-API-002_01_ESTADO_INICIAL_200.png`

![Estado inicial — HTTP 200](../Evidencias/INC-API-002_01_ESTADO_INICIAL_200.png)

### Evidência 2 — Falha HTTP 503

**Ficheiro:** `INC-API-002_02_FALHA_MYSQL_503.png`

![Falha de ligação MySQL — HTTP 503](../Evidencias/INC-API-002_02_FALHA_MYSQL_503.png)

### Evidência 3 — Recuperação Definitiva

**Ficheiro:** `INC-API-002_04_RECUPERACAO_FINAL_8000.png`

![Recuperação definitiva na porta 8000](../Evidencias/INC-API-002_04_RECUPERACAO_FINAL_8000.png)

## 17. Recomendações Preventivas

- Confirmar as variáveis de ambiente utilizadas pela aplicação antes de iniciar o servidor.
- Evitar a execução simultânea de várias instâncias desnecessárias do Uvicorn.
- Verificar a disponibilidade da porta HTTP antes de iniciar uma nova instância.
- Utilizar logs para identificar falhas de conectividade.
- Documentar alterações temporárias de configuração.
- Restaurar as configurações originais após os testes.
- Validar a recuperação através de testes HTTP e consultas SQL.
- Evitar expor credenciais ou detalhes sensíveis nas respostas da API.

## 18. Competências Demonstradas

- Investigação de incidentes aplicacionais.
- Diagnóstico de conectividade Python–MySQL.
- Interpretação de erros MySQL 2003.
- Análise de respostas HTTP 503.
- Verificação de variáveis de ambiente.
- Utilização de PowerShell para diagnóstico.
- Identificação de processos Python.
- Análise de conflitos de portas TCP.
- Gestão de instâncias Uvicorn.
- Recuperação de serviços aplicacionais.
- Validação de integridade de dados.
- Utilização de testes automáticos para validar a recuperação.
- Produção de documentação técnica.

## 19. Conclusão

O incidente simulado INC-API-002 permitiu reproduzir uma falha de comunicação entre FastAPI e MySQL e validar o comportamento HTTP 503.

Durante a recuperação, foi identificado um segundo problema relacionado com a ocupação da porta HTTP 8000 por um processo Python residual.

Após a restauração da configuração MySQL e a libertação da porta HTTP, a aplicação voltou a funcionar no endereço original.

A recuperação foi confirmada através de HTTP 200 OK e três testes automáticos aprovados.

**Estado final: Resolvido e validado.**

---

*Laboratório desenvolvido com dados fictícios, num ambiente local e controlado, para demonstração de competências*
