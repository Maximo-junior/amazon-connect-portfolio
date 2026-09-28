# 🏛️ Arquitetura Detalhada — Projeto 7: Ares Serverless

## 1. Visão do Fluxo de Dados

A arquitetura foi desenhada para executar uma consulta transacional de exames por voz, utilizando o Amazon Connect como camada de atendimento, AWS Lambda para processamento da regra de negócio e Amazon DynamoDB para persistência dos dados.

### Sequência Transacional

1. **Entrada Telefônica (PSTN):**
   A chamada externa chega ao número telefônico associado ao Amazon Connect e é direcionada ao contact flow `AR_CF_Consulta_Serverless`.

2. **Setup de Áudio e Governança:**
   O fluxo configura a voz neural `Vitória` (`pt-BR`) para as mensagens de voz e habilita o registro de logs da execução do contact flow.

3. **Captura DTMF:**
   O bloco `AR_GetPacienteId` reproduz a mensagem de orientação e solicita que o usuário informe os 4 dígitos do identificador do exame. O bloco possui limite de entrada e controle de tempo entre os dígitos.

4. **Persistência de Contexto:**
   O bloco `AR_SetPacienteId` utiliza o valor capturado em `$.StoredCustomerInput` e o armazena como atributo de contato `PacienteId` no namespace de atributos definidos pelo usuário.

5. **Invocação Síncrona:**
   O bloco `AR_InvokeConsultaExame` invoca a função Lambda `AR_LF_ConsultaExame` de forma síncrona e envia `PacienteId` como parâmetro dinâmico da chamada.

6. **Lookup NoSQL:**
   A Lambda consulta a tabela `AR_TB_Pacientes` utilizando `GetItem` e a chave `PacienteId`.

7. **Retorno Estruturado:**
   A Lambda retorna os dados em formato compatível com `STRING_MAP`, permitindo que o Amazon Connect disponibilize os valores retornados como atributos externos da execução.

8. **Decisão e Ramificação:**
   O bloco `AR_CheckStatusRetorno` avalia `$.External.status` e direciona a chamada conforme o resultado:

   * `FOUND`: direciona para a mensagem com os dados do exame e do laudo.
   * `NOT_FOUND`: direciona para a mensagem informando que nenhum exame foi localizado para o identificador informado.
   * **Falha de invocação/timeout:** direciona para o tratamento de falha técnica e tentativa de transferência para atendimento humano.
   * **Status inesperado:** direciona para o tratamento de status não reconhecido e posterior transferência para a fila `AR_Q_Consultas`.

---

## 2. Contrato de Interface — Amazon Connect → AWS Lambda

### Payload conceitual

O Amazon Connect envia o identificador do paciente/exame como parâmetro da invocação da Lambda.

Exemplo simplificado:

```json
{
  "Details": {
    "Parameters": {
      "PacienteId": "1001"
    }
  }
}
```

A Lambda utiliza esse parâmetro para realizar a consulta na tabela `AR_TB_Pacientes`.

> **Nota:** O payload completo recebido pela Lambda também contém informações de contexto do contato, como `ContactData`, mas o parâmetro utilizado pela regra de negócio neste projeto é `PacienteId`.

### Parâmetro de entrada

| Campo            | Valor                     |
| ---------------- | ------------------------- |
| Chave            | `PacienteId`              |
| Origem           | Atributo de contato       |
| Valor de exemplo | `1001`                    |
| Tipo             | String                    |
| Origem dinâmica  | `$.Attributes.PacienteId` |

### Fluxo do parâmetro

```text
DTMF: 1001
    ↓
$.StoredCustomerInput
    ↓
AR_SetPacienteId
    ↓
$.Attributes.PacienteId
    ↓
AR_InvokeConsultaExame
    ↓
Lambda: AR_LF_ConsultaExame
    ↓
DynamoDB: AR_TB_Pacientes
```

---

## 3. Contrato de Retorno — AWS Lambda → Amazon Connect

A Lambda retorna um mapa de strings contendo o status da consulta e, quando encontrado, os dados necessários para a resposta de voz.

Exemplo de sucesso:

```json
{
  "status": "FOUND",
  "nome_paciente": "João da Silva",
  "tipo_exame": "Hemograma",
  "data_exame": "2026-09-25",
  "status_laudo": "Disponível"
}
```

Exemplo de paciente não localizado:

```json
{
  "status": "NOT_FOUND"
}
```

O Amazon Connect utiliza o atributo `status` para determinar a ramificação do fluxo.

---

## 4. Componentes Principais

| Componente                  | Responsabilidade                                          |
| --------------------------- | --------------------------------------------------------- |
| Amazon Connect              | Atendimento telefônico e orquestração do contact flow     |
| `AR_CF_Consulta_Serverless` | Orquestração da transação                                 |
| `AR_GetPacienteId`          | Captura do identificador via DTMF                         |
| `AR_SetPacienteId`          | Persistência do identificador como atributo de contato    |
| `AR_InvokeConsultaExame`    | Invocação síncrona da Lambda                              |
| `AR_LF_ConsultaExame`       | Regra de negócio e consulta ao banco                      |
| `AR_TB_Pacientes`           | Persistência dos dados dos pacientes/exames               |
| `AR_CheckStatusRetorno`     | Avaliação do resultado da consulta                        |
| `AR_Q_Consultas`            | Destino para atendimento humano em cenários de transbordo |
| Amazon CloudWatch           | Observabilidade e logs da execução                        |

---

## 5. Estratégia de Tratamento de Falhas

A arquitetura separa falhas de negócio de falhas técnicas.

### Falha de negócio

Exemplo:

```text
PacienteId não encontrado
        ↓
status = NOT_FOUND
        ↓
Mensagem "exame não localizado"
```

Nesse cenário, a infraestrutura está funcionando; simplesmente não existe registro correspondente ao identificador informado.

### Falha técnica

Exemplo:

```text
Erro/timeout na invocação Lambda
        ↓
Falha técnica
        ↓
Mensagem de indisponibilidade
        ↓
Tentativa de transferência para atendimento humano
```

Essa separação permite que o fluxo apresente uma resposta diferente para um dado inexistente e para uma indisponibilidade técnica.

---

## 6. Fluxo de Alto Nível

```text
┌──────────────────────┐
│      Telefone        │
│       PSTN           │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Amazon Connect     │
│ AR_CF_Consulta_      │
│      Serverless      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Captura DTMF       │
│    PacienteId        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Contact Attribute    │
│ PacienteId = 1001    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      AWS Lambda      │
│ AR_LF_ConsultaExame  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      DynamoDB        │
│   AR_TB_Pacientes    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Status da consulta │
│ FOUND / NOT_FOUND    │
└──────────┬───────────┘
           │
       ┌───┴────┐
       ▼        ▼
    FOUND    NOT_FOUND
       │        │
       ▼        ▼
   Resultado  Mensagem
    do exame  de não
              localização
```

---

## 7. Observabilidade

O contact flow possui logging habilitado para acompanhar a execução da transação.

A função Lambda também registra eventos relevantes da execução, permitindo investigar situações como:

* identificador não localizado;
* execução da função;
* resultado da consulta;
* falhas de processamento;
* comportamento inesperado durante a integração.

Essa camada de observabilidade permite correlacionar a chamada telefônica, a execução do contact flow e o processamento realizado pela Lambda.

---

## 8. Resultado da Arquitetura

O Projeto 7 implementa um fluxo serverless de consulta de exames por voz no qual:

```text
Usuário
   ↓
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
Resultado
   ↓
Resposta de voz
```

A arquitetura mantém a camada de atendimento desacoplada da regra de negócio, permitindo que o Amazon Connect seja responsável pela experiência de voz e orquestração, enquanto a Lambda concentra o processamento e o DynamoDB fornece a persistência dos dados.
