#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_to_drive.py — Leva o RESULTADO FINAL do workspace local para o Google Drive.

Use SÓ no final, quando todas as análises e o relatório estiverem prontos.
Trabalha-se 100% local (ver setup_workspace.py); este script faz a única cópia
para o Drive — o ponto mais lento/instável, por isso fica por último e uma vez só.

Por padrão copia os ENTREGÁVEIS e as saídas produzidas (relatório .docx/.html,
scripts .R fonte, .json de conteúdo, figuras e tabelas), sem reenviar a base bruta
(que já está no Drive). Com --tudo copia a pasta inteira do projeto.

Uso:
    python3 sync_to_drive.py "<pasta do projeto local>" "<pasta destino no Drive>" [--tudo]

Exemplo:
    python3 sync_to_drive.py \\
        "~/Downloads/Relatórios Automatizados/Relatório TCC Ricardo" \\
        "/caminho/Drive/37 - TCC Ricardo/Project_Ricardo"
"""
import os
import sys
import shutil
import fnmatch

# Entregáveis de nível superior (a base bruta .xlsx/.sav fica de fora de propósito;
# tabelas .csv saem dentro de saida_tabelas/).
PADROES = ("*.docx", "*.html", "*.R", "*.r", "*.json", "*.png", "*.pdf", "*.md")
SUBPASTAS = ("saida_figuras", "saida_tabelas")


def copiar_match(origem, destino, padroes=None):
    """Copia arquivos de `origem` para `destino`. Se `padroes` for None, copia
    todos (usado nas subpastas de saída, que só contêm conteúdo gerado)."""
    os.makedirs(destino, exist_ok=True)
    n = 0
    for nome in sorted(os.listdir(origem)):
        cam = os.path.join(origem, nome)
        if not os.path.isfile(cam):
            continue
        # ignora locks/temporários do Office, LibreOffice e macOS
        if nome.startswith("~$") or nome.startswith(".~") or nome.startswith(".#") or nome == ".DS_Store" or nome.endswith(".tmp"):
            continue
        if padroes is None or any(fnmatch.fnmatch(nome, p) for p in padroes):
            shutil.copy2(cam, os.path.join(destino, nome))
            print(f"  -> {nome}")
            n += 1
    return n


def main():
    if len(sys.argv) < 3:
        print('Uso: python3 sync_to_drive.py "<pasta projeto local>" "<pasta destino Drive>" [--tudo]')
        sys.exit(1)

    origem = os.path.expanduser(sys.argv[1]).rstrip("/")
    destino = os.path.expanduser(sys.argv[2])
    tudo = "--tudo" in sys.argv[3:]

    if not os.path.isdir(origem):
        print(f"[ERRO] pasta de origem não existe: {origem}")
        sys.exit(1)

    print(f"Copiando de:\n  {origem}\npara:\n  {destino}\n")

    if tudo:
        alvo = os.path.join(destino, os.path.basename(origem))
        shutil.copytree(origem, alvo, dirs_exist_ok=True)
        print(f"\nPasta inteira copiada -> {alvo}")
        return

    total = copiar_match(origem, destino, PADROES)
    for sp in SUBPASTAS:
        sp_orig = os.path.join(origem, sp)
        if os.path.isdir(sp_orig) and os.listdir(sp_orig):
            print(f"[{sp}/]")
            total += copiar_match(sp_orig, os.path.join(destino, sp))

    print(f"\nConcluído: {total} arquivo(s) levado(s) para o Drive.")


if __name__ == "__main__":
    main()
