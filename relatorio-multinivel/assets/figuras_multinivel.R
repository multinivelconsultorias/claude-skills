# =====================================================================
# Receita de figuras (identidade visual Multinivel)
#
# Paleta e regras extraidas do Design System da marca
# ("4. Imagens/Multinível - Sonar/Design System/02-Cores.md", secao
# "Aplicacao em graficos de dados"):
#   ordem de series: esmeralda, teal, verde, cinza, ambar
#   serie protagonista em esmeralda; demais em neutros/teal
#   fundo branco ou paper; sem linhas de grade (pedido do cliente)
#
# Barras com cantos arredondados desenhadas como poligonos, sem
# dependencia de pacotes externos ao tidyverse.
#
# Saidas: saida_figuras/figura_*.png
# =====================================================================

if (!require(pacman)) install.packages("pacman")
pacman::p_load(dplyr, ggplot2, forcats, scales, systemfonts)

base <- readRDS("BASE_TRATADA.rds")

# --- Cores da marca ---------------------------------------------------
MN <- list(esmeralda = "#00C896", esmeralda600 = "#0AA37B",
           verde = "#3DB54A", teal = "#16697A", petroleo = "#0A2E2E",
           menta = "#CFF3EA", ink = "#111417", cinza700 = "#3A4747",
           cinza500 = "#5E6E6E", cinza300 = "#C6D0D0", paper = "#F5F7F7")

# Fonte das figuras: sem serifa, por contraste com o corpo do relatorio,
# que permanece em Times New Roman.
#
# Preferencia: San Francisco, a fonte de sistema da Apple. Ela nao e
# exposta como familia pelo systemfonts (o arquivo declara "System
# Font"), de modo que e registrada explicitamente a partir do arquivo,
# com os pesos Regular, Italic e Mono. Se o arquivo nao existir (outro
# sistema operacional), cai na cascata das fontes da marca.
registrar_san_francisco <- function() {
  reg  <- "/System/Library/Fonts/SFNS.ttf"
  ital <- "/System/Library/Fonts/SFNSItalic.ttf"
  if (!file.exists(reg)) return(FALSE)
  systemfonts::register_font(
    name = "San Francisco",
    plain = reg, bold = reg,
    italic = if (file.exists(ital)) ital else reg,
    bolditalic = if (file.exists(ital)) ital else reg,
    features = systemfonts::font_feature(ligatures = "standard"))
  TRUE
}

resolver_fonte <- function(preferidas = c("San Francisco", "Poppins",
                                          "Montserrat", "Avenir Next",
                                          "Helvetica Neue")) {
  registrar_san_francisco()
  disp <- unique(c(systemfonts::system_fonts()$family,
                   systemfonts::registry_fonts()$family))
  achou <- preferidas[preferidas %in% disp]
  if (length(achou) == 0) return("sans")
  achou[1]
}
FONTE <- resolver_fonte()
cat("Fonte das figuras:", FONTE, "\n")

tema_mn <- function(base_size = 12, eixo_x = TRUE) {
  theme_minimal(base_family = FONTE, base_size = base_size) +
    theme(
      panel.grid      = element_blank(),          # sem linhas de grade
      panel.background = element_blank(),
      plot.background  = element_rect(fill = "white", color = NA),
      axis.line.x = if (eixo_x)
        element_line(color = MN$cinza300, linewidth = .5) else element_blank(),
      axis.ticks  = element_blank(),
      axis.text   = element_text(color = MN$cinza700, size = base_size - 1),
      axis.title  = element_text(color = MN$cinza500, size = base_size - 1),
      legend.position = "top",
      legend.justification = "left",
      legend.key.size = unit(.45, "cm"),
      legend.text = element_text(color = MN$cinza700, size = base_size - 1),
      plot.margin = margin(10, 18, 8, 8))
}

# ---------------------------------------------------------------------
# Poligonos de canto arredondado
# ---------------------------------------------------------------------
arco <- function(cx, cy, rx, ry, de, ate, n = 24) {
  a <- seq(de, ate, length.out = n)
  data.frame(x = cx + rx * cos(a), y = cy + ry * sin(a))
}

# Barra horizontal: base rente ao eixo, ponta arredondada
barra_h_poly <- function(valor, centro, altura, rx, ry, grupo) {
  r <- min(rx, valor)
  rbind(
    data.frame(x = 0, y = centro - altura / 2),
    data.frame(x = valor - r, y = centro - altura / 2),
    arco(valor - r, centro - altura / 2 + ry, r, ry, -pi / 2, 0),
    arco(valor - r, centro + altura / 2 - ry, r, ry, 0, pi / 2),
    data.frame(x = 0, y = centro + altura / 2)
  ) %>% dplyr::mutate(grupo = grupo)
}

# Coluna vertical: base rente ao eixo, topo arredondado
barra_v_poly <- function(valor, centro, largura, rx, ry, grupo) {
  r <- min(ry, valor)
  rbind(
    data.frame(x = centro - largura / 2, y = 0),
    data.frame(x = centro - largura / 2, y = valor - r),
    arco(centro - largura / 2 + rx, valor - r, rx, r, pi, pi / 2),
    arco(centro + largura / 2 - rx, valor - r, rx, r, pi / 2, 0),
    data.frame(x = centro + largura / 2, y = 0)
  ) %>% dplyr::mutate(grupo = grupo)
}

salvar <- function(g, arq, w, h) {
  ggsave(file.path("saida_figuras", arq), g, width = w, height = h,
         dpi = 300, bg = "white")
}

# ---------------------------------------------------------------------
# Figuras de barras horizontais (categoria unica)
# ---------------------------------------------------------------------
fig_barras_h <- function(v, arq, w = 7, h = 4.2) {
  x <- base[[v]]; x <- x[!is.na(x)]
  d <- as.data.frame(table(x)); names(d) <- c("cat", "n")
  d$pct <- 100 * d$n / sum(d$n)
  d <- d[order(d$pct), ]
  d$pos <- seq_len(nrow(d))
  # protagonista (maior categoria) em esmeralda; demais em teal
  d$cor <- ifelse(d$pct == max(d$pct), MN$esmeralda, MN$teal)

  rx <- max(d$pct) * .020
  polys <- do.call(rbind, lapply(seq_len(nrow(d)), function(i)
    barra_h_poly(d$pct[i], d$pos[i], .62, rx, .10, d$cat[i])))
  polys$cor <- d$cor[match(polys$grupo, d$cat)]

  d$rot <- paste0(d$n, " (", format(round(d$pct, 1), decimal.mark = ",",
                                    nsmall = 1, trim = TRUE), "%)")
  d$dentro <- d$pct >= .22 * max(d$pct)

  ggplot() +
    geom_segment(aes(x = 0, xend = 0, y = .35, yend = nrow(d) + .65),
                 color = MN$cinza300, linewidth = .5) +
    geom_polygon(data = polys, aes(x, y, group = grupo, fill = cor)) +
    scale_fill_identity() +
    geom_text(data = subset(d, dentro), aes(pct, pos, label = rot),
              hjust = 1.18, color = "white", family = FONTE, size = 3.7) +
    geom_text(data = subset(d, !dentro), aes(pct, pos, label = rot),
              hjust = -.15, color = MN$cinza700, family = FONTE, size = 3.7) +
    scale_y_continuous(breaks = d$pos, labels = d$cat, expand = expansion(add = .6)) +
    scale_x_continuous(expand = expansion(mult = c(0, .16))) +
    labs(x = "Percentual (%)", y = NULL) +
    tema_mn(eixo_x = FALSE) +
    theme(axis.text.y = element_text(color = MN$ink, size = 11.5),
          axis.text.x = element_blank(), axis.title.x = element_blank()) -> g
  salvar(g, arq, w, h); g
}

fig_barras_h("agente_grupo",  "figura_2_agente_causal.png", 7, 4.2)
fig_barras_h("circunstancia", "figura_3_circunstancia.png", 7, 3.6)
fig_barras_h("turno_entrada", "figura_4_turno.png",         7, 3.6)

# ---------------------------------------------------------------------
# Figura 1 - faixa etaria por sexo (colunas agrupadas)
# ---------------------------------------------------------------------
d1 <- base %>% count(faixa_etaria, sexo) %>%
  tidyr::complete(faixa_etaria, sexo, fill = list(n = 0))
d1$xi <- as.numeric(d1$faixa_etaria) +
  ifelse(d1$sexo == "Masculino", -.17, .17)
d1$cor <- ifelse(d1$sexo == "Masculino", MN$esmeralda, MN$teal)

ry1 <- max(d1$n) * .030
p1 <- do.call(rbind, lapply(seq_len(nrow(d1)), function(i)
  barra_v_poly(d1$n[i], d1$xi[i], .30, .045, ry1, paste0("g", i))))
p1$cor <- d1$cor[as.integer(sub("g", "", p1$grupo))]

g1 <- ggplot() +
  geom_polygon(data = p1, aes(x, y, group = grupo, fill = cor)) +
  scale_fill_identity() +
  geom_text(data = d1, aes(xi, n, label = n), vjust = -.75,
            family = FONTE, size = 3.7, color = MN$cinza700) +
  # legenda manual, ja que o preenchimento e identidade
  geom_point(data = data.frame(x = c(.72, 1.20), y = max(d1$n) * 1.20,
                               cor = c(MN$esmeralda, MN$teal)),
             aes(x, y, color = cor), size = 3.2, shape = 15) +
  geom_text(data = data.frame(x = c(.80, 1.28), y = max(d1$n) * 1.20,
                              lab = c("Masculino", "Feminino")),
            aes(x, y, label = lab), hjust = 0, family = FONTE,
            size = 3.6, color = MN$cinza700) +
  scale_color_identity() +
  scale_x_continuous(breaks = 1:3, labels = levels(base$faixa_etaria)) +
  scale_y_continuous(expand = expansion(mult = c(0, .28))) +
  labs(x = NULL, y = NULL) +
  tema_mn() +
  theme(axis.text.x = element_text(color = MN$ink, size = 11.5),
        axis.text.y = element_blank())
salvar(g1, "figura_1_faixa_etaria_sexo.png", 7, 4.2)

# ---------------------------------------------------------------------
# Figura 5 - distribuicao mensal (colunas; pico em esmeralda)
# ---------------------------------------------------------------------
d5 <- base %>% count(mes_admissao, .drop = FALSE) %>%
  mutate(xi = as.numeric(mes_admissao),
         cor = ifelse(n == max(n), MN$esmeralda, MN$teal))
ry5 <- max(d5$n) * .030
p5 <- do.call(rbind, lapply(which(d5$n > 0), function(i)
  barra_v_poly(d5$n[i], d5$xi[i], .58, .085, ry5, paste0("m", i))))
p5$cor <- d5$cor[as.integer(sub("m", "", p5$grupo))]

g5 <- ggplot() +
  geom_polygon(data = p5, aes(x, y, group = grupo, fill = cor)) +
  scale_fill_identity() +
  geom_text(data = subset(d5, n > 0), aes(xi, n, label = n), vjust = -.75,
            family = FONTE, size = 3.7, color = MN$cinza700) +
  scale_x_continuous(breaks = 1:12, labels = levels(base$mes_admissao)) +
  scale_y_continuous(expand = expansion(mult = c(0, .20))) +
  labs(x = NULL, y = NULL) +
  tema_mn() +
  theme(axis.text.x = element_text(color = MN$ink, size = 10.5,
                                   angle = 45, hjust = 1),
        axis.text.y = element_blank())
salvar(g5, "figura_5_mes_admissao.png", 7, 4)

cat("\nScript 06 concluido.\n")
