# Arquitetura Técnica — Projeto 8 (Ares Conversational)

## 1. Visão Geral
O **Projeto 8** implementa o primeiro ponto de contacto conversacional inteligente do Complexo Hospitalar Ares Saúde, combinando o **Amazon Connect** para orquestração de voz e telefonia com o **Amazon Lex V2** para processamento de linguagem natural (NLU), integrando-se de forma síncrona com o backend serverless construído sobre **AWS Lambda** e **Amazon DynamoDB**.

## 2. Diagrama de Fluxo e Topologia

```text
                             [ Chamada Telefônica / DID ]
                                           │
                                           ▼
                                 [ Amazon Connect ]
                           (AR_CF_Conversational / pt-BR)
                                           │
                                           ▼
                                 [ Amazon Lex V2 ]
                             (AR_Lex_AtendimentoAres)
                                           │
                  ┌────────────────────────┼────────────────────────┐
                  │ (ConsultarExame)       │ (Outras Intenções)     │ (Default / Fallback)
                  ▼                        ▼                        ▼
        [ Captura DTMF ]         [ Respostas de Negócio ]   [ AR_PlayFallback ]
        (4 dígitos: PacienteId)   (Financeiro / Canc./Ag.)         │
                  │                                                 ▼
                  ▼                                        [ AR_SetQueue_Basic ]
         [ AWS Lambda ]                                            │
       (AR_LF_ConsultaExame)                                        ▼
                  │                                       [ Fila de Atendimento ]
                  ▼
         [ Amazon DynamoDB ]
         (AR_TB_Pacientes)
                  │
                  ▼
       [ Validação Defensiva ]
      ($.External.status == SUCCESS)
                  │
         ┌────────┴────────┐
         │ (True)          │ (False / NOT_FOUND)
         ▼                 ▼
  [ Síntese do Laudo ]  [ AR_PlayFallback ]
  (AR_PlayLaudoExame)             │
         │                        ▼
         ▼              [ AR_SetQueue_Basic ]
    [ Desconexão ]
