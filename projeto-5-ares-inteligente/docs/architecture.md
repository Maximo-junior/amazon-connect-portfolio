# 🏛️ Arquitetura Técnica — Projeto 5: Ares Inteligente

**Ecossistema Ares Saúde | Complexo: Hospital Ares**

## 1. Visão Geral da Arquitetura

O Projeto 5 implementa uma camada de autosserviço orientada a inteligência conversacional (NLU) e integração com backend serverless. A solução automatiza a consulta de laudos de exames sem intervenção humana, oferecendo transbordo assistido para filas de atendimento em caso de necessidade ou solicitação explícita.

A arquitetura foi projetada considerando uma integração entre **Amazon Connect, camada de inteligência conversacional e AWS Lambda**, mantendo neste projeto uma abordagem de desenvolvimento e simulação local para preservar a política institucional de **Custo Real = R$ 0,00**.

A arquitetura adota o princípio de **desacoplamento de componentes**, separando a orquestração da experiência de voz, os módulos reutilizáveis, a camada de inteligência conversacional e a lógica de backend.

- **Front-end de Voz/CCaaS:** Amazon Connect (`AR_CF_Ares_Inteligente`).

- **Submódulos Reutilizáveis:** `AR_MD_Inicializacao`, `AR_MD_Verifica_Horario` e `AR_MD_Tratamento_Erros`.

- **Camada de Inteligência Conversacional:** Simulação conceitual de NLU baseada no Amazon Lex V2, representando o reconhecimento da intenção do paciente.

- **Backend Serverless:** AWS Lambda (`AR_LF_ConsultaExame`), responsável pela lógica de consulta e preparação do contrato de dados consumido pelo Contact Flow.

- **Ambiente de Desenvolvimento:** Código Python da Lambda desenvolvido e versionado localmente no VS Code, com eventos e contratos JSON utilizados para simulação e validação.

> **Nota de Implementação:** A função `AR_LF_ConsultaExame` representa a arquitetura de backend serverless que seria executada em AWS Lambda em um ambiente implantado. Neste projeto, a função não é provisionada ou executada na AWS, sendo validada localmente por meio do código Python e dos contratos JSON, em conformidade com a política de **Custo Real = R$ 0,00**.

---

## 2. Diagrama Lógico de Integração

```
                               ┌──────────────────────────────────┐
                               │   Chamada Entrante do Paciente   │
                               └────────────────┬─────────────────┘
                                                │
                                                ▼
                               ┌──────────────────────────────────┐
                               │  AR_MD_Inicializacao (Logs+Voz) │
                               └────────────────┬─────────────────┘
                                                │
                                           (Sucesso)
                                                │
                                                ▼
                               ┌──────────────────────────────────┐
                               │     AR_MD_Verifica_Horario       │
                               └───────────────┬──────────────────┘
                                               │
                                        (Dentro do Horário)
                                               │
                                               ▼
                               ┌──────────────────────────────────┐
                               │      AR_CF_Ares_Inteligente      │
                               │   Get Customer Input (NLU/DTMF)  │
                               └───────────────┬──────────────────┘
                                               │
                       ┌───────────────────────┴───────────────────────┐
                       │                                               │
                (Branch 1: Exames)                            (Branch 2: Transbordo)
                       │                                               │
                       ▼                                               ▼
              ┌────────────────────────┐                    ┌────────────────────────┐
              │ Backend Serverless     │                    │ Definir Fila:          │
              │ AR_LF_ConsultaExame    │                    │ AR_Q_Consultas         │
              │ (Simulação Local)      │                    └───────────┬────────────┘
              └──────────┬─────────────┘                                │
                         │                                              ▼
                         │                                  ┌────────────────────────┐
                         │                                  │ Transferir para Fila   │
                         │                                  └────────────────────────┘
                         │
                         ▼
              ┌────────────────────────┐
              │ Play Prompt Dinâmico   │
              │ (Laudo Disponível)     │
              └──────────┬─────────────┘
                         │
                         ▼
              ┌────────────────────────┐
              │ Encerramento /         │
              │ Desconexão             │
              └────────────────────────┘
```
## 3. Responsabilidades dos Componentes

### Amazon Connect — `AR_CF_Ares_Inteligente`

Responsável pela orquestração da jornada de voz, recebimento da entrada do paciente, direcionamento das ramificações, reprodução dos prompts e transferência para atendimento humano.

### `AR_MD_Inicializacao`

Responsável pelas etapas iniciais da chamada, incluindo inicialização de contexto, registros e mensagens de entrada.

### `AR_MD_Verifica_Horario`

Responsável pela validação do horário de funcionamento e pelo direcionamento da chamada conforme a disponibilidade do atendimento.

### `AR_MD_Tratamento_Erros`

Responsável pelo tratamento padronizado de entradas inválidas, timeouts e excesso de tentativas, evitando loops indefinidos no Contact Flow.

### `AR_LF_ConsultaExame`

Representa a camada de backend responsável pela consulta do exame e pela preparação dos dados que serão consumidos pelo Contact Flow.

A implementação foi desenvolvida em **Python no VS Code**, permitindo versionamento, organização do código, testes locais e validação dos contratos JSON.

Em uma implantação real, essa lógica poderia ser executada como uma função **AWS Lambda** e integrada ao Amazon Connect.

### Camada NLU

Representa conceitualmente a utilização do **Amazon Lex V2** para identificação da intenção do paciente, permitindo que uma interação por linguagem natural seja convertida em uma intenção de negócio, como consulta de exames ou solicitação de atendimento humano.

Neste projeto, essa camada permanece em caráter de simulação para preservar a estratégia de custo zero.

---

## 4. Estratégia FinOps

O projeto foi estruturado para demonstrar a arquitetura e a lógica de integração sem gerar custos reais de execução.

Por esse motivo:

- O código da Lambda é desenvolvido localmente no VS Code.
- Os contratos de entrada e saída são representados por arquivos JSON.
- Os cenários de sucesso, paciente não encontrado e erro são simulados localmente.
- A integração real com serviços tarifados não é provisionada.
- O Amazon Connect é utilizado para modelagem dos Contact Flows e módulos.
- A camada NLU é representada conceitualmente.
- A execução real da Lambda em produção fica como etapa futura de implantação.

Essa estratégia permite demonstrar conhecimentos de **Amazon Connect, arquitetura serverless, Python, contratos de API, tratamento de erros, modularização e FinOps**, mantendo o projeto dentro da premissa de **Custo Real = R$ 0,00**.
```

---

