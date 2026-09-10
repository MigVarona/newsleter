from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    Image,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path("/Users/miguelvarona/Proyectos/newsleter")
OUTPUT = ROOT / "output/pdf/CV-Miguel-Varona-Gallego-Product-Engineer-Optimizado.pdf"
PHOTO = ROOT / "tmp/pdfs/source-image-000.png"

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

FONT_DIR = Path("/System/Library/Fonts/Supplemental")
pdfmetrics.registerFont(TTFont("Arial", str(FONT_DIR / "Arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", str(FONT_DIR / "Arial Bold.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Italic", str(FONT_DIR / "Arial Italic.ttf")))

PAGE_W, PAGE_H = A4
MARGIN_X = 18 * mm
TOP_MARGIN = 15 * mm
BOTTOM_MARGIN = 16 * mm
CONTENT_W = PAGE_W - (2 * MARGIN_X)
LABEL_W = 30 * mm
GUTTER = 5 * mm
BODY_W = CONTENT_W - LABEL_W - GUTTER

INK = colors.HexColor("#20262C")
BLUE = colors.HexColor("#2F638B")
MUTED = colors.HexColor("#748392")
LIGHT = colors.HexColor("#D7E0E7")


def style(name, **kwargs):
    base = {
        "fontName": "Arial",
        "fontSize": 9.9,
        "leading": 13.2,
        "textColor": INK,
        "spaceAfter": 0,
        "spaceBefore": 0,
    }
    base.update(kwargs)
    return ParagraphStyle(name, **base)


STYLES = {
    "name": style("name", fontName="Arial-Bold", fontSize=25, leading=27, spaceAfter=3),
    "title": style("title", fontName="Arial-Bold", fontSize=14.6, leading=17, textColor=BLUE, spaceAfter=5),
    "tagline": style("tagline", fontSize=8.4, leading=10.5, textColor=MUTED, spaceAfter=9),
    "contact": style("contact", fontSize=8.9, leading=11.6, textColor=MUTED),
    "label": style("label", fontName="Arial-Bold", fontSize=8.5, leading=10, textColor=BLUE),
    "body": style("body"),
    "body_small": style("body_small", fontSize=9.35, leading=12.5),
    "role": style("role", fontName="Arial-Bold", fontSize=11.1, leading=13.4, textColor=BLUE, spaceAfter=2),
    "meta": style("meta", fontSize=8.9, leading=11.1, textColor=MUTED, spaceAfter=4),
    "desc": style("desc", fontName="Arial-Italic", fontSize=9.0, leading=11.9, textColor=MUTED, spaceAfter=4),
    "bullet": style("bullet", leftIndent=9, firstLineIndent=-7, bulletIndent=0, spaceAfter=3),
    "bullet_small": style("bullet_small", fontSize=9.35, leading=12.5, leftIndent=9, firstLineIndent=-7, bulletIndent=0, spaceAfter=2.5),
    "skill": style("skill", fontSize=9.2, leading=12.2, leftIndent=8, firstLineIndent=-6, bulletIndent=0, spaceAfter=2.5),
    "footer_left": style("footer_left", fontSize=7.4, leading=8.5, textColor=colors.HexColor("#93A2AF")),
    "footer_right": style("footer_right", fontSize=7.4, leading=8.5, textColor=colors.HexColor("#93A2AF"), alignment=TA_RIGHT),
}


def p(text, style_name="body"):
    return Paragraph(text, STYLES[style_name])


def bullet(text, compact=False):
    return Paragraph(text, STYLES["bullet_small" if compact else "bullet"], bulletText="•")


def role(title, organization, details, description=None):
    blocks = [p(title, "role"), p(f"<b>{organization}</b> &nbsp;|&nbsp; {details}", "meta")]
    if description:
        blocks.append(p(description, "desc"))
    return blocks


def section(label, blocks, top_space=0):
    right = []
    if top_space:
        right.append(Spacer(1, top_space))
    right.extend(
        [
            HRFlowable(width="100%", thickness=0.65, color=LIGHT, spaceBefore=0, spaceAfter=4),
            *blocks,
        ]
    )
    table = Table(
        [[p(label.upper(), "label"), right]],
        colWidths=[LABEL_W, BODY_W],
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return table


def footer(canvas, doc):
    canvas.saveState()
    canvas.setTitle("CV Miguel Varona Gallego - Full-Stack Product Engineer")
    canvas.setAuthor("Miguel Varona Gallego")
    y = 8.2 * mm
    left = Paragraph("Miguel Varona Gallego | Full-Stack Product Engineer", STYLES["footer_left"])
    right = Paragraph(
        f'<link href="mailto:migvaronag@gmail.com" color="#93A2AF">migvaronag@gmail.com</link>'
        f' &nbsp;|&nbsp; <link href="https://github.com/MigVarona" color="#93A2AF">github.com/MigVarona</link>'
        f' &nbsp;|&nbsp; {doc.page} / 2',
        STYLES["footer_right"],
    )
    left.wrapOn(canvas, CONTENT_W * 0.47, 12)
    right.wrapOn(canvas, CONTENT_W * 0.53, 12)
    left.drawOn(canvas, MARGIN_X, y)
    right.drawOn(canvas, MARGIN_X + CONTENT_W * 0.47, y)
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    leftMargin=MARGIN_X,
    rightMargin=MARGIN_X,
    topMargin=TOP_MARGIN,
    bottomMargin=BOTTOM_MARGIN,
    title="CV Miguel Varona Gallego - Full-Stack Product Engineer",
    author="Miguel Varona Gallego",
    subject="Curriculum vitae",
)

frame = Frame(
    MARGIN_X,
    BOTTOM_MARGIN,
    CONTENT_W,
    PAGE_H - TOP_MARGIN - BOTTOM_MARGIN,
    leftPadding=0,
    rightPadding=0,
    topPadding=0,
    bottomPadding=0,
)
doc.addPageTemplates([PageTemplate(id="cv", frames=[frame], onPage=footer)])

header_left = [
    p("MIGUEL VARONA GALLEGO", "name"),
    p("FULL-STACK PRODUCT ENGINEER", "title"),
    p("WEB Y MOBILE &nbsp;|&nbsp; NEXT.JS · TYPESCRIPT · NODE.JS · REACT NATIVE &nbsp;|&nbsp; IA APLICADA", "tagline"),
    HRFlowable(width="100%", thickness=0.7, color=LIGHT, spaceBefore=0, spaceAfter=6),
    p(
        'Madrid, España &nbsp;|&nbsp; <link href="tel:+34652592293" color="#748392">+34 652 592 293</link>'
        ' &nbsp;|&nbsp; <link href="mailto:migvaronag@gmail.com" color="#2F638B">migvaronag@gmail.com</link>',
        "contact",
    ),
    p(
        '<link href="https://wearecapa.es" color="#2F638B">wearecapa.es</link>'
        ' &nbsp;|&nbsp; <link href="https://linkedin.com/in/miguelvaronagallego" color="#2F638B">linkedin.com/in/miguelvaronagallego</link>'
        ' &nbsp;|&nbsp; <link href="https://github.com/MigVarona" color="#2F638B">github.com/MigVarona</link>',
        "contact",
    ),
]

photo = Image(str(PHOTO), width=32 * mm, height=32 * mm)
header = Table([[header_left, photo]], colWidths=[CONTENT_W - 37 * mm, 37 * mm], hAlign="LEFT")
header.setStyle(
    TableStyle(
        [
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]
    )
)

story = [header, Spacer(1, 8)]

profile = [
    p(
        "Full-Stack Product Engineer con enfoque end-to-end en productos web y móviles. Diseño, desarrollo y llevo a producción aplicaciones con TypeScript, React/Next.js, Node.js, React Native y PostgreSQL/Supabase, incorporando Server-Side Rendering (SSR), seguridad, pagos e integraciones de IA.",
        "body",
    ),
    Spacer(1, 5),
    p(
        "Anteriormente fundé y dirigí durante nueve años una empresa de hasta 30 personas, por lo que combino ingeniería, producto y criterio de negocio.",
        "body",
    ),
]
story.extend([section("Perfil", profile), Spacer(1, 9)])

experience_1 = []
experience_1.extend(
    role(
        "Full-Stack Product Engineer",
        'WEARECAPA · <link href="https://wearecapa.es" color="#2F638B">wearecapa.es</link>',
        "mar. 2026 - actualidad | Madrid",
        "Estudio de producto digital especializado en aplicaciones web y móviles, plataformas SaaS e integraciones de IA para clientes y productos propios.",
    )
)
experience_1.extend(
    [
        bullet("Lidero el ciclo completo de producto: alcance funcional, UX/UI, frontend, backend, despliegue y evolución en producción; integro APIs, automatizaciones y servicios de terceros."),
        bullet('<b>Bookarta</b>: construí y lancé un SaaS B2B multi-tenant para restauración, con clientes activos en España y Europa e ingresos recurrentes desde el primer mes. Implementé aislamiento por organización con RLS, suscripciones con Stripe y extracción estructurada de cartas con OpenAI. <link href="https://bookarta.es" color="#2F638B">bookarta.es</link>'),
        bullet('<b>Flare</b>: desarrollé una experiencia web y una app móvil sincronizadas en tiempo real para espacios compartidos. <link href="https://holaflare.xyz" color="#2F638B">holaflare.xyz</link>'),
        bullet('<b>RENEW</b>: desarrollé una plataforma editorial de salud, web y móvil, orientada a conversión y SEO. <link href="https://renew-habits.com" color="#2F638B">renew-habits.com</link>'),
        Spacer(1, 7),
    ]
)
experience_1.extend(
    role(
        "Auditor de seguridad y desarrollador backend | Freelance",
        "Cliente SaaS B2B multi-tenant · Malt",
        "desde jul. 2026 · por proyectos · Remoto",
    )
)
experience_1.extend(
    [
        bullet("Detecté y corregí dos vulnerabilidades no identificadas previamente, incluida una de gravedad alta, en un backend sobre Supabase y PostgreSQL."),
        bullet("Implementé un parche SQL mínimo y reversible, reforcé las políticas RLS, revisé credenciales y validé el aislamiento mediante pruebas directas sobre la API, documentando evidencias y rollback."),
        Spacer(1, 7),
    ]
)
experience_1.extend(
    role(
        "Full-Stack Developer y Responsable Digital",
        'AMAE · <link href="https://premiosamae.com" color="#2F638B">premiosamae.com</link>',
        "may. 2025 - actualidad | Remoto",
    )
)
experience_1.extend(
    [
        bullet("Desarrollo el ecosistema digital de la asociación: web institucional, herramientas internas y plataforma de gestión de los Premios AMAE.", compact=True),
        bullet("Construí los flujos de inscripción, documentación y votación que gestionaron más de 200 inscripciones en 10 categorías, con permisos RLS para candidato, jurado y administración.", compact=True),
    ]
)
story.extend([section("Experiencia", experience_1), PageBreak()])

experience_2 = []
experience_2.extend(
    role(
        "Full-Stack Developer",
        "Agencia para el Empleo de Madrid",
        "feb. 2024 - dic. 2024 | Madrid",
    )
)
experience_2.extend(
    [
        bullet("Desarrollé una plataforma web con IA para apoyar y automatizar procesos de orientación laboral, incluyendo una experiencia inmersiva y un asistente virtual.", compact=True),
        bullet("Integré flujos con OpenAI para generar, estructurar y gestionar contenidos sobre React, Node.js, Express y Docker; definí requisitos con usuarios y stakeholders.", compact=True),
        Spacer(1, 6),
    ]
)
experience_2.extend(
    role(
        "Fundador y CEO",
        'Carmencita Film Lab · <link href="https://carmencitafilmlab.com" color="#2F638B">carmencitafilmlab.com</link>',
        "jul. 2013 - jul. 2022 | Valencia",
    )
)
experience_2.extend(
    [
        bullet("Fundé y dirigí durante nueve años un laboratorio fotográfico de referencia, con clientes en toda Europa y un equipo de hasta 30 personas.", compact=True),
        bullet("Dirigí producto, operaciones y estrategia comercial internacional, y coordiné tecnología, sistemas internos y presencia digital.", compact=True),
        Spacer(1, 6),
    ]
)
experience_2.extend(
    role(
        "Docente | Fotografía Fine Art",
        "EFTI - Escuela de Fotografía y Centro de Imagen",
        "2015 - 2017 | Madrid",
    )
)
experience_2.append(
    bullet("Impartí composición avanzada, iluminación y postproducción, y tutoricé proyectos personales.", compact=True)
)
story.extend([section("Experiencia", experience_2), Spacer(1, 8)])

skills = [
    Paragraph("<b>Producto</b>: definición funcional, arquitectura, modelado de datos, UX/UI, Figma y entrega end-to-end.", STYLES["skill"], bulletText="•"),
    Paragraph("<b>Frontend y mobile</b>: TypeScript, JavaScript, React, Next.js, Server-Side Rendering (SSR), Tailwind CSS, Three.js, React Native, Expo y EAS Build.", STYLES["skill"], bulletText="•"),
    Paragraph("<b>Backend y datos</b>: Node.js, Express, APIs REST, PostgreSQL, Supabase, MySQL y MongoDB.", STYLES["skill"], bulletText="•"),
    Paragraph("<b>SaaS y seguridad</b>: multi-tenant, autenticación, Supabase RLS, seguridad de bases de datos, Stripe y Resend.", STYLES["skill"], bulletText="•"),
    Paragraph("<b>IA aplicada</b>: OpenAI, Anthropic y Groq; extracción y estructuración de datos, asistentes, automatización de flujos e integración de LLMs en producto.", STYLES["skill"], bulletText="•"),
    Paragraph("<b>Cloud y delivery</b>: Vercel, AWS, Railway, Docker, GitHub Actions y CI/CD; desarrollo asistido con Claude Code, Cursor y Copilot.", STYLES["skill"], bulletText="•"),
]
story.extend([section("Competencias", skills), Spacer(1, 8)])

education = [
    p("<b><font color='#2F638B'>Bootcamp Full Stack Developer - 1.000 horas</font></b>", "body_small"),
    p("<b>Factoría F5</b> | Madrid | 2022 - 2023", "meta"),
    p("JavaScript, React, Next.js, Node.js, Express, MongoDB, Git y Docker; Three.js y A-Frame para WebXR y 3D en navegador.", "body_small"),
    Spacer(1, 5),
    p("<b><font color='#2F638B'>Técnico Superior en Imagen</font></b>", "body_small"),
    p("<b>IES Príncipe Felipe</b> | Madrid | 2010 - 2012", "meta"),
]
story.extend([section("Formación", education), Spacer(1, 7)])

languages = [p("<b>Español</b>: nativo &nbsp;&nbsp;|&nbsp;&nbsp; <b>Inglés</b>: B2", "body")]
story.append(section("Idiomas", languages))

doc.build(story)
print(OUTPUT)
