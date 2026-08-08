# Templates de trechos reutilizáveis (verbatim do acervo)

> Blocos de "Análise de dados" e fórmulas de Resultados que o Julio reutiliza.
> Copie e **adapte** (nomes de variáveis, instrumentos, grupos). Substitua o ano de
> `R Core Team` pelo ano corrente do relatório. Mantenha a voz e os pontos de corte.

---

## A. Bloco "Análise de dados" — DESCRITIVA + COMPARAÇÃO (o mais comum)

> Versão completa (descritiva + normalidade + Mann-Whitney/Kruskal + qui-quadrado + efeito + post hoc).

"O software R foi utilizado para a realização das análises estatísticas (R Core Team, 2026). As estatísticas descritivas foram analisadas através da frequência e percentual das categorias para as variáveis qualitativas (categóricas), enquanto para as variáveis numéricas, investigou-se a média, mediana, desvio padrão, quartis, valor mínimo e máximo, além da análise da normalidade da distribuição, através do teste de Shapiro-Wilk, com resultados significativos indicando assimetria significativa da distribuição (Miot, 2017). A partir disso, em casos de assimetria na distribuição das variáveis numéricas, utilizou-se de testes estatísticos não paramétricos, sendo o teste de Mann-Whitney para investigar as diferenças entre dois grupos (Brunner, Bathke & Konietschke, 2018), enquanto para três ou mais grupos, utilizou-se do teste de Kruskal-Wallis, com post hoc realizado através do teste de Dunn com correção de Holm (Pohlert, 2014). Para a análise das estimativas do tamanho de efeito, utilizou-se o coeficiente de correlação rank-bisserial, que indica diferença pequena quando 0,20, moderada quando 0,50 e grande quando alcançados valores de 0,80 (Serdar, Cihan, Yücel & Serdar, 2021). Ademais, utilizou-se de testes de qui-quadrado (χ²) ou exato de Fisher para investigar possíveis associações entre [VARIÁVEIS] (Kim, 2017). O tamanho do efeito foi avaliado através do teste V de Cramér, no qual resultados 0,10 indicam associação fraca, valores 0,30 sugerem associações moderadas e resultados 0,50 indicam associação forte (Serdar, Cihan, Yücel & Serdar, 2021). Já os testes post hoc do χ² foram analisados através da análise dos resíduos padronizados ajustados, nos quais resultados ≥ 1,96 apontam associações significativas na tabela de referência cruzada (Sharpe, 2015)."

---

## B. Bloco "Análise de dados" — SÓ DESCRITIVA (perfil de amostra)

"Os dados foram analisados através da linguagem R de programação (R Core Team, 2026). Utilizou-se de estatísticas descritivas para investigar o perfil da amostra do estudo, sendo a frequência absoluta e o percentual, em casos de variáveis qualitativas, enquanto para variáveis quantitativas, utilizou-se da média, desvio padrão, quartis, valores mínimo e máximo."

---

## C. Bloco — CORRELAÇÃO

"Para a análise das associações entre as variáveis numéricas, a escolha do coeficiente se deu a partir da normalidade das distribuições (teste de Shapiro-Wilk; Miot, 2017). Em casos de normalidade, utilizou-se do coeficiente r de Pearson, enquanto para dados assimétricos, utilizou-se do coeficiente rho (ρ) de Spearman (Miot, 2018). Quanto à magnitude, valores próximos a 0,10 indicam correlação fraca, 0,30 moderada e 0,50 forte (Cohen, 1992)."

---

## D. Bloco — ANOVA MISTA NÃO-PARAMÉTRICA (longitudinal, nparLD)

"Posteriormente, para a análise do possível efeito diferencial da intervenção [entre GRUPOS], optou-se pela utilização de Análises de Variância (ANOVAs) mistas e não paramétricas, através do pacote nparLD (Noguchi, Gel, Brunner & Konietschke, 2012), considerando como fator transversal o grupo [GRUPOS] e como medida intra-sujeito os momentos de mensuração [TEMPOS]. Além disso, testes de Wilcoxon signed-rank foram propostos para investigar a eficácia da intervenção (Brunner, Bathke & Konietschke, 2018), com tamanho do efeito analisado através do coeficiente de correlação rank-bisserial (Serdar, Cihan, Yücel & Serdar, 2021)."

---

## E. Bloco — AFE (Análise Fatorial Exploratória)

"A Análise Fatorial Exploratória (AFE) foi conduzida para avaliar a estrutura interna do instrumento (Damásio, 2012). Inicialmente, a adequação da matriz de dados foi verificada por meio do índice Kaiser-Meyer-Olkin (KMO) e do Teste de Esfericidade de Bartlett (Damásio, 2012). O número de fatores a reter foi definido pela análise paralela de Horn (Horn, 1965). Para a extração, considerou-se o método de [mínimos quadrados/máxima verossimilhança] com rotação [oblimin/promin], adequado para [dados ordinais/contínuos]. Como ponto de corte das cargas fatoriais, adotou-se λ ≥ |0,30| (Hair et al., 2009)."

---

## F. Bloco — AFC / MEE (Análise Fatorial Confirmatória e SEM)

"A Análise Fatorial Confirmatória (AFC) foi conduzida por meio da linguagem R com o pacote lavaan (Rosseel, 2012), utilizando o método de estimação WLSMV, apropriado para dados categóricos/ordinais e com correção aos desvios de normalidade (Li, 2016). A adequação do modelo foi avaliada pelos índices: (a) χ², com valores adequados quando p < 0,05; (b) χ²/gl, satisfatório quando < 5, preferencialmente < 3; (c) CFI e (d) TLI, bons quando > 0,90 e excelentes se ≥ 0,95; (e) RMSEA, adequado com ≤ 0,08, com limite superior do intervalo de confiança < 0,10; e (f) SRMR, satisfatório quando ≤ 0,08 (Hair et al., 2009; Kline, 2016; Brown, 2015). A consistência interna foi avaliada pelos coeficientes Alfa (⍺) de Cronbach, Ômega (⍵) de McDonald e Confiabilidade Composta (CC), com valores acima de 0,70 indicando boa consistência interna (Bland & Altman, 1997; Hayes & Coutts, 2020), além da Variância Média Extraída (AVE > 0,50)."

---

## G. Bloco — TRI (Teoria de Resposta ao Item)

"Posteriormente, optou-se pela investigação dos parâmetros individuais dos itens, a partir do paradigma da Teoria de Resposta ao Item (TRI). Utilizou-se do Modelo de Resposta Gradual (Samejima, 1969), estimado por meio do pacote mirt (Chalmers, 2012), investigando-se os parâmetros de discriminação (a) e de dificuldade (b) de cada item. Quanto à interpretação do parâmetro de discriminação, utilizou-se do critério de Pasquali (2020), sendo: muito baixa (0,01 – 0,34), baixa (0,35 – 0,64), moderada (0,65 – 1,34), alta (1,35 – 1,69) e muito alta (acima de 1,70). Para os parâmetros de dificuldade, considerou-se a amplitude entre -3 e +3, no qual valores mais próximos do limite superior indicam maior nível de traço latente necessário para assinalar as maiores categorias de resposta (Pasquali & Primi, 2003)."

---

## H. Bloco — INVARIÂNCIA DE MEDIDA

"Quanto à invariância da medida, investigou-se a equivalência da estrutura fatorial entre os grupos [GRUPOS], através da comparação sequencial dos modelos configural, métrico (fraco), escalar (forte) e estrito (Damásio, 2013). A invariância foi sustentada quando a variação do CFI (ΔCFI) entre modelos aninhados foi inferior a 0,01 (Cheung & Rensvold, 2002)."

---

## I. Bloco — ANÁLISE DE REDES (network analysis)

"A estrutura de relações entre [VARIÁVEIS/ITENS] foi investigada por meio da análise de redes. A rede foi estimada pelo método EBICglasso, que aplica regularização para a estimação de correlações parciais (Epskamp et al., 2012; Costantini et al., 2015), por meio dos pacotes qgraph e bootnet. Foram investigados os índices de centralidade (força, proximidade e intermediação), e a acurácia e estabilidade das estimativas foram avaliadas por bootstrap (Machado, Vissoci & Epskamp, 2015)."

---

## J. Bloco — REGRESSÃO

"Modelos de regressão [linear/logística] foram realizados para investigar o efeito de [PREDITORES] sobre [DESFECHO] (Field, 2020). Os pressupostos foram verificados quanto à normalidade dos resíduos, homocedasticidade (teste de Breusch-Pagan; Breusch & Pagan, 1979), ausência de autocorrelação (Durbin & Watson, 1950) e ausência de observações influentes (distância de Cook; Cook & Weisberg, 1994). Para os modelos lineares, reportaram-se os coeficientes não padronizados (B) e padronizados (Beta); para os modelos logísticos, os coeficientes (B) e as razões de chances (OR), com seus respectivos intervalos de confiança. A qualidade global de cada modelo foi avaliada através da estatística F (modelos lineares) ou do qui-quadrado de razão de verossimilhança (modelos logísticos), dos coeficientes de determinação (R² e R² ajustado nos lineares; pseudo-R² de McFadden e de Nagelkerke nos logísticos) e dos critérios de informação de Akaike (AIC) e Bayesiano (BIC). Adotou-se como categoria de referência [o grupo de maior frequência / o grupo de interesse do estudo]."

---

## Fórmulas de Resultados (verbatim, com placeholders)

**Abertura descritiva:**
"Inicialmente, investigou-se [descritivamente] [O QUE]. Os resultados podem ser conferidos na Tabela 1."

**Caracterização da amostra:**
"Contou-se com a participação de [N] pessoas, com idades variando entre [min] e [max] anos (M= [x], DP= [x]), sendo a maior parte da amostra composta de pessoas do sexo [feminino/masculino] ([x]%) e [característica] ([x]%)."

**Resultado de qui-quadrado com resíduos:**
"A partir disso, foi possível observar que [GRUPO] se associou com [CATEGORIA] (SR = [x]), [...]. Os resultados podem ser conferidos na Tabela [N]."

**Resultado de comparação (não significativo):**
"Os resultados dos testes comparativos podem ser conferidos na Tabela [N], e apontam que não houve diferença estatisticamente significativa entre os grupos para [DESFECHO] (p = [x])."

**Resultado de comparação (significativo, com efeito) — redação fluida (nomear grupos e direção):**
"[GRUPO A] apresentou [maiores/menores] [DESFECHO] quando comparado a [GRUPO B] (p = [x]), com tamanho de efeito [pequeno/moderado/alto] (rrb = [x])."
- Ex.: "pessoas que precisaram sair de casa apresentaram maiores níveis de depressão (DASS-21) quando comparadas a quem não precisou sair de casa (p = 0,017; rrb = 0,17, efeito pequeno)."

**Resultado de regressão logística (traduzir o OR em chances):**
"Observou-se que [PREDITOR] associou-se ao desfecho (B = [x], OR = [x], p = [x]). Sendo assim, pode-se inferir que [o aumento de uma unidade em / pertencer a] [PREDITOR] [aumenta/reduz] em cerca de [OR] vez as chances de [DESFECHO], em relação a [categoria de referência]." (OR > 1 aumenta; OR < 1 reduz as chances.)
- Estatísticas do modelo: "O modelo apresentou qui-quadrado de razão de verossimilhança [χ²(gl) = x, p = x], pseudo-R² de McFadden de [x], AIC de [x] e BIC de [x]."

**Resultado de regressão linear:**
"[PREDITOR] associou-se a [DESFECHO] (B = [x], Beta = [x], p = [x]); o aumento de uma unidade em [PREDITOR] associa-se a [um aumento/uma redução] de [x] em [DESFECHO]. O modelo explicou cerca de [x]% da variância do desfecho [F(gl1, gl2) = x, p = x; AIC = x; BIC = x]."

**Resultado de mediação (cadeia narrada, sem o símbolo "→"):**
"Os resultados podem ser conferidos na Tabela [N] e na Figura [N], e apontam efeito indireto significativo de [X] sobre [Y], por meio de [M] (a*b = [x]; IC95% [x; x]). Como o efeito direto não foi significativo (c′ = [x]; p = [x]), caracteriza-se mediação total, com cerca de [x]% do efeito ocorrendo pela via indireta. Sendo assim, pode-se inferir que [X] contribui para [a piora/o aumento de] [M], que por sua vez associa-se [ao aumento/à redução de] [Y]. Por outro lado, não foi observado efeito direto de [X] sobre [Y]."

**Índices de ajuste (AFC):**
"Os índices de ajuste do modelo apontaram um ajuste [adequado/satisfatório/excelente] da estrutura proposta [χ² = [x], gl = [x], χ²/gl = [x], CFI = [x], TLI = [x]; RMSEA (95% CI): [x] ([x] – [x]); SRMR = [x]]."

**Confiabilidade:**
"Quanto à consistência interna, observaram-se resultados [adequados/excelentes] para [todos os] fatores, conforme aponta a Tabela [N]."

**Fecho de seção/considerações finais:**
"A partir dos resultados encontrados, é possível inferir que [SÍNTESE]. Em conjunto, os resultados indicam que [INSTRUMENTO/INTERVENÇÃO] apresenta [evidências de validade / efeito], recomendando-se [USO/PRÓXIMO PASSO]."
