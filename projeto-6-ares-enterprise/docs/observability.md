# 📊 Arquitetura de Observabilidade & Amazon CloudWatch
**Ecossistema Ares Saúde | Monitorização Proativa**

---

## 📡 Métricas Críticas Monitorizadas no Amazon Connect

| Métrica CloudWatch | Namespace | Unidade | Limiar de Alarme | Ação Recomendada |
| :--- | :--- | :--- | :--- | :--- |
| `ContactFlowErrors` | `AWS/Connect` | Count | `> 3 em 5 min` | Notificar equipa de engenharia de fluxos para inspeção de logs. |
| `MissedCalls` | `AWS/Connect` | Count | `> 5 em 15 min` | Verificar status dos agentes e integridade do WebRTC/CCP. |
| `QueueCapacityExceededErrors` | `AWS/Connect` | Count | `> 1 em 5 min` | Avaliar transbordo ou acionamento de operadores de reserva. |
| `CallsBreachingConcurrencyQuota` | `AWS/Connect` | Count | `> 0 em 1 min` | Solicitar expansão emergencial de quotas de concorrência à AWS. |

---

## 🔍 Estratégia de Diagnóstico via CloudWatch Logs
* **Contact Flow Logs:** Habilitados centralmente em todos os fluxos através do bloco de configuração de log.
* **Campos Auditados:** `ContactId`, `Timestamp`, `DisconnectReason`, `Parameters` e saídas de módulos externos.
* **Segurança de Dados:** Atributos contendo informações confidenciais não devem ser persistidos em logs abertos, cumprindo os requisitos de privacidade e governança hospitalar.
