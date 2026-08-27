---
name: tlc-delivery
description: "Executa uma spec fechada do TLC Spec Pilot com TDD, testes, commits atômicos e PR. Use em uma sub-issue pronta para entrega; não use para discovery, requisitos ou redesenho de arquitetura."
---

# TLC Delivery

Implemente uma feature a partir de uma sub-issue com handoff fechado do TLC Spec. Use para executar tarefas prontas para entrega, abrir um PR e fornecer evidência de verificação.

## Pré-condição

Leia a issue de entrega e a issue-pai. Só inicie quando existirem: repositório-alvo, critérios de aceite testáveis, decisões/invariantes relevantes, tarefas ordenadas, estratégia de teste e limites de escopo.

Se qualquer item material estiver ausente ou contraditório, não faça discovery nem invente uma solução: comente a lacuna, aplique `input-humano` quando depender do membro, ou devolva a questão ao TLC Spec Pilot.

## Fluxo

1. Faça checkout apenas do repositório declarado no handoff. Leia as convenções e reconcilie a spec com o código existente; uma incompatibilidade material volta ao Spec Pilot.
2. Execute as tarefas na ordem definida. Use TDD por padrão: escreva ou ajuste o teste que demonstra o critério de aceite, faça-o falhar, implemente o mínimo necessário e rode o gate. Para bug ou regressão, diagnostique antes de propor a correção.
3. Mantenha um commit atômico por tarefa lógica e use Conventional Commits. Não enfraqueça, pule ou apague testes para obter verde.
4. Preserve o escopo e as decisões da spec. Uma mudança arquitetural, nova dependência, migração de risco ou requisito extra exige retorno ao Spec Pilot.
5. Antes de abrir o PR, execute a suíte e as verificações aplicáveis; confira o diff contra todos os critérios de aceite e contra o vazamento de português em código. Código, identificadores, nomes de testes, mensagens, migrations, branches, commits e PR são sempre em inglês.
6. Abra o PR sem fazer merge. Comente na sub-issue: link do PR, branch, commits, testes/gates executados, cobertura dos critérios de aceite, desvios aprovados e pendências. Mencione que está pronto para Code Review.

## Limites

- Não refaça Specify, Design ou Tasks; o seu trabalho é executar uma spec fechada.
- Não faça merge nem declare critério externo verificado sem evidência.
- Ao receber correções aceitas do Evaluate Code Review, aplique-as no mesmo PR seguindo este fluxo e reporte a nova evidência.
- Responda no idioma do membro.
