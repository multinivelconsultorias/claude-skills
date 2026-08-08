# Catálogo de pacotes R — fluxo de trabalho Multinível

> Pacotes que o Julio usa, organizados por tipo de análise, com as funções centrais
> e o pacote-citação correspondente. Confirmado a partir dos scripts `.R`/`.Rmd` do
> acervo e da mineração dos relatórios.

## Carregamento padrão (preâmbulo dele)

```r
# O padrão do Julio é usar pacman para carregar tudo de uma vez:
if (!require("pacman")) install.packages("pacman")
pacman::p_load(tidyverse, psych, readxl)   # base recorrente
```

- `pacman::p_load(...)` — carrega (e instala se faltar) vários pacotes. **É a assinatura dele.**
- `tidyverse` — manipulação (`dplyr`, `tidyr`), gráficos (`ggplot2`), leitura (`readr`).
- `readxl::read_xlsx("dados.xlsx")` — leitura de Excel (entrada mais comum).
- `haven` — leitura de `.sav` (SPSS).
- `glimpse(dados)` / `psych::describe(dados)` — primeiro olhar na base.

---

## Por família de análise

### Descritiva e normalidade
| Função | Pacote | Uso |
|---|---|---|
| `describe()`, `describeBy()` | **psych** | descritivas (média, DP, assimetria, curtose) |
| `shapiro.test()` | stats (base) | Shapiro-Wilk |
| `mvn(..., mvnTest="mardia")` | **MVN** | normalidade multivariada (Mardia) |
| `car::leveneTest()` | **car** | homogeneidade de variâncias |
| `rstatix` | rstatix | testes "tidy" + effect size (alternativa) |

### Comparação de grupos (não-paramétrica — o forte dele)
| Função | Pacote | Uso |
|---|---|---|
| `wilcox.test()` | stats | Mann-Whitney / Wilcoxon |
| `kruskal.test()` | stats | Kruskal-Wallis |
| `PMCMRplus::kwAllPairsDunnTest()` / `dunnTest()` (FSA) | **PMCMRplus** / **FSA** | post hoc de Dunn |
| `npar.t.test()`, `nparcomp()` | **nparcomp** | comparação não-paramétrica + IC (post hoc multivariado) |
| `nparLD()` | **nparLD** | ANOVA não-paramétrica longitudinal / medidas repetidas (F1-LD-F1 etc.) |
| `rstatix::wilcox_effsize()` / `kruskal_effsize()` | **rstatix** | tamanho de efeito (r, eta²) |

### Comparação de grupos (paramétrica)
| Função | Pacote | Uso |
|---|---|---|
| `t.test()`, `aov()` | stats | t de Student, ANOVA |
| `afex::aov_ez()` | afex | ANOVA fatorial/mista |
| `emmeans()` | emmeans | médias marginais + post hoc |
| `effectsize::cohens_d()`, `eta_squared()` | **effectsize** | d, η², ε² |

### Associação categórica
| Função | Pacote | Uso |
|---|---|---|
| `chisq.test()`, `fisher.test()` | stats | qui-quadrado / Fisher |
| `chisq.test()$stdres` | stats | resíduos padronizados ajustados (corte ≥ 1,96) |
| `rcompanion::cramerV()` / `vcd::assocstats()` | rcompanion / vcd | V de Cramér |

### Correlação
| Função | Pacote | Uso |
|---|---|---|
| `cor()`, `cor.test()` | stats | Pearson / Spearman |
| `psych::corr.test()` | psych | matriz de correlações + p |
| `corrplot()` | corrplot | heatmap/correlograma |

### Confiabilidade / fidedignidade
| Função | Pacote | Uso |
|---|---|---|
| `reliability(keys=..., items=...)` | **psych** | alfa de Cronbach + ômega de McDonald (corte > 0,70) |
| `alpha()`, `omega()` | psych | alfa / ômega isolados |
| `semTools::reliability()` / `compRelSEM()` | **semTools** | confiabilidade composta a partir do SEM |
| `irr` / `irrCAC` | irr / irrCAC | kappa, ICC, Gwet AC1 |
| função custom `composite_reliability()` | (dele) | CC a partir das cargas padronizadas (ver script) |

### Análise fatorial exploratória (AFE)
| Função | Pacote | Uso |
|---|---|---|
| `KMO()`, `cortest.bartlett()` | **psych** | adequação amostral |
| `fa.parallel()` | psych | análise paralela de Horn |
| `nFactors` | nFactors | retenção de fatores |
| `fa()` | psych | extração (ex.: WLS/ML, rotação oblimin) |
| `EFA.MRFA` / `EFAtools` | EFA.MRFA / EFAtools | MRFA e diagnósticos alternativos |

### AFC / SEM / invariância
| Função | Pacote | Uso |
|---|---|---|
| `cfa()`, `sem()` | **lavaan** | AFC e modelos estruturais |
| `estimator="WLSMV"` | lavaan | dados ordinais/não normais |
| `fitMeasures(..., c("cfi.robust","tli.robust","rmsea.robust","srmr"))` | lavaan | índices robustos |
| `standardizedSolution()` | lavaan | cargas padronizadas |
| `measurementInvariance()` / `compareFit()` | **semTools** | invariância configural/métrica/escalar |
| `semPaths()` | **semPlot** | diagrama de caminhos |

### TRI / IRT
| Função | Pacote | Uso |
|---|---|---|
| `mirt(data, 1, itemtype="graded")` | **mirt** | modelo de resposta gradual (Samejima) |
| `coef(modelo, IRTpars=TRUE)` | mirt | parâmetros a (discriminação) e b (dificuldade) |
| `plot(modelo, type="trace"/"info")` | mirt | curvas características / de informação |
| `itemfit()`, `M2()` | mirt | ajuste do item/modelo |

### Análise de redes
| Função | Pacote | Uso |
|---|---|---|
| `estimateNetwork(data, default="EBICglasso")` | **bootnet** | estimação da rede |
| `qgraph()` | **qgraph** | visualização da rede |
| `centralityPlot()` | qgraph | força, proximidade, intermediação |
| `bootnet()` | bootnet | estabilidade/acurácia das arestas |
| `EGA()` | EGAnet | análise de grafos exploratória |

### Regressão e diagnósticos
| Função | Pacote | Uso |
|---|---|---|
| `lm()`, `glm()` | stats | regressão |
| `lmtest::bptest()` | lmtest | Breusch-Pagan (heterocedasticidade) |
| `car::durbinWatsonTest()` | car | autocorrelação |
| `cooks.distance()` | stats | outliers influentes |
| `performance::check_model()` | performance | diagnósticos visuais |

### Mediação / moderação
| Função | Pacote | Uso |
|---|---|---|
| `lavaan` (com `:=`) | lavaan | mediação/moderação com bootstrap |
| `processR` / `mediation` | processR / mediation | abordagem PROCESS (Hayes) |

### PERMANOVA / multivariada (perfil/ecologia)
| Função | Pacote | Uso |
|---|---|---|
| `adonis2()` | **vegan** | PERMANOVA |
| `pairwise.adonis()` | **pairwiseAdonis** | comparações par a par |
| `MANOVA.RM` | MANOVA.RM | MANOVA com resampling |

### Saída / tabelas / relatório
| Função | Pacote | Uso |
|---|---|---|
| `flextable` / `officer` | flextable/officer | tabelas formatadas → Word |
| `gtsummary` / `apaTables` | gtsummary/apaTables | tabelas estilo APA |
| `knitr` / R Markdown | knitr | render para PDF/HTML/Word |

---

## Preâmbulo completo sugerido (cobre a maioria dos relatórios)

```r
if (!require("pacman")) install.packages("pacman")
pacman::p_load(
  tidyverse, readxl, haven,        # leitura + manipulação
  psych,                            # descritiva, AFE, confiabilidade
  car, rstatix, effectsize,         # pressupostos + effect size
  PMCMRplus, FSA, nparcomp, nparLD, # não-paramétrica + post hoc
  rcompanion, vcd,                  # V de Cramér
  lavaan, semTools, semPlot, MVN,   # AFC/SEM/invariância
  mirt,                             # TRI
  qgraph, bootnet, EGAnet,          # redes
  corrplot, ggpubr, patchwork,      # gráficos
  flextable, officer                # tabelas Word
)
```
