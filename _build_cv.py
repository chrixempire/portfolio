#!/usr/bin/env python3
"""Generate Christian Anyikamadu CV as a formatted DOCX matching the sample layout."""

import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn, nsmap
from docx.shared import Cm, Inches, Pt, RGBColor, Twips
from docx.enum.table import WD_TABLE_ALIGNMENT

NAVY = RGBColor(0x1A, 0x1A, 0x1A)
MUTED = RGBColor(0x3A, 0x3A, 0x3A)
RULE = "1A1A1A"
FONT = "Calibri"


def set_run(run, *, size=11, bold=False, italic=False, color=NAVY, font=FONT):
    run.font.name = font
    run._element.rPr.rFonts.set(qn("w:eastAsia"), font)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color


def set_paragraph_spacing(p, before=0, after=0, line=240, after_auto=False):
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    # 240 twips = single; 230 keeps it compact like the sample
    pf.line_spacing = line / 240.0
    pPr = p._p.get_or_add_pPr()
    if after_auto:
        spacing = pPr.find(qn("w:spacing"))
        if spacing is None:
            spacing = OxmlElement("w:spacing")
            pPr.append(spacing)


def set_run_font_theme(run):
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), FONT)
    rFonts.set(qn("w:hAnsi"), FONT)
    rFonts.set(qn("w:cs"), FONT)


def add_bottom_border(paragraph, color=RULE, sz="12"):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = pPr.find(qn("w:pBdr"))
    if pBdr is None:
        pBdr = OxmlElement("w:pBdr")
        pPr.append(pBdr)
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), sz)
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), color)
    existing = pBdr.find(qn("w:bottom"))
    if existing is not None:
        pBdr.remove(existing)
    pBdr.append(bottom)


def shade_cell(cell, fill="FFFFFF"):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    shd.set(qn("w:val"), "clear")
    tcPr.append(shd)


def set_cell_margins(cell, top=0, bottom=0, left=0, right=0):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for edge, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        node = OxmlElement(f"w:{edge}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def prevent_row_split(row):
    tr = row._tr
    trPr = tr.get_or_add_trPr()
    cant = OxmlElement("w:cantSplit")
    trPr.append(cant)


def set_table_fixed(table, widths):
    table.autofit = False
    table.allow_autofit = False
    tbl = table._tbl
    tblPr = tbl.tblPr
    tblW = tblPr.find(qn("w:tblW"))
    if tblW is None:
        tblW = OxmlElement("w:tblW")
        tblPr.append(tblW)
    total = sum(widths)
    tblW.set(qn("w:w"), str(total))
    tblW.set(qn("w:type"), "dxa")
    grid = tbl.find(qn("w:tblGrid"))
    if grid is not None:
        tbl.remove(grid)
    grid = OxmlElement("w:tblGrid")
    for w in widths:
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), str(w))
        grid.append(gc)
    tbl.insert(1, grid)
    for row in table.rows:
        for i, cell in enumerate(row.cells):
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            tcW = tcPr.find(qn("w:tcW"))
            if tcW is None:
                tcW = OxmlElement("w:tcW")
                tcPr.append(tcW)
            tcW.set(qn("w:w"), str(widths[i]))
            tcW.set(qn("w:type"), "dxa")


def clear_table_borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "nil")
        el.set(qn("w:sz"), "0")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "auto")
        borders.append(el)
    existing = tblPr.find(qn("w:tblBorders"))
    if existing is not None:
        tblPr.remove(existing)
    tblPr.append(borders)


def add_centered(doc, text, *, size, bold=False, before=0, after=0, color=NAVY):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p, before=before, after=after, line=230)
    run = p.add_run(text)
    set_run(run, size=size, bold=bold, color=color)
    set_run_font_theme(run)
    return p


def add_section_heading(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_paragraph_spacing(p, before=10, after=4, line=220)
    run = p.add_run(text.upper())
    set_run(run, size=11.5, bold=True)
    set_run_font_theme(run)
    add_bottom_border(p, sz="12")
    return p


def add_body(doc, text, *, size=10.5, italic=False, before=2, after=4, bold=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    set_paragraph_spacing(p, before=before, after=after, line=230)
    run = p.add_run(text)
    set_run(run, size=size, italic=italic, bold=bold)
    set_run_font_theme(run)
    return p


def add_job_header(doc, left, right, usable_dxa):
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    left_w = int(usable_dxa * 0.68)
    right_w = usable_dxa - left_w
    set_table_fixed(table, [left_w, right_w])
    clear_table_borders(table)
    prevent_row_split(table.rows[0])

    lc, rc = table.rows[0].cells
    set_cell_margins(lc, top=40, bottom=0, left=0, right=60)
    set_cell_margins(rc, top=40, bottom=0, left=40, right=0)

    lp = lc.paragraphs[0]
    lp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_paragraph_spacing(lp, before=0, after=0, line=220)
    lr = lp.add_run(left)
    set_run(lr, size=11, bold=True)
    set_run_font_theme(lr)

    rp = rc.paragraphs[0]
    rp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_paragraph_spacing(rp, before=0, after=0, line=220)
    rr = rp.add_run(right)
    set_run(rr, size=10.5, bold=False)
    set_run_font_theme(rr)
    return table


def add_location(doc, text):
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=0, after=1, line=220)
    run = p.add_run(text)
    set_run(run, size=10, italic=False, color=MUTED)
    set_run_font_theme(run)
    return p


def add_tools(doc, text):
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=0, after=3, line=220)
    label = p.add_run("Tools — ")
    set_run(label, size=10, italic=True, color=MUTED)
    set_run_font_theme(label)
    rest = p.add_run(text)
    set_run(rest, size=10, italic=True, color=MUTED)
    set_run_font_theme(rest)
    return p


def add_product_heading(doc, text):
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=5, after=1, line=220)
    run = p.add_run(text)
    set_run(run, size=10.5, bold=True, italic=False)
    set_run_font_theme(run)
    return p


def add_bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    set_paragraph_spacing(p, before=0, after=1, line=226)
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.first_line_indent = Inches(-0.15)
    # clear default runs
    if p.runs:
        p.runs[0].text = ""
    run = p.add_run(text)
    set_run(run, size=10.5)
    set_run_font_theme(run)
    return p


def add_skill_line(doc, label, items):
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=1, after=2, line=226)
    lr = p.add_run(f"{label}:  ")
    set_run(lr, size=10.5, bold=True)
    set_run_font_theme(lr)
    ir = p.add_run(items)
    set_run(ir, size=10.5)
    set_run_font_theme(ir)
    return p


def set_document_calibri(doc):
    """Force Calibri as the document theme, Normal, and list styles."""
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = NAVY
    rPr = normal.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    for attr in ("ascii", "hAnsi", "cs", "eastAsia"):
        rFonts.set(qn(f"w:{attr}"), FONT)

    try:
        bullet = doc.styles["List Bullet"]
        bullet.font.name = FONT
        bullet.font.size = Pt(10.5)
        bullet.font.color.rgb = NAVY
        brPr = bullet.element.get_or_add_rPr()
        bFonts = brPr.find(qn("w:rFonts"))
        if bFonts is None:
            bFonts = OxmlElement("w:rFonts")
            brPr.insert(0, bFonts)
        for attr in ("ascii", "hAnsi", "cs", "eastAsia"):
            bFonts.set(qn(f"w:{attr}"), FONT)
    except KeyError:
        pass

    # Pin theme latin typefaces to Calibri (major + minor).
    for rel in doc.part.rels.values():
        if "theme" in rel.reltype:
            xml = rel.target_part.blob.decode("utf-8")
            xml = re.sub(r'(<a:latin\b[^>]*typeface=")[^"]*(")', rf'\1{FONT}\2', xml)
            rel.target_part._blob = xml.encode("utf-8")

    # Document-level run defaults
    styles_el = doc.styles.element
    rPrDefault = styles_el.find(qn("w:docDefaults"))
    if rPrDefault is not None:
        rPr = rPrDefault.find(".//" + qn("w:rPr"))
        if rPr is not None:
            rFonts = rPr.find(qn("w:rFonts"))
            if rFonts is None:
                rFonts = OxmlElement("w:rFonts")
                rPr.insert(0, rFonts)
            for attr in ("ascii", "hAnsi", "cs", "eastAsia"):
                rFonts.set(qn(f"w:{attr}"), FONT)


def build():
    doc = Document()
    set_document_calibri(doc)

    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.55)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)

    usable_dxa = int((8.5 - 0.7 - 0.7) * 1440)

    # Header
    name = add_centered(doc, "Christian Anyikamadu", size=26, bold=True, after=1)
    add_centered(
        doc,
        "Product Engineer  |  Frontend Engineer",
        size=12,
        bold=False,
        before=0,
        after=2,
    )
    contact = add_centered(
        doc,
        "Lagos, Nigeria   |   +234 814 299 3740   |   anyikamaduchris@gmail.com   |   linkedin.com/in/anyikamaduchris   |   github.com/chrixempire",
        size=9.5,
        before=0,
        after=6,
        color=MUTED,
    )
    add_bottom_border(contact, sz="16")

    # Summary
    add_section_heading(doc, "SUMMARY")
    add_body(
        doc,
        "Product Engineer | Frontend Engineer with 4 years of experience building and shipping production web applications across fintech, procurement, SaaS, e-commerce, and marketplace products. Strong in React, Next.js, TypeScript, JavaScript, REST APIs, WebSockets, Nuxt.js, Vue.js, and frontend architecture, with experience building reusable components, responsive interfaces, and end-to-end product features in collaboration with product, design, and backend teams.",
        size=10.5,
        before=4,
        after=2,
    )

    # Experience
    add_section_heading(doc, "EXPERIENCE")

    # Bayana
    add_job_header(
        doc,
        "Frontend Engineer, Bayana (Contract)",
        "Jan 2026 – Present",
        usable_dxa,
    )
    add_location(doc, "Lagos, Nigeria")
    add_tools(doc, "JavaScript, TypeScript, React.js, Next.js, CSS, Tailwind CSS")
    add_product_heading(doc, "Bayana — NGO Volunteer & Donor Platform")
    add_bullet(
        doc,
        "Owned frontend development for Bayana, a platform connecting verified NGOs with volunteers and donors, taking core product features from requirements through production delivery.",
    )
    add_bullet(
        doc,
        "Built reusable React components and responsive interfaces for NGO event creation, management, community engagement, messaging, and broadcast communications.",
    )
    add_bullet(
        doc,
        "Developed messaging and broadcasting workflows that enabled NGOs to communicate with and engage their communities through the platform.",
    )
    add_bullet(
        doc,
        "Integrated frontend features with backend REST APIs and collaborated with the engineering team to deliver and iterate on production-ready functionality.",
    )

    # Acumen
    add_job_header(
        doc,
        "Frontend Engineer, Acumen Digital",
        "Apr 2025 – Aug 2026",
        usable_dxa,
    )
    add_location(doc, "Lagos, Nigeria")
    add_tools(
        doc,
        "JavaScript, TypeScript, React.js, Next.js, Vue.js, Nuxt.js, CSS, Tailwind CSS",
    )
    add_bullet(
        doc,
        "Owned and shipped production frontend features across fintech, FX, procurement, lending, and marketplace products, taking features from requirements through implementation, testing, and release.",
    )
    add_bullet(
        doc,
        "Collaborated with product, design, backend, and QA teams on frontend architecture, technical decisions, code reviews, debugging, and production releases.",
    )

    add_product_heading(doc, "Octupus — Prediction Market Platform")
    add_bullet(
        doc,
        "Contributed to the development of Octupus, a real-time prediction market platform, building core trading experiences that allow users to discover markets, buy and sell outcome shares, and manage their positions.",
    )
    add_bullet(
        doc,
        "Built key market interfaces supporting multiple outcomes and markets within a single event, enabling users to explore different prediction opportunities and trade positions seamlessly.",
    )
    add_bullet(
        doc,
        "Developed responsive buy/sell trading flows, including stake selection, position previews, transaction states, confirmations, and real-time updates across active markets.",
    )

    add_product_heading(doc, "Tendar — Lending-as-a-Service")
    add_bullet(
        doc,
        "Built frontend experiences for a lending platform where users originate, track, and repay loans from a centralized dashboard.",
    )
    add_bullet(
        doc,
        "Instrumental in developing and delivering Lending-as-a-Service (LaaS) features, including automated loan disbursement and recollections, and tools to speed up lending operations.",
    )
    add_bullet(
        doc,
        "Built and optimized KYC processes for Tendar’s Buy Now Pay Later feature, including BVN verification, document upload, and customer selfies through custom solutions that ensured speed and flexibility to change.",
    )

    add_product_heading(doc, "Kaorex — Trading & Escrow Platform")
    add_bullet(
        doc,
        "Built and shipped escrow, trading, live chat, reviews, compliance, and real-time transaction experiences.",
    )
    add_bullet(
        doc,
        "Owned frontend implementation across customer and admin applications, integrating REST APIs and WebSockets for real-time transaction experiences.",
    )
    add_bullet(
        doc,
        "Redesigned key product workflows and built reusable UI components to improve usability and development efficiency.",
    )
    add_bullet(
        doc,
        "Collaborated with product, design, and backend teams to ship, test, and iterate production features.",
    )

    add_product_heading(doc, "GoPath — Dynamic Form Builder")
    add_bullet(
        doc,
        "Led frontend development of a dynamic form builder that enabled users to create, configure, and distribute custom forms without engineering support.",
    )
    add_bullet(
        doc,
        "Designed reusable form components and workflows for dynamic configuration, validation, publishing, and form management.",
    )

    # IPC
    add_job_header(
        doc,
        "Frontend Engineer, Independent Purchasing Company – Africa",
        "Nov 2022 – Mar 2025",
        usable_dxa,
    )
    add_location(doc, "Lagos, Nigeria")
    add_tools(doc, "JavaScript, TypeScript, React.js, Vue.js, Nuxt.js, CSS, Tailwind CSS")

    add_product_heading(doc, "Daash — Inventory Management SaaS")
    add_bullet(
        doc,
        "Contributed to frontend engineering and product direction, overseeing frontend architecture, code quality, and product improvements.",
    )
    add_bullet(
        doc,
        "Implemented payment integrations supporting multiple payment methods and streamlined checkout workflows.",
    )

    add_product_heading(doc, "GoSource — B2B Food Procurement Platform")
    add_bullet(
        doc,
        "Led end-to-end frontend development across the customer web app, admin dashboard, and marketing website.",
    )
    add_bullet(
        doc,
        "Built procurement, checkout, payment, order management, and customer-facing workflows.",
    )
    add_bullet(
        doc,
        "Contributed to nearly $70K in revenue within two months and a 3x increase in customer growth and retention through iterative product improvements.",
    )
    add_bullet(
        doc,
        "Scaled the engineering team from 3 to 10, establishing code review, documentation, and mentorship practices.",
    )

    add_product_heading(doc, "Papa’s Grill — Ordering and Admin Platform")
    add_bullet(
        doc,
        "Contributed to the development of Papa’s Grill marketing website, procurement platform, and admin dashboard, which led to a 50%+ increase in profitability through improved customer experience and ordering workflows.",
    )
    add_bullet(
        doc,
        "Helped acquire more than 1,000 users during the first month after launch.",
    )

    # Other products
    add_section_heading(doc, "OTHER PRODUCTS AND COLLABORATIONS")

    add_job_header(doc, "Frontend Engineer, PostHearts", "Apr 2025 – Dec 2025", usable_dxa)
    add_location(doc, "Lagos, Nigeria")
    add_tools(doc, "JavaScript, TypeScript, React.js, Next.js, CSS, Tailwind CSS")
    add_product_heading(doc, "PostHearts — Digital Letter-Making Platform")
    add_bullet(
        doc,
        "Built React frontend experiences for PostHearts, developing an interactive letter editor with typography, backgrounds, photos, stickers, emojis, and responsive content creation workflows.",
    )
    add_bullet(
        doc,
        "Implemented responsive creation and sharing experiences, integrated product APIs, and collaborated with design and engineering to ship polished, production-ready features across web and mobile.",
    )

    add_job_header(doc, "Frontend Engineer, Quality", "Aug 2025 – Present", usable_dxa)
    add_location(doc, "Lagos, Nigeria")
    add_tools(doc, "JavaScript, TypeScript, React.js, Next.js, CSS, Tailwind CSS")
    add_product_heading(doc, "Quality — Real-Time Feedback Platform")
    add_bullet(
        doc,
        "Contributed to Quality, a real-time feedback platform for team collaboration and feedback management.",
    )
    add_bullet(
        doc,
        "Built responsive Next.js interfaces, reusable React components, and micro-interactions for core workflows.",
    )
    add_bullet(
        doc,
        "Integrated REST APIs and real-time features, collaborating with product and engineering teams to ship production-ready features.",
    )

    # Skills
    add_section_heading(doc, "SKILLS")
    add_skill_line(
        doc,
        "Product & Engineering",
        "Product Development  ·  Feature Ownership  ·  Frontend Architecture  ·  Component Architecture  ·  Technical Collaboration  ·  API Integration  ·  Performance Optimization  ·  Technical Problem Solving  ·  Cross-functional Collaboration  ·  Code Review",
    )
    add_skill_line(
        doc,
        "Frontend",
        "React.js  ·  Next.js  ·  Vue.js  ·  Nuxt.js  ·  TypeScript  ·  JavaScript  ·  HTML5  ·  CSS3  ·  Tailwind CSS  ·  Sass",
    )
    add_skill_line(
        doc,
        "APIs & Architecture",
        "REST APIs  ·  WebSockets  ·  State Management  ·  Responsive Design",
    )
    add_skill_line(
        doc,
        "Testing & Tools",
        "Jest  ·  Unit Testing  ·  Integration Testing  ·  API Testing  ·  Git  ·  GitHub  ·  Postman  ·  Figma  ·  Jira  ·  Vite",
    )
    add_skill_line(
        doc,
        "Deployment",
        "Vercel  ·  Netlify  ·  Railway  ·  CI/CD",
    )

    # Education
    add_section_heading(doc, "EDUCATION")
    add_job_header(
        doc,
        "B.Eng. Electrical and Electronics Engineering — First Class Honours",
        "2018 – 2023",
        usable_dxa,
    )
    add_location(
        doc,
        "Olusegun Agagu University of Science and Technology (OAUSTECH), Nigeria",
    )

    out = "/Users/acumenmac/Documents/codebase/personal/portfolio/Christian_Anyikamadu_CV.docx"
    doc.save(out)
    print(out)


if __name__ == "__main__":
    build()
