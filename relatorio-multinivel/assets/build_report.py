#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_report.py — Gera um .docx no estilo Multinível (APA 7).

Uso:
    python3 build_report.py conteudo.json saida.docx [--sem-faixas] [--sem-marca] [--com-logo]

Identidade visual (padrão desde 23/10/2026, igual ao relatório-modelo da Cristiane 17.10):
cabeçalho e rodapé em faixa com o número da página e a marca d'água da Multinível em todas
as páginas (template_multinivel.py). --sem-faixas / --sem-marca, ou "options":
{"faixas": false} / {"marca_dagua": false}, desligam cada parte. A logo avulsa no topo da
1ª página fica desligada (a faixa já traz a logo); --com-logo ou {"logo": true} a liga.

Requer: python-docx  (pip install python-docx)

Marcação inline aceita em qualquer texto: **negrito** e *itálico*
(asteriscos de significância como "5,708*" ou "* p < 0,05" ficam literais).

Formato do JSON de conteúdo (todos os campos opcionais exceto "blocks"):
{
  "org": "multinivel",                       # cabeçalho de 3 linhas (SEMPRE multinivel;
                                             #  "naopare" foi descontinuado e cai no default)
  "title": "Relatório de Análise de dados", # linha 1 (default por org)
  "author": "Julio Cezar Albuquerque da Costa",
  "options": {                               # sobrescreve defaults de formatação
      "space_after_pt": 12, "first_line_indent_cm": 0, "table_font_size_pt": 10,
      "body_size_pt": 12, "line_spacing": 1.5, "margins_cm": 2.5, "justify": true,
      "faixas": true, "marca_dagua": true, "marca_dagua_largura_cm": 13, "marca_dagua_pular_primeira": false,
      "logo": false, "logo_largura_cm": 5.5
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
     {"type": "ref", "text": "Miot, H. A. (2017). Avaliação... *Jornal Vascular Brasileiro, 16*(2)"}
  ]
}
"""
import sys, json, os, re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

VERSAO = "2026-10-23.2"  # data da última mudança de comportamento; comparada com a cópia canônica da skill
SKILL_CANONICA = os.path.expanduser("~/.claude/skills/relatorio-multinivel/assets")


def verificar_versao():
    """Cada projeto trabalha com uma CÓPIA deste script (setup_workspace.py). Se a skill tiver
    mudado depois, a cópia gera relatório fora do padrão (ex.: sem logo e sem marca d'água).
    Avisa alto quando a cópia canônica da skill é mais nova do que este arquivo."""
    try:
        canon = os.path.join(SKILL_CANONICA, "build_report.py")
        aqui = os.path.abspath(__file__)
        if not os.path.isfile(canon) or os.path.samefile(aqui, canon):
            return
        m = re.search(r'^VERSAO = "([^"]+)"', open(canon, encoding="utf-8").read(), re.M)
        if m and m.group(1) > VERSAO:
            print(f"[ATENÇÃO] Este build_report.py ({VERSAO}) está DESATUALIZADO em relação à skill ({m.group(1)}).")
            print(f"          Rode de novo: python3 \"{os.path.join(SKILL_CANONICA, 'setup_workspace.py')}\" \"<Nome do Projeto>\"")
            print("          (atualiza os scripts de apoio sem apagar nada) e gere o relatório outra vez.")
    except Exception:
        pass


DEFAULTS = {
    "font": "Times New Roman",
    "body_size_pt": 12,
    "line_spacing": 1.5,
    "space_after_pt": 0,
    "first_line_indent_cm": 1.25,
    "justify": True,
    "margins_cm": 2.5,
    "table_font_size_pt": 10,
    "references_hanging_indent_cm": 1.25,
    "lang": "pt-BR",
    # Identidade visual do relatório-modelo aprovado em 23/10/2026 (template_multinivel.py):
    # cabeçalho e rodapé em faixa (com nº de página) e marca d'água (símbolo rede-M, g-600 a 14%,
    # nós vazados com sombra, 13 cm, atrás do texto, todas as páginas).
    "faixas": True,
    "marca_dagua": True,
    "marca_dagua_largura_cm": 13.0,
    "marca_dagua_pular_primeira": False,
    # Logo avulsa no topo da 1ª página: DESLIGADA, porque a faixa do cabeçalho já traz a logo.
    "logo": False,
    "logo_largura_cm": 5.5,
    "logo_espaco_pt": 10,
}

HEADERS = {
    "multinivel": ["Relatório de Análise de dados",
                   "Multinível – Soluções em Psicometria e Análise de dados",
                   "Julio Cezar Albuquerque da Costa"],
    # NAOPARE descontinuado (set/2026): mantido como alias do cabeçalho Multinível
    # para que relatórios antigos não quebrem.
    "naopare":    ["Relatório de Análise de dados",
                   "Multinível – Soluções em Psicometria e Análise de dados",
                   "Julio Cezar Albuquerque da Costa"],
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


# ---------------------------------------------------------------------------
# Marcação inline: **negrito** e *itálico* (corpo, células, notas, referências).
# Os delimitadores exigem conteúdo colado (sem espaço) e não podem estar
# encostados em letra/dígito do lado de fora. Isso preserva os asteriscos de
# significância ("5,708*", "* p < 0,05; ** p < 0,01; *** p < 0,001").
# ---------------------------------------------------------------------------
import re as _re
_BOLD = _re.compile(r'(?<![*\w])\*\*(?=[^\s*])(.+?)(?<=[^\s*])\*\*(?![*\w])')
_ITAL = _re.compile(r'(?<![*\w])\*(?=[^\s*])(.+?)(?<=[^\s*])\*(?![*\w])')


def parse_inline(text, bold=False, italic=False):
    segs, pos = [], 0
    while pos < len(text):
        cands = [m for m in (_BOLD.search(text, pos), _ITAL.search(text, pos)) if m]
        if not cands:
            segs.append((text[pos:], bold, italic))
            break
        m = min(cands, key=lambda x: (x.start(), 0 if x.re is _BOLD else 1))
        if m.start() > pos:
            segs.append((text[pos:m.start()], bold, italic))
        if m.re is _BOLD:
            segs += parse_inline(m.group(1), True, italic)
        else:
            segs += parse_inline(m.group(1), bold, True)
        pos = m.end()
    return [sg for sg in segs if sg[0]]


def add_rich(par, text, size, font, bold=False, italic=False):
    for t, b, i in parse_inline(str(text), bold, italic):
        style_run(par.add_run(t), size, bold=b, italic=i, font=font)


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
    add_rich(p, text, size if size else opt["body_size_pt"], opt["font"], bold=bold, italic=italic)
    return p


def set_autofit_contents(tbl):
    """Força AutoAjuste de conteúdo (tblLayout=autofit, larguras automáticas)."""
    tbl.autofit = True
    tbl.allow_autofit = True
    tblPr = tbl._tbl.tblPr
    layout = tblPr.find(qn('w:tblLayout'))
    if layout is None:
        layout = OxmlElement('w:tblLayout'); tblPr.append(layout)
    layout.set(qn('w:type'), 'autofit')
    tblW = tblPr.find(qn('w:tblW'))
    if tblW is None:
        tblW = OxmlElement('w:tblW'); tblPr.append(tblW)
    tblW.set(qn('w:type'), 'auto'); tblW.set(qn('w:w'), '0')
    for row in tbl.rows:
        for cell in row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcW = tcPr.find(qn('w:tcW'))
            if tcW is None:
                tcW = OxmlElement('w:tcW'); tcPr.append(tcW)
            tcW.set(qn('w:type'), 'auto'); tcW.set(qn('w:w'), '0')


def add_table(doc, block, opt, trailing_space=12):
    header = block.get("header", [])
    rows = block.get("rows", [])
    ncol = len(header) if header else (len(rows[0]) if rows else 1)
    tbl = doc.add_table(rows=0, cols=ncol)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tsize = block.get("font_size_pt", opt["table_font_size_pt"])   # tamanho por tabela (opcional)
    border = {'sz': 4, 'val': 'single', 'color': '000000'}

    # título como 1ª linha da tabela: mesclada em todas as colunas e SEM bordas
    if block.get("caption"):
        cells = tbl.add_row().cells
        merged = cells[0]
        for c in cells[1:]:
            merged = merged.merge(c)
        par = merged.paragraphs[0]
        fmt_paragraph(par, opt, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=2,
                      line_spacing=1.0, first_line_indent=0)
        add_rich(par, block["caption"], opt["body_size_pt"], opt["font"])
        set_cell_border(merged, top=None, bottom=None, left=None, right=None)

    # header row
    if header:
        hr = tbl.add_row().cells
        for i, htext in enumerate(header):
            par = hr[i].paragraphs[0]
            fmt_paragraph(par, opt, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2,
                          line_spacing=1.0, first_line_indent=0)
            add_rich(par, str(htext), tsize, opt["font"], bold=True)
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
            add_rich(par, val, tsize, opt["font"])
            # only bottom border on the very last row (table bottom)
            set_cell_border(cells[ci], top=None,
                            bottom=border if is_last else None,
                            left=None, right=None)

    set_autofit_contents(tbl)
    # note below
    if block.get("note"):
        np = doc.add_paragraph()
        fmt_paragraph(np, opt, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=trailing_space,
                      first_line_indent=0)
        # "Nota." in italic, rest regular
        note = block["note"]
        if note.lower().startswith("nota."):
            r1 = np.add_run("Nota.")
            style_run(r1, tsize, italic=True, font=opt["font"])
            add_rich(np, note[5:], tsize, opt["font"])
        else:
            add_rich(np, note, tsize, opt["font"])


def add_figure(doc, block, opt, trailing_space=12):
    from docx.shared import Inches
    if block.get("path") and os.path.exists(block["path"]):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fmt_paragraph(p, opt, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2,
                      first_line_indent=0)
        run = p.add_run()
        run.add_picture(block["path"], width=Cm(block.get("width_cm", 15)))
    else:
        add_para(doc, f"[Figura ausente: {block.get('path','?')}]", opt,
                 italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=0)
    if block.get("caption"):
        add_para(doc, block["caption"], opt, size=opt["body_size_pt"],
                 align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=0, space_after=trailing_space)


# ---------------------------------------------------------------------------
# Idioma do documento. Sem isto o Word abre o .docx com o idioma da instalação
# e sublinha o texto inteiro como erro de digitação. Marca-se o padrão do
# documento, cada estilo e cada run já escrito.
# ---------------------------------------------------------------------------
def _lang_mark(rpr, idioma):
    lang = rpr.find(qn('w:lang'))
    if lang is None:
        lang = OxmlElement('w:lang')
        rpr.append(lang)
    lang.set(qn('w:val'), idioma)
    lang.set(qn('w:eastAsia'), idioma)
    if lang.get(qn('w:bidi')) is None:
        lang.set(qn('w:bidi'), 'ar-SA')


def _lang_get_or_add(pai, tag):
    el = pai.find(qn(tag))
    if el is None:
        el = OxmlElement(tag)
        pai.insert(0, el)
    return el


def set_document_language(doc, idioma="pt-BR"):
    raiz = doc.styles.element
    defaults = _lang_get_or_add(raiz, 'w:docDefaults')
    rpr_default = _lang_get_or_add(defaults, 'w:rPrDefault')
    _lang_mark(_lang_get_or_add(rpr_default, 'w:rPr'), idioma)
    for estilo in raiz.findall(qn('w:style')):
        rpr = estilo.find(qn('w:rPr'))
        if rpr is None:
            rpr = OxmlElement('w:rPr')
            estilo.append(rpr)
        _lang_mark(rpr, idioma)
    for run in doc.element.body.iter(qn('w:r')):
        _lang_mark(_lang_get_or_add(run, 'w:rPr'), idioma)
    try:
        st = doc.settings.element
        tfl = st.find(qn('w:themeFontLang'))
        if tfl is None:
            tfl = OxmlElement('w:themeFontLang')
            st.append(tfl)
        tfl.set(qn('w:val'), idioma)
        tfl.set(qn('w:eastAsia'), idioma)
    except Exception:
        pass


def aplicar_identidade(doc, opt):
    """Identidade visual do relatório-modelo (23/10/2026): cabeçalho e rodapé em faixa com o
    número da página, e marca d'água em todas as páginas. Usa template_multinivel.py e os PNGs
    que ficam ao lado deste script (o setup_workspace.py copia tudo para o PROJETO_DIR)."""
    aqui = os.path.dirname(os.path.abspath(__file__))
    if aqui not in sys.path:
        sys.path.insert(0, aqui)
    try:
        import template_multinivel
    except ImportError:
        print("[AVISO] template_multinivel.py não está ao lado do build_report.py: relatório SEM cabeçalho, rodapé e marca d'água.")
        return None
    return template_multinivel.aplicar_template(
        doc, faixas=bool(opt.get("faixas", True)), marca=bool(opt.get("marca_dagua", True)),
        largura_marca_cm=float(opt.get("marca_dagua_largura_cm", 13.0)),
        pular_primeira=bool(opt.get("marca_dagua_pular_primeira", False)))


def inserir_logo(doc, opt):
    """Logo horizontal da Multinível (versão para fundo claro) centralizada no topo da primeira
    página, acima do cabeçalho. Usa logo-multinivel-horizontal.png, que fica ao lado deste script
    (o setup_workspace.py copia para o PROJETO_DIR). Se faltar, avisa e segue sem a logo."""
    aqui = os.path.dirname(os.path.abspath(__file__))
    png = os.path.join(aqui, "logo-multinivel-horizontal.png")
    if not os.path.isfile(png):
        print("[AVISO] logo-multinivel-horizontal.png não está ao lado do build_report.py: relatório SEM a logo no topo.")
        return False
    p = doc.add_paragraph()
    fmt_paragraph(p, opt, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=float(opt.get("logo_espaco_pt", 10)),
                  first_line_indent=0, line_spacing=1.0)
    p.add_run().add_picture(png, width=Cm(float(opt.get("logo_largura_cm", 5.5))))
    print(f"Logo Multinível inserida no topo ({opt.get('logo_largura_cm', 5.5)} cm).")
    return True


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

    # logo da Multinível no topo da 1ª página (acima do cabeçalho de 3 linhas)
    if opt.get("logo", False):
        inserir_logo(doc, opt)

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
    # (o espaço antes do 1º título já separa do cabeçalho)
    justify = WD_ALIGN_PARAGRAPH.JUSTIFY if opt["justify"] else WD_ALIGN_PARAGRAPH.LEFT

    # Espaço só em transições: antes dos títulos (space_before) e ao redor de
    # figuras/tabelas. Parágrafos de corpo em sequência não recebem espaço (só recuo).
    blocks = content.get("blocks", [])
    SB = {"h1": 18, "h2": 14, "h3": 10}
    for i, block in enumerate(blocks):
        t = block.get("type")
        nxt = blocks[i + 1].get("type") if i + 1 < len(blocks) else None
        if t in ("h1", "h2", "h3"):
            add_para(doc, block["text"], opt, bold=True, italic=(t == "h3"),
                     align=WD_ALIGN_PARAGRAPH.CENTER if t == "h1" else WD_ALIGN_PARAGRAPH.LEFT,
                     first_line_indent=0, space_before=SB[t], space_after=0)
        elif t == "p":
            sa = 12 if nxt in ("figure", "table") else 0
            add_para(doc, block["text"], opt, align=justify,
                     first_line_indent=opt["first_line_indent_cm"], space_after=sa)
        elif t == "table":
            add_table(doc, block, opt, trailing_space=(0 if nxt in ("h1", "h2", "h3") else 12))
        elif t == "figure":
            add_figure(doc, block, opt, trailing_space=(0 if nxt in ("h1", "h2", "h3") else 12))
        elif t == "ref":
            p = doc.add_paragraph()
            fmt_paragraph(p, opt, align=WD_ALIGN_PARAGRAPH.LEFT,
                          hanging=opt["references_hanging_indent_cm"])
            add_rich(p, block["text"], opt["body_size_pt"], opt["font"])
        elif t == "pagebreak":
            doc.add_page_break()
        else:
            # unknown -> treat as paragraph
            if block.get("text"):
                add_para(doc, block["text"], opt, align=justify,
                         first_line_indent=opt["first_line_indent_cm"])

    if opt.get("faixas", True) or opt.get("marca_dagua", True):
        aplicar_identidade(doc, opt)
    set_document_language(doc, opt.get("lang") or "pt-BR")
    doc.save(out_path)
    print(f"OK -> {out_path}")


def main():
    print(f"build_report.py {VERSAO}")
    verificar_versao()
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)
    with open(args[0], encoding="utf-8") as fh:
        content = json.load(fh)
    if "--sem-marca" in flags:
        content.setdefault("options", {})["marca_dagua"] = False
    if "--sem-faixas" in flags:
        content.setdefault("options", {})["faixas"] = False
    if "--com-logo" in flags:
        content.setdefault("options", {})["logo"] = True
    build(content, args[1])


if __name__ == "__main__":
    main()
