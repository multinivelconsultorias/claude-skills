#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrai o texto de todos os PDFs de uma pasta, para varredura rápida do corpus.

Uso:
    python3 extrai_corpus.py "<pasta com PDFs>" "<pasta de saída>"

Gera um .txt por PDF e imprime uma tabela com páginas e caracteres extraídos.
Um PDF com muitas páginas e pouquíssimo texto provavelmente é digitalizado sem
OCR: o script sinaliza esses casos, porque nenhuma busca por palavra-chave vai
encontrá-los.

Depois de rodar, mapeie o vocabulário antes de ler qualquer coisa:

    cd <pasta de saída>
    for f in *.txt; do echo "== $f"; \
      grep -oiE "termo1|termo2|termo3" "$f" | sort | uniq -c | sort -rn | head; done

Isso diz em minutos quais fontes têm o que interessa.
"""
import os, re, sys, glob

try:
    from pypdf import PdfReader
except ImportError:  # pypdf antigo
    from PyPDF2 import PdfReader


def extrai(pdf_path, out_dir):
    leitor = PdfReader(pdf_path)
    paginas = []
    for pagina in leitor.pages:
        try:
            paginas.append(pagina.extract_text() or "")
        except Exception:
            paginas.append("")
    texto = "\n\n".join(paginas)
    nome = re.sub(r"[^A-Za-z0-9]+", "_", os.path.basename(pdf_path))[:60] + ".txt"
    destino = os.path.join(out_dir, nome)
    with open(destino, "w", encoding="utf8") as fh:
        fh.write(texto)
    return destino, len(leitor.pages), len(texto)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    pdfs = sorted(glob.glob(os.path.join(src, "*.pdf")))
    if not pdfs:
        print(f"Nenhum PDF em {src}")
        sys.exit(1)
    print(f"{'págs':>5} {'chars':>8}  arquivo")
    suspeitos = []
    for pdf in pdfs:
        destino, n_pag, n_chr = extrai(pdf, out)
        print(f"{n_pag:>5} {n_chr:>8}  {os.path.basename(destino)}")
        if n_pag > 2 and n_chr / n_pag < 200:
            suspeitos.append(os.path.basename(pdf))
    print(f"\n{len(pdfs)} arquivos -> {out}")
    if suspeitos:
        print("\nPouco texto por página, provavelmente digitalizados sem OCR:")
        for s in suspeitos:
            print("  -", s)


if __name__ == "__main__":
    main()
