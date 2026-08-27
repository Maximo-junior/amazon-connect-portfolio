# 🔍 Troubleshooting e Diagnóstico Técnico — Projeto 3
**Ecossistema Ares Saúde | Módulo: Contact Attributes e Roteamento por Contexto**

---

## 📌 Metodologia de Investigação
Seguindo o padrão de engenharia do portfólio Ares Saúde, cada incidente operacional ou desvio comportamental identificado durante a fase de testes e homologação é tratado sob a metodologia estruturada:
1. **Sintoma:** Descrição objetiva da falha observada.
2. **O que sabemos:** Fatos confirmados e configurações vigentes.
3. **O que ainda não sabemos:** Pontos cegos sob investigação.
4. **Hipóteses:** Levantamento causal baseado na arquitetura da AWS.
5. **Causa Raiz:** Explicação técnica do comportamento do motor do Amazon Connect.
6. **Solução Adotada:** Correção aplicada no laboratório (FinOps R$ 0,00) e recomendação corporativa para produção.

---

## 🚨 Incidente 01: Desvio Imediato para "Opção Inválida / Timeout" no Emulador de Web Chat

### 1. Sintoma
Ao iniciar a interação no emulador de chat (*Test Chat*) com o fluxo `AR_CF_Triagem_Contexto`, a mensagem de saudação era reproduzida e, imediatamente (sem tempo para digitação do usuário) ou logo após o envio do dígito `1`, o sistema executava duas vezes consecutivas a mensagem *"Opção inválida ou tempo de resposta esgotado"*, acionando a regra de limite de tentativas e desconectando a sessão.

### 2. O que sabemos
* O Contact Flow foi construído como uma URA de Voz Inbound (`CanalEntrada = Voz_Inbound`).
* O bloco `Obter informações dos clientes` (`GetParticipantInput`) estava parametrizado com a aba **DTMF** ativa e opções numéricas `1`, `2` e `3`.
* O canal utilizado para o disparo do teste foi a janela de **Web Chat** do console administrativo.
* O tempo limite (*timeout*) estava inicialmente configurado para 5 segundos.

### 3. O que ainda não sabíamos
* Se o canal de Chat do Amazon Connect realizava a conversão implícita de caracteres de texto (*strings* ASCII `"1"`, `"2"`, `"3"`) em eventos de tom telefônico (frequências RFC 2833).

### 4. Hipóteses Levantadas
* **Hipótese 1:** O temporizador de 5 segundos contava antes do carregamento visual do componente no navegador, forçando um disparo prematuro da ramificação `InputTimeLimitExceeded`.
* **Hipótese 2:** O bloco `GetParticipantInput` configurado exclusivamente na aba DTMF rejeita mensagens de texto livre, disparando o erro `NoMatchingCondition` (*Default / Padrão*) por incompatibilidade de canal de mídia.
* **Hipótese 3:** Falha na persistência dos atributos de inicialização de contagem de tentativas (`Tentativas = 0`).

### 5. Causa Raiz Técnica
O bloco `Obter informações dos clientes` (*Get customer input*) na modalidade **DTMF** foi projetado para capturar frequências de áudio de sinalização telefônica (Dual-Tone Multi-Frequency) presentes exclusivamente em fluxos de voz (*Voice Inbound*).

No canal de Web Chat, as mensagens trafegam como *payloads* JSON contendo *strings* textuais. O compilador de execução do Amazon Connect **não realiza parsing de texto para DTMF automaticamente**. Ao receber a mensagem `"1"` via chat, o analisador léxico do bloco identifica que não houve bipe de telefonia e desvia a execução para a saída `NoMatchingCondition` (Padrão). O contador de tentativas foi incrementado até atingir o threshold (`Tentativas >= 2`), acionando o encerramento gracioso via `AR_PR_Encerramento` ➔ `DisconnectParticipant`.

### 6. Solução e Diferenciação Arquitetural

* **🧪 No Laboratório (FinOps R$ 0,00):**
  O fluxo `AR_CF_Triagem_Contexto` é formalmente classificado e homologado como uma **URA de Telefonia/Voz**. A validação foi concluída através da compilação e publicação do grafo no Flow Designer, da integridade do arquivo de definição `AR_CF_Triagem_Contexto_v3.json` e do pareamento de atributos no softphone WebRTC/CCP, sem provisionar números PSTN pagos.

* **🏢 Em Ambientes Corporativos de Produção:**
  Para suporte Omnichannel verdadeiro (mesmo fluxo atendendo Voz e Chat simultaneamente), as organizações adotam:
  1. **Separação de Canais:** Roteamento inicial via `Check contact attributes` avaliando o atributo de sistema `Channel` (`VOICE` vs `CHAT`).
  2. **Tratamento de Chat:** Uso de blocos **Enviar mensagem interativa** (*Send interactive message*) com componentes do tipo *Quick Replies* / *List Pickers*, onde o clique do usuário devolve um valor estruturado nativo para o chat.
  3. **NLU com Amazon Lex:** Uso de bots com intents mapeadas para reconhecer tanto a fala/tom quanto o texto digitado livremente pelo usuário.

---

## 🚨 Incidente 02: Pontas Soltas de Erro e Risco de Chamada Muda (*Silent Drop*)

### 1. Sintoma
Durante a modelagem inicial dos blocos `Ver atributos do contato` (*Set contact attributes*) e `Verificar atributos do contato` (*Check contact attributes*), as saídas de exceção técnica (`Erro` e `Sem correspondência`) não possuíam conexões definidas no canvas.

### 2. Causa Raiz
Em cenários de degradação interna da AWS ou falha na leitura da memória de sessão, a ausência de tratamento explícito na ramificação `Erro` resulta em terminação imediata da chamada pelo Amazon Connect (*Drop silencioso*), gerando uma experiência negativa ao usuário final.

### 3. Solução Aplicada
Convergência de todas as saídas de exceção técnica não recuperáveis dos blocos de atributos para o bloco de áudio defensivo `AR_PR_Encerramento` (*"Número de tentativas excedido..."* ou aviso de indisponibilidade sistêmica) antes da transição final para o bloco `Desconectar` (*Graceful Degradation*).
