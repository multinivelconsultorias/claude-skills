# Skill: relatorio-multinivel

Gera relatórios de consultoria em análise de dados/psicometria no **estilo da Multinível / NAOPARE**
(Julio Cezar). Lê a base → define/aplica o delineamento estatístico → escreve o código R →
roda as análises → escreve o relatório fiel ao estilo, cobrindo os 6 tópicos.

## Como usar
No Claude Code, em qualquer projeto:
```
/relatorio-multinivel
```
ou descreva a tarefa (ex.: "analise esta base .xlsx e escreva o relatório no meu estilo").
A skill é acionada por gatilhos como "relatório Multinível", "relatório de análise de dados",
"delineamento estatístico", "relatório psicométrico".

## Estrutura
```
relatorio-multinivel/
├── SKILL.md                         # instruções principais + procedimento
├── README.md                        # este arquivo
├── references/
│   ├── 01-estilo-de-escrita.md      # voz, vícios (com frequências), frases-fórmula, cortes
│   ├── 02-referencias-por-teste.md  # teste -> citação (legível por humano)
│   ├── 02-referencias-por-teste.json# teste -> citação (lookup programático)
│   ├── 03-referencias-apa7.md       # entradas APA 7 completas (núcleo do acervo)
│   ├── 04-pacotes-r.md              # pacotes/funções R por análise + preâmbulo
│   ├── 05-graficos.md               # gráficos do autor + 10 propostas novas (código)
│   ├── 06-formatacao-apa7.md        # TNR 12/tabelas 10, entrelinha 1,5, tabela Estilo2 APA
│   └── 07-templates-trechos.md      # blocos verbatim "Análise de dados" + fórmulas
└── assets/
    ├── setup_workspace.py           # monta o workspace local em Downloads e copia base+scripts
    ├── sync_to_drive.py             # leva o resultado final para o Drive (1 cópia, no fim)
    ├── build_report.py              # gera o .docx final formatado (a partir de JSON) no relatório-modelo
    ├── template_multinivel.py       # cabeçalho + rodapé (nº de página) + marca d'água do relatório-modelo
    ├── marca_dagua.py               # módulo da marca d'água (sozinho: carimba .docx ou .pdf)
    ├── cabecalho-multinivel.png     # faixa do cabeçalho (logo oficial positiva + eyebrow)
    ├── rodape-multinivel.png        # faixa do rodapé (logo oficial negativa + contatos + malha)
    ├── marca-dagua-multinivel.png   # marca d'água (g-600 a 14%, nós vazados com sombra)
    ├── logo-multinivel-horizontal.png # logo avulsa (opcional, desligada por padrão)
    ├── analise_template.R           # esqueleto de análise (descritiva→testes→AFE/AFC/TRI/redes)
    └── explore_data.py              # perfila a base e sugere o delineamento
```

## Fluxo local-first
Para fugir da lentidão/instabilidade do Google Drive, todo o trabalho roda em disco local
e só o resultado final é sincronizado para o Drive:
```
~/Downloads/Relatórios Automatizados/   <- pasta geral (todos os relatórios)
    <Nome do Projeto>/                  <- uma pasta por projeto/banco (base + scripts + saídas + .docx)
```
1. `setup_workspace.py "<Projeto>" "<base>"` → cria a pasta e copia base + scripts para lá.
2. Rodam-se as análises (R) e gera-se o `.docx` **dentro dessa pasta**.
3. `sync_to_drive.py "<pasta local>" "<destino no Drive>"` → leva só o resultado final ao Drive.

## Saída
- `.docx` final formatado (APA 7, TNR 12, tabelas 10pt estilo APA, entrelinha 1,5, 12pt entre parágrafos), no relatório-modelo aprovado em 23/10/2026: faixa de cabeçalho com a logo, faixa de rodapé com contatos e número da página, e marca d'água em todas as páginas.
- Markdown/`.R` fonte com o código das análises (preferência: entregar ambos).

## Base do conhecimento
Tudo foi destilado de **328 relatórios reais** (2020–2026) das pastas Multinível e NAOPARE.
Uma cópia desta base também fica na pasta de trabalho (`_Skill Multinível/`) para consulta/edição.

## Manutenção
- Para ajustar o estilo: edite os arquivos em `references/`.
- Para mudar a formatação do `.docx`: edite os `DEFAULTS` no topo de `assets/build_report.py` (inclusive `faixas`, `marca_dagua`, `logo`).
- Para trocar as faixas ou a marca d'água: os PNG e os geradores (`gerar_faixas.py`, `gerar_marca_dagua.py`) ficam em `2. Multinível/1. Consultorias/2026/00 - Marca d'água Multinível/`; gere de novo, substitua os PNGs em `assets/` e suba a `VERSAO` do `build_report.py`.
- Novas referências: acrescente em `03-referencias-apa7.md` e mapeie em `02-referencias-por-teste.*`.
