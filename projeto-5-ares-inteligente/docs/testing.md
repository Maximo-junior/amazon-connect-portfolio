# 🧪 Matriz de Testes — Projeto 5: Ares Inteligente

**Ecossistema Ares Saúde | Complexo: Hospital Ares**

---

| ID | Cenário / Objetivo | Pré-condição | Entrada | Comportamento Esperado | Status |
|---|---|---|---|---|---|
| TC-011 | Autosserviço de Exame com Laudo Disponível | Fluxo modelado e contrato `FOUND` válido | Entrada DTMF `1` (ou Intent Lex) | Simular o retorno dos dados do laudo (Ressonância Magnética, 20/09), reproduzir a resposta ao paciente e seguir para encerramento com sucesso | 🟢 PASS |

| TC-012 | Transbordo para Fila Humana | Chamada ativa no menu inicial | Entrada DTMF `2` (Falar com Atendente) | Direcionar para a fila `AR_Q_Consultas` e executar a etapa de transferência para atendimento humano | 🟢 PASS |

| TC-013 | Tratamento de Entrada Inválida no Autosserviço | Menu inicial aguardando dígito | Entrada inválida (ex.: `8`) | Acionar `AR_MD_Tratamento_Erros`, informar o paciente sobre a opção inválida e retornar ao menu | 🟢 PASS |

| TC-014 | Excesso de Tentativas sem Seleção | Menu inicial aguardando entrada | 2 timeouts consecutivos | Identificar `Tentativas >= 2`, reproduzir a mensagem de limite de tentativas e encerrar o fluxo | 🟢 PASS |

| TC-015 | Contrato Serverless: Consulta com Sucesso | Script local `consulta_exame.py` e contrato de entrada válido | Evento com `idPaciente: "ARES-702"` | Retornar `statusCode: 200`, `statusExame: "FOUND"` e os metadados simulados do laudo | 🟢 PASS |

| TC-016 | Contrato Serverless: Paciente Não Encontrado | Script local `consulta_exame.py` e contrato de entrada válido | Evento com `idPaciente: "ARES-999"` | Retornar `statusCode: 404` e `statusExame: "NOT_FOUND"` | 🟢 PASS |

| TC-017 | Resiliência em Falha de Processamento | Script local `consulta_exame.py` | Evento com parâmetro obrigatório ausente ou payload inválido | Validar o tratamento controlado da exceção, retornando erro estruturado sem interrupção não tratada da execução | 🟢 PASS |

| TC-018 | Contrato Serverless: Timeout Simulado | Script local `consulta_exame.py` e cenário de timeout definido | Evento válido com condição de timeout simulada | Retornar `statusExame: "TIMEOUT"` e permitir que o fluxo trate a indisponibilidade conforme o contrato definido | 🟢 PASS |

| TC-019 | Contrato Serverless: Erro Interno Simulado | Script local `consulta_exame.py` | Evento que provoque falha interna controlada | Retornar `statusExame: "ERROR"` com resposta estruturada, sem exceção não tratada | 🟢 PASS |

---

## 📌 Observações de Execução

Os testes **TC-011 a TC-014** validam o comportamento lógico do Contact Flow e de seus módulos reutilizáveis.

Os testes **TC-015 a TC-019** validam o contrato e a lógica da função `AR_LF_ConsultaExame` por meio de execução local e eventos JSON simulados.

Neste projeto, a função Lambda não é implantada ou executada em infraestrutura AWS tarifada. Os testes serverless representam o comportamento esperado de uma futura função AWS Lambda e são executados localmente para preservar a política de:

> **Custo Real = R$ 0,00**

Os contratos utilizados nos testes estão armazenados em `simulations/lambda/`.

---

## Cenários de resposta

| Status | Significado |
|---|---|
| `FOUND` | Exame localizado e dados disponíveis |
| `NOT_FOUND` | Paciente ou exame não localizado |
| `TIMEOUT` | Consulta excedeu o tempo esperado |
| `ERROR` | Falha interna ou erro controlado no processamento |

---

## 🔗 Relação com os Artefatos

| Componente | Artefato relacionado |
|---|---|
| Contact Flow | `src/contact-flows/AR_CF_Ares_Inteligente.json` |
| Lambda modelada | `src/lambda/consulta_exame.py` |
| Evento de entrada | `simulations/lambda/event-connect-request.json` |
| Resposta `FOUND` | `simulations/lambda/response-found.json` |
| Resposta `NOT_FOUND` | `simulations/lambda/response-not-found.json` |
| Resposta `TIMEOUT` | `simulations/lambda/response-timeout.json` |
| Resposta `ERROR` | `simulations/lambda/response-error.json` |
