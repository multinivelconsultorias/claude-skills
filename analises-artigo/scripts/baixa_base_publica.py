#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baixa uma base pública, verifica integridade e registra a proveniência.

Uso:
    python3 baixa_base_publica.py <url> <pasta destino> [--nome "ENEM 2023"] [--orgao INEP]

O que faz, e por que cada passo importa:

- baixa em streaming, para não estourar memória com arquivos de vários GB;
- calcula o SHA-256, que é o que permite provar meses depois que o arquivo
  analisado é o mesmo que está no ar (ou provar que o órgão republicou);
- descompacta .zip listando o conteúdo, sem sobrescrever nada em silêncio;
- escreve/atualiza um PROVENIENCIA.md na pasta destino.

Não faz download de coisa alguma que exija login ou aceite de termos. Se a
base pedir cadastro, baixe manualmente e rode com --registrar-apenas para
gerar o registro de proveniência do arquivo que já está no disco.
"""
import argparse, hashlib, os, sys, zipfile
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.parse import urlparse

BLOCO = 1 << 20  # 1 MiB


def humano(n):
    for u in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or u == "TB":
            return f"{n:.1f} {u}" if u != "B" else f"{n} B"
        n /= 1024


def baixa(url, destino):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (pesquisa academica)"})
    with urlopen(req) as resp:
        total = int(resp.headers.get("Content-Length") or 0)
        h = hashlib.sha256()
        lidos = 0
        with open(destino, "wb") as fh:
            while True:
                bloco = resp.read(BLOCO)
                if not bloco:
                    break
                fh.write(bloco); h.update(bloco); lidos += len(bloco)
                if total:
                    pct = 100 * lidos / total
                    print(f"\r  {humano(lidos)} / {humano(total)} ({pct:.1f}%)",
                          end="", flush=True)
                else:
                    print(f"\r  {humano(lidos)}", end="", flush=True)
        print()
    return h.hexdigest(), lidos


def hash_local(caminho):
    h = hashlib.sha256(); n = 0
    with open(caminho, "rb") as fh:
        while True:
            bloco = fh.read(BLOCO)
            if not bloco:
                break
            h.update(bloco); n += len(bloco)
    return h.hexdigest(), n


def descompacta(caminho, pasta):
    if not zipfile.is_zipfile(caminho):
        return []
    with zipfile.ZipFile(caminho) as z:
        nomes = z.namelist()
        print(f"  {len(nomes)} arquivos no zip:")
        for n in nomes[:20]:
            print("   -", n)
        if len(nomes) > 20:
            print(f"   ... e mais {len(nomes) - 20}")
        alvo = os.path.join(pasta, os.path.splitext(os.path.basename(caminho))[0])
        os.makedirs(alvo, exist_ok=True)
        z.extractall(alvo)
        print(f"  extraído em {alvo}")
        return nomes


def registra(pasta, bloco):
    caminho = os.path.join(pasta, "PROVENIENCIA.md")
    novo = not os.path.exists(caminho)
    with open(caminho, "a", encoding="utf8") as fh:
        if novo:
            fh.write("# Proveniência das bases\n\n"
                     "Registro de origem de cada base usada no projeto. "
                     "Preencha à mão o recorte aplicado e a contagem de linhas "
                     "depois de rodar o `00_prep`.\n\n")
        fh.write(bloco)
    print(f"\nProveniência registrada em {caminho}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url", help="URL do arquivo, ou caminho local com --registrar-apenas")
    ap.add_argument("destino", help="pasta onde salvar")
    ap.add_argument("--nome", default="", help='ex.: "ENEM 2023 — Microdados"')
    ap.add_argument("--orgao", default="", help="ex.: INEP")
    ap.add_argument("--registrar-apenas", action="store_true",
                    help="não baixa; só registra um arquivo que já está no disco")
    a = ap.parse_args()

    os.makedirs(a.destino, exist_ok=True)

    if a.registrar_apenas:
        arquivo = a.url
        if not os.path.exists(arquivo):
            sys.exit(f"Arquivo não encontrado: {arquivo}")
        print(f"Calculando hash de {arquivo}...")
        sha, tam = hash_local(arquivo)
        origem = "(baixado manualmente)"
    else:
        nome_arq = os.path.basename(urlparse(a.url).path) or "download.bin"
        arquivo = os.path.join(a.destino, nome_arq)
        if os.path.exists(arquivo):
            sys.exit(f"Já existe: {arquivo}\nApague ou use --registrar-apenas.")
        print(f"Baixando {a.url}")
        sha, tam = baixa(a.url, arquivo)
        origem = a.url

    conteudo = descompacta(arquivo, a.destino)

    agora = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d")
    bloco = (f"## {a.nome or os.path.basename(arquivo)}\n"
             f"- Órgão: {a.orgao or '<preencher>'}\n"
             f"- Origem: {origem}\n"
             f"- Arquivo: `{os.path.basename(arquivo)}`\n"
             f"- Baixado em: {agora}\n"
             f"- Tamanho: {humano(tam)}\n"
             f"- SHA-256: `{sha}`\n")
    if conteudo:
        bloco += f"- Conteúdo do zip: {len(conteudo)} arquivos\n"
    bloco += ("- Dicionário: <preencher>\n"
              "- Recorte aplicado no 00_prep: <preencher>\n"
              "- Linhas: <brutas> -> <após recorte>\n\n")

    registra(a.destino, bloco)
    print(f"SHA-256: {sha}")
    print("\nPróximo passo: leia o dicionário antes de calcular qualquer estatística, "
          "e confira os códigos de não-resposta com perfila_base.py.")


if __name__ == "__main__":
    main()
