# 🧪 Matriz de Testes — Projeto 4: Modularização Hospitalar
**Ecossistema Ares Saúde | Complexo: Hospital Ares**

Esta matriz cobre a validação estrutural, execução modular, regras de horário e limites defensivos.

| ID | Cenário / Objetivo | Pré-condição | Entrada | Comportamento Esperado | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-001** | Inicialização Corporativa Modular | Módulo `AR_MD_Inicializacao` publicado | Início da chamada | Ativar logs no CloudWatch, definir voz Vitória Neural e retornar ao orquestrador | 🟢 PASS |
| **TC-002** | Roteamento em Horário Comercial | Chamada executada de Seg a Sex (08:00 - 18:00) | Entrada de chamada | `AR_MD_Verifica_Horario` valida horário aberto e avança para a saudação | 🟢 PASS |
| **TC-003** | Roteamento Fora de Horário | Chamada fora do expediente de `AR_HO_Clinica` | Entrada de chamada | Reproduzir áudio de encerramento institucional e desconectar via módulo | 🟢 PASS |
| **TC-004** | Seleção Menu: Opção 1 (Consultas) | Chamada no menu principal | DTMF `1` | Definir fila `AR_Q_Consultas` e transferir para atendimento | 🟢 PASS |
| **TC-005** | Seleção Menu: Opção 2 (Exames) | Chamada no menu principal | DTMF `2` | Definir fila `AR_Q_Exames` e transferir para atendimento | 🟢 PASS |
| **TC-006** | Seleção Menu: Opção 3 (Financeiro) | Chamada no menu principal | DTMF `3` | Definir fila `AR_Q_Financeiro` e transferir para atendimento | 🟢 PASS |
| **TC-007** | Tratamento de Opção Inválida (1ª Tentativa) | Chamada no menu principal | DTMF `9` | Invocar `AR_MD_Tratamento_Erros`, tocar prompt de erro, definir `Tentativas=1` e retornar ao menu | 🟢 PASS |
| **TC-008** | Tratamento de Timeout (1ª Tentativa) | Chamada no menu principal | Sem dígito (5s) | Invocar `AR_MD_Tratamento_Erros`, alertar timeout e reexecutar menu | 🟢 PASS |
| **TC-009** | Limite Excedido de Tentativas | `Tentativas = 1` no contato | DTMF inválido ou Timeout | Invocar `AR_MD_Tratamento_Erros`, avaliar `Tentativas >= 2`, tocar prompt de limite e desconectar | 🟢 PASS |
| **TC-010** | Degradação Graciosa em Falha Geral | Simulação de indisponibilidade em filas | Erro de infraestrutura | Desvio determinístico para o nó `Desconectar` sem interrupção abrupta da sessão | 🟢 PASS |
