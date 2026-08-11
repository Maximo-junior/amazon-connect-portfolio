# 🏥 Projeto 1 — URA de Triagem Inicial | Clínica Ares

## 📋 Visão Geral

Este projeto contempla o desenho, arquitetura, implementação e validação de uma URA (Unidade de Resposta Audível) de Triagem Inicial para a **Clínica Ares**, um grupo médico fictício utilizado como cenário para o desenvolvimento de um ecossistema de Contact Center no Amazon Connect.

A solução representa a primeira camada de atendimento receptivo, responsável por identificar o setor desejado pelo paciente e direcionar logicamente a chamada entre:

- **1 — Consultas**
- **2 — Exames**
- **3 — Financeiro**

Além da navegação DTMF, o projeto implementa um circuito defensivo anti-loop, responsável pelo tratamento de entradas inválidas e ausência de resposta (Timeout), evitando que o cliente permaneça indefinidamente dentro da URA.

> 💰 **Premissa FinOps:** O laboratório foi desenvolvido priorizando custo real de **R$ 0,00**, simulando componentes que exigiriam recursos adicionais ou telefonia pública.

---

## 🎯 Problema de Negócio

A Clínica Ares identificou a necessidade de melhorar sua etapa inicial de atendimento, reduzindo problemas relacionados a:

- Menus complexos;
- Direcionamento incorreto de chamadas;
- Opções digitadas incorretamente;
- Ausência de interação do cliente;
- Repetições indefinidas dentro da URA;
- Consumo desnecessário de recursos.

Como solução, foi criada uma URA simples e objetiva, permitindo que o paciente escolha diretamente o setor desejado.

Neste primeiro projeto, os departamentos ainda não possuem filas reais de atendimento. Os destinos de Consultas, Exames e Financeiro são representados por prompts e caminhos simulados, permitindo concentrar o desenvolvimento nos fundamentos do Amazon Connect, na lógica da URA, no controle de estado e no tratamento de exceções.

---

## 🏛️ Arquitetura da Solução

### Componentes Principais

| Componente | Implementação |
| :--- | :--- |
| **Contact Flow** | `AR_CF_Triagem_Inicial` |
| **Síntese de Voz** | Amazon Polly (Voz Vitória - pt-BR) |
| **Entrada do Cliente** | DTMF (Opções 1, 2 e 3) |
| **Timeout** | 5 segundos |
| **Controle de Estado** | User Defined Attribute (`Tentativas`) |
| **Tratamento de Falhas** | Circuito defensivo anti-loop (Limite: 2 falhas) |
| **Destinos** | Simulados via TTS |
| **Telefonia Pública** | Não provisionada (FinOps R$ 0,00) |

---

## 🏷️ Governança de Nomenclatura

Para manter organização, padronização e facilitar a evolução futura do ambiente, os recursos seguem uma convenção de nomenclatura utilizando o prefixo `AR`, referente ao ecossistema Ares.

- **Contact Flow:** `AR_CF_Triagem_Inicial`
- **Prompts / TTS:**
  - `AR_PR_Saudacao`
  - `AR_PR_Menu_Principal`
  - `AR_PR_Opcao_Invalida`
  - `AR_PR_Encerramento`

| Recurso | Finalidade |
| :--- | :--- |
| `AR_PR_Saudacao` | Mensagem inicial de boas-vindas |
| `AR_PR_Menu_Principal` | Apresentação das opções Consultas, Exames e Financeiro |
| `AR_PR_Opcao_Invalida` | Tratamento de entrada inválida ou ausência de resposta |
| `AR_PR_Encerramento` | Mensagem executada antes da finalização do contato |

Essa estrutura cria uma base de governança que poderá ser reutilizada nos próximos projetos do Ecossistema Ares Saúde.

---

## ☎️ Menu Principal — DTMF

O menu principal utiliza entrada via teclado numérico (DTMF) para identificar o setor desejado pelo paciente:

- **Digite 1** → Consultas
- **Digite 2** → Exames
- **Digite 3** → Financeiro

O sistema aguarda a interação durante **5 segundos**. Uma entrada válida direciona o contato para o respectivo destino lógico. Como este projeto não utiliza filas reais, cada setor possui uma confirmação simulada antes do encerramento do contato.

---

## 🛡️ Circuito Defensivo Anti-Loop

Um dos principais objetivos técnicos deste projeto é impedir que uma chamada permaneça presa indefinidamente dentro da URA. Para isso, foi implementado um controle de tentativas utilizando atributos de contato.

### 1. Inicialização
No início do fluxo é criado o atributo `Tentativas = 0`, funcionando como um controle de estado durante a execução do contato.

### 2. Entrada Inválida & Timeout
Caso o cliente digite qualquer opção diferente de `1`, `2` ou `3`, ou caso nenhuma entrada seja recebida durante os 5 segundos configurados, o evento é tratado da seguinte forma:

Entrada Inválida / Timeout
            ↓
  AR_PR_Opcao_Invalida
            ↓
  Incrementa Tentativas
            ↓
    Verifica Limite




[ INÍCIO ]
                    │
                    ▼
      ┌─────────────────────────────┐
      │ AR_CF_Triagem_Inicial       │
      └──────────────┬──────────────┘
                     │
                     ▼
      ┌─────────────────────────────┐
      │ Tentativas = 0              │
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
  │         Tentativas + 1
  │                  │
  │                  ▼
  │           Tentativas < 2?
  │             /          \
  │           SIM          NÃO
  │            │             │
  └────────────┘             ▼
                    AR_PR_Encerramento
                             │
                             ▼
                        [ DISCONNECT ]
