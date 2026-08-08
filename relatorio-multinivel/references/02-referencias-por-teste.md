# Banco de referências por teste estatístico — Multinível

> Mapeamento teste → referência(s) que o Julio cita habitualmente, extraído por
> co-ocorrência em 328 relatórios. A **referência primária** é a que ele usa na
> maioria das vezes (frequência entre colchetes). Use sempre a primária; as
> secundárias servem de alternativa/complemento.
> A entrada bibliográfica completa em APA 7 está em `03-referencias-apa7.md`.
> Versão legível por máquina: `02-referencias-por-teste.json`.

---

## Normalidade e pressupostos

| Teste / conceito | Referência primária | Secundárias |
|---|---|---|
| **Shapiro-Wilk** (normalidade) | **Miot (2017)** [48×] | Razali & Wah (2011); Mishra et al. (2019); Field (2024) |
| Kolmogorov-Smirnov | Field (2020) | Razali & Wah (2011); Thode (2002) |
| Comparação de testes de normalidade | Razali & Wah (2011) | — |
| **Normalidade multivariada (Mardia)** | **Mardia (1970)** [29×] | Li (2016) |
| Homogeneidade de variâncias (Levene) | Shingala & Rajyaguru (2015) | Miot (2017) |
| Outliers / distância de Cook / Mahalanobis | **Cook & Weisberg (1994)** [13×] | Field (2024) |
| Dados ausentes (Little MCAR) | Little (1988) | — |

## Comparação de grupos — não-paramétrica

| Teste | Referência primária | Secundárias |
|---|---|---|
| **Mann-Whitney** (2 grupos indep.) | **Brunner, Bathke & Konietschke (2018)** [16×] | Field (2024); Mishra et al. (2019) |
| **Kruskal-Wallis** (3+ grupos) | **Pohlert (2014)** / Brunner, Bathke & Konietschke (2018) | Kruskal & Wallis (1952) |
| **Dunn** (post hoc de Kruskal) | **Pohlert (2014)** [20×] | Dunn (1964) |
| Wilcoxon (pareado) | Conover (1999) | Brunner, Bathke & Konietschke (2018) |
| Friedman (medidas repetidas) | Dancey & Reidy (2018) | Zimmerman & Zumbo (1993) |
| ANOVA/MANOVA não-paramétrica longitudinal | **Noguchi, Gel, Brunner & Konietschke (2012)** [nparLD] | Brunner, Bathke & Konietschke (2018) |

## Comparação de grupos — paramétrica

| Teste | Referência primária | Secundárias |
|---|---|---|
| teste t de Student | Harris & Hardin (2013) | Field (2024); Al-Achi (2019) |
| ANOVA | Field (2024) | Dancey & Reidy (2018) |
| Welch (variâncias desiguais) | Shingala & Rajyaguru (2015) | — |
| Games-Howell (post hoc) | Shingala & Rajyaguru (2015) | — |
| Post hoc de ANOVA paramétrica (preferir **Holm**) | **Chen, Feng & Yi (2017)** | Tukey: Konietschke et al. (2015) |
| **Correção Holm / Bonferroni** (múltiplas comparações) | **Chen, Feng & Yi (2017)** | Pohlert (2014); Dunn (1964) |
| Controle de FDR (Benjamini-Hochberg) | **Benjamini & Hochberg (1995)** [26×] | — |

## Associação entre variáveis categóricas

| Teste | Referência primária | Secundárias |
|---|---|---|
| **Qui-quadrado (χ²) / Fisher** | **Kim (2017)** [21×] | Hair et al. (2009) |
| **Resíduos padronizados ajustados** (post hoc χ²) | **Sharpe (2015)** [17×] | Kim (2017) |
| **V de Cramér** (tamanho de efeito) | **Serdar, Cihan, Yücel & Serdar (2021)** | Kim (2017) |

## Correlação

| Teste | Referência primária | Secundárias |
|---|---|---|
| **Pearson** | **Miot (2018)** | Field (2024) |
| **Spearman** | **Miot (2018)** [13×] | Field (2024); Cohen (1992) |
| Magnitude da correlação | Cohen (1992) | Dancey & Reidy (2018) |

## Tamanho de efeito (effect size)

| Medida | Referência primária | Secundárias |
|---|---|---|
| d de Cohen | Cohen (1988) | Serdar et al. (2021); Durlak (2009) |
| r / rank-biserial (Mann-Whitney/Wilcoxon) | **Serdar, Cihan, Yücel & Serdar (2021)** | — |
| V de Cramér (χ²) | **Serdar, Cihan, Yücel & Serdar (2021)** | Kim (2017) |
| eta² (η²) / epsilon² (ε²) | Serdar et al. (2021) | Cohen (1988); Tomczak & Tomczak |
| Diretrizes gerais de effect size | Cohen (1988, 1992) | Gignac & Szodorai (2016) |

## Confiabilidade / fidedignidade

| Medida | Referência primária | Secundárias |
|---|---|---|
| **Alfa de Cronbach** | Bland & Altman (1997) | Hayes & Coutts (2020) |
| **Ômega de McDonald** | **Hayes & Coutts (2020)** | McDonald (1999) |
| Confiabilidade composta (CC) / AVE | Hair et al. (2009) | Jorgensen et al. (2016) [semTools] |
| ICC (correlação intraclasse) | Polit (2014) | Silove et al. (1993) |
| Kappa de Cohen | Cohen (1960) | Altman (1991) |
| Kappa de Fleiss (múltiplos juízes) | Fleiss (1981) | — |
| Gwet AC1 / AC2 | Gwet (2008) | — |

## Análise fatorial exploratória (AFE)

| Conceito | Referência primária | Secundárias |
|---|---|---|
| **AFE (geral)** | **Damásio (2012)** | Watkins (2018); Bandalos & Finney (2018) |
| **KMO** | **Damásio (2012)** | Kaiser (1974); Hutcheson & Sofroniou (1999) |
| **Teste de esfericidade de Bartlett** | **Damásio (2012)** [15×] | — |
| **Análise paralela de Horn** (retenção) | **Horn (1965)** [28×] | Damásio (2012); Raiche & Magis (2020) [nFactors] |
| Estimador para dados ordinais (WLSMV) | Li (2016) | Finney & DiStefano (2013) |

## Análise fatorial confirmatória (AFC) e SEM

| Conceito | Referência primária | Secundárias |
|---|---|---|
| **AFC (geral)** | **Hair et al. (2009)** | Brown (2015); Kline (2016) |
| **Índices de ajuste (RMSEA, CFI, TLI, SRMR)** | **Hair et al. (2009)** [21×] + **Kline (2016)** [15×] | Brown (2015); Hu & Bentler (1999); Byrne (2013) |
| **Invariância de medida** | **Cheung & Rensvold (2002)** [10×] | Damásio (2013) |
| Modelagem de equações estruturais (MEE/SEM) | Kline (2016) | Marôco (2010); Byrne (2013) |
| Pacote lavaan | Rosseel (2012) | — |
| Pacote semTools (confiabilidade/invariância) | Jorgensen et al. (2016) | — |
| Dados não normais/categóricos em SEM | Finney & DiStefano (2013) | Li (2016) |

## Teoria de Resposta ao Item (TRI/IRT)

| Conceito | Referência primária | Secundárias |
|---|---|---|
| **Modelo de resposta gradual (GRM)** | **Samejima (1969)** [42×] | Muraki & Carlson (1995) |
| **Pacote mirt** | **Chalmers (2012)** [29×] | — |
| **TRI — teoria (PT-BR)** | **Pasquali (2020)** [66×] | Pasquali & Primi (2003); Andrade, Laros & Lima (2021) |
| TRI multidimensional | Reckase (2009) | Cai & Hansen (2013) |
| TRI — introdução | Bichi & Talib (2018) | Embretson & Reise (2000) |

## Análise de redes (network analysis)

| Conceito | Referência primária | Secundárias |
|---|---|---|
| **EBICglasso / estimação / qgraph** | **Epskamp et al. (2012)** | — |
| **Tutorial de redes** | Costantini et al. (2015) | — |
| **Redes (PT-BR)** | **Machado, Vissoci & Epskamp (2015)** | — |
| Teoria de redes | Newman (2018) | — |
| Centralidade em redes ponderadas | Opsahl, Agneessens & Skvoretz (2010) | — |

## Regressão

| Conceito | Referência primária | Secundárias |
|---|---|---|
| Regressão linear / múltipla | **Field (2020)** | Field (2024); evitar Damásio (2013) aqui |
| Heterocedasticidade (Breusch-Pagan) | Breusch & Pagan (1979) | Astivia & Zumbo (2019) |
| Autocorrelação (Durbin-Watson) | Durbin & Watson (1950) | — |
| Outliers / influência (Cook) | Cook & Weisberg (1994) | — |

## Mediação e moderação

| Conceito | Referência primária | Secundárias |
|---|---|---|
| Mediação/moderação (PROCESS) | Hayes (2013, 2017) | Prado, Korelo & Silva (2014) |

## Poder e tamanho amostral

| Conceito | Referência primária | Secundárias |
|---|---|---|
| G*Power | Faul et al. (2007) | Erdfelder, Faul & Buchner (1996) |
| Tamanho amostral em AFE/AFC/SEM | Kyriazos (2018) | — |

## PERMANOVA / dados multivariados (ecologia/perfil)

| Conceito | Referência primária | Secundárias |
|---|---|---|
| PERMANOVA / adonis (pacote vegan) | Oksanen et al. (2019) | — |
| Comparações par a par (pairwiseAdonis) | Arbizu (2020) | — |

## Validade de conteúdo

| Conceito | Referência primária | Secundárias |
|---|---|---|
| Validade (geral) | Sireci & Sukin (2013) | AERA/APA/NCME (2014) |
| Padrões de testagem | AERA, APA & NCME (2014) | — |

## Software

| Item | Citação |
|---|---|
| **R** | **R Core Team (ANO)** — usar o ano corrente do relatório (ex.: 2025, 2026). Em relatórios antigos: 2022. |

---

### Como usar este banco ao escrever
1. Identifique cada teste/análise do delineamento.
2. Puxe a **referência primária** correspondente.
3. Insira a citação **imediatamente após a menção do teste**, no formato `(Sobrenome, ano)`.
4. Garanta que toda citação usada apareça na lista de Referências (APA 7) ao final.
