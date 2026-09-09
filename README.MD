# Fundamentos para a Certificação Data Engineer Associate

E-book introdutório para organizar os estudos para a certificação **Databricks Certified Data Engineer Associate**. O conteúdo apresenta plataforma lakehouse, arquitetura medalhão, ingestão, transformações com SQL e PySpark, Delta Lake, notebooks, Lakeflow Jobs, Unity Catalog, otimização e uma rota prática de revisão.

> Este material apresenta uma seleção introdutória de fundamentos e não cobre individualmente todos os objetivos do exame.

## Entregável

- [E-book em PDF](output/fundamentos-data-engineer-associate.pdf)
- [Código-fonte do gerador](src/build_ebook.py)
- [Prompt de texto](src/prompts/texto.md)
- [Prompt da imagem](src/prompts/imagem.md)

## Ferramentas utilizadas

- **Codex**: planejamento, pesquisa, estruturação, redação e revisão.
- **Gerador de imagens do Codex**: ilustração original da capa.
- **Python e ReportLab**: diagramação e geração do PDF.
- **PyMuPDF**: ferramenta auxiliar de controle de qualidade, usada fora do gerador para renderizar o PDF em imagens e permitir a inspeção visual das páginas.

## Como gerar o PDF

Com Python instalado, execute:

```bash
python -m pip install -r requirements.txt
python src/build_ebook.py
```

O arquivo será criado em `output/fundamentos-data-engineer-associate.pdf`. O script procura Noto Sans ou DejaVu Sans em caminhos comuns e, se nenhuma delas estiver disponível, usa as fontes internas Helvetica e Courier do ReportLab.

## Processo de criação

1. Análise temporária das transcrições da formação para identificar requisitos de entrega e princípios de diagramação.
2. Consulta ao guia oficial vigente do exame e à documentação oficial do Databricks.
3. Elaboração e revisão humana do conteúdo, com foco em iniciantes.
4. Geração da capa e montagem programática do e-book.
5. Renderização e inspeção visual das 18 páginas antes da publicação.

Os PDFs da formação foram usados somente como material de consulta e **não fazem parte deste repositório**.

## Observação

Este é um material independente de estudo. Não é treinamento oficial, não garante aprovação e deve ser conferido com o [guia oficial do exame](https://www.databricks.com/sites/default/files/2026-03/databricks-certified-data-engineer-associate-exam-guide-may-4-2026.pdf) antes da prova.

## Projeto-base

Estrutura inicial baseada no projeto educacional [prompts-recipe-to-create-a-ebook](https://github.com/felipeAguiarCode/prompts-recipe-to-create-a-ebook), de Felipe Aguiar, disponibilizado como referência durante a formação da DIO. Conteúdo, capa, prompts e PDF foram personalizados para este projeto.

Projeto desenvolvido por **Marconiadsf** para o desafio de criação de e-book com IA generativa da DIO.
