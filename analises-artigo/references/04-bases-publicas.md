# Bases públicas: baixar, verificar e documentar

Análise sobre microdado público só é auditável se outra pessoa conseguir chegar ao mesmo arquivo. Isso exige registrar de onde veio, quando, e o que foi feito com ele antes da primeira análise — porque as bases mudam: o INEP republica edições com correções, o IBGE revisa pesos, o DATASUS atualiza registros retroativamente.

## Regra de ouro

**Baixe uma vez, congele, e nunca reprocesse do original.** O `00_prep` lê o arquivo bruto, filtra, tipa e salva o artefato. Todo o resto lê o artefato. Se o órgão republicar a base amanhã, seus resultados continuam explicáveis.

## O arquivo de proveniência

Crie um `PROVENIENCIA.md` na pasta do projeto e registre cada base:

```markdown
## ENEM 2023 — Microdados
- Órgão: INEP
- Página: https://www.gov.br/inep/.../microdados/enem
- Arquivo: microdados_enem_2023.zip
- Baixado em: 2026-08-08
- Tamanho: 2,1 GB | SHA-256: a3f5...
- Dicionário: Dicionário_Microdados_Enem_2023.xlsx (incluído no zip)
- Recorte aplicado no 00_prep: participantes de Alagoas, presentes nos dois dias
- Linhas: 3.933.955 brutas -> 41.207 após recorte
```

O par "linhas brutas → linhas após recorte" é o que mais evita retrabalho: seis meses depois, é a primeira coisa que você não vai lembrar.

Use `scripts/baixa_base_publica.py`, que baixa, calcula o hash, descompacta e escreve esse bloco automaticamente.

## Onde ficam as principais bases brasileiras

| Base | Órgão | O que tem | Formato típico |
|---|---|---|---|
| ENEM | INEP | microdados por participante, notas por área, questionário socioeconômico | CSV `;` latin-1, ~2 GB por edição |
| SAEB / Prova Brasil | INEP | desempenho de estudantes, questionários de aluno, professor, diretor e escola | CSV por instrumento |
| Censo Escolar | INEP | escolas, turmas, docentes, matrículas | CSV grandes, um por entidade |
| Censo da Educação Superior | INEP | cursos, docentes, alunos | CSV |
| PNAD Contínua | IBGE | trabalho, renda, domicílio, trimestral | arquivo de largura fixa + dicionário |
| Censo Demográfico | IBGE | domicílios e pessoas | largura fixa, muito grande |
| SIM, SINAN, SIH, SINASC | DATASUS | mortalidade, agravos de notificação, internações, nascidos vivos | DBC/DBF, ou via `PySUS` |
| PeNSE, VIGITEL | Ministério da Saúde | saúde do escolar, vigilância por telefone | CSV/SPSS |
| PISA | OCDE | desempenho e questionários, comparação internacional | SPSS/SAS |

Duas armadilhas recorrentes nas bases do INEP: **encoding latin-1** (ler como UTF-8 corrompe acentos silenciosamente) e **separador ponto e vírgula**. Nas do IBGE, o arquivo é de **largura fixa** e não faz sentido sem o dicionário que define as posições — leia o dicionário antes de tentar abrir o dado.

## Códigos de não-resposta

Este é o erro mais caro em microdado público, porque não gera erro nenhum: valores como `9`, `99`, `999`, `-1`, `88` costumam significar "não sabe", "não respondeu" ou "não se aplica", e entram nas médias como se fossem observações reais.

**Leia o dicionário antes de calcular qualquer estatística.** Depois, converta explicitamente e registre quantos casos foram afetados:

```python
NAO_RESPOSTA = {"Q006": [], "TP_ESCOLA": [1], "NU_IDADE": [999]}
for col, codigos in NAO_RESPOSTA.items():
    if codigos:
        n = df[col].isin(codigos).sum()
        df.loc[df[col].isin(codigos), col] = pd.NA
        print(f"{col}: {n} casos convertidos em ausente {codigos}")
```

`scripts/perfila_base.py` sinaliza candidatos automaticamente: colunas numéricas com picos isolados em valores extremos redondos.

## Pesos amostrais

PNAD, PISA, PeNSE e VIGITEL são amostras complexas. Média simples sobre elas dá número errado, e não um pouco errado. Use o desenho:

```python
# statsmodels aceita pesos em vários estimadores
mod = smf.wls("y ~ x1 + x2", data=df, weights=df["peso"]).fit()
```

Para variância correta com estratos e conglomerados, o caminho maduro é o pacote `survey` em R. Quando o artigo depender de erro padrão ou intervalo de confiança sobre amostra complexa, prepare em Python e modele em R.

O PISA tem, além disso, **valores plausíveis**: o desempenho vem em cinco ou dez colunas e a análise correta roda em todas e combina os resultados. Rodar só na primeira subestima o erro padrão.

## Verificações antes de analisar

Rode `scripts/perfila_base.py` e confira, no mínimo:

1. **Número de linhas bate com o que o órgão documenta** para aquela edição.
2. **Acentos íntegros** numa coluna de texto — se aparecer `Ã`, o encoding está errado.
3. **Faixas plausíveis** nas numéricas: idade entre 0 e 120, nota entre 0 e 1000.
4. **Cardinalidade das categóricas** contra o dicionário: uma variável de sexo com sete níveis indica leitura desalinhada.
5. **Ausentes por coluna**, com atenção às que serão preditoras.

## Ética e uso

Microdados públicos são anonimizados, mas cruzar várias fontes pode reidentificar pessoas em municípios pequenos. Não junte bases com o objetivo de individualizar, e reporte resultados agregados quando a célula tiver poucos casos. Cite a fonte no artigo com órgão, base, edição e data de acesso — é exigência da maioria dos periódicos e é o que torna o resultado verificável.
