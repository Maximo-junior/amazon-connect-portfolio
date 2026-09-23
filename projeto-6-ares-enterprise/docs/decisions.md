# 🏛️ Architecture Decision Records (ADR)
**Projeto 6: Ares Enterprise | Complexo Hospitalar Ares**

---

## ADR-010: Segregação Granular de Perfis de Segurança (Least Privilege)
* **Status:** Aprovado
* **Contexto:** A operação do Hospital Ares necessita de segregação de funções para operadores, supervisores, engenharia de fluxos e auditoria, evitando alterações indevidas em produção e cumprindo normas de compliance.
* **Decisão:** Criar quatro Security Profiles nativos (`AR_SP_Atendente`, `AR_SP_Supervisor`, `AR_SP_Admin_Fluxos`, `AR_SP_Auditoria_Compliance`) aplicando o princípio do menor privilégio. Operadores acedem estritamente ao CCP, enquanto permissões de publicação de fluxos ficam restritas à engenharia.
* **Consequências Positivas:** Eliminação de riscos operacionais por alterações acidentais e conformidade com requisitos de auditoria.
* **Trade-offs:** Necessidade de gestão contínua de atribuição de utilizadores a perfis específicos.

---

## ADR-011: Fluxo de Contingência Degradada (Disaster Recovery Flow)
* **Status:** Aprovado
* **Contexto:** Em cenários de falha massiva de postos de trabalho, queda de agentes ou indisponibilidade de backend, o paciente não pode deparar-se com chamadas mudas ou encerramentos abruptos sem aviso.
* **Decisão:** Construir o fluxo dedicado `AR_CF_Contingencia_DR`, parametrizado com mensagem institucional de contingência, habilitação de logs e desconexão controlada, pronto para assumir o número de entrada principal em menos de 5 minutos (RTO <= 5 min).
* **Consequências Positivas:** Preservação da experiência do paciente e garantia de continuidade operacional em modo seguro.
* **Trade-offs:** Atendimento humano fica temporariamente suspenso durante a ativação do protocolo.

---

## ADR-012: Observabilidade Centralizada sem Custos Extras (FinOps)
* **Status:** Aprovado
* **Contexto:** É necessário monitorizar falhas de execução de fluxos e capacidade de filas sem estourar o orçamento do laboratório.
* **Decisão:** Mapear os limiares de alarmes no CloudWatch baseados nas métricas nativas do Connect (`ContactFlowErrors`, `QueueCapacityExceededErrors`), retendo logs operacionais apenas pelo período auditável.
* **Consequências Positivas:** Visibilidade operacional completa mantendo o custo real auditado em R$ 0,00.
