# 🏥 Projeto 8 — Ares Conversational
**Orquestração Conversacional Inteligente com Amazon Connect, Amazon Lex V2, AWS Lambda e Amazon DynamoDB**

---

## 📌 Status do Projeto
🟢 **IMPLEMENTADO E VALIDADO**
*Implementação real na AWS com testes controlados via simulação de NLU e chamadas telefônicas reais (PSTN inbound via DID US).*

---

## 📖 1. Visão Geral e Contexto de Negócio
No ecossistema hospitalar do **Complexo Hospitalar Ares Saúde**, o atendimento ao paciente dependia anteriormente de URAs baseadas em menus numéricos fixos (DTMF). Embora funcionais, menus rígidos geravam atrito, tempo excessivo de navegação e aumento no abandono de chamadas.

O **Projeto 8** moderniza essa camada de entrada, introduzindo uma interface de voz conversacional orientada por Processamento de Linguagem Natural (NLU). O paciente expressa sua necessidade em linguagem natural e o sistema classifica a intenção, extrai identificadores, consulta a base de dados clínica serverless e fornece respostas imediatas ou encaminha com segurança para filas especializadas.

> ⚠️ **Aviso de Dados Fictícios:** Toda a base clínica, nomes de pacientes (`Carlos Eduardo`), tipos de exame, telefones e protocolos (`1001`, `9999`) são puramente ilustrativos e desenvolvidos exclusivamente para demonstração de portfólio técnico. Nenhum dado sensível real foi utilizado.

---

## 🏗️ 2. Arquitetura da Solução

O fluxo transacional opera de forma integrada entre quatro serviços centrais da AWS:

```text
                                [ Chamada Telefônica Inbound (DID US) ]
                                                   │
                                                   ▼
                                         [ Amazon Connect ]
                                   (AR_CF_Conversational / pt-BR)
                                                   │
                                                   ▼
                                         [ Amazon Lex V2 ]
                                     (AR_Lex_AtendimentoAres)
                                                   │
                  ┌────────────────────────────────┼────────────────────────────────┐
                  │ (ConsultarExame)               │ (Outras Intenções)             │ (Default / Fallback)
                  ▼                                ▼                                ▼
        [ Captura DTMF ]                 [ Prompts de Negócio ]           [ AR_PlayFallback ]
        (4 dígitos: PacienteId)          (Financeiro / Canc. / Agend.)            │
                  │                                                                ▼
                  ▼                                                       [ AR_SetQueue_Basic ]
         [ AWS Lambda ]                                                            │
       (AR_LF_ConsultaExame)                                                       ▼
                  │                                                       [ Fila de Atendimento ]
                  ▼
         [ Amazon DynamoDB ]
         (AR_TB_Pacientes)
                  │
                  ▼
       [ AR_CheckLaudoValido ]
      ($.External.status == SUCCESS)
                  │
         ┌────────┴────────┐
         │ (True)          │ (False / NOT_FOUND)
         ▼                 ▼
  [ AR_PlayLaudoExame ] [ AR_PlayFallback ]
         │                 │
         ▼                 ▼
    [ Desconexão ]   [ Transferência para Fila ]
