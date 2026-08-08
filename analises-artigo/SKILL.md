---
name: analises-artigo
description: Conduz análises de dados auditáveis para artigos, teses e relatórios, em R ou Python, sobre bases locais do computador ou bases públicas baixadas da internet (ENEM, SAEB, PNAD, DATASUS, Censo Escolar, PISA e afins). Monta o pipeline em scripts numerados que qualquer pessoa consegue reexecutar, com travas que fazem a geração falhar quando a prosa deixa de corresponder aos números, e produz o relatório de análise de dados em .docx e .html. Use sempre que o usuário mencionar rodar análises, montar pipeline, tratar ou limpar uma base, baixar microdados, refazer um modelo, trocar estimador ou tratamento de desfecho, gerar tabelas e figuras, ou escrever o relatório das análises. Vale também para pedidos que parecem pontuais — "só roda uma regressão", "confere esse número", "troca o modelo final" — porque o valor está em deixar o resultado reexecutável e o texto amarrado aos dados desde a primeira análise.
---

# Análises de dados auditáveis

Auditável quer dizer três coisas concretas: **outra pessoa consegue reexecutar** e chegar ao mesmo resultado; **cada número do texto tem origem rastreável** até um objeto do modelo; e **o texto falha em vez de mentir** quando uma decisão analítica muda.

A terceira é a menos óbvia e a mais valiosa. Em qualquer artigo empírico, decisões mudam: o desfecho vira binário, o estimador troca, um revisor pede outra especificação. Quando os números vivem digitados no texto, cada mudança custa um dia e deixa erros silenciosos — um beta desatualizado, um "apenas X foi significativo" que já não é verdade. A arquitetura aqui inverte a dependência: **o texto é uma função dos objetos do modelo**.

## Onde começar

Identifique em que ponto o usuário está antes de agir. Se já existe pipeline, não reconstrua. Se ele pede um número, entregue o número e ofereça o resto.

| Situação | Vá para |
|---|---|
| Base já no computador | `references/01-pipeline-r.md` ou `references/02-pipeline-python.md` |
| Base pública a baixar (ENEM, SAEB, PNAD, DATASUS...) | `references/04-bases-publicas.md` primeiro |
| Análises prontas, falta o relatório | `references/03-relatorio.md` |
| Algo quebrou e o erro é obscuro | `references/05-gotchas.md` |

**Estilo do relatório:** esta skill cuida da arquitetura e da geração. Se o projeto tiver um padrão de escrita definido — voz, citações por teste, formatação de tabelas —, acione a skill correspondente. Para os projetos da Multinível/NAOPARE, é `/relatorio-multinivel`.

## R ou Python

Pergunte ao usuário se ele tiver preferência; se não tiver, escolha pelo que a análise exige, não por gosto:

- **R** para modelagem estatística clássica e psicometria: equações estruturais (`lavaan`), análise fatorial, teoria de resposta ao item (`mirt`), redes psicométricas (`bootnet`, `qgraph`), modelos mistos (`lme4`), não paramétricos com tamanho de efeito (`rstatix`). O ecossistema é mais completo e as convenções de reporte são as que os periódicos esperam.
- **Python** para bases grandes e trabalho pesado de preparação: microdados públicos com milhões de linhas, junções de múltiplas fontes, leitura em blocos, dicionários de variáveis, séries temporais longas. `pandas`, `pyarrow`, `statsmodels`, `pingouin`, `scikit-learn`.

Misturar é comum e legítimo: preparar em Python, salvar em Parquet, modelar em R. Quando fizer isso, o script de preparação salva um artefato único e documentado, e o pipeline de modelagem parte dele.

Os princípios abaixo valem para as duas linguagens. O que muda é a sintaxe.

## Os seis princípios

**Scripts numerados, um artefato cada.** `00_prep` → `01_descritivas` → ... → `NN_relatorio`. Cada script lê os artefatos anteriores, salva o seu, imprime um `OK_<NOME>` no fim. Rodar do zero é rodar em ordem.

**Trabalhe em disco local; sincronize no fim.** Pastas de nuvem sincronizada são lentas e instáveis para leitura e escrita intermediária.

**Nenhum número escrito à mão no texto.** Se você digitou `β = 0,332` numa frase, está errado: escreva a interpolação que busca o valor no objeto.

**Trave as afirmações qualitativas.** Números interpolados se atualizam sozinhos; frases como "apenas", "todos", "nenhum", "três das quatro", "o maior coeficiente" não. Cada uma dessas precisa de uma asserção que derrube a geração quando deixar de valer:

```r
# a prosa afirma três caminhos significativos, nenhum deles do grupo Z
stopifnot(n_sig == 3, all(coef$pvalue[coef$rhs %in% grupo_z] >= 0.05))
```

```python
# a prosa afirma três coeficientes significativos, nenhum deles do grupo Z
assert n_sig == 3, f"a prosa afirma 3 significativos, encontrei {n_sig}"
assert (coef.loc[coef.termo.isin(grupo_z), "p"] >= 0.05).all()
```

Esta é a peça central. Quando a trava quebra, você descobriu que a mudança alterou a substância do achado, não só os decimais — que é exatamente o momento em que o texto precisa ser repensado, e exatamente o momento que passa despercebido sem ela.

**Parametrize o que pode mudar.** Tratamento do desfecho, estimador, categorização, conjunto de covariáveis: argumentos de função, nunca código duplicado. O teste é objetivo — trocar a decisão deve ser uma linha.

**Documente a proveniência do dado.** Para base local: caminho, data e o que foi filtrado. Para base pública: URL, órgão, ano de referência, data do download, tamanho do arquivo e verificação de integridade. Sem isso a análise não é reexecutável, por mais limpo que o código esteja.

## O arquivo de contexto

Mantenha um `CONTEXTO_<PROJETO>.md` atualizado **a cada decisão**, não no fim. É o que permite retomar o projeto depois de semanas ou passar para outra pessoa. Seções que se pagam: onde estão as coisas; ordem do pipeline e comando de build; estrutura atual do relatório; resultados-chave com números reais; decisões do autor a cumprir, numeradas e datadas, marcando as revogadas em vez de apagá-las; gotchas que custaram tempo; e pendências. Modelo em `assets/CONTEXTO_TEMPLATE.md`.

## Regras de honestidade analítica

**Nunca invente número.** Resultado vem da execução. Na ausência, use marcador explícito e diga que está faltando.

**Reporte o ajuste como ele é.** Índice fora do ponto de corte é declarado e qualificado no texto. Maquiar é o tipo de coisa que um revisor encontra e que derruba a confiança no resto do artigo.

**Coeficiente com sinal invertido em relação à correlação simples é supressão, não achado.** Não tem leitura substantiva. Reporte na tabela de sensibilidade com a ressalva, não construa argumento sobre ele, e prefira a especificação em que ele não aparece — ajuste equivalente não compensa carregar um caminho que não se pode interpretar.

**Alternativas descartadas viram linhas de tabela de sensibilidade, não código deletado.** O modelo que não venceu é a evidência de por que o vencedor venceu.

**Quando o usuário reverter uma decisão, reverta por inteiro:** script, prosa, travas, figuras, arquivo de contexto. Reversão pela metade é pior que nenhuma, porque deixa o texto afirmando algo que o modelo não produz mais.

## Incluídos

`assets/`
- `build_report.py`, `json2html.py` — JSON de conteúdo para `.docx` e `.html`
- `md2docx.py` — Markdown para `.docx`, útil para memorandos e notas técnicas
- `template_prep.R`, `template_relatorio.R` — esqueletos do primeiro e do último script do pipeline em R
- `CONTEXTO_TEMPLATE.md` — modelo do arquivo de handoff

`scripts/`
- `baixa_base_publica.py` — baixa, verifica integridade e registra a proveniência de uma base pública
- `perfila_base.py` — perfil rápido de qualquer base: tipos, ausentes, cardinalidade, candidatos a código de não-resposta
