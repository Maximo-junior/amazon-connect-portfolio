
# Projeto 1: URA de Triagem Inicial – Clínica Ares 🏥

## 📋 Visão Geral

Este projeto consiste no desenho, arquitetura e implementação de uma URA (Unidade de Resposta Audível) de triagem inicial para a **Clínica Ares**, um grupo médico fictício em expansão.

O foco principal é estruturar o primeiro contato do cliente, simplificando a identificação do setor desejado e aplicando regras de tratamento de falhas para evitar repetições indefinidas no fluxo.

---

## 💼 Contexto de Negócio

A Clínica Ares identificou a necessidade de melhorar sua etapa inicial de atendimento, reduzindo problemas relacionados a menus complexos, opções digitadas incorretamente e ausência de interação por parte do cliente.

A solução propõe um menu de triagem simples, com três opções:

- **1 — Consultas**
- **2 — Exames**
- **3 — Financeiro**

Neste primeiro projeto, os departamentos ainda não possuem filas reais de atendimento. Cada opção será representada por um destino simulado, permitindo concentrar o desenvolvimento nos fundamentos de lógica da URA e tratamento de exceções.

---

## 🛠️ Detalhes de Arquitetura e Fluxo

### 1. Governança de Nomenclatura (Naming Conventions)

Para manter um padrão de organização, todos os recursos utilizam o prefixo `AR` (Ares), seguido pelo tipo de recurso e sua função:

- **Contact Flow:** `AR_CF_Triagem_Inicial`
- **Prompts (TTS):**
  - `AR_PR_Saudacao` — Boas-vindas
  - `AR_PR_Menu_Principal` — Opções de atendimento
  - `AR_PR_Opcao_Invalida` — Tratamento de opção inválida
  - `AR_PR_Encerramento` — Mensagem de encerramento

### 2. Circuito Defensivo (UX/CX Base)

Para tratar falhas de digitação ou ausência de interação, o fluxo possui regras de tratamento de exceções:

- **Opção Inválida:** caso o cliente digite uma opção diferente de `1`, `2` ou `3`.
- **Timeout:** caso o cliente não forneça nenhuma entrada dentro do tempo configurado.
- **Controle de Tentativas:** o cliente terá até duas tentativas para fornecer uma opção válida. Caso o limite seja atingido, o fluxo executará a mensagem `AR_PR_Encerramento` e finalizará o contato.

O objetivo é impedir que o cliente permaneça preso em um loop infinito dentro da URA.

---

## 📐 Fluxograma da Solução

O desenho lógico da URA segue a estrutura abaixo:

```text
                [ INÍCIO ]
                    │
                    ▼
      ┌─────────────────────────────┐
      │ AR_CF_Triagem_Inicial       │
      └──────────────┬──────────────┘
                     │
                     ▼
      ┌─────────────────────────────┐
      │ AR_PR_Saudacao              │
      │ "Bem-vindo à Clínica Ares"  │
      └──────────────┬──────────────┘
                     │
                     ▼
      ┌─────────────────────────────┐
  ┌──►│ AR_PR_Menu_Principal        │
  │   │                             │
  │   │ 1 - Consultas               │
  │   │ 2 - Exames                  │
  │   │ 3 - Financeiro              │
  │   └──────────────┬──────────────┘
  │                  │
  │        ┌─────────┼─────────┐
  │        │         │         │
  │        ▼         ▼         ▼
  │   [Opção 1] [Opção 2] [Opção 3]
  │        │         │         │
  │        ▼         ▼         ▼
  │   Consultas   Exames   Financeiro
  │        │         │         │
  │        └─────────┼─────────┘
  │                  │
  │                  ▼
  │         [ Destino Simulado ]
  │                  │
  │                  ▼
  │        AR_PR_Encerramento
  │                  │
  │                  ▼
  │             [ DISCONNECT ]
  │
  │
  │    [ Opção Inválida / Timeout ]
  │                  │
  │                  ▼
  │       AR_PR_Opcao_Invalida
  │                  │
  │                  ▼
  │       [ Controle de Tentativas ]
  │                  │
  │            Tentativa < 2?
  │             /          \
  │           SIM          NÃO
  │            │             │
  └────────────┘             ▼
                    AR_PR_Encerramento
                             │
                             ▼
                        [ DISCONNECT ]
````

---

## 🪙 Abordagem FinOps (Custo Zero)

Este projeto foi estruturado com a premissa de não gerar intencionalmente custos durante o laboratório.

Para isso:

* **Telefonia Pública não provisionada:** nenhum número real DID ou Toll-Free será utilizado no projeto.
* **Destinos simulados:** Consultas, Exames e Financeiro serão representados logicamente, sem utilização de filas ou atendimento real.
* **Sem integrações externas:** Amazon Lex, AWS Lambda, APIs externas e outros serviços adicionais não fazem parte deste projeto.
* **Simulação e documentação:** componentes que poderiam exigir recursos tarifados serão representados através da arquitetura e da documentação técnica.

O foco deste primeiro projeto é exclusivamente o aprendizado e implementação da lógica básica de uma URA no Amazon Connect.

```
```
