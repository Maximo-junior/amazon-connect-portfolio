# 🏛️ Arquitetura Corporativa, Resiliência e Governança
**Projeto 6: Ares Enterprise | Complexo Hospitalar Ares**

---

## 📌 Visão Geral da Arquitetura
O Projeto 6 formaliza a camada de governança corporativa e continuidade de negócio (*Business Continuity Plan - BCP*) do Complexo Hospitalar Ares. O desenho arquitetural assegura uma separação rigorosa entre a **Camada de Controlo (Control Plane)** e a **Camada de Execução de Voz (Data/Execution Plane)**, estabelecendo mecanismos de recuperação rápida contra incidentes técnicos operacionais.

---

## 🏗️ Topologia da Solução

```text
                                  CAMADA DE CONTROLO (RBAC)
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │                                Amazon Connect                                   │
    │                                                                                 │
    │  [AR_SP_Atendente]    [AR_SP_Supervisor]    [AR_SP_Auditoria]   [AR_SP_Admin]   │
    │      (CCP Only)         (Real-Time Met.)     (Logs/Relatórios)   (Flows/Deploy) │
    └───────────────────────────────────────────────────────┬─────────────────────────┘
                                                            │ Governação & Manobra
                                                            ▼
                                  CAMADA DE EXECUÇÃO (Voz & DR)
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │                                                                                 │
    │   [ Chamada Recebida ] ──▶ [ Número Telefónico Principal (DID) ]                │
    │                                           │                                     │
    │               ┌───────────────────────────┴───────────────────────────┐         │
    │               │ (Operação Regular)        │ (Incidente / Failover)    │         │
    │               ▼                           ▼                           │         │
    │     [ AR_CF_Hospital_Principal ]   [ AR_CF_Contingencia_DR ]          │         │
    │         (Triagem / Filas)                 │                           │         │
    │                                           ├─▶ Set Voice (Neural)      │         │
    │                                           ├─▶ Set Logging Behavior    │         │
    │                                           ├─▶ Play Message (Aviso PA) │         │
    │                                           └─▶ Disconnect Controlado   │         │
    │                                                   │                   │         │
    │                                                   ▼                   │         │
    │                                           [ CloudWatch Logs ]         │         │
    └─────────────────────────────────────────────────────────────────────────────────┘
