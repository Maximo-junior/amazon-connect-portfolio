# 🧪 Matriz de Testes Operacionais e Continuidade (DR)
**Projeto 6: Ares Enterprise**

| ID | Cenário de Teste | Pré-condição | Entrada / Ação | Resultado Esperado | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-021** | Validação de Acesso do Atendente | Perfil `AR_SP_Atendente` atribuído | Iniciar sessão no Amazon Connect | Acesso restrito ao painel CCP; menus de edição de fluxos inacessíveis. | 🟢 PASS |
| **TC-022** | Validação de Permissão de Fluxos | Perfil `AR_SP_Admin_Fluxos` ativo | Aceder a Routing ➔ Contact Flows | Permissão total para editar, criar e publicar fluxos e módulos. | 🟢 PASS |
| **TC-023** | Execução do Fluxo de DR | `AR_CF_Contingencia_DR` publicado | Chamada simulada para o fluxo | Reprodução da mensagem de contingência hospitalar e encerramento limpo. | 🟢 PASS |
| **TC-024** | Simulação de Failover de Emergência | Número apontado para URA principal | Alterar apontamento para fluxo de DR | Tráfego comutado em menos de 5 minutos sem erro sistémico. | 🟢 PASS |
| **TC-025** | Rastreabilidade de Logs de DR | `Set logging behavior` habilitado | Disparo de chamada no fluxo de DR | Registo do evento gerado no Amazon CloudWatch Logs com ContactId. | 🟢 PASS |
