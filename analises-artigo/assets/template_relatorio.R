# =====================================================================
# NN_relatorio.R — Esqueleto do gerador de conteúdo do relatório.
#
# Monta o JSON que os conversores transformam em .docx e .html.
# Nenhum número é escrito à mão: tudo vem dos .rds do pipeline.
# Toda afirmação qualitativa da prosa tem uma trava correspondente.
# =====================================================================
if (!require("pacman")) install.packages("pacman", repos = "https://cloud.r-project.org")
pacman::p_load(dplyr)
PROJ <- "<CAMINHO DA PASTA LOCAL DO PROJETO>"
setwd(PROJ)

# --- artefatos do pipeline -------------------------------------------
DESC  <- readRDS("desc.rds")
MOD   <- readRDS("modelo.rds")
D     <- readRDS("dados.rds")

# --- formatação numérica em português --------------------------------
# Nota: o `else` precisa ficar dentro das chaves. Solto no nível superior,
# o R fecha a expressão na linha do `if` e acusa "unexpected 'else'".
f <- function(x, d = 2) {
  if (is.null(x) || length(x) == 0 || is.na(x)) "—"
  else formatC(round(as.numeric(x), d), format = "f", digits = d, decimal.mark = ",")
}
f1 <- function(x) f(x, 1); f3 <- function(x) f(x, 3)
fa <- function(x, d = 3) f(abs(as.numeric(x)), d)   # módulo, p/ evitar sinal no corpo
fp <- function(p) {
  if (is.null(p) || is.na(p)) "—"
  else if (p < 0.001) "< 0,001"
  else sub("[.]", ",", formatC(round(p, 3), format = "f", digits = 3))
}
pe <- function(p) {
  if (is.null(p) || is.na(p)) "p = —"
  else if (p < 0.001) "p < 0,001"
  else paste0("p = ", fp(p))
}

# --- construtores de bloco -------------------------------------------
jq   <- function(s) { s <- as.character(s); s <- gsub('\\\\','\\\\\\\\',s)
                      s <- gsub('"','\\\\"',s); s <- gsub('\n','\\\\n',s); paste0('"',s,'"') }
jarr <- function(v) paste0('[', paste(vapply(v, jq, character(1)), collapse = ','), ']')
B <- list(); add <- function(x) B[[length(B)+1]] <<- x
p    <- function(...) add(paste0('{"type":"p","text":',  jq(paste0(...)), '}'))
h1   <- function(t)   add(paste0('{"type":"h1","text":', jq(t), '}'))
h2   <- function(t)   add(paste0('{"type":"h2","text":', jq(t), '}'))
h3   <- function(t)   add(paste0('{"type":"h3","text":', jq(t), '}'))
refp <- function(t)   add(paste0('{"type":"ref","text":',jq(t), '}'))
fig  <- function(path, cap, w = 15)
  add(paste0('{"type":"figure","path":', jq(path), ',"caption":', jq(cap), ',"width_cm":', w, '}'))
tbl  <- function(cap, header, rows, note = NULL) {
  rowsj <- paste0('[', paste(vapply(rows, jarr, character(1)), collapse = ','), ']')
  add(paste0('{"type":"table","caption":', jq(cap), ',"header":', jarr(header),
             ',"rows":', rowsj, if (!is.null(note)) paste0(',"note":', jq(note)) else '', '}')) }

# --- numeração automática --------------------------------------------
nt <- 0; nf <- 0
TAB <- function() { nt <<- nt + 1; paste0("Tabela ", nt) }
FIG <- function() { nf <<- nf + 1; paste0("Figura ", nf) }

# --- rótulos legíveis das variáveis ----------------------------------
lab <- c(var_a = "Nome apresentável de var_a",
         var_b = "Nome apresentável de var_b")
L <- function(v) if (v %in% names(lab)) unname(lab[[v]]) else gsub("_", " ", v)

# =====================================================================
# CORPO DO RELATÓRIO
# =====================================================================
h1("Resultados")
h2("Nome da análise")

tabn <- TAB()
p(sprintf("Conector inicial, investigou-se <o quê>, através de <procedimento>. Os resultados podem ser conferidos na %s e apontam <interpretação traduzida, com grupos e direção nomeados>.", tabn))
tbl(paste0(tabn, ". Título da tabela"),
    c("Coluna 1", "Coluna 2"),
    lapply(seq_len(nrow(DESC)), function(i) c(L(DESC$v[i]), f3(DESC$valor[i]))),
    "Nota. Explicação de cada abreviação usada na tabela.")

# --- exemplo do padrão das travas ------------------------------------
coef    <- MOD$std[MOD$std$op == "~", ]
sig     <- coef[coef$pvalue < 0.05, ]
n_sig   <- nrow(sig)
maior   <- sig$rhs[which.max(abs(sig$est.std))]

# A prosa abaixo afirma três coisas que os números não garantem sozinhos:
# quantos caminhos foram significativos, qual foi o maior, e que nenhum
# preditor do grupo Z alcançou significância. Cada uma vira uma asserção.
stopifnot(n_sig == 3,
          maior == "var_a",
          all(coef$pvalue[coef$rhs %in% grupo_z] >= 0.05))

p(sprintf("Entre os preditores examinados, três alcançaram significância, com o maior coeficiente em %s (β = %s, %s). Nenhum dos preditores do grupo Z foi significativo.",
  L(maior), f3(sig$est.std[sig$rhs == maior]), pe(sig$pvalue[sig$rhs == maior])))

# =====================================================================
h1("Referências")
for (r in sort(c(
  "Sobrenome, N. (ano). Título do trabalho. Periódico, vol(n), pp–pp."
))) refp(r)

# =====================================================================
json <- paste0('{"org":"multinivel","title":"Relatório de Análise de dados",',
               '"author":"<AUTOR>",',
               '"options":{"first_line_indent_cm":1.25,"space_after_pt":0},"blocks":[',
               paste(unlist(B), collapse = ','), ']}')
writeLines(enc2utf8(json), "conteudo.json", useBytes = TRUE)
# o .docx não incorpora vetores: a versão para Word aponta para o PNG
writeLines(enc2utf8(gsub('.svg"', '.png"', json, fixed = TRUE)),
           "conteudo_docx.json", useBytes = TRUE)
cat("OK_RELATORIO —", length(B), "blocos |", nt, "tabelas |", nf, "figuras\n")
