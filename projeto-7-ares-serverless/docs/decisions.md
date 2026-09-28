# 🧭 Registros de Decisões Arquiteturais (ADRs)

## Projeto 7 — Ares Serverless

Este documento registra as principais decisões técnicas adotadas durante a implementação do projeto.

---

## ADR 001 — DynamoDB On-Demand

**Contexto**

A tabela `AR_TB_Pacientes` armazena os dados utilizados pela consulta automatizada de exames.

O volume esperado de consultas é baixo e pode variar, sem necessidade de manter capacidade de leitura e escrita provisionada continuamente.

**Decisão**

Utilizar o modo **On-Demand (`PAY_PER_REQUEST`)** do Amazon DynamoDB.

**Justificativa**

* O volume de requisições é esporádico e imprevisível.
* Não é necessário definir capacidade fixa de leitura e escrita.
* O modelo acompanha a utilização real da aplicação.
* Simplifica a operação do banco para o cenário do projeto.

**Consequência**

A tabela não exige configuração manual de RCU/WCU para o cenário implementado, e o custo varia conforme a utilização efetiva do serviço.

---

## ADR 002 — Invocação Síncrona da Lambda

**Contexto**

O Contact Flow precisa receber o resultado da consulta antes de decidir qual caminho seguir.

A resposta da Lambda determina se o paciente foi encontrado, não foi localizado ou se ocorreu alguma falha durante a consulta.

**Decisão**

Utilizar a Lambda `AR_LF_ConsultaExame` com **invocação síncrona** e **timeout de 3 segundos**.

**Justificativa**

A execução síncrona permite que o Contact Flow aguarde o resultado da consulta e utilize os dados retornados para continuar o atendimento.

O timeout de 3 segundos mantém uma janela controlada para a execução da função, enquanto o fluxo possui tratamento específico para falhas de invocação ou timeout.

**Consequência**

O fluxo pode tomar decisões com base no resultado retornado pela Lambda:

* `FOUND` → apresenta os dados do exame ao paciente.
* `NOT_FOUND` → informa que o identificador não foi localizado.
* Falha de execução ou timeout → informa indisponibilidade e direciona para atendimento humano.
* Status inesperado → direciona para tratamento específico e, posteriormente, atendimento humano.

---

## ADR 003 — Persistência do Identificador como Atributo de Contato

**Contexto**

O identificador informado pelo paciente via DTMF precisa ser reutilizado posteriormente na chamada da Lambda.

**Decisão**

Armazenar o valor recebido em um atributo de contato chamado `PacienteId`.

**Fluxo**

```text
DTMF
  ↓
$.StoredCustomerInput
  ↓
AR_SetPacienteId
  ↓
$.Attributes.PacienteId
  ↓
AR_InvokeConsultaExame
```

**Justificativa**

O uso de um atributo de contato permite manter o identificador durante a execução do Contact Flow e utilizá-lo como parâmetro da Lambda.

**Consequência**

O valor informado pelo paciente pode ser enviado dinamicamente para a Lambda sem necessidade de valores fixos no Contact Flow.

---

## ADR 004 — Retorno Estruturado da Lambda

**Contexto**

O Contact Flow precisa diferenciar os resultados da consulta para direcionar o atendimento para caminhos distintos.

**Decisão**

A Lambda retorna um objeto estruturado contendo, entre outros campos, o atributo `status`.

Exemplos:

```json
{
  "status": "FOUND",
  "nome_paciente": "Paciente Teste",
  "tipo_exame": "Exame de imagem",
  "data_exame": "2026-09-24",
  "status_laudo": "Disponível"
}
```

```json
{
  "status": "NOT_FOUND"
}
```

**Justificativa**

Um retorno estruturado permite separar a lógica de negócio da lógica de roteamento do Contact Flow.

**Consequência**

O bloco `AR_CheckStatusRetorno` pode avaliar `$.External.status` e direcionar a chamada para o tratamento correspondente.

---

## ADR 005 — Tratamento Explícito de Falhas

**Contexto**

Uma aplicação de atendimento telefônico precisa possuir comportamento definido para situações em que a consulta automática não pode ser concluída.

**Decisão**

Implementar caminhos específicos para:

* entrada inválida ou timeout de DTMF;
* erro na execução da Lambda;
* timeout da Lambda;
* paciente não localizado;
* status inesperado retornado pela consulta.

**Justificativa**

Evita que uma falha técnica resulte em uma experiência sem tratamento para o paciente.

**Consequência**

Falhas técnicas podem ser comunicadas por voz e direcionadas para a fila `AR_Q_Consultas`, permitindo continuidade do atendimento por um agente.

---

## ADR 006 — Consulta por DTMF

**Contexto**

O projeto precisa permitir que o paciente informe seu identificador utilizando uma chamada telefônica convencional.

**Decisão**

Utilizar entrada DTMF com limite de **4 dígitos**.

**Justificativa**

O identificador utilizado no cenário de demonstração possui quatro dígitos e o DTMF permite realizar a consulta diretamente pelo telefone, sem depender de uma aplicação web ou aplicativo móvel.

**Consequência**

O paciente informa o identificador pelo teclado do telefone e o valor é utilizado pelo fluxo serverless para realizar a consulta.

---

## Resumo das decisões

| Decisão                       | Implementação             |
| ----------------------------- | ------------------------- |
| Banco de dados                | DynamoDB On-Demand        |
| Persistência do identificador | Atributo `PacienteId`     |
| Entrada do paciente           | DTMF                      |
| Limite de entrada             | 4 dígitos                 |
| Computação                    | AWS Lambda                |
| Invocação                     | Síncrona                  |
| Timeout da Lambda             | 3 segundos                |
| Contrato de retorno           | `STRING_MAP`              |
| Status principal              | `FOUND` / `NOT_FOUND`     |
| Tratamento de falhas          | Fluxos específicos + fila |
| Atendimento humano            | `AR_Q_Consultas`          |

---

## Resultado

As decisões foram aplicadas no Contact Flow `AR_CF_Consulta_Serverless` e validadas por meio de chamadas telefônicas reais utilizando o número DID associado ao Amazon Connect.

O fluxo foi validado com cenários de sucesso, paciente não localizado, entradas inválidas e tratamento de falhas.
