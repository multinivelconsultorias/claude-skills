---
name: roteiro-artigo
description: Monta o roteiro das seções teóricas de um artigo e faz a varredura de referências que as sustenta, privilegiando literatura dos últimos cinco anos (cerca de 70% do conjunto) e artigos em acesso aberto, sem descartar os pagos quando forem incontornáveis. Constrói o roteiro tanto a partir de resultados estatísticos, em artigos quantitativos, quanto a partir das perguntas de pesquisa e dos eixos temáticos, em artigos qualitativos, e cobre Introdução e Discussão — que exigem estratégias de busca diferentes. Use sempre que o usuário mencionar introdução, discussão, referencial teórico, estado da arte, roteiro do artigo, buscar ou atualizar referências, achar a lacuna, "o que já existe sobre isso", justificar o estudo, comparar meus achados com a literatura, ou quando pedir ajuda para transformar resultados prontos em texto. Vale também quando o pedido parecer só bibliográfico ("me acha uns artigos sobre X"), porque o valor está em amarrar cada referência a uma função específica no argumento.
---

# Roteiro e referências

Um roteiro não é uma lista de temas: é o esqueleto do argumento, parágrafo a parágrafo, com a função de cada um e a referência que o sustenta. A Introdução existe para tornar os resultados previsíveis; a Discussão, para situá-los. Quem termina a Introdução deve conseguir antecipar quais hipóteses serão testadas e por que a análise tem a forma que tem.

Por isso o roteiro se escreve **de trás para frente**: a partir dos resultados, em artigos quantitativos, ou das perguntas e eixos temáticos, em qualitativos.

## Fluxo

1. **Enuncie a tese em uma frase.** A única coisa que o leitor precisa aceitar. Ela sai da leitura honesta do material, inclusive das partes fracas. Se não for defensável a partir do que se tem, o problema está no artigo, e é isso que se deve dizer ao autor.
2. **Varra as fontes**, da mais barata à mais cara: o que o autor já escreveu, o corpus local do projeto, e só então a busca externa. Ver `references/01-busca-de-referencias.md`.
3. **Verifique a lacuna antes de afirmá-la.** Procure ativamente o estudo mais próximo do que o autor fez. Se existir, a lacuna fica mais estreita e mais forte, e aquele estudo vira citação obrigatória.
4. **Monte o mapa parágrafo a parágrafo.** Introdução em `references/02-roteiro-introducao.md`; Discussão em `references/03-roteiro-discussao.md`.
5. **Entregue com as pendências de verificação explícitas.**

## As duas metas quantitativas

**Cerca de 70% das referências dos últimos cinco anos.** Não é regra de estilo: é o que sinaliza a um editor que o artigo conhece o estado atual do campo. Os 30% restantes existem para o que não envelhece — o trabalho que criou o construto, a escala original, o marco teórico, a meta-análise que ainda é a melhor síntese disponível. Se você não consegue justificar por que uma referência antiga está ali, ela provavelmente deveria ser substituída por uma recente.

Ao entregar, informe a proporção alcançada. Quando não chegar a 70%, diga em quais blocos a literatura recente é escassa — às vezes é sinal de que o tema é maduro, às vezes de que a busca ficou estreita demais.

**Priorize acesso aberto, mas não o transforme em critério de qualidade.** Referência que o autor consegue baixar é referência que ele consegue ler antes de citar, e citar sem ler é como erro entra em artigo. Marque cada item na entrega: `[OA]` aberto, `[$]` pago, `[pre]` preprint. Quando um trabalho fechado for incontornável — costuma ser a meta-análise central ou o estudo mais próximo do artigo —, inclua e sinalize, para que o autor decida se busca pelo acesso institucional.

## Densidade e tamanho

Uma referência por parágrafo é boa densidade. Para uma introdução de 12 a 15 parágrafos, de 10 a 15 referências. Discussões tendem a precisar de mais, porque cada achado pede pelo menos um ponto de comparação.

Cada bloco do roteiro deve terminar amarrado a algo específico do artigo. Se você não consegue dizer qual resultado ou qual pergunta o parágrafo prepara, ele não deveria estar ali.

## Quantitativo e qualitativo

Em artigos **quantitativos**, o roteiro parte dos resultados: cada bloco da Introdução prepara uma hipótese, e cada seção da Discussão confronta um achado com a literatura. O que organiza é a cadeia de inferência.

Em artigos **qualitativos**, parte das perguntas de pesquisa e dos eixos que emergiram do material: cada bloco da Introdução constrói a pertinência de uma pergunta, e a Discussão põe cada eixo temático em diálogo. O que organiza é a construção do objeto. Muda o vocabulário — não "hipótese sustentada" e sim "eixo que dialoga com", não "tamanho de efeito" e sim "convergência ou tensão com o que a literatura descreve" —, mas a arquitetura do roteiro é a mesma.

## Regras de honestidade bibliográfica

**Nunca invente uma referência, um DOI ou uma página.** Um dado bibliográfico inventado é indistinguível de um verdadeiro até alguém tentar buscá-lo, e aí compromete o artigo inteiro. Quando não conseguir confirmar volume ou paginação, entregue assim mesmo e marque a pendência — lacuna assumida é sempre melhor que preenchimento por inferência.

**Não afirme o conteúdo de um trabalho que você não leu.** Título e resumo autorizam dizer sobre o que ele trata; não autorizam atribuir-lhe um achado específico. Quando a informação vier de um resumo, diga isso ao autor.

**Confira a coerência interna do documento:** citação no texto sem entrada na lista, entrada sem citação, divergência de ano entre uma e outra. É rápido e pega erros que passariam pela revisão.

## Restrições de linguagem

Alguns projetos têm embargos — jurídicos, institucionais, de acordo com financiador — que limitam o que o texto pode afirmar. Quando houver, registre no roteiro: o vocabulário proibido, o substituto e o princípio por trás. Ver `references/04-restricoes-de-linguagem.md`.

## Incluídos

`scripts/`
- `busca_openalex.py` — busca no catálogo aberto da OpenAlex, com filtro de recência e marcação de acesso aberto. Serve para descobrir o que existe; não substitui a leitura nem a conferência na fonte.
- `extrai_corpus.py` — extrai o texto de todos os PDFs de uma pasta e sinaliza os digitalizados sem OCR, que são invisíveis a qualquer busca por palavra-chave.

`assets/`
- `ROTEIRO_TEMPLATE.md` — estrutura da entrega
- `md2docx.py` — converte o roteiro para `.docx`, para o autor anotar no Word
