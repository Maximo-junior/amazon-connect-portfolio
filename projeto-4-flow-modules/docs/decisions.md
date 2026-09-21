```markdown
# 📋 Architecture Decision Records (ADRs) — Projeto 4
**Ecossistema Ares Saúde | Complexo: Hospital Ares**

---

## ADR-005: Adoção de Flow Modules para Eliminação de Código Repetitivo (DRY)
* **Status:** Aprovado
* **Data:** 2026-09-21
* **Contexto:** Com a expansão da Clínica Ares para um Complexo Hospitalar, múltiplos fluxos de atendimento seriam criados (Recepção, Urgência, Consultas). Cada fluxo demandava replicação manual de cabeçalhos de telemetria, definição de voz e blocos de horário.
* **Decisão:** Extrair componentes transversais para submódulos independentes utilizando *Flow Modules* (`contactFlowModule`).
* **Consequências:**
  * *Positivas:* Manutenção centralizada. Alterações de horário ou voz são aplicadas uma única vez e herdadas por todos os fluxos.
  * *Mitigações:* Necessidade de rigor na definição de contratos de saída com blocos `Retornar` (*Exit flow module*).

---

## ADR-006: Centralização de Tratamento de Erros e Controle Anti-Loop
* **Status:** Aprovado
* **Data:** 2026-09-21
* **Contexto:** Menus de autoatendimento necessitam de proteção contra loops infinitos causados por entradas repetidamente inválidas ou timeouts. Implementar contadores manuais em cada ponto de decisão gera inconsistência na experiência do paciente.
* **Decisão:** Implementar o módulo corporativo `AR_MD_Tratamento_Erros` responsável por auditar, computar o atributo de contato `Tentativas` e decidir deterministamente entre devolver o controle ao menu ou encerrar o contato.
* **Consequências:**
  * *Positivas:* Política uniforme de experiência do cliente (CX) e segurança operacional em toda a instituição.
  * *Mitigações:* O fluxo orquestrador deve mapear explicitamente o retorno do módulo para o ponto de reentrada do menu.

---

## ADR-007: Isolamento de Artefatos no Repositório (Flow-as-Code)
* **Status:** Aprovado
* **Data:** 2026-09-21
* **Contexto:** Módulos e fluxos possuem tipos de recursos e esquemas de compilação diferentes no Amazon Connect (`contactFlowModule` vs. `contactFlow`). Misturá-los na mesma pasta dificulta esteiras de CI/CD automatizadas.
* **Decisão:** Adotar a estrutura estrita de diretórios `src/contact-flows/` e `src/flow-modules/`.
* **Consequências:**
  * *Positivas:* Compatibilidade com pipelines de implantação via AWS CLI e CDK, garantindo que dependências modulares sejam publicadas antes dos fluxos consumidores.
