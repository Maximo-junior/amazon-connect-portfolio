# 🌐 Amazon Connect Engineering Portfolio — Ecossistema Ares Saúde

> **Laboratório prático de Amazon Connect, AWS, CCaaS, APIs, CTI, CRM e desenvolvimento de aplicações para Contact Center.**

O **Ecossistema Ares Saúde** é um laboratório de engenharia criado para demonstrar, de forma **progressiva, prática e tecnicamente documentada**, a evolução de uma arquitetura de Contact Center utilizando **Amazon Connect e serviços AWS**.

A solução parte de uma estrutura inicial de atendimento e evolui gradualmente para um ecossistema integrado envolvendo:

* Amazon Connect
* Contact Flows
* URA / IVR
* Filas e roteamento
* Contact Attributes
* Flow Modules
* AWS Serverless
* APIs REST
* Amazon Lex
* AWS Lambda
* Amazon DynamoDB
* CTI
* CRM
* Screen Pop
* Salesforce
* EspoCRM
* Twenty CRM
* Segurança e IAM
* Observabilidade
* FinOps
* Tratamento de falhas
* Testes e troubleshooting
* Desenvolvimento Front-End
* Aplicação Web para Contact Center

> **Importante:** o Ares Saúde é um cenário fictício criado exclusivamente para fins educacionais e de portfólio. Todos os dados utilizados são fictícios.

---

# 🎯 O que este portfólio demonstra

O objetivo não é apenas apresentar conhecimento sobre serviços AWS, mas demonstrar a capacidade de:

* Projetar arquiteturas de Contact Center
* Criar e evoluir Contact Flows
* Trabalhar com filas, roteamento e contexto
* Utilizar Contact Attributes
* Desenvolver arquiteturas modulares
* Integrar Amazon Connect com serviços AWS
* Desenvolver integrações via APIs
* Trabalhar com Serverless
* Integrar soluções de CRM e CTI
* Desenvolver interfaces com Vue.js e TypeScript
* Implementar tratamento de erros e cenários de falha
* Aplicar IAM e princípios de Least Privilege
* Trabalhar com observabilidade
* Analisar e controlar custos
* Criar testes positivos e negativos
* Investigar problemas e realizar troubleshooting
* Documentar decisões arquiteturais
* Explicar trade-offs técnicos
* Construir uma experiência visual própria para atendimento

A proposta é demonstrar **evolução técnica**, e não apenas uma coleção de tecnologias.

---

# 🗺️ Trilha de Evolução Arquitetural

O Ecossistema Ares Saúde é desenvolvido de forma incremental.

Cada projeto reutiliza conceitos, componentes e decisões dos projetos anteriores, aumentando progressivamente a complexidade da solução.

---

## 🔹 Fase 1 — Fundação Amazon Connect

| Projeto                                                         | Nível                  | Escopo Técnico Principal                                                        | Status        |
| --------------------------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------- | ------------- |
| 🚀 [Projeto 1 — Ares Triagem Inicial](./projeto-1-triagem-ares) | Básico                 | Contact Flows, URA/IVR, prompts, menus e tratamento de erros                    | **Concluído** |
| 🚀 Projeto 2 — Ares Routing & Queues                            | Básico+                | Queues, Routing Profiles, Hours of Operation, agentes e transbordo              | **Concluído** |
| 🚀 Projeto 3 — Ares Context & Contact Attributes                | Intermediário          | Contact Attributes, contexto de contato, segmentação e roteamento contextual    | **Concluído** |
| 🚀 Projeto 4 — Ares Modular Architecture                        | Intermediário/Avançado | Flow Modules, reutilização de componentes e arquitetura multi-departamental     | **Concluído** |
| 🚀 Projeto 5 — Ares Inteligente                                 | Avançado               | Autosserviço, inteligência conversacional, integrações e arquitetura serverless | **Concluído** |
| 🚀 Projeto 6 — Ares Enterprise                                  | Profissional           | Segurança, governança, observabilidade, FinOps e Disaster Recovery              | **Concluído** |

---

# 🔹 Fase 2 — AWS Serverless, APIs e Integrações

A segunda fase amplia o Ecossistema Ares para além dos recursos nativos do Contact Flow.

| Projeto                                     | Nível        | Escopo Técnico Principal                                                   | Status                 |
| ------------------------------------------- | ------------ | -------------------------------------------------------------------------- | ---------------------- |
| 🔜 Projeto 7 — Ares Serverless              | Avançado     | Amazon Connect, AWS Lambda, DynamoDB, IAM, validação e tratamento de erros | **Em desenvolvimento** |
| 🔜 Projeto 8 — Ares Conversational          | Avançado     | Amazon Connect, Amazon Lex, Lambda, DynamoDB/API e NLU                     | **Planejado**          |
| 🔜 Projeto 9 — Ares API & Integrations      | Avançado     | Lambda, APIs REST, JSON, autenticação, timeout, retry e sistemas externos  | **Planejado**          |
| 🔜 Projeto 10 — Ares CTI & CRM Architecture | Profissional | CTI, CRM, contexto de atendimento, Screen Pop e arquitetura de integração  | **Planejado**          |

---

# 🔹 Fase 3 — CRM, CTI e Integrações Corporativas

Nesta fase, os conceitos desenvolvidos anteriormente serão aplicados em cenários de integração com diferentes modelos de CRM.

| Projeto                                            | Nível        | Escopo Técnico Principal                                                    | Status        |
| -------------------------------------------------- | ------------ | --------------------------------------------------------------------------- | ------------- |
| 🔜 Projeto 11 — Salesforce Customer Identification | Profissional | Salesforce API, identificação do cliente, Contact Attributes e Screen Pop   | **Planejado** |
| 🔜 Projeto 12 — Salesforce Service Automation      | Profissional | Cases, Activities, pós-atendimento, automação e idempotência                | **Planejado** |
| 🔜 Projeto 13 — EspoCRM Integration                | Profissional | REST API, contatos, contas, atividades, Cases e integração com Connect      | **Planejado** |
| 🔜 Projeto 14 — Twenty CRM Integration             | Profissional | APIs, pessoas, empresas, oportunidades, atividades e integração com Connect | **Planejado** |

### CRM utilizados no laboratório

**Salesforce** será utilizado como referência de um CRM corporativo.

**EspoCRM** e **Twenty** serão priorizados para experimentação prática quando uma implementação real puder ser realizada de forma segura e controlada.

> O fato de uma plataforma ser open source ou self-hosted não significa automaticamente custo zero. Infraestrutura, armazenamento, tráfego e outros componentes serão avaliados individualmente.

---

# 🔹 Fase 4 — Ares Contact Center Web App

A quarta fase transforma os conhecimentos desenvolvidos nos Projetos 1–14 em uma aplicação web própria para atendimento.

O objetivo não é criar uma landing page.

O objetivo é desenvolver uma **interface funcional de Contact Center**, construída principalmente com **Vue.js e TypeScript**, capaz de apresentar informações do atendimento e consumir dados provenientes do Amazon Connect, AWS, APIs e CRMs.

| Projeto                                     | Nível        | Escopo Técnico Principal                                                                    | Status        |
| ------------------------------------------- | ------------ | ------------------------------------------------------------------------------------------- | ------------- |
| 🚀 Projeto 15 — Ares Contact Center Web App | Profissional | Vue.js, TypeScript, APIs, CTI, Screen Pop, contexto do atendimento e integração com AWS/CRM | **Planejado** |

O P15 funcionará como uma camada visual de consolidação dos projetos anteriores.

---

# 🏗️ Evolução da Arquitetura

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
Salesforce + EspoCRM + Twenty
     ↓
P15
Ares Contact Center Web App
     ↓
Front-End + APIs + AWS + Connect + CRM
```

O objetivo não é criar projetos independentes.

A proposta é demonstrar a **evolução de uma arquitetura de Contact Center ao longo de diferentes níveis de complexidade**.

---

# 🛠️ Stack Tecnológica

## ☁️ Core CCaaS

* Amazon Connect
* Contact Flows
* Queues
* Routing Profiles
* Hours of Operation
* Contact Attributes
* Flow Modules
* Agent Workspace / CCP

## ⚙️ AWS & Serverless

* AWS Lambda
* Amazon DynamoDB
* Amazon Lex
* Amazon Polly
* Amazon CloudWatch
* AWS IAM
* AWS Secrets Manager, quando aplicável
* AWS CLI
* AWS SDK
* Outros serviços AWS conforme necessidade arquitetural

## 🔌 APIs & Integrações

* APIs REST
* HTTP / JSON
* Autenticação
* OAuth
* Web APIs
* Integrações com sistemas externos
* Timeout
* Retry
* Exponential Backoff
* Idempotência
* Circuit Breaker, quando aplicável
* Tratamento de erros

## 🏢 CRM & CTI

* Salesforce
* EspoCRM
* Twenty CRM
* CTI
* Screen Pop
* Customer Identification
* Contact Attributes
* Cases
* Activities
* Pós-atendimento

## 💻 Desenvolvimento

* Python
* Node.js
* TypeScript
* JavaScript
* Vue.js
* HTML
* CSS
* Git
* GitHub
* Testes automatizados, quando aplicável

---

# 🖥️ Ares Contact Center Web App

O Projeto 15 adicionará uma camada Front-End própria ao Ecossistema Ares.

A aplicação será desenvolvida principalmente no **Visual Studio Code**, utilizando:

* Vue.js
* TypeScript
* HTML
* CSS
* REST / HTTP
* APIs
* Backend / Serverless

O **Amazon Connect Console** continuará sendo utilizado para os recursos próprios do Contact Center, como:

* Contact Flows
* Queues
* Routing Profiles
* Agents
* Contact Attributes
* Hours of Operation
* Flow Modules

Os demais recursos AWS poderão ser desenvolvidos ou configurados utilizando:

* VS Code
* AWS Console
* AWS CLI
* AWS SDK

A ferramenta será escolhida de acordo com a natureza de cada componente.

---

# 🖥️ Conceito do Ares Contact Center Web App

```text
┌─────────────────────────────────────────────────────────────┐
│ ARES CONTACT CENTER                         🟢 Disponível   │
├───────────────┬─────────────────────────────┬───────────────┤
│               │                             │               │
│ ☎ Contato     │          Cliente            │ Atendimento   │
│               │                             │               │
│ +55 (...)     │          ARES-001           │ Consultas     │
│               │                             │ Exames        │
│ Contact ID    │          Histórico          │ Financeiro    │
│               │                             │               │
│               │          Consulta            │ 📝 Notas      │
│               │          Exame               │               │
│               │                             │ 🟢 Em curso   │
│               │                             │               │
└───────────────┴─────────────────────────────┴───────────────┘
```

A aplicação poderá demonstrar progressivamente:

* Identificação do cliente
* Contact ID
* Contact Attributes
* Screen Pop
* Informações do cliente
* Histórico de contatos
* Fila
* Agente
* Status do atendimento
* Motivo do contato
* Dados provenientes de CRM
* Abertura e atualização de Cases
* Activities
* Notas
* Pós-atendimento
* Consulta a APIs
* Loading
* Timeout
* Indisponibilidade de integração
* Autenticação
* Controle de sessão
* Tratamento de erros

As funcionalidades serão implementadas conforme a evolução dos projetos anteriores.

---

# 🔄 Arquitetura do P15

Arquitetura de referência:

```text
                 ┌──────────────────────────┐
                 │      ARES WEB APP        │
                 │                          │
                 │   Vue.js + TypeScript    │
                 │                          │
                 │   Interface do Agente    │
                 └────────────┬─────────────┘
                              │
                           HTTPS
                              │
                              ▼
                 ┌──────────────────────────┐
                 │       Backend/API        │
                 │                          │
                 │   Lambda / REST API      │
                 └────────────┬─────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
     Amazon Connect       DynamoDB           CRM/API
            │                 │                 │
            │                 │        ┌────────┼────────┐
            │                 │        ▼        ▼        ▼
            │                 │   Salesforce EspoCRM Twenty
            │                 │
            ▼                 │
     Contact Attributes      │
     Contact Flow            │
     Contact ID              │
     Queue                   │
     Agent                   │
```

A arquitetura final deverá representar **somente aquilo que realmente foi implementado**.

---

# 🔗 Relação do P15 com os Projetos Anteriores

```text
P1–P6
Fundamentos Amazon Connect
        ↓
P7–P10
AWS + Serverless + APIs
        ↓
P11–P14
CRM + CTI + Screen Pop
        ↓
P15
Ares Contact Center Web App
```

Durante o desenvolvimento será identificado claramente:

* O que foi herdado
* O que foi reutilizado
* O que foi adaptado
* O que foi desenvolvido novamente
* O que foi adicionado
* O que permanece simulado
* O que é conceitual
* O que foi realmente integrado

---

# 💰 FinOps e Política de Execução

O objetivo financeiro do laboratório é manter o **custo operacional em R$ 0,00 sempre que isso for tecnicamente possível**.

Entretanto, a possibilidade de cobrança não significa automaticamente que um recurso será proibido ou apenas simulado.

Antes de executar qualquer recurso potencialmente tarifado, será identificado:

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

## 🔄 Fluxo de decisão

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

> **Free Tier ou créditos disponíveis não são considerados garantia automática de custo zero.**

---

# 🏷️ Classificação dos Recursos

Cada projeto diferencia claramente o que foi realmente realizado.

### 🟢 Implementado e Validado

Recurso configurado e validado por meio de testes controlados.

### 🟢 Implementado — Teste Controlado

Recurso configurado e executado de maneira limitada, com monitoramento de consumo e encerramento após a validação.

### 🟡 Simulado

A arquitetura foi desenvolvida e documentada, mas a execução real não foi realizada por ausência de uma forma segura de validação dentro das condições do laboratório.

A documentação poderá incluir:

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

> **O portfólio não classifica como "implementado" aquilo que não foi efetivamente configurado e validado.**

---

# 🔐 Segurança

Todos os projetos utilizam dados fictícios.

Exemplos:

```text
ARES-001
ARES-002
ARES-003
```

Nenhum projeto deverá conter:

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
* AWS Secrets Manager
* Tokens temporários
* Identificadores fictícios

---

# 🧪 Testes e Confiabilidade

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

Quando aplicável, serão utilizados:

* Retry
* Exponential Backoff
* Idempotência
* Validação de entrada
* Tratamento de exceções
* Logs estruturados
* Correlation ID
* Troubleshooting

---

# 📊 Observabilidade

As integrações deverão considerar, quando aplicável:

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

> Credenciais, tokens e informações sensíveis nunca deverão ser registrados nos logs.

---

# 📚 Documentação

Cada projeto poderá possuir sua própria documentação técnica.

Estrutura de referência:

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

A estrutura poderá variar de acordo com a natureza de cada projeto.

---

# 🎥 Evidências e Demonstrações

Os projetos priorizam evidências práticas.

Quando aplicável, serão utilizados:

* Screenshots
* Vídeos
* Código
* Requests
* Responses
* Logs
* AWS Console
* Amazon Connect Console
* Aplicação funcionando
* Diagramas
* Testes
* Tratamento de erros

## 🎬 Estrutura de demonstração

```text
1. Apresentar o problema
2. Apresentar a arquitetura
3. Demonstrar a solução
4. Mostrar a implementação
5. Executar um teste
6. Demonstrar um cenário de erro
7. Mostrar o tratamento do erro
8. Mostrar código relevante
9. Mostrar AWS / Amazon Connect quando aplicável
10. Explicar o que foi realmente implementado
11. Explicar custos e decisões de FinOps
```

No P15, o foco da demonstração será principalmente a aplicação funcionando e sua integração com os componentes do Ecossistema Ares.

---

# 🧠 Princípio de Desenvolvimento

O laboratório segue uma abordagem de:

```text
EXPLICAR
   ↓
EXECUTAR
   ↓
VALIDAR
   ↓
DOCUMENTAR
   ↓
AVANÇAR
```

Cada etapa deverá responder:

* Por que isso existe?
* Quando utilizar?
* Quando não utilizar?
* Como funciona?
* Quanto pode custar?
* Como proteger?
* Como testar?
* Como observar?
* Como diagnosticar?
* Como explicar isso em uma entrevista?

---

# 🎯 Objetivo Profissional

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
      +
Front-End
```

A proposta é demonstrar não apenas conhecimento teórico, mas a capacidade de:

* Projetar soluções
* Implementar integrações
* Desenvolver aplicações
* Investigar problemas
* Tratar falhas
* Documentar decisões
* Controlar custos
* Aplicar segurança
* Testar cenários
* Explicar arquiteturas
* Construir experiências para atendimento

---

# 🚀 Status do Portfólio

### Fase 1 — Fundação Amazon Connect

**P1 → P6**

✅ **Concluída**

### Fase 2 — AWS & Integrações

**P7 → P10**

🔄 **Em desenvolvimento**

### Fase 3 — CRM & CTI

**P11 → P14**

🔜 **Planejada**

### Fase 4 — Ares Contact Center Web App

**P15**

🔜 **Planejada**

---

# 📌 Status de Implementação

O status apresentado neste README representa o estado atual do laboratório.

Projetos futuros não são apresentados como experiência profissional prévia.

Cada implementação deverá indicar claramente se determinado componente foi:

* **Implementado e validado**
* **Implementado em teste controlado**
* **Simulado**
* **Conceitual**

Essa distinção existe para manter a **transparência técnica do portfólio**.

---

# 👨‍💻 Sobre

**Máximo Monteiro**

**Technical Support Analyst N2/N3 | Front-End Developer | AWS Cloud & Amazon Connect**

Este portfólio representa meu processo de especialização em **Amazon Connect, AWS, CCaaS, CTI e integrações**, combinando minha experiência anterior em suporte técnico e desenvolvimento com uma trajetória prática de construção e documentação de soluções em nuvem.

### 🔗 Links

* **LinkedIn:** https://www.linkedin.com/in/maximojunior/
* **GitHub:** https://github.com/Maximo-junior

---

# 📖 Navegação

* [Projeto 1 — Ares Triagem Inicial](./projeto-1-triagem-ares)
* Projeto 2 — Ares Routing & Queues
* Projeto 3 — Ares Context & Contact Attributes
* Projeto 4 — Ares Modular Architecture
* Projeto 5 — Ares Inteligente
* Projeto 6 — Ares Enterprise
* Projeto 7 — Ares Serverless
* Projeto 8 — Ares Conversational
* Projeto 9 — Ares API & Integrations
* Projeto 10 — Ares CTI & CRM Architecture
* Projeto 11 — Salesforce Customer Identification
* Projeto 12 — Salesforce Service Automation
* Projeto 13 — EspoCRM Integration
* Projeto 14 — Twenty CRM Integration
* Projeto 15 — Ares Contact Center Web App

---

## 🚀 Visão Final

O Ecossistema Ares Saúde representa uma jornada de aprendizado e construção que parte de **Amazon Connect e Contact Flows** e evolui para uma arquitetura envolvendo:

```text
Contact Center
      ↓
Amazon Connect
      ↓
AWS
      ↓
Serverless
      ↓
APIs
      ↓
CTI
      ↓
CRM
      ↓
Screen Pop
      ↓
Front-End
      ↓
Ares Contact Center Web App
```

O objetivo final é demonstrar a capacidade de **projetar, implementar, testar, observar, documentar e explicar soluções de Contact Center**, mantendo transparência sobre aquilo que foi efetivamente construído.

> **Construir. Validar. Documentar. Explicar. Evoluir.**
