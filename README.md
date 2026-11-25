# 🌐 Amazon Connect Engineering Portfolio — Ecossistema Ares Saúde

> Laboratório prático de Amazon Connect, AWS, CCaaS, IA generativa aplicada a atendimento, integrações e CRM.

O **Ecossistema Ares Saúde** é um laboratório que construo projeto a projeto para aprender e demonstrar, com evidência, como se projeta, implementa, opera e explica uma operação de contact center na AWS. A Ares é uma rede de saúde fictícia: pacientes, telefones, CPFs, exames e médicos são inventados, e mesmo assim são tratados como dado sensível (LGPD) para treinar o hábito certo.

A trilha tem duas fases bem diferentes. Os Projetos 1 a 8 cobriram os fundamentos do Amazon Connect: contact flows, URA, filas, roteamento, contact attributes, flow modules, Lambda com DynamoDB e Lex. A partir do Projeto 9 o laboratório recomeça do zero, numa conta AWS nova, com cara de ambiente de produção: infraestrutura como código em Terraform, pipeline com GitHub Actions, identidade corporativa, segurança em camadas, IA generativa rodando de verdade na instância, observabilidade e custo controlado. O foco também muda: os canais digitais (chat web, WhatsApp, mensagens de voz, chamada pelo site) e a voz conversacional com IA passam a ser o centro, e a URA com menu de teclas fica para trás.

> **Importante:** este é um projeto de portfólio. O que está aqui foi construído em laboratório e não é apresentado como experiência em produção.

---

## 🗺️ Trilha de projetos

### Fase 1 — Fundação Amazon Connect ✅

| Projeto | Escopo técnico principal | Status |
| --- | --- | --- |
| [P1 — Ares Triagem Inicial](./projeto-1-triagem-ares) | Contact flows, URA/IVR, prompts, menus e tratamento de erros | Concluído |
| P2 — Ares Routing & Queues | Filas, routing profiles, hours of operation, agentes e transbordo | Concluído |
| P3 — Ares Context & Contact Attributes | Contact attributes, contexto do contato e roteamento contextual | Concluído |
| P4 — Ares Modular Architecture | Flow modules e arquitetura multidepartamental | Concluído |
| P5 — Ares Inteligente | Autosserviço, inteligência conversacional e arquitetura serverless | Concluído |
| P6 — Ares Enterprise | Segurança, governança, observabilidade, FinOps e DR | Concluído |

### Fase 2 — Serverless e Conversacional ✅

| Projeto | Escopo técnico principal | Status |
| --- | --- | --- |
| P7 — Ares Serverless | Amazon Connect, Lambda, DynamoDB, IAM, validação e tratamento de erros | Concluído |
| [P8 — Ares Conversational](./projeto-8-conversational) | Atendimento conversacional por voz com NLU: Amazon Connect (`AR_CF_Conversational`), Amazon Lex V2 (`AR_Lex_AtendimentoAres`), AWS Lambda (`AR_LF_ConsultaExame`), DynamoDB (`AR_TB_Pacientes`) e chamadas PSTN via DID US | Concluído |

### Fase 3 — Atendimento digital com IA

Conta AWS nova, Terraform desde o primeiro recurso e o paciente atendido por chat e WhatsApp com IA, segurança clínica e passagem para o humano sem repetir nada.

| Projeto | Escopo técnico principal | Status |
| --- | --- | --- |
| [P9 — Ares Digital Front Door](./projeto-9-digital-front-door) | Fundação da conta nova, chat web (`Ares_Fluxo_Recepcao_Digital`), identificação via DynamoDB (`AR_TB_Pacientes`), IA de recepção com Amazon Bedrock (`AR_LF_Recepcao_Classificar`) e handoff com contexto exibido em tempo real na View customizada `AR_VW_Ficha_Paciente` (`AR_FL_Guia_Atendente`) | Concluído |

## 🏗️ Arquitetura alvo

O diagrama abaixo é o destino da trilha, não o estado atual. Ao fim de cada projeto o diagrama "as-built" mostra apenas o que foi de fato construído.

```text
   Paciente (WhatsApp · Chat web · Voz com IA · Chamada pelo site · Email · SMS)
                                  │
                       Amazon Connect (dev / prod)
                                  │
     ┌──────────────┬─────────────┼─────────────┬──────────────┐
 Contact Flows   Routing &    Agentes de IA    Lex V2 +    Contact Lens
 & Modules       Quick Conn.  do Connect       Bedrock     & Analytics
     └──────────────┴─────────────┼─────────────┴──────────────┘
                                  │
              Middleware / Integration Layer (VPC)
      API Gateway · Lambda · SQS/DLQ · EventBridge · Secrets
                                  │
           ┌──────────────────────┼──────────────────────┐
     Mock Hospital            Salesforce            Knowledge Base
                                  │
