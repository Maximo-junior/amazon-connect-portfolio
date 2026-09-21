# 🤖 Ares Inteligente — IA Conversacional e Serverless (Projeto 5)

**Amazon Connect Engineering Portfolio | Nível: Avançado**

---

## 🎯 Visão Geral

O Projeto 5 introduz a camada de **Autosserviço Resolutivo (First Contact Resolution — FCR)** no Hospital Ares, utilizando uma arquitetura orientada a AWS Lambda, modelagem de interfaces para NLU e integração com Amazon Connect.

O fluxo `AR_CF_Ares_Inteligente` representa um cenário de atendimento automatizado para consulta de laudos de exames, reduzindo a necessidade de triagem manual e mantendo rotas de contingência para atendimento humano.

> **Nota de arquitetura:** neste projeto, a infraestrutura AWS não é provisionada nem executada em ambiente tarifado. A Lambda é desenvolvida localmente em Python e seu comportamento é validado por meio de eventos JSON, respostas simuladas e contratos de integração versionados no repositório.

---

## 🏛️ Destaques da Arquitetura

- **Autosserviço Serverless:** função Python `consulta_exame.py`, desenvolvida localmente como representação do backend `AR_LF_ConsultaExame`, preparada para uma futura integração com sistemas de prontuário eletrônico.
- **Modelagem de Contratos de Integração:** especificação formal dos eventos de entrada (`event-connect-request.json`) e dos possíveis resultados de negócio, incluindo `FOUND`, `NOT_FOUND`, `TIMEOUT` e `ERROR`.
- **Reutilização Modular:** utilização dos submódulos desenvolvidos no Projeto 4:
  - `AR_MD_Inicializacao`
  - `AR_MD_Verifica_Horario`
  - `AR_MD_Tratamento_Erros`
- **Transbordo Assistido:** rota direta para a fila departamental `AR_Q_Consultas` caso o paciente solicite atendimento humano ou ocorra uma condição que impeça o autosserviço.
- **Modelagem NLU / DTMF:** representação de entrada do cliente utilizando linguagem natural e DTMF, permitindo diferentes formas de interação com o fluxo.
- **Política FinOps — R$ 0,00:** desenvolvimento e validação realizados localmente, sem implantação ou execução de recursos AWS tarifados neste projeto.

---

## 📁 Estrutura do Projeto

```text
projeto-5-ares-inteligente/
│
├── README.md
│
├── docs/
│   ├── architecture.md
│   ├── decisions.md
│   ├── testing.md
│   └── troubleshooting.md
│
├── evidence/
│   └── diagramas/
│       └── AR_CF_Ares_Inteligente.png
│
├── simulations/
│   └── lambda/
│       ├── event-connect-request.json
│       ├── response-found.json
│       ├── response-not-found.json
│       ├── response-timeout.json
│       └── response-error.json
│
└── src/
    ├── contact-flows/
    │   └── AR_CF_Ares_Inteligente.json
    │
    └── lambda/
        └── consulta_exame.py
```

---

## 🏗️ Diagrama Lógico de Integração

```text
                         ┌──────────────────────────────────┐
                         │   Chamada Entrante do Paciente   │
                         └────────────────┬─────────────────┘
                                          │
                                          ▼
                         ┌──────────────────────────────────┐
                         │   AR_MD_Inicializacao            │
                         │   Logs + Voz                     │
                         └────────────────┬─────────────────┘
                                          │
                                   (Sucesso)
                                          │
                                          ▼
                         ┌──────────────────────────────────┐
                         │   AR_MD_Verifica_Horario         │
                         └────────────────┬─────────────────┘
                                          │
                                  (Dentro do Horário)
                                          │
                                          ▼
                         ┌──────────────────────────────────┐
                         │   AR_CF_Ares_Inteligente         │
                         │   Get Customer Input             │
                         │   NLU / DTMF                     │
                         └───────────────┬───────────┬──────┘
                                         │           │
                      (Branch 1: Exames) │           │ (Branch 2: Transbordo)
                                         ▼           ▼
                          ┌─────────────────────┐  ┌─────────────────────┐
                          │ AR_LF_ConsultaExame │  │ Definir Fila:       │
                          │ Lambda modelada     │  │ AR_Q_Consultas      │
                          │ Execução simulada   │  └──────────┬──────────┘
                          └──────────┬──────────┘             │
                                     │                        ▼
                                     ▼              ┌─────────────────────┐
                          ┌─────────────────────┐   │ Transferir para     │
                          │ Play Prompt         │   │ Fila                │
                          │ Resultado dinâmico  │   └─────────────────────┘
                          └──────────┬──────────┘
                                     │
                                     ▼
                          ┌─────────────────────┐
                          │ Encerramento        │
                          │ / Desconexão        │
                          └─────────────────────┘
```

---

## 🧠 Fluxo de Negócio

O fluxo segue uma sequência lógica de atendimento:

1. O paciente inicia a chamada.
2. O módulo `AR_MD_Inicializacao` realiza a preparação inicial do contato.
3. O módulo `AR_MD_Verifica_Horario` valida o horário de atendimento.
4. O fluxo `AR_CF_Ares_Inteligente` coleta a intenção do paciente utilizando NLU ou DTMF.
5. Quando a intenção corresponde à consulta de exames, o fluxo direciona a requisição para `AR_LF_ConsultaExame`.
6. A função processa o evento de entrada e retorna um contrato de resposta.
7. O resultado pode representar:
   - `FOUND` — laudo localizado;
   - `NOT_FOUND` — laudo não localizado;
   - `TIMEOUT` — indisponibilidade ou expiração da consulta;
   - `ERROR` — erro no processamento.
8. O Contact Flow utiliza o resultado para determinar a próxima ação.
9. Quando necessário, o paciente é direcionado para a fila `AR_Q_Consultas`.

---

## 🐍 Desenvolvimento Local da Lambda

A função `AR_LF_ConsultaExame` é desenvolvida em **Python**, utilizando o **VS Code** como ambiente de desenvolvimento.

A implementação permanece dentro do repositório Git e é tratada como um artefato de software versionável.

O fluxo de desenvolvimento adotado é:

```text
VS Code
   ↓
Python
   ↓
Eventos JSON
   ↓
Testes e simulações locais
   ↓
Git / Versionamento
   ↓
Futura possibilidade de CI/CD
   ↓
AWS Lambda
```

Neste Projeto 5, a última etapa **não é executada**.

A AWS Lambda é utilizada como referência arquitetural e modelo de execução, enquanto o comportamento da função é validado localmente.

---

## 💰 Política FinOps

O Projeto 5 possui como requisito a manutenção de:

> **Custo Real = R$ 0,00**

Por esse motivo:

- Não há implantação da função Lambda em infraestrutura AWS tarifada;
- Não há invocações reais da Lambda;
- Não há integração real com sistemas externos de prontuário;
- Eventos de entrada são representados por arquivos JSON;
- Respostas de negócio são simuladas e versionadas;
- A lógica da função é executada e validada localmente;
- O comportamento esperado da arquitetura é documentado para uma futura implantação.

A decisão de desenvolvimento local está documentada no:

**ADR-008 — Desenvolvimento Local da Lambda e Preservação da Política FinOps**

---

## 🧪 Simulações

Os cenários de integração são representados por contratos JSON dentro de `simulations/lambda/`.

Os cenários contemplados são:

| Cenário | Arquivo | Resultado |
|---|---|---|
| Laudo encontrado | `response-found.json` | `FOUND` |
| Laudo não encontrado | `response-not-found.json` | `NOT_FOUND` |
| Tempo excedido | `response-timeout.json` | `TIMEOUT` |
| Erro de processamento | `response-error.json` | `ERROR` |

Essa abordagem permite validar os diferentes caminhos de negócio sem necessidade de consumir serviços AWS tarifados.

---

## 🔐 Princípios Arquiteturais

O Projeto 5 segue os seguintes princípios:

- **Serverless-first:** arquitetura preparada para execução serverless;
- **Separation of Concerns:** separação entre Contact Flow, lógica de negócio e contratos;
- **Modularidade:** reutilização dos módulos desenvolvidos anteriormente;
- **Versionamento:** artefatos mantidos em Git;
- **Testabilidade:** cenários representados por eventos e respostas determinísticas;
- **Observabilidade futura:** arquitetura preparada para integração com logs e métricas;
- **FinOps:** nenhum consumo de infraestrutura AWS tarifada durante a etapa de portfólio;
- **Evolução incremental:** estrutura preparada para futura integração com APIs, sistemas de prontuário, Amazon Lex e serviços AWS.

---

## 🚀 Evolução Futura

Em uma implementação real, a arquitetura poderia evoluir para:

```text
Amazon Connect
       │
       ▼
Amazon Lex / NLU
       │
       ▼
AWS Lambda
       │
       ▼
API / Sistema de Prontuário
       │
       ▼
Resultado do Exame
       │
       ▼
Amazon Connect
       │
       ├── Autosserviço
       │
       └── Transferência para Atendimento Humano
```

A infraestrutura poderia posteriormente ser provisionada e versionada utilizando Infrastructure as Code, acompanhada de pipeline de CI/CD, observabilidade e controles adicionais de segurança e governança.
