# 🏛️ Arquitetura Técnica — Projeto 4: Modularização com Flow Modules
**Ecossistema Ares Saúde | Complexo: Hospital Ares**

## 1. Visão Geral da Arquitetura
O Projeto 4 marca a transição da arquitetura monolítica da Clínica Ares para um modelo modular orientado a componentes corporativos reaproveitáveis (*Flow Modules*). O fluxo mestre `AR_CF_Hospital_Principal` atua como um orquestrador desacoplado, delegando responsabilidades transversais a três módulos especializados:

1. **`AR_MD_Inicializacao`**: Ativação de telemetria no Amazon CloudWatch e definição do motor de voz institucional.
2. **`AR_MD_Verifica_Horario`**: Avaliação de conformidade com o horário de funcionamento e encerramento de contingência fora de expediente.
3. **`AR_MD_Tratamento_Erros`**: Controle centralizado de exceções, contagem de retentativas e desligamento seguro anti-loop.

---

## 2. Diagrama de Arquitetura Lógica

```
                               ┌────────────────────────────────────────┐
                               │   Entrada da Chamada Hospitalar        │
                               └──────────────────┬─────────────────────┘
                                                  │
                                                  ▼
                               ┌────────────────────────────────────────┐
                               │     Invoke: AR_MD_Inicializacao        │
                               │  - FlowLoggingBehavior: Enabled        │
                               │  - Set Voice: Vitoria (Neural, pt-BR)  │
                               └──────────────────┬─────────────────────┘
                                                  │ (Sucesso)
                                                  ▼
                               ┌────────────────────────────────────────┐
                               │    Invoke: AR_MD_Verifica_Horario      │
                               │  - Tabela: AR_HO_Clinica               │
                               └──────────┬──────────────────┬──────────┘
                                          │                  │
                         (Dentro Horário) │                  │ (Fora / Erro)
                                          ▼                  ▼
              ┌─────────────────────────────────────┐   ┌───────────────────────────┐
              │      AR_CF_Hospital_Principal       │   │ Prompt: Fechado           │
              │  - Play Prompt: Boas-vindas         │   │ Disconnect                │
              │  - Get Customer Input (DTMF 1, 2, 3)│   └───────────────────────────┘
              └───────┬───────────┬───────────┬─────┘
                      │           │           │
           (Opção 1)  │ (Opção 2) │ (Opção 3) │ (Inválido / Timeout / Erro)
                      ▼           ▼           ▼           │
             ┌──────────┐┌──────────┐┌──────────┐         ▼
             │ Set Queue││ Set Queue││ Set Queue│ ┌───────────────────────────────┐
             │Consultas ││  Exames  ││Financeiro│ │ Invoke: AR_MD_Tratamento_Erros│
             └────┬─────┘└────┬─────┘└────┬─────┘ │ - Play Prompt: Opção Inválida │
                  │           │           │       │ - Set Attribute: Tentativas=1 │
                  ▼           ▼           ▼       │ - Check Attribute: < 2        │
             ┌──────────────────────────────────┐ └───────┬───────────────────┬───┘
             │        Transfer to Queue         │         │ (Retentativa)     │ (Excedido)
             └──────────────────────────────────┘         ▼                   ▼
                                                 (Volta ao Menu)   ┌───────────────────┐
                                                                   │ Prompt: Limite    │
                                                                   │ Disconnect        │
                                                                   └───────────────────┘
