#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setup_workspace.py — Prepara o workspace LOCAL para um relatório Multinível.

Filosofia "local-first": todo o trabalho (bases, scripts, saídas e .docx) acontece
em disco local rápido, NUNCA direto no Google Drive (que é lento/instável). Só o
resultado final é levado para o Drive depois, com sync_to_drive.py.

Estrutura criada:
    ~/Downloads/Relatórios Automatizados/        <- pasta geral (todos os relatórios)
        <Nome do Projeto>/                       <- uma pasta por projeto/banco
            <base copiada>.xlsx
            analise_template.R  build_report.py  explore_data.py
            template_multinivel.py  marca_dagua.py  + PNGs do cabeçalho, rodapé, marca d'água e logo
            saida_tabelas/   saida_figuras/

Uso:
    python3 setup_workspace.py "<Nome do Projeto>" "<base1>" ["<base2>" ...]
    python3 setup_workspace.py "<Nome do Projeto>"            # só atualiza os scripts de um projeto existente

Exemplo:
    python3 setup_workspace.py "Relatório TCC Ricardo" \\
        "/caminho/Project_Ricardo/Banco_tratado.xlsx"

O que faz:
    1. Cria ~/Downloads/Relatórios Automatizados/ (se não existir).
    2. Cria a pasta do projeto dentro dela.
    3. Copia cada base informada para a pasta do projeto (download do Drive 1x).
    4. Copia os scripts de apoio da skill para a pasta do projeto (self-contained).
    5. Cria as subpastas saida_tabelas/ e saida_figuras/.
    6. Imprime o caminho do projeto na linha PROJETO_DIR=... (use como diretório
       de trabalho de todas as análises).
"""
import os
import sys
import shutil

PASTA_GERAL = "Relatórios Automatizados"
SCRIPTS_SKILL = ("analise_template.R", "build_report.py", "explore_data.py",
                 "template_multinivel.py", "marca_dagua.py",        # identidade visual (modelo 23/10/2026)
                 "cabecalho-multinivel.png", "rodape-multinivel.png", "marca-dagua-multinivel.png",
                 "logo-multinivel-horizontal.png")                  # logo avulsa (opcional, desligada)


def main():
    if len(sys.argv) < 2:
        print('Uso: python3 setup_workspace.py "<Nome do Projeto>" ["<base1>" "<base2>" ...]')
        print('     (só com o nome do projeto: atualiza os scripts de apoio de um projeto já existente)')
        sys.exit(1)

    projeto = sys.argv[1].strip()
    bases = sys.argv[2:]

    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    pasta_proj = os.path.join(downloads, PASTA_GERAL, projeto)
    os.makedirs(os.path.join(pasta_proj, "saida_tabelas"), exist_ok=True)
    os.makedirs(os.path.join(pasta_proj, "saida_figuras"), exist_ok=True)

    print(f"Workspace local: {pasta_proj}\n")

    # 1. Copiar as bases para o projeto (download sob demanda do Drive, 1x só)
    copiadas = []
    for b in bases:
        b = os.path.expanduser(b)
        if not os.path.isfile(b):
            print(f"  [AVISO] base não encontrada, pulando: {b}")
            continue
        dst = os.path.join(pasta_proj, os.path.basename(b))
        shutil.copy2(b, dst)
        copiadas.append(dst)
        print(f"  base   -> {os.path.basename(dst)}")

    # 2. Copiar os scripts de apoio da skill (mesma pasta deste arquivo). Em projeto já
    #    existente, ATUALIZA as cópias (guardando a anterior se for diferente): uma cópia
    #    antiga de build_report.py gera relatório fora do padrão (sem logo/marca d'água).
    import filecmp, time
    assets_dir = os.path.dirname(os.path.abspath(__file__))
    carimbo = time.strftime("%Y%m%d-%H%M")
    for nome in SCRIPTS_SKILL:
        src = os.path.join(assets_dir, nome)
        dst = os.path.join(pasta_proj, nome)
        if not os.path.isfile(src):
            print(f"  [AVISO] faltando na skill: {nome}")
            continue
        if os.path.isfile(dst) and not filecmp.cmp(src, dst, shallow=False):
            shutil.copy2(dst, f"{dst}.anterior-{carimbo}")
            shutil.copy2(src, dst)
            print(f"  script ATUALIZADO -> {nome} (versão anterior guardada como {nome}.anterior-{carimbo})")
        elif os.path.isfile(dst):
            print(f"  script ok -> {nome}")
        else:
            shutil.copy2(src, dst)
            print(f"  script -> {nome}")

    if bases and not copiadas:
        print("\n  [AVISO] Nenhuma base foi copiada. Confira os caminhos informados.")

    # Linha machine-readable com o diretório do projeto
    print(f"\nPROJETO_DIR={pasta_proj}")
    print("\nPronto. Rode as análises com este diretório como working dir, ex.:")
    print(f'  LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 Rscript -e \'setwd("{pasta_proj}"); source("analise_projeto.R")\'')


if __name__ == "__main__":
    main()
