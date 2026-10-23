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
    ├── build_report.py              # gera o .docx final formatado (a partir de JSON); logo no topo + marca d'água
    ├── marca_dagua.py               # aplica a marca d'água (símbolo rede-M) em .docx e .pdf
    ├── marca-dagua-multinivel.png   # marca d'água (versão atual da marca, g-600 a 16%/10%)
    ├── logo-multinivel-horizontal.png # logo horizontal para papel claro (topo da 1ª página)
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
- `.docx` final formatado (APA 7, TNR 12, tabelas 10pt estilo APA, entrelinha 1,5, 12pt entre parágrafos), com a logo da Multinível no topo da primeira página e a marca d'água em todas as páginas.
- Markdown/`.R` fonte com o código das análises (preferência: entregar ambos).

## Base do conhecimento
Tudo foi destilado de **328 relatórios reais** (2020–2026) das pastas Multinível e NAOPARE.
Uma cópia desta base também fica na pasta de trabalho (`_Skill Multinível/`) para consulta/edição.

## Manutenção
- Para ajustar o estilo: edite os arquivos em `references/`.
- Para mudar a formatação do `.docx`: edite os `DEFAULTS` no topo de `assets/build_report.py` (inclusive `logo`, `logo_largura_cm`, `marca_dagua`).
- Para trocar a logo ou a marca d'água: os PNG vêm de `2. Multinível/Logos multinível/Logos por tema (site)/` (pasta `claro/` e `_fonte/`).
- Novas referências: acrescente em `03-referencias-apa7.md` e mapeie em `02-referencias-por-teste.*`.
