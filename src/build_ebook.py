from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, Image, KeepTogether, PageBreak, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "fundamentos-data-engineer-associate.pdf"
COVER = ROOT / "assets" / "cover-generated.png"

NAVY = colors.HexColor("#071827")
INK = colors.HexColor("#132231")
MUTED = colors.HexColor("#506271")
CORAL = colors.HexColor("#FF6B5F")
CYAN = colors.HexColor("#42D7E8")
PALE = colors.HexColor("#EDF7F8")
WHITE = colors.white

FONT_CANDIDATES = [
    (
        Path("/usr/share/fonts/google-noto-vf/NotoSans[wght].ttf"),
        Path("/usr/share/fonts/google-noto-vf/NotoSans[wght].ttf"),
        Path("/usr/share/fonts/google-noto-vf/NotoSansMono[wght].ttf"),
    ),
    (
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
    ),
]

FONT_REGULAR, FONT_BOLD, FONT_MONO = "Helvetica", "Helvetica-Bold", "Courier"
for regular_path, bold_path, mono_path in FONT_CANDIDATES:
    if all(path.exists() for path in (regular_path, bold_path, mono_path)):
        pdfmetrics.registerFont(TTFont("ProjectSans", str(regular_path)))
        pdfmetrics.registerFont(TTFont("ProjectSans-Bold", str(bold_path)))
        pdfmetrics.registerFont(TTFont("ProjectMono", str(mono_path)))
        FONT_REGULAR, FONT_BOLD, FONT_MONO = "ProjectSans", "ProjectSans-Bold", "ProjectMono"
        break

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleX", fontName=FONT_BOLD, fontSize=31, leading=35, textColor=WHITE, spaceAfter=10))
styles.add(ParagraphStyle(name="SubX", fontName=FONT_REGULAR, fontSize=14, leading=19, textColor=colors.HexColor("#D7E9EE")))
styles.add(ParagraphStyle(name="H1X", fontName=FONT_BOLD, fontSize=23, leading=28, textColor=NAVY, spaceAfter=13))
styles.add(ParagraphStyle(name="H2X", fontName=FONT_BOLD, fontSize=14, leading=18, textColor=CORAL, spaceBefore=10, spaceAfter=6))
styles.add(ParagraphStyle(name="BodyX", fontName=FONT_REGULAR, fontSize=10.2, leading=15, textColor=INK, spaceAfter=8))
styles.add(ParagraphStyle(name="SmallX", fontName=FONT_REGULAR, fontSize=8.2, leading=11, textColor=MUTED, spaceAfter=4))
styles.add(ParagraphStyle(name="CodeX", fontName=FONT_MONO, fontSize=7.8, leading=11, textColor=colors.HexColor("#DCEFF4"), backColor=NAVY, borderPadding=8, spaceBefore=5, spaceAfter=9))
styles.add(ParagraphStyle(name="QuoteX", fontName=FONT_REGULAR, fontSize=10.2, leading=15, leftIndent=11, borderColor=CYAN, borderWidth=2, borderPadding=8, textColor=INK, backColor=PALE, spaceAfter=9))
styles.add(ParagraphStyle(name="CenterX", fontName=FONT_REGULAR, fontSize=10, leading=15, alignment=TA_CENTER, textColor=INK))
styles.add(ParagraphStyle(name="TableCellX", fontName=FONT_REGULAR, fontSize=9, leading=11, textColor=INK))
styles.add(ParagraphStyle(name="TableHeadX", fontName=FONT_BOLD, fontSize=9, leading=11, textColor=WHITE))


def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page == 1:
        canvas.drawImage(str(COVER), 0, 0, width=A4[0], height=A4[1], mask="auto")
        canvas.setFillColor(colors.Color(0.02, 0.07, 0.12, alpha=0.82))
        canvas.roundRect(15 * mm, 48 * mm, A4[0] - 30 * mm, 86 * mm, 5 * mm, fill=1, stroke=0)
        canvas.setFillColor(CYAN)
        canvas.setFont(FONT_BOLD, 10)
        canvas.drawString(25 * mm, 120 * mm, "GUIA INTRODUTÓRIO - EDIÇÃO 2026")
        cover_title = Paragraph("Fundamentos para a Certificação<br/>Data Engineer Associate", styles["TitleX"])
        cover_title.wrapOn(canvas, A4[0] - 50 * mm, 48 * mm)
        cover_title.drawOn(canvas, 25 * mm, 69 * mm)
        canvas.setFillColor(WHITE)
        canvas.setFont(FONT_REGULAR, 9)
        canvas.drawString(25 * mm, 58 * mm, "Databricks - roteiro de estudo para iniciantes")
        canvas.restoreState()
        return
    canvas.setFillColor(NAVY)
    canvas.rect(0, A4[1] - 13 * mm, A4[0], 13 * mm, fill=1, stroke=0)
    canvas.setFont(FONT_BOLD, 8)
    canvas.setFillColor(WHITE)
    canvas.drawString(18 * mm, A4[1] - 8.5 * mm, "FUNDAMENTOS PARA A CERTIFICAÇÃO DATA ENGINEER ASSOCIATE")
    canvas.setFont(FONT_REGULAR, 8)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"{doc.page}")
    canvas.setStrokeColor(CYAN)
    canvas.setLineWidth(0.7)
    canvas.line(18 * mm, 14 * mm, A4[0] - 18 * mm, 14 * mm)
    canvas.restoreState()


def title(text, kicker=None):
    out = []
    if kicker:
        out.append(Paragraph(kicker.upper(), styles["SmallX"]))
    out.append(Paragraph(text, styles["H1X"]))
    return out


def p(text, style="BodyX"):
    return Paragraph(text, styles[style])


def bullets(items):
    return [Paragraph(f"• {item}", styles["BodyX"]) for item in items]


def source(text):
    return Paragraph(f"Fonte: {text}", styles["SmallX"])


def page(story, heading, body, kicker=None):
    story.extend(title(heading, kicker))
    story.extend(body)
    story.append(PageBreak())


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
    topMargin=21 * mm, bottomMargin=18 * mm,
    title="Fundamentos para a Certificação Data Engineer Associate",
    author="Marconiadsf", subject="Guia introdutório de estudos para Databricks Data Engineer Associate",
)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
doc.addPageTemplates([PageTemplate(id="content", frames=[frame], onPage=header_footer)])
story = []

# Capa
story.append(Spacer(1, 1))
story.append(PageBreak())

page(story, "Antes de começar", [
    p("Este guia organiza os fundamentos cobrados na certificação <b>Databricks Certified Data Engineer Associate</b>. Ele foi escrito para quem está iniciando e precisa transformar o guia oficial em uma rota de estudo."),
    p("O material <b>não substitui prática na plataforma</b>, treinamento oficial nem o guia vigente do exame. Produtos, nomes e objetivos podem mudar; confira novamente a página oficial antes de agendar a prova.", "QuoteX"),
    p("Este material apresenta uma seleção introdutória de fundamentos e não cobre individualmente todos os objetivos do exame.", "QuoteX"),
    p("Ao final, você deverá reconhecer os principais componentes da plataforma, entender o percurso de um dado em uma arquitetura lakehouse e saber quais atividades praticar em cada domínio."),
    source("Databricks Certified Data Engineer Associate Exam Guide, versão válida a partir de 4 maio 2026."),
], "ORIENTAÇÃO")

page(story, "Como este e-book organiza os estudos", [
    p("O guia oficial vigente informa <b>45 questões pontuadas</b>, <b>90 minutos</b>, formato de múltipla escolha e ausência de pré-requisito obrigatório. A Databricks recomenda experiência prática antes da tentativa."),
    p("A tabela abaixo é uma organização didática deste e-book. Ela não reproduz individualmente as seções ou todos os objetivos do guia oficial."),
    Table([
        ["Domínio de estudo", "O que revisar"],
        ["Plataforma", "workspace, arquitetura e capacidades"],
        ["Ingestão e carga", "fontes, formatos, batch e streaming"],
        ["Transformação e modelagem", "SQL, PySpark, Delta e arquitetura medalhão"],
        ["Produção", "Lakeflow Jobs, pipelines e CI/CD"],
        ["Operação", "monitoramento, solução de problemas e otimização"],
        ["Governança e segurança", "Unity Catalog, permissões e qualidade"],
    ], colWidths=[48 * mm, 113 * mm], style=TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTNAME", (0, 1), (-1, -1), FONT_REGULAR),
        ("FONTSIZE", (0, 0), (-1, -1), 9), ("LEADING", (0, 0), (-1, -1), 12),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#C8D8DD")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ])),
    Spacer(1, 8), source("Guia oficial do exame, maio de 2026."),
], "MAPA DE ESTUDO")

page(story, "A plataforma em uma visão única", [
    p("A Databricks Data Intelligence Platform reúne engenharia de dados, análise, machine learning e inteligência artificial sobre uma base lakehouse. Para a prova, pense menos em uma lista de produtos e mais no fluxo completo do dado."),
    p("<b>Fontes → ingestão → armazenamento → transformação → consumo → governança</b>", "QuoteX"),
    *bullets([
        "O workspace organiza notebooks, consultas, jobs e outros ativos de trabalho.",
        "A computação executa consultas e transformações sem precisar estar acoplada ao armazenamento.",
        "Delta Lake fornece tabelas confiáveis sobre armazenamento de objetos.",
        "Unity Catalog centraliza descoberta, permissões, linhagem e governança de dados e IA.",
    ]),
    source("Databricks documentation: What is Databricks?; What is a data lakehouse?"),
], "1 · PLATAFORMA")

page(story, "Lakehouse combina flexibilidade e controle", [
    p("Um <b>data lake</b> aceita grande variedade de dados e escala com baixo acoplamento. Um <b>data warehouse</b> favorece dados estruturados, governança e consumo analítico. O lakehouse busca reunir essas propriedades em uma única arquitetura."),
    p("No Databricks, o Apache Spark oferece processamento distribuído, enquanto Delta Lake adiciona uma camada de armazenamento otimizada com transações ACID e controle de esquema."),
    p("Para estudar, diferencie responsabilidades: Spark processa; Delta Lake estrutura e protege tabelas; Unity Catalog governa ativos.", "QuoteX"),
    source("Databricks documentation: What is a data lakehouse?; What is Delta Lake?"),
], "2 · LAKEHOUSE")

page(story, "Bronze, prata e ouro indicam qualidade", [
    p("A arquitetura medalhão organiza o dado em camadas que aumentam progressivamente sua qualidade e utilidade."),
    Table([
        [Paragraph(value, styles["TableHeadX"]) for value in ["Camada", "Estado", "Uso típico"]],
        [Paragraph(value, styles["TableCellX"]) for value in ["Bronze", "bruto e rastreável", "preservar a chegada e permitir reprocessamento"]],
        [Paragraph(value, styles["TableCellX"]) for value in ["Prata", "limpo e validado", "padronizar tipos, remover duplicidades e integrar fontes"]],
        [Paragraph(value, styles["TableCellX"]) for value in ["Ouro", "agregado e orientado ao negócio", "alimentar indicadores, relatórios e produtos de dados"]],
    ], colWidths=[29 * mm, 50 * mm, 82 * mm], style=TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTNAME", (0, 1), (-1, -1), FONT_REGULAR),
        ("FONTSIZE", (0, 0), (-1, -1), 9), ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#C8D8DD")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ])),
    Spacer(1, 8), p("A camada não é definida pelo nome do arquivo, e sim pelo nível de refinamento e pelo contrato que oferece aos consumidores."),
    source("Databricks documentation: What is the medallion lakehouse architecture?"),
], "3 · MODELAGEM")

page(story, "Ingestão começa pela natureza da fonte", [
    p("Antes de escolher uma ferramenta, responda: os dados chegam em lote ou continuamente? O esquema é estável? É necessário reprocessar? Qual latência o consumidor exige?"),
    *bullets([
        "Batch: cargas periódicas e conjuntos delimitados.",
        "Streaming: eventos contínuos tratados de forma incremental.",
        "Auto Loader: ingestão incremental de novos arquivos em armazenamento de nuvem.",
        "COPY INTO: carga idempotente de arquivos para tabelas Delta em cenários adequados.",
    ]),
    p("Na prática, carregue um CSV pequeno, observe o esquema inferido e depois declare explicitamente os tipos esperados. Compare o resultado quando chega uma coluna inesperada."),
    source("Databricks documentation: ETL quick start; Auto Loader; COPY INTO."),
], "4 · INGESTÃO")

page(story, "Transformações devem ser legíveis e testáveis", [
    p("A prova exige reconhecer transformações com SQL e PySpark. Concentre-se em seleção, filtros, junções, agregações, tratamento de nulos e criação de colunas."),
    p("<font color='#7FEAF3'>from</font> pyspark.sql <font color='#7FEAF3'>import</font> functions <font color='#7FEAF3'>as</font> F<br/><br/>resultado = (vendas<br/>    .filter(F.col('valor') &gt; 0)<br/>    .groupBy('produto')<br/>    .agg(F.sum('valor').alias('receita')))", "CodeX"),
    p("Entenda o resultado de cada etapa antes de memorizar métodos. Em SQL, pratique a mesma lógica com <b>WHERE</b>, <b>GROUP BY</b>, funções de agregação e junções."),
    p("Prefira funções nativas de Spark a UDFs quando houver equivalente: o otimizador consegue compreender e melhorar o plano de execução.", "QuoteX"),
    source("Databricks documentation: PySpark transformations; Spark SQL."),
], "5 · TRANSFORMAÇÃO")

page(story, "Delta Lake torna pipelines confiáveis", [
    p("Tabelas Delta mantêm um log de transações associado aos arquivos de dados. Isso possibilita garantias ACID, evolução e validação de esquema e operações de atualização."),
    *bullets([
        "MERGE combina inserções e atualizações de maneira declarativa.",
        "Time travel permite consultar versões anteriores dentro da retenção disponível.",
        "Schema enforcement bloqueia gravações incompatíveis.",
        "OPTIMIZE reorganiza arquivos para melhorar determinados padrões de leitura.",
    ]),
    p("Não confunda confiabilidade lógica com desempenho automático: formato, tamanho de arquivos, filtros e padrão de consulta continuam relevantes."),
    source("Databricks documentation: What is Delta Lake?; Delta table optimization."),
], "6 · DELTA LAKE")

page(story, "Notebooks são ambiente de desenvolvimento", [
    p("Notebooks do Databricks combinam código, texto e resultados. Eles suportam Python, SQL, Scala e R, colaboração e visualizações. Para estudos iniciais, Python e SQL cobrem a maior parte das atividades de engenharia de dados."),
    *bullets([
        "Anexe o notebook a uma computação compatível antes de executar células.",
        "Use comandos mágicos, como %sql e %python, para alternar linguagens quando necessário.",
        "Separe lógica reutilizável em arquivos ou módulos em vez de concentrar tudo em um notebook.",
        "Versione código e mantenha parâmetros fora da lógica principal.",
    ]),
    source("Databricks documentation: Develop code in Databricks notebooks; Choose a development language."),
], "7 · DESENVOLVIMENTO")

page(story, "Produção exige orquestração e observabilidade", [
    p("Um notebook executado manualmente ainda não é um pipeline de produção. Lakeflow Jobs organiza tarefas, dependências, agendas, parâmetros e tentativas de execução."),
    *bullets([
        "Defina tarefas pequenas, com entradas e saídas claras.",
        "Configure dependências para impedir consumo antes da conclusão da etapa anterior.",
        "Use parâmetros para evitar cópias quase idênticas do mesmo código.",
        "Acompanhe falhas, duração, custo e qualidade das saídas.",
        "Trate CI/CD como promoção controlada de código e configuração entre ambientes.",
    ]),
    p("Para cada falha, descubra primeiro se a causa está no código, nos dados, na configuração ou nos recursos de computação.", "QuoteX"),
    source("Databricks exam guide 2026; Databricks documentation: Lakeflow Jobs."),
], "8 · PRODUÇÃO")

page(story, "Governança começa pelo menor privilégio", [
    p("Unity Catalog organiza ativos em uma hierarquia de metastore, catálogo, esquema e objeto. Permissões devem conceder somente o acesso necessário para cada identidade e tarefa."),
    *bullets([
        "Tabelas gerenciadas têm ciclo de vida de dados e metadados controlado pela plataforma.",
        "Tabelas externas mantêm dados em uma localização externa definida.",
        "GRANT concede privilégios; REVOKE remove privilégios.",
        "Linhagem ajuda a compreender origens, transformações e consumidores.",
        "Credenciais e segredos não devem ser gravados diretamente em notebooks.",
    ]),
    p("Governança não é apenas bloquear: ela permite que pessoas encontrem e usem dados confiáveis dentro de regras claras."),
    source("Databricks documentation: Unity Catalog; Manage privileges."),
], "9 · GOVERNANÇA")

page(story, "Otimização começa pela evidência", [
    p("Evite decorar uma única solução para qualquer lentidão. Observe métricas, plano de execução, volume de dados, distribuição entre partições e padrão de leitura."),
    *bullets([
        "Muitos arquivos pequenos aumentam o custo de listagem e planejamento.",
        "Filtros seletivos reduzem a quantidade de dados lida.",
        "Junções podem exigir redistribuição de dados entre executores.",
        "Skew concentra trabalho em poucas partições e prolonga a etapa mais lenta.",
        "Logs e histórico de execução ajudam a separar sintomas de causas.",
    ]),
    p("Regra de estudo: identifique o gargalo antes de escolher a otimização.", "QuoteX"),
    source("Databricks documentation: Optimization recommendations; Spark UI."),
], "10 · OPERAÇÃO")

page(story, "Plano de estudo em quatro ciclos", [
    Table([
        ["Ciclo", "Foco", "Entrega prática"],
        ["1", "plataforma, lakehouse e Delta", "criar workspace de estudo e uma tabela Delta"],
        ["2", "ingestão, SQL e PySpark", "carregar CSV, limpar dados e comparar SQL/PySpark"],
        ["3", "medalhão, jobs e governança", "pipeline bronze-prata-ouro com permissões"],
        ["4", "operação e revisão", "investigar uma falha, revisar objetivos e responder simulados"],
    ], colWidths=[18 * mm, 58 * mm, 85 * mm], style=TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTNAME", (0, 1), (-1, -1), FONT_REGULAR),
        ("FONTSIZE", (0, 0), (-1, -1), 9), ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#C8D8DD")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ])),
    Spacer(1, 10), p("Não avance apenas porque leu o tópico. Cada ciclo termina com algo executado, observado e explicado com suas próprias palavras."),
], "11 · ROTA PRÁTICA")

questions = [
    "1. Qual componente adiciona transações ACID às tabelas do lakehouse?",
    "2. Em qual camada ficam os dados mais próximos da origem?",
    "3. Qual é a diferença essencial entre batch e streaming?",
    "4. Para que serve uma operação MERGE?",
    "5. Por que funções nativas de Spark tendem a ser preferíveis a UDFs?",
    "6. Qual serviço organiza tarefas e dependências de produção?",
    "7. Qual componente centraliza governança de dados e IA?",
    "8. O que schema enforcement evita?",
    "9. Por que muitos arquivos pequenos podem prejudicar uma carga?",
    "10. Qual deve ser o primeiro passo diante de uma consulta lenta?",
]
page(story, "Teste sua compreensão", [*bullets(questions), p("Responda sem consultar as páginas anteriores. Depois explique por que as alternativas erradas estariam erradas; esse exercício prepara melhor para questões de cenário.", "QuoteX")], "12 · REVISÃO")

page(story, "Gabarito comentado", [
    *bullets([
        "1. Delta Lake.", "2. Bronze.", "3. Batch processa conjuntos delimitados; streaming trata eventos continuamente ou de forma incremental.",
        "4. Combinar inserções, atualizações e, conforme a lógica, exclusões entre fonte e destino.",
        "5. O otimizador compreende funções nativas e pode planejar sua execução.", "6. Lakeflow Jobs.",
        "7. Unity Catalog.", "8. A gravação de dados incompatíveis com o esquema esperado.",
        "9. Eles aumentam custos de listagem, abertura e planejamento.", "10. Observar métricas e o plano para localizar o gargalo.",
    ]),
    p("Use o gabarito para localizar lacunas, não para decorar frases."),
], "13 · REVISÃO")

page(story, "Checklist antes da prova", [
    *bullets([
        "Rebaixei o guia oficial e confirmei que esta é a versão vigente para minha data.",
        "Consigo explicar lakehouse, Delta Lake e Unity Catalog sem consultar anotações.",
        "Pratiquei transformações equivalentes em SQL e PySpark.",
        "Construí ao menos um fluxo bronze-prata-ouro.",
        "Criei e acompanhei um job com mais de uma tarefa.",
        "Revisei permissões, tabelas gerenciadas e externas e linhagem.",
        "Consigo investigar uma falha usando logs e métricas.",
        "Treinei questões de cenário dentro do tempo disponível.",
    ]),
    p("A certificação mede reconhecimento e aplicação de fundamentos. A prática reduz a dependência de memorização isolada."),
], "14 · FECHAMENTO")

story.extend(title("Referências essenciais", "FONTES"))
for label, url in [
    ("Guia oficial do exame - maio de 2026", "https://www.databricks.com/sites/default/files/2026-03/databricks-certified-data-engineer-associate-exam-guide-may-4-2026.pdf"),
    ("O que é um data lakehouse?", "https://docs.databricks.com/aws/en/lakehouse/"),
    ("Arquitetura medalhão", "https://docs.databricks.com/aws/en/lakehouse/medallion"),
    ("Delta Lake", "https://docs.databricks.com/aws/en/delta"),
    ("Notebooks do Databricks", "https://docs.databricks.com/aws/en/notebooks/notebooks-code"),
    ("Unity Catalog", "https://docs.databricks.com/aws/en/data-governance/unity-catalog/"),
    ("Lakeflow Jobs", "https://docs.databricks.com/aws/en/jobs/"),
]:
    story.append(p(f"<b>{label}</b><br/><link href='{url}' color='#087D8C'>{url}</link>"))
story.append(Spacer(1, 12))
story.append(p("Conteúdo produzido com apoio do Codex e revisado a partir de documentação oficial. A capa foi criada pelo gerador de imagens integrado ao Codex. Estrutura inicial inspirada no projeto educacional de Felipe Aguiar disponibilizado pela DIO.", "QuoteX"))

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
doc.build(story)
print(OUTPUT)
