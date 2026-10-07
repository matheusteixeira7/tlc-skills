---
name: projetos-catadores-editais
description: Elabora projetos de captação de recursos para cooperativas e associações de catadores de materiais recicláveis em editais privados (fundações, institutos empresariais, programas de ESG e logística reversa), lendo o PDF do edital, conferindo cada seção com a legislação de resíduos (PNRS Lei 12.305/2010, Decreto 10.936/2022, leis de cooperativas, NRs) e gerando o projeto final em Word (.docx). Use quando o usuário disser coisas como "escrever projeto para edital", "projeto para cooperativa de catadores", "proposta para fundação/instituto", "projeto de reciclagem para captar recurso", "monta o projeto desse edital", "galpão de triagem", "prensa/caminhão para a cooperativa" ou enviar um PDF de edital ligado a reciclagem ou resíduos. NÃO use para PGRS, PGRSS, PGRCC ou PMGIRS (planos de gerenciamento), projetos de engenharia de aterro, nem para editais públicos/convênios (FUNASA, Transferegov, emendas parlamentares).
license: CC-BY-4.0
metadata:
  author: Jailson
  version: 1.0.0
---

# Projetos para Cooperativas de Catadores em Editais Privados

Transforma um edital privado (PDF) + dados de uma cooperativa/associação de catadores em um projeto completo, aderente ao edital e à legislação, entregue em `.docx`.

## Regras críticas (leia antes de tudo)

1. **O edital é a regra principal.** A maioria das reprovações vem de requisito do edital esquecido (seção obrigatória, limite de caracteres, despesa vedada, anexo faltando), não de falta de citação legal. Tudo começa e termina na matriz do edital (Passo 1 e Passo 6).
2. **Nunca invente dados da cooperativa.** Número de cooperados, toneladas/mês, renda média, dados do município, valores de orçamento: se o usuário não informou, escreva `[PREENCHER: o que falta]`. Um número inventado num projeto de captação é pior que uma lacuna, porque pode desclassificar a proposta ou gerar problema na prestação de contas.
3. **Cite só normas que estão em `references/legislacao.md`.** Nunca gere número de artigo, inciso ou data de memória. Se precisar de uma norma que não está no arquivo, escreva `[CONFERIR NORMA: assunto]` e avise o usuário. Artigo errado em projeto técnico destrói a credibilidade da proposta.
4. **Escreva em português do Brasil**, tom técnico mas acessível. O avaliador de edital privado geralmente não é jurista: lei serve para mostrar alinhamento e conformidade, não para encher texto.

## Fluxo de trabalho

### Passo 1: Ler o edital e montar a matriz de requisitos

Leia o PDF inteiro com a ferramenta de leitura (em PDFs longos, leia por faixas de páginas). Extraia e mostre ao usuário uma tabela com:

| Item | O que extrair |
| --- | --- |
| Proponente elegível | Quem pode concorrer (cooperativa, associação, tempo mínimo de CNPJ, faturamento máximo) |
| Valor e prazo | Valor mínimo/máximo por projeto, duração máxima, data-limite de envio |
| Seções obrigatórias | Lista exata, na ordem e com os nomes que o edital usa |
| Limites | Caracteres ou páginas por seção/campo |
| Critérios de avaliação | Cada critério com peso/pontuação |
| Despesas permitidas e vedadas | Itens financiáveis, vedações, teto por rubrica, contrapartida exigida |
| Anexos e documentos | Tudo que precisa ir junto |
| Temas prioritários | Gênero, raça, juventude, território, clima, inovação etc. |

Resultado esperado: a matriz preenchida. Itens que o edital não menciona ficam como "não especificado". Não siga em frente sem essa matriz: ela é o checklist do Passo 6.

### Passo 2: Coletar os dados da cooperativa

Pergunte de uma vez só (em lista curta) o que faltar. Aceite respostas parciais.

- Nome, CNPJ, cidade/UF, ano de fundação, forma jurídica (cooperativa ou associação)
- Número de cooperados/associados, % de mulheres, % de pessoas negras, faixa etária
- Volume triado por mês (t/mês), principais materiais, renda média mensal por cooperado
- Infraestrutura atual: galpão (próprio, cedido, alugado), equipamentos, veículos
- Parcerias: contrato com a prefeitura para coleta seletiva? Acordos de logística reversa? Compradores?
- Problema principal que o projeto resolve e o que será comprado/feito com o recurso
- Situação documental (ver checklist de habilitação em `references/secoes-projeto.md`)

Se o usuário não souber algo, siga com `[PREENCHER: ...]`. Não trave o fluxo.

### Passo 3: Mapear a legislação aplicável

Leia `references/legislacao.md`. Ele está organizado pela seção do projeto onde cada norma entra (justificativa, governança, segurança do trabalho, orçamento etc.). Selecione só o que tem relação com o que o projeto propõe. Exemplos:

- Comprar prensa ou esteira → normas de segurança de máquinas e EPI na metodologia e no orçamento.
- Ampliar coleta seletiva com a prefeitura → artigos da PNRS sobre integração de catadores e dispensa de licitação.
- Venda de créditos de logística reversa → decreto dos certificados de crédito de reciclagem.

Resultado esperado: uma lista curta "norma → em qual seção será citada → por quê".

### Passo 4: Escrever o projeto

Leia `references/secoes-projeto.md` para o roteiro de cada seção, banco de indicadores e alinhamento com ODS. Regras:

- Use **exatamente** os nomes e a ordem de seções do edital. Se o edital não definir, use a estrutura padrão do arquivo de referência.
- Responda aos critérios de avaliação de forma explícita: cada critério de peso alto precisa de pelo menos um parágrafo que o atenda de forma visível.
- Metas sempre mensuráveis (número + unidade + prazo). Ex.: "ampliar a triagem de 18 t/mês para 30 t/mês até o mês 12".
- Orçamento só com rubricas permitidas pelo edital; marque contrapartida separadamente.
- Escreva o rascunho em Markdown num arquivo `projeto-<cooperativa>.md` no diretório de trabalho, com cada seção como `## Título da seção`. Tabelas em Markdown para cronograma e orçamento.

### Passo 5: Conferir limites de caracteres

Se o edital tiver limites, crie um JSON `{"Título da seção": limite}` e rode:

```bash
python3 "<pasta desta skill>/scripts/checar_limites.py" projeto-<cooperativa>.md limites.json
```

O script conta caracteres com espaços por seção `##` (o padrão da maioria dos formulários) e aponta o que estourou. Corte o texto até tudo passar. Se o edital contar sem espaços, use `--sem-espacos`.

### Passo 6: Revisão de conformidade

Confira o rascunho contra:

1. **A matriz do Passo 1**: cada seção obrigatória existe? Cada critério de avaliação foi atendido? Nenhuma despesa vedada no orçamento? Contrapartida presente se exigida?
2. **Checklist legal** (fim de `references/legislacao.md`): segurança do trabalho, proibição de trabalho infantil, LGPD para dados dos cooperados, governança cooperativista.
3. **Placeholders**: liste todos os `[PREENCHER: ...]` e `[CONFERIR NORMA: ...]` restantes.

Resultado esperado: uma tabela "requisito → atendido? → onde no texto" e a lista de pendências.

### Passo 7: Gerar o .docx

```bash
python3 "<pasta desta skill>/scripts/gerar_docx.py" projeto-<cooperativa>.md projeto-<cooperativa>.docx
```

`<pasta desta skill>` é o diretório onde este SKILL.md está. O script não precisa de nenhuma biblioteca externa. Ele converte títulos (`#` vira título do documento, `##` seção, `###` subseção), parágrafos, listas, **negrito**, *itálico* e tabelas Markdown simples. Depois de gerar, confira que o arquivo abre com `textutil -convert txt projeto-<cooperativa>.docx -stdout | head` (macOS).

Entregue ao usuário: o caminho do `.docx`, a tabela de conformidade do Passo 6 e a lista de pendências.

## Exemplos

### Exemplo 1: edital completo, dados quase todos

Usuário diz: "Segue o edital do Instituto X. Projeto para a Coopervida de Juiz de Fora, 42 cooperados, querem uma prensa e uma balança."
Ações:
1. Lê o PDF e monta a matriz (ex.: limite de R$ 150 mil, 5 seções, 2.000 caracteres cada, veda reforma de imóvel).
2. Pergunta só o que falta: volume mensal, renda média, situação do galpão.
3. Seleciona normas: PNRS (integração de catadores), NR-12 (máquinas), NR-6 (EPI), leis de cooperativas.
4. Escreve as 5 seções com os nomes do edital, orçamento com prensa, balança, EPI e capacitação em NR-12.
5. Roda `checar_limites.py` e corta o que passou de 2.000 caracteres.
6. Revisão de conformidade e gera o `.docx`.
Resultado: `projeto-coopervida.docx` + tabela de conformidade + pendências (ex.: `[PREENCHER: renda média atual]`).

### Exemplo 2: só a ideia, sem edital ainda

Usuário diz: "Quero adiantar um projeto de caminhão para a associação de catadores de Maricá, ainda não tenho o edital."
Ações: pula o Passo 1, avisa que a estrutura será a padrão e precisará ser adaptada ao edital, coleta dados e escreve com a estrutura de `references/secoes-projeto.md`.
Resultado: projeto-base em `.docx` pronto para ser adaptado quando o edital sair.

### Exemplo 3: adaptar projeto existente para novo edital

Usuário diz: "Adapta esse projeto que já escrevi para o edital da Fundação Y" (envia o .docx/.md antigo e o PDF).
Ações: monta a matriz do novo edital, reorganiza o texto antigo nas seções do novo edital, corta para os novos limites, refaz a revisão de conformidade.
Resultado: novo `.docx` + lista do que o edital novo pede e o projeto antigo não tinha.

## Problemas comuns

### O PDF do edital não abre ou vem sem texto (escaneado)
Causa: PDF de imagem. Solução: leia as páginas como imagem com a ferramenta de leitura. Se ainda assim estiver ilegível, peça ao usuário para colar o texto das seções de requisitos e critérios.

### O edital tem formulário online e não aceita .docx
Gere o `.docx` mesmo assim (serve de arquivo de trabalho) e entregue também o texto de cada campo separado no chat, com a contagem de caracteres.

### `checar_limites.py` diz que uma seção não foi encontrada
Causa: o título `##` no Markdown está diferente da chave no JSON. Solução: use exatamente o mesmo texto nos dois.

### O usuário pede uma norma que não está em `references/legislacao.md`
Não cite de memória. Marque `[CONFERIR NORMA: ...]`, diga ao usuário qual fonte oficial consultar (planalto.gov.br, in.gov.br) e, se houver ferramenta de busca disponível, verifique antes de incluir.
