#!/usr/bin/env python3
"""
build_oai_cv.py — Generates tailored 1-page executive CV for OpenAI
Role: Community Communications Lead (Product & Research Communications / Culture & Community Engagement)
Paradigm: 6-Month Comms Automation Arc & Operator-Storyteller
Linear Ticket: MIN-208
"""

import os
import sys
import io
import pypdf
import pymupdf  # fitz
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
        r = pymupdf.Rect(b[:4])
        if not page_rect.contains(r):
            out_of_bounds.append((i, r, b[4][:20]))
            
    # Check pairwise bounding box collisions
    overlaps = []
    tol = 0.5  # points tolerance
    for i in range(len(text_blocks)):
        r1 = pymupdf.Rect(text_blocks[i][:4])
        for j in range(i + 1, len(text_blocks)):
            r2 = pymupdf.Rect(text_blocks[j][:4])
            inter = r1 & r2
            if not inter.is_empty and inter.width > tol and inter.height > tol:
                overlaps.append((i, j, inter, text_blocks[i][4][:20], text_blocks[j][4][:20]))
                
    doc_fitz.close()
    
    return {
        "page_count": page_count,
        "total_text_blocks": len(text_blocks),
        "out_of_bounds_count": len(out_of_bounds),
        "text_overlap_count": len(overlaps),
        "overlaps": overlaps
    }

def build_pdf(output_pdf="cv-pavel-cherkashin-oai.pdf", output_png="cv-pavel-cherkashin-oai-hd.png"):
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
    
    # Palette tailored to OpenAI
    c_primary = colors.HexColor("#0F172A")    # Deep Slate
    c_oai = colors.HexColor("#10A37F")        # OpenAI Green / Emerald
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
        spaceAfter=2
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
        fontSize=8.2,
        leading=10.2,
        textColor=c_muted,
        spaceAfter=3.0
    )
    
    hero_style = ParagraphStyle(
        'HeroText',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=8.1,
        leading=10.8,
        textColor=c_primary,
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.0,
        leading=11.2,
        textColor=c_navy,
        spaceBefore=3.0,
        spaceAfter=1.8
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=8.1,
        leading=10.8,
        textColor=c_body,
    )
    
    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=8.1,
        leading=10.8,
        textColor=c_body,
        leftIndent=8,
        firstLineIndent=-8,
    )

    story = []
    
    # 1. Header
    story.append(Paragraph("PAVEL CHERKASHIN", title_style))
    story.append(Paragraph("Community Communications Lead &bull; Operator-Storyteller &bull; 6-Month Comms Automation Arc", subtitle_style))
    story.append(Paragraph("San Francisco, CA (Hybrid / Relocation) &nbsp;|&nbsp; pavel@mindrock.capital &nbsp;|&nbsp; linkedin.com/in/pavelcherkashin &nbsp;|&nbsp; github.com/minutta", contact_style))
    
    # 2. Hero Callout Box
    hero_p = Paragraph(
        "<b>Operating Thesis:</b> <i>\"Automating communications operations—story sourcing, editorial cadence, distribution reach, and sentiment telemetry—while fiercely preserving human judgment, cultural taste, trust, and authentic community voices. Bringing OpenAI products closer to everyday communities by propelling AI out of tech subcultures into mainstream culture (sports, music, design, food, fandoms) on a disciplined 6-month arc.\"</i>",
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
    story.append(Spacer(1, 3.5))
    
    # 3. Strategic Alignment: Bridging Products to Communities & Mainstream Culture
    story.append(Paragraph("STRATEGIC FOCUS: COMMUNITY-FIRST NARRATIVES &amp; CULTURAL CROSSOVER", section_title_style))
    thesis_text = (
        "OpenAI is at an inflection point: transitioning from developer novelty to essential everyday fabric across global society. True earned media is not won through dry product feature announcements, but by illuminating the human builders, small business owners, students, and creative communities whose lives are transformed by AI. As an operator-storyteller who has conducted 5,000+ deep founder interviews, authored university textbooks, spearheaded regional tech ecosystems, and built autonomous agent workflows, I align narrative strategy from campaign inception. I connect decentralized community stories into enduring cultural narratives—bridging technical precision with popular resonance across music, culinary arts, sports, and grassroots builder fandoms."
    )
    story.append(Paragraph(thesis_text, body_style))
    story.append(Spacer(1, 3.5))
    
    # 4. The 6-Month Comms Automation Arc
    story.append(Paragraph("THE 6-MONTH COMMS AUTOMATION ARC (OPERATIONAL PRIORITIES &amp; MILESTONES)", section_title_style))
    
    arc_data = [
        [
            Paragraph("<b>Months 1–2</b><br/><font color='#10A37F'><b>Sourcing &amp; Radar</b></font>", ParagraphStyle('H1', parent=body_style, fontName='Helvetica-Bold', fontSize=7.8, leading=9.6)),
            Paragraph("<b>Community Sourcing Engine &amp; Cultural Radar:</b> Deploy automated discovery pipelines to source high-impact builder, student, and small-business stories. Establish cultural listening radar across non-tech verticals (sports, music, industrial design, culinary arts). Codify authentic voice guidelines: human-first tone, zero corporate puffery, and strict technical accuracy on AI capabilities and boundaries.", body_style)
        ],
        [
            Paragraph("<b>Months 3–4</b><br/><font color='#10A37F'><b>Campaigns &amp; Voices</b></font>", ParagraphStyle('H2', parent=body_style, fontName='Helvetica-Bold', fontSize=7.8, leading=9.6)),
            Paragraph("<b>Cultural Campaigns, Earned Attention &amp; Regional Hubs:</b> Execute sustained multi-month narrative arcs moving AI into popular culture. Partner with regional comms teams to localize creator stories globally. Turn community participation into the core story through interactive campaigns, earned media features, and trusted spokesperson representation for community-led initiatives.", body_style)
        ],
        [
            Paragraph("<b>Months 5–6</b><br/><font color='#10A37F'><b>Systems &amp; Hand-Off</b></font>", ParagraphStyle('H3', parent=body_style, fontName='Helvetica-Bold', fontSize=7.8, leading=9.6)),
            Paragraph("<b>Codified Editorial Architecture &amp; Product Feedback Loops:</b> Codify editorial calendars, rapid-response playbooks, and sentiment dashboards into repeatable automated workflows. Embed bi-directional community feedback loops directly into OpenAI product and research roadmaps. Hand off daily execution to regional leads and autonomous monitoring systems, transitioning into ongoing advisory.", body_style)
        ],
    ]
    arc_table = Table(arc_data, colWidths=[92, usable_width - 92])
    arc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, colors.HexColor("#E2E8F0")),
    ]))
    story.append(arc_table)
    story.append(Spacer(1, 3.5))
    
    # 5. Core Execution Capabilities
    story.append(Paragraph("CORE COMMUNICATIONS &amp; EXECUTION CAPABILITIES", section_title_style))
    cap_data = [
        [
            Paragraph("&bull; <b>Authentic Storytelling &amp; Voice:</b> Published university textbook author; essayist with sharp editorial judgment, turning dense technical abstractions into gripping human stories.", bullet_style),
            Paragraph("&bull; <b>Global Community Sourcing:</b> 5,000+ deep-dive founder conversations; managed Russia &amp; CIS regional operations; skilled at identifying and elevating authentic grassroots voices.", bullet_style),
        ],
        [
            Paragraph("&bull; <b>Cultural Crossover &amp; Earned Media:</b> Bridging frontier AI into mass culture—sports, fashion, music, design, culinary arts—securing earned attention beyond tech echo chambers.", bullet_style),
            Paragraph("&bull; <b>AI-Native Comms Operations:</b> Architect of autonomous multi-agent operational swarms; automated sentiment ingestion, KYA verification, and formal policy/SEC comment filings.", bullet_style),
        ]
    ]
    cap_table = Table(cap_data, colWidths=[usable_width/2.0, usable_width/2.0])
    cap_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(cap_table)
    story.append(Spacer(1, 3.5))
    
    # 6. Selected Track Record: Operator-Storyteller
    story.append(Paragraph("SELECTED CAREER TRACK RECORD &amp; NARRATIVE LEADERSHIP", section_title_style))
    
    story.append(Paragraph("<b>Managing Partner &amp; Chief Storyteller</b> &mdash; <i>Mindrock Capital / Vestor.In</i> (2016–Present)", ParagraphStyle('Exp1', parent=body_style, fontName='Helvetica-Bold', fontSize=8.0, leading=10.0)))
    story.append(Paragraph("&bull; Orchestrated narratives for $100M+ deployed in technology ventures. Pioneered AI-native communications and autonomous agent meshes, translating complex frontier algorithms into clear institutional narratives.", bullet_style))
    story.append(Spacer(1, 2.0))
    
    story.append(Paragraph("<b>Author &amp; Educator</b> &mdash; <i>Venture Capital &amp; Entrepreneurship University Textbook</i>", ParagraphStyle('Exp2', parent=body_style, fontName='Helvetica-Bold', fontSize=8.0, leading=10.0)))
    story.append(Paragraph("&bull; Authored authoritative, voice-driven university textbook utilized in business schools across Eastern Europe; focused entirely on practitioner voice, founder resilience, and community trust without vanity promotion.", bullet_style))
    story.append(Spacer(1, 2.0))

    story.append(Paragraph("<b>Decentralized Publishing &amp; Community Building</b> &mdash; <i>Nostr-First &amp; Cross-Cultural Campaigns</i>", ParagraphStyle('Exp3', parent=body_style, fontName='Helvetica-Bold', fontSize=8.0, leading=10.0)))
    story.append(Paragraph("&bull; Developed 30-day narrative distribution plans, multi-lingual campaign teasers (RU/EN/ZH), and the 'Serendipity Stalking' methodology. Mobilized decentralized communities across open protocols.", bullet_style))
    story.append(Spacer(1, 2.0))
    
    story.append(Paragraph("<b>Investment Lead &amp; Mentor</b> &mdash; <i>Founder Institute Alumnus (2014) &amp; Decile Start Fund</i>", ParagraphStyle('Exp4', parent=body_style, fontName='Helvetica-Bold', fontSize=8.0, leading=10.0)))
    story.append(Paragraph("&bull; Conducted 5,000+ founder interviews; mentored first-time creators and students on positioning, story architecture, and pitching; structured regional accelerator hubs in San Francisco bridging global founders with US partners.", bullet_style))
    story.append(Spacer(1, 3.5))
    
    # 7. Education & Global Community Footprint (Replaces internal mandate note)
    story.append(Paragraph("EDUCATION, GLOBAL ECOSYSTEMS &amp; CREDENTIALS", section_title_style))
    edu_text = (
        "&bull; <b>Quantitative Foundation &amp; Systems:</b> Applied Mathematics &amp; Computer Science, Russian State University of Oil &amp; Gas.<br/>"
        "&bull; <b>Global Accelerator Alumnus &amp; Ecosystem:</b> Founder Institute (Silicon Valley Alumnus, 2014) &amp; Decile Start Fund Investment Lead.<br/>"
        "&bull; <b>Languages &amp; Cross-Cultural Reach:</b> Fluent English, native Russian; deep creator, founder, and builder relationships across US, Europe, and Asia."
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
    out_pdf = sys.argv[1] if len(sys.argv) > 1 else "cv-pavel-cherkashin-oai.pdf"
    out_png = sys.argv[2] if len(sys.argv) > 2 else "cv-pavel-cherkashin-oai-hd.png"
    build_pdf(out_pdf, out_png)
