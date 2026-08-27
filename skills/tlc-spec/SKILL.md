---
name: tlc-spec
description: "Planeja features em Specify → Design → Tasks e produz um handoff fechado para o TLC Delivery. Use ao transformar uma demanda em requisitos testáveis, decisões de design e tarefas atômicas; não use para implementar código."
---

# TLC Spec

Transforme uma feature em uma entrega pronta para execução. Use quando a issue ainda precisa de requisitos, decisões de design ou decomposição. Encerre antes de escrever código.

## Escopo

Execute `Specify → Design → Tasks`, adaptando a profundidade à complexidade. Não faça checkout de repositório para alterar código, não crie branch, commit ou PR e não implemente nenhuma tarefa.

Os artefatos de produto pertencem à issue do Multica e aos seus comentários, nunca a arquivos de spec ou design commitados no repositório.

## Fluxo

1. Leia a issue inteira e os comentários relevantes. Se uma decisão humana for necessária, aplique `input-humano`, explique a pergunta, mova a issue para `blocked` e pare.
2. Escreva a especificação com requisitos identificáveis e critérios de aceite testáveis, preferencialmente em EARS (`Quando ... o sistema deve ...`). Declare pressupostos e o que está fora de escopo.
3. Registre apenas as decisões de design que afetam a implementação: componentes, dados, interfaces, invariantes, migrações, falhas e compatibilidade. Não invente arquitetura para mudanças simples.
4. Quebre a entrega em tarefas atômicas, ordenadas e verificáveis. Para cada tarefa, declare objetivo, arquivos ou áreas esperadas, testes, gate e dependências. Cada tarefa deve caber em um commit lógico.
5. Publique na issue um bloco `## Handoff para TLC Delivery` contendo: repositório-alvo, requisitos e critérios de aceite, decisões/invariantes, tarefas ordenadas, estratégia de teste, riscos, decisões adiadas e fora de escopo.
6. Antes do handoff, verifique que o Delivery conseguiria iniciar sem redescobrir produto ou arquitetura. Se faltar informação material, volte à especificação ou bloqueie para input humano.
7. Crie uma sub-issue de entrega atribuída a **TLC Delivery**. Copie para ela um link para a issue-pai e o bloco de handoff; declare o repositório-alvo explicitamente. Deixe a issue-pai em `in_progress` e a sub-issue pronta para iniciar.

## Limites

- Não implemente, não abra PR e não reescreva a decisão durante a entrega.
- Uma descoberta técnica que invalide a spec deve voltar como pergunta/risco para esta issue, não ser resolvida silenciosamente pelo Delivery.
- Responda no idioma do membro.
