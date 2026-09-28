# 🏥 Projeto 7 — Ares Serverless: Consulta Automatizada de Exames

> **Classificação de Implementação:** 🟢 IMPLEMENTADO E VALIDADO
> **Status:** Homologado de ponta a ponta com tráfego telefônico real (PSTN/DDI), processamento serverless síncrono e banco de dados NoSQL.

---

## 🎯 Visão Geral do Projeto

No contexto do **Complexo Hospitalar Ares**, o **Projeto 7** implementa uma camada de autosserviço transacional para consulta de exames por voz.

O objetivo é permitir que o paciente ligue para a central, informe o identificador do exame utilizando o teclado telefônico (DTMF) e receba automaticamente, por voz neural, o resultado da consulta armazenado na base de dados.

Quando a consulta não pode ser concluída automaticamente, o fluxo possui mecanismos de tratamento de falhas e transbordo para atendimento humano.

---

## 🏗️ Arquitetura da Solução

A solução utiliza Amazon Connect, AWS Lambda e Amazon DynamoDB em uma arquitetura síncrona e desacoplada.

```text
[ Paciente / Telefone ]
          │
          │ Chamada telefônica PSTN
          ▼
[ Amazon Connect ]
          │
          │ Contact Flow
          ▼
[ AR_CF_Consulta_Serverless ]
          │
          │ Captura de 4 dígitos DTMF
          ▼
[ AR_SetPacienteId ]
          │
          │ $.Attributes.PacienteId
          ▼
[ AWS Lambda ]
[ AR_LF_ConsultaExame ]
          │
          │ GetItem
          ▼
[ Amazon DynamoDB ]
[ AR_TB_Pacientes ]
          │
          │ Resultado
          ▼
[ AR_CheckStatusRetorno ]
          │
       ┌──┴───────────────┐
       │                  │
    FOUND             NOT_FOUND
       │                  │
       ▼                  ▼
[ Dados do exame ]   [ Não localizado ]
       │
       ▼
[ Amazon Connect / Polly ]
       │
       ▼
[ Resposta de voz ]
```

---

## 🔄 Fluxo Transacional

### 1. Entrada da chamada

O paciente realiza uma chamada para o número telefônico associado ao Amazon Connect.

A chamada é direcionada para o contact flow:

```text
AR_CF_Consulta_Serverless
```

### 2. Captura do identificador

O bloco:

```text
AR_GetPacienteId
```

solicita ao paciente que informe os quatro dígitos do identificador utilizando DTMF.

O valor informado é armazenado pelo Amazon Connect em:

```text
$.StoredCustomerInput
```

### 3. Persistência do contexto

O bloco:

```text
AR_SetPacienteId
```

converte o valor capturado em um atributo de contato:

```text
$.Attributes.PacienteId
```

Exemplo:

```text
Paciente digita: 1001
        ↓
StoredCustomerInput
        ↓
PacienteId = 1001
```

### 4. Invocação da Lambda

O bloco:

```text
AR_InvokeConsultaExame
```

realiza uma invocação **síncrona** da função:

```text
AR_LF_ConsultaExame
```

O `PacienteId` é enviado dinamicamente como parâmetro.

Exemplo conceitual:

```json
{
  "Details": {
    "Parameters": {
      "PacienteId": "1001"
    }
  }
}
```

### 5. Consulta ao DynamoDB

A Lambda utiliza o `PacienteId` para executar uma consulta pontual (`GetItem`) na tabela:

```text
AR_TB_Pacientes
```

A tabela funciona como fonte dos dados utilizados na consulta automatizada.

### 6. Processamento do resultado

A Lambda retorna um mapa de strings (`STRING_MAP`) para o Amazon Connect.

Exemplo de retorno encontrado:

```json
{
  "status": "FOUND",
  "nome_paciente": "João da Silva",
  "tipo_exame": "Hemograma",
  "data_exame": "2026-09-25",
  "status_laudo": "Disponível"
}
```

Quando não existe registro:

```json
{
  "status": "NOT_FOUND"
}
```

### 7. Decisão no Contact Flow

O bloco:

```text
AR_CheckStatusRetorno
```

avalia:

```text
$.External.status
```

e direciona a execução conforme o resultado.

| Status            | Comportamento                                                |
| ----------------- | ------------------------------------------------------------ |
| `FOUND`           | Reproduz os dados do exame por voz                           |
| `NOT_FOUND`       | Informa que não foi localizado um exame para o identificador |
| Falha técnica     | Informa indisponibilidade e tenta realizar transbordo        |
| Status inesperado | Direciona para tratamento de status não reconhecido          |

---

## 🗣️ Experiência de Voz

A resposta ao paciente utiliza voz neural em português brasileiro:

```text
Voz: Vitória
Idioma: pt-BR
Engine: Neural
```

Em caso de resultado encontrado, o Contact Flow utiliza atributos retornados pela Lambda para construir dinamicamente a mensagem.

Exemplo:

```text
Olá, João. Localizamos seu exame de Hemograma realizado em
25/09/2026. O laudo consta como disponível.
```

Os valores são interpolados diretamente no Contact Flow por meio de atributos externos, como:

```text
$.External.nome_paciente
$.External.tipo_exame
$.External.data_exame
$.External.status_laudo
```

---

## 🛡️ Tratamento de Falhas

O projeto diferencia falhas de negócio de falhas técnicas.

### Paciente não localizado

```text
PacienteId
    ↓
DynamoDB
    ↓
Nenhum registro
    ↓
NOT_FOUND
    ↓
Mensagem de não localização
```

### Falha técnica

```text
Lambda / integração
        ↓
Erro ou timeout
        ↓
AR_Msg_FalhaTecnica
        ↓
Tentativa de transbordo
        ↓
AR_Q_Consultas
```

### Status inesperado

```text
Resultado não reconhecido
        ↓
AR_Msg_StatusInesperado
        ↓
AR_Q_Consultas
```

---

## 🧩 Componentes AWS

| Serviço / Componente  | Responsabilidade                      |
| --------------------- | ------------------------------------- |
| **Amazon Connect**    | Atendimento telefônico e orquestração |
| **Contact Flow**      | Controle da jornada transacional      |
| **AWS Lambda**        | Processamento da consulta             |
| **Amazon DynamoDB**   | Persistência dos dados                |
| **Amazon Polly**      | Síntese neural de voz                 |
| **Amazon CloudWatch** | Logs e observabilidade                |

### Componentes do Contact Flow

| Bloco                     | Função                                 |
| ------------------------- | -------------------------------------- |
| `AR_GetPacienteId`        | Captura do identificador via DTMF      |
| `AR_SetPacienteId`        | Armazena o identificador como atributo |
| `AR_InvokeConsultaExame`  | Invoca a Lambda                        |
| `AR_CheckStatusRetorno`   | Avalia o resultado                     |
| `AR_Msg_LaudoDisponivel`  | Resposta para consulta encontrada      |
| `AR_Msg_NaoLocalizado`    | Resposta para consulta não encontrada  |
| `AR_Msg_FalhaTecnica`     | Tratamento de falhas                   |
| `AR_Msg_StatusInesperado` | Tratamento de respostas inesperadas    |
| `AR_Q_Consultas`          | Fila de transbordo                     |

---

## 🧪 Cenários Validados

O fluxo foi testado utilizando chamadas telefônicas reais.

### Cenário 1 — Consulta encontrada

```text
Entrada: 1001
Resultado: FOUND
Comportamento: dados do exame reproduzidos por voz
```

### Cenário 2 — Consulta não encontrada

```text
Entrada: 9999
Resultado: NOT_FOUND
Comportamento: mensagem informando que nenhum exame foi localizado
```

### Cenário 3 — Entrada inválida / timeout

```text
Entrada inválida ou ausência de entrada
Resultado: falha de captura
Comportamento: mensagem de falha técnica / transbordo
```

### Cenário 4 — Status inesperado

```text
Status diferente de FOUND / NOT_FOUND
Resultado: status inesperado
Comportamento: tratamento de status + transbordo
```

---

## 📊 Observabilidade

O Contact Flow possui logging habilitado para permitir o acompanhamento da execução.

A AWS Lambda também registra eventos relevantes da execução, permitindo investigar:

* execução da função;
* identificadores consultados;
* resultado da consulta;
* pacientes não localizados;
* falhas de processamento;
* comportamento inesperado.

A observabilidade permite correlacionar o comportamento do Contact Flow com o processamento realizado pela Lambda.

---

## 💰 Estratégia de Custo

O projeto foi desenvolvido priorizando componentes serverless e recursos de baixo acoplamento operacional.

A arquitetura utiliza:

* Amazon Connect;
* AWS Lambda;
* Amazon DynamoDB;
* Amazon CloudWatch;
* Amazon Polly.

Os testes de desenvolvimento foram realizados com foco em controle de consumo e uso consciente dos recursos da AWS.

> **Nota:** custos de telefonia/PSTN, uso do Amazon Connect e demais serviços dependem da região, volume de utilização e recursos efetivamente consumidos.

---

## 📁 Estrutura do Projeto

```text
projeto-7-ares-serverless/
│
├── README.md
├── ARCHITECTURE.md
│
├── lambda/
│   └── AR_LF_ConsultaExame/
│       └── lambda_function.py
│
├── contact-flow/
│   └── AR_CF_Consulta_Serverless.json
│
├── dynamodb/
│   └── AR_TB_Pacientes.json
│
└── docs/
    └── screenshots/
```

---

## 🚀 Resultado

O **Projeto 7 — Ares Serverless** demonstra uma integração completa entre atendimento de voz, captura de dados via DTMF, atributos de contato, processamento serverless e persistência NoSQL.

A jornada implementada é:

```text
Telefone
   ↓
Amazon Connect
   ↓
DTMF
   ↓
Contact Attribute
   ↓
AWS Lambda
   ↓
DynamoDB
   ↓
Resultado da consulta
   ↓
Amazon Connect
   ↓
Voz neural
   ↓
Paciente
```

O projeto foi **implementado, publicado e validado através de chamadas telefônicas reais**, incluindo cenários de sucesso, ausência de registro e tratamento de falhas.
