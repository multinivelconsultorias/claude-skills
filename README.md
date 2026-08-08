# Skills

Skills do Claude Code para produção de artigos científicos e relatórios de análise de dados.

Uma skill é um conjunto de instruções que o Claude carrega quando a tarefa corresponde ao que ela cobre. Cada pasta aqui é uma skill: o `SKILL.md` traz as instruções principais, `references/` traz o aprofundamento carregado sob demanda, `assets/` os modelos e conversores, e `scripts/` os utilitários executáveis.

## As três skills

### `analises-artigo`
Análises de dados auditáveis, em R ou Python, sobre bases locais ou públicas (ENEM, SAEB, PNAD, DATASUS, PISA). Monta o pipeline em scripts numerados que outra pessoa consegue reexecutar, com **travas** que fazem a geração do relatório falhar quando a prosa deixa de corresponder aos números. Produz o relatório em `.docx` e `.html` a partir de um JSON de conteúdo.

A ideia central: o texto é uma função dos objetos do modelo. Trocar uma decisão analítica passa a ser editar uma linha e rodar de novo, em vez de varrer o documento atrás de números desatualizados.

### `roteiro-artigo`
Roteiro das seções teóricas e varredura de referências, para Introdução **e** Discussão — que exigem estratégias de busca diferentes. Privilegia literatura dos últimos cinco anos (cerca de 70% do conjunto) e acesso aberto. Serve tanto a artigos quantitativos, partindo dos resultados, quanto a qualitativos, partindo das perguntas de pesquisa.

Entrega um mapa parágrafo a parágrafo: a função de cada um no argumento e a referência que o sustenta.

### `relatorio-multinivel`
Estilo de escrita e formatação dos relatórios da Multinível/NAOPARE: voz, citações por teste estatístico, convenções de tabelas e figuras, formatação APA 7. É a camada de estilo; as outras duas cuidam da arquitetura.

## Instalação

Clone dentro do diretório de skills do Claude Code:

```bash
git clone <url-deste-repo> ~/.claude/skills
```

Se já houver um `~/.claude/skills`, clone em outro lugar e copie as pastas que quiser. As skills passam a estar disponíveis na próxima sessão, e são acionadas pelo nome (`/analises-artigo`) ou automaticamente, quando a tarefa corresponde à descrição.

## Dependências

Os scripts em Python precisam de `python-docx` (geração de `.docx`), `pypdf` (extração de corpus) e `pandas` com `pyarrow` (perfil de bases). O `busca_openalex.py` usa só a biblioteca padrão, mas exige os certificados raiz instalados — no macOS, rode uma vez:

```
"/Applications/Python 3.x/Install Certificates.command"
```

Os templates em R usam `pacman` para carregar o que cada análise pedir.

## Como isso costuma ser usado em sequência

1. `analises-artigo` monta o pipeline e gera o relatório de análise de dados
2. `roteiro-artigo` monta a Introdução a partir dos resultados e busca as referências
3. `relatorio-multinivel` entra quando o entregável segue o padrão de escrita da consultoria
