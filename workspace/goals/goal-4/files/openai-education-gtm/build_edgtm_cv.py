#!/usr/bin/env python3
"""
build_edgtm_cv.py — Generates tailored 1-page executive CV for OpenAI
Role: Global Head of Education GTM
Location: San Francisco, CA (Hybrid / On-site)
Strategic Angle: Operator + Investor + Teacher; Education GTM system & team; Adobe 1.5M+ license landmark deal.
Linear Ticket: MIN-211
"""

import os
import sys
import io
import pypdf
import pymupdf  # PyMuPDF / fitz
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.pdfgen import canvas
from reportlab import rl_config

# Enforce deterministic byte-for-byte ReportLab PDF rendering
rl_config.invariant = 1

class InvariantCanvas(canvas.Canvas):
    """Custom ReportLab Canvas enforcing byte-level reproducible output."""
    def __init__(self, *args, **kwargs):
        kwargs['invariant'] = 1
        kwargs['pageCompression'] = 1
        super().__init__(*args, **kwargs)

def verify_layout_and_collisions(pdf_path):
    """
    Programmatically verifies:
    1. Single-page constraint (len == 1)
    2. Page boundary containment (all text blocks inside printable page rectangle)
    3. Pairwise text collisions between distinct text blocks
    """
    reader = pypdf.PdfReader(pdf_path)
    page_count = len(reader.pages)
    if page_count != 1:
        raise ValueError(f"CV is {page_count} pages; must be exactly 1 page!")

    doc_fitz = pymupdf.open(pdf_path)
    page = doc_fitz[0]
    page_rect = page.rect
    blocks = page.get_text("blocks")

    # Check text block containment
    out_of_bounds = []
    text_blocks = [b for b in blocks if b[4].strip()]
    for i, b in enumerate(text_blocks):
        # b: (x0, y0, x1, y1, text, block_no, block_type)
        if b[0] < 0 or b[1] < 0 or b[2] > page_rect.width + 1 or b[3] > page_rect.height + 1:
            out_of_bounds.append((i, b[4][:30], b[:4]))

    # Check pairwise vertical overlaps
    overlaps = []
    for i in range(len(text_blocks)):
        for j in range(i + 1, len(text_blocks)):
            b1 = text_blocks[i]
            b2 = text_blocks[j]
            # Check horizontal overlap
            h_overlap = max(0, min(b1[2], b2[2]) - max(b1[0], b2[0]))
            # Check vertical overlap
            v_overlap = max(0, min(b1[3], b2[3]) - max(b1[1], b2[1]))
            # Consider overlap if significant area intersects
            if h_overlap > 15 and v_overlap > 3.0:
                overlaps.append({
                    "b1": b1[4][:30].strip(),
                    "b2": b2[4][:30].strip(),
                    "h_overlap": round(h_overlap, 1),
                    "v_overlap": round(v_overlap, 1)
                })

    doc_fitz.close()
    return {
        "page_count": page_count,
        "total_text_blocks": len(text_blocks),
        "text_overlap_count": len(overlaps),
        "out_of_bounds_count": len(out_of_bounds),
        "overlaps": overlaps,
        "out_of_bounds": out_of_bounds
    }

def build_pdf(output_pdf="cv-pavel-cherkashin-edgtm.pdf", output_png="cv-pavel-cherkashin-edgtm-hd.png"):
    pdf_dir = os.path.dirname(os.path.abspath(output_pdf))
    if pdf_dir:
        os.makedirs(pdf_dir, exist_ok=True)

    # Letter is 612 x 792 pt
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        leftMargin=34,
        rightMargin=34,
        topMargin=22,
        bottomMargin=18,
    )

    usable_width = 612 - 68  # 544 pt

    # Palette tailored to OpenAI & Global Education GTM
    c_primary = colors.HexColor("#0F172A")    # Deep Slate
    c_oai = colors.HexColor("#10A37F")        # OpenAI Emerald Green
    c_navy = colors.HexColor("#1E3A8A")       # Deep Navy / Academic Blue
    c_body = colors.HexColor("#1E293B")       # Dark Charcoal
    c_muted = colors.HexColor("#475569")      # Muted Slate
    c_bg = colors.HexColor("#F8FAFC")         # Clean Light Slate
    c_border = colors.HexColor("#CBD5E1")     # Light border

    base_styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18.0,
        leading=20.0,
        textColor=c_primary,
        spaceAfter=1.5
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.0,
        leading=11.0,
        textColor=c_oai,
        spaceAfter=2.0
    )

    contact_style = ParagraphStyle(
        'DocContact',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=8.0,
        leading=10.0,
        textColor=c_muted,
        spaceAfter=2.8
    )

    hero_style = ParagraphStyle(
        'HeroText',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.6,
        textColor=c_primary,
    )

    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.7,
        leading=11.0,
        textColor=c_navy,
        spaceBefore=2.8,
        spaceAfter=1.6
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=10.0,
        textColor=c_body,
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.8,
        textColor=c_body,
        leftIndent=8,
        firstLineIndent=-8,
    )

    story = []

    # 1. Header
    story.append(Paragraph("PAVEL CHERKASHIN", title_style))
    story.append(Paragraph("Global Head of Education GTM &bull; Institutional AI Licensing &bull; Operator &bull; Investor &bull; Educator", subtitle_style))
    story.append(Paragraph("San Francisco, CA (Hybrid / On-site) &nbsp;|&nbsp; pavel@mindrock.capital &nbsp;|&nbsp; linkedin.com/in/pavelcherkashin &nbsp;|&nbsp; github.com/minutta", contact_style))

    # 2. Hero Callout Box
    hero_p = Paragraph(
        "<b>Executive Thesis:</b> <i>\"Scaling OpenAI's education footprint from departmental pilots to pervasive campus and nationwide deployments. Rare combination of enterprise licensing executive (negotiated Adobe's largest global education transaction in corporate history: 1.5M+ Adobe CS licenses across national systems), venture investor ($100M+ deployed in frontier technology), and published university textbook author. Architecting high-velocity GTM systems, partner ecosystems, and sales teams that empower millions of students and educators while maintaining rigorous data privacy and governance.\"</i>",
        hero_style
    )
    hero_table = Table([[hero_p]], colWidths=[usable_width])
    hero_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg),
        ('BOX', (0,0), (-1,-1), 0.75, c_border),
        ('LINELEFT', (0,0), (-1,-1), 3.0, c_oai),
        ('TOPPADDING', (0,0), (-1,-1), 2.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.8),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(hero_table)
    story.append(Spacer(1, 2.0))

    # 3. Strategic Alignment: Global Education GTM Architecture
    story.append(Paragraph("STRATEGIC FOCUS: GLOBAL EDUCATION GTM SYSTEM &amp; TEAM LEADERSHIP", section_title_style))
    thesis_text = (
        "Education is OpenAI's most transformative enterprise frontier: converting universities, community colleges, and national ministries from cautious observers into campus-wide AI adopters. Sustainable education GTM requires solving complex institutional hurdles: procurement bureaucracy, strict data privacy standards (FERPA, GDPR, COPPA), administrative cost pressures, and faculty pedagogical alignment. Having scaled technology businesses as an operator, evaluated market economics as a venture capitalist, and taught in university lecture halls as a textbook author, I design GTM engines that pair consultative high-touch sales with automated campus enablement—positioning ChatGPT Edu as the indispensable cognitive infrastructure for learning and research."
    )
    story.append(Paragraph(thesis_text, body_style))
    story.append(Spacer(1, 2.0))

    # 4. The 6-Month Education GTM Acceleration Arc
    story.append(Paragraph("THE 6-MONTH EDUCATION GTM ACCELERATION ARC (OPERATIONAL MILESTONES)", section_title_style))

    arc_data = [
        [
            Paragraph("<b>Months 1–2</b><br/><font color='#10A37F'><b>Lighthouses &amp; Packaging</b></font>", ParagraphStyle('H1', parent=body_style, fontName='Helvetica-Bold', fontSize=7.4, leading=9.0)),
            Paragraph("<b>Enterprise Education Packaging &amp; Flagship Lighthouses:</b> Establish standardized, tiered commercial agreements for ChatGPT Edu (departmental, campus-wide, and research supercomputing tiers). Close initial lighthouse deals with top-tier research universities. Publish institutional governance playbooks addressing student data privacy, academic integrity, and FERPA compliance.", body_style)
        ],
        [
            Paragraph("<b>Months 3–4</b><br/><font color='#10A37F'><b>National &amp; Ministry Scale</b></font>", ParagraphStyle('H2', parent=body_style, fontName='Helvetica-Bold', fontSize=7.4, leading=9.0)),
            Paragraph("<b>Statewide &amp; Ministry Agreements (Adobe Deal Blueprint):</b> Replicate the 1.5M+ seat licensing model across state university systems and international ministries of education. Build a world-class education sales, solutions engineering, and customer success motion. Deploy education-specialized channel partners and systems integrators to accelerate institutional onboarding.", body_style)
        ],
        [
            Paragraph("<b>Months 5–6</b><br/><font color='#10A37F'><b>Curriculum &amp; Telemetry Loops</b></font>", ParagraphStyle('H3', parent=body_style, fontName='Helvetica-Bold', fontSize=7.4, leading=9.0)),
            Paragraph("<b>Autonomous Onboarding &amp; Academic Research Loops:</b> Implement automated administrative provisioning pipelines for 100k+ student campuses. Synthesize educator usage telemetry directly into OpenAI product roadmaps. Launch OpenAI Education Advisory Board connecting leading academic deans with OpenAI research leadership.", body_style)
        ],
    ]
    arc_table = Table(arc_data, colWidths=[90, usable_width - 90])
    arc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, colors.HexColor("#E2E8F0")),
    ]))
    story.append(arc_table)
    story.append(Spacer(1, 2.0))

    # 5. Core Capabilities Grid
    story.append(Paragraph("CORE EDUCATION GTM &amp; INSTITUTIONAL CAPABILITIES", section_title_style))
    cap_data = [
        [
            Paragraph("&bull; <b>Mega-Scale Enterprise Licensing:</b> Proven record closing 7- and 8-figure institutional agreements, multi-campus deployments, and government-backed educational frameworks.", bullet_style),
            Paragraph("&bull; <b>Campus AI Governance &amp; Compliance:</b> Deep command of student privacy (FERPA, GDPR, COPPA), enterprise security standards, data segregation, and AI safety protocols.", bullet_style),
        ],
        [
            Paragraph("&bull; <b>Pedagogical Innovation &amp; Academic Authority:</b> Published university textbook author with firsthand insight into curriculum design, faculty resistance, and student adoption dynamics.", bullet_style),
            Paragraph("&bull; <b>GTM Systems &amp; Autonomous Telemetry:</b> Architect of AI-native sales automation pipelines, automated license provisioning, and high-retention customer success systems.", bullet_style),
        ]
    ]
    cap_table = Table(cap_data, colWidths=[usable_width/2.0, usable_width/2.0])
    cap_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 1.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.0),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(cap_table)
    story.append(Spacer(1, 2.0))

    # 6. Selected Career Track Record
    story.append(Paragraph("SELECTED CAREER TRACK RECORD &amp; INSTITUTIONAL LEADERSHIP", section_title_style))

    story.append(Paragraph("<b>Regional Director &amp; Enterprise Licensing Executive</b> &mdash; <i>Adobe Systems / Enterprise Operations</i>", ParagraphStyle('Exp1', parent=body_style, fontName='Helvetica-Bold', fontSize=7.7, leading=9.5)))
    story.append(Paragraph("&bull; <b>Adobe Landmark Global Deal:</b> Spearheaded, negotiated, and closed the <b>largest global education transaction in Adobe's corporate history</b>, deploying <b>1.5M+ Adobe Creative Suite licenses</b> across regional academic networks and education ministries. Built the end-to-end institutional procurement framework, multi-tier reseller ecosystem, and teacher enablement programs.", bullet_style))
    story.append(Spacer(1, 1.5))

    story.append(Paragraph("<b>Managing Partner &amp; Ecosystem Architect</b> &mdash; <i>Mindrock Capital / Vestor.In</i> (2016–Present)", ParagraphStyle('Exp2', parent=body_style, fontName='Helvetica-Bold', fontSize=7.7, leading=9.5)))
    story.append(Paragraph("&bull; Directed enterprise technology investments and deployed $100M+ into frontier AI, compute infrastructure, and developer platforms. Built autonomous agent systems automating enterprise sales workflows, partner intake, and data telemetry.", bullet_style))
    story.append(Spacer(1, 1.5))

    story.append(Paragraph("<b>Author &amp; University Educator</b> &mdash; <i>Venture Capital &amp; Entrepreneurship University Textbook</i>", ParagraphStyle('Exp3', parent=body_style, fontName='Helvetica-Bold', fontSize=7.7, leading=9.5)))
    story.append(Paragraph("&bull; Authored authoritative, widely adopted university textbook used across business schools and computer science faculties. Designed experiential case pedagogy bridging frontier technology commercialization with academic curriculum.", bullet_style))
    story.append(Spacer(1, 1.5))

    story.append(Paragraph("<b>Global Accelerator Lead &amp; Mentor</b> &mdash; <i>Founder Institute Alumnus (2014) &amp; Decile Start Fund</i>", ParagraphStyle('Exp4', parent=body_style, fontName='Helvetica-Bold', fontSize=7.7, leading=9.5)))
    story.append(Paragraph("&bull; Evaluated and mentored 5,000+ university founders, researchers, and students. Established global university incubator pipelines connecting international academic talent with Silicon Valley capital and research ecosystems.", bullet_style))
    story.append(Spacer(1, 2.5))

    # 7. Education & Global Footprint
    story.append(Paragraph("EDUCATION, GLOBAL ECOSYSTEMS &amp; CREDENTIALS", section_title_style))
    edu_text = (
        "&bull; <b>Quantitative Foundation &amp; Systems:</b> Applied Mathematics &amp; Computer Science, Russian State University of Oil &amp; Gas.<br/>"
        "&bull; <b>Global Network &amp; Accelerator:</b> Founder Institute Silicon Valley Alumnus (2014); established relationships across US, European, and Asian universities.<br/>"
        "&bull; <b>Languages &amp; Cross-Cultural Reach:</b> Fluent English, native Russian; seasoned executive in cross-border institutional diplomacy."
    )
    story.append(Paragraph(edu_text, bullet_style))

    doc.build(story, canvasmaker=InvariantCanvas)

    # Programmatic Layout & Collision Verification
    report = verify_layout_and_collisions(output_pdf)
    print(f"Programmatic verification: page_count={report['page_count']}, text_blocks={report['total_text_blocks']}, collisions={report['text_overlap_count']}, out_of_bounds={report['out_of_bounds_count']}")

    if report['page_count'] != 1:
        raise ValueError(f"CV is {report['page_count']} pages; must be exactly 1 page!")
    if report['text_overlap_count'] != 0:
        raise ValueError(f"Found {report['text_overlap_count']} text collisions: {report['overlaps']}")
    if report['out_of_bounds_count'] != 0:
        raise ValueError(f"Found {report['out_of_bounds_count']} blocks out of bounds!")

    print(f"Successfully generated 1-page CV: {output_pdf}")

    # Export 300 DPI HD PNG
    if output_png:
        doc_fitz = pymupdf.open(output_pdf)
        page = doc_fitz[0]
        zoom = 300 / 72  # 300 DPI
        mat = pymupdf.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        img.save(output_png, dpi=(300, 300))
        png_size = os.path.getsize(output_png)
        print(f"Successfully generated 300 DPI HD PNG: {output_png} ({png_size} bytes, ~{png_size / (1024*1024):.2f} MB)")
        doc_fitz.close()

    return output_pdf, output_png

if __name__ == "__main__":
    out_pdf = sys.argv[1] if len(sys.argv) > 1 else "cv-pavel-cherkashin-edgtm.pdf"
    out_png = sys.argv[2] if len(sys.argv) > 2 else "cv-pavel-cherkashin-edgtm-hd.png"
    build_pdf(out_pdf, out_png)
