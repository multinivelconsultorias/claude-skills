# Convenções de tabelas e figuras — Multinível (regras obrigatórias)

> Regras pedidas pelo Julio para padronizar os relatórios. Valem para **todos** os
> relatórios gerados pela skill. Aplicam-se ao gerador `build_report.py` (que já
> aceita tabelas/figuras genéricas) — o que muda é **como montar o conteúdo**.

## 1. Associações bivariadas (qui-quadrado / Fisher) → tabela de referência cruzada
- Sempre apresentar como **tabela de contingência (cross-tab)**, com a **variável fixa
  do estudo nas colunas** (ex.: o desfecho "Sair de casa": colunas "Não" e "Sim").
- Linhas = categorias de cada variável investigada, agrupadas por variável.
- Cada célula traz **n (%)** dentro da coluna (percentual por grupo da variável fixa).
- A linha-cabeçalho de cada variável carrega a estatística resumo (**p** e **V de Cramér**).
- **Pós-hoc:** marcar em **negrito** as células cujos resíduos padronizados ajustados
  têm |SR| ≥ 1,96 (Sharpe, 2015). A nota explica o negrito.

Esqueleto:
```
Tabela N. Frequências e associações de [variáveis] segundo [variável fixa]
| Variável / Categoria | Não — n (%) | Sim — n (%) | p | V de Cramér |
| Classe social #      |             |             | 0,501 | 0,11 |
|   Baixa              | 45 (35,4)   | 26 (32,5)   |       |      |
|   Média              | ...         | ...         |       |      |
| Renda (depois) *     |             |             | 0,053 | 0,19 |
|   ...                |             |             |       |      |
```

## 2. Identificação do teste e do tamanho de efeito (regra geral de TODAS as tabelas)
- **Nunca usar coluna nem linha "Teste".** O teste é identificado por um **símbolo**
  anexado ao nome da variável (ou dito **no título/nota da tabela**, quando a tabela inteira
  usa um único teste) e **explicado na nota**. Vale para **todas** as tabelas de teste —
  qui-quadrado/Fisher, **comparações (Mann-Whitney/Kruskal-Wallis)**, correlação etc.
  > Foi o caso da Tabela 3 (Mann-Whitney): o nome do teste **não** deve aparecer escrito na
  > tabela; basta o símbolo + a nota (ou dizê-lo no título, já que a tabela toda usa o mesmo teste).
- Símbolos padrão:
  - `*` = qui-quadrado de Pearson; `#` = exato de Fisher (esperadas < 5)
  - `ᵃ` = Mann-Whitney; `ᵇ` = Kruskal-Wallis; `ᶜ` = Wilcoxon (pareado)
  - `†` = razão de verossimilhança; `‡` = qui-quadrado com correção de Yates
- **Tamanho de efeito (paralelo teste↔efeito):** cada teste tem a sua medida própria —
  Mann-Whitney/Wilcoxon → rank-biserial (*rrb*); Kruskal-Wallis → *ε²*/*η²*; qui²/Fisher →
  *V* de Cramér; correlação → o próprio *r*/ρ. Esse paralelo é **declarado na "Análise de
  dados" (metodologia)**; na tabela o efeito é **coluna própria** (`rrb`, `V`…); e o **valor
  é citado no corpo do texto** ao descrever cada resultado, com o ponto de corte.
- Nota-modelo (cross-tab): *"Nota. * Qui-quadrado de Pearson; # Exato de Fisher. n (%):
  frequência e percentual por coluna. **Negrito**: resíduo padronizado ajustado |SR| ≥ 1,96
  (Sharpe, 2015). V de Cramér: tamanho de efeito."*

## 3. Heatmap de correlações
- **Sempre** incluir **legenda de cores** (colorbar) com gradação **−1 a +1**.
- **Anotar cada célula com o coeficiente de correlação** (r/ρ) — nunca o valor-p.
- Paleta **divergente** com **branco no centro (0)** e cores **fortes nos extremos**
  (correlações fracas ≈ brancas; fortes ≈ saturadas). Sugerido: azul-petróleo (+) /
  vinho (−), ou `RdBu`.
- **Cor do texto adaptativa**: texto escuro sobre células claras, texto branco sobre
  células escuras (regra: branco quando |r| ≥ ~0,5), para legibilidade em qualquer caso.
- Vírgula decimal nos rótulos. Receita em `05-graficos.md` (item “Heatmap anotado”).

## 4. Regressão → categoria de referência, B/OR (e Beta) e estatísticas do modelo

### 4.1 Categoria de referência (obrigatório)
- **A nota da tabela começa SEMPRE pela categoria de referência** do desfecho (logística) e
  dos preditores categóricos — é a **primeira informação da nota**.
  Ex.: *"Nota. Categoria de referência: pessoas que não precisaram sair de casa. B: ..."*
- **Como escolher a referência:** por padrão, o **nível de maior frequência** (maior n) —
  boa abordagem para a maioria dos relatórios. **Exceção:** quando o estudo define um grupo
  de interesse, usa-se a referência do estudo (no TCC Ricardo, a referência é sempre
  "precisar sair de casa"). Confirmar pelo objetivo do estudo.

### 4.2 Colunas
- **Logística:** **B** (log-odds) **e OR** (e^B), com **IC95% do OR** e p.
  Ordem: `Preditor | Nível | B | OR | IC95% (OR) | p`.
- **Linear:** **B (não padronizado) e Beta (β padronizado)**, com IC95% e p.
  Ordem: `Preditor | Nível | B | Beta | IC95% (B) | p`.
- B/OR via `broom::tidy(m, exponentiate = FALSE/TRUE)`; Beta via coeficientes padronizados
  (`parameters::standardise_parameters` ou `lm.beta`).

### 4.3 Estatísticas do modelo (obrigatório — citar no corpo do texto e/ou no rodapé)
- **Sempre** reportar as estatísticas globais do modelo, no mínimo:
  - **Linear:** `F(gl1, gl2)`, p, **R²** (e R² ajustado), **AIC**, **BIC**.
  - **Logística:** **χ²(gl)** do modelo (razão de verossimilhança) e p; **pseudo-R²**
    (McFadden e/ou Nagelkerke); **AIC**; **BIC**; quando útil, AUC.
- Nota-modelo (logística): *"Nota. Categoria de referência: [grupo]. B: coeficiente logístico
  (log-odds); OR: razão de chances (e^B); IC95%: intervalo de confiança do OR. Modelo:
  χ²(gl) = [x], p = [x]; R² de McFadden = [x]; AIC = [x]; BIC = [x]."*

## 5. Mediação e moderação → tabela padronizada + figura com coeficientes

### 5.0 Sempre em duas versões: bruta e ajustada (obrigatório)
- Todo modelo de **mediação e de moderação** é estimado em **duas versões**: **bruta**
  (sem covariáveis) e **ajustada** por covariáveis relevantes — por padrão **idade e
  sexo/gênero**, acrescentando outras pertinentes ao estudo (ex.: diagnóstico prévio, renda).
- **Apresentar as duas lado a lado** (tabela comparativa: efeito e p/p-FDR no bruto vs. no
  ajustado) e **interpretar a robustez**: se o efeito mantém magnitude e significância ao
  ajuste, é robusto; se enfraquece/some, pode haver confundimento — ou perda de poder
  (checar o n, que cai quando uma covariável tem faltantes).
- Com muitos modelos, aplicar a **correção por múltiplas comparações (FDR) dentro de cada
  versão** (separadamente para bruto e ajustado).
- Vale tanto para um único modelo focal quanto para grids exploratórios de muitos modelos.
- **Amostras pequenas:** quando o n não comporta termos de interação confiáveis, fazer
  **moderação estratificada** — dividir a amostra pelos níveis do moderador e estimar a
  associação (correlação/teste) dentro de cada estrato, reportando os resultados lado a lado
  por estrato. *(Preferência do Julio, jun/2026.)*

### 5.1 Tabela de mediação — notação compacta na coluna "Caminho/efeito"
- A coluna **"Caminho/efeito"** usa **notação por letras**, não nomes por extenso:
  **a, b, (a\*b), c, c′** (para modelos simples como o do TCC Ricardo). Em modelos com mais
  caminhos, estender no mesmo padrão (a1, b1, …).
  - **a** = efeito de X sobre M; **b** = efeito de M sobre Y (controlando X);
    **(a\*b)** = efeito indireto; **c** = efeito total; **c′** = efeito direto.
- Colunas: `Caminho/efeito | Coeficiente | IC95% | p`. A linha de **(a\*b)** traz o IC bootstrap.
- Nota-modelo: *"Nota. a: efeito de [X] sobre [M]; b: efeito de [M] sobre [Y]; (a\*b): efeito
  indireto; c: efeito total; c′: efeito direto. IC95% do efeito indireto por bootstrap."*

### 5.2 Figura (sempre que possível)
- Gerar o **diagrama de caminhos** com os **coeficientes anotados nas setas**.
- **Mediação:** X, M, Y com os caminhos a, b, c′ e o efeito indireto (a\*b) com IC;
  significância (* p < 0,05).
- **Moderação:** X sobre Y com o moderador e a interação sobre o caminho; anotar o
  coeficiente da **interação** e as **inclinações simples**.
- Receita base-R em `05-graficos.md`. Legenda: "Figura N. Modelo de mediação com
  coeficientes (* p < 0,05)."
- **As setas e a notação ficam na figura/tabela.** No **corpo do texto**, a cadeia é
  **descrita por extenso e de forma narrada** (sem o símbolo "→"); ver o guia de estilo,
  §3.1 (interpretação acessível) e §7.1 (símbolos e hífen no texto).

## 6. Formato físico das tabelas e pós-testes (preferência do Julio, jun/2026)
- **AutoAjuste de conteúdo** (AutoFit to Contents) em todas as tabelas, sem larguras fixas.
- **Título como 1ª linha da própria tabela**, mesclada em todas as colunas e **sem bordas**
  (integrada, fica "invisível"), em vez de parágrafo acima. Implementado em `assets/build_report.py`.
- **Parágrafos de corpo com recuo de 1ª linha** (1,25 cm).
- **ANOVA paramétrica:** post hoc com **correção de Holm** (Chen, Feng & Yi, 2017), não Tukey;
  Kruskal-Wallis segue com Dunn + Holm (Pohlert, 2014).
