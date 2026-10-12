# Modelo NLU & Especificação do Amazon Lex V2

## 1. Identificação do Bot
* **Nome do Bot:** `AR_Lex_AtendimentoAres`
* **Bot ID:** `PGBYHB6K6V`
* **Bot Alias:** `TestBotAlias` (`TSTALIASID`)
* **Idioma:** `Portuguese (BR)` (`pt_BR`)
* **Confidence Threshold:** `0.85`

## 2. Matriz de Intenções e Frases de Treino (*Sample Utterances*)

### 2.1. `ConsultarExame`
Intenção destinada a identificar solicitações de laudos e resultados laboratoriais/imagem.
* `Gostaria de ver o resultado do meu exame`
* `Quero consultar o laudo do meu exame`
* `Resultado de exame`
* `Ver meu laudo`
* `Consultar exame laboratorial`
* `Quero saber o resultado da minha ressonância`

### 2.2. `ConsultarAgendamento`
Intenção para consulta de consultas e procedimentos futuros marcados.
* `Gostaria de verificar a data da minha consulta`
* `Quando é o meu próximo agendamento`
* `Consultar agendamento de retorno`
* `Verificar horário marcado no hospital`

### 2.3. `CancelarAgendamento`
Intenção defensiva para cancelamentos e desmarcações.
* `Quero cancelar meu agendamento`
* `Preciso cancelar uma consulta marcada`
* `Desejo desmarcar minha consulta`
* `Não poderei comparecer e quero desmarcar meu exame`
> *Nota de Design:* A palavra isolada "cancelar" foi removida deliberadamente para evitar sobreposição vetorial com ruídos.

### 2.4. `ConsultarFinanceiro`
Intenção para envio de faturas, recibos e segunda via de boletos.
* `Segunda via do boleto`
* `Preciso pagar minha fatura`
* `Emitir boleto de cobrança`
* `Informações sobre pagamento do hospital`

### 2.5. `FalarComAtendente`
Intenção para transbordo assistido para operadores humanos.
* `Quero falar com um atendente humano`
* `Transferir para atendimento humano`
* `Falar com a equipe de suporte`
* `Preciso de ajuda de um atendente`

### 2.6. `AMAZON.FallbackIntent`
Intenção incorporada (*built-in*) acionada automaticamente quando todas as intenções concorrentes obtêm pontuação inferior a `0.85`.
* **Ação no Connect:** Dispara a saída `Default`, reproduzindo mensagem de contingência e transferindo para a fila básica.

## 3. Telemetria de Calibração (Inspeção Real)

| Frase de Entrada | Intenção Classificada | Score NLU | Resultado da Ação |
| :--- | :--- | :--- | :--- |
| `Gostaria de ver o resultado do meu exame` | `ConsultarExame` | **`0.92`** | 🟢 Aceite ($\ge 0.85$) |
| `Quero cancelar meu agendamento` | `CancelarAgendamento` | **`1.00`** | 🟢 Aceite ($\ge 0.85$) |
| `Quero falar com um atendente humano` | `FalarComAtendente` | **`0.93`** | 🟢 Aceite ($\ge 0.85$) |
| `abobrinha azul com parafuso de madeira` | `ConsultarFinanceiro` *(residual)* | **`0.76`** | 🔴 **Rejeitado para Fallback** ($0.76 < 0.85$) |
