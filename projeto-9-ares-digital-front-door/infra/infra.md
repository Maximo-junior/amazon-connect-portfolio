# 🧱 Infraestrutura & Provisionamento — Projeto 9 (`Ares Digital Front Door`)

> **Status de Provisionamento:** 🟢 Implementado e Validado via AWS Console & Amazon Connect Console
> **Padrão Arquitetural:** Serverless • Pay-per-Use (FinOps) • IAM Least Privilege

---

## 🎯 Visão Geral da Infraestrutura

Neste MVP da Fase 3, toda a infraestrutura foi provisionada e validada diretamente no **AWS Console** e no **Amazon Connect Console** (`us-east-1`), garantindo agilidade na validação funcional, controle estrito de custos (FinOps) e inspeção ponta a ponta antes de empacotar módulos em Terraform nos projetos seguintes.

```text
[Amazon Connect Instance (us-east-1)]
 ├── Contact Flow Principal : Ares_Fluxo_Recepcao_Digital
 ├── Step-by-Step Guide    : AR_FL_Guia_Atendente
 └── Agent Workspace View  : AR_VW_Ficha_Paciente
        │
        ├──► [AWS Lambda] AR_LF_Paciente_Identificar ──► [DynamoDB] AR_TB_Pacientes
        └──► [AWS Lambda] AR_LF_Recepcao_Classificar ──► [Amazon Bedrock]
