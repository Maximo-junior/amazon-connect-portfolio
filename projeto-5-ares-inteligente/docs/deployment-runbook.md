# 🚀 Runbook de Implantação em Produção — Projeto 5
**Ecossistema Ares Saúde | Módulo: Ares Inteligente**

---

## 🎯 Objetivo
Este runbook descreve as etapas técnicas necessárias para transicionar o microsserviço serverless e a camada conversacional do ambiente de desenvolvimento local (VS Code / FinOps R$ 0,00) para um ambiente corporativo ativo na AWS.

---

## 📋 Pré-requisitos
* Permissões de IAM para criação de funções no AWS Lambda e configuração da instância do Amazon Connect.
* Instância do Amazon Connect previamente provisionada com as filas departamentais criadas.
* Código da função disponível em `src/lambda/consulta_exame.py`.

---

## 🛠️ Procedimento de Implantação

### Etapa 1: Provisionamento da Função no AWS Lambda
1. Acesse o console da AWS e navegue até o serviço **AWS Lambda**.
2. Clique em **Create function** (Criar função) e selecione **Author from scratch**.
3. Configure os parâmetros básicos:
   * **Function name:** `AR_LF_ConsultaExame`
   * **Runtime:** `Python 3.12` (ou superior)
   * **Architecture:** `x86_64`
4. Em **Permissions**, garanta que a role de execução possua a política gerenciada `AWSLambdaBasicExecutionRole` para escrita no Amazon CloudWatch Logs.
5. Copie o código-fonte de `src/lambda/consulta_exame.py`, cole no editor inline da Lambda e clique em **Deploy**.

---

### Etapa 2: Autorização de Invocação (Resource-Based Policy)
Por segurança de menor privilégio (*Least Privilege*), o Amazon Connect rejeita chamadas a Lambdas que não foram explicitamente associadas à instância:
1. No console da AWS, acesse o serviço **Amazon Connect**.
2. Clique no **Instance alias** da sua central de atendimento.
3. No painel de navegação esquerdo, clique em **Contact flows** (Fluxos de contato).
4. Role até a seção **AWS Lambda**:
   * No menu suspenso, selecione a função `AR_LF_ConsultaExame`.
   * Clique em **+ Add Lambda Function** (+ Adicionar função Lambda).
5. *Nota de Auditoria:* A AWS aplicará automaticamente uma política baseada em recurso permitindo que o serviço `connect.amazonaws.com` invoque a função através da ação `lambda:InvokeFunction`.

---

### Etapa 3: Integração no Flow Designer
1. Acesse o console do Amazon Connect com perfil de administrador/designer.
2. Abra o fluxo de contato `AR_CF_Ares_Inteligente`.
3. Substitua o bloco de simulação pelo bloco **Invoke AWS Lambda function** (Invocar função do AWS Lambda).
4. Configure as propriedades do bloco:
   * **Function:** Selecione `AR_LF_ConsultaExame`.
   * **Timeout:** Defina como `5` segundos (máximo de 8s suportado pelo Connect).
   * **Input Parameters:**
     * *Destination key:* `idPaciente`
     * *Value:* Mapeado via entrada DTMF coletada ou Slot do Amazon Lex.

---

### Etapa 4: Interpolação Dinâmica de Voz (Amazon Polly)
No bloco **Play prompt** (Reproduzir mensagem) subsequente, configure o sintetizador de voz com texto dinâmico consumindo o namespace de atributos externos:

"Localizamos o seu laudo de $.External.tipoExame liberado em $.External.dataLiberacao. A situação atual é: $.External.situacaoLaudo. A Ares Saúde agradece sua ligação."

### Etapa 5: Validação e Contingência Defensiva

1. **Roteamento de Sucesso:**
   * Conecte a saída de **Success** do bloco **Invoke AWS Lambda function** diretamente ao bloco de reprodução dinâmica do laudo (*Play prompt*).

2. **Circuito de Falha e Contingência:**
   * Conecte a saída de **Error** do bloco Lambda diretamente ao módulo corporativo `AR_MD_Tratamento_Erros`.
   * **Comportamento em Falha:** Em cenários de indisponibilidade da API, *timeout* (tempo de execução superior a 5 segundos) ou erro 500 retornado pelo backend hospitalar, o fluxo aciona a política centralizada de retentativas ou executa o transbordo gracioso para atendimento humano na fila `AR_Q_Consultas`, impedindo quedas abruptas de conexão (*silent drops*) ou períodos prolongados de silêncio na linha.
