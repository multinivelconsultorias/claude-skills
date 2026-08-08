# Especificação de formatação — APA 7 + Word (Multinível / NAOPARE)

> Confirmado por inspeção direta dos `.docx` de 2024–2026 (perfil de 328 arquivos +
> leitura do XML do estilo de tabela). É o que o gerador `assets/build_report.py` aplica.

## Corpo do texto
- **Fonte:** Times New Roman.
- **Tamanho:** 12 pt.
- **Entrelinhas:** 1,5.
- **Espaço depois do parágrafo:** **0 pt** (preferência do Julio). **Não** se usa espaçamento entre parágrafos do mesmo bloco; o espaçamento aparece **só entre seções** (espaço *antes* dos títulos: 18 pt antes de Nível 1, 14 pt antes de Nível 2, 10 pt antes de Nível 3).
- **Recuo de primeira linha:** **1,25 cm** (equivale a um "tab") em todo parágrafo de corpo. Títulos, legendas, notas e referências **não** recebem recuo de primeira linha.
  - *(Alternativa "bloco" antiga, se algum cliente pedir: 12 pt depois + 0 de recuo. Parametrizável em `space_after_pt` e `first_line_indent_cm`.)*
- **Alinhamento:** justificado.
- **Margens:** 2,5 cm (padrão APA) em todos os lados. *(ABNT usa 3 cm esq./sup. e 2 cm dir./inf. — parametrizável.)*
- **Idioma:** pt-BR (vírgula decimal).

## Títulos (cabeçalhos de seção)
- **Nível 1** (Método, Resultados, Referências): Times New Roman, **negrito**, 12 pt, centralizado (APA Nível 1).
- **Nível 2** (Análise de dados, Participantes, Estudo N): negrito, alinhado à esquerda.
- **Nível 3** (subanálises): negrito itálico, à esquerda.
- Sem numeração automática nos títulos (estilo do autor).

## Tabelas (estilo "Estilo2" = APA) — CONFIRMADO no XML
- **Bordas:** apenas **linha superior e inferior** da tabela + **linha sob a linha de cabeçalho**. **Nenhuma linha vertical**; nenhuma linha interna entre linhas de dados. Espessura **0,5 pt** (`sz=4`), cor preta. *(Medido: Estilo2 tem `top: single sz=4` e `bottom: single sz=4`.)*
- **Fonte interna:** Times New Roman **10 pt** (corpo e cabeçalho).
- **Cabeçalho:** negrito, centralizado, com borda inferior.
- **Células de dados:** rótulos (1ª coluna) à esquerda; números centralizados.
- **Largura:** **autoajuste de conteúdo** (AutoFit to Contents), sem larguras fixas.
- **Título da tabela:** como **primeira linha da própria tabela**, **mesclada em todas as colunas** e **sem bordas** (integrada à tabela, fica "invisível"), no formato **"Tabela N. Título descritivo"**. *(Preferência do Julio, jun/2026; antes ficava como parágrafo acima.)*
- **Nota:** **abaixo**, iniciando com "Nota." (com "Nota" em itálico), 10 pt, explicando abreviações e significâncias. Ver `01-estilo-de-escrita.md` §6.1.
- Tabela vinda de software externo: "Fonte: Elaborado pelo autor."

## Figuras
- **Legenda:** **abaixo** da figura (estilo do autor), formato **"Figura N. Título"**, 12 pt.
- Imagem centralizada, largura ~16 cm, 300 dpi (ver `05-graficos.md`).
- Quando aplicável: "Fonte: Elaborado pelo autor."

## Referências
- Seção "Referências" (Nível 1).
- **APA 7**, ordem alfabética por sobrenome.
- **Recuo deslocado** (hanging indent) de 1,25 cm.
- Times New Roman 12, entrelinha 1,5.
- Só incluir o que foi citado. Banco completo em `03-referencias-apa7.md`.

## Resumo legível por máquina (defaults do gerador)
```json
{
  "font": "Times New Roman",
  "body_size_pt": 12,
  "line_spacing": 1.5,
  "space_after_pt": 0,
  "first_line_indent_cm": 1.25,
  "justify": true,
  "margins_cm": 2.5,
  "table_font_size_pt": 10,
  "table_style": "apa_top_bottom_header",
  "table_border_pt": 0.5,
  "caption_table_position": "merged_title_row",
  "table_autofit": "contents",
  "caption_figure_position": "below",
  "references_hanging_indent_cm": 1.25
}
```
