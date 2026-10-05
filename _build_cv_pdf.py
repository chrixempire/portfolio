#!/usr/bin/env python3
"""Generate Christian Anyikamadu CV as a PDF matching the sample layout."""

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

NAVY = HexColor("#1A1A1A")
MUTED = HexColor("#3A3A3A")
FONT_DIR = Path("/Users/acumenmac/Documents/codebase/personal/portfolio/fonts")

pdfmetrics.registerFont(TTFont("Calibri", str(FONT_DIR / "Calibri.ttf")))
pdfmetrics.registerFont(TTFont("Calibri-Bold", str(FONT_DIR / "Calibri-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Calibri-Italic", str(FONT_DIR / "Calibri-Italic.ttf")))
pdfmetrics.registerFont(TTFont("Calibri-BoldItalic", str(FONT_DIR / "Calibri-BoldItalic.ttf")))
pdfmetrics.registerFontFamily(
    "Calibri",
    normal="Calibri",
    bold="Calibri-Bold",
    italic="Calibri-Italic",
    boldItalic="Calibri-BoldItalic",
)

OUT = "/Users/acumenmac/Documents/codebase/personal/portfolio/Christian_Anyikamadu_CV.pdf"


def styles():
    s = getSampleStyleSheet()
    s.add(
        ParagraphStyle(
            name="Name",
            fontName="Calibri-Bold",
            fontSize=20,
            leading=24,
            alignment=TA_CENTER,
            textColor=NAVY,
            spaceAfter=1,
        )
    )
    s.add(
        ParagraphStyle(
            name="TitleLine",
            fontName="Calibri",
            fontSize=11,
            leading=14,
            alignment=TA_CENTER,
            textColor=NAVY,
            spaceAfter=3,
        )
    )
    s.add(
        ParagraphStyle(
            name="Contact",
            fontName="Calibri",
            fontSize=8.5,
            leading=11,
            alignment=TA_CENTER,
            textColor=MUTED,
            spaceAfter=4,
        )
    )
    s.add(
        ParagraphStyle(
            name="Section",
            fontName="Calibri-Bold",
            fontSize=11,
            leading=14,
            alignment=TA_LEFT,
            textColor=NAVY,
            spaceBefore=6,
            spaceAfter=2,
        )
    )
    s.add(
        ParagraphStyle(
            name="Summary",
            fontName="Calibri",
            fontSize=9.75,
            leading=12.4,
            alignment=TA_JUSTIFY,
            textColor=NAVY,
            spaceAfter=2,
        )
    )
    s.add(
        ParagraphStyle(
            name="JobLeft",
            fontName="Calibri-Bold",
            fontSize=10.5,
            leading=13,
            alignment=TA_LEFT,
            textColor=NAVY,
        )
    )
    s.add(
        ParagraphStyle(
            name="JobRight",
            fontName="Calibri",
            fontSize=10,
            leading=13,
            alignment=TA_RIGHT,
            textColor=NAVY,
        )
    )
    s.add(
        ParagraphStyle(
            name="Location",
            fontName="Calibri",
            fontSize=9.5,
            leading=12,
            textColor=MUTED,
            spaceAfter=0,
        )
    )
    s.add(
        ParagraphStyle(
            name="Tools",
            fontName="Calibri-Italic",
            fontSize=9,
            leading=12,
            textColor=MUTED,
            spaceAfter=3,
        )
    )
    s.add(
        ParagraphStyle(
            name="Product",
            fontName="Calibri-Bold",
            fontSize=10,
            leading=13,
            textColor=NAVY,
            spaceBefore=3,
            spaceAfter=0,
        )
    )
    s.add(
        ParagraphStyle(
            name="BulletText",
            fontName="Calibri",
            fontSize=9.75,
            leading=12.2,
            alignment=TA_LEFT,
            textColor=NAVY,
            leftIndent=12,
            firstLineIndent=-10,
            spaceBefore=0,
            spaceAfter=1,
        )
    )
    s.add(
        ParagraphStyle(
            name="Skill",
            fontName="Calibri",
            fontSize=10,
            leading=13,
            textColor=NAVY,
            spaceBefore=0,
            spaceAfter=1,
        )
    )
    return s


def rule():
    return HRFlowable(width="100%", thickness=0.8, color=NAVY, spaceBefore=0, spaceAfter=2)


def section(st, text):
    return KeepTogether([Paragraph(text.upper(), st["Section"]), rule()])


def job_header(st, left, right):
    table = Table(
        [[Paragraph(left, st["JobLeft"]), Paragraph(right, st["JobRight"])]],
        colWidths=[5.0 * inch, 2.1 * inch],
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return table


def bullets(st, items):
    return [Paragraph(f"•  {item}", st["BulletText"]) for item in items]


def build():
    st = styles()
    story = []

    story.append(Paragraph("Christian Anyikamadu", st["Name"]))
    story.append(Paragraph("Product Engineer  |  Frontend Engineer", st["TitleLine"]))
    story.append(
        Paragraph(
            "Lagos, Nigeria   |   +234 814 299 3740   |   anyikamaduchris@gmail.com   |   linkedin.com/in/anyikamaduchris   |   github.com/chrixempire",
            st["Contact"],
        )
    )
    story.append(HRFlowable(width="100%", thickness=1.1, color=NAVY, spaceBefore=0, spaceAfter=2))

    story.append(section(st, "SUMMARY"))
    story.append(
        Paragraph(
            "Product Engineer | Frontend Engineer with 4 years of experience building and shipping production web applications across fintech, procurement, SaaS, e-commerce, and marketplace products. Strong in React, Next.js, TypeScript, JavaScript, REST APIs, WebSockets, Nuxt.js, Vue.js, and frontend architecture, with experience building reusable components, responsive interfaces, and end-to-end product features in collaboration with product, design, and backend teams.",
            st["Summary"],
        )
    )

    story.append(section(st, "EXPERIENCE"))

    story.append(job_header(st, "Frontend Engineer, Bayana (Contract)", "Jan 2026 – Present"))
    story.append(Paragraph("Lagos, Nigeria", st["Location"]))
    story.append(Paragraph("Tools — JavaScript, TypeScript, React.js, Next.js, CSS, Tailwind CSS", st["Tools"]))
    story.append(Paragraph("Bayana — NGO Volunteer &amp; Donor Platform", st["Product"]))
    story.extend(
        bullets(
            st,
            [
                "Owned frontend development for Bayana, a platform connecting verified NGOs with volunteers and donors, taking core product features from requirements through production delivery.",
                "Built reusable React components and responsive interfaces for NGO event creation, management, community engagement, messaging, and broadcast communications.",
                "Developed messaging and broadcasting workflows that enabled NGOs to communicate with and engage their communities through the platform.",
                "Integrated frontend features with backend REST APIs and collaborated with the engineering team to deliver and iterate on production-ready functionality.",
            ],
        )
    )

    story.append(job_header(st, "Frontend Engineer, Acumen Digital", "Apr 2025 – Aug 2026"))
    story.append(Paragraph("Lagos, Nigeria", st["Location"]))
    story.append(
        Paragraph(
            "Tools — JavaScript, TypeScript, React.js, Next.js, Vue.js, Nuxt.js, CSS, Tailwind CSS",
            st["Tools"],
        )
    )
    story.extend(
        bullets(
            st,
            [
                "Owned and shipped production frontend features across fintech, FX, procurement, lending, and marketplace products, taking features from requirements through implementation, testing, and release.",
                "Collaborated with product, design, backend, and QA teams on frontend architecture, technical decisions, code reviews, debugging, and production releases.",
            ],
        )
    )
    story.append(Paragraph("Octupus — Prediction Market Platform", st["Product"]))
    story.extend(
        bullets(
            st,
            [
                "Contributed to the development of Octupus, a real-time prediction market platform, building core trading experiences that allow users to discover markets, buy and sell outcome shares, and manage their positions.",
                "Built key market interfaces supporting multiple outcomes and markets within a single event, enabling users to explore different prediction opportunities and trade positions seamlessly.",
                "Developed responsive buy/sell trading flows, including stake selection, position previews, transaction states, confirmations, and real-time updates across active markets.",
            ],
        )
    )
    story.append(Paragraph("Tendar — Lending-as-a-Service", st["Product"]))
    story.extend(
        bullets(
            st,
            [
                "Built frontend experiences for a lending platform where users originate, track, and repay loans from a centralized dashboard.",
                "Instrumental in developing and delivering Lending-as-a-Service (LaaS) features, including automated loan disbursement and recollections, and tools to speed up lending operations.",
                "Built and optimized KYC processes for Tendar’s Buy Now Pay Later feature, including BVN verification, document upload, and customer selfies through custom solutions that ensured speed and flexibility to change.",
            ],
        )
    )
    story.append(Paragraph("Kaorex — Trading &amp; Escrow Platform", st["Product"]))
    story.extend(
        bullets(
            st,
            [
                "Built and shipped escrow, trading, live chat, reviews, compliance, and real-time transaction experiences.",
                "Owned frontend implementation across customer and admin applications, integrating REST APIs and WebSockets for real-time transaction experiences.",
                "Redesigned key product workflows and built reusable UI components to improve usability and development efficiency.",
                "Collaborated with product, design, and backend teams to ship, test, and iterate production features.",
            ],
        )
    )
    story.append(Paragraph("GoPath — Dynamic Form Builder", st["Product"]))
    story.extend(
        bullets(
            st,
            [
                "Led frontend development of a dynamic form builder that enabled users to create, configure, and distribute custom forms without engineering support.",
                "Designed reusable form components and workflows for dynamic configuration, validation, publishing, and form management.",
            ],
        )
    )

    story.append(
        job_header(
            st,
            "Frontend Engineer, Independent Purchasing Company – Africa",
            "Nov 2022 – Mar 2025",
        )
    )
    story.append(Paragraph("Lagos, Nigeria", st["Location"]))
    story.append(Paragraph("Tools — JavaScript, TypeScript, React.js, Vue.js, Nuxt.js, CSS, Tailwind CSS", st["Tools"]))
    story.append(Paragraph("Daash — Inventory Management SaaS", st["Product"]))
    story.extend(
        bullets(
            st,
            [
                "Contributed to frontend engineering and product direction, overseeing frontend architecture, code quality, and product improvements.",
                "Implemented payment integrations supporting multiple payment methods and streamlined checkout workflows.",
            ],
        )
    )
    story.append(Paragraph("GoSource — B2B Food Procurement Platform", st["Product"]))
    story.extend(
        bullets(
            st,
            [
                "Led end-to-end frontend development across the customer web app, admin dashboard, and marketing website.",
                "Built procurement, checkout, payment, order management, and customer-facing workflows.",
                "Contributed to nearly $70K in revenue within two months and a 3x increase in customer growth and retention through iterative product improvements.",
                "Scaled the engineering team from 3 to 10, establishing code review, documentation, and mentorship practices.",
            ],
        )
    )
    story.append(Paragraph("Papa’s Grill — Ordering and Admin Platform", st["Product"]))
    story.extend(
        bullets(
            st,
            [
                "Contributed to the development of Papa’s Grill marketing website, procurement platform, and admin dashboard, which led to a 50%+ increase in profitability through improved customer experience and ordering workflows.",
                "Helped acquire more than 1,000 users during the first month after launch.",
            ],
        )
    )

    story.append(section(st, "OTHER PRODUCTS AND COLLABORATIONS"))
    story.append(job_header(st, "Frontend Engineer, PostHearts", "Apr 2025 – Dec 2025"))
    story.append(Paragraph("Lagos, Nigeria", st["Location"]))
    story.append(Paragraph("Tools — JavaScript, TypeScript, React.js, Next.js, CSS, Tailwind CSS", st["Tools"]))
    story.append(Paragraph("PostHearts — Digital Letter-Making Platform", st["Product"]))
    story.extend(
        bullets(
            st,
            [
                "Built React frontend experiences for PostHearts, developing an interactive letter editor with typography, backgrounds, photos, stickers, emojis, and responsive content creation workflows.",
                "Implemented responsive creation and sharing experiences, integrated product APIs, and collaborated with design and engineering to ship polished, production-ready features across web and mobile.",
            ],
        )
    )
    story.append(job_header(st, "Frontend Engineer, Quality", "Aug 2025 – Present"))
    story.append(Paragraph("Lagos, Nigeria", st["Location"]))
    story.append(Paragraph("Tools — JavaScript, TypeScript, React.js, Next.js, CSS, Tailwind CSS", st["Tools"]))
    story.append(Paragraph("Quality — Real-Time Feedback Platform", st["Product"]))
    story.extend(
        bullets(
            st,
            [
                "Contributed to Quality, a real-time feedback platform for team collaboration and feedback management.",
                "Built responsive Next.js interfaces, reusable React components, and micro-interactions for core workflows.",
                "Integrated REST APIs and real-time features, collaborating with product and engineering teams to ship production-ready features.",
            ],
        )
    )

    story.append(section(st, "SKILLS"))
    story.append(
        Paragraph(
            "<b>Product &amp; Engineering:</b>  Product Development  ·  Feature Ownership  ·  Frontend Architecture  ·  Component Architecture  ·  Technical Collaboration  ·  API Integration  ·  Performance Optimization  ·  Technical Problem Solving  ·  Cross-functional Collaboration  ·  Code Review",
            st["Skill"],
        )
    )
    story.append(
        Paragraph(
            "<b>Frontend:</b>  React.js  ·  Next.js  ·  Vue.js  ·  Nuxt.js  ·  TypeScript  ·  JavaScript  ·  HTML5  ·  CSS3  ·  Tailwind CSS  ·  Sass",
            st["Skill"],
        )
    )
    story.append(
        Paragraph(
            "<b>APIs &amp; Architecture:</b>  REST APIs  ·  WebSockets  ·  State Management  ·  Responsive Design",
            st["Skill"],
        )
    )
    story.append(
        Paragraph(
            "<b>Testing &amp; Tools:</b>  Jest  ·  Unit Testing  ·  Integration Testing  ·  API Testing  ·  Git  ·  GitHub  ·  Postman  ·  Figma  ·  Jira  ·  Vite",
            st["Skill"],
        )
    )
    story.append(
        Paragraph(
            "<b>Deployment:</b>  Vercel  ·  Netlify  ·  Railway  ·  CI/CD",
            st["Skill"],
        )
    )

    story.append(section(st, "EDUCATION"))
    story.append(
        job_header(
            st,
            "B.Eng. Electrical and Electronics Engineering — First Class Honours",
            "2018 – 2023",
        )
    )
    story.append(
        Paragraph(
            "Olusegun Agagu University of Science and Technology (OAUSTECH), Nigeria",
            st["Location"],
        )
    )
    story.append(Spacer(1, 4))

    doc = SimpleDocTemplate(
        OUT,
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.45 * inch,
        bottomMargin=0.4 * inch,
        title="Christian Anyikamadu — CV",
        author="Christian Anyikamadu",
    )
    doc.build(story)
    print(OUT)


if __name__ == "__main__":
    build()
