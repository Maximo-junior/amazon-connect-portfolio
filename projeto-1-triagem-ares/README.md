# Projeto 1: URA de Triagem Inicial – Clínica Ares 🏥

## 📋 Visão Geral
Este projeto consiste no desenho, arquitetura e implementação da URA (Unidade de Resposta Audível) de triagem inicial para a **Clínica Ares**, um grupo médico em expansão. O foco principal é otimizar o atendimento receptivo de clientes, eliminando gargalos de triagem e aplicando regras rígidas de tratamento de falhas.

---

## 💼 Contexto de Negócio
A Clínica Ares identificou que mais de 40% das chamadas perdidas ou abandonadas ocorriam devido a tempos de espera excessivos no primeiro contato ou por falhas de digitação do cliente em menus complexos.
Esta solução resolve o problema estabelecendo um menu de triagem simples de nível único, direcionando o tráfego para os departamentos corretos e protegendo o sistema contra loops de atendimento que estressam o cliente e consomem recursos.

---

## 🛠️ Detalhes de Arquitetura e Fluxo

### 1. Governança de Nomenclatura (Naming Conventions)
Para manter o padrão de governança corporativa, todos os recursos utilizam o prefixo `AR` (Ares), seguido pelo tipo de recurso e função:
*   **Contact Flow:** `AR_CF_Triagem_Inicial`
*   **Prompts (TTS):**
    *   `AR_PR_Saudacao` (Boas-vindas)
    *   `AR_PR_Menu_Principal` (Opções de atendimento)
    *   `AR_PR_Encerramento` (Mensagem de tchau cortês)

### 2. O Circuito Defensivo (UX/CX Base)
Para mitigar falhas de digitação ou ausência de interação, projetamos um fluxo inteligente de tratamento de exceções:
*   **Default (Opção Inválida):** Caso o cliente digite uma tecla inexistente no menu.
*   **Timeout (Tempo Limite):** Caso o cliente não digite nenhuma opção dentro do limite de 5 segundos.
*   **Contador de Tentativas:** O cliente tem direito a duas tentativas de digitação. Se errar ou não responder pela segunda vez consecutiva, o sistema executa uma mensagem cortês de encerramento (`AR_PR_Encerramento`) e desliga a chamada com segurança, impedindo que o contato fique preso infinitamente na URA.

---

## 📐 Fluxograma da Solução

O desenho lógico da URA segue a estrutura de decisão abaixo:

```text
               [ INÍCIO DA CHAMADA ]
                         │
                         ▼
        ┌──────────────────────────────────┐
        │  AR_CF_Triagem_Inicial (Flow)    │
        └──────────────────────────────────┘
                         │
                         ▼
        ┌──────────────────────────────────┐
        │       AR_PR_Saudacao (TTS)       │
        │ "Obrigado por ligar para a Ares" │
        └──────────────────────────────────┘
                         │
                         ▼
      ┌──────────────────────────────────────┐
 ───► │      AR_PR_Menu_Principal            │ ◄─── Retornos limitados
│     │  "Digite 1, 2 ou 3 para os setores"  │     (Circuito Defensivo)
│     └──────────────────────────────────────┘
│            │           │          │
│        [Opção 1]   [Opção 2]  [Opção 3]
│            │           │          │
│            ▼           ▼          ▼
│       ┌─────────┐ ┌─────────┐ ┌─────────┐
│       │ Fila:   │ │ Fila:   │ │ Fila:   │
│       │ Consult │ │ Exames  │ │ Finance │
│       └─────────┘ └─────────┘ └─────────┘
│
│      (Se Errar o Teclado / Tempo Limite Esgotar)
│            │
│            ▼
│     [ Branches: Default / Timeout ]
│            │
│            ▼
│     [ Incrementa Contador de Erros ]
│            │
│    (Tentativa <= 2?)
│     /             \
│   [Sim]           [Não]
│    /               \
└───┘                 ▼
             ┌──────────────────────────────────┐
             │       AR_PR_Encerramento         │
             │   "Limite de tentativas excedido.│
             │     Por favor, tente mais tarde" │
             └──────────────────────────────────┘
                              │
                              ▼
                       [ DISCONNECT ]


## 🪙 Abordagem FinOps (Custo Zero)
Para garantir risco zero de cobrança na AWS, o projeto foi arquitetado sob as seguintes premissas:

*   **Telefonia Pública Desativada:** Sem números de telefone reais (DID/Toll-Free) associados, evitando custos de assinatura mensal da operadora.
*   **Simulação Digital:** Validação do fluxo executada exclusivamente através de emulação via Web Chat nativo da AWS.
*   **Sem Serviços Cognitivos Pagos:** Uso exclusivo do motor nativo de Text-to-Speech (TTS) padrão da AWS, sem dependências de inteligência artificial externa (Amazon Lex) tarifada por requisição.
