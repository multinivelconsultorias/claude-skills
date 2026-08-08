# =====================================================================
# 00_prep.R — Leitura da base bruta e derivação das variáveis do estudo.
#
# Este é o único script que toca a base bruta. Tudo o que vem depois lê
# o .rds gerado aqui. Isso garante que nenhuma análise dependa de uma
# transformação feita ad hoc no meio do caminho.
#
# Registre neste cabeçalho toda decisão de derivação que não seja óbvia:
# pontos de corte, agrupamento de categorias, tratamento de ausentes,
# e a regra de qualquer variável derivada de texto livre.
# =====================================================================
if (!require("pacman")) install.packages("pacman", repos = "https://cloud.r-project.org")
pacman::p_load(dplyr, readxl)
PROJ <- "<CAMINHO DA PASTA LOCAL DO PROJETO>"
setwd(PROJ); set.seed(2026)

d <- read_excel("<base bruta>.xlsx")
cat("Base bruta:", nrow(d), "x", ncol(d), "\n")

# --- escores dos instrumentos ----------------------------------------
# Some ou faça a média dos itens conforme o manual do instrumento, e
# deixe explícito qual dos dois, porque isso muda os pontos de corte.

# --- variáveis categóricas do modelo ---------------------------------
# Agrupamentos de categorias entram aqui, com o motivo no comentário.
# Deixe registrado qual é a categoria de referência de cada uma.

# --- variáveis derivadas de texto livre ------------------------------
# Regras de expressão regular sobre respostas abertas erram grafias e
# casos-limite. Crie a versão corrigida ao lado da original, compare, e
# registre quantos casos mudam. Não substitua uma pela outra em silêncio.
#
# d$origem      <- grepl("padrao1|padrao2", tolower(d$campo_aberto))
# d$origem_corr <- grepl("padrao1|padrao2|variante", tolower(d$campo_aberto))
# cat("Casos reclassificados:", sum(d$origem != d$origem_corr, na.rm = TRUE), "\n")

# --- conferências antes de salvar ------------------------------------
# Imprima as distribuições das variáveis do modelo. É aqui que aparecem
# categorias com n pequeno demais, ausentes inesperados e códigos de
# não-resposta que passaram como valores válidos.
# for (v in vars_modelo) { cat("\n==", v, "\n"); print(table(d[[v]], useNA = "ifany")) }

saveRDS(d, "dados.rds")
cat("\nOK_PREP —", nrow(d), "x", ncol(d), "\n")
