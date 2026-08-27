# 📞 Arquitetura de Referência: Queued Callback (Simulado)

## 📌 Visão Geral
O **Queued Callback** (Retorno de Chamada em Fila) é um padrão de Customer Experience (CX) no Amazon Connect que impede que o cliente fique retido na linha durante períodos de alta demanda.

Em conformidade com a governança **FinOps R$ 0,00**, esta funcionalidade é documentada no nível de arquitetura de produção (**🟡 SIMULADO**), pois sua execução real requer linha externa (PSTN/DID) e tarifação de minutos de discagem ativa (*Outbound*).

---

## 🏛️ Fluxo Lógico de Produção

```
[ Cliente na Fila de Espera ]
         │
         ▼
[ Condição: Tempo estimado de espera > SLA ]
         │
         ▼
[ Bloco: Get customer input ] ──► "Deseja que retornemos a ligação quando for sua vez? Digite 1."
         │ (1 - Sim)
         ▼
[ Bloco: Set callback number ] ──► Armazena o número do cliente (System Attribute: Customer Number)
         │
         ▼
[ Bloco: Transfer to queue (Callback) ] ──► O Connect reserva a posição do cliente na fila
         │
         ▼
[ Desconexão da Chamada Inbound ] (Cliente desliga sem perder a posição)
         │
         ▼ (Quando o agente fica Available e chega a vez do cliente)
[ Amazon Connect disca para o Agente ] ──► [ Agente atende ] ──► [ Connect disca para o Cliente ] ──► [ Conexão Estabelecida ]
