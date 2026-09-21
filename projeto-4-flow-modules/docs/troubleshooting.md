# 🔍 Troubleshooting e Diagnóstico Técnico — Projeto 4
**Ecossistema Ares Saúde | Complexo: Hospital Ares**

Casos técnicos reais investigados e solucionados durante o desenvolvimento dos módulos e do orquestrador hospitalar:

---

### Caso 1: Falha ao Publicar Módulo com Nós Abertos
* **Sintoma:** Faixa vermelha no topo da tela indicando *"Falha ao publicar o módulo"*.
* **Causa Raiz:** O bloco `Definir voz` continha ramificações de saída (`Êxito` e `Erro`) sem nenhuma aresta conectada a um nó posterior.
* **Diagnóstico:** O compilador de Flow Modules no Amazon Connect constrói um grafo acíclico direcionado estrito; módulos não aceitam pontas soltas.
* **Resolução:** Inclusão do bloco terminal `Retornar` (*Exit flow module*) e ancoragem de ambas as saídas de voz no bloco de retorno.

---

### Caso 2: Utilização Inadequada de Bloco Terminal `Desconectar` em Submódulo
* **Sintoma:** O módulo de inicialização desligava a chamada logo após carregar os logs e a voz, impedindo a continuidade do atendimento.
* **Causa Raiz:** Uso do bloco `Desconectar` (*Disconnect*) em vez de `Retornar` (*Exit flow module*).
* **Diagnóstico:** `Disconnect` encerra a sessão SIP/WebRTC imediatamente. Submódulos reutilizáveis devem sempre empregar `Retornar` para devolver o controle ao fluxo chamador.
* **Resolução:** Substituição imediata do bloco de desconexão pelo bloco `Retornar`.

---

### Caso 3: Erro de Nó Não Ancorado no Bloco `Invocar módulo`
* **Sintoma:** Ícone vermelho `(X)` na ramificação `Sem correspondência` do bloco de invocação do módulo de erros.
* **Causa Raiz:** A aresta gráfica foi solta na área livre próxima ao bloco `Obter informações dos clientes` sem engatar na porta de entrada (*Entry point*).
* **Diagnóstico:** Validação visual de conexão indicando nó incompleto no compilador do Flow Designer.
* **Resolução:** Exclusão da linha órfã e reconstrução da conexão diretamente no conector de entrada do bloco do menu.
