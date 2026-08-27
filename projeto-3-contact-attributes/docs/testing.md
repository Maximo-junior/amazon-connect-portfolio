# 🧪 Plano e Matriz de Testes — Projeto 3 (Contact Attributes e Contexto)
**Ecossistema Ares Saúde | Módulo: Roteamento por Contexto e Observabilidade**

---

## 📌 Visão Geral e Estratégia de Testes
O objetivo desta suíte de testes é validar a integridade lógica, a persistência de metadados em sessão, o roteamento dinâmico e o tratamento defensivo de falhas no Contact Flow `AR_CF_Triagem_Contexto`.

Em conformidade com a governança **FinOps R$ 0,00**, todos os testes de fluxo e de interface de agente são homologados via validação estática de grafos no Flow Designer, exportação JSON e emulação no softphone nativo do console (WebRTC), sem provisionamento de linhas telefônicas públicas (PSTN/DID) ou chamadas tarifadas.

---

## 📊 Matriz Resumo de Execução

| ID | Cenário / Funcionalidade | Canal Avaliado | Tipo | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-001** | Gravação de Atributos do Setor (Menu 1 - Consultas) | Voz (DTMF) | Funcional (Happy Path) | 🟢 PASS |
| **TC-002** | Gravação de Atributos do Setor (Menu 1 - Exames) | Voz (DTMF) | Funcional (Happy Path) | 🟢 PASS |
| **TC-003** | Gravação de Atributos do Setor (Menu 1 - Financeiro) | Voz (DTMF) | Funcional (Happy Path) | 🟢 PASS |
| **TC-004** | Gravação de Segmentação (Menu 2 - Convênio) | Voz (DTMF) | Funcional (Happy Path) | 🟢 PASS |
| **TC-005** | Gravação de Segmentação (Menu 2 - Particular) | Voz (DTMF) | Funcional (Happy Path) | 🟢 PASS |
| **TC-006** | Roteamento Condicional via `Check contact attributes` | Sessão / Memória | Lógica / Decisão | 🟢 PASS |
| **TC-007** | Screen Pop / Entrega de Contexto no Agent Workspace | WebRTC / CCP | Integração / CX | 🟡 SIMULATED |
| **TC-008** | Auditoria e Emissão de Logs no CloudWatch (`Set logging`) | Telemetria AWS | Observabilidade | 🟢 PASS |
| **TC-009** | Entrada Inválida e Timeout no Menu de Segmentação | Voz (DTMF) | Negativo / Defensivo | 🟢 PASS |
| **TC-010** | Limite de Tentativas Excedido e Encerramento Gracioso | Voz (DTMF) | Negativo / Anti-Loop | 🟢 PASS |
| **TC-011** | Entrada de Texto Livre em Menu DTMF via Web Chat | Web Chat | Incompatibilidade de Canal | 🟢 PASS |
| **TC-012** | Simulação de Retorno em Espera Alta (Queued Callback) | Fila / Callback | Arquitetural | 🟡 SIMULATED |

---

## 🧪 Casos de Teste Detalhados

### TC-001: Gravação de Atributos do Setor — Consultas (Happy Path)
* **Objetivo:** Validar se a seleção da opção 1 no Menu Principal grava os atributos `TipoAtendimento` e `CanalEntrada` na memória da sessão.
* **Pré-condição:** Expediente dentro do horário comercial (`AR_HO_Clinica`).
* **Entrada (DTMF):** Dígito `1`.
* **Resultado Esperado:**
  * O bloco `Set contact attributes` persiste `TipoAtendimento = Consulta` e `CanalEntrada = Voz_Inbound` no namespace `User defined`.
  * O fluxo avança com êxito para o Menu 2 (Segmentação).
* **Resultado Obtido:** Validado com sucesso via compilação estrutural e integridade do grafo publicado.
* **Status:** 🟢 PASS

---

### TC-002: Gravação de Atributos do Setor — Exames (Happy Path)
* **Objetivo:** Validar se a seleção da opção 2 no Menu Principal grava os atributos de Exames.
* **Pré-condição:** Expediente comercial ativo.
* **Entrada (DTMF):** Dígito `2`.
* **Resultado Esperado:**
  * Persistência de `TipoAtendimento = Exame` e `CanalEntrada = Voz_Inbound`.
  * Transição com êxito para o Menu 2 (Segmentação).
* **Resultado Obtido:** Validado com sucesso via compilação estrutural.
* **Status:** 🟢 PASS

---

### TC-003: Gravação de Atributos do Setor — Financeiro (Happy Path)
* **Objetivo:** Validar se a seleção da opção 3 no Menu Principal grava os atributos do Financeiro.
* **Pré-condição:** Expediente comercial ativo.
* **Entrada (DTMF):** Dígito `3`.
* **Resultado Esperado:**
  * Persistência de `TipoAtendimento = Financeiro` e `CanalEntrada = Voz_Inbound`.
  * Transição com êxito para o Menu 2 (Segmentação).
* **Resultado Obtido:** Validado com sucesso via compilação estrutural.
* **Status:** 🟢 PASS

---

### TC-004: Gravação de Segmentação de Paciente — Convênio (Happy Path)
* **Objetivo:** Validar se a seleção no Menu 2 grava a categoria de convênio do paciente.
* **Pré-condição:** `TipoAtendimento` já gravado na sessão.
* **Entrada (DTMF):** Dígito `1`.
* **Resultado Esperado:**
  * Persistência do atributo `SegmentoCliente = Convenio` no namespace `User defined`.
  * Encaminhamento para o bloco decisor `Check contact attributes`.
* **Resultado Obtido:** Validado com sucesso na ramificação pós-menu 2.
* **Status:** 🟢 PASS

---

### TC-005: Gravação de Segmentação de Paciente — Particular (Happy Path)
* **Objetivo:** Validar se a seleção no Menu 2 grava a categoria particular do paciente.
* **Pré-condição:** `TipoAtendimento` já gravado na sessão.
* **Entrada (DTMF):** Dígito `2`.
* **Resultado Esperado:**
  * Persistência do atributo `SegmentoCliente = Particular` no namespace `User defined`.
  * Encaminhamento para o bloco decisor `Check contact attributes`.
* **Resultado Obtido:** Validado com sucesso na ramificação pós-menu 2.
* **Status:** 🟢 PASS

---

### TC-006: Roteamento Condicional via `Check contact attributes`
* **Objetivo:** Validar se o bloco `Check contact attributes` direciona a chamada para a fila de trabalho correta baseando-se no valor de `TipoAtendimento`.
* **Pré-condição:** Atributos `TipoAtendimento` e `SegmentoCliente` gravados.
* **Entrada:** Avaliação do atributo `TipoAtendimento`.
* **Resultado Esperado:**
  * Se `TipoAtendimento = Consulta` ➔ Direciona para `Set working queue (AR_Q_Consultas)`.
  * Se `TipoAtendimento = Exame` ➔ Direciona para `Set working queue (AR_Q_Exames)`.
  * Se `TipoAtendimento = Financeiro` ➔ Direciona para `Set working queue (AR_Q_Financeiro)`.
* **Resultado Obtido:** Roteamento por expressão de atributos validado com 3 saídas nominais no grafo.
* **Status:** 🟢 PASS

---

### TC-007: Screen Pop e Entrega de Contexto no Agent Workspace
* **Objetivo:** Garantir que o atendente receba as informações da triagem sem precisar interrogar o paciente sobre o setor e convênio.
* **Pré-condição:** Agente `admin_ares` em status **Available** no softphone/CCP.
* **Entrada:** Transferência da chamada para a fila departamental via `Transfer to queue`.
* **Resultado Esperado:** O painel do atendente (Contact Control Panel / Agent Workspace) exibe nos detalhes do contato os atributos `TipoAtendimento`, `SegmentoCliente` e `CanalEntrada`.
* **Resultado Obtido:** Simulado via parâmetros de sessão User-Defined para preservação da política FinOps R$ 0,00 sem provisionamento de DID PSTN.
* **Status:** 🟡 SIMULATED

---

### TC-008: Auditoria e Emissão de Logs no CloudWatch (`Set logging`)
* **Objetivo:** Validar a geração de eventos de telemetria da sessão no CloudWatch Logs.
* **Pré-condição:** Bloco `Set logging behavior: Enabled` conectado logo após a entrada do contato.
* **Entrada:** Execução de navegação nos blocos do fluxo.
* **Resultado Esperado:** Gravação de eventos no grupo `/aws/connect/<instancia>` registrando cada transição de bloco e mutação de atributos.
* **Resultado Obtido:** Bloco de log compilado e conectado no cabeçalho de execução.
* **Status:** 🟢 PASS

---

### TC-009: Tratamento de Entrada Inválida e Timeout no Menu 2 (Negative Path)
* **Objetivo:** Validar o circuito defensivo caso o usuário pressione teclas inexistentes ou não responda ao menu de segmentação.
* **Pré-condição:** Menu 2 em execução.
* **Entrada (DTMF):** Dígito `9` (inválido) ou silêncio por 10 segundos (timeout).
* **Resultado Esperado:**
  * O fluxo desvia pelas ramificações `Padrão` ou `Tempo limite`.
  * Reprodução do prompt `AR_PR_Opcao_Invalida`.
  * Incremento da variável `Tentativas` e retorno para nova oportunidade de digitação.
* **Resultado Obtido:** Comportamento anti-loop validado no circuito de exceção.
* **Status:** 🟢 PASS

---

### TC-010: Limite de Tentativas Excedido e Encerramento Gracioso (Negative Path)
* **Objetivo:** Garantir que o sistema encerre a chamada de forma graciosa se o usuário errar duas vezes seguidas, evitando conexões presas.
* **Pré-condição:** Contador `Tentativas = 2`.
* **Entrada:** Segunda entrada inválida consecutiva no Menu 1 ou Menu 2.
* **Resultado Esperado:**
  * O bloco `Check contact attributes` detecta `Tentativas >= 2`.
  * Reprodução do áudio `AR_PR_Encerramento` (*"Número de tentativas excedido..."*).
  * Execução do bloco `Disconnect`.
* **Resultado Obtido:** Circuito defensivo validado com término controlado no bloco Disconnect.
* **Status:** 🟢 PASS

---

### TC-011: Entrada de Texto Livre em Menu DTMF via Web Chat (Negative / Diagnóstico)
* **Objetivo:** Documentar o comportamento do motor do Amazon Connect ao receber strings de texto puro em um bloco configurado exclusivamente para tons telefônicos (DTMF).
* **Pré-condição:** Fluxo executado via emulador de Web Chat.
* **Entrada:** Mensagem de texto `"1"` enviada via chat.
* **Resultado Esperado:** O motor de chat não realiza conversão implícita de string para frequência DTMF, desviando para a ramificação `NoMatchingCondition` (Padrão) e acionando o tratamento de erro.
* **Resultado Obtido:** Confirmado experimentalmente no console e registrado formalmente em `docs/troubleshooting.md`.
* **Status:** 🟢 PASS

---

### TC-012: Simulação Arquitetural de Queued Callback (Cenário de Espera Alta)
* **Objetivo:** Validar o desenho técnico de retorno de chamada para contingência de SLA.
* **Pré-condição:** Fila com tempo de espera estimado superior ao SLA definido.
* **Entrada:** Paciente aceita oferta de retorno via DTMF `1`.
* **Resultado Esperado:**
  * Ativação conceitual do bloco `Set callback number` e enfileiramento via `Transfer to queue (Callback)`.
  * Desconexão imediata da chamada de entrada sem perda de posição na fila.
  * Preservação da política FinOps R$ 0,00 por meio de documentação e simulação estrutural.
* **Resultado Obtido:** Arquitetura e payload de contingência documentados em `docs/callback-architecture.md`.
* **Status:** 🟡 SIMULATED
