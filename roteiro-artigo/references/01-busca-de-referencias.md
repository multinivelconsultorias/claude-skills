# Varredura de referências

## Ordem, da mais barata à mais cara

**(1) O que o autor já escreveu.** Artigos anteriores, tese, projeto, revisões de escopo, relatórios. Extraia as listas de referências e cruze com os blocos temáticos do roteiro. Autores maduros costumam já ter metade do que precisam e não se lembram disso — num caso real, os dois artigos anteriores da tese continham doze das quatorze referências que a introdução do terceiro exigia.

**(2) O corpus local do projeto.** Geralmente uma pasta de PDFs. Converta tudo em texto e mapeie o vocabulário antes de ler qualquer coisa:

```bash
python3 scripts/extrai_corpus.py "<pasta com PDFs>" "<saída>"
cd "<saída>"
for f in *.txt; do echo "== $f"; \
  grep -oiE "termo1|termo2|termo3" "$f" | sort | uniq -c | sort -rn | head; done
```

Isso diz em minutos quais fontes têm o que interessa e evita ler 177 páginas de um livro para descobrir que o capítulo útil tem três.

**(3) Busca externa.** Só agora, porque agora você sabe o que falta.

## Onde buscar

| Fonte | Serve para | Acesso |
|---|---|---|
| **OpenAlex** | varredura ampla, filtro por ano, status de acesso aberto, contagem de citações | API livre, sem chave — use `scripts/busca_openalex.py` |
| **PubMed / Europe PMC** | saúde, psicologia clínica, epidemiologia | livre; PMC tem texto completo |
| **SciELO** | literatura latino-americana, artigos em português | integralmente aberto |
| **LILACS / BVS** | saúde na América Latina, inclusive literatura cinzenta | livre |
| **DOAJ** | só periódicos de acesso aberto | livre |
| **Crossref** | conferir metadado e DOI | API livre |
| **Google Scholar** | cobertura ampla, "citado por" | sem API; use busca web |
| **PsyArXiv, SocArXiv, medRxiv** | preprints, o que ainda não saiu | livre |
| **Unpaywall** | achar versão aberta de artigo pago | API livre |

Para literatura brasileira em psicologia, saúde coletiva e educação, **SciELO e LILACS costumam render mais que a OpenAlex**, porque indexam periódicos nacionais que os catálogos internacionais cobrem mal. Quando o artigo for sobre um fenômeno brasileiro, comece por elas.

## Como consultar a OpenAlex sem se enganar

O `scripts/busca_openalex.py` exige, por padrão, que **todas** as palavras da consulta apareçam no título ou no resumo. Isso dá precisão alta e um recall que despenca depressa. Os números abaixo foram medidos, não estimados:

| Consulta | Resultados | Qualidade |
|---|---|---|
| `forced relocation mental health` | 93 | o artigo mais pertinente em primeiro lugar |
| `forced relocation disaster mental health` | 13 | quase todos fora do tema |
| `involuntary resettlement psychological distress` | 0 | vocabulário que a literatura não usa |
| `solastalgia` | 309 | conceito único, excelente |

**Duas a quatro palavras por consulta, e várias consultas estreitas em vez de uma longa.** Zero resultado quase nunca significa que não existe literatura: significa que você usou um vocabulário que o campo não usa. Troque por sinônimos antes de concluir qualquer coisa.

O modo `--amplo` busca no texto todo e ordena por relevância, mas a relevância da OpenAlex é puxada pela contagem de citações — relatórios do Lancet sobem ao topo de quase qualquer consulta de saúde. Use só quando o modo padrão não devolver nada.

## Estratégia de busca

**Busque em duas línguas.** Um mesmo tema tem literaturas paralelas em português e inglês que quase não se citam. Para fenômenos brasileiros, a produção nacional costuma ser a mais pertinente e a menos encontrável por termo em inglês.

**Varie o nível de abstração.** Três camadas, do específico ao geral: o fenômeno exato ("subsidência", "realocação forçada"), a classe do fenômeno ("desastre tecnológico", "deslocamento involuntário") e o mecanismo ("apego ao lugar", "apoio social como amortecedor"). A camada do meio costuma ser a mais produtiva e a que se esquece.

**Procure revisões e meta-análises primeiro.** Uma revisão recente entrega o estado do campo, as referências fundadoras e as lacunas declaradas, tudo de uma vez. Filtre por `--tipo review` e ordene por ano.

**Procure a referência que quase fez o mesmo.** O achado mais valioso de uma varredura é o estudo que mediu o efeito, não conseguiu explicar o mecanismo e **disse isso explicitamente**. Ele entrega a melhor posição argumentativa possível: o parágrafo termina na frase em que os autores declaram o que não puderam medir, e o seguinte abre dizendo que é isso que este estudo faz. Para encontrá-los, busque por expressões como "could not identify the mechanism", "we were unable to measure", "future research should examine", "remains unclear".

## A regra dos 70%

Cerca de 70% das referências devem ser dos últimos cinco anos. Ao montar a lista, classifique cada item:

- **Recente e substituível** — a maioria. Se sair uma revisão mais nova, troca.
- **Antiga e insubstituível** — a escala original, o trabalho que criou o construto, o marco teórico. Fica.
- **Antiga e substituível** — o alvo. Procure a versão recente do mesmo argumento.

Um teste rápido para a terceira categoria: pegue a referência antiga, busque quem a citou nos últimos cinco anos e veja se algum desses trabalhos faz o mesmo serviço com dados novos.

Informe a proporção alcançada na entrega. Quando não chegar a 70%, diga em quais blocos e por quê.

## Marcação de acesso

Na entrega, marque cada referência:

- `[OA]` acesso aberto, com o link do PDF quando houver
- `[$]` fechado
- `[pre]` preprint, ainda sem revisão por pares

Preprint é citável, mas o autor precisa saber que é preprint, porque alguns periódicos restringem e porque a versão publicada pode divergir. Quando um trabalho fechado for incontornável, inclua e sinalize — a decisão de buscar pelo acesso institucional é do autor.

## Verificação

Confirme autores, ano, periódico, volume e páginas **na fonte**, não no catálogo: metadado de catálogo tem erro de paginação e de nome com frequência. Quando o editor bloquear o acesso — acontece muito —, entregue com a pendência marcada em vez de completar por inferência.

Nunca reconstrua uma referência de memória sem avisar que foi isso que você fez. E nunca atribua um achado específico a um trabalho cujo texto você não leu: título e resumo autorizam dizer sobre o que ele trata, não o que ele encontrou.
