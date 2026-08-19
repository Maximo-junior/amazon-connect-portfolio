# 🧪 Plano e Matriz de Testes — Projeto 2 (Expansão do Atendimento e Filas Reais)

## 📌 Estratégia de Testes
Em conformidade com a política de governança **FinOps R$ 0,00**, a homologação do ecossistema de roteamento da Clínica Ares (composto pelo Contact Flow `AR_CF_Triagem_Inicial`, horário `AR_HO_Clinica`, filas reais `AR_Q_Consultas`, `AR_Q_Exames`, `AR_Q_Financeiro`, Routing Profile `AR_RP_Atendimento` e agente `admin_ares`) foi conduzida por meio de:
1. **Validação Estática e de Compilação:** Inspeção estrutural de grafos e publicação no Amazon Connect Flow Designer sem pontas soltas.
2. **Homologação Operacional WebRTC:** Teste de ciclo de vida e disponibilidade de agente via Contact Control Panel (CCP) / Agent Workspace no navegador com custo isento.
3. **Simulação de Tráfego Telefônico (PSTN/DID):** Mapeamento do comportamento de rede pública e enfileiramento documentados como simulados para evitar tarifação de números públicos e minutos tarifados.

---

## 🧪 Casos de Teste (Test Cases)

### TC-001: Validação de Expediente Comercial Ativo (In Hours Path)
- **Objetivo:** Garantir que contatos recebidos de segunda a sexta-feira, das 08h às 18h, prossigam para a triagem.
- **Pré-condição:** Tabela de horário `AR_HO_Clinica` associada ao bloco `Verificar horário de funcionamento`.
- **Entrada:** Contato gerado durante a janela de atendimento.
- **Resultado Esperado:** O bloco `Verificar horário de funcionamento` avalia a condição como verdadeira (`Dentro do horário`), encaminha para a reprodução da saudação de boas-vindas (`AR_PR_Saudacao`) e apresenta o menu de opções principal.
- **Status:** 🟢 PASS (Validado via análise de fluxo e compilação no Flow Designer).

### TC-002: Bloqueio de Atendimento Fora do Expediente (Out of Hours Path)
- **Objetivo:** Garantir que contatos fora do horário comercial não entrem em filas humanas e recebam aviso contextual.
- **Pré-condição:** Horário do contato fora da janela de Seg-Sex das 08h às 18h (`AR_HO_Clinica`).
- **Entrada:** Contato gerado aos fins de semana ou após as 18h.
- **Resultado Esperado:** O bloco `Verificar horário de funcionamento` aciona a ramificação `Fora do horário`, reproduz a mensagem *"Nosso horário de atendimento é de segunda a sexta-feira, das 8h às 18h. No momento estamos fechados. Obrigado por ligar para a Clínica Ares."* e encerra a conexão no bloco `Desconectar`.
- **Status:** 🟢 PASS (Validado via análise de fluxo e compilação no Flow Designer).

### TC-003: Roteamento Real para a Fila de Consultas (Happy Path)
- **Objetivo:** Validar o direcionamento da Opção 1 para a fila real `AR_Q_Consultas` e entrega ao atendente.
- **Pré-condição:** Expediente aberto, agente `admin_ares` com status **Available** no CCP vinculado ao perfil `AR_RP_Atendimento`.
- **Entrada (DTMF):** Tecla `1` pressionada durante a execução do menu.
- **Resultado Esperado:**
  1. O bloco `Definir fila de trabalho` carrega `AR_Q_Consultas` no atributo de sessão.
  2. O bloco `Transferir para fila` inicia o enfileiramento real.
  3. O CCP do agente recebe o alerta sonoro e visual de chamada entrante.
- **Resultado Obtido:** Lógica de fluxo compilada com sucesso e agente colocado em prontidão **Available** no Agent Workspace (tráfego PSTN simulado por FinOps).
- **Status:** 🟡 SIMULATED

### TC-004: Roteamento Real para a Fila de Exames (Happy Path)
- **Objetivo:** Validar o direcionamento da Opção 2 para a fila real `AR_Q_Exames` e entrega ao atendente.
- **Pré-condição:** Expediente aberto, agente `admin_ares` com status **Available** no CCP vinculado ao perfil `AR_RP_Atendimento`.
- **Entrada (DTMF):** Tecla `2` pressionada durante a execução do menu.
- **Resultado Esperado:**
  1. O bloco `Definir fila de trabalho` carrega `AR_Q_Exames` no atributo de sessão.
  2. O bloco `Transferir para fila` inicia o enfileiramento real da chamada.
- **Resultado Obtido:** Lógica de fluxo compilada com sucesso e agente em prontidão (tráfego PSTN simulado por FinOps).
- **Status:** 🟡 SIMULATED

### TC-005: Roteamento Real para a Fila do Setor Financeiro (Happy Path)
- **Objetivo:** Validar o direcionamento da Opção 3 para a fila real `AR_Q_Financeiro` e entrega ao atendente.
- **Pré-condição:** Expediente aberto, agente `admin_ares` com status **Available** no CCP vinculado ao perfil `AR_RP_Atendimento`.
- **Entrada (DTMF):** Tecla `3` pressionada durante a execução do menu.
- **Resultado Esperado:**
  1. O bloco `Definir fila de trabalho` carrega `AR_Q_Financeiro` no atributo de sessão.
  2. O bloco `Transferir para fila` inicia o enfileiramento real da chamada.
- **Resultado Obtido:** Lógica de fluxo compilada com sucesso e agente em prontidão (tráfego PSTN simulado por FinOps).
- **Status:** 🟡 SIMULATED

### TC-006: Tratamento de Capacidade Esgotada ou Falha de Fila (Negative/Defensive Path)
- **Objetivo:** Validar o comportamento do fluxo caso a fila atinja o limite ou ocorra falha de roteamento.
- **Pré-condição:** Fila sem capacidade operacional ou erro interno no bloco de transferência.
- **Entrada:** Contato encaminhado para o bloco `Transferir para fila`.
- **Resultado Esperado:** As saídas `Sem espaço` (*At capacity*) e `Erro` (*Error*) desviam a chamada com segurança diretamente para o bloco `Desconectar`, evitando retenção indevida ou linha muda.
- **Status:** 🟢 PASS (Tratamento defensivo compilado e validado no Flow Designer).

### TC-007: Ciclo de Vida do Agente no Contact Control Panel (CCP)
- **Objetivo:** Validar a autenticação, permissões e alternância de status operacional do operador.
- **Pré-condição:** Usuário `admin_ares` provisionado com Security Profile `Admin` e associado ao Routing Profile `AR_RP_Atendimento`.
- **Entrada:** Acesso ao Agent Workspace e alteração do seletor de presença de **Offline** para **Available**.
- **Resultado Esperado:** O painel inicializa a conexão WebRTC de áudio (Softphone) e exibe o indicador verde **Available**, sinalizando prontidão para receber contatos.
- **Status:** 🟢 PASS (Validado visualmente e operacionalmente no console).
