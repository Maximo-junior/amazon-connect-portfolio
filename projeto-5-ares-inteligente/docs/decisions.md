# 📋 Architecture Decision Records (ADRs) — Projeto 5
**Ecossistema Ares Saúde | Complexo: Hospital Ares**

---

## ADR-008: Desenvolvimento Local da Lambda e Preservação da Política FinOps

* **Status:** Aprovado
* **Data:** 2026-09-21

---

### Contexto
A implementação do backend `AR_LF_ConsultaExame` utiliza AWS Lambda como referência arquitetural, porém o projeto possui como requisito institucional a manutenção de **Custo Real = R$ 0,00**.

Além da questão de custos, o código da função Lambda é tratado como componente de software e, portanto, deve possuir uma estrutura adequada para desenvolvimento, testes, versionamento e manutenção.

---

### Decisão
O código da Lambda será desenvolvido e mantido localmente no **VS Code**, em **Python**, dentro do repositório do projeto, em vez de ser escrito diretamente no editor inline do console da AWS Lambda.

O console da AWS Lambda é adequado para alterações rápidas, testes pontuais e funções simples. No entanto, para este projeto, o desenvolvimento local oferece uma estrutura alinhada às práticas de engenharia de software, permitindo:

* **Organização estruturada:** Isolamento do código em arquivos e diretórios padronizados (`src/lambda/`);
* **Versionamento contínuo:** Rastreamento granular de alterações utilizando Git;
* **Auditoria de código:** Comparação e rastreamento de mudanças via commits e pull requests;
* **Modularidade e reuso:** Reutilização facilitada de funções auxiliares e regras de negócio;
* **Testes unitários e de contrato:** Execução e validação local antes de qualquer implantação em nuvem (Shift-Left);
* **Validação de contratos (API-First):** Verificação estrita dos contratos de entrada (`event`) e saída (`flat key-value`);
* **Documentação de cenários:** Mapeamento explícito de simulações declarativas em JSON (`simulations/lambda/`);
* **Automação (CI/CD / IaC):** Preparação da base de código para integração com pipelines de implantação automatizada (GitHub Actions, AWS SAM ou AWS CDK).

A função `AR_LF_ConsultaExame` é tratada como um artefato de software versionável, e não como um script descartável criado na console web.

Neste **Projeto 5**, a função não é submetida a provisionamento em infraestrutura AWS tarifada. O comportamento do microsserviço é validado por meio do código Python, eventos de teste e contratos de interface simulados e armazenados no repositório.

---

### Justificativa Técnica
A escolha pelo VS Code não decorre de incapacidade de execução no console da AWS, mas sim da estruturação correta do ciclo de desenvolvimento de software (*SDLC*).

Em um cenário corporativo de produção, o ciclo de vida do código segue o fluxo:

```
VS Code (Desenvolvimento Local)
       │
       ▼
Git / GitHub (Versionamento e Revisão)
       │
       ▼
Testes Unitários / Linters (Shift-Left Testing)
       │
       ▼
Pipeline CI/CD (GitHub Actions / AWS SAM)
       │
       ▼
AWS Lambda (Ambiente de Execução / Runtime)
```
Dessa forma, separar desenvolvimento de execução melhora a rastreabilidade e permite que o mesmo código seja revisado, testado e versionado antes de chegar à infraestrutura. ```

### Consequências
Positivas:

- Código organizado e versionado no Git;
- Maior facilidade de manutenção;
- Possibilidade de testes automatizados;
- Histórico completo das alterações;
- Estrutura preparada para futura implantação via CI/CD ou IaC;
- Maior proximidade com práticas reais de desenvolvimento serverless;
- Nenhum custo de execução da Lambda neste projeto enquanto permanecer apenas em ambiente local/simulado.

### Mitigação:
Como a função não é efetivamente implantada neste projeto, as integrações com o Amazon Connect são representadas por contratos JSON e valores simulados, permitindo demonstrar a lógica de integração sem gerar consumo real de serviços tarifados.
