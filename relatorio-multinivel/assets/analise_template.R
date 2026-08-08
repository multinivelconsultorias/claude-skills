# =============================================================================
# analise_template.R — Esqueleto de análise no fluxo Multinível / NAOPARE
# Adapte os nomes das colunas e selecione apenas os blocos do seu delineamento.
# Exporta tabelas (.csv) e figuras (.png) para montar o relatório.
# =============================================================================
#
# ÁRVORE DE DECISÃO DO DELINEAMENTO (resumo do estilo do autor):
#   Descrever amostra ............... frequência/% (categóricas); M, Mdn, DP, quartis, min, max (numéricas)
#   Numérica: normalidade ........... Shapiro-Wilk (Miot, 2017) -> assimétrica => não-paramétrico
#   2 grupos indep. ................. Mann-Whitney (Brunner et al., 2018) | t de Student se normal
#   3+ grupos indep. ................ Kruskal-Wallis + Dunn/Holm (Pohlert, 2014) | ANOVA + post hoc Holm (Chen, Feng & Yi, 2017) se normal
#   Pareado/repetido (2) ............ Wilcoxon signed-rank
#   Longitudinal/misto .............. nparLD (Noguchi et al., 2012)
#   Categórica x categórica ......... Qui-quadrado/Fisher (Kim, 2017) + resíduos >=1,96 (Sharpe, 2015) + V de Cramér (Serdar et al., 2021)
#   Correlação ...................... Pearson | Spearman conforme normalidade (Miot, 2018)
#   Regressão linear/múltipla ....... lm; B e Beta; F, R², AIC, BIC (Field, 2020)
#   Moderação (amostra pequena) ..... estratificar pelo moderador (subgrupos), não termo de interação
#   Estrutura interna (escala) ...... AFE (Damásio, 2012) -> AFC/MEE lavaan WLSMV -> CI (psych) -> TRI mirt (Samejima, 1969) -> invariância (Cheung & Rensvold, 2002)
# =============================================================================

# ---- 0. Pacotes -------------------------------------------------------------
if (!require("pacman")) install.packages("pacman")
pacman::p_load(
  tidyverse, readxl, haven,          # leitura + manipulação
  psych,                              # descritiva, AFE, confiabilidade
  car, rstatix, effectsize,          # pressupostos + tamanho de efeito
  PMCMRplus, FSA, nparcomp, nparLD,   # não-paramétrica + post hoc
  rcompanion, vcd,                    # V de Cramér
  ggpubr, patchwork                   # gráficos
  # lavaan, semTools, semPlot, MVN,   # (descomente p/ AFC/SEM)
  # mirt,                             # (descomente p/ TRI)
  # qgraph, bootnet, EGAnet           # (descomente p/ redes)
)

# ---- 0.1 Tema gráfico Multinível -------------------------------------------
tema_multinivel <- function(base_size = 12) {
  theme_minimal(base_family = "Times New Roman", base_size = base_size) +
    theme(panel.grid.minor = element_blank(),
          panel.grid.major.x = element_blank(),
          axis.line = element_line(color = "grey30"),
          plot.title = element_text(face = "bold"),
          plot.caption = element_text(color = "grey40", hjust = 0),
          legend.position = "bottom")
}
PAL <- c("#2C5F6F", "#C0703A", "#6E8B3D", "#8C4A5F", "#4F6D7A")
dir.create("saida_tabelas", showWarnings = FALSE)
dir.create("saida_figuras", showWarnings = FALSE)
salvar_fig <- function(nome) ggsave(file.path("saida_figuras", nome),
                                    width = 16, height = 10, units = "cm", dpi = 300)

# ---- 1. Carregar a base -----------------------------------------------------
# dados <- read_xlsx("dados.xlsx")          # Excel
# dados <- read_csv2("dados.csv")           # CSV pt-BR (; e ,)
# dados <- read_sav("dados.sav")            # SPSS
glimpse(dados)

# Defina grupos/desfechos (AJUSTE):
# grupo  <- "Grupo"                         # variável de agrupamento
# numericas  <- c("escore1", "escore2")     # desfechos numéricos
# categoricas <- c("sexo", "escolaridade")  # variáveis categóricas

# ---- 2. Descritivas ---------------------------------------------------------
desc_num <- psych::describe(dados[ , numericas, drop = FALSE])
write.csv(desc_num, "saida_tabelas/descritiva_numericas.csv", fileEncoding = "UTF-8")

freq_cat <- map_dfr(categoricas, function(v) {
  dados %>% count(.data[[v]]) %>%
    mutate(variavel = v, pct = round(100 * n / sum(n), 1)) %>%
    rename(categoria = 1)
})
write.csv(freq_cat, "saida_tabelas/frequencias_categoricas.csv",
          row.names = FALSE, fileEncoding = "UTF-8")

# ---- 3. Normalidade (Shapiro-Wilk) -----------------------------------------
norm_tab <- map_dfr(numericas, function(v) {
  x <- dados[[v]]; sw <- shapiro.test(x)
  tibble(variavel = v, W = round(unname(sw$statistic), 3),
         p = signif(sw$p.value, 3),
         distribuicao = ifelse(sw$p.value < 0.05, "assimétrica", "simétrica"))
})
write.csv(norm_tab, "saida_tabelas/normalidade.csv", row.names = FALSE, fileEncoding = "UTF-8")

# ---- 4. Comparação de 2 grupos (Mann-Whitney + rank-biserial) --------------
# res_mw <- map_dfr(numericas, function(v) {
#   f <- as.formula(paste0("`", v, "` ~ `", grupo, "`"))
#   w <- wilcox.test(f, data = dados)
#   es <- rstatix::wilcox_effsize(dados, f)
#   tibble(desfecho = v, W = unname(w$statistic), p = signif(w$p.value, 3),
#          rrb = round(es$effsize, 3), magnitude = es$magnitude)
# })
# write.csv(res_mw, "saida_tabelas/mann_whitney.csv", row.names = FALSE, fileEncoding = "UTF-8")

# ---- 4b. Comparação 3+ grupos (Kruskal-Wallis + Dunn/Holm + eta²) -----------
# res_kw <- map_dfr(numericas, function(v) {
#   f <- as.formula(paste0("`", v, "` ~ `", grupo, "`"))
#   k <- kruskal.test(f, data = dados)
#   es <- rstatix::kruskal_effsize(dados, f)
#   tibble(desfecho = v, chi2 = round(unname(k$statistic),3), gl = k$parameter,
#          p = signif(k$p.value,3), eta2 = round(es$effsize,3), magnitude = es$magnitude)
# })
# write.csv(res_kw, "saida_tabelas/kruskal.csv", row.names = FALSE, fileEncoding = "UTF-8")
# # Post hoc de Dunn (correção de Holm) para os significativos:
# # FSA::dunnTest(as.formula(paste0("`",v,"` ~ `",grupo,"`")), data = dados, method = "holm")

# ---- 5. Associação categórica (qui-quadrado + resíduos + V de Cramér) -------
qui_resultado <- function(v1, v2) {
  tab <- table(dados[[v1]], dados[[v2]])
  ch  <- suppressWarnings(chisq.test(tab))
  vcr <- rcompanion::cramerV(tab)
  list(tabela = tab,
       resumo = tibble(var1 = v1, var2 = v2,
                       chi2 = round(unname(ch$statistic), 3),
                       gl = unname(ch$parameter), p = signif(ch$p.value, 3),
                       V = round(as.numeric(vcr), 3)),
       residuos = round(ch$stdres, 3))   # |SR| >= 1,96 = significativo (Sharpe, 2015)
}
# ex.: r <- qui_resultado("Grupo", "sexo"); print(r$resumo); print(r$residuos)

# ---- 6. Correlação (Pearson/Spearman) --------------------------------------
# metodo <- ifelse(all(norm_tab$distribuicao == "simétrica"), "pearson", "spearman")
# corr <- psych::corr.test(dados[ , numericas], method = metodo)
# write.csv(round(corr$r, 3), "saida_tabelas/correlacoes_r.csv", fileEncoding = "UTF-8")
# write.csv(round(corr$p, 3), "saida_tabelas/correlacoes_p.csv", fileEncoding = "UTF-8")

# ---- 7. Gráficos exemplo ----------------------------------------------------
# Boxplot + jitter + média
# ggplot(dados, aes(.data[[grupo]], .data[[numericas[1]]], fill = .data[[grupo]])) +
#   geom_boxplot(width=.55, alpha=.35, outlier.shape=NA) +
#   geom_jitter(width=.12, alpha=.45, size=1.6) +
#   stat_summary(fun=mean, geom="point", shape=23, size=3, fill="white") +
#   scale_fill_manual(values=PAL) + labs(x=NULL, y=numericas[1]) +
#   tema_multinivel() + theme(legend.position="none")
# salvar_fig("fig_boxplot.png")

# =============================================================================
# BLOCOS PSICOMÉTRICOS (descomente os pacotes no topo)
# =============================================================================

# ---- A. AFE (psych) --------------------------------------------------------
# itens <- dados %>% select(starts_with("Q"))
# KMO(itens); cortest.bartlett(itens)
# fa.parallel(itens, fa = "fa")                       # análise paralela de Horn
# efa <- fa(itens, nfactors = 1, fm = "wls", rotate = "oblimin"); print(efa$loadings, cutoff = .30)

# ---- B. AFC / MEE (lavaan, WLSMV) ------------------------------------------
# modelo <- '
#   F1 =~ Q1 + Q2 + Q3 + Q4
#   F2 =~ Q5 + Q6 + Q7 + Q8
# '
# fit <- lavaan::cfa(modelo, data = dados, estimator = "WLSMV", ordered = TRUE)
# lavaan::fitMeasures(fit, c("chisq.scaled","df.scaled","pvalue.scaled",
#   "cfi.robust","tli.robust","rmsea.robust","rmsea.ci.lower.robust",
#   "rmsea.ci.upper.robust","srmr"))
# lavaan::standardizedSolution(fit)
# semTools::reliability(fit)                          # alfa/ômega/CC/AVE
# semPlot::semPaths(fit, what="std", layout="tree2", rotation=2)

# ---- C. Consistência interna (psych::reliability) --------------------------
# fatores <- list(F1=c("Q1","Q2","Q3","Q4"), F2=c("Q5","Q6","Q7","Q8"))
# CI <- psych::reliability(keys = fatores, items = dados); print(CI, digits = 3)  # >0,70 satisfatório

# ---- D. TRI (mirt) — Modelo de Resposta Gradual ----------------------------
# mod_tri <- mirt::mirt(itens, 1, itemtype = "graded")
# coef(mod_tri, simplify = TRUE, IRTpars = TRUE)      # a (discriminação) e b (dificuldade)
# plot(mod_tri, type = "trace"); plot(mod_tri, type = "info")
# Cortes de 'a' (Pasquali, 2020): muito baixa .01-.34; baixa .35-.64; moderada .65-1.34; alta 1.35-1.69; muito alta >1.70

# ---- E. Invariância (semTools) ---------------------------------------------
# semTools::measurementInvariance(modelo, data = dados, group = grupo, estimator = "WLSMV", ordered = TRUE)
# # ΔCFI < 0,01 sustenta invariância (Cheung & Rensvold, 2002)

# ---- F. Redes (bootnet/qgraph) ---------------------------------------------
# net <- bootnet::estimateNetwork(itens, default = "EBICglasso")
# qgraph::qgraph(net$graph, layout = "spring", theme = "colorblind", labels = colnames(itens))
# qgraph::centralityPlot(net)

# =============================================================================
cat("\nConcluído. Tabelas em ./saida_tabelas e figuras em ./saida_figuras\n")
