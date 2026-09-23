# 🌐 Amazon Connect Engineering Portfolio — Ecossistema Ares

Este repositório centraliza a construção de soluções de **Contact Center utilizando Amazon Connect** e o ecossistema de nuvem da **Amazon Web Services (AWS)**.

O objetivo deste portfólio é demonstrar, de forma **prática, progressiva e tecnicamente documentada**, conhecimentos em:

* Arquitetura de Contact Center
* Customer Experience (CX)
* Contact Flows
* URA/IVR
* Filas e roteamento
* Contact Attributes
* Arquitetura modular
* AWS Serverless
* APIs e integrações
* IA conversacional
* CTI e CRM
* Segurança e IAM
* Observabilidade
* Governança
* FinOps
* Tratamento de falhas
* Testes e troubleshooting
* Integrações corporativas

Os projetos representam a evolução tecnológica de uma organização de saúde fictícia chamada **Ares Saúde**, partindo de uma estrutura inicial de triagem e evoluindo progressivamente para uma arquitetura de Contact Center integrada a serviços AWS, APIs, CTI e plataformas CRM.

---

## 🗺️ Trilha de Evolução Arquitetural

O Ecossistema Ares Saúde é desenvolvido de forma incremental.

Cada projeto reutiliza conceitos, componentes e decisões dos projetos anteriores, aumentando gradualmente a complexidade técnica da solução.

### 🔹 Fase 1 — Fundação Amazon Connect

| Projeto                                                         | Nível                  | Escopo Técnico Principal                                                        | Status        |
| --------------------------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------- | ------------- |
| 🚀 [Projeto 1 — Ares Triagem Inicial](./projeto-1-triagem-ares) | Básico                 | Contact Flows, URA/IVR, prompts, menus e tratamento de erros                    | **Concluído** |
| 🚀 Projeto 2 — Ares Routing & Queues                            | Básico +               | Queues, Routing Profiles, Hours of Operation, agentes e transbordo              | **Concluído** |
| 🚀 Projeto 3 — Ares Context & Contact Attributes                | Intermediário          | Contact Attributes, contexto de contato, segmentação e roteamento contextual    | **Concluído** |
| 🚀 Projeto 4 — Ares Modular Architecture                        | Intermediário Avançado | Flow Modules, reutilização de componentes e arquitetura multi-departamental     | **Concluído** |
| 🚀 Projeto 5 — Ares Inteligente                                 | Avançado               | Autosserviço, inteligência conversacional, integrações e arquitetura serverless | **Concluído** |
| 🚀 Projeto 6 — Ares Enterprise                                  | Profissional           | Segurança, governança, observabilidade, FinOps e Disaster Recovery              | **Em desenvolvimento** |

---

## 🔹 Fase 2 — AWS Serverless, APIs e Integrações

A segunda fase amplia o Ecossistema Ares para além dos recursos nativos de Contact Flow, introduzindo integrações práticas com serviços AWS e sistemas externos.

| Projeto                                     | Nível        | Escopo Técnico Principal                                                   | Status        |
| ------------------------------------------- | ------------ | -------------------------------------------------------------------------- | ------------- |
| 🔜 Projeto 7 — Ares Serverless              | Avançado     | Amazon Connect, AWS Lambda, DynamoDB, IAM, validação e tratamento de erros | **Planejado** |
| 🔜 Projeto 8 — Ares Conversational          | Avançado     | Amazon Connect, Amazon Lex, Lambda, DynamoDB/API e NLU                     | **Planejado** |
| 🔜 Projeto 9 — Ares API & Integrations      | Avançado     | Lambda, APIs REST, JSON, autenticação, timeout, retry e sistemas externos  | **Planejado** |
| 🔜 Projeto 10 — Ares CTI & CRM Architecture | Profissional | CTI, CRM, contexto de atendimento, Screen Pop e arquitetura de integração  | **Planejado** |

---

## 🔹 Fase 3 — CRM, CTI e Integrações Corporativas

A terceira fase aplica os conceitos desenvolvidos anteriormente em cenários de integração com plataformas CRM utilizadas em ambientes corporativos.

| Projeto                                            | Nível        | Escopo Técnico Principal                                                  | Status        |
| -------------------------------------------------- | ------------ | ------------------------------------------------------------------------- | ------------- |
| 🔜 Projeto 11 — Salesforce Customer Identification | Profissional | Salesforce API, identificação do cliente, Contact Attributes e Screen Pop | **Planejado** |
| 🔜 Projeto 12 — Salesforce Service Automation      | Profissional | Cases, Activities, pós-atendimento, automação e idempotência              | **Planejado** |
| 🔜 Projeto 13 — HubSpot Integration                | Profissional | HubSpot API, contatos, atividades, autenticação e integração com Connect  | **Planejado** |
| 🔜 Projeto 14 — Microsoft Dynamics 365             | Profissional | CTI, Customer Service, Dataverse, Web API e integração com Connect        | **Planejado** |

---

## 🏗️ Evolução da Arquitetura

A arquitetura do Ecossistema Ares evolui progressivamente:

```text
P1
Amazon Connect
      ↓
Contact Flows / URA
      ↓
P2
Queues + Routing
      ↓
P3
Contact Attributes + Contexto
      ↓
P4
Flow Modules + Arquitetura Modular
      ↓
P5
Autosserviço + Inteligência
      ↓
P6
Segurança + Governança + Observabilidade
      ↓
P7
Lambda + DynamoDB
      ↓
P8
Lex + Lambda + Backend
      ↓
P9
APIs + Sistemas Externos
      ↓
P10
CTI + CRM Architecture
      ↓
P11–P14
Salesforce + HubSpot + Dynamics 365
```

O objetivo não é criar projetos independentes, mas demonstrar a **evolução de uma arquitetura de Contact Center ao longo de diferentes níveis de complexidade**.

---

## 🛠️ Stack Tecnológica

### ☁️ Core CCaaS

* Amazon Connect
* Contact Flows
* Queues
* Routing Profiles
* Hours of Operation
* Contact Attributes
* Flow Modules
* Agent Workspace / CCP

### ⚙️ AWS & Serverless

* AWS Lambda
* Amazon DynamoDB
* Amazon Lex
* Amazon Polly
* Amazon CloudWatch
* AWS IAM
* AWS Secrets Manager, quando aplicável
* Outros serviços AWS conforme necessidade arquitetural

### 🔌 Integrações

* APIs REST
* HTTP/JSON
* Autenticação
* OAuth
* Web APIs
* Integrações com sistemas externos
* Tratamento de timeout
* Retry e Backoff
* Idempotência
* Circuit Breaker em cenários aplicáveis

### 🏢 CRM & CTI

* Salesforce
* HubSpot
* Microsoft Dynamics 365
* CTI
* Screen Pop
* Customer Identification
* Cases
* Activities
* Pós-atendimento

### 💻 Desenvolvimento

* Python
* Node.js
* TypeScript
* JavaScript
* Git/GitHub
* Testes automatizados quando aplicável

---

## 💰 FinOps e Política de Execução

O objetivo financeiro do laboratório é manter o **custo operacional em R$ 0,00 sempre que isso for tecnicamente possível**, mas a possibilidade de cobrança **não significa automaticamente que o recurso será proibido ou apenas simulado**.

Antes de executar qualquer recurso potencialmente tarifado, o projeto deve identificar:

* Qual recurso está sendo utilizado
* Qual função ele desempenha
* Se existe possibilidade de cobrança
* O que exatamente gera consumo
* Qual é a unidade de cobrança
* Se existe Free Tier ou outra condição aplicável
* Qual ação efetivamente gera consumo
* Qual é o nível de risco financeiro
* Se existe uma forma segura de realizar um teste controlado
* Como interromper o consumo
* Como remover os recursos
* Como verificar posteriormente o consumo

### 🔄 Fluxo de decisão

```text
IMPLEMENTAR
     ↓
IDENTIFICAR O QUE GERA COBRANÇA
     ↓
ANALISAR RISCO
     ↓
DEFINIR TESTE SEGURO
     ↓
EXECUTAR CONTROLADAMENTE
     ↓
PARAR / LIMPAR RECURSOS
     ↓
VERIFICAR CONSUMO
     ↓
DOCUMENTAR
```

A existência de um serviço potencialmente tarifado não determina sozinha sua classificação.

A decisão será baseada no **mecanismo real de cobrança e na possibilidade de realizar uma validação controlada**.

> ⚠️ Free Tier ou créditos disponíveis não são considerados garantia automática de custo zero.

---

## 🏷️ Classificação dos Recursos

Cada projeto diferencia claramente o que foi realmente realizado no ambiente AWS.

### 🟢 Implementado e Validado

Recurso configurado e validado por meio de testes controlados.

### 🟢 Implementado — Teste Controlado

Recurso configurado e executado de maneira limitada, com monitoramento de consumo e encerramento após a validação.

### 🟡 Simulado

A arquitetura foi desenvolvida e documentada, mas a execução real não foi realizada por ausência de uma forma segura de validação dentro das condições do laboratório.

A documentação pode incluir:

* Arquitetura
* Fluxo
* Payloads
* Respostas
* Tratamento de erros
* Casos de teste
* Integrações
* Comportamento esperado
* Limitações

### 🔵 Conceitual

Recurso estudado e documentado como parte da arquitetura, mas que não foi configurado nem executado.

> O portfólio não classifica como "implementado" aquilo que não foi efetivamente configurado e validado.

---

## 🔐 Segurança

Todos os projetos utilizam dados fictícios.

Exemplo:

```text
ARES-001
ARES-002
ARES-003
```

Nenhum projeto deve conter:

* Credenciais reais
* Access Keys
* Secret Keys
* Tokens
* Senhas
* Dados reais de clientes
* Informações pessoais reais

Quando necessário, serão utilizados:

* Variáveis de ambiente
* `.env.example`
* `.gitignore`
* IAM Least Privilege
* OAuth
* Secrets Manager
* Tokens temporários
* Identificadores fictícios

---

## 🧪 Testes e Confiabilidade

Os projetos devem considerar não apenas o caminho de sucesso, mas também cenários de falha.

Exemplos:

```text
SUCCESS
NOT_FOUND
INVALID_INPUT
UNAUTHORIZED
FORBIDDEN
TIMEOUT
RATE_LIMIT
INTERNAL_ERROR
SERVICE_UNAVAILABLE
INVALID_RESPONSE
```

Quando aplicável, também serão utilizados:

* Retry
* Exponential Backoff
* Idempotência
* Validação de entrada
* Tratamento de exceções
* Logs estruturados
* Correlation ID
* Troubleshooting

---

## 📊 Observabilidade

As integrações devem considerar, quando aplicável:

* Contact ID
* Flow ID
* Correlation ID
* Status da operação
* Latência
* Código HTTP
* Erros
* Timeout
* Retry
* Falhas de autenticação
* Indisponibilidade de serviços

Credenciais e tokens nunca devem ser registrados nos logs.

---

## 📚 Documentação

Cada projeto pode possuir sua própria documentação técnica, incluindo:

```text
README.md
docs/
├── architecture.md
├── integration.md
├── finops.md
├── testing.md
├── troubleshooting.md
└── decisions.md

src/
tests/
simulations/
evidence/
diagrams/
```

A estrutura pode variar conforme a natureza de cada projeto.

---

## 🎯 Objetivo Profissional

O objetivo deste portfólio é demonstrar uma evolução prática em **Amazon Connect Engineering**, conectando conhecimentos de:

```text
Amazon Connect
      +
AWS
      +
Serverless
      +
APIs
      +
CTI
      +
CRM
      +
Desenvolvimento
      +
Suporte Técnico
```

A proposta é demonstrar não apenas conhecimento teórico, mas a capacidade de:

* Projetar soluções
* Implementar integrações
* Investigar problemas
* Tratar falhas
* Documentar decisões
* Controlar custos
* Aplicar segurança
* Testar cenários
* Explicar uma arquitetura técnica

---

## 🚀 Status do Portfólio

### Fase 1 — Fundação

**P1 → P6**

✅ **Em Desenvolvimento**

### Fase 2 — AWS & Integrações

**P7 → P10**

🔜 **Planejada**

### Fase 3 — CRM & CTI

**P11 → P14**

🔜 **Planejada**

---

## 👨‍💻 Sobre

**Máximo Monteiro**

Technical Support Analyst N2/N3 | Front-End Developer | AWS & Amazon Connect

Este portfólio representa meu processo de especialização em **Amazon Connect, AWS, CCaaS, CTI e integrações**, combinando minha experiência anterior em suporte técnico e desenvolvimento com uma trajetória prática de construção de soluções em nuvem.

**LinkedIn:** https://www.linkedin.com/in/maximojunior/

**GitHub:** https://github.com/Maximo-junior
