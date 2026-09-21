# 🔍 Troubleshooting e Diagnóstico Técnico — Projeto 5

**Ecossistema Ares Saúde | Complexo: Hospital Ares**

---

## Caso 1: Falha na Leitura de Atributos Externos no Amazon Connect

* **Sintoma:** O bloco *Play prompt* permanece em silêncio ou direciona a execução para uma ramificação de erro ao tentar utilizar valores retornados pela Lambda.

* **Causa Raiz:** O contrato de saída da função não estava alinhado com a forma como os valores seriam consumidos pelo Amazon Connect. Em um cenário de integração, estruturas aninhadas, chaves inconsistentes ou referências incorretas podem impedir que o fluxo encontre o valor esperado.

* **Diagnóstico:** Foi realizada a validação do contrato de saída da `AR_LF_ConsultaExame`, verificando a correspondência entre as chaves retornadas pelo backend e as referências utilizadas no Contact Flow.

  Para facilitar o consumo pelo fluxo e reduzir ambiguidades, o projeto adotou uma estrutura de retorno simples, com atributos diretamente acessíveis e valores em formato `string`.

* **Resolução:** O handler Python foi ajustado para retornar os dados necessários em um formato plano e previsível, por exemplo:

  ```text
  statusExame: "FOUND"
  tipoExame: "Ressonância Magnética"
  dataExame: "20/09/2026"
  laudoDisponivel: "true"
  ```

  Dessa forma, o Contact Flow consegue utilizar diretamente os atributos retornados no processamento da Lambda.

* **Validação:** Como a Lambda não foi implantada na AWS neste projeto, a validação foi realizada por meio dos contratos JSON e dos eventos simulados armazenados no repositório, preservando a política de **Custo Real = R$ 0,00**.

---

## Caso 2: Loop Infinito por Ausência de Resposta no Menu Inteligente

* **Sintoma:** A chamada permanece repetindo indefinidamente a saudação inicial do assistente virtual quando o paciente não fornece uma resposta válida.

* **Causa Raiz:** As saídas de `Tempo limite` e `Padrão` do bloco de entrada estavam conectadas novamente ao menu sem um mecanismo de controle de tentativas.

* **Diagnóstico:** A ausência de um contador ou de uma política determinística de retentativas permitia que o Contact Flow retornasse continuamente ao mesmo ponto de interação.

  Esse comportamento poderia manter a chamada em loop indefinidamente, sem uma condição determinística para interromper as tentativas.

* **Resolução:** As saídas de erro e ausência de entrada foram direcionadas para o módulo reutilizável `AR_MD_Tratamento_Erros`, responsável por controlar a quantidade de tentativas.

  Após atingir o limite configurado de **duas falhas**, o módulo reproduz uma mensagem informativa e encerra a chamada.

* **Resultado:** O fluxo passou a possuir comportamento determinístico para entradas inválidas e timeouts, evitando loops infinitos e garantindo uma experiência previsível para o paciente.

---

## Considerações Técnicas

O troubleshooting do Projeto 5 segue uma abordagem baseada na análise do **contrato entre os componentes**, no comportamento do **Contact Flow** e na aplicação de mecanismos de **resiliência e controle de erros**.

A arquitetura separa as responsabilidades entre:

* **Amazon Connect:** responsável pela orquestração da experiência de voz e execução do Contact Flow.
* **`AR_LF_ConsultaExame`:** responsável pela lógica de consulta e pelo contrato de dados da camada serverless.
* **`AR_MD_Tratamento_Erros`:** responsável pelo tratamento padronizado de entradas inválidas, timeouts e limite de tentativas.
* **Contratos JSON:** utilizados para representar e validar os eventos de entrada e saída da Lambda durante o desenvolvimento.
* **VS Code:** utilizado como ambiente de desenvolvimento da função Python, permitindo organização, versionamento e testes do código antes de uma eventual implantação.
* **Simulações locais:** utilizadas para validar o comportamento da integração sem necessidade de provisionar a função Lambda em ambiente AWS.

Essa abordagem permite identificar problemas de integração antes de uma eventual implantação em produção e mantém o projeto alinhado à política de **FinOps de Custo Real = R$ 0,00**.
