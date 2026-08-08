# Catálogo de gráficos — Multinível

> (A) O que o Julio **já usa** (replicar quando o tipo de análise pedir) e
> (B) **propostas novas**, mais estilizadas, para enriquecer a visualização.
> Legendas no padrão "Figura N. Título" (abaixo da figura, APA 7).
> Paleta padrão proposta: tons sóbrios (cinza/azul-petróleo) ou `viridis` para daltonismo.

---

## (A) Gráficos já utilizados no acervo

Categorias extraídas das legendas de 438 figuras:

| Tipo | Quando aparece | Pacote/função |
|---|---|---|
| **Scree plot / análise paralela** | retenção de fatores na AFE | `psych::fa.parallel()`, `nFactors` |
| **Diagrama de caminhos (path/SEM)** | AFC, modelo estrutural, mensuração | `semPlot::semPaths()` |
| **Rede (network)** | análise de redes, correlações parciais | `qgraph()` |
| **Curvas TRI** (características CCI / informação TIF) | TRI | `mirt::plot(type="trace"/"info")` |
| **Boxplot** | distribuição de escores por grupo | `ggplot2::geom_boxplot()` |
| **Barras / colunas** | frequências, percentuais, médias por grupo | `geom_col()` / `geom_bar()` |
| **Dispersão / correlograma / heatmap** | correlações entre fatores/itens | `corrplot()`, `geom_point()` |
| **Histograma / densidade** | distribuição, resíduos | `geom_histogram()`, `geom_density()` |
| **Perfil de médias / linhas** | interação grupo×tempo, evolução longitudinal | `geom_line()` + `geom_point()` |
| **Diagrama de mediação/moderação** | modelos de regressão com caminhos | `semPaths()` / `DiagrammeR` |
| **Violino** | distribuição (variação do boxplot) | `geom_violin()` |

Legendas reais (modelo de redação):
- "Figura 1. Análise paralela de Horn"
- "Figura 2. Diagrama de caminhos do modelo de mensuração"
- "Figura 3. Curvas características dos itens (CCI)"
- "Figura 1. Boxplot dos escores por grupo"
- "Figura 2. Rede de correlações parciais (EBICglasso)"

---

## (B) Propostas novas (mais estilizadas)

> Mantêm a sobriedade APA, mas melhoram leitura. Todas em `ggplot2` com um tema-base comum.

### Tema-base Multinível (usar em todos)
```r
library(ggplot2)
tema_multinivel <- function(base_size = 12) {
  theme_minimal(base_family = "Times New Roman", base_size = base_size) +
    theme(
      panel.grid.minor = element_blank(),
      panel.grid.major.x = element_blank(),
      axis.line = element_line(color = "grey30"),
      axis.title = element_text(color = "grey20"),
      plot.title = element_text(face = "bold", size = base_size + 1),
      plot.caption = element_text(color = "grey40", hjust = 0),
      legend.position = "bottom"
    )
}
PAL <- c("#2C5F6F", "#C0703A", "#6E8B3D", "#8C4A5F", "#4F6D7A") # paleta sóbria
```

### 1. Boxplot + jitter + média (melhor que boxplot puro)
```r
ggplot(df, aes(x = grupo, y = escore, fill = grupo)) +
  geom_boxplot(width = .55, alpha = .35, outlier.shape = NA) +
  geom_jitter(width = .12, alpha = .45, size = 1.6) +
  stat_summary(fun = mean, geom = "point", shape = 23, size = 3, fill = "white") +
  scale_fill_manual(values = PAL) +
  labs(x = NULL, y = "Escore", caption = "Losango = média") +
  tema_multinivel() + theme(legend.position = "none")
# Figura X. Distribuição dos escores por grupo (boxplot com observações individuais)
```

### 2. Raincloud (densidade + box + pontos) — distribuição rica
```r
# requer ggdist
library(ggdist)
ggplot(df, aes(x = grupo, y = escore, fill = grupo)) +
  ggdist::stat_halfeye(adjust = .6, width = .5, justification = -.2, .width = 0) +
  geom_boxplot(width = .12, outlier.shape = NA, alpha = .5) +
  ggdist::stat_dots(side = "left", justification = 1.1, dotsize = .5) +
  scale_fill_manual(values = PAL) +
  labs(x = NULL, y = "Escore") + tema_multinivel() + theme(legend.position = "none")
# Figura X. Distribuição dos escores por grupo (raincloud)
```

### 3. Barras de frequência com rótulos (categóricas)
```r
ggplot(df_freq, aes(x = reorder(categoria, n), y = n)) +
  geom_col(fill = PAL[1], width = .7) +
  geom_text(aes(label = sprintf("%d (%.1f%%)", n, pct)), hjust = -.1, size = 3.5) +
  coord_flip() + expand_limits(y = max(df_freq$n) * 1.15) +
  labs(x = NULL, y = "Frequência") + tema_multinivel()
# Figura X. Distribuição de frequência das categorias
```
> **Rótulo de % em barras horizontais (preferência do Julio, jun/2026):** mostrar o percentual
> **dentro** da barra (texto **branco**) quando ela é larga e **fora** (texto **preto**) quando
> é curta. Receita: dois `geom_text` filtrando por largura — `hjust=1.12, colour="white"` para
> barras largas (ex.: proporção ≥ 0,12) e `hjust=-0.15, colour="black"` para as curtas.

### 4. Perfil de médias com IC (interação grupo × tempo)
```r
ggplot(resumo, aes(x = tempo, y = media, color = grupo, group = grupo)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2.6) +
  geom_errorbar(aes(ymin = media - ic, ymax = media + ic), width = .12) +
  scale_color_manual(values = PAL) +
  labs(x = "Tempo", y = "Média estimada", color = NULL) + tema_multinivel()
# Figura X. Perfil das médias ao longo do tempo, por grupo (barras = IC 95%)
```

### 5. Heatmap de correlações (anotado, legenda −1..+1, texto adaptativo) — PADRÃO OBRIGATÓRIO
Regras (ver `08-convencoes-tabelas-figuras.md` §3): colorbar de −1 a +1; **coeficiente
em cada célula** (nunca o p); branco no centro, cores fortes nos extremos; **cor do
texto adaptativa** (branco quando |r| ≥ 0,5) para legibilidade.
```r
library(reshape2)
m <- round(cor(itens, use = "pairwise", method = "spearman"), 2)
dd <- melt(m, na.rm = TRUE)
dd$lab <- sub("\\.", ",", formatC(dd$value, format="f", digits=2))   # vírgula decimal
dd$txt <- ifelse(abs(dd$value) >= 0.5, "branco", "escuro")           # texto adaptativo
ggplot(dd, aes(Var1, Var2, fill = value)) +
  geom_tile(color = "white") +
  geom_text(aes(label = lab, color = txt), size = 3, show.legend = FALSE) +
  scale_color_manual(values = c(branco = "white", escuro = "grey15")) +
  scale_fill_gradient2(low = "#8C1D40", mid = "white", high = "#1F5C73",
                       midpoint = 0, limits = c(-1, 1), breaks = seq(-1, 1, .5),
                       name = "ρ", guide = guide_colorbar(barheight = 8)) +
  labs(x = NULL, y = NULL) + tema_multinivel() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1), panel.grid = element_blank(),
        legend.position = "right")
# Figura X. Matriz de correlações de Spearman (a colorbar à direita indica a magnitude e o sentido).
```
> **Base R** (quando o relatório roda sem ggplot, como no fluxo do gerador): use
> `image()` com `colorRampPalette(c("#8C1D40","white","#1F5C73"))(100)`, `zlim=c(-1,1)`,
> desenhe os rótulos com `text(... col = ifelse(abs(r)>=0.5,"white","grey15"))` e
> acrescente uma faixa de cor (colorbar) com `legend`/`image` lateral rotulada de −1 a +1.

### 6. Diagrama de caminhos (AFC/SEM) estilizado
```r
library(semPlot)
semPaths(fit, what = "std", whatLabels = "std",
         layout = "tree2", rotation = 2, edge.label.cex = 0.9,
         sizeMan = 6, sizeLat = 9, nCharNodes = 0,
         edge.color = "grey40", color = list(lat = "#2C5F6F33", man = "#C0703A22"),
         mar = c(4, 4, 4, 4))
# Figura X. Diagrama de caminhos do modelo com cargas padronizadas
```

### 7. Forest plot de tamanhos de efeito (síntese de comparações)
```r
ggplot(ef, aes(x = estimativa, y = reorder(desfecho, estimativa))) +
  geom_vline(xintercept = 0, linetype = 2, color = "grey60") +
  geom_errorbarh(aes(xmin = ic_inf, xmax = ic_sup), height = .2) +
  geom_point(size = 3, color = PAL[1]) +
  labs(x = "Tamanho de efeito (r) [IC 95%]", y = NULL) + tema_multinivel()
# Figura X. Tamanhos de efeito das comparações entre grupos (IC 95%)
```

### 8. Rede psicométrica estilizada (qgraph)
```r
library(qgraph); library(bootnet)
net <- estimateNetwork(itens, default = "EBICglasso")
qgraph(net$graph, layout = "spring", theme = "colorblind",
       labels = colnames(itens), label.cex = 1.1,
       posCol = "#2C5F6F", negCol = "#C0703A", vsize = 7, border.width = 1.5)
# Figura X. Rede de correlações parciais (EBICglasso)
```

### 9. Curvas TRI mais limpas (mirt → ggplot)
```r
# Curva de informação do teste
plot(modelo_tri, type = "info", theta_lim = c(-4, 4))
# Curvas características por item (trace lines)
plot(modelo_tri, type = "trace", which.items = 1:6,
     facet_items = TRUE, theta_lim = c(-4, 4))
# Figura X. Curvas características dos itens (modelo de resposta gradual)
```

### 10. Diagrama de mediação/moderação anotado — PADRÃO OBRIGATÓRIO
Ver `08-convencoes-tabelas-figuras.md` §5: sempre gerar a figura com os **coeficientes
nas setas** (a, b, c′ e indireto a×b com IC; significância com *). Receita base-R (sem
dependências), que casa com o gerador do fluxo Multinível:
```r
# m: lista com a,b,cp,ind (cada um com $est e $p) — ex.: saída de mediacao_moderacao.R
png("saida_figuras/fig_mediacao.png", width=1700, height=900, res=200)
op <- par(mar=c(1,1,2,1)); plot.new(); plot.window(xlim=c(0,10), ylim=c(0,6))
star <- function(p) if (is.na(p)) "" else if (p<0.001) "***" else if (p<0.01) "**" else if (p<0.05) "*" else ""
vg <- function(x,d=3) sub("\\.", ",", formatC(round(x,d), format="f", digits=d))
box <- function(x,y,txt){ rect(x-1.4,y-.5,x+1.4,y+.5, border="#2C5F6F", lwd=2, col="#2C5F6F11"); text(x,y,txt, font=2, cex=.9) }
arr <- function(x0,y0,x1,y1,lab){ arrows(x0,y0,x1,y1, length=.12, lwd=2, col="grey30"); text((x0+x1)/2,(y0+y1)/2+.3, lab, cex=.85) }
box(5,5,"M\n(mediador)"); box(1.6,1,"X\n(antecedente)"); box(8.4,1,"Y\n(desfecho)")
arr(2.6,1.6,4.2,4.5, paste0("a = ", vg(m$a$est), star(m$a$p)))
arr(5.8,4.5,7.4,1.6, paste0("b = ", vg(m$b$est), star(m$b$p)))
arr(3.0,1,7.0,1,    paste0("c' = ", vg(m$cp$est), star(m$cp$p)))
text(5,0.2, paste0("Efeito indireto a×b = ", vg(m$ind$est),
     "  IC95% [", vg(m$ind$lci), "; ", vg(m$ind$uci), "]"), cex=.85, font=3)
par(op); dev.off()
# Figura X. Modelo de mediação com coeficientes (* p<0,05; ** p<0,01; *** p<0,001).
```
Para **moderação**, desenhar X→Y com a seta do termo de interação incidindo sobre o
caminho e anotar o coeficiente da interação + inclinações simples (slopes) por grupo.

---

## Convenções de exportação
```r
ggsave("figura_X.png", width = 16, height = 10, units = "cm", dpi = 300)
```
- 300 dpi, largura ~16 cm (cabe na página com margens).
- Texto das figuras em Times New Roman 12 (ou 10 para rótulos densos), coerente com o corpo.
- Rótulos de eixo e legendas em português, vírgula decimal quando possível.
- Legenda da figura **abaixo** da imagem: "Figura N. Descrição."
