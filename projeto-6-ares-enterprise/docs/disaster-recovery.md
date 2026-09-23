# 🚨 Plano de Continuidade e Disaster Recovery (DR)
**Ecossistema Ares Saúde | Governança Hospitalar**

---

## 🎯 Objetivos de Continuidade (SLAs de Engenharia)
* **RTO (Recovery Time Objective):** `<= 5 minutos`. Tempo limite para transferir o tráfego do canal principal para o modo degradado de contingência.
* **RPO (Recovery Point Objective):** `<= 0 minutos` para metadados de roteamento (infraestrutura declarativa versionada via Flow-as-Code no GitHub).

---

## 🏢 Cenários de Ativação do Protocolo de Contingência
1. **Falha Sistémica nos Postos dos Agentes:** Queda de rede física, energia ou indisponibilidade total dos postos de atendimento humano.
2. **Indisponibilidade de Integração Crítica:** Falhas consecutivas no backend ou APIs hospitalares sem recuperação via retry.
3. **Crise Sanitária ou Evento de Massa:** Sobrecarga severa de filas ultrapassando a capacidade operacional, exigindo comunicação institucional imediata.

---

## 🛠️ Runbook Operacional: Procedimento de Virada para DR

### Procedimento de Acionamento (Failover):
1. O Tech Lead / Engenheiro On-Call acede à consola administrativa do Amazon Connect com o perfil `AR_SP_Admin_Fluxos`.
2. Aceda ao menu **Routing** ➔ **Phone numbers**.
3. Selecione o número principal de entrada do Hospital Ares.
4. No campo **Contact flow / IVR**, altere o apontamento de `AR_CF_Hospital_Principal` para:
   👉 **`AR_CF_Contingencia_DR`**
5. Clique em **Save**.
6. **Validação:** Ligue através do WebRTC / Test Audio e confirme a reprodução da mensagem de contingência seguida de desconexão graciosa.
*Tempo médio de execução:* ~90 segundos.

### Procedimento de Retorno (Failback):
1. Verifique a estabilização comprovada dos sistemas operacionais e a disponibilidade dos agentes nas filas (`AR_Q_*`).
2. Aceda a **Routing** ➔ **Phone numbers**.
3. Reaponte o número para o fluxo de produção principal: `AR_CF_Hospital_Principal`.
4. Clique em **Save** e valide a execução da triagem regular.
