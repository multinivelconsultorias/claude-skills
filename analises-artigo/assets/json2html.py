#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Converte conteudo_docx.json (fonte única) em relatório HTML estilo Multinível.
Uso: python3 json2html.py conteudo_docx.json relatorio.html"""
import json, sys, html

def esc(s): return html.escape(str(s), quote=False)

HEADERS = {
 "multinivel": ["Relatório de Análise de dados",
                "Multinível – Soluções em Psicometria e Análise de dados",
                "Julio Cezar Albuquerque da Costa"],
 "naopare":    ["Relatório de Análise de dados",
                "Núcleo de Atenção Orientada para Resultados – NAOPARE",
                "Julio Cezar Albuquerque"],
}

CSS = (
 'body{font-family:"Times New Roman",Georgia,serif;font-size:12pt;line-height:1.5;color:#1a1a1a;'
 'max-width:900px;margin:32px auto;padding:0 24px;text-align:justify}'
 'h1{font-size:15pt;text-align:center;margin:6px 0}'
 'h2{font-size:13pt;border-bottom:1.5px solid #2C5F6F;padding-bottom:3px;margin-top:28px;color:#2C5F6F}'
 'h3{font-size:12pt;margin-top:18px}'
 # corpo: recuo de primeira linha e sem espaçamento entre parágrafos
 'p{margin:0;text-indent:1.25cm}'
 '.sub{text-align:center;font-size:11pt;color:#444;margin:0;text-indent:0}'
 'table{border-collapse:collapse;width:100%;margin:14px 0;font-size:10pt}'
 'th,td{padding:5px 8px}'
 'thead th{border-top:1.2px solid #000;border-bottom:1.2px solid #000;text-align:center}'
 'tbody tr:last-child td{border-bottom:1.2px solid #000}'
 'td:first-child,th:first-child{text-align:left}td{text-align:center}'
 '.nota{font-size:9pt;color:#444;margin:-6px 0 14px;text-indent:0}'
 'caption{caption-side:top;text-align:left;font-weight:bold;font-size:10pt;margin-bottom:4px}'
)

def render_table(b):
    out = ['<table><caption>%s</caption>' % esc(b.get("caption",""))]
    header = b.get("header", []); rows = b.get("rows", [])
    if header:
        out.append('<thead><tr>' + ''.join('<th>%s</th>' % esc(h) for h in header) + '</tr></thead>')
    out.append('<tbody>')
    for r in rows:
        out.append('<tr>' + ''.join('<td>%s</td>' % esc(c) for c in r) + '</tr>')
    out.append('</tbody></table>')
    if b.get("note"):
        note = b["note"]
        if note.lower().startswith("nota."):
            out.append('<p class="nota"><em>Nota.</em>%s</p>' % esc(note[5:]))
        else:
            out.append('<p class="nota">%s</p>' % esc(note))
    return ''.join(out)

def main():
    src, outp = sys.argv[1], sys.argv[2]
    doc = json.load(open(src, encoding="utf-8"))
    org = doc.get("org", "multinivel")
    hdr = HEADERS.get(org, HEADERS["multinivel"])
    H = ['<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">',
         '<title>Relatório de Análise de dados</title>',
         '<style>%s</style></head><body>' % CSS,
         '<h1>%s</h1>' % esc(hdr[0]),
         '<p class="sub">%s</p>' % esc(hdr[1]),
         '<p class="sub">%s</p>' % esc(hdr[2])]
    first_p = False; in_refs = False
    for b in doc.get("blocks", []):
        t = b.get("type")
        if t != "ref" and in_refs:
            H.append('</div>'); in_refs = False
        if t == "p":
            if not first_p:
                H.append('<p class="sub" style="margin-top:8px"><em>%s</em></p>' % esc(b["text"]))
                first_p = True
            else:
                H.append('<p>%s</p>' % esc(b["text"]))
        elif t == "h1":
            H.append('<h2>%s</h2>' % esc(b["text"]))   # seção (Método/Resultados/...)
        elif t == "h2":
            H.append('<h3>%s</h3>' % esc(b["text"]))   # subseção (Análise de dados/Estudo N)
        elif t == "h3":
            H.append('<h4 style="margin-bottom:2px">%s</h4>' % esc(b["text"]))   # hipótese
        elif t == "pagebreak":
            H.append('<hr style="border:none;border-top:1px dashed #ccc;margin:18px 0">')
        elif t == "table":
            H.append(render_table(b))
        elif t == "figure":
            if b.get("path"):
                H.append('<p style="text-align:center;text-indent:0;margin-top:14px"><img src="%s" style="max-width:90%%"></p>' % esc(b["path"]))
            if b.get("caption"):
                H.append('<p class="nota">%s</p>' % esc(b["caption"]))
        elif t == "ref":
            if not in_refs:
                H.append('<div style="font-size:11pt">'); in_refs = True
            H.append('<p style="text-indent:-1.25cm;margin-left:1.25cm">%s</p>' % esc(b["text"]))
    if in_refs:
        H.append('</div>')
    H.append('</body></html>')
    with open(outp, "w", encoding="utf-8") as fh:
        fh.write('\n'.join(H))
    print("OK -> %s (%d blocos)" % (outp, len(doc.get("blocks", []))))

if __name__ == "__main__":
    main()
