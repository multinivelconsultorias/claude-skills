# Relatório de análise de dados

O último script do pipeline não escreve o relatório: ele escreve um **JSON de conteúdo**, e conversores transformam esse JSON em `.docx` e `.html`. A separação existe porque o texto precisa ser derivado dos objetos do modelo, e porque o mesmo conteúdo tem de sair em dois formatos sem divergir.

## O JSON de conteúdo

```json
{
  "org": "multinivel",
  "title": "Relatório de Análise de dados",
  "author": "Nome do autor",
  "options": {"first_line_indent_cm": 1.25, "space_after_pt": 0},
  "blocks": [
    {"type": "h1", "text": "Método"},
    {"type": "h2", "text": "Análise de dados"},
    {"type": "h3", "text": "Subseção"},
    {"type": "p",  "text": "Texto do parágrafo..."},
    {"type": "table", "caption": "Tabela 1. ...", "header": ["A","B"],
     "rows": [["1","2"]], "note": "Nota. ..."},
    {"type": "figure", "path": "saida_figuras/fig.svg", "caption": "Figura 1. ...", "width_cm": 15},
    {"type": "ref", "text": "Sobrenome, N. (ano). Título..."}
  ]
}
```

## Helpers de formatação numérica

O R escreve ponto decimal; o português usa vírgula. Defina os conversores uma vez no topo do gerador e use-os em toda parte:

```r
f <- function(x, d = 2) {
  if (is.null(x) || length(x) == 0 || is.na(x)) "—"
  else formatC(round(as.numeric(x), d), format = "f", digits = d, decimal.mark = ",")
}
f1 <- function(x) f(x, 1); f3 <- function(x) f(x, 3)
fa <- function(x, d = 3) f(abs(as.numeric(x)), d)          # valor absoluto
fp <- function(p) {
  if (is.na(p)) "—"
  else if (p < 0.001) "< 0,001"
  else sub("[.]", ",", formatC(round(p, 3), format = "f", digits = 3))
}
pe <- function(p) {
  if (is.na(p)) "p = —" else if (p < 0.001) "p < 0,001" else paste0("p = ", fp(p))
}
```

O `else` precisa ficar dentro das chaves. Solto no nível superior, o R fecha a expressão na linha do `if` e acusa `unexpected 'else'`. Use `[.]` em vez de `\\.` nos padrões, para não brigar com escapes quando o script for invocado por `Rscript -e`.

`fa()` existe porque muitos estilos evitam sinal negativo no corpo do texto: reporta-se o módulo e diz-se a direção por extenso ("0,227 em módulo, com sinal negativo").

## Numeração automática de tabelas e figuras

Nunca escreva "Tabela 4" à mão — inserir uma tabela no meio quebra tudo o que vem depois. Use contadores:

```r
nt <- 0; nf <- 0
TAB <- function() { nt <<- nt + 1; paste0("Tabela ", nt) }
FIG <- function() { nf <<- nf + 1; paste0("Figura ", nf) }

tabn <- TAB()
p(sprintf("Os resultados podem ser conferidos na %s.", tabn))
tbl(paste0(tabn, ". Título da tabela"), header, rows, nota)
```

## As travas

Este é o mecanismo que dá o nome "auditável" ao pipeline. Números gerados por `sprintf` se atualizam sozinhos quando a análise muda; **afirmações qualitativas não**. Frases com "apenas", "todos", "nenhum", "três das quatro", "o maior" continuam ali, agora falsas.

Para cada uma dessas frases, escreva a asserção correspondente imediatamente antes ou depois, com um comentário dizendo o que a prosa afirma:

```r
# travas da prosa: humor em três das quatro estimações, somáticos em duas,
# decréscimo em uma e nenhuma subescala do DASS-21 em qualquer delas
stopifnot(conta_sig("Humor") == 3, conta_sig("Somaticos") == 2,
          conta_sig("Decrescimo") == 1, sum(vapply(dass3, conta_sig, numeric(1))) == 0)
```

Quando uma trava quebra, a geração falha e você descobriu que a mudança alterou a substância do achado, não só os decimais. É exatamente o momento em que o texto precisa ser repensado — e é o momento que, sem trava, passa despercebido.

Vale a pena travar: contagens de caminhos significativos; a identidade do maior ou menor coeficiente; sinais; comparações entre modelos ("o ajuste piorou"); e qualquer "nenhum" ou "todos".

## Build

Rode com o diretório de trabalho na pasta do projeto. Se rodar de outro lugar, as figuras somem do `.docx` **sem erro algum** — o arquivo é gerado, só que sem imagens.

```bash
python3 -c "import os,sys,runpy; os.chdir('<PASTA>'); \
  sys.argv=['json2html.py','conteudo.json','relatorio.html']; runpy.run_path('json2html.py',run_name='__main__'); \
  sys.argv=['build_report.py','conteudo_docx.json','relatorio.docx']; runpy.run_path('build_report.py',run_name='__main__')"
```

## Dois JSONs quando houver vetor

O Word não incorpora SVG. O HTML fica melhor com SVG. A solução é gerar o JSON uma vez e derivar o segundo por substituição:

```r
writeLines(enc2utf8(json), "conteudo.json", useBytes = TRUE)
json_docx <- gsub('.svg"', '.png"', json, fixed = TRUE)
writeLines(enc2utf8(json_docx), "conteudo_docx.json", useBytes = TRUE)
```

Isso exige que cada figura seja salva nos dois formatos, com o mesmo nome base.

## Verificação depois do build

Confira programaticamente, não visualmente:

```python
import zipfile, unicodedata, re
z = zipfile.ZipFile("relatorio.docx")
xml = unicodedata.normalize("NFC", z.read("word/document.xml").decode("utf8"))
print("figuras:", [n for n in z.namelist() if n.startswith("word/media/")])
print("mojibake:", "Ã" in xml)
print("recuo 1,25cm:", xml.count('w:firstLine="709"'))
```

Atenção ao comparar texto: o macOS costuma produzir Unicode decomposto (NFD), então `"dicotômico" in xml` pode dar falso negativo. Normalize para NFC antes de procurar.

## Opções de formatação

O bloco `options` controla o corpo do documento. As mais pedidas:

| Opção | Efeito |
|---|---|
| `first_line_indent_cm` | recuo de primeira linha dos parágrafos de corpo |
| `space_after_pt` | espaçamento depois de cada parágrafo (0 para o padrão APA com recuo) |
| `block_gap_pt` | separação entre blocos (títulos, tabelas, figuras) e o texto ao redor |
| `line_spacing`, `body_size_pt`, `margins_cm`, `justify` | o resto |

`block_gap_pt` é separado de `space_after_pt` de propósito: zerar o espaçamento entre parágrafos é uma escolha tipográfica comum, mas grudar um título no parágrafo anterior nunca é. Se o autor pedir "sem espaçamento entre parágrafos", aplique a `space_after_pt` e preserve `block_gap_pt`, explicando a distinção.
