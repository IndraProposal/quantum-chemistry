#!/usr/bin/env python3
"""
build_academy_cv.py — Generates tailored 1-page executive CV for OpenAI
Role: Academy Partnerships Lead / Associate (Global Affairs)
Location: San Francisco, CA (Hybrid / On-site)
Strategic Angle: End-to-end partner portfolio (Academy Jams, Community Trainer Program) & partner ops automation
Paradigm: 6-Month Partner Ops Automation Arc & Operator-Educator
Linear Ticket: MIN-212
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

def build_pdf(output_pdf="cv-pavel-cherkashin-academy.pdf", output_png="cv-pavel-cherkashin-academy-hd.png"):
    pdf_dir = os.path.dirname(os.path.abspath(output_pdf))
    if pdf_dir:
        os.makedirs(pdf_dir, exist_ok=True)
    
    # Letter is 612 x 792 pt
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        leftMargin=34,
        rightMargin=34,
        topMargin=24,
        bottomMargin=20,
    )
    
    usable_width = 612 - 68  # 544 pt
    
    # Palette tailored to OpenAI & Global Affairs
    c_primary = colors.HexColor("#0F172A")    # Deep Slate
    c_oai = colors.HexColor("#10A37F")        # OpenAI Emerald Green
    c_navy = colors.HexColor("#0F766E")       # Deep Teal
    c_body = colors.HexColor("#1E293B")       # Dark Charcoal
    c_muted = colors.HexColor("#475569")      # Muted Slate
    c_bg = colors.HexColor("#F8FAFC")         # Clean Light Slate
    c_border = colors.HexColor("#CBD5E1")     # Light border
    
    base_styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18.5,
        leading=20.5,
        textColor=c_primary,
        spaceAfter=1.5
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.0,
        leading=11.2,
        textColor=c_oai,
        spaceAfter=2.0
    )
    
    contact_style = ParagraphStyle(
        'DocContact',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=8.1,
        leading=10.2,
        textColor=c_muted,
        spaceAfter=3.0
    )
    
    hero_style = ParagraphStyle(
        'HeroText',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=8.0,
        leading=10.8,
        textColor=c_primary,
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.9,
        leading=11.2,
        textColor=c_navy,
        spaceBefore=3.0,
        spaceAfter=1.8
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.7,
        leading=10.2,
        textColor=c_body,
    )
    
    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.7,
        leading=10.1,
        textColor=c_body,
        leftIndent=8,
        firstLineIndent=-8,
    )

    story = []
    
    # 1. Header
    story.append(Paragraph("PAVEL CHERKASHIN", title_style))
    story.append(Paragraph("Academy Partnerships Lead &bull; Global Affairs &bull; Partner Portfolio &amp; Ops Automation", subtitle_style))
    story.append(Paragraph("San Francisco, CA (Hybrid / Relocation) &nbsp;|&nbsp; pavel@mindrock.capital &nbsp;|&nbsp; linkedin.com/in/pavelcherkashin &nbsp;|&nbsp; github.com/minutta", contact_style))
    
    # 2. Hero Callout Box
    hero_p = Paragraph(
        "<b>Operating Thesis:</b> <i>\"Empowering grassroots builders, educational institutions, and civil society worldwide through accessible frontier AI. Scaling OpenAI Academy partner programs—from high-energy Academy Jams to train-the-trainer Community Trainer cohorts—while building automated operational infrastructure (intake pipelines, API credit allocation, impact telemetry, and curriculum distribution) that multiplies partner impact without administrative bloat.\"</i>",
        hero_style
    )
    hero_table = Table([[hero_p]], colWidths=[usable_width])
    hero_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg),
        ('BOX', (0,0), (-1,-1), 0.75, c_border),
        ('LINELEFT', (0,0), (-1,-1), 3.0, c_oai),
        ('TOPPADDING', (0,0), (-1,-1), 3.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.0),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(hero_table)
    story.append(Spacer(1, 2.5))
    
    # 3. Strategic Alignment: Global Affairs & Academy Ecosystem
    story.append(Paragraph("STRATEGIC FOCUS: GLOBAL AFFAIRS &amp; SCALABLE ACADEMY ECOSYSTEMS", section_title_style))
    thesis_text = (
        "OpenAI Academy serves as a cornerstone of OpenAI's Global Affairs mission: democratizing access to frontier intelligence by investing directly in developers, educators, and organizations solving local challenges in low- and middle-income regions. Sustainable ecosystem expansion requires more than transactional credit grants; it demands an end-to-end partner operating framework. As a published university textbook author, mentor to 5,000+ founders and students, former regional technology executive across Eastern Europe/CIS, and builder of autonomous agent swarms, I bridge high-level policy objectives with rigorous operational execution. I translate institutional partnerships into vibrant community-led builder ecosystems that advance economic opportunity, educational equity, and responsible AI adoption."
    )
    story.append(Paragraph(thesis_text, body_style))
    story.append(Spacer(1, 2.5))
    
    # 4. The 6-Month Partner Ops Automation Arc
    story.append(Paragraph("THE 6-MONTH PARTNER OPS AUTOMATION ARC (OPERATIONAL PRIORITIES &amp; MILESTONES)", section_title_style))
    
    arc_data = [
        [
            Paragraph("<b>Months 1–2</b><br/><font color='#10A37F'><b>Architecture &amp; Onboarding</b></font>", ParagraphStyle('H1', parent=body_style, fontName='Helvetica-Bold', fontSize=7.6, leading=9.2)),
            Paragraph("<b>Partner Portfolio Blueprint &amp; Automated Intake:</b> Map partner tiers across universities, NGOs, and developer collectives. Establish automated partner onboarding pipelines: application triage, API credit allocation, verification (KYA/sanctions compliance), and kickoff cadences. Launch initial pilot series of localized Academy Jams with regional university partners.", body_style)
        ],
        [
            Paragraph("<b>Months 3–4</b><br/><font color='#10A37F'><b>Community Trainers &amp; Scale</b></font>", ParagraphStyle('H2', parent=body_style, fontName='Helvetica-Bold', fontSize=7.6, leading=9.2)),
            Paragraph("<b>Community Trainer Program &amp; Mentorship Mesh:</b> Roll out standardized train-the-trainer cohorts to empower local professors, tech hubs, and NGO leads. Implement mentorship-matching workflows connecting OpenAI research/engineering volunteers with partner initiatives. Deliver multi-regional Academy Jams supporting grassroots problem-solving.", body_style)
        ],
        [
            Paragraph("<b>Months 5–6</b><br/><font color='#10A37F'><b>Telemetry &amp; Product Loops</b></font>", ParagraphStyle('H3', parent=body_style, fontName='Helvetica-Bold', fontSize=7.6, leading=9.2)),
            Paragraph("<b>Partner Impact Telemetry &amp; Codified Playbooks:</b> Deploy real-time partner dashboards tracking project completion, developer engagement, and local economic impact. Synthesize partner learnings directly into OpenAI product roadmaps and Global Affairs policy briefings. Hand off automated operational playbooks to regional teams for self-driving scale.", body_style)
        ],
    ]
    arc_table = Table(arc_data, colWidths=[92, usable_width - 92])
    arc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, colors.HexColor("#E2E8F0")),
    ]))
    story.append(arc_table)
    story.append(Spacer(1, 2.5))
    
    # 5. Core Execution Capabilities
    story.append(Paragraph("CORE PARTNERSHIP &amp; OPERATIONAL CAPABILITIES", section_title_style))
    cap_data = [
        [
            Paragraph("&bull; <b>End-to-End Partner Lifecycle:</b> Managing institutional relationships from discovery to contracting, program launch, impact measurement, and long-term cohort expansion.", bullet_style),
            Paragraph("&bull; <b>Academy Jams &amp; Hackathons:</b> Designed and hosted dozens of hands-on builder hackathons, developer showcases, and sprint competitions across international ecosystems.", bullet_style),
        ],
        [
            Paragraph("&bull; <b>Community Trainer Scaling:</b> Author of university curricula; experienced in designing train-the-trainer frameworks that empower local educators to scale knowledge exponentially.", bullet_style),
            Paragraph("&bull; <b>Partner Ops Automation:</b> Architect of autonomous multi-agent pipelines; automating credit distribution, partner milestone telemetry, and regulatory compliance reporting.", bullet_style),
        ]
    ]
    cap_table = Table(cap_data, colWidths=[usable_width/2.0, usable_width/2.0])
    cap_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(cap_table)
    story.append(Spacer(1, 2.5))
    
    # 6. Selected Track Record: Operator-Educator
    story.append(Paragraph("SELECTED CAREER TRACK RECORD &amp; INSTITUTIONAL LEADERSHIP", section_title_style))
    
    story.append(Paragraph("<b>Managing Partner &amp; Ecosystem Architect</b> &mdash; <i>Mindrock Capital / Vestor.In</i> (2016–Present)", ParagraphStyle('Exp1', parent=body_style, fontName='Helvetica-Bold', fontSize=7.9, leading=9.8)))
    story.append(Paragraph("&bull; Orchestrated strategic partnerships and deployed $100M+ across frontier technology ventures. Architected AI-native operational automation systems that slashed administrative friction for international partner networks.", bullet_style))
    story.append(Spacer(1, 1.8))
    
    story.append(Paragraph("<b>Author &amp; Educator</b> &mdash; <i>Venture Capital &amp; Entrepreneurship University Textbook</i>", ParagraphStyle('Exp2', parent=body_style, fontName='Helvetica-Bold', fontSize=7.9, leading=9.8)))
    story.append(Paragraph("&bull; Authored authoritative, voice-driven university textbook utilized in business schools across Eastern Europe. Designed experiential pedagogy and case studies empowering students, educators, and first-time founders.", bullet_style))
    story.append(Spacer(1, 1.8))

    story.append(Paragraph("<b>Investment Lead &amp; Mentor</b> &mdash; <i>Founder Institute Alumnus (2014) &amp; Decile Start Fund</i>", ParagraphStyle('Exp3', parent=body_style, fontName='Helvetica-Bold', fontSize=7.9, leading=9.8)))
    story.append(Paragraph("&bull; Conducted 5,000+ deep-dive founder and educator evaluations; structured regional accelerator pipelines in San Francisco bridging global emerging market talent with Silicon Valley resources and mentors.", bullet_style))
    story.append(Spacer(1, 1.8))
    
    story.append(Paragraph("<b>Regional Country Manager &amp; Director</b> &mdash; <i>Enterprise Technology &amp; Regional Operations</i>", ParagraphStyle('Exp4', parent=body_style, fontName='Helvetica-Bold', fontSize=7.9, leading=9.8)))
    story.append(Paragraph("&bull; Led regional market operations across Russia &amp; CIS; negotiated collaborative programs with university computer science departments, government innovation agencies, and national developer communities.", bullet_style))
    story.append(Spacer(1, 3.0))
    
    # 7. Education & Global Footprint
    story.append(Paragraph("EDUCATION, GLOBAL ECOSYSTEMS &amp; CREDENTIALS", section_title_style))
    edu_text = (
        "&bull; <b>Quantitative Foundation &amp; Systems:</b> Applied Mathematics &amp; Computer Science, Russian State University of Oil &amp; Gas.<br/>"
        "&bull; <b>Global Accelerator Alumnus &amp; Ecosystem:</b> Founder Institute (Silicon Valley Alumnus, 2014) &amp; Decile Start Fund Investment Lead.<br/>"
        "&bull; <b>Languages &amp; Cross-Cultural Reach:</b> Fluent English, native Russian; deep educator, policymaker, and builder relationships across US, Europe, and Asia."
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
    out_pdf = sys.argv[1] if len(sys.argv) > 1 else "cv-pavel-cherkashin-academy.pdf"
    out_png = sys.argv[2] if len(sys.argv) > 2 else "cv-pavel-cherkashin-academy-hd.png"
    build_pdf(out_pdf, out_png)
