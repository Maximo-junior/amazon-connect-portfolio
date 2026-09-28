# 🧪 Relatório de Testes e Troubleshooting — Projeto 7

## 1. Matriz de Homologação E2E

As validações foram realizadas por meio de chamadas telefônicas reais para o número DID associado ao Amazon Connect, utilizando a rede telefônica pública (PSTN).

O objetivo foi validar o fluxo completo:

```text
Chamada telefônica
      ↓
Amazon Connect
      ↓
Coleta DTMF
      ↓
Atributo PacienteId
      ↓
AWS Lambda
      ↓
DynamoDB
      ↓
Resultado da consulta
      ↓
Resposta por voz
```

---

### `TC-E2E-001`: Happy Path — Laudo Disponível

* **Entrada DTMF:** `1001`
* **Resultado esperado:** Identificar o paciente e reproduzir as informações do exame com status `Disponível`.
* **Resultado obtido:** A voz neural Vitória informou:

> "Olá, Carlos Eduardo. Localizamos seu exame de Ressonância Magnética realizado em 28/10. O laudo consta como: Disponível. O Complexo Hospitalar Ares agradece a sua ligação."

* **Status:** 🟢 PASS

---

### `TC-E2E-002`: Regra de Negócio — Laudo Em Análise

* **Entrada DTMF:** `1002`
* **Resultado esperado:** Identificar o paciente e reproduzir o exame com status `Em Análise`.
* **Resultado obtido:** A voz neural informou:

> "Olá, Mariana Souza. Localizamos seu exame de Hemograma Completo realizado em 29/10. O laudo consta como: Em Análise."

* **Status:** 🟢 PASS

---

### `TC-E2E-003`: Regra de Negócio — Laudo Pendente

* **Entrada DTMF:** `1003`
* **Resultado esperado:** Identificar o paciente e reproduzir o exame com status `Pendente`.
* **Resultado obtido:** A voz neural informou:

> "Olá, Beatriz Lima. Localizamos seu exame de Ecocardiograma realizado em 30/10. O laudo consta como: Pendente."

* **Status:** 🟢 PASS

---

### `TC-E2E-004`: Unhappy Path — Identificador Inexistente

* **Entrada DTMF:** `9999`
* **Resultado esperado:** A Lambda retornar `NOT_FOUND` e o Contact Flow informar que nenhum exame foi localizado.
* **Resultado obtido:** A voz neural informou:

> "Não localizamos nenhum exame cadastrado para este identificador. Por favor, confirme os dados com a nossa equipe de atendimento."

* **Status:** 🟢 PASS

---

### `TC-E2E-005`: Timeout de Entrada DTMF

* **Entrada:** Nenhuma tecla pressionada durante o período configurado.
* **Resultado esperado:** O bloco de coleta de DTMF atingir o limite de espera e seguir para o tratamento de erro configurado.
* **Resultado obtido:** O fluxo executou o tratamento de contingência e direcionou a chamada para o caminho configurado para atendimento humano.
* **Status:** 🟢 PASS

---

## 2. Troubleshooting e Incidentes

Durante a implementação, foram identificados e corrigidos problemas de configuração no ambiente.

### Incidente 1 — Chamada não era atendida pela URA

**Sintoma**

Ao realizar a chamada para o DID, a chamada permanecia em estado de conexão e o Contact Flow não era executado.

**Investigação**

Foi realizada a verificação da configuração de telefonia da instância Amazon Connect e dos registros disponíveis para o fluxo.

**Causa**

A opção de recebimento de chamadas de entrada do Amazon Connect estava desabilitada na configuração de telefonia da instância.

**Correção**

A opção de chamadas de entrada foi habilitada e a configuração da instância foi salva.

**Resultado**

Após a alteração, as chamadas passaram a ser recebidas pelo Amazon Connect e o Contact Flow foi executado normalmente.

---

### Incidente 2 — Lambda retornava `NOT_FOUND` para o identificador `1001`

**Sintoma**

A URA recebia a chamada e capturava corretamente o identificador `1001`, porém a Lambda retornava `NOT_FOUND`, mesmo existindo um registro correspondente no DynamoDB.

**Investigação**

A análise dos logs da Lambda no CloudWatch indicou que o identificador recebido não correspondia ao registro esperado.

Ao revisar o bloco `AR_InvokeConsultaExame`, foi identificado que o parâmetro `PacienteId` estava sendo enviado de forma incorreta, como valor literal, em vez de utilizar o atributo coletado durante a chamada.

**Causa raiz**

O parâmetro estava configurado como valor fixo:

```text
PacienteId = "PacienteId"
```

em vez de utilizar dinamicamente o atributo de contato:

```text
$.Attributes.PacienteId
```

**Correção**

O parâmetro `PacienteId` foi configurado no bloco `AR_InvokeConsultaExame` para utilizar dinamicamente o atributo definido pelo Contact Flow.

Configuração final:

```text
Lambda:
AR_LF_ConsultaExame

Modo:
Síncrono

Parâmetro:
PacienteId

Origem:
User defined → PacienteId
```

**Resultado**

Após a correção, o identificador `1001` passou a ser enviado corretamente para a Lambda, permitindo a consulta do registro no DynamoDB.

O fluxo foi posteriormente validado por chamada telefônica real.

---

## 3. Cenários Validados

| Cenário                              |         Entrada | Resultado              |  Status |
| ------------------------------------ | --------------: | ---------------------- | :-----: |
| Paciente encontrado — Disponível     |          `1001` | Laudo reproduzido      | 🟢 PASS |
| Paciente encontrado — Em Análise     |          `1002` | Status reproduzido     | 🟢 PASS |
| Paciente encontrado — Pendente       |          `1003` | Status reproduzido     | 🟢 PASS |
| Identificador inexistente            |          `9999` | `NOT_FOUND` tratado    | 🟢 PASS |
| Timeout de DTMF                      | Nenhuma entrada | Contingência executada | 🟢 PASS |
| Chamada recebida pelo Amazon Connect |               — | Contact Flow executado | 🟢 PASS |
| Integração Connect → Lambda          |    `PacienteId` | Consulta executada     | 🟢 PASS |
| Lambda → DynamoDB                    |    `PacienteId` | Registro consultado    | 🟢 PASS |

---

## 4. Resultado da Homologação

O Projeto 7 foi validado de ponta a ponta utilizando tráfego telefônico real.

A homologação confirmou a integração entre:

* Amazon Connect;
* Contact Flow;
* entrada DTMF;
* atributos de contato;
* AWS Lambda;
* Amazon DynamoDB;
* processamento do resultado;
* resposta por voz;
* tratamento de exceções e contingências.

O fluxo principal e os cenários de erro previstos foram executados com sucesso.
