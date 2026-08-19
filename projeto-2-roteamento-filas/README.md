# 🏥 Projeto 2 — Roteamento e Filas de Atendimento | Clínica Ares

## 📋 Visão Geral
Este projeto contempla a evolução da infraestrutura de atendimento da **Clínica Ares**, transformando os destinos simulados da URA de Triagem Inicial em uma arquitetura de roteamento real com distribuição de contatos para agentes humanos.

## 🎯 Problema de Negócio
Com o crescimento da clínica, os pacientes precisam ser direcionados a equipes humanas especializadas de acordo com o setor escolhido (**Consultas**, **Exames** e **Financeiro**). Além disso, a clínica precisa restringir o recebimento de chamadas ao seu horário de atendimento e gerenciar a disponibilidade dos operadores.

## 🏛️ Arquitetura da Solução
- **Ponto de Entrada:** Contact Flow `AR_CF_Triagem_Inicial` (v2)
- **Horário de Funcionamento:** `AR_HO_Clinica` (Seg a Sex, 08h às 18h)
- **Filas de Atendimento (Queues):**
  - `AR_Q_Consultas`
  - `AR_Q_Exames`
  - `AR_Q_Financeiro`
- **Perfil de Roteamento (Routing Profile):** `AR_RP_Atendimento`
- **Interface do Agente:** Agent Workspace / CCP (Softphone web)

## 💰 Política FinOps — Custo Zero (R$ 0,00)
- Filas, perfis de roteamento e horários de funcionamento são recursos nativos sem custo de provisionamento.
- Os testes com agente logado serão validados via softphone/chat nativo do console, preservando a regra de não tarifação de linhas telefônicas (PSTN/DID).


## 🎓 Competências Adquiridas (Projeto 2)

Ao finalizar este projeto, demonstrei e validei na prática:

* **Consigo explicar:** A diferença estrutural entre **Queue** (armazenamento do contato em espera) e **Routing Profile** (habilidades/perfis do agente que consom essas filas), compreendendo por que são desacoplados na arquitetura AWS.
* **Consigo configurar:** Horários de operação (**Hours of Operation**), Filas de atendimento (**Queues**), Perfis de roteamento (**Routing Profiles**) e associação de agentes (**Users/Softphone**).
* **Consigo configurar:** Blocos de decisão temporal (`Check hours of operation`) e blocos de distribuição de carga (`Set working queue` e `Transfer to queue`) no Flow Designer.
* **Consigo diagnosticar:** Resolução de falhas de publicação no Flow Designer decorrentes de pontas soltas (ramos de erro desconectados) ou formulários de blocos não confirmados.
* **Consigo documentar:** A evolução arquitetural de destinos simulados para roteamento real multidepartamental sob a governança FinOps (R$ 0,00).

---

## 🚀 Próxima Evolução
Agora que os departamentos possuem estrutura real de roteamento e agentes operacionais, o próximo passo na evolução da Clínica Ares é a introdução de **Contexto e Roteamento Avançado** no **Projeto 3 (Contact Attributes e Contexto)**.

## 📐 Fluxograma da Solução (Projeto 2)

```
                                [ INÍCIO ]
                                    │
                                    ▼
                      ┌───────────────────────────┐
                      │    Set Voice (Vitória)    │
                      └─────────────┬─────────────┘
                                    │
                                    ▼
                      ┌───────────────────────────┐
                      │      Tentativas = 0       │
                      └─────────────┬─────────────┘
                                    │
                                    ▼
                      ┌───────────────────────────┐
                      │ Check Hours of Operation  │
                      │      (AR_HO_Clinica)      │
                      └──────┬─────────────┬──────┘
                             │             │
              ┌──────────────┘             └──────────────┐
              ▼ (In hours)                                ▼ (Out of hours / Error)
┌───────────────────────────┐               ┌───────────────────────────┐
│     AR_PR_Saudacao        │               │   AR_PR_Fechado (TTS)     │
│ "Bem-vindo à Clínica..."  │               │ "Nosso horário é Seg-Sex" │
└─────────────┬─────────────┘               └─────────────┬─────────────┘
              │                                           │
              ▼                                           ▼
┌───────────────────────────┐                      [ DISCONNECT ]
│    Get customer input   │
│ 1-Cons / 2-Exam / 3-Fin   │
└──────┬──────┬──────┬──────┘
       │      │      │
       │      │      └──────────────┐
       │      └──────┐              │
       ▼ (1)         ▼ (2)          ▼ (3)
┌─────────────┐┌─────────────┐┌─────────────┐
│Set Working Q││Set Working Q││Set Working Q│
│AR_Q_Consults││ AR_Q_Exames ││AR_Q_Finance │
└──────┬──────┘└──────┬──────┘└──────┬──────┘
       │              │              │
       └──────────────┼──────────────┘
                      │
                      ▼
        ┌───────────────────────────┐
        │     Transfer to Queue     │
        └──────┬─────────────┬──────┘
               │             │
               ▼ (Success)   ▼ (Error / At capacity)
        ┌─────────────┐ ┌───────────────────────────┐
        │  AR_RP_Aten │ │   AR_PR_Encerramento      │
        │      │      │ └─────────────┬─────────────┘
        │      ▼      │               │
        │ [ AGENTE ]  │               ▼
        └─────────────┘          [ DISCONNECT ]
