# CONTEXTO — <NOME DO ARTIGO OU PROJETO>
> Handoff para retomar depois de limpar a janela de contexto. Atualizado em <data> (<o que mudou por último>).
> Ao retomar: LER este arquivo + acionar a skill **`/roteiro-artigo`** (e `/relatorio-multinivel` se o estilo for da Multinível).

---

## 0. Onde estão as coisas

- **Trabalho (local):** `<caminho da pasta local>`
- **Entrega:** `<caminho na nuvem>`
- **Entregáveis:** `<arquivo>.docx` + `.html` (**N tabelas, M figuras**). Fontes: `conteudo.json` (HTML, SVG) e `conteudo_docx.json` (Word, PNG).
- **Base:** `<arquivo>.rds` (linhas x colunas), derivado de `<origem>`.

## 1. O artigo

- **Título:** <título>
- **N =** <n>; n analítico varia por análise (<faixa>).
- **Exigências do projeto:** <ineditismo, embargos, prazos, revista-alvo>

## 2. Pipeline (rodar nesta ordem, cwd = pasta local, `LC_ALL=en_US.UTF-8`)

```
1. 00_prep.R        -> dados.rds       (<o que faz>)
2. 01_<nome>.R      -> <nome>.rds      (<o que faz>)
...
N. NN_relatorio.R   -> conteudo.json + conteudo_docx.json
build:
   python3 -c "import os,sys,runpy; os.chdir('<PASTA>'); \
     sys.argv=['json2html.py','conteudo.json','<saida>.html']; runpy.run_path('json2html.py',run_name='__main__'); \
     sys.argv=['build_report.py','conteudo_docx.json','<saida>.docx']; runpy.run_path('build_report.py',run_name='__main__')"
sync: cp dos entregáveis + scripts + *.rds + saida_figuras/ para a pasta de entrega.
```

## 3. Estrutura atual do relatório

**Método:** <subseções>
**Resultados:** <lista numerada das análises, com as tabelas e figuras de cada uma>
**<demais seções>**

## 4. Hipóteses

| | Hipótese | Testada por | Resultado |
|---|---|---|---|
| H1 | | | |

## 5. Resultados-chave (números reais)

- **<análise>:** <números>
- **<modelo final>:** <índices de ajuste, npar, n, razão casos por parâmetro>
  - <blocos de coeficientes>
  - <efeitos indiretos>
  - <sensibilidades>
  - <o que foi testado e rejeitado, com o motivo>

## 6. Decisões do autor (CUMPRIR)

Numeradas, com data e motivo. Quando revogadas, marcar como revogada em vez de apagar — o histórico evita reabrir discussões encerradas.

1. **<decisão>** — <motivo>, <data>.
2. ~~<decisão revogada>~~ — **revogada em <data>**: <novo entendimento>.

## 7. Gotchas (custaram tempo, não repetir)

### 7.1 <título>
<descrição do problema, do sintoma e da solução>

## 8. Justificativas de especificação

Análises que embasaram uma escolha e saíram do relatório, mas que sustentam a defesa se um revisor perguntar.

## 9. Pendências / próximos passos

- [ ] <item>
