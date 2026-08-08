# Pipeline de análises auditáveis em R

## Por que assim

Um artigo empírico é reescrito muitas vezes, e quase sempre por causa de uma decisão analítica que muda: o desfecho vira binário, o estimador troca, um preditor é recategorizado, um revisor pede uma sensibilidade. Quando os resultados vivem em planilhas e o texto é digitado à mão, cada mudança dessas exige varrer o documento inteiro procurando números — e o que sobra são erros silenciosos.

O pipeline resolve isso invertendo a dependência: **o texto é uma função dos objetos do modelo**. Trocar uma decisão passa a ser editar uma linha e rodar de novo.

## Estrutura de arquivos

```
<projeto>/
├── 00_prep.R            -> dados.rds
├── 01_descritivas.R     -> desc.rds
├── 02_<analise>.R       -> <analise>.rds   + saida_figuras/*.svg|png
├── ...
├── NN_relatorio.R       -> conteudo.json + conteudo_docx.json
├── build_report.py, json2html.py
├── saida_figuras/
├── CONTEXTO_<PROJETO>.md
└── <base bruta>
```

Numere na ordem de execução. Um script, um artefato `.rds`. O nome do `.rds` acompanha o do script. Cada script termina com `cat("OK_<NOME>\n")` para que a saída do terminal diga o que rodou.

## Invocação

Sempre com o diretório de trabalho na pasta do projeto e a localidade forçada, senão acentos corrompem na escrita de arquivos:

```bash
LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 Rscript 04_modelo.R
```

Ao gravar JSON ou CSV pelo R, use `writeLines(enc2utf8(x), arquivo, useBytes=TRUE)`.

## Cabeçalho de cada script

Comece cada arquivo com um comentário que explique **o que ele faz e por que as decisões são as que são**. Esse cabeçalho é onde o raciocínio metodológico fica registrado — não no chat, que se perde, nem no artigo, que é resumido demais. Quando uma decisão for revertida, mantenha o registro do que foi testado e por que caiu:

```r
# =====================================================================
# 04_modelo.R — Modelo explicativo (path analysis, lavaan).
#
# TRATAMENTO DO DESFECHO: dicotômico, estimado por MLR+FIML.
#
# NOTA: o desfecho já foi tomado como contínuo, e essa versão foi
# abandonada porque nela o caminho de X para Y sai negativo contra uma
# correlação simples positiva (rho = 0,21), efeito de supressão sem
# leitura substantiva. Sob dicotomização o caminho perde significância.
# O tratamento contínuo permanece como linha da tabela de sensibilidade.
# =====================================================================
```

## Parametrize o que pode mudar

O erro comum é escrever o modelo uma vez e copiá-lo para cada variante. Em vez disso, escreva um construtor:

```r
mk <- function(y = "Auto_b", facs = sint7, qv_para_auto = FALSE, com_indiretos = TRUE) {
  # ... monta a sintaxe do modelo a partir dos argumentos
}
roda_con <- function(m) sem(m, data = d, estimator = "MLR",   missing = "fiml")
roda_cat <- function(m, y) sem(m, data = d, estimator = "WLSMV", ordered = y, missing = "pairwise")

f_principal <- roda_con(mk("Auto_b"))
f_sensib_1  <- roda_cat(mk("Auto_bin"), "Auto_bin")
f_sensib_2  <- roda_con(mk("Auto"))
```

O teste é simples: **trocar a decisão deve ser uma linha.** Se for preciso reescrever um bloco, o construtor está mal fatorado.

## Guarde o que descartou

Modelos alternativos não são lixo, são a justificativa da escolha. Guarde-os numa lista nomeada e leve para uma tabela de sensibilidade no relatório:

```r
TRAT <- list(
  bin_ml = trat(f_principal, "Dicotômico, máxima verossimilhança robusta (modelo final)", "Auto_b", FALSE),
  bin_w  = trat(f_sensib_1,  "Dicotômico, mínimos quadrados ponderados", "Auto_bin", TRUE),
  con    = trat(f_sensib_2,  "Contínuo, máxima verossimilhança robusta", "Auto", FALSE))
```

Quando o autor perguntar "e se fosse de outro jeito?", a resposta já está no `.rds`.

## Diagnósticos que se pagam

Quando duas especificações deveriam produzir resultados iguais em alguma parte, verifique isso no script e salve o resultado. Exemplo real: ao retirar a camada terminal de um modelo recursivo estimado por máxima verossimilhança, os coeficientes anteriores devem permanecer idênticos, por separabilidade entre equações.

```r
cmp <- merge(STD_completo[STD_completo$op == "~" & STD_completo$lhs != y, c("lhs","rhs","est.std")],
             STD_reduzido[STD_reduzido$op == "~",             c("lhs","rhs","est.std")],
             by = c("lhs","rhs"))
dif <- max(abs(cmp$est.std.x - cmp$est.std.y))
cat("Maior diferença nos caminhos anteriores ao desfecho:", sprintf("%.4f\n", dif))
```

Esse número vira um achado do artigo e, ao mesmo tempo, um teste de regressão do pipeline.

## O arquivo de contexto

`CONTEXTO_<PROJETO>.md` é o handoff. Atualize-o **a cada decisão**, não no fim. Seções que se pagam:

0. Onde estão as coisas — pasta local, pasta de entrega, entregáveis, base
1. O artigo — título, N, exigências do projeto
2. Pipeline — ordem de execução e o comando de build
3. Estrutura atual do relatório — seções, tabelas e figuras numeradas
4. Hipóteses e o que as testa
5. Resultados-chave com os números reais
6. Decisões do autor a cumprir — numeradas, com a data e o motivo; quando revogadas, marque como revogada em vez de apagar
7. Gotchas — o que custou tempo e não deve ser repetido
8. Justificativas de especificação — as análises que embasaram uma escolha e saíram do relatório
9. Pendências

Modelo em `assets/CONTEXTO_TEMPLATE.md`.

## Sincronização

Trabalhe local. No fim, copie para a nuvem os entregáveis, os scripts, os `.rds` e a pasta de figuras. Se o autor mantém o `.docx` aberto no Word, avise para fechar e reabrir: o Word pode gravar por cima da versão nova com a que tem em memória.
