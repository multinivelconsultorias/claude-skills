# Guia de estilo de escrita — Relatórios Multinível

> Destilado de 328 relatórios (2020–2026) escritos por Julio Cezar Albuquerque da Costa.
> Objetivo: reproduzir fielmente a voz do autor, **incluindo seus vícios de linguagem (em dose um pouco menor que o natural)**.

---

## 1. Cabeçalho institucional (3 linhas fixas, sem numeração)

**Sempre Multinível**, independentemente da área do estudo:
```
Relatório de Análise de dados
Multinível – Soluções em Psicometria e Análise de dados
Julio Cezar Albuquerque da Costa
```

> **Regra fixa (set/2026):** **nunca usar o cabeçalho NAOPARE.** Relatórios de saúde e
> epidemiologia também levam o cabeçalho Multinível. O `org` do `build_report.py` é
> sempre `"multinivel"`.

- O travessão é "–" (en dash), não hífen.
- Às vezes o título é "Relatório de Consultoria" ou "Relatório psicométrico". O padrão dominante recente (2025–2026) é **"Relatório de Análise de dados"** (só "Relatório" e nomes próprios com maiúscula).
- O cabeçalho NAOPARE é frequente no acervo histórico (91×), mas foi **descontinuado**: não reproduzi-lo.

---

## 2. Macroestrutura (ordem das seções)

```
[Cabeçalho]
Método
  Participantes          (quando há caracterização amostral)
  Análise de dados       (sempre — descreve software + testes)
Resultados
  Estudo 1. [tema]       (quando há objetivos distintos)
  Estudo 2. [tema]
  ...
Referências              (nem sempre presente; em validação/psicometria, sim)
```

- **"Método"** e **"Resultados"** são os dois grandes títulos.
- **"Análise de dados"** é subseção de Método e é o trecho **mais reutilizado** entre relatórios (ver `07-templates-trechos.md`).
- Quando há mais de um objetivo, divide os Resultados em **"Estudo N. [descrição temática]"** — ex.: `Estudo 1. Associações com variáveis categóricas`, `Estudo 2. Diferenças entre os grupos`. Geralmente em negrito no corpo, sem quebrar em nova seção.
- Em relatórios psicométricos a sequência dos blocos é: estrutura interna (AFE/AFC/MEE) → parâmetros dos itens (TRI) → consistência interna → (invariância) → (normas/percentis) → considerações finais.
- Versões em espanhol mantêm o esqueleto: "Resumen ejecutivo → Contextualización → Análisis de datos → Estructura interna → ... → Conclusiones → Referencias → Apéndices".

---

## 3. Voz e tempo verbal

- **Voz passiva sintética (partícula "-se") é obrigatória.** Terceira pessoa, impessoal, pretérito perfeito. **Nunca** primeira pessoa.
- Verbos recorrentes (use estes):
  `investigou-se`, `investigaram-se`, `utilizou-se`, `optou-se`, `observou-se`, `observaram-se`, `analisou-se`, `verificou-se`, `considerou-se`, `realizou-se`, `constatou-se`, `pode-se inferir`, `foi possível observar`, `foram analisados/realizadas`.
- Estrutura nuclear para introduzir uma análise: **"optou-se pela [investigação/realização/utilização] de [técnica], a fim de [objetivo]"**.
- Exemplos verbatim:
  - "investigou-se descritivamente a distribuição de adolescentes..."
  - "optou-se pela utilização de Análises de Variância (ANOVAs) mistas..."
  - "observou-se que a maior parte da amostra foi composta de..."
  - "Posteriormente, optou-se pela investigação dos parâmetros individuais dos itens, a partir do paradigma da Teoria de Resposta ao Item (TRI)."

---

## 3.1. Interpretação acessível dos resultados (traduzir para quem não sabe estatística)

> Pedido explícito do Julio — este é o "calcanhar de Aquiles" da skill. Além de reportar os
> números, **explicar o que significam em linguagem comum**, nomeando os grupos e a direção
> do efeito. Reportar o número **e** traduzi-lo. Mantém-se a voz passiva sintética.

- **Comparações entre grupos** — não basta dizer que houve diferença; dizer **quem** teve
  **mais/menos** de quê, **comparado a quem**:
  - Em vez de: *"Depressão (DASS-21) (p = 0,017; rrb = 0,17, efeito pequeno), com escores superiores entre quem precisou sair de casa"*.
  - Escrever: *"**pessoas que precisaram sair de casa apresentaram maiores níveis de depressão (DASS-21) quando comparadas a quem não precisou sair de casa** (p = 0,017; rrb = 0,17, efeito pequeno)."*
  - Padrão: *"[grupo A] apresentou [maiores/menores] [desfecho] quando comparado a [grupo B] (estatística; tamanho de efeito)."*
- **Efeitos de modelos fatoriais (ANOVA, nparLD, GEE) — dizer o que significam na prática.**
  Não parar no ATS/F/χ² de Wald. Após reportar, traduzir: efeito de **grupo** = os grupos diferiram
  no nível do desfecho considerando os momentos em conjunto; efeito de **momento** = o desfecho
  mudou ao longo do tempo considerando os grupos em conjunto; **interação** = a diferença entre os
  grupos não se manteve constante entre os momentos, isto é, os grupos evoluíram de forma distinta.
  Em seguida, o post hoc diz **quem** mudou e em que direção.
- **Tamanho de efeito considerável sem significância (amostras pequenas).** Quando houver
  comparações não significativas com efeito de magnitude **moderada ou superior**, listá-las e
  registrar que a ausência de significância pode decorrer de limitação do poder amostral, e não
  necessariamente de ausência de efeito. Se os efeitos não significativos forem **pequenos**,
  dizê-lo — não estender o argumento do poder a efeitos de fato reduzidos.
- **Regressão logística — traduzir o OR em chances.** Sempre dizer o que a razão de chances
  significa na prática (OR > 1 aumenta as chances; OR < 1 reduz as chances):
  - Em vez de só: *"variação da Saúde física/mental e vida (QVAS): B = −0,452, OR = 0,64, p = 0,002"*.
  - Acrescentar: *"**Sendo assim, pode-se inferir que o aumento de uma unidade na variação da percepção de saúde física, mental e vida reduz em cerca de 0,64 vez as chances de a pessoa ter precisado sair de casa**"* (equivale a reduzir as chances em torno de 36%).
- **Regressão linear:** *"o aumento de uma unidade em [preditor] associa-se a um aumento/redução
  de [B] em [desfecho]"*, citando o **Beta** como a força padronizada da associação.
- **Mediação — narrar a cadeia causal** (ver `08-convencoes` §5):
  - Em vez de parar em *"(a\*b = 0,111; IC95% [0,042; 0,196]) ... mediação total ... 57%"*.
  - Concluir: *"**Sendo assim, pode-se inferir que a necessidade de sair de casa contribui para a piora da percepção de saúde física e mental, que por sua vez associa-se ao aumento dos níveis de depressão. Por outro lado, não foi observado efeito direto da necessidade de sair de casa sobre a depressão, resultado que se manteve sem significância estatística mesmo considerando o efeito mediador da percepção de saúde física e mental.**"*
- **Sempre citar as estatísticas globais do modelo** ao apresentar regressões: F(gl) ou χ²(gl),
  p, R²/pseudo-R², AIC e BIC (ver `08-convencoes` §4.3).
- **Encadear vários resultados com conectivos, não com ";" em série.** Ao apresentar uma
  sequência de achados no mesmo parágrafo (vários preditores, várias comparações, várias
  mediações), **não** separá-los todos por ponto-e-vírgula — isso cria pausas bruscas e
  trava a leitura. Quebrar em frases ligadas por **conectivos variados**, escolhidos pelo
  sentido:
  - **aditivos** (mesma direção): *Além disso, Ademais, Adicionalmente, Da mesma forma, Outrossim*;
  - **adversativos** (quando a direção se inverte, ex.: de um aumento para uma redução):
    *Por outro lado, Em contrapartida, Contudo, No entanto*;
  - **de consequência** (quando um decorre do outro): *Por conseguinte, Dessa forma, Diante disso*.
  - Alternar os conectivos para não repetir o mesmo (dosagem de vícios, §4); o ";" fica
    reservado a separar dados curtos dentro de um mesmo achado (ex.: "p = 0,017; rrb = 0,17").
  - Ex.: em vez de *"…reduziu as chances…; estar na categoria X aumentou…; o aumento em Y reduziu…"*,
    escrever *"…reduziu as chances… Por outro lado, estar na categoria X aumentou… Ademais, o aumento em Y reduziu…"*.
- A **classificação** do tamanho de efeito segue os **pontos de corte** (§8) — muda a redação,
  não o critério. (No exemplo acima, rrb = 0,17 é **pequeno**, abaixo de 0,20.)

---

## 4. Vícios de linguagem característicos (reproduzir com moderação)

**Frequências reais no corpus (328 relatórios)** — quanto maior, mais "Julio":

| Conector / vício | Ocorrências | Como usar |
|---|---|---|
| **"Além disso,"** | 963 | Adição. O mais usado de todos. |
| **"Ademais,"** | 692 | Sinônimo de "Além disso"; alternar entre os dois. |
| **"A partir disso,"** | 677 | Conector de consequência. **Marca registrada.** Não abrir vários parágrafos seguidos com ele. |
| **"Posteriormente,"** | 532 | Sequência temporal entre análises. |
| **"Por fim,"** | 470 | Fechamento de bloco. |
| **"Finalmente,"** | 328 | Última análise da sequência. |
| **"Inicialmente,"** | 293 | Abertura dos Resultados / primeira análise. |
| **"Quanto a / Quanto à"** | 280 | Mudança de tópico ("Quanto à amostra..."). |
| **"Diante disso,"** | 115 | Consequência (variante de "A partir disso"). |
| **"utilizou-se DE / DA / DO"** | — | Com preposição: "utilizou-se **de** estatísticas descritivas". Vício-assinatura. |
| **"através de / do / da"** | — | Instrumental: "através do teste de Shapiro-Wilk". Alternar com "por meio de". |
| **"sendo"** | — | Enumerativo: "testes não paramétricos, **sendo** o teste de Mann-Whitney...". |
| **"apresentou/apresentaram resultados [qualificador]"** | — | "apresentou resultados adequados/satisfatórios/excelentes/questionáveis". |
| **"Já quando considerado(a)..."** | — | Transição para subgrupo/resultado secundário. |
| **"pode-se inferir que"** | — | Conclusão parcial cautelosa. |

> **Regra de dosagem (pedido explícito do Julio):** manter a voz, mas reduzir a densidade de vícios — não abrir vários parágrafos seguidos com "A partir disso,"; alternar "Além disso/Ademais"; variar "através de" com "por meio de"; não repetir "possíveis associações" em excesso. Meta: soar como ele, com ~70–80% da densidade original de conectores.

---

## 5. Frases-fórmula (usar literalmente)

**Remissão a tabela/figura** (fórmula nuclear — "podem ser conferidos na" aparece **628×**; "pode ser conferido na" 76×; "podem ser conferidas na" 66×; "pode ser conferida na" 32×; "podem ser observados na" 15×):
- "Os resultados podem ser conferidos na Tabela X."
- "Os resultados detalhados podem ser conferidos na Tabela X."
- "Os resultados podem ser conferidos na Tabela X, bem como [complemento]."
- "..., os resultados podem ser conferidos na Tabela X, e apontam que [achado]."
- "As cargas fatoriais podem ser conferidas na Tabela X."
- "Os índices de ajuste do modelo podem ser conferidos na Tabela X."
- "Os parâmetros dos itens podem ser conferidos na Tabela X."
- "As curvas características dos itens podem ser observadas na Figura X."
- "O modelo confirmatório pode ser conferido na Figura X."
- Variante "conforme aponta": "conforme aponta a Tabela X" / "conforme detalha a Tabela X".

**Abertura de Resultados:**
- "Inicialmente, investigou-se descritivamente [...]. Os resultados podem ser conferidos na Tabela 1."

**Caracterização da amostra:**
- "Contou-se com a participação de N pessoas, com idades variando entre X e Y anos (M= X,XX, DP= X,XX), sendo a maior parte da amostra composta de pessoas do sexo feminino (XX,X%)..."
- "a maior parte da amostra foi composta de pessoas do sexo masculino (73,79%), autodeclaradas pessoas pardas (66,02%), com ensino médio completo (33,01%)..."

---

## 5.1. O que NÃO entra na seção "Análise de dados" (regra set/2026)

> O relatório é insumo de **peça científica** (artigo, dissertação, tese). O Método relata o
> que o leitor precisa para **julgar e reproduzir** os resultados, não o diário do tratamento
> da base.

**Entra:** o software e os testes com suas citações; o tratamento de **dados faltantes** (e
sobre que denominador os percentuais foram calculados); **exclusão de casos ou registros**, com
o motivo; **arbitragem entre fontes conflitantes** quando muda o resultado; variáveis que
**ficaram de fora** e por quê.

**Não entra** (é operação óbvia de preparo, vive no script e no parecer, não no relatório):
- transformar texto livre ou descrições em categorias, e derivar variáveis desse texto;
- corrigir erro de digitação, unificar grafia, caixa e acentuação de rótulos;
- agrupar categorias de baixa frequência, quando o agrupamento já é visível na tabela;
- coerção de tipo, renomeação de colunas, remoção de linhas vazias;
- qual coluna redundante foi mantida entre duas equivalentes.

Regra prática: se a frase descreve algo que **qualquer analista faria da mesma forma** e que
não altera a interpretação do resultado, ela sai do relatório. Se um revisor pudesse
questionar a escolha, ela fica.

---

## 5.2. O relatório reporta o resultado, não o percurso (regra set/2026 — pedido explícito do Julio)

> Origem: revisão do relatório Jade E3, em que o Julio marcou em **vermelho** (remover) e
> **amarelo** (vício de IA) trechos com um denominador comum. **Nada disto entra em nenhum
> relatório gerado por esta skill.**

O Método e os Resultados são peça **publicável**. Descrevem a especificação adotada e o que
foi encontrado. **Não** descrevem o caminho até ela, o que foi descartado, as limitações do
ferramental estatístico, nem a diligência do analista.

**Proibido — com os exemplos reais que motivaram a regra:**

| Categoria | Exemplo removido | Por quê |
|---|---|---|
| **Narrar o que não pôde ser feito** | "Observou-se que as distribuições gama, normal inversa e de Poisson não puderam ser ajustadas, uma vez que exigem valores estritamente positivos… Investigou-se ainda a família de Tweedie, em 5 valores do parâmetro… Nenhum deles se mostrou estimável" | Tentativas frustradas vivem no script. O relatório informa a distribuição **adotada**. |
| **Explicar limitação teórica do próprio método** | "considerando que as Equações de Estimação Generalizadas não se apoiam em uma função de verossimilhança plena, razão pela qual não produzem os critérios de informação de Akaike e Bayesiano" | O leitor não precisa de aula sobre o estimador. Diga o que foi feito ("a partir dos resíduos de Pearson") e siga. |
| **Reportar seleção de componentes acessórios** | "Quanto à matriz de correlação de trabalho, as quatro estruturas comparadas através do QIC apresentaram valores praticamente idênticos… manteve-se a estrutura permutável" | Em GEE, reportar **função de ligação e distribuição**. Estrutura de correlação, otimizador, critérios de convergência ficam de fora. |
| **Justificar a própria diligência** | "de modo que a distribuição de trabalho não fosse assumida por convenção"; "condição prévia a qualquer escolha de modelo" | Autoelogio metodológico. O rigor aparece no resultado, não no anúncio dele. |
| **Remeter a arquivos de trabalho** | "As estatísticas completas… encontram-se no arquivo de saída das análises" | **Nunca** mencionar saída, output, CSV, planilha de resultados ou pasta do projeto. Nada disso é publicado. |
| **Explicar decisão de visualização na legenda** | "Nota. O eixo horizontal foi ajustado à região central de cada distribuição, de modo que valores extremos situam-se fora da área visível." | A legenda nomeia o que a figura mostra. Ajuste de eixo, número de *bins*, transparência e afins não entram. |

**Teste prático:** se a frase descreve **o analista trabalhando** (testou, verificou, descartou,
constatou que não dava, tomou o cuidado de) em vez de **o estudo encontrando**, ela sai.

---

## 5.3. Dois-pontos explicativo — vício de IA, proibido (regra set/2026)

**Nunca** usar dois-pontos no corpo do texto para anunciar uma explicação, uma conclusão ou
uma reformulação. É a construção que mais denuncia texto gerado por IA e **não existe** no
acervo do autor.

- ❌ "A inspeção visual confirma a leitura: a curva normal mostra-se excessivamente achatada…"
- ✅ "A inspeção visual confirma a leitura, uma vez que a curva normal mostra-se excessivamente achatada…"
- ❌ "A primeira delas diz respeito à própria variável desfecho: as distribuições apresentaram…"
- ✅ "A primeira delas diz respeito à própria variável desfecho, cujas distribuições apresentaram…"

Formas de reescrever, na ordem de preferência: oração relativa ("cujo", "o que", "uma vez
que"), vírgula com conector ("pois", "dado que", "de modo que"), ou dois períodos separados.

**Única exceção mantida:** enumeração anunciada por **"a saber:"** — idioma do próprio autor
("os oito eletrodos investigados, a saber: Fp1, Fp2, …"). Fora dela, sem dois-pontos.

Vale para o mesmo padrão com travessão e parênteses explicativos em série, já coberto no §7.1.

---

## 6. Padrão de parágrafo

- **Análise de dados (Método):** parágrafos LONGOS (4–7 frases). Em relatórios com muitos testes, 2–4 parágrafos: (1) descritiva + normalidade; (2) testes de diferença + tamanho de efeito; (3) testes de associação + post hoc; (4) modelos especiais (ANOVA mista/nparLD/TRI/SEM). Cada teste seguido **imediatamente** da citação entre parênteses.
- **Resultados:** parágrafos MÉDIOS (3–5 frases), seguindo o ciclo:
  `conector de transição → o que foi investigado (verbo "-se") → remissão à Tabela/Figura → interpretação dos achados principais (com pontos de corte)`.
- **Um parágrafo = uma análise = uma tabela/figura.**
- Frases longas, com orações subordinadas e enumerações separadas por vírgula.

---

## 6.1. Notas de rodapé de tabela (padrão recorrente)

Abaixo das tabelas, o Julio insere uma **"Nota."** explicando abreviações. Exemplos verbatim:
- "Nota. M: Média; DP: Desvio Padrão; Q: Quartis; Min: valor Mínimo; Max: valor Máximo; W: teste de Shapiro-Wilk; p: Nível de significância do teste de Shapiro-Wilk."
- "Nota. *Resultados significativos no teste de qui-quadrado; n: Número de pessoas no grupo; %: Percentual; Dif (%): Diferença nos percentuais por grupo; p: Nível de significância do teste de qui-quadrado; V: Estimativa do tamanho do efeito; **Negrito**: Teste post hoc com significância estatística, indica prevalência de determinada categoria de resposta."
- Tabelas de confiabilidade: "*⍺ (alfa de Cronbach); **⍵ (ômega de McDonald); ***CC (Confiabilidade Composta); ****AVE (Variância Média Extraída)."
- Tabelas geradas no Factor/Excel: "Fonte: Elaborado pelo autor."

---

## 7. Convenções numéricas

- **Vírgula decimal sempre** (padrão PT-BR): `0,20`; `1,96`; `p = 0,001`.
- Médias e desvios: **"M= 82,39, DP= 7,12"** (espaço depois do "="; abreviações M e DP em maiúsculas).
- Percentuais: 1–2 casas decimais com vírgula: `73,79%`, `65,4%`.
- Resíduos padronizados ajustados: **"SR = X,XXX"** (3 casas). Significância em χ² post hoc: `|SR| ≥ 1,96`.
- p-valores: `p = 0,032` ou `p < 0,001`.
- Símbolos: `χ²`, `≥`, `≤`, `λ`, `⍺`, `⍵`, `η²`, `ε²`, `ρ`. Tamanho de efeito: `r`, `V`, `d`, `rrb` (rank-biserial).
- Índices de ajuste reportados inline entre colchetes: `[χ² = 1073,212, gl = 270, χ²/gl = 3,974, CFI = 0,933, TLI = 0,926; RMSEA (95% CI): 0,077 (0,072 a 0,082); SRMR = 0,080]`. (Intervalos no texto com "a", não com traço — ver §7.1.)

---

## 7.1. Símbolos e hífen no corpo do texto (regras de pontuação — pedido do Julio)

- **Proibido hífen/travessão ("-", "–", "—") no corpo do texto**, com duas exceções:
  (a) **termos compostos** que o exigem (qui-quadrado, Mann-Whitney, Shapiro-Wilk,
  Kruskal-Wallis, rank-biserial, DASS-21, WHOQOL-BREF) e (b) **referências** (nomes,
  intervalos de página). Se evitar o traço exigir escrever mais, escreva mais.
  - Intervalos: "de 1 a 3 salários mínimos" (nunca "1-3 SM"); "entre 0,072 e 0,082";
    "idade de 18 a 65 anos".
  - Travessão de aposto: trocar por vírgula, parênteses, "ou seja", "a saber" ou ":".
  - Rótulos de variável com traço (ex.: "Saúde física/mental e vida — variação") são
    **reescritos por extenso no texto** ("a variação da percepção de saúde física, mental e
    vida"); o rótulo com traço fica **só na tabela**.
  - **Valores negativos:** no texto, descrever o sentido ("coeficiente negativo", "redução");
    o número com sinal (B = −0,452) fica **na tabela**.
- **Símbolos não convencionais ficam restritos a tabelas, figuras e notas.** Em especial,
  **não usar "→" no corpo do texto** (típico de mediação): a cadeia é **narrada por extenso**
  (§3.1). Setas, `*`, `#`, `‡` etc. vivem nas tabelas/figuras e são explicados na nota.
- Exceção fixa: o **cabeçalho institucional** mantém o en dash "–" ("Multinível – Soluções…"),
  por ser parte do nome da marca, não corpo de texto.

---

## 8. Como cada teste é reportado (com pontos de corte verbatim)

- **Normalidade:** "...através do teste de Shapiro-Wilk, com resultados significativos indicando assimetria significativa da distribuição (Miot, 2017)."
- **Tamanho de efeito rank-biserial (Mann-Whitney/Wilcoxon):** "indica diferença pequena quando 0,20, diferenças moderadas quando 0,50 e grande diferença entre os grupos quando alcançados valores de 0,80 (Serdar, Cihan, Yücel & Serdar, 2021)."
- **V de Cramér:** "resultados 0,10 indicam associação fraca, valores 0,30 sugerem associações moderadas e resultados 0,50 indicam associação forte (Serdar, Cihan, Yücel & Serdar, 2021)."
- **Resíduos padronizados ajustados:** "os testes post hoc do χ2 foram analisados através da análise dos resíduos padronizados ajustados, nos quais resultados ≥ 1,96 apontam associações significativas na tabela de referência cruzada (Sharpe, 2015)."
- **Apresentação de qui²/Fisher (regra fixa):** sempre como **tabela de referência cruzada** com a variável fixa do estudo nas **colunas** (n e % por coluna); **não** usar coluna "Teste" — sinalizar o teste por **símbolo** no nome da variável (`*` qui-quadrado, `#` Fisher) e explicar na nota; marcar em **negrito** as células com |SR| ≥ 1,96. Ver `08-convencoes-tabelas-figuras.md`.
- **Regressão logística (regra fixa):** reportar **B e OR** (não só OR), com IC95% do OR e p. Ver `08-convencoes-tabelas-figuras.md` §4.
- **Heatmap de correlação (regra fixa):** colorbar −1..+1, coeficiente em cada célula, texto adaptativo. **Mediação/moderação (regra fixa):** gerar figura com coeficientes nas setas. Ver `08-convencoes-tabelas-figuras.md` §3 e §5.
- **eta² (η², tamanho de efeito Kruskal-Wallis):** "com valores baixos de 0,01 até 0,06, moderados de 0,06 até 0,14 e acima de 0,14 como altos (Serdar, Cihan, Yücel & Serdar, 2021)."
- **Índices de ajuste (AFC/SEM) — fórmula verbatim:** "(a) χ², com valores adequados quando p < 0,05; (b) χ²/gl, satisfatório quando < 5 [preferencialmente < 3]; (c) CFI e (d) TLI, bons quando > 0,90 e excelentes se ≥ 0,95; (e) RMSEA, adequado com ≤ 0,08, com limite superior do IC < 0,10; e (f) SRMR, satisfatório quando ≤ 0,08 (Hair et al., 2009; Kline, 2016; Brown, 2015)."
- **Confiabilidade:** "para todos os coeficientes de consistência interna, esperam-se resultados acima de 0,70 (Bland & Altman, 1997; Hayes & Coutts, 2020)." Coeficientes: ⍺ de Cronbach, ⍵ de McDonald, CC. AVE > 0,50.
- **Cargas fatoriais:** "todas as cargas fatoriais apontando resultados significativos e com magnitude suficiente para saturação dos itens nos fatores latentes estimados (λ > |0,30|, p < 0,05)" (Hair et al., 2009).
- **KMO:** "valores iguais ou superiores a 0,60 indicando resultados aceitáveis" (Kaiser, 1974); 0,80–0,90 ótimos, > 0,90 excelentes (Hutcheson & Sofroniou, 1999). Bartlett deve ser significativo (p < 0,05).
- **TRI — discriminação (a), critério de Pasquali (2020), verbatim:** "muito baixa (0,01 – 0,34), baixa (0,35 – 0,64), moderada (0,65 – 1,34), alta (1,35 – 1,69) e muito alta (acima de 1,70)". Dificuldade (b): amplitude entre -3 e +3.
- **Curva ROC / AUC:** "valores substancialmente altos (AUC = 0,915, IC95% = 0,888 – 0,942, p < 0,001)"; ponto de corte ótimo via índice de Youden.
- **Correlação:** Pearson (dados normais) e Spearman/ρ (assimétricos), ambos → (Miot, 2018). Magnitude (Cohen, 1992): pequena ~0,10; moderada ~0,30; forte ~0,50.

---

## 9. Conclusões / considerações finais

- Tom assertivo e técnico. Retomam: (a) estrutura/achado principal, (b) consistência/qualidade psicométrica, (c) recomendação de uso ou síntese prática.
- Em psicometria: confirmam estrutura fatorial, consistência interna satisfatória e recomendam o uso do instrumento. Apontam limitações (ex.: amostra ideal por número de parâmetros, segundo Kyriazos, 2018).
- Frases verbatim: "A partir dos resultados encontrados nas diversas técnicas psicométricas empregadas no estudo das evidências de validade do [instrumento], é possível inferir que..."; "Em conjunto, os resultados indicam que o [instrumento] apresenta evidência empírica suficiente de validade estrutural, qualidade de itens e confiabilidade para seu uso."
- Quando solicitado, há versão "reduzida" do relatório (mesmo conteúdo, menos detalhamento metodológico).

---

## 10. Checklist de fidelidade (rodar mentalmente antes de entregar)

- [ ] Cabeçalho de 3 linhas Multinível (**nunca** NAOPARE).
- [ ] Voz passiva sintética em 100% das descrições metodológicas.
- [ ] Cada teste com citação imediata entre parênteses (ver `02-referencias-por-teste`).
- [ ] Pontos de corte explicitados ao interpretar tamanho de efeito/ajuste.
- [ ] Fórmula "Os resultados podem ser conferidos na Tabela X" antes de cada tabela.
- [ ] Vírgula decimal; "M= X, DP= X".
- [ ] Conectores de transição abrindo parágrafos — **sem** repetir "A partir disso," em excesso.
- [ ] Um parágrafo por análise/tabela.
- [ ] Títulos no padrão "Tabela N. Título" (acima) / "Figura N. Título" (abaixo).
- [ ] Nota de rodapé explicando abreviações sob cada tabela.
- [ ] Seção Referências em APA 7, ordem alfabética, só com o que foi citado.
- [ ] **Nenhum dois-pontos explicativo no corpo do texto** (só "a saber:") — §5.3.
- [ ] **Nenhuma menção a arquivo de saída, output, CSV ou pasta do projeto** — §5.2.
- [ ] **Nenhum relato do que foi testado e descartado**, de limitação do método estatístico, de seleção de estrutura de correlação, nem de autojustificação metodológica — §5.2.
- [ ] **Legendas de figura sem explicação de ajuste de eixo ou de parâmetro gráfico** — §5.2.
