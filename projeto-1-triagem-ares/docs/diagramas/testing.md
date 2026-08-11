# 🧪 Plano e Matriz de Testes — Projeto 1 (Clínica Ares)

## 📌 Estratégia de Testes
Em conformidade com a política de governança **FinOps R$ 0,00**, a homologação do Contact Flow `AR_CF_Triagem_Inicial` foi conduzida por meio de **Testes de Mesa (Dry Run / Static Flow Walkthrough)** e validação estática no Amazon Connect Flow Designer, evitando a necessidade de tarifação de linhas telefônicas (PSTN/DID).

## 🧪 Casos de Teste (Test Cases)

### TC-001: Navegação para Consultas (Happy Path)
- **Objetivo:** Validar o direcionamento do cliente para a opção 1.
- **Pré-condição:** Fluxo publicado e ativo no Amazon Connect.
- **Entrada (DTMF):** Tecla `1` pressionada durante a execução do menu.
- **Resultado Esperado:** O sistema reconhece a opção 1, reproduz a mensagem *"Você selecionou o setor de Consultas. Encaminhando seu atendimento."* e redireciona a chamada para o bloco `Desconectar`.
- **Status:** 🟢 PASS (Validado via análise de grafos no Flow Designer).

### TC-002: Navegação para Exames (Happy Path)
- **Objetivo:** Validar o direcionamento do cliente para a opção 2.
- **Pré-condição:** Fluxo publicado e ativo no Amazon Connect.
- **Entrada (DTMF):** Tecla `2` pressionada durante a execução do menu.
- **Resultado Esperado:** O sistema reconhece a opção 2, reproduz a mensagem *"Você selecionou o setor de Exames. Encaminhando seu atendimento."* e redireciona a chamada para o bloco `Desconectar`.
- **Status:** 🟢 PASS (Validado via análise de grafos no Flow Designer).

### TC-003: Navegação para Financeiro (Happy Path)
- **Objetivo:** Validar o direcionamento do cliente para a opção 3.
- **Pré-condição:** Fluxo publicado e ativo no Amazon Connect.
- **Entrada (DTMF):** Tecla `3` pressionada durante a execução do menu.
- **Resultado Esperado:** O sistema reconhece a opção 3, reproduz a mensagem *"Você selecionou o setor Financeiro. Encaminhando seu atendimento."* e redireciona a chamada para o bloco `Desconectar`.
- **Status:** 🟢 PASS (Validado via análise de grafos no Flow Designer).

### TC-004: Entrada Inválida (First Retry)
- **Objetivo:** Validar o tratamento para teclas inválidas digitadas no teclado.
- **Pré-condição:** Atributo de sessão `Tentativas` inicializado em `0`.
- **Entrada (DTMF):** Tecla `9` (opção inexistente no menu).
- **Resultado Esperado:** O sistema identifica a entrada inválida via ramificação `Padrão`, reproduz o áudio *"Opção inválida ou tempo de resposta esgotado."*, incrementa o atributo para `Tentativas = 1` e retorna a linha de conexão para a entrada do menu principal.
- **Status:** 🟢 PASS (Validado via análise de grafos no Flow Designer).

### TC-005: Ausência de Entrada (Timeout)
- **Objetivo:** Validar o tratamento para silêncio prolongado do usuário.
- **Pré-condição:** Atributo de sessão `Tentativas` inicializado em `0`.
- **Entrada:** Silêncio / Nenhuma tecla pressionada por 5 segundos.
- **Resultado Esperado:** O sistema aciona a ramificação `Tempo limite`, reproduz o áudio *"Opção inválida ou tempo de resposta esgotado."*, incrementa o atributo para `Tentativas = 1` e retorna a linha de conexão para a entrada do menu principal.
- **Status:** 🟢 PASS (Validado via análise de grafos no Flow Designer).

### TC-006: Limite de Tentativas Excedido (Max Retries)
- **Objetivo:** Validar o encerramento gracioso ao atingir o limite de falhas.
- **Pré-condição:** Atributo de sessão `Tentativas` já em `1`.
- **Entrada (DTMF):** Tecla `8` (segunda entrada inválida consecutiva).
- **Resultado Esperado:** O atributo é atualizado para `Tentativas = 2`. O bloco `Verificar atributos do contato` avalia a condição `Tentativas < 2` como FALSA (`Sem correspondência`), encaminha para a mensagem *"Número de tentativas excedido. O atendimento será encerrado. Obrigado."* e finaliza no bloco `Desconectar`.
- **Status:** 🟢 PASS (Validado via análise de grafos no Flow Designer).
