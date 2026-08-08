#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
explore_data.py — Perfila uma base de dados para ajudar a sugerir o delineamento.

Uso:
    python3 explore_data.py caminho/dados.xlsx [--sheet 0] [--sep ;]

Suporta .xlsx/.xls (precisa de openpyxl/pandas) e .csv/.tsv.
Para .sav (SPSS), use o R (haven) — aqui mostramos só uma dica.

Saída: para cada coluna — tipo inferido (numérica/categórica/binária), n válido,
% faltante, nº de níveis (se categórica) e amostra de valores. Ao final, sugere
testes prováveis no estilo Multinível.
"""
import sys, os, json

def load(path, sheet=0, sep=None):
    ext = os.path.splitext(path)[1].lower()
    try:
        import pandas as pd
    except ImportError:
        print("ERRO: pandas não instalado. Tente: pip install pandas openpyxl")
        sys.exit(1)
    if ext in (".xlsx", ".xls"):
        return pd.read_excel(path, sheet_name=sheet)
    if ext in (".csv", ".tsv", ".txt"):
        if sep is None:
            sep = "\t" if ext == ".tsv" else None  # let pandas sniff for csv
        return pd.read_csv(path, sep=sep, engine="python")
    if ext == ".sav":
        print("Base .sav (SPSS): carregue no R com haven::read_sav(). "
              "Este script não lê .sav.")
        sys.exit(1)
    print(f"Extensão não suportada: {ext}")
    sys.exit(1)


def profile(df):
    import pandas as pd
    n = len(df)
    rows = []
    for col in df.columns:
        s = df[col]
        nvalid = int(s.notna().sum())
        miss = round(100 * (n - nvalid) / n, 1) if n else 0
        nun = int(s.nunique(dropna=True))
        is_num = pd.api.types.is_numeric_dtype(s)
        if is_num and nun > 10:
            kind = "numérica"
        elif nun == 2:
            kind = "binária"
        elif is_num and nun <= 10:
            kind = "numérica-discreta/ordinal"
        else:
            kind = "categórica"
        sample = list(pd.Series(s.dropna().unique()[:6]).astype(str))
        rows.append({"coluna": str(col), "tipo": kind, "n_valido": nvalid,
                     "faltante_%": miss, "niveis": nun, "exemplos": sample})
    return n, rows


def suggest(rows):
    nums = [r for r in rows if r["tipo"].startswith("numérica")]
    cats = [r for r in rows if r["tipo"] in ("categórica", "binária")]
    bins = [r for r in rows if r["tipo"] == "binária"]
    s = []
    s.append("Descritivas: frequência/% (categóricas); M, Mdn, DP, quartis, min, max (numéricas).")
    if nums:
        s.append("Normalidade das numéricas: Shapiro-Wilk (Miot, 2017) -> se assimétrica, usar não-paramétrico.")
    if nums and bins:
        s.append("Numérica x binária: Mann-Whitney (Brunner et al., 2018) + rank-biserial (Serdar et al., 2021).")
    if nums and any(c for c in cats if c["niveis"] >= 3):
        s.append("Numérica x (3+ grupos): Kruskal-Wallis + Dunn/Holm (Pohlert, 2014) + eta² (Serdar et al., 2021).")
    if len(cats) >= 2:
        s.append("Categórica x categórica: qui-quadrado/Fisher (Kim, 2017) + resíduos >=1,96 (Sharpe, 2015) + V de Cramér (Serdar et al., 2021).")
    if len(nums) >= 2:
        s.append("Entre numéricas: correlação Pearson/Spearman conforme normalidade (Miot, 2018).")
    likert = [r for r in rows if r["tipo"] in ("numérica-discreta/ordinal",) and r["niveis"] <= 7]
    if len(likert) >= 6:
        s.append("Muitos itens ordinais (Likert): possível validação de escala — AFE (Damásio, 2012) -> AFC/MEE (lavaan, WLSMV) -> consistência interna -> TRI (mirt).")
    return s


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    path = sys.argv[1]
    sheet = 0; sep = None
    if "--sheet" in sys.argv:
        sheet = sys.argv[sys.argv.index("--sheet") + 1]
        try: sheet = int(sheet)
        except ValueError: pass
    if "--sep" in sys.argv:
        sep = sys.argv[sys.argv.index("--sep") + 1]
    df = load(path, sheet=sheet, sep=sep)
    n, rows = profile(df)
    print(f"=== {os.path.basename(path)} — {n} linhas, {len(rows)} colunas ===\n")
    print(f"{'coluna':<28} {'tipo':<26} {'n':>6} {'falt%':>6} {'níveis':>7}  exemplos")
    print("-" * 100)
    for r in rows:
        ex = ", ".join(r["exemplos"])[:38]
        print(f"{r['coluna'][:27]:<28} {r['tipo']:<26} {r['n_valido']:>6} "
              f"{r['faltante_%']:>6} {r['niveis']:>7}  {ex}")
    print("\n=== Sugestão de delineamento (estilo Multinível) ===")
    for line in suggest(rows):
        print("  •", line)
    print("\n(Confirme os papéis das variáveis antes de rodar analise_template.R.)")


if __name__ == "__main__":
    main()
