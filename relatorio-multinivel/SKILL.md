---
name: relatorio-multinivel
description: >-
  Gera relatórios de consultoria em análise de dados/psicometria no estilo da empresa Multinível (Julio Cezar).
  Use quando o usuário tiver uma base de dados (.xlsx/.csv/.sav) e quiser: (1) definir ou aplicar um delineamento
  estatístico (testes), (2) gerar código R que roda as análises, e (3) escrever o relatório final no estilo da
  Multinível — voz passiva, vícios de linguagem do autor, tabelas APA (Times New Roman 12/tabelas 10,
  entrelinha 1,5), referências por teste em APA 7, pacotes R habituais e gráficos. Gatilhos: "relatório Multinível",
  "relatório de análise de dados", "analisar essa base e escrever o relatório", "delineamento estatístico",
  "relatório psicométrico", "AFE/AFC/TRI/qui-quadrado e escrever no meu estilo".
---

# Relatório Multinível — análise de dados + redação no estilo do Julio

Esta skill reproduz o fluxo de consultoria da **Multinível**: ler a base de dados →
definir (ou aplicar) o delineamento estatístico → escrever o código R → rodar as análises →
**escrever o relatório** fiel ao estilo do autor, cobrindo os 6 tópicos: (1) estilo de escrita,
(2) formatação, (3) referências por teste, (4) gráficos, (5) APA 7, (6) pacotes R.

## Arquivos de referência (LEIA conforme a necessidade)

Estão em `references/` (todos destilados de 328 relatórios reais):

| Arquivo | Use quando |
|---|---|
| `01-estilo-de-escrita.md` | **Sempre.** Voz, vícios de linguagem (com frequências), frases-fórmula, parágrafos, cortes verbatim, checklist. |
| `02-referencias-por-teste.md` / `.json` | Para escolher a citação certa de cada teste. O `.json` é para lookup programático. |
| `03-referencias-apa7.md` | Para montar a seção Referências (entradas APA 7 completas). |
| `04-pacotes-r.md` | Para escolher pacotes/funções R por análise + preâmbulo `pacman::p_load`. |
| `05-graficos.md` | Para replicar gráficos do autor ou propor novos (com código ggplot2 + tema). |
| `06-formatacao-apa7.md` | Para a formatação Word/APA (fontes, tabelas Estilo2, margens). |
| `07-templates-trechos.md` | Blocos verbatim de "Análise de dados" e fórmulas de Resultados, prontos para adaptar. |

## Scripts de apoio (em `assets/`)

- `assets/setup_workspace.py` — **monta o workspace local-first** em `~/Downloads/Relatórios Automatizados/<Projeto>/`: copia a(s) base(s) e os scripts de apoio para lá e cria `saida_tabelas/`/`saida_figuras/`. Rode no início (ver Passo 0.5).
- `assets/sync_to_drive.py` — **leva o resultado final para o Drive** (única cópia para o Drive, no fim). Copia entregáveis + figuras + tabelas; `--tudo` copia a pasta inteira.
- `assets/build_report.py` — gera o `.docx` final já formatado (TNR 12, entrelinha 1,5, 12pt depois, tabelas APA Estilo2, legendas, referências com recuo deslocado). Lê um JSON de conteúdo. **Insere a logo horizontal da Multinível no topo da primeira página** (centralizada, 5,5 cm, acima do cabeçalho de 3 linhas; `logo-multinivel-horizontal.png` ao lado; desligar com `--sem-logo` ou `"options": {"logo": false}`; `logo_largura_cm` ajusta) e **aplica a marca d'água da Multinível por padrão** (ver `marca_dagua.py`; `--sem-marca` desliga). Requer `python-docx`.
- `assets/marca_dagua.py` — **marca d'água da Multinível** (símbolo rede-M da versão atual da marca, em verde g-600: nós a 16% e traços a 10%, 13 cm, centralizada, atrás do texto, em todas as páginas; gerado a partir do vetor oficial do logo, out/2026). O `build_report.py` importa `marcar_document()` daqui e **já aplica a marca em todo `.docx` gerado** (desligar: `"options": {"marca_dagua": false}` no JSON ou `--sem-marca`; ajustes: `marca_dagua_largura_cm`, `marca_dagua_pular_primeira`). Para relatórios já existentes ou `.pdf`: `python3 marca_dagua.py relatorio.docx` gera `relatorio (marca d'água).docx` (`--no-lugar` sobrescreve, `--pular-primeira` poupa a capa). Usa o `marca-dagua-multinivel.png` ao lado (ambos copiados para o `PROJETO_DIR` pelo `setup_workspace.py`, junto com `logo-multinivel-horizontal.png`). Fonte dos dois PNG (SVG, gerador e versões por tema do site): `2. Multinível/Logos multinível/Logos por tema (site)/` (ver `LEIA-ME.md` e `_fonte/`); a marca d'água antiga, com sombras, segue em `4. Imagens/Multinível - Sonar/Design System/assets/marca-dagua/`.
- `assets/analise_template.R` — esqueleto de script R que carrega a base, roda o delineamento (descritiva → normalidade → testes → efeito → post hoc; e blocos de AFE/AFC/TRI/redes), exporta tabelas (.csv) e figuras (.png) com o tema Multinível.
- `assets/explore_data.py` — perfila rapidamente a base (tipos de variável, n, faltantes, níveis) para ajudar a sugerir o delineamento sem depender do R.

> **Atalho:** a skill canônica fica em `~/.claude/skills/relatorio-multinivel/`. Nos comandos abaixo, `$SKILL` = esse caminho.

## Procedimento (siga em ordem)

### Passo 0 — Entender o pedido e a base
1. O cabeçalho é **sempre Multinível**, qualquer que seja a área do estudo (psicometria, saúde, epidemiologia). **Nunca usar NAOPARE.**
2. Localize a base (`.xlsx`, `.csv`, `.sav`). Se não houver, peça. **Não rode análises ainda no caminho do Drive** — primeiro monte o workspace local (Passo 0.5).
3. Defina o **nome do projeto** (vira o nome da pasta). Use algo legível, ex.: "Relatório TCC Ricardo", ou o nome do projeto R. Confirme com o usuário se houver dúvida.

### Passo 0.5 — Workspace local-first (trabalhar em disco local, sincronizar só no fim)
> O Google Drive é a maior fonte de lentidão/instabilidade. **Todo o trabalho roda local**; só o resultado final vai para o Drive (Passo 5).

1. Monte o workspace e traga as bases + scripts para o disco local:
   ```
   python3 "$SKILL/assets/setup_workspace.py" "<Nome do Projeto>" "<caminho/da/base.xlsx>"
   ```
   Isso cria `~/Downloads/Relatórios Automatizados/<Nome do Projeto>/` com a(s) base(s) copiada(s), os scripts de apoio (`analise_template.R`, `build_report.py`, `explore_data.py`, `marca_dagua.py` e os PNGs da logo e da marca d'água) e as subpastas `saida_tabelas/` e `saida_figuras/`. Anote o caminho impresso em `PROJETO_DIR=...` — **ele é o diretório de trabalho de tudo a seguir**.
   **Rode este comando mesmo que a pasta do projeto já exista** (projeto antigo, retomado ou criado por outra sessão): ele não apaga nada e **atualiza os scripts de apoio para a versão atual da skill** (pode ser chamado só com o nome do projeto, sem bases). Cada projeto trabalha com uma *cópia* dos scripts; uma cópia antiga de `build_report.py` gera relatório **sem logo e sem marca d'água** (foi o que aconteceu em 22/10/2026). Nunca edite o `build_report.py` dentro do projeto: ajuste pelo `options` do JSON.
2. **A partir daqui, todos os comandos rodam dentro de `PROJETO_DIR`** (e referenciam scripts/bases por nome simples, pois já estão lá). Nunca leia/escreva intermediários no Drive.
3. Perfile a base **local**: `python3 explore_data.py <base.xlsx>` (rodando em `PROJETO_DIR`) para saber variáveis, tipos, n e faltantes. Não invente nomes de colunas — confirme.

### Passo 1 — Delineamento estatístico
- **Se o usuário já forneceu o delineamento**, aplique-o.
- **Se não**, proponha-o a partir das variáveis e do objetivo, seguindo a árvore de decisão em `assets/analise_template.R` (topo do arquivo) e o mapa de `02-referencias-por-teste.md`. Princípios do autor:
  - Variável numérica: descritiva + **Shapiro-Wilk**; se assimétrica → não-paramétrico.
  - 2 grupos → **Mann-Whitney** (ou t); 3+ → **Kruskal-Wallis** + **Dunn/Holm**; pareado → Wilcoxon; longitudinal → **nparLD**.
  - Categóricas → **qui-quadrado/Fisher** + **resíduos padronizados (≥1,96)** + **V de Cramér**.
  - Correlação → Pearson/Spearman conforme normalidade.
  - Validação de escala → AFE → AFC/MEE (lavaan, WLSMV) → consistência interna → TRI (mirt) → invariância.
- **Confirme o delineamento com o usuário** antes de escrever muito código, salvo se ele pediu para seguir direto.

### Passo 2 — Código R (dentro do `PROJETO_DIR`)
- Parta do `analise_template.R` (já copiado para o `PROJETO_DIR`) e salve o script adaptado **na própria pasta do projeto** (ex.: `analise_projeto.R`), apontando para a base local. Adapte aos nomes reais das colunas e ao delineamento.
- Use o preâmbulo `pacman::p_load(...)` de `04-pacotes-r.md`. Use só os pacotes necessários.
- O script deve **exportar**: tabelas como `.csv` (em `saida_tabelas/`) e figuras como `.png` (em `saida_figuras/`, tema Multinível) — tudo relativo ao `PROJETO_DIR`.
- Rode o R **com o `PROJETO_DIR` como working dir** e **forçando UTF-8** (senão os acentos corrompem ao gravar arquivos):
  ```
  LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 Rscript -e 'setwd("<PROJETO_DIR>"); source("analise_projeto.R")'
  ```
  (ao escrever JSON/CSV pelo R, use `writeLines(enc2utf8(x), arquivo, useBytes=TRUE)`).
- Se o R não estiver disponível, entregue o script para o usuário rodar e peça os outputs. **Nunca invente resultados numéricos** — use os reais do R ou deixe placeholders claros (`[x]`) se ainda não houver dados.

### Passo 3 — Escrever o relatório (os 6 tópicos)
Monte o conteúdo seguindo `01-estilo-de-escrita.md` e `07-templates-trechos.md`:
1. **Cabeçalho** (3 linhas, sempre Multinível). A logo horizontal entra sozinha acima dele, pelo `build_report.py`; não a repita no conteúdo.
2. **Método › Análise de dados** — adapte o bloco verbatim do template ao delineamento; cada teste com sua citação (`02-referencias-por-teste`).
3. **Método › Participantes** (se houver caracterização).
4. **Resultados** — um parágrafo por análise/tabela, com a fórmula "Os resultados podem ser conferidos na Tabela X" + interpretação com pontos de corte. Divida em "Estudo N." se houver múltiplos objetivos.
5. **Considerações finais** (quando pertinente).
6. **Referências** — APA 7, só as citadas, de `03-referencias-apa7.md`.
Respeite a **dosagem de vícios** (§4 do guia): soar como o autor, sem repetição excessiva.

### Passo 4 — Gerar o documento (dentro do `PROJETO_DIR`)
- Monte um JSON de conteúdo (estrutura em `build_report.py`, topo) e rode, **na pasta do projeto**:
  `python3 build_report.py conteudo.json relatorio.docx`
- **Atenção ao working dir:** o `build_report.py` resolve as figuras pelo caminho **relativo ao cwd** (ex.: `saida_figuras/fig.png`). Se rodar do diretório errado, as figuras somem do `.docx` **sem erro**. Garanta cwd = `PROJETO_DIR`. Forma prompt-free (sem `cd`):
  ```
  python3 -c "import os,sys,runpy; os.chdir('<PROJETO_DIR>'); sys.argv=['build_report.py','conteudo.json','relatorio.docx']; runpy.run_path('build_report.py',run_name='__main__')"
  ```
  Confira depois que o `.docx` tem `word/media/` preenchido e os acentos íntegros (sem mojibake).
- **Logo e marca d'água:** o `build_report.py` já insere a logo no topo da primeira página (o terminal imprime `Logo Multinível inserida no topo`) e a marca da Multinível em todas as páginas (`Marca d'água Multinível aplicada`; no `.docx`, o cabeçalho traz a imagem `Marca d'água Multinível`). Só desligue se o Julio pedir (`--sem-logo`, `--sem-marca`). Se o relatório também for entregue em `.pdf`, exporte pelo Word (a marca vai junto) ou carimbe o PDF com `python3 marca_dagua.py relatorio.pdf --no-lugar`. **Confira as duas linhas no terminal a cada geração**; o `build_report.py` também imprime a própria versão e avisa `[ATENÇÃO] ... DESATUALIZADO` quando a cópia do projeto está atrás da skill. Se faltar linha ou aparecer `[AVISO]`/`[ATENÇÃO]`, rode `setup_workspace.py "<Nome do Projeto>"` de novo e gere outra vez. Não entregue relatório sem logo e marca d'água.
- Entregue **ambos**: o `.docx` formatado **e** o Markdown/`.R` fonte (preferência do Julio: "Ambos"). Tudo fica no `PROJETO_DIR`.
- Rode o **checklist de fidelidade** (§10 do guia) antes de entregar.

### Passo 5 — Levar o resultado para o Google Drive (só no fim)
> Esta é a **única** cópia para o Drive — feita quando tudo está pronto e validado.

- Confirme com o usuário a pasta destino no Drive (em geral a pasta original do projeto).
- Rode:
  ```
  python3 "$SKILL/assets/sync_to_drive.py" "<PROJETO_DIR>" "<pasta destino no Drive>"
  ```
  Por padrão leva os entregáveis + `saida_figuras/` + `saida_tabelas/` (sem reenviar a base bruta). Use `--tudo` para copiar a pasta inteira.
- Informe ao usuário **os dois caminhos**: o local (`PROJETO_DIR`, onde tudo foi gerado) e o do Drive (cópia final).

## Regras de ouro
- **Reprodutibilidade de procedimentos aleatórios.** Todo teste com reamostragem ou simulação
  (permutação, bootstrap, `fisher.test(simulate.p.value = TRUE)`, `npar.t.test(method = "permu")`,
  `npar.t.test.paired`) recebe `set.seed()` **imediatamente antes da chamada**. Sem isso o p-valor
  muda a cada execução e o número publicado não é reproduzível. Conferir rodando o script duas vezes.
- **Marcação no conteúdo:** o `build_report.py` interpreta `**negrito**` e `*itálico*` em
  parágrafos, células, notas e referências (itálico de periódico e volume nas referências APA).
  Asteriscos de significância colados ao número (`5,708*`) ou soltos (`* p < 0,05`) ficam literais.
- **Local-first sempre.** Trabalhe em `~/Downloads/Relatórios Automatizados/<Projeto>/` (uma pasta por projeto/banco), com a base e os scripts copiados para lá. O Drive recebe **uma única cópia, no fim** (Passo 5). Nunca rode análises lendo/escrevendo direto no Drive.
- **Logo e marca d'água Multinível em todo relatório** (padrão do `build_report.py` desde out/2026): logo horizontal no topo da primeira página e símbolo rede-M claro atrás do texto, os dois na versão atual da marca (a do site). Não remover sem pedido do Julio.
- **Voz passiva sintética sempre** ("investigou-se", "utilizou-se", "optou-se"). Nunca 1ª pessoa.
- **Toda menção a teste vem com a citação** que o Julio usa (Shapiro→Miot 2017; resíduos→Sharpe 2015; qui-quadrado→Kim 2017; Mann-Whitney→Brunner et al. 2018; Kruskal/Dunn→Pohlert 2014; V de Cramér/efeito→Serdar et al. 2021; correlação→Miot 2018; KMO/Bartlett/AFE→Damásio 2012; ajuste→Hair et al. 2009 + Kline 2016; invariância→Cheung & Rensvold 2002; TRI→Samejima 1969/Chalmers 2012/Pasquali 2020).
- **Sempre explicitar pontos de corte** ao interpretar tamanho de efeito e índices de ajuste.
- **Interpretar para leigos** (calcanhar de Aquiles da skill). Além do número, traduzir: nomear grupos e direção nas comparações ("[grupo A] apresentou maiores [X] que [grupo B]"); traduzir o **OR em chances**; **narrar a cadeia causal** da mediação. Ver `01-estilo` §3.1.
- **Sem símbolos no corpo do texto.** Proibido "→"; proibido hífen/travessão ("-", "–", "—") salvo termos ("qui-quadrado") e referências; intervalos com "a" ("de 1 a 3 SM"). Símbolos só em tabelas/figuras/notas. Ver `01-estilo` §7.1.
- **Tabelas de teste sem coluna "Teste":** identificar o teste por símbolo + nota (vale também para Mann-Whitney/comparações); tamanho de efeito em coluna própria. Ver `08-convencoes` §2.
- **Regressão:** categoria de referência como **1ª informação da nota** (default = grupo de maior frequência; ou o grupo de interesse do estudo); reportar B e OR (logística) ou B e Beta (linear) **+ estatísticas do modelo** (F ou χ², p, R²/pseudo-R², AIC, BIC). Ver `08-convencoes` §4.
- **Mediação/moderação:** estimar **sempre em duas versões — bruta e ajustada** (idade e sexo/gênero + covariáveis do estudo), apresentadas lado a lado, com FDR por versão; tabela de mediação com a, b, (a\*b), c, c′. Ver `08-convencoes` §5.
- **Vírgula decimal**; "M= X, DP= X"; tabelas 10pt estilo APA (só bordas horizontais); legendas de tabela acima, de figura abaixo.
- **Não inventar dados.** Resultados vêm do R; na ausência, placeholders explícitos.
- Atualizar **R Core Team** para o ano corrente do relatório.
- **Convenções jun/2026 (Cristiane Peçanha):** parágrafos com **recuo de 1ª linha** (1,25 cm); tabelas com **autoajuste de conteúdo** e **título como 1ª linha mesclada e sem bordas** (já no `build_report.py`); **ANOVA com post hoc de Holm** (Chen, Feng & Yi, 2017), não Tukey; **regressão citando Field (2020)** (não Damásio 2013); **moderação com amostra pequena via análise estratificada** por subgrupos (não termo de interação); **rótulo de % dentro (branco)/fora (preto) das barras** horizontais; escores clínicos podem entrar como numéricos (correlação) **e** categorizados (ANOVA); exportar **BASE_TRATADA.xlsx** via `writexl`. Ver `06`, `02`, `05`, `08`.
