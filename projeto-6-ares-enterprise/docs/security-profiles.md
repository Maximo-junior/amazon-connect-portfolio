# 🔐 Matriz de Perfis de Segurança e Governança RBAC
**Projeto 6: Ares Enterprise | Complexo Hospitalar Ares**

---

## 🎯 Objetivo Arquitetural
Estabelecer o controlo de acesso baseado em funções (*Role-Based Access Control* - RBAC) através de perfis nativos (*Security Profiles*) no Amazon Connect, implementando o princípio do menor privilégio (*Least Privilege*) para cumprir normas regulamentares e de conformidade em saúde (como LGPD e HIPAA).

---

## 🛡️ Princípio do Menor Privilégio (*Least Privilege*)
Nenhum utilizador ou operador no ecossistema Ares possui permissões globais de administração. O acesso é estritamente limitado às ferramentas indispensáveis para a execução da respetiva função operacional ou técnica. A ausência de permissão explícita configura um **Implicit Deny** pelo motor de autorização do Amazon Connect.

---

## 👥 Perfis Corporativos Implementados

### 1. `AR_SP_Atendente`
* **Função Organizacional:** Operador de teleatendimento hospitalar (linha da frente).
* **Descrição Técnica:** Acesso exclusivo ao painel de atendimento para receção, transferência e encerramento de contactos.
* **Permissões Concedidas:**
  * **Contact Control Panel (CCP):** `Access Contact Control Panel` habilitado.
* **Restrições Mandatórias:**
  * Sem acesso a Contact Flows (0/32 caixas marcadas em Channels and Flows).
  * Sem acesso a relatórios e métricas em tempo real ou históricas.
  * Sem acesso a gestão de filas, utilizadores ou números telefónicos.

---

### 2. `AR_SP_Supervisor`
* **Função Organizacional:** Gestão e monitorização operacional de equipas e filas.
* **Descrição Técnica:** Acompanhamento do tráfego hospitalar em tempo real e análise de desempenho da operação.
* **Permissões Concedidas:**
  * **Analytics and Optimization / Metrics:** `Real-time metrics` (View) e `Historical metrics` (View).
  * **Contact Control Panel (CCP):** `Access Contact Control Panel` (para apoio operacional e testes assistidos).
  * **Users:** `Users` (View).
* **Restrições Mandatórias:**
  * Sem permissão de edição (*Edit*) ou publicação (*Publish*) em fluxos de contacto.
  * Sem permissão de alteração estrutural de filas ou regras de roteamento.

---

### 3. `AR_SP_Admin_Fluxos`
* **Função Organizacional:** Engenharia de Contact Center e infraestrutura de voz (CCaaS Engineering).
* **Descrição Técnica:** Manutenção, desenvolvimento, teste e manobra de contingência dos fluxos de atendimento.
* **Permissões Concedidas:**
  * **Channels and Flows:**
    * `Flows`: View, Edit, Create, Publish.
    * `Flow modules`: View, Edit, Create, Publish.
    * `Prompts`: View, Create, Edit.
  * **Routing:** `Queues` (View) e `Routing profiles` (View).
  * **Contact Control Panel (CCP):** `Access Contact Control Panel` (para testes via WebRTC).
* **Restrições Mandatórias (FinOps & Segurança):**
  * `Phone numbers`: Desmarcado (proibição de reivindicar novos números pagos sem alinhamento FinOps).
  * `Channels and Flows`: `Remove` desmarcado (proteção contra exclusão acidental de recursos).

---

### 4. `AR_SP_Auditoria_Compliance`
* **Função Organizacional:** Auditoria médica, conformidade jurídica e segurança da informação.
* **Descrição Técnica:** Acesso exclusivo de somente leitura para verificação de relatórios históricos, parâmetros de atendimento e trilhas de auditoria.
* **Permissões Concedidas:**
  * **Analytics and Optimization:** `Historical metrics` (View), `Saved reports` (View) e `Contact search` (View).
  * **Channels and Flows:** `Flows` (View) e `Flow modules` (View).
  * **Routing:** `Queues` (View), `Routing profiles` (View) e `Hours of operation` (View).
  * **Users:** `Users` (View) e `Security profiles` (View).
* **Restrições Mandatórias:**
  * Perfil estritamente Read-Only (0 permissões de Create, Edit, Publish ou Remove).
  * Sem acesso ao CCP (0/11 caixas no Contact Control Panel).

---

## 📊 Matriz Comparativa de Permissões

| Categoria / Recurso | `AR_SP_Atendente` | `AR_SP_Supervisor` | `AR_SP_Admin_Fluxos` | `AR_SP_Auditoria_Compliance` |
| :--- | :---: | :---: | :---: | :---: |
| **Painel CCP (Atendimento)** | 🟢 Acesso | 🟢 Acesso | 🟢 Acesso | 🔴 Negado |
| **Flows (View)** | 🔴 Negado | 🔴 Negado | 🟢 Permitido | 🟢 Permitido |
| **Flows (Edit / Publish)** | 🔴 Negado | 🔴 Negado | 🟢 Permitido | 🔴 Negado |
| **Métricas em Tempo Real** | 🔴 Negado | 🟢 Permitido | 🔴 Opcional | 🔴 Negado |
| **Métricas Históricas** | 🔴 Negado | 🟢 Permitido | 🔴 Opcional | 🟢 Permitido |
| **Gestão de Utilizadores** | 🔴 Negado | 🟢 View | 🔴 Negado | 🟢 View |
| **Reivindicação de DIDs** | 🔴 Negado | 🔴 Negado | 🔴 Negado (FinOps) | 🔴 Negado |
