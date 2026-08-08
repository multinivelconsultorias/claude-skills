# Gotchas acumulados

Cada item aqui custou tempo real. Consulte antes de depurar do zero.

## lavaan e modelos de caminhos

**Covariâncias residuais deixam de ser liberadas quando os fatores viram preditores.** Se há um desfecho depois de um bloco de variáveis, o `lavaan` para de liberar automaticamente as covariâncias residuais entre elas. É preciso declará-las de forma explícita, senão o ajuste desaba sem motivo aparente. Um helper resolve:

```r
cr <- function(g) { if (length(g) < 2) return(character(0))
  o <- c(); for (i in 1:(length(g)-1)) for (j in (i+1):length(g))
    o <- c(o, sprintf("%s ~~ %s", g[i], g[j])); o }
```

**O inverso também vale.** Ao *retirar* um caminho para o desfecho, o `lavaan` **libera** a covariância residual correspondente, e a poda não acontece de fato — o número de parâmetros não muda. Para podar de verdade, fixe: `Desfecho ~~ 0*fator`.

**O `lavaan` não libera covariância entre variáveis ligadas por caminho dirigido**, ainda que indireto.

**Mínimos quadrados ponderados não preservam a separabilidade entre equações.** Num modelo recursivo, o desajuste das equações posteriores se propaga para as anteriores sob WLSMV e DWLS. Sintoma: um caminho do bloco dos antecedentes, significativo na regressão isolada e no teste bivariado, cai para praticamente zero no modelo completo. Como é propriedade do estimador e não do tratamento do desfecho, verifique rodando o mesmo desfecho contínuo sob DWLS. Sob máxima verossimilhança a separabilidade se preserva — os coeficientes anteriores ficam idênticos até a quarta casa.

**Modelos com conjuntos diferentes de variáveis não são aninhados.** Nem qui-quadrado de diferença nem critérios de informação os comparam. Se você retirar uma camada do modelo, a comparação com o modelo completo é descritiva, e o texto precisa dizer isso. Espere também que retirar um bloco bem ajustado **piore** os índices globais, o que é contraintuitivo mas aritmético.

## Supressão

Um coeficiente com sinal invertido em relação à correlação simples é supressão, não achado. Costuma aparecer quando preditores da mesma família têm covariância residual alta. Reporte na tabela de sensibilidade com a ressalva de não interpretar; não construa argumento sobre ele; e prefira a especificação em que ele não aparece, mesmo que o ajuste seja equivalente. Ajuste igual não compensa carregar um caminho que não se pode ler.

## Figuras

**O device `svg()` do R depende do cairo**, indisponível em várias instalações de macOS (falha com `libSM.6.dylib`). Use `svglite::svglite()`.

**Salve cada figura em SVG e PNG com o mesmo nome base**, porque o Word não incorpora vetor e o HTML fica melhor com ele.

**Diagramas de caminho desenhados à mão em R** (com `rect`, `arrows` e `text`) dão controle total sobre quais caminhos aparecem, mas os rótulos colidem quando há muitas setas cruzando. Parametrize a posição do rótulo ao longo da seta e o deslocamento perpendicular, e alterne o sinal do deslocamento por índice para separar rótulos vizinhos.

## R

`sprintf` trata `%` como marcador: para um `%` literal escreva `%%`. Quebra silenciosamente notas de tabela que mencionam "IC 95%".

`rstatix::kruskal_effsize` devolve **η²H**, não ε². Rotule certo.

Escrita de arquivos com acento exige `LC_ALL=en_US.UTF-8` na invocação e `writeLines(enc2utf8(x), arquivo, useBytes = TRUE)` no código.

Em `Rscript -e`, cuidado com escapes de regex: `'\\.'` dentro de aspas simples no shell vira erro de "unrecognized escape". Prefira `[.]` ou escreva o script em arquivo.

## Build de documentos

**Rode os conversores com o cwd na pasta do projeto.** Fora dela, as figuras somem do `.docx` sem erro nenhum.

**Ao verificar texto dentro do `.docx`, normalize para NFC antes de procurar.** O macOS produz Unicode decomposto, e `"dicotômico" in xml` dá falso negativo mesmo com o texto correto no arquivo.

**Se o autor estiver com o `.docx` aberto no Word**, avise para fechar e reabrir depois de regerar. O Word pode gravar por cima da versão nova com a que tem em memória. O sintoma é um arquivo `~$nome.docx` na pasta.

## Dados

**Verifique se a variável que você quer decompor existe decomposta.** Um escore que chega ao pipeline já agregado (uma proporção de três indicadores, por exemplo) não pode ser reconstruído sem os itens originais. Antes de propor uma análise que precise das partes, confirme que elas existem na base bruta — e se não existirem, diga isso em vez de propor a análise.

**Regras de derivação por texto livre falham silenciosamente.** Uma variável derivada por expressão regular sobre respostas abertas erra grafias e casos-limite. Faça uma versão corrigida, compare as duas, e documente quantos casos mudam e o que acontece com os resultados. Mantenha a decisão sobre qual usar registrada no `CONTEXTO`.
