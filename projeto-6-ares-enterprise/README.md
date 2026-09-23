# 🏛️ Projeto 6 — Ares Enterprise: Governança, DR e Observabilidade
**Ecossistema Hospitalar Ares | Amazon Connect CCaaS Architecture**

Este repositório consolida a camada corporativa e de governança do Complexo Hospitalar Ares, encerrando a Fundação de Arquitetura do Contact Center.

## 📌 Visão Geral da Solução
O Projeto 6 implementa as práticas de sustentação de ambientes de missão crítica:
* **Segregação de Funções (RBAC):** Quatro Security Profiles corporativos desenhados sob o princípio de Menor Privilégio (*Least Privilege*).
* **Continuidade de Negócios (DR):** Fluxo dedicado `AR_CF_Contingencia_DR` com RTO <= 5 minutos e RPO <= 0 minutos (Flow-as-Code).
* **Observabilidade Proativa:** Mapeamento de métricas operacionais e limiares de alarme no Amazon CloudWatch.
* **Procedimentos Operacionais (SOP):** Runbook detalhado para acionamento de contingência e retorno assistido (*Failover / Failback*).

## 📂 Estrutura do Repositório
```
projeto-6-ares-enterprise/
├── README.md
├── docs/
│   ├── architecture.md
│   ├── decisions.md
│   ├── disaster-recovery.md
│   ├── observability.md
│   ├── security-profiles.md
│   ├── testing.md
│   └── troubleshooting.md
├── evidence/
│   ├── diagramas/
│   └── security-profiles/
└── src/
    └── contact-flows/
        └── AR_CF_Contingencia_DR.json


## 📐 Fluxograma da Operação de Contingência (Disaster Recovery)

```
       [ Incidente Crítico Detectado ] (Queda de agentes / Indisponibilidade de Filas)
                       │
                       ▼
       [ Acionamento do Runbook de DR ] (Engenharia com perfil AR_SP_Admin_Fluxos)
                       │
                       ▼
       [ Comutação do Apontamento do Número ] ────▶ Aponta para: AR_CF_Contingencia_DR
                                                               │
                       ┌───────────────────────────────────────┘
                       │
                       ▼
       ┌───────────────────────────────┐
       │     AR_CF_Contingencia_DR     │
       │            (Início)           │
       └───────────────┬───────────────┘
                       │
                       ▼
       ┌───────────────────────────────┐
       │          Definir Voz          │ ────▶ Voz Neural (Camila/Vitória pt-BR)
       └───────────────┬───────────────┘
                       │
                       ▼
       ┌───────────────────────────────┐
       │  Habilitar Registro em Log    │ ────▶ Gera auditoria no CloudWatch Logs
       └───────────────┬───────────────┘
                       │
                       ▼
       ┌───────────────────────────────┐
       │     Reproduzir Mensagem       │ ────▶ "Atenção: o Complexo Hospitalar Ares
       │        (Play Message)         │        está operando em contingência..."
       └───────────────┬───────────────┘
                       │ (Êxito ou Erro)
                       ▼
       ┌───────────────────────────────┐
       │          Desconectar          │ ────▶ Encerramento limpo e seguro
       └───────────────────────────────┘
