# Relatório Completo de Engenharia: Troubleshooting & Resolução de Incidentes
**Projeto 8 — Ares Conversational (Amazon Connect • Amazon Lex V2 • AWS Lambda • Amazon DynamoDB)**

Este relatório consolida a investigação técnica, análise de telemetria e soluções arquiteturais aplicadas para sanar todos os erros e desvios de rota identificados durante o ciclo de desenvolvimento e homologação do Projeto 8.

---

## 📑 Matriz Geral de Incidentes Resolvidos

| ID | Camada | Componente Afetado | Falha Observada | Causa Raiz Técnica | Solução Aplicada |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **INC-01** | Backend / URA | Contact Flow (`AR_CF_Conversational`) | Consulta de exame lia atributos vazios ou quebrava o fluxo. | Falta de bloco defensivo de validação antes do prompt de leitura. | Inserção do bloco de decisão `AR_CheckLaudoValido` avaliando atributo de status. |
| **INC-02** | NLU / Lex V2 | Intenção `ConsultarFinanceiro` | Frase de ruído (*"abobrinha..."*) acionava mensagens de fatura/boleto. | Utterance de treino excessivamente ampla (`"Assunto financeiro"`). | Expurgo da frase genérica e manutenção de sentenças restritas a cobrança. |
| **INC-03** | NLU / Lex V2 | Intenção `CancelarAgendamento` | Ruído com conectivo *"com"* ativava cancelamento de consulta. | Presença de palavras isoladas no treino (`"cancelar"` solto). | Remoção dos monossílabos e substituição por sentenças completas com verbo e objeto. |
| **INC-04** | NLU / Lex V2 | Intenção `FalarComAtendente` | Ruído residual atingia score `0.82` e transferia para operador humano. | Termos isolados (`"falar"`, `"ajuda"`) somados a threshold permissivo (< `0.82`). | Limpeza de vocábulos soltos e elevação do limiar de corte do idioma para `0.85`. |
| **INC-05** | Integração API | Lambda `AR_LF_ConsultaExame` | Protocolo válido `1001` caía no prompt de contingência (fallback). | Quebra de contrato de string: Lambda devolvia `"FOUND"` e o Connect exigia `"SUCCESS"`. | Refatoração do retorno da Lambda para `"status": "SUCCESS"` e novo deploy. |

---

## 🛑 INC-01: Ausência de Validação Defensiva de Atributos da Lambda

### 1. O Erro
Nas primeiras iterações do Contact Flow, a saída de sucesso (`Success`) do bloco *Invoke AWS Lambda function* (`AR_InvokeConsultaExame`) conectava-se diretamente ao bloco de reprodução de voz (`AR_PlayLaudoExame`). Quando um paciente inexistente era digitado (ex.: protocolo `9999`), a URA tentava reproduzir o laudo sintetizando valores vazios:
> *"Olá, . Localizamos seu exame de . O laudo consta como: ."*

### 2. A Causa Raiz
A ramificação `Success` do bloco *Invoke AWS Lambda function* no Amazon Connect monitora exclusivamente o **sucesso de transporte da requisição (HTTP 200)**. Se a função executa sem falhas de runtime mas o registro não existe no banco de dados, a Lambda responde com sucesso técnico devolvendo campos nulos. O Connect não valida semanticamente se os atributos contêm valores válidos antes de enviá-los ao sintetizador Polly.

### 3. A Solução Empregada
Implementou-se o princípio de arquitetura defensiva no fluxo:
1. Desfez-se a ligação direta entre `AR_InvokeConsultaExame` e `AR_PlayLaudoExame`.
2. Inseriu-se o bloco `AR_CheckLaudoValido` (bloco de decisão do tipo *Compare* / *Check contact attributes*) entre a invocação da Lambda e o áudio de leitura[cite: 2, 5].
3. O bloco foi parametrizado para avaliar se a chave de controle externa (`$.External.status`) atende aos critérios de sucesso antes de liberar a síntese do áudio clínico[cite: 5]. Se a condição falhar, o contato é desviado para o bloco de contingência `AR_PlayFallback`[cite: 2, 5].

---

## 🛑 INC-02: Falso Positivo de NLU na Intenção `ConsultarFinanceiro`

### 1. O Erro
Ao realizar chamadas telefônicas reais e pronunciar entradas completamente fora de domínio (ex.: *"abobrinha azul com parafuso de madeira"*), o Amazon Lex V2 classificava a fala como intenção financeira, sintetizando o áudio:
> *"Para assuntos financeiros, emissão de faturas e segunda via de boletos, encaminhamos as orientações de pagamento para o seu telefone de cadastro via SMS."*[cite: 5]

### 2. A Causa Raiz
Na definição da intenção `ConsultarFinanceiro` (`Intent.json`), havia sido cadastrada a seguinte *sample utterance*:
* `"Assunto financeiro"`

Essa expressão de apenas duas palavras genéricas expandiu demasiadamente a fronteira semântica (vetor de embeddings) da intenção. Em chamadas telefônicas (onde o áudio é comprimido pelo codec PSTN a 8 kHz), ruídos e pausas fonéticas acabavam sendo atraídos por essa frase vaga, recebendo score estatístico superior ao threshold configurado na época[cite: 7].

### 3. A Solução Empregada
1. No console do Amazon Lex V2, acessou-se a intenção `ConsultarFinanceiro` sob o idioma `Portuguese (BR)`.
2. **Remoção:** Excluiu-se a frase ampla `"Assunto financeiro"`.
3. **Reestruturação:** Mantiveram-se apenas frases completas que contextualizam diretamente o ato de pagamento (`"Segunda via do boleto"`, `"Preciso pagar minha fatura"`, `"Emitir boleto de cobrança"`).
4. Executou-se o **Criar (*Build*)** do bot[cite: 3].

---

## 🛑 INC-03: Falso Positivo de NLU na Intenção `CancelarAgendamento`

### 1. O Erro
Após corrigir a intenção financeira, novo teste falado da mesma expressão de ruído (*"abobrinha azul com parafuso de madeira"*) produziu um novo desvio incorreto, ativando `CancelarAgendamento`[cite: 7]:
> *"Entendemos sua solicitação. O seu pedido de cancelamento de consulta ou exame foi registrado com sucesso em nosso sistema hospitalar."*[cite: 5]

### 2. A Causa Raiz
Na intenção `CancelarAgendamento`, existiam frases de treino com monossílabos e termos soltos:
* `"cancelar"` (palavra única)
* `"cancelar exame"`[cite: 6]
* `"cancelar consulta"`[cite: 6]

A adição do conectivo *"com"* na pronúncia (*"abobrinha azul **com** parafuso..."*)[cite: 7] gerou uma correlação fonética espúria com o radical do verbo *"cancelar"*. O classificador encontrou a menor distância vetorial justamente nessa intenção permissiva, atribuindo pontuação superior ao limiar residual[cite: 7].

### 3. A Solução Empregada
1. No console do Lex V2, acessou-se a intenção `CancelarAgendamento`[cite: 6].
2. **Remoção:** Excluíram-se todas as expressões de palavra única ou termos soltos (`"cancelar"`, `"cancelar exame"`, `"cancelar consulta"`)[cite: 6].
3. **Reestruturação:** Adicionaram-se sentenças estruturadas contendo obrigatoriamente sujeito, verbo e contexto hospitalar:
   * `"Quero cancelar meu agendamento"`
   * `"Preciso cancelar uma consulta marcada"`
   * `"Desejo desmarcar minha consulta"`
   * `"Não poderei comparecer e quero desmarcar meu exame"`
4. Executou-se nova compilação (*Build*) do modelo[cite: 3].

---

## 🛑 INC-04: Atração Residual na Intenção `FalarComAtendente` e Calibração de Threshold

### 1. O Erro
Com o bloqueio das intenções anteriores, a frase fora de domínio passou a ativar a intenção de transbordo humano `FalarComAtendente`, transferindo a ligação diretamente para a fila de espera.

### 2. A Causa Raiz
A investigação via botão **Inspecionar** (*Inspect*) do Lex V2 expôs os scores matemáticos reais do motor:
```json
"interpretations": [
  {
    "nluConfidence": { "score": 0.82 },
    "intent": { "name": "FalarComAtendente" }
  },
  {
    "intent": { "name": "FallbackIntent" }
  },
  {
    "nluConfidence": { "score": 0.76 },
    "intent": { "name": "ConsultarFinanceiro" }
  }
]
