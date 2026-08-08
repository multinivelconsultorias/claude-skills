# Pipeline em Python

Mesma arquitetura do pipeline em R: scripts numerados, um artefato cada, nenhum número escrito à mão, travas nas afirmações qualitativas. O que muda é a sintaxe e algumas conveniências que o Python oferece para bases grandes.

## Estrutura

```
<projeto>/
├── 00_prep.py            -> dados.parquet
├── 01_descritivas.py     -> desc.pkl
├── 02_<analise>.py       -> <analise>.pkl  + saida_figuras/*.png|svg
├── NN_relatorio.py       -> conteudo.json + conteudo_docx.json
├── build_report.py, json2html.py
├── PROVENIENCIA.md
└── CONTEXTO_<PROJETO>.md
```

## Formato dos artefatos

**Parquet para dados tabulares.** Preserva tipos, comprime bem e lê rápido — o que importa quando o `00_prep` roda uma vez e os outros scripts leem dezenas de vezes.

```python
df.to_parquet("dados.parquet", index=False)
df = pd.read_parquet("dados.parquet")
```

**Pickle apenas para resultados de modelo**, que não têm representação tabular. Registre a versão das bibliotecas junto, porque pickle quebra entre versões:

```python
import pickle, sys, statsmodels
res = {"modelo": fit, "versoes": {"python": sys.version.split()[0],
                                  "statsmodels": statsmodels.__version__}}
pickle.dump(res, open("modelo.pkl", "wb"))
```

**Nunca CSV como artefato intermediário.** Perde tipos, e um float que vira string no meio do pipeline é um bug que aparece três scripts depois.

## Bases grandes

Microdados públicos costumam ter milhões de linhas e centenas de colunas, e ler tudo estoura a memória sem necessidade — quase sempre você precisa de vinte colunas.

```python
# leia só o que vai usar
cols = ["TP_SEXO", "NU_NOTA_MT", "NU_NOTA_LC", "TP_ESCOLA", "SG_UF_PROVA"]
df = pd.read_csv(arquivo, sep=";", encoding="latin-1", usecols=cols)

# ou em blocos, quando nem a seleção cabe
partes = []
for bloco in pd.read_csv(arquivo, sep=";", encoding="latin-1",
                         usecols=cols, chunksize=500_000):
    partes.append(bloco.query("SG_UF_PROVA == 'AL'"))
df = pd.concat(partes, ignore_index=True)
```

Depois de filtrar, salve em Parquet e nunca mais toque no arquivo original. O `00_prep` é o único script que lê a base bruta.

## Reprodutibilidade

Fixe a semente em tudo que sorteia e registre as versões no artefato:

```python
import numpy as np, random
SEED = 2026
random.seed(SEED); np.random.seed(SEED)
```

Congele o ambiente uma vez e versione o arquivo junto com os scripts:

```bash
python3 -m pip freeze > requirements.txt
```

## As travas

Em Python a trava é o `assert`, e a mensagem importa: quando quebrar meses depois, você quer saber o que a prosa afirmava.

```python
n_sig = int((coef["p"] < 0.05).sum())
maior = coef.loc[coef["beta"].abs().idxmax(), "termo"]

# a prosa afirma três preditores significativos, o maior sendo idade,
# e nenhum preditor do bloco socioeconômico significativo
assert n_sig == 3, f"a prosa afirma 3 significativos; encontrei {n_sig}"
assert maior == "idade", f"a prosa afirma que o maior é idade; é {maior}"
assert (coef.loc[coef.termo.isin(bloco_se), "p"] >= 0.05).all(), \
    "a prosa afirma que nenhum preditor socioeconômico foi significativo"

p(f"Entre os preditores examinados, três alcançaram significância, "
  f"com o maior coeficiente em {L(maior)} (β = {f3(b_maior)}, {pe(p_maior)}).")
```

Rode os scripts com `python3 -O` desligado — a flag `-O` remove os `assert`, e aí a trava não existe. Se precisar de garantia mesmo sob otimização, use `if not cond: raise AssertionError(...)`.

## Formatação numérica em português

O mesmo problema do R: ponto decimal e sinal negativo no corpo do texto. Defina uma vez:

```python
def f(x, d=2):
    if x is None or pd.isna(x):
        return "—"
    return f"{x:.{d}f}".replace(".", ",")

def f1(x): return f(x, 1)
def f3(x): return f(x, 3)
def fa(x, d=3): return f(abs(x), d)          # módulo, evita o sinal no corpo

def fp(p):
    if p is None or pd.isna(p): return "—"
    return "< 0,001" if p < 0.001 else f"{p:.3f}".replace(".", ",")

def pe(p):
    if p is None or pd.isna(p): return "p = —"
    return "p < 0,001" if p < 0.001 else f"p = {fp(p)}"
```

## Geração do JSON de conteúdo

O último script monta a mesma estrutura de blocos descrita em `03-relatorio.md`, e os mesmos conversores servem:

```python
import json
blocos = []
def p(txt):   blocos.append({"type": "p", "text": txt})
def h1(txt):  blocos.append({"type": "h1", "text": txt})
def tbl(cap, header, rows, note=None):
    b = {"type": "table", "caption": cap, "header": header, "rows": rows}
    if note: b["note"] = note
    blocos.append(b)

nt = 0
def TAB():
    global nt; nt += 1; return f"Tabela {nt}"

doc = {"org": "multinivel", "title": "Relatório de Análise de dados",
       "author": "<AUTOR>",
       "options": {"first_line_indent_cm": 1.25, "space_after_pt": 0},
       "blocks": blocos}
json.dump(doc, open("conteudo.json", "w", encoding="utf8"), ensure_ascii=False)
json.dump(json.loads(json.dumps(doc).replace('.svg"', '.png"')),
          open("conteudo_docx.json", "w", encoding="utf8"), ensure_ascii=False)
print(f"OK_RELATORIO — {len(blocos)} blocos | {nt} tabelas")
```

## Pacotes por tipo de análise

| Análise | Pacote |
|---|---|
| descritivas, normalidade, testes, tamanho de efeito | `pingouin` |
| regressão linear e logística, modelos mistos, robustez | `statsmodels` |
| equações estruturais, análise fatorial | `semopy`, `factor_analyzer` — mas prefira o `lavaan` em R quando o modelo for central ao artigo, porque o reporte esperado pelos periódicos é o dele |
| tabelas de contingência, qui-quadrado, resíduos | `scipy.stats` + cálculo manual dos resíduos padronizados |
| gráficos | `matplotlib` com tema explícito; `seaborn` para distribuições |
| leitura de bases grandes | `pyarrow`, `pandas` com `usecols` e `chunksize` |

`pingouin` é preferível ao `scipy` puro para testes de hipótese porque devolve tamanho de efeito e intervalo de confiança na mesma saída, que é o que o relatório precisa reportar.

## Figuras

Salve nos dois formatos, com o mesmo nome base, porque o Word não incorpora SVG e o HTML fica melhor com ele:

```python
for ext in ("svg", "png"):
    fig.savefig(f"saida_figuras/fig_modelo.{ext}", dpi=200, bbox_inches="tight")
```

Fixe tamanho e fonte no início do script em vez de deixar o padrão, senão as figuras saem com escalas diferentes entre si:

```python
import matplotlib as mpl
mpl.rcParams.update({"figure.figsize": (8, 5), "font.size": 11,
                     "font.family": "serif", "savefig.bbox": "tight"})
```
