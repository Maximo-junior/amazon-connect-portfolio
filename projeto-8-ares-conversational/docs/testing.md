# Homologação & Casos de Teste — Projeto 8

## 1. Metodologia de Teste
Os testes foram executados em duas etapas complementares:
1. **Simulação Web a Custo Zero:** Inspeção de payloads no console do Amazon Lex V2.
2. **Telefonia Real Controlada:** Chamadas de voz originadas para o número DID US alocado na instância do Amazon Connect, avaliando o comportamento conjunto de ASR, NLU, DTMF, Lambda e síntese TTS.

## 2. Matriz de Casos de Teste

| ID | Cenário | Entrada do Utilizador | Comportamento Esperado | Resultado Obtido | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-008-01** | Caminho Feliz Consulta Exame | Voz: *"Gostaria de ver o resultado do meu exame"*<br>DTMF: `1001` | Lex reconhece `ConsultarExame`, Connect coleta `1001`, Lambda valida `status=SUCCESS` e Polly reproduz laudo de Carlos Eduardo. | Laudo reproduzido com sucesso: *"Olá, Carlos Eduardo. Localizamos seu exame..."*. | 🟢 **PASS** |
| **TC-008-02** | Consulta Agendamento | Voz: *"Quando é o meu próximo agendamento"* | Lex reconhece `ConsultarAgendamento` e Connect sintetiza prompt de retorno às 14h de quinta-feira. | Mensagem de agendamento reproduzida e chamada finalizada. | 🟢 **PASS** |
| **TC-008-03** | Cancelamento de Agendamento | Voz: *"Quero cancelar meu agendamento"* | Lex reconhece `CancelarAgendamento` e Connect confirma registro de desmarcação no sistema. | Mensagem de cancelamento reproduzida com sucesso. | 🟢 **PASS** |
| **TC-008-04** | Assunto Financeiro | Voz: *"Segunda via do boleto"* | Lex reconhece `ConsultarFinanceiro` e informa envio de orientações de pagamento por SMS. | Mensagem de boleto reproduzida com sucesso. | 🟢 **PASS** |
| **TC-008-05** | Transbordo para Atendente | Voz: *"Quero falar com um atendente humano"* | Lex reconhece `FalarComAtendente` e Connect transfere chamada para a fila `BasicQueue`. | Chamada enfileirada com sucesso na fila de suporte. | 🟢 **PASS** |
| **TC-008-06** | Defesa de NLU (Ruído Acústico) | Voz: *"Abobrinha azul com parafuso de madeira"* | Score fica abaixo do limiar (0.76 < 0.85); Lex desvia para Fallback; Connect toca prompt de contingência e transfere. | Prompt de contingência reproduzido sem disparar intenção indevida. | 🟢 **PASS** |
| **TC-008-07** | Defesa de Backend (Paciente Inexistente) | Voz: *"Gostaria de ver o resultado do meu exame"*<br>DTMF: `9999` | Lambda devolve `status=NOT_FOUND`; bloco `AR_CheckLaudoValido` avalia falso e desvia para prompt de contingência. | URA não reproduziu strings vazias; chamada desviada para contingência. | 🟢 **PASS** |

## 3. Rastreabilidade de Evidências
* **Áudios de Chamadas:** Armazenados em `evidence/audio/` (`TC-008-01_sucesso_consulta_exame.mp3` e `TC-008-06_fallback_ruido.mp3`).
* **Telemetria CloudWatch:** Logs JSON salvos em `evidence/cloudwatch/`.
* **Exportações:** Contact Flow publicado (`AR_CF_Conversational.json`) e pacote do bot Lex V2 (`AR_Lex_AtendimentoAres_Export.zip`).
