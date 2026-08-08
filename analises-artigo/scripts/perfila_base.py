#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Perfil rápido de uma base, com foco no que costuma dar errado em microdado público.

Uso:
    python3 perfila_base.py <arquivo> [--sep ";"] [--encoding latin-1] [--n 200000]

Aceita .csv, .tsv, .parquet, .xlsx, .sav, .dta.

Além do perfil usual (tipos, ausentes, cardinalidade), sinaliza três coisas que
não geram erro nenhum e estragam a análise em silêncio:

- códigos de não-resposta (9, 99, 999, -1, 88) tratados como valores válidos;
- encoding errado, detectado por caracteres de mojibake em colunas de texto;
- colunas numéricas lidas como texto, que quebram qualquer estatística.
"""
import argparse, os, re, sys

import pandas as pd

SUSPEITOS = [-9, -8, -4, -3, -2, -1, 7, 8, 9, 77, 88, 97, 98, 99,
             777, 888, 997, 998, 999, 9999, 99999]
MOJIBAKE = re.compile(r"Ã[\x80-\xbf]|Â[\x80-\xbf]|�")


def carrega(caminho, sep, encoding, n):
    ext = os.path.splitext(caminho)[1].lower()
    if ext == ".parquet":
        return pd.read_parquet(caminho)
    if ext in (".xlsx", ".xls"):
        return pd.read_excel(caminho, nrows=n)
    if ext == ".sav":
        return pd.read_spss(caminho)
    if ext == ".dta":
        return pd.read_stata(caminho)
    return pd.read_csv(caminho, sep=sep, encoding=encoding, nrows=n,
                       low_memory=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("arquivo")
    ap.add_argument("--sep", default=";")
    ap.add_argument("--encoding", default="latin-1")
    ap.add_argument("--n", type=int, default=200_000,
                    help="linhas lidas para o perfil (0 = todas)")
    a = ap.parse_args()

    if not os.path.exists(a.arquivo):
        sys.exit(f"Arquivo não encontrado: {a.arquivo}")

    df = carrega(a.arquivo, a.sep, a.encoding, a.n or None)
    print(f"\n{'='*72}\n{os.path.basename(a.arquivo)}: {len(df):,} linhas x {len(df.columns)} colunas")
    if a.n and len(df) == a.n:
        print(f"(amostra das primeiras {a.n:,} linhas; use --n 0 para ler tudo)")
    print("="*72)

    print(f"\n{'coluna':<28} {'tipo':<10} {'ausentes':>9} {'únicos':>8}  exemplo")
    print("-"*72)
    for c in df.columns:
        s = df[c]
        na = f"{100*s.isna().mean():.1f}%"
        ex = s.dropna().iloc[0] if s.notna().any() else "—"
        ex = str(ex)[:22]
        print(f"{str(c)[:28]:<28} {str(s.dtype):<10} {na:>9} {s.nunique():>8}  {ex}")

    # --- códigos de não-resposta -------------------------------------
    achados = []
    for c in df.select_dtypes("number").columns:
        s = df[c].dropna()
        if s.empty or s.nunique() < 3:
            continue
        mediana = s.median()
        for v in SUSPEITOS:
            if v in s.values:
                freq = (s == v).mean()
                # suspeito = valor extremo, frequente e longe do centro
                if freq > 0.005 and abs(v - mediana) > 3 * (s.std() or 1):
                    achados.append((c, v, freq))
    if achados:
        print(f"\n{'='*72}\nCANDIDATOS A CÓDIGO DE NÃO-RESPOSTA")
        print("Valores extremos e frequentes. CONFIRME NO DICIONÁRIO antes de\n"
              "calcular qualquer média — eles entram na conta como observação real.")
        print("-"*72)
        for c, v, f in sorted(achados, key=lambda x: -x[2]):
            print(f"  {str(c)[:30]:<30} valor {v:>7}  em {100*f:.1f}% dos casos")

    # --- encoding ----------------------------------------------------
    ruins = []
    for c in df.select_dtypes("object").columns:
        amostra = df[c].dropna().astype(str).head(2000)
        if amostra.str.contains(MOJIBAKE, regex=True).any():
            ruins.append(c)
    if ruins:
        print(f"\n{'='*72}\nENCODING PROVAVELMENTE ERRADO")
        print(f"Mojibake em: {', '.join(map(str, ruins[:10]))}")
        print(f"Tente --encoding utf-8 (você usou {a.encoding}).")

    # --- numéricas lidas como texto ----------------------------------
    textuais = []
    for c in df.select_dtypes("object").columns:
        s = df[c].dropna().astype(str).head(2000)
        if s.empty:
            continue
        conv = pd.to_numeric(s.str.replace(",", ".", regex=False), errors="coerce")
        if conv.notna().mean() > 0.95:
            textuais.append(c)
    if textuais:
        print(f"\n{'='*72}\nNUMÉRICAS LIDAS COMO TEXTO")
        print(f"{', '.join(map(str, textuais[:10]))}")
        print("Provável decimal com vírgula. Converta no 00_prep.")

    print(f"\n{'='*72}\nPróximo passo: confirme cada achado acima no dicionário da base\n"
          f"e trate no 00_prep, registrando quantos casos foram afetados.\n")


if __name__ == "__main__":
    main()
