#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_report.py — Gera um .docx no estilo Multinível/NAOPARE (APA 7).

Uso:
    python3 build_report.py conteudo.json saida.docx

Requer: python-docx  (pip install python-docx)

Formato do JSON de conteúdo (todos os campos opcionais exceto "blocks"):
{
  "org": "multinivel" | "naopare",          # define o cabeçalho de 3 linhas
  "title": "Relatório de Análise de dados", # linha 1 (default por org)
  "author": "Julio Cezar Albuquerque da Costa",
  "options": {                               # sobrescreve defaults de formatação
      "space_after_pt": 12, "first_line_indent_cm": 0, "table_font_size_pt": 10,
      "body_size_pt": 12, "line_spacing": 1.5, "margins_cm": 2.5, "justify": true
  },
  "blocks": [
     {"type": "h1", "text": "Método"},
     {"type": "h2", "text": "Análise de dados"},
     {"type": "p",  "text": "O software R foi utilizado..."},
     {"type": "table",
        "caption": "Tabela 1. Características sociodemográficas",
        "header": ["Variável", "Categoria", "n", "%"],
        "rows": [["Sexo","Feminino","66","65,4"], ["","Masculino","35","34,7"]],
        "note": "Nota. n: frequência; %: percentual."},
     {"type": "figure", "path": "figura_1.png", "caption": "Figura 1. Boxplot dos escores por grupo"},
     {"type": "h1", "text": "Referências"},
     {"type": "ref", "text": "Miot, H. A. (2017). Avaliação da normalidade..."}
  ]
}
"""
import sys, json, os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

DEFAULTS = {
    "font": "Times New Roman",
    "body_size_pt": 12,
    "line_spacing": 1.5,
    "space_after_pt": 12,
    "first_line_indent_cm": 0,
    # separação entre blocos (títulos, tabelas e figuras) e o texto que os cerca;
    # independe do espaçamento entre parágrafos de corpo
    "block_gap_pt": 12,
    "justify": True,
    "margins_cm": 2.5,
    "table_font_size_pt": 10,
    "references_hanging_indent_cm": 1.25,
}

HEADERS = {
    "multinivel": ["Relatório de Análise de dados",
                   "Multinível – Soluções em Psicometria e Análise de dados",
                   "Julio Cezar Albuquerque da Costa"],
    "naopare":    ["Relatório de Análise de dados",
                   "Núcleo de Atenção Orientada para Resultados – NAOPARE",
                   "Julio Cezar Albuquerque"],
}


def set_cell_border(cell, **kwargs):
    """Aplica bordas a uma célula. kwargs: top/bottom/left/right = dict(sz, val, color)."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.find(qn('w:tcBorders'))
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    for edge in ('top', 'bottom', 'left', 'right'):
        spec = kwargs.get(edge)
        el = tcBorders.find(qn('w:' + edge))
        if el is None:
            el = OxmlElement('w:' + edge)
            tcBorders.append(el)
        if spec is None:
            el.set(qn('w:val'), 'nil')
        else:
            el.set(qn('w:val'), spec.get('val', 'single'))
            el.set(qn('w:sz'), str(spec.get('sz', 4)))
            el.set(qn('w:space'), '0')
            el.set(qn('w:color'), spec.get('color', '000000'))


def style_run(run, size, bold=False, italic=False, font="Times New Roman"):
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    # ensure complex/East-Asian also use the font
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.append(rfonts)
    for attr in ('w:ascii', 'w:hAnsi', 'w:cs'):
        rfonts.set(qn(attr), font)


def fmt_paragraph(p, opt, align=None, space_after=None, first_line_indent=None,
                  line_spacing=None, hanging=None, space_before=None):
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = line_spacing if line_spacing is not None else opt["line_spacing"]
    pf.space_before = Pt(space_before if space_before is not None else 0)
    pf.space_after = Pt(space_after if space_after is not None else opt["space_after_pt"])
    if align is not None:
        p.alignment = align
    if first_line_indent is not None:
        pf.first_line_indent = Cm(first_line_indent)
    if hanging is not None:
        pf.left_indent = Cm(hanging)
        pf.first_line_indent = Cm(-hanging)


def add_para(doc, text, opt, size=None, bold=False, italic=False, align=None,
             space_after=None, first_line_indent=None, space_before=None):
    p = doc.add_paragraph()
    fmt_paragraph(p, opt, align=align, space_after=space_after,
                  first_line_indent=first_line_indent, space_before=space_before)
    run = p.add_run(text)
    style_run(run, size if size else opt["body_size_pt"], bold=bold, italic=italic,
              font=opt["font"])
    return p


def add_table(doc, block, opt):
    # caption above
    if block.get("caption"):
        cap = add_para(doc, block["caption"], opt, size=opt["body_size_pt"],
                       bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=2,
                       first_line_indent=0, space_before=opt["block_gap_pt"])
    header = block.get("header", [])
    rows = block.get("rows", [])
    ncol = len(header) if header else (len(rows[0]) if rows else 1)
    tbl = doc.add_table(rows=0, cols=ncol)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = True
    tsize = opt["table_font_size_pt"]
    border = {'sz': 4, 'val': 'single', 'color': '000000'}

    # header row
    if header:
        hr = tbl.add_row().cells
        for i, htext in enumerate(header):
            par = hr[i].paragraphs[0]
            fmt_paragraph(par, opt, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2,
                          line_spacing=1.0, first_line_indent=0)
            r = par.add_run(str(htext))
            style_run(r, tsize, bold=True, font=opt["font"])
            # top border for header (table top) + bottom border (under header)
            set_cell_border(hr[i], top=border, bottom=border, left=None, right=None)

    # data rows
    for ri, row in enumerate(rows):
        cells = tbl.add_row().cells
        is_last = (ri == len(rows) - 1)
        for ci in range(ncol):
            val = str(row[ci]) if ci < len(row) else ""
            par = cells[ci].paragraphs[0]
            align = WD_ALIGN_PARAGRAPH.LEFT if ci == 0 else WD_ALIGN_PARAGRAPH.CENTER
            fmt_paragraph(par, opt, align=align, space_after=2, line_spacing=1.0,
                          first_line_indent=0)
            r = par.add_run(val)
            style_run(r, tsize, font=opt["font"])
            # only bottom border on the very last row (table bottom)
            set_cell_border(cells[ci], top=None,
                            bottom=border if is_last else None,
                            left=None, right=None)
    # note below
    if block.get("note"):
        np = doc.add_paragraph()
        fmt_paragraph(np, opt, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=opt["block_gap_pt"],
                      first_line_indent=0)
        # "Nota." in italic, rest regular
        note = block["note"]
        if note.lower().startswith("nota."):
            r1 = np.add_run("Nota.")
            style_run(r1, tsize, italic=True, font=opt["font"])
            r2 = np.add_run(note[5:])
            style_run(r2, tsize, font=opt["font"])
        else:
            r = np.add_run(note)
            style_run(r, tsize, font=opt["font"])


def add_figure(doc, block, opt):
    from docx.shared import Inches
    if block.get("path") and os.path.exists(block["path"]):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fmt_paragraph(p, opt, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2,
                      first_line_indent=0, space_before=opt["block_gap_pt"])
        run = p.add_run()
        run.add_picture(block["path"], width=Cm(block.get("width_cm", 15)))
    else:
        add_para(doc, f"[Figura ausente: {block.get('path','?')}]", opt,
                 italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=0,
                 space_before=opt["block_gap_pt"])
    if block.get("caption"):
        add_para(doc, block["caption"], opt, size=opt["body_size_pt"],
                 align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=0,
                 space_after=opt["block_gap_pt"])


def build(content, out_path):
    opt = dict(DEFAULTS)
    opt.update(content.get("options", {}) or {})
    doc = Document()

    # base Normal style
    normal = doc.styles['Normal']
    normal.font.name = opt["font"]
    normal.font.size = Pt(opt["body_size_pt"])

    # margins
    for section in doc.sections:
        section.top_margin = Cm(opt["margins_cm"])
        section.bottom_margin = Cm(opt["margins_cm"])
        section.left_margin = Cm(opt["margins_cm"])
        section.right_margin = Cm(opt["margins_cm"])

    # header (3 lines, centered)
    org = content.get("org", "multinivel")
    hdr = list(HEADERS.get(org, HEADERS["multinivel"]))
    if content.get("title"):
        hdr[0] = content["title"]
    if content.get("author"):
        hdr[2] = content["author"]
    for i, line in enumerate(hdr):
        add_para(doc, line, opt, size=opt["body_size_pt"], bold=(i == 0),
                 align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2, first_line_indent=0)
    # small gap
    add_para(doc, "", opt, space_after=opt["block_gap_pt"], first_line_indent=0)

    justify = WD_ALIGN_PARAGRAPH.JUSTIFY if opt["justify"] else WD_ALIGN_PARAGRAPH.LEFT

    for block in content.get("blocks", []):
        t = block.get("type")
        if t == "h1":
            add_para(doc, block["text"], opt, bold=True,
                     align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=0,
                     space_before=opt["block_gap_pt"])
        elif t == "h2":
            add_para(doc, block["text"], opt, bold=True,
                     align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=0,
                     space_before=opt["block_gap_pt"])
        elif t == "h3":
            add_para(doc, block["text"], opt, bold=True, italic=True,
                     align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=0,
                     space_before=opt["block_gap_pt"])
        elif t == "p":
            add_para(doc, block["text"], opt, align=justify,
                     first_line_indent=opt["first_line_indent_cm"])
        elif t == "table":
            add_table(doc, block, opt)
        elif t == "figure":
            add_figure(doc, block, opt)
        elif t == "ref":
            p = doc.add_paragraph()
            fmt_paragraph(p, opt, align=WD_ALIGN_PARAGRAPH.LEFT,
                          hanging=opt["references_hanging_indent_cm"])
            r = p.add_run(block["text"])
            style_run(r, opt["body_size_pt"], font=opt["font"])
        elif t == "pagebreak":
            doc.add_page_break()
        else:
            # unknown -> treat as paragraph
            if block.get("text"):
                add_para(doc, block["text"], opt, align=justify,
                         first_line_indent=opt["first_line_indent_cm"])

    doc.save(out_path)
    print(f"OK -> {out_path}")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as fh:
        content = json.load(fh)
    build(content, sys.argv[2])


if __name__ == "__main__":
    main()
