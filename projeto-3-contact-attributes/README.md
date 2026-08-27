# 🏥 Projeto 3 — Contact Attributes, Contexto e Roteamento Dinâmico | Clínica Ares

## 📋 Visão Geral
Este projeto contempla a evolução da inteligência de dados da **Clínica Ares**, introduzindo a captura e persistência de metadados em tempo real através de **Contact Attributes (User-Defined)**, observabilidade com **CloudWatch Logs** e entrega de contexto operacional (**Screen Pop**) no painel do atendente.

## 🎯 Problema de Negócio
No Projeto 2, as chamadas eram distribuídas para as filas departamentais, porém o atendimento ainda ocorria de maneira genérica:
1. **Falta de Segmentação:** Pacientes de **Convênio** e **Particular** concorriam na mesma fila sem distinção de regras ou prioridades.
2. **Perda de Contexto para o Atendente:** O operador atendia a chamada "às cegas", sem saber as opções digitadas na URA, precisando questionar novamente todos os dados.
3. **Falta de Observabilidade e Espera Prolongada:** Inexistência de rastreamento detalhado de eventos da chamada e falta de alternativas para períodos de alta demanda.

## 🏛️ Arquitetura da Solução
- **Ponto de Entrada e Logs:** Contact Flow `AR_CF_Triagem_Contexto` com `Set logging behavior` (CloudWatch ativo)
- **Horário de Funcionamento:** `AR_HO_Clinica` (Seg a Sex, 08h às 18h)
- **Atributos de Sessão (User-Defined):**
  - `TipoAtendimento` (`Consulta`, `Exame`, `Financeiro`)
  - `SegmentoCliente` (`Convenio`, `Particular`)
  - `CanalEntrada` (`Voz_Inbound`)
- **Decisão Dinâmica:** Bloco `Check contact attributes` avaliando regras de contexto
- **Filas de Atendimento (Queues):** `AR_Q_Consultas`, `AR_Q_Exames`, `AR_Q_Financeiro`
- **Perfil de Roteamento:** `AR_RP_Atendimento`
- **Interface do Agente:** Agent Workspace / CCP com exibição contextual de atributos
- **Resiliência de Espera:** Arquitetura de *Queued Callback* (Retorno de Chamada Simulado)

## 💰 Política FinOps — Custo Zero (R$ 0,00)
- A gravação e verificação de Contact Attributes e a emissão de logs básicos no CloudWatch estão dentro da faixa gratuita de operação.
- A validação de recebimento de contexto é feita via Softphone nativo (WebRTC) no console.
- A funcionalidade de *Queued Callback* e a telefonia pública (PSTN/DID) são tratadas como simulações arquiteturais documentadas, evitando tarifas de números e chamadas ativas de saída (*Outbound*).

## 🎓 Competências Adquiridas (Projeto 3)

Ao finalizar este projeto, demonstrei e validei na prática:

* **Consigo explicar:** A diferença estrutural entre atributos definidos pelo usuário (*User-Defined*) e atributos do sistema (*System Attributes*), além do ciclo de vida dessas variáveis durante a sessão do contato.
* **Consigo configurar:** O bloco `Set logging behavior` para habilitar a rastreabilidade e depuração de chamadas via CloudWatch Logs.
* **Consigo configurar:** A persistência de dados com `Set contact attributes` e o roteamento condicional inteligente através de `Check contact attributes`.
* **Consigo arquitetar:** A estratégia de mitigação de tempo de espera utilizando o padrão *Queued Callback* em conformidade com as diretrizes FinOps (R$ 0,00).
* **Consigo validar:** A entrega de metadados em tempo real no painel do operador (Agent Workspace / CCP), eliminando perguntas repetitivas no início do atendimento.

---

## 🚀 Próxima Evolução
Com o contexto e a segmentação estabelecidos, o próximo passo na evolução do Ecossistema Ares Saúde é a **Modularização Corporativa** no **Projeto 4 (Flow Modules — `AR_MD_*`)**, reduzindo duplicações de blocos e centralizando tratamentos de erros.

## 📐 Fluxograma da Solução (Projeto 3)

```text
                                [ INÍCIO ]
                                    │
                                    ▼
                      ┌───────────────────────────┐
                      │    Set Logging Behavior   │ (Habilita CloudWatch)
                      └─────────────┬─────────────┘
                                    │
                                    ▼
                      ┌───────────────────────────┐
                      │    Set Voice (Vitória)    │
                      └─────────────┬─────────────┘
                                    │
                                    ▼
                      ┌───────────────────────────┐
                      │ Check Hours of Operation  │ (AR_HO_Clinica)
                      └──────┬─────────────┬──────┘
                             │             │
              ┌──────────────┘             └──────────────┐
              ▼ (In hours)                                ▼ (Out of hours / Error)
┌───────────────────────────┐                       ┌───────────────────────────┐
│     AR_PR_Saudacao        │                       │   AR_PR_Fechado (TTS)     │
│ "Bem-vindo à Clínica..."  │                       └─────────────┬─────────────┘
└─────────────┬─────────────┘                                     │
              │                                                   ▼
              ▼                                             [ DISCONNECT ]
┌───────────────────────────┐
│   Menu 1: Setor (DTMF)    │ ◄───────────────────────────┐
│ 1-Cons / 2-Exam / 3-Fin   │                             │
└──────┬──────┬──────┬──────┘                             │ (Retentativas)
       │ (1)  │ (2)  │ (3)                                │
       │      │      └──────────────┐                     │
       │      └──────┐              │                     │
       ▼             ▼              ▼                     │
┌─────────────┐┌─────────────┐┌─────────────┐             │
│Set Attribute││Set Attribute││Set Attribute│             │
│TipoAtend =  ││TipoAtend =  ││TipoAtend =  │             │
│"Consulta"   ││"Exame"      ││"Financeiro" │             │
└──────┬──────┘└──────┬──────┘└──────┬──────┘             │
       │              │              │                    │
       └──────────────┼──────────────┘                    │
                      │                                   │
                      ▼                                   │
       ┌───────────────────────────┐                      │
       │   Menu 2: Segmento (DTMF) │                      │
       │ 1-Convênio / 2-Particular │                      │
       └──────┬─────────────┬──────┘                      │
              │ (1)         │ (2)                         │
              ▼             ▼                             │
       ┌─────────────┐┌─────────────┐                     │
       │Set Attribute││Set Attribute│                     │
       │Segmento =   ││Segmento =   │                     │
       │"Convenio"   ││"Particular" │                     │
       └──────┬──────┘└──────┬──────┘                     │
              │              │                            │
              └──────┬───────┘                            │
                     │                                    │
                     ▼                                    │
       ┌───────────────────────────┐                      │
       │ Check Contact Attributes  │                      │
       │ (Roteamento por Contexto) │                      │
       └──────┬─────────────┬──────┘                      │
              │             │                             │
              ▼             ▼                             │
       ┌─────────────┐┌─────────────┐                     │
       │Set Working Q││Set Working Q│                     │
       │(Consultas)  ││ (Exames...) │                     │
       └──────┬──────┘└──────┬──────┘                     │
              │              │                            │
              └──────┬───────┘                            │
                     │                                    │
                     ▼                                    │
       ┌───────────────────────────┐                      │
       │     Transfer to Queue     │                      │
       └──────┬─────────────┬──────┘                      │
              │             │                             │
              │             ▼ (Espera Alta / Simulação)   │
              │     ┌───────────────────────────┐         │
              │     │ 🟡 Queued Callback        │         │
              │     │ (Oferta de Retorno)       │         │
              │     └─────────────┬─────────────┘         │
              │                   │                       │
              ▼                   ▼                       │
         [ AGENTE ]          [ DISCONNECT ]               │
                                                          │
       ┌──────────────────────────────────────────────────┴─────┐
       │ Tratamento de Erros: Timeout / Inválido / Max Retries │
       └────────────────────────────────────────────────────────┘
