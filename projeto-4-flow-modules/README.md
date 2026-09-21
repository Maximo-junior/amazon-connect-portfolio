# 🏥 Projeto 4 — Modularização com Flow Modules | Hospital Ares

## 📋 Visão Geral
Este projeto contempla a evolução da arquitetura do ecossistema **Ares Saúde** através da transição para um complexo hospitalar multidepartamental (**Hospital Ares**). O objetivo central é introduzir a reutilização de componentes por meio de **Flow Modules (`AR_MD_*`)**, eliminando duplicações de lógica através do princípio *DRY* (*Don't Repeat Yourself*), estabelecendo contratos padronizados de interface e centralizando o tratamento de erros e exceções.

## 🎯 Problema de Negócio
Com a expansão da operação da Clínica para a estrutura de um Hospital com múltiplos pontos de entrada e setores (Consultas, Exames, Financeiro, Pronto Atendimento e Internação), a abordagem monolítica dos projetos anteriores revelou gargalos operacionais:
1. **Duplicação Excessiva de Blocos (*Code Smell*):** Cada novo fluxo exigia a reconstrução manual do cabeçalho de inicialização (ativação de registos no CloudWatch e voz do Polly) e de validações de horário.
2. **Elevado Esforço de Manutenção e Débito Técnico:** Alterações na tabela horária de atendimento, na voz institucional ou nas mensagens de falha sistémica obrigavam a alterações manuais em múltiplos Contact Flows.
3. **Dispersão e Inconsistência no Tratamento de Exceções:** Ausência de um circuito padrão centralizado para controlo de retentativas e término gracioso (*Graceful Degradation*), elevando o risco de desconexões abruptas (*silent drops*).

## 🏛️ Arquitetura da Solução
- **Contact Flow Orquestrador Mestre:** `AR_CF_Hospital_Principal` — atua estritamente na navegação setorial e na integração de módulos.
- **Módulos Reutilizáveis (Flow Modules — `contactFlowModule`):**
  - `AR_MD_Inicializacao`: Centraliza a habilitação de telemetria com `Set logging behavior: Enabled` e a definição da voz neural de atendimento (Vitória, pt-BR).
  - `AR_MD_Verifica_Horario`: Centraliza a validação contra a tabela `AR_HO_Clinica` e a execução da mensagem de transbordo fora de expediente.
  - `AR_MD_Tratamento_Erros`: Padroniza o circuito anti-loop com controlo de contadores de sessão (`Tentativas`), mensagens auditivas de erro e saídas controladas.
- **Mecanismos de Interoperabilidade Modular:**
  - `Invoke flow module`: Chamada síncrona do fluxo mestre para o submódulo.
  - `Exit flow module`: Retorno determinístico para o fluxo chamador através de canais nomeados de sucesso ou exceção.
- **Filas e Encaminhamento:** Reutilização das filas `AR_Q_Consultas`, `AR_Q_Exames` e `AR_Q_Financeiro` vinculadas ao perfil unificado `AR_RP_Atendimento`.

## 💰 Política FinOps — Custo Zero (R$ 0,00)
- A criação, edição e publicação de Flow Modules e Contact Flows operam integralmente na camada de gestão gratuita do Amazon Connect.
- O provisionamento de números telefónicos públicos (DID/Toll-Free) e a tarifação por minutos de rede pública (PSTN) são mantidos como simulações conceituais e arquiteturais.
- A validação de execução modular é realizada através de validação estática de grafos compilados, esquemas exportados em JSON e emulação no softphone WebRTC integrado no console, preservando a regra inegociável de **Custo R$ 0,00**.

## 🎓 Competências Adquiridas (Projeto 4)

Ao finalizar este projeto, demonstrei e validei na prática:

* **Consigo explicar:** As vantagens de adotar Flow Modules no Amazon Connect, detalhando como a modularização reduz o débito técnico, previne erros de replicação manual e viabiliza a manutenção centralizada em ambientes de nível empresarial (*Enterprise*).
* **Consigo configurar:** A criação e publicação de módulos com o tipo de recurso `contactFlowModule`, estruturando pontos de saída controlados com o bloco `Exit flow module`.
* **Consigo orquestrar:** A integração entre fluxos de contacto mestres e submódulos utilizando o bloco `Invoke flow module`, tratando adequadamente as ramificações de sucesso e erro.
* **Consigo arquitetar:** O isolamento de responsabilidades operacionais, segregando inicialização de telemetria, verificações temporais de negócio e tratamento defensivo anti-loop em componentes isolados.
* **Consigo validar:** A integridade de execução e o estado das variáveis de sessão transmitidas de forma transparente entre o fluxo mestre e os submódulos invocados.

---

## 🚀 Próxima Evolução
Com a arquitetura modular estabelecida e a eliminação de duplicações no Hospital Ares, a próxima etapa da jornada é o **Projeto 5 (Automação, NLU e Integrações Serverless)**, onde introduziremos o reconhecimento de intenções via **Amazon Lex** e integração de dados com sistemas hospitalares através do **AWS Lambda**.

## 📐 Fluxograma da Solução (Projeto 4)

```
               ┌─────────────────────────────────────────┐
               │  Contact Flow: AR_CF_Hospital_Principal │
               └────────────────────┬────────────────────┘
                                    │
                                    ▼
               ┌─────────────────────────────────────────┐
               │       Invoke: AR_MD_Inicializacao       │
               │   (Logging: Enabled ➔ Voz: Vitória)    │
               └────────────────────┬────────────────────┘
                                    │ (Sucesso)
                                    ▼
               ┌─────────────────────────────────────────┐
               │     Invoke: AR_MD_Verifica_Horario      │
               │    (AR_HO_Clinica / Tratamento Fora)    │
               └──────────────┬───────────────────┬──────┘
                              │ (Aberto)          │ (Fechado / Erro)
                              ▼                   ▼
    ┌───────────────────────────────────┐   ┌──────────────────┐
    │    Menu Principal de Serviços     │   │ [ Disconnect ]   │
    │ 1-Consultas / 2-Exames / 3-Finan  │   └──────────────────┘
    └─────────────────┬─────────────────┘
                      │
                      │ (Entrada Inválida / Timeout)
                      ▼
    ┌───────────────────────────────────┐
    │   Invoke: AR_MD_Tratamento_Erros  │
    │  (Gestão de Tentativas e Mensagens)│
    └──────────┬─────────────────────┬──┘
               │ (Retentar)          │ (Limite Excedido)
               ▼                     ▼
        [ Retorna Menu ]      ┌──────────────────┐
                              │  AR_PR_Encerrar  │
                              └────────┬─────────┘
                                       │
                                       ▼
                                [ Disconnect ]
