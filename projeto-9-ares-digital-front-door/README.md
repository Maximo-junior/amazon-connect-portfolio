# 🏥 P9 — Ares Digital Front Door (Recepção Digital Inteligente & Agent Workspace)

> **Fase 3 — Atendimento Digital com IA** | Ecossistema Ares Saúde
> **Status:** 🟢 Implementado e Validado

---

## 🎯 Problema & Objetivo

Em atendimentos tradicionais, o paciente precisa informar seus dados cadastrais e repetir o motivo do contato ao ser transferido para um atendente humano.

O objetivo do **Projeto 9** é validar a recepção digital da **Ares Saúde** no Amazon Connect: o paciente inicia o contato pelo **Chat Web**, é identificado automaticamente no **Amazon DynamoDB**, passa pela triagem inteligente do **Amazon Bedrock** e é transferido para a especialista com o contexto completo exibido em tempo real no **Agent Workspace** através da View customizada **`AR_VW_Ficha_Paciente`**.

---

## 🛠️ Stack Tecnológica Utilizada

| Categoria | Tecnologia / Serviço | Papel na Arquitetura |
| --- | --- | --- |
| **CCaaS & Orquestração** | **Amazon Connect** (`us-east-1`) | Instância de contact center gerenciando o canal de Chat Web, filas, roteamento e *Contact Attributes*. |
| **Motor de Fluxos** | **Amazon Connect Contact Flows** | Orquestração do fluxo principal de recepção (`Ares_Fluxo_Recepcao_Digital`) e do fluxo de guia do agente (`AR_FL_Guia_Atendente`). |
| **Interface do Especialista** | **Amazon Connect Views & Step-by-Step Guides** | Construção da ficha dinâmica (`AR_VW_Ficha_Paciente`) exibida automaticamente (*Screen Pop*) no **Agent Workspace**. |
| **Estilização de UI** | **HTML5 & CSS3 Inline (`HTML Box`)** | Criação do cabeçalho, divisores de seção e rodapé institucional em degradê roxo (`#3B1E70` → `#6B46C1`), combinados com componentes nativos do Connect. |
| **Compute Serverless** | **AWS Lambda (Python)** | Execução sob demanda das regras de negócio (`AR_LF_Paciente_Identificar` e `AR_LF_Recepcao_Classificar`) com contratos JSON planos. |
| **Banco de Dados NoSQL** | **Amazon DynamoDB** (`PAY_PER_REQUEST`) | Armazenamento cadastral dos pacientes fictícios (`AR_TB_Pacientes`) com leitura de baixa latência por `paciente_id`. |
| **IA Generativa** | **Amazon Bedrock** | Processamento de linguagem natural para classificar a intenção/fila (`PRIORITARIO`), urgência (`MEDIA`) e gerar o resumo clínico (`resumo_ia`). |
| **Segurança & Governança** | **AWS IAM & CloudWatch Logs** | Roles dedicadas com princípio do menor privilégio (*Least Privilege*) e logs estruturados de execução sem exposição de dados sensíveis. |

---

## 🏗️ Arquitetura Implementada

```text
[Paciente — Chat Web]
        │
        ▼
[Amazon Connect: Ares_Fluxo_Recepcao_Digital]
        │
        ├──► 1. Identificação do Paciente (AWS Lambda ──► DynamoDB: AR_TB_Pacientes)
        ├──► 2. Triagem & Classificação (AWS Lambda ──► Amazon Bedrock)
        ├──► 3. Roteamento para Fila (Contact Attributes)
        │
        ▼
[Fluxo de Guia: AR_FL_Guia_Atendente]
        │
        ▼
[Agent Workspace: Screen Pop ──► AR_VW_Ficha_Paciente]

+-------------------------------------------+



                    |     ▶ ENTRY POINT (Início Chat Web)       |
                    +-------------------------------------------+
                                          |
                                          v
                    +-------------------------------------------+
                    |           Set Logging Behavior            |
                    |         (Enable CloudWatch Logs)          |
                    +-------------------------------------------+
                                          |
                                          v
                    +-------------------------------------------+
                    |              Set Event Flow               |
                    |  DefaultAgentUI ➔ AR_FL_Guia_Atendente    |
                    +-------------------------------------------+
                                          |
                                          v
                    +-------------------------------------------+
                    |           Store Customer Input            |
                    |  "Olá! Bem-vindo à Ares Saúde. Informe    |
                    |   seu número de paciente (ex: 1001):"     |
                    +-------------------------------------------+
                                          |
                                          v
                    +-------------------------------------------+
                    |          ⚡ Invoke AWS Lambda             |
                    |        AR_LF_Paciente_Identificar         |
                    |      (Consulta DynamoDB: AR_TB_Pacientes) |
                    +-------------------------------------------+
                           /                             \
              [Success]   /                               \   [Error / Timeout]
                         v                                 v
        +---------------------------------+       +---------------------------------+
        |   Check Contact Attributes      |       |      Set Contact Attributes     |
        |     Paciente encontrado?        |       |   (Fallback: Modo Visitante)    |
        +---------------------------------+       +---------------------------------+
               /                   \                               |
       [Sim]  /                     \  [Não]                       |
             v                       +-----------------------------+
+-------------------------+                                        |
| Set Contact Attributes  |                                        |
| • nome_paciente         |                                        |
| • paciente_id           |                                        |
| • convenio              |                                        |
| • pendencia_financeira  |                                        |
| • ultimo_exame          |                                        |
+-------------------------+                                        |
             \                                                     |
              +-------------------------+--------------------------+
                                        |
                                        v
                    +-------------------------------------------+
                    |           Store Customer Input            |
                    |  "Olá $.Attributes.nome_paciente!         |
                    |   Como posso ajudar você hoje?"           |
                    +-------------------------------------------+
                                          |
                                          v
                    +-------------------------------------------+
                    |          🧠 Invoke AWS Lambda             |
                    |        AR_LF_Recepcao_Classificar         |
                    |     (Triagem & Resumo: Amazon Bedrock)    |
                    +-------------------------------------------+
                           /                             \
              [Success]   /                               \   [Error / Timeout]
                         v                                 v
        +---------------------------------+       +---------------------------------+
        |     Set Contact Attributes      |       |      Set Contact Attributes     |
        | • intencao (ex: PRIORITARIO)    |       |  (Fallback: Triagem Padrão)     |
        | • urgencia (ex: MEDIA)          |       +---------------------------------+
        | • resumo_ia                     |                        |
        +---------------------------------+                        |
                         \                                         |
                          +--------------------+-------------------+
                                               |
                                               v
                    +-------------------------------------------+
                    |            Set Working Queue              |
                    |      (Define Fila: ex. PRIORITARIO)       |
                    +-------------------------------------------+
                                               |
                                               v
                    +-------------------------------------------+
                    |               Send Message                |
                    |  "Vou transferir você agora para nossa    |
                    |   equipe de atendimento."                 |
                    +-------------------------------------------+
                                               |
                                               v
                    +-------------------------------------------+
                    |          📲 Transfer to Queue             |
                    |    (Encaminha para Especialista Humano)   |
                    +-------------------------------------------+
                           /                             \
           [Atribuído]    /                               \   [Erro na Fila]
                         v                                 v
        +---------------------------------+       +---------------------------------+
        |  Aciona AR_FL_Guia_Atendente    |       |       ✖ Disconnect / Hang up    |
        +---------------------------------+       +---------------------------------+
