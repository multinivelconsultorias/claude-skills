# Handoff — Skill Multinível + teste TCC Ricardo
> Contexto para retomar em nova sessão. Atualizado em 2026-06-01.

## 1. Quem é o usuário
**Julio Cezar Albuquerque (da Costa)** — consultor em análise de dados/psicometria, marcas **Multinível** (psicometria) e **NAOPARE** (saúde/epidemiologia). Trabalha em **R**, escreve em **pt-BR**, formata em **APA 7**. Entrega "Relatórios de Análise de dados".

## 2. O que foi construído (a skill)
Skill global **`/relatorio-multinivel`**, destilada de **328 relatórios** (2020–2026). Fluxo: **monta workspace local** → lê base → define/aplica delineamento → escreve código R → roda análises → escreve o relatório no estilo dele → **leva só o resultado ao Drive**.

**Locais:**
- Skill canônica (disco local rápido): `~/.claude/skills/relatorio-multinivel/`
- Cópia editável no Drive: `.../2. Multinível/12 - Treinamento relatórios até 30.06.26/_Skill Multinível/` (mantida em par com a canônica)
- Memória do projeto (local): `~/.claude/projects/-Users-...-30-06-26/memory/` → `MEMORY.md`, `user-julio-multinivel.md`, `project-skill-relatorio-multinivel.md`, `feedback-estilo-relatorios.md`

**Estrutura da skill:**
- `SKILL.md`, `README.md`, `HANDOFF.md`
- `references/01-estilo-de-escrita.md` — voz passiva sintética; vícios com frequência; fórmulas; **§3.1 interpretação acessível**; **§7.1 símbolos/hífen no corpo do texto**; checklist.
- `references/02-referencias-por-teste.md` + `.json` — teste → citação fixa.
- `references/03-referencias-apa7.md`; `04-pacotes-r.md`; `05-graficos.md`; `06-formatacao-apa7.md` (TNR 12 / tabelas 10pt / entrelinha 1,5 / 12pt após parágrafo / tabela Estilo2 = só bordas horizontais / margens 2,5cm).
- `references/07-templates-trechos.md` — blocos "Análise de dados" + fórmulas de Resultados (fluidas: comparação, regressão com tradução de OR, mediação narrada).
- `references/08-convencoes-tabelas-figuras.md` — convenções obrigatórias de tabelas/figuras (ver §5).
- `assets/setup_workspace.py` — monta o workspace local e copia base+scripts.
- `assets/sync_to_drive.py` — leva o resultado final ao Drive (1 cópia, no fim; `--tudo` p/ pasta inteira).
- `assets/build_report.py` — gera o `.docx` formatado a partir de JSON. `assets/analise_template.R`, `assets/explore_data.py`.

## 3. Citações fixas por teste (núcleo)
Shapiro→Miot(2017); resíduos padronizados→Sharpe(2015); qui²/Fisher→Kim(2017); Mann-Whitney→Brunner,Bathke&Konietschke(2018); Kruskal/Dunn→Pohlert(2014); V de Cramér e tamanho de efeito→Serdar et al.(2021); correlação→Miot(2018); KMO/Bartlett/AFE→Damásio(2012); ajuste AFC→Hair et al.(2009)+Kline(2016); invariância→Cheung&Rensvold(2002); TRI→Samejima(1969)/Chalmers(2012)/Pasquali(2020); regressão logística→Fernandes et al.(2020); mediação→Hayes(2013); lavaan→Rosseel(2012). Software: R Core Team (ano corrente).

## 4. Decisões já tomadas pelo Julio
- Saída: **DOCX + HTML/.R fonte** (ambos).
- Espaçamento: **12pt após parágrafo**, entrelinha 1,5, sem recuo. Referências **APA 7**.
- **Local-first**: trabalhar em `~/Downloads/Relatórios Automatizados/<Projeto>/`; uma pasta por projeto/banco; só o resultado vai ao Drive.
- **Mediação/moderação sempre em duas versões** (bruta e ajustada por idade/sexo + covariáveis do estudo).
- Tamanho de efeito: critério de **Serdar et al. (2021)**. Skill global + cópia editável no Drive.

## 5. Convenções de redação e tabelas (todas na skill — `08-convencoes` e `01-estilo`)
1. **Qui²/Fisher → cross-tab** com a variável fixa do estudo nas **colunas** (n e % por coluna); pós-hoc por resíduos |SR|≥1,96 em negrito.
2. **Identificação do teste por símbolo + nota** (nunca coluna "Teste"); vale também p/ comparações (Mann-Whitney etc.). **Tamanho de efeito em coluna própria**, com o paralelo teste↔efeito declarado na metodologia.
3. **Heatmap de correlações**: colorbar −1 a +1, coeficiente em cada célula, texto adaptativo.
4. **Regressão**: **categoria de referência como 1ª info da nota** (default = grupo de maior frequência; ou o grupo de interesse); **B e OR** (logística) ou **B e Beta** (linear), com IC95%; **+ estatísticas do modelo** (F/χ², p, R²/pseudo-R², AIC, BIC).
5. **Mediação/moderação**: **duas versões (bruta + ajustada)**, lado a lado, com **FDR por versão**; tabela de mediação com **a, b, (a*b), c, c′**; **figura** com coeficientes nas setas.
6. **Interpretação acessível** (calcanhar de Aquiles): traduzir **OR em chances**, **narrar a cadeia** da mediação, nomear grupos e direção nas comparações.
7. **Sem "→" e sem hífen/travessão no corpo** (exceto termos como qui-quadrado e referências); intervalos com "a".
8. **Encadear achados com conectivos** (aditivos / adversativos quando a direção inverte), nunca ";" em série.

## 6. Projeto-teste: TCC Ricardo (afundamento do solo em Maceió)
- **Pasta local (trabalho):** `~/Downloads/Relatórios Automatizados/Relatório TCC Ricardo/`
- **Pasta Drive (resultado):** `.../1. Acadêmico/98 - Correções de artigos/37 - TCC Ricardo/Project_Ricardo/`
- **Base:** `Banco_tratado.xlsx` (213×150). Desfecho: **Sair_de_casa** (0=não,1=sim). Instrumentos: DASS-21 (Depressao/Ansiedade/Estresse), QVAS (Saude_FM_Vida_ANTES/DEPOIS/delta, Acompanhamento_PSICQ, Autolesoes_ANTES/DEPOIS/delta), SRQ, WHOQOL-BREF (Fisico/Psicologico/Relacoes_sociais/Meio_ambiente). Sociodemográficas + Renda antes/depois.

**Pipeline (rodar nesta ordem, com cwd = pasta local):**
1. `medmod_grid.R` — grid de mediações + moderações simples (X = sair de casa) entre **16 fatores** (DASS-21, WHOQOL, QVAS delta/depois e **SRQ: 4 fatores + escore geral**), **em duas versões (bruta e ajustada por idade+gênero)**, bootstrap via `.lm.fit`, **FDR (Benjamini-Hochberg)**; salva `medmod_grid.rds` + 4 CSVs.
2. `sem_path.R` — path analysis (lavaan, MLR): mediação SEM (mediador comum = percepção de saúde) + moderação SEM (multigroup e interação, DASS→WHOQOL). Salva `sem_path.rds`.
3. `sem_seq.R` — **modelo sequencial de 3 estágios** (Sair → Δ percepção de saúde → sintomas → Δ autolesões/ideação), DASS-21 OU SRQ; gera o diagrama `fig_sem_5c.png`. Salva `sem_seq.rds`.
4. `aplica_convencoes.R` — recalcula Estudos 1–4, lê os 3 `.rds`, monta `conteudo_docx.json` + figuras (correlações, diagrama de mediação focal).
5. `build_report.py conteudo_docx.json relatorio.docx` e `json2html.py conteudo_docx.json relatorio.html`.

**Entregáveis:** `relatorio.docx` (**3 figuras, 16 tabelas**), `relatorio.html`. (Artefatos antigos a limpar na pasta do Drive: `analise_estatistica.R`, `gera_docx.R`, `gera_relatorio.R`, `code.r`, `resultados_medmod.rds`, `tab_*.csv`, e cópias soltas tipo `relatorio__.docx`.)

**Resultados (N=207 válidos):**
- Estudo 1 (qui²/Fisher): nenhuma associação sociodemográfica sig; tendências Ocupação (p=0,056) e Renda pós (p=0,053).
- Estudo 2 (Mann-Whitney): saúde-vida Δ **p<0,001** (rrb=0,23); Depressão p=0,017; saúde-vida DEPOIS p=0,024; Estresse p=0,047 — piores em quem saiu.
- Estudo 3: correlações de Spearman (heatmap anotado).
- Estudo 4 (regressão logística; multi n=196; AUC 0,70; McFadden 0,10): multivariável → Renda pós >5 SM **OR 8,56** (p=0,017); univariadas: ΔSaúde OR 0,64 etc.
- Estudo 5 (grid, FDR): **mediação bruta → 9 sig após FDR, todas via variação da percepção de saúde** (Depressão, Ansiedade, Estresse, Autolesões depois, Físico, Meio ambiente + 3 fatores do SRQ); **ajustada → 0**; **moderação → 0** (7 brutas como exploratórias, Tabela 7). Anexo: Tabelas A1–A4.
- Estudo 5b (path analysis): mediação SEM confirma os indiretos via percepção de saúde; **moderação SEM (multigroup + interação) sem moderação significativa**.
- Estudo 5c (path analysis, MLR — modelo PRINCIPAL): **cadeia sequencial de 3 estágios** Sair → Δ percepção de saúde (β=−0,22) → sintomas (β −0,29 a −0,31) → Δ autolesões/ideação (via Ansiedade β=0,35; Humor SRQ β=0,23). Ajuste: χ²/gl 1,2–1,3; CFI 0,996; RMSEA ~0,03 (mais gl e mais defensável que os de 2 estágios, quase saturados). Tabela 10 (ajuste), 11/12 (todos os parâmetros), Figura 3 (diagrama SEM).

## 7. Ambiente (IMPORTANTE)
- **R 4.5.1** com pacotes (readxl, tidyverse, lavaan, rcompanion, rstatix, car, broom…). **python-docx 1.2.0**. **pandoc ausente** (usar python-docx).
- **Rscript:** exportar `LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8` (senão corrompe acentos); JSON do R via `writeLines(enc2utf8(x), file, useBytes=TRUE)`; rodar com `setwd("<PROJETO_DIR>")` para os caminhos relativos funcionarem.
- **build_report.py / json2html.py resolvem figuras relativo ao cwd** → rodar com cwd = pasta do projeto (forma prompt-free: `python3 -c "import os,runpy,sys; os.chdir('<DIR>'); sys.argv=[...]; runpy.run_path('build_report.py',run_name='__main__')"`). Se rodar do lugar errado, as figuras somem do `.docx` sem erro.
- **Google Drive (CloudStorage) é lento/instável**: `find`/`grep` recursivos na "My Drive" travam; ler/escrever dispara download/upload sob demanda. **Local-first resolve** (§4): trabalhar em `~/Downloads/Relatórios Automatizados/` e sincronizar só no fim com `sync_to_drive.py`.
- Bootstrap de mediação via **`.lm.fit`** (rápido): o grid (≈210 modelos × 2 versões) roda em poucos minutos.
- **SEM (path analysis): usar MLR** (robusto à assimetria) para os escores contínuos. **Não usar WLSMV** aqui — as variáveis são escores/médias contínuos (não ordinais); o DWLS gera solução imprópria (variâncias negativas, vcov não positiva definida). Modelos quase saturados (poucos gl) têm índices de ajuste pouco diagnósticos → preferir modelos com mais gl (ex.: a cadeia de 3 estágios do Estudo 5c).
- **`sync_to_drive.py` agora ignora locks/temporários** (`~$*`, `.~*`, `.DS_Store`, `.tmp`); ainda assim, **fechar o Word antes de sincronizar** evita levar o arquivo de bloqueio. Atenção a cópias soltas (`relatorio__.docx`) no workspace.
- **Lições de processo:** NÃO empilhar muitas tool calls em paralelo no Drive; uma chamada por vez quando o canal está instável.

## 8. Pendências / próximos passos
- [x] **Local-first** — FEITO (`setup_workspace.py` + `sync_to_drive.py`).
- [ ] **Limpar artefatos antigos** na pasta do Ricardo (`analise_estatistica.R`, `gera_docx.R`, `gera_relatorio.R`, `code.r`, `resultados_medmod.rds`, `tab_*.csv` de execuções anteriores).
- [ ] (opcional) Uniformizar rótulos longos de renda nas tabelas/figuras.

## 9. Como retomar
Acionar **`/relatorio-multinivel`** (ou pedir "relatório de análise de dados"). Para um projeto novo: `setup_workspace.py "<Projeto>" "<base>"` → rodar análises na pasta local → `sync_to_drive.py` no fim. Para continuar o **TCC Ricardo**: a pasta local `~/Downloads/Relatórios Automatizados/Relatório TCC Ricardo/` já está montada; rodar o pipeline completo, nesta ordem — `medmod_grid.R` → `sem_path.R` → `sem_seq.R` → `aplica_convencoes.R` → `build_report.py conteudo_docx.json relatorio.docx` → `json2html.py conteudo_docx.json relatorio.html` — e sincronizar com `sync_to_drive.py`. Todos os Rscript com `LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8` e `setwd()` na pasta; os python com `os.chdir` na pasta. O relatório já está pronto e sincronizado no Drive — reproduzir só é necessário se houver novas mudanças.
