```markdown
# Registos de Decisão de Arquitetura (ADRs) — Projeto 8

## ADR 008.1 — Calibração Rígida do Limiar de Confiança do Amazon Lex V2

### Contexto
Durante os testes de homologação com canal telefônico (áudio 8 kHz via PSTN), expressões fora de contexto hospitalar (ex.: *"abobrinha azul com parafuso de madeira"*) atingiam pontuações entre `0.76` e `0.82` em intenções com raio semântico amplo (`ConsultarFinanceiro` e `FalarComAtendente`), gerando falsos positivos graves.

### Decisão
1. Higienizar as *sample utterances* de todas as intenções de negócio, removendo termos de palavra única (como *"cancelar"*, *"falar"* ou *"atendente"* soltos).
2. Fixar o `nluIntentConfidenceThreshold` do idioma `pt_BR` em **`0.85`**.

### Justificativa Técnica
A análise do payload do Lex V2 revelou que frases legítimas de negócio (`ConsultarExame`, `CancelarAgendamento`) pontuam entre `0.92` e `1.00`, enquanto o ruído fonético atinge no máximo `0.82`. O limiar em `0.85` cria uma separação determinística: ruídos caem obrigatoriamente no `FallbackIntent`, sem impactar os utilizadores legítimos.

### Consequências
* **Positivas:** Rejeição robusta de ruído de fundo e direcionamento consistente para a contingência da URA.
* **Trade-off:** Exige que frases de negócio tenham contexto sintático claro; entradas ambíguas de palavra única são descartadas para a fila humana.

---

## ADR 008.2 — Contrato de Dados Padronizado e Validação Defensiva de Atributos

### Contexto
O bloco de invocação de Lambda no Amazon Connect possui duas ramificações básicas: `Success` e `Error`. No entanto, `Success` sinaliza apenas que a função executou sem exceções de runtime (código HTTP 200 de transporte). Quando um paciente não é localizado, a função executa com sucesso, mas devolve dados vazios. Se o fluxo seguir direto para a reprodução do laudo, a URA sintetiza frases truncadas ou campos nulos (*"Olá, . Localizamos seu exame de..."*).

### Decisão
1. Padronizar a resposta da Lambda com a chave explícita de controle `status`:
   * `status = "SUCCESS"` quando o registo existe no DynamoDB.
   * `status = "NOT_FOUND"` quando a chave primária não existe.
2. Inserir o bloco `AR_CheckLaudoValido` (*Compare*) imediatamente após a Lambda para validar se `$.External.status == "SUCCESS"`.

### Justificativa Técnica
Garante que falhas de negócio não sejam mascaradas como sucessos funcionais, impedindo vazamento de strings vazias para a experiência do chamador e enviando casos não encontrados para o fallback com transferência assistida.

### Consequências
* **Positivas:** Resiliência auditável e conformidade com práticas de engenharia de software hospitalar.
* **Trade-off:** Adiciona um bloco lógico a mais no Contact Flow, aumentando minimamente a latência de decisão (~10ms).
