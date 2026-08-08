#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Busca referências na OpenAlex, com filtro de recência e marcação de acesso aberto.

Uso:
    python3 busca_openalex.py "forced relocation mental health" --desde 2021 --n 25
    python3 busca_openalex.py "solastalgia" --so-abertas --formato apa
    python3 busca_openalex.py "disaster suicidal ideation" --tipo review

USE DE DUAS A QUATRO PALAVRAS POR BUSCA, e faça várias buscas estreitas em vez
de uma longa. A busca padrão exige que TODAS as palavras apareçam no título ou
no resumo, o que dá precisão alta e recall que despenca: "forced relocation
mental health" devolve 93 resultados com o artigo certo em primeiro lugar;
acrescente "disaster" e caem para 13, quase todos fora do tema.

Se precisar de varredura ampla, use --amplo, que busca no texto todo e ordena
por relevância. O efeito colateral é que trabalhos muito citados e genéricos
sobem ao topo — relatórios do Lancet aparecem em quase qualquer consulta de
saúde. Prefira o padrão e refine os termos.

Por que a OpenAlex: é catálogo aberto, cobre mais de 250 milhões de trabalhos,
não exige chave de API e devolve o status de acesso aberto junto com o registro,
que é exatamente o que se precisa para montar uma lista de referências privilegiando
o que o autor consegue baixar. Não substitui a leitura: serve para descobrir o que
existe e decidir o que vale a pena buscar por inteiro.

Marcação de acesso na saída:
    [OA]  acesso aberto, com link direto para o PDF quando houver
    [$]   fechado; ainda pode valer a pena pelo acesso institucional
    [pre] preprint

Sempre confirme os dados bibliográficos na fonte antes de citar. Metadado de
catálogo tem erro de paginação e de nome com alguma frequência.
"""
import argparse, json, ssl, sys, urllib.parse, urllib.request
from datetime import datetime

API = "https://api.openalex.org/works"
# A OpenAlex pede um e-mail de contato para entrar no "polite pool", que é mais
# rápido e estável. Troque pelo seu.
MAILTO = "pesquisa@exemplo.org"

REMEDIO_SSL = """
O Python desta máquina não tem os certificados raiz instalados, então não
consegue validar a conexão. Duas formas de resolver, em ordem de preferência:

  1) rode o instalador que vem com o Python:
     "/Applications/Python 3.14/Install Certificates.command"

  2) ou instale o pacote de certificados:
     python3 -m pip install --user certifi

Nenhuma das duas desativa a verificação — elas fornecem os certificados que
faltam. Enquanto isso não for feito, use a busca web e verifique cada
referência na fonte.
"""


def contexto_ssl():
    """Contexto TLS com verificação ativa. Nunca desativar: metadado
    bibliográfico vindo de conexão não verificada não é confiável."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def busca(query, desde, n, so_abertas, tipo, amplo, ordem):
    filtros = [f"from_publication_date:{desde}-01-01"]
    if so_abertas:
        filtros.append("is_oa:true")
    if tipo:
        filtros.append(f"type:{tipo}")
    params = {"per-page": min(n, 50), "sort": ordem, "mailto": MAILTO}
    if amplo:
        # busca no texto todo; recall alto, precisão baixa
        params["search"] = query
    else:
        # exige todos os termos no título ou no resumo; é o padrão porque
        # precisão importa mais que volume quando se monta lista de referências
        filtros.insert(0, f"title_and_abstract.search:{query}")
    params["filter"] = ",".join(filtros)
    url = f"{API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": f"pesquisa-academica ({MAILTO})"})
    with urllib.request.urlopen(req, timeout=30, context=contexto_ssl()) as resp:
        return json.load(resp)


def autores(w, limite=6):
    nomes = []
    for a in w.get("authorships", [])[:limite]:
        nome = (a.get("author") or {}).get("display_name") or ""
        partes = nome.split()
        if len(partes) >= 2:
            iniciais = " ".join(f"{p[0]}." for p in partes[:-1])
            nomes.append(f"{partes[-1]}, {iniciais}")
        elif nome:
            nomes.append(nome)
    if len(w.get("authorships", [])) > limite:
        nomes.append("et al.")
    return ", ".join(nomes) or "[sem autoria]"


def periodico(w):
    loc = w.get("primary_location") or {}
    src = loc.get("source") or {}
    return src.get("display_name") or "[sem periódico]"


def acesso(w):
    oa = w.get("open_access") or {}
    if (w.get("type") or "") == "preprint":
        return "[pre]", oa.get("oa_url") or ""
    if oa.get("is_oa"):
        return "[OA]", oa.get("oa_url") or ""
    return "[$] ", ""


def apa(w):
    bib = w.get("biblio") or {}
    vol, iss = bib.get("volume"), bib.get("issue")
    p1, p2 = bib.get("first_page"), bib.get("last_page")
    ref = f"{autores(w)} ({w.get('publication_year','s.d.')}). {w.get('title','[sem título]')}. "
    ref += f"*{periodico(w)}*"
    if vol:
        ref += f", {vol}"
        if iss:
            ref += f"({iss})"
    if p1:
        ref += f", {p1}" + (f"–{p2}" if p2 and p2 != p1 else "")
    ref += "."
    if w.get("doi"):
        ref += f" {w['doi']}"
    return ref


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--desde", type=int, default=datetime.now().year - 5,
                    help="ano inicial (padrão: últimos 5 anos)")
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--so-abertas", action="store_true")
    ap.add_argument("--tipo", default="article",
                    help="article, review, book-chapter, preprint... (vazio = todos)")
    ap.add_argument("--formato", choices=["lista", "apa"], default="lista")
    ap.add_argument("--amplo", action="store_true",
                    help="busca no texto todo em vez de título e resumo; mais recall, menos precisão")
    ap.add_argument("--ordem", default="relevance_score:desc",
                    help="relevance_score:desc | cited_by_count:desc | publication_date:desc")
    a = ap.parse_args()

    n_termos = len(a.query.split())
    if n_termos > 4 and not a.amplo:
        print(f"\nAviso: {n_termos} palavras. A busca exige todas elas no título ou no "
              f"resumo,\ne o recall despenca acima de quatro. Se vier pouca coisa, encurte.",
              file=sys.stderr)

    try:
        dados = busca(a.query, a.desde, a.n, a.so_abertas, a.tipo, a.amplo, a.ordem)
    except ssl.SSLError as e:
        sys.exit(f"Falha de TLS ao consultar a OpenAlex: {e}\n{REMEDIO_SSL}")
    except urllib.error.URLError as e:
        motivo = getattr(e, "reason", e)
        if isinstance(motivo, ssl.SSLError) or "CERTIFICATE_VERIFY_FAILED" in str(motivo):
            sys.exit(f"Falha de TLS ao consultar a OpenAlex: {motivo}\n{REMEDIO_SSL}")
        sys.exit(f"Sem conexão com a OpenAlex: {motivo}\n"
                 f"Use a busca web e verifique cada referência na fonte.")
    except Exception as e:
        sys.exit(f"Falha ao consultar a OpenAlex: {e}\n"
                 f"Use a busca web e verifique cada referência na fonte.")

    itens = dados.get("results", [])
    total = (dados.get("meta") or {}).get("count", 0)
    modo = "texto todo" if a.amplo else "título e resumo"
    print(f'\n"{a.query}" — {modo} — desde {a.desde} — {total} resultados, mostrando {len(itens)}\n')

    if total == 0:
        print("Nada encontrado. Tente, nesta ordem: encurtar para dois termos,\n"
              "trocar por sinônimos do campo, buscar em português, ou --amplo.\n")
        return
    if total < 10 and not a.amplo:
        print("Poucos resultados: a combinação de termos pode estar restritiva demais.\n")

    n_oa = 0
    for i, w in enumerate(itens, 1):
        marca, link = acesso(w)
        if marca == "[OA]":
            n_oa += 1
        if a.formato == "apa":
            print(f"{marca} {apa(w)}")
            if link:
                print(f"      PDF: {link}")
            print()
        else:
            cit = w.get("cited_by_count", 0)
            print(f"{i:>2}. {marca} {w.get('publication_year','s.d.')} · {cit} citações")
            print(f"    {w.get('title','[sem título]')}")
            print(f"    {autores(w, 3)} · {periodico(w)}")
            if w.get("doi"):
                print(f"    {w['doi']}")
            if link:
                print(f"    PDF: {link}")
            print()

    if itens:
        print(f"{n_oa} de {len(itens)} em acesso aberto.")
    print("Confirme autores, ano, volume e páginas na fonte antes de citar.\n")


if __name__ == "__main__":
    main()
