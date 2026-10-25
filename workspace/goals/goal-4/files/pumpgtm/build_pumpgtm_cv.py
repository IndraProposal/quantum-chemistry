#!/usr/bin/env python3
"""
build_pumpgtm_cv.py — Generates tailored 1-page technical CV for PumpGTM
Role: Full-Stack Engineer, GTM product
Company: PumpGTM (YC backed, pumpgtm.com)
Terms: 100% remote, paid 1-month trial, 6 days/week 9am-6pm PT, ship from day 1
Linear Ticket: MIN-214
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

def build_pdf(output_pdf="cv-pavel-cherkashin-pumpgtm.pdf", output_png="cv-pavel-cherkashin-pumpgtm-hd.png"):
    pdf_dir = os.path.dirname(os.path.abspath(output_pdf))
    if pdf_dir:
        os.makedirs(pdf_dir, exist_ok=True)
    
    # Letter is 612 x 792 pt
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        leftMargin=34,
        rightMargin=34,
        topMargin=20,
        bottomMargin=18,
    )
    
    usable_width = 612 - 68  # 544 pt
    
    # Color palette tailored to PumpGTM (Warm Coral / Tech Navy / Crisp Slate)
    c_primary = colors.HexColor("#0F172A")    # Deep Slate
    c_brand = colors.HexColor("#EA580C")      # Pump Coral / Flame
    c_navy = colors.HexColor("#1E3A8A")       # Enterprise Navy
    c_body = colors.HexColor("#1E293B")       # Dark Charcoal
    c_muted = colors.HexColor("#475569")      # Muted Slate
    c_bg = colors.HexColor("#FFF7ED")         # Warm Light Coral Tint
    c_border = colors.HexColor("#FED7AA")     # Warm border
    
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
        fontSize=8.8,
        leading=11.0,
        textColor=c_brand,
        spaceAfter=2.0
    )
    
    contact_style = ParagraphStyle(
        'DocContact',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.0,
        textColor=c_muted,
        spaceAfter=3.0
    )
    
    hero_style = ParagraphStyle(
        'HeroText',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=10.2,
        textColor=c_primary,
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10.8,
        textColor=c_navy,
        spaceBefore=2.5,
        spaceAfter=1.5
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.4,
        leading=9.6,
        textColor=c_body,
    )
    
    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.3,
        leading=9.5,
        textColor=c_body,
        leftIndent=8,
        firstLineIndent=-8,
    )

    story = []
    
    # 1. Header
    story.append(Paragraph("PAVEL CHERKASHIN", title_style))
    story.append(Paragraph("Full-Stack Systems Engineer &bull; GTM Product Architecture &bull; Outbound Automation", subtitle_style))
    story.append(Paragraph("San Francisco, CA (PT) &nbsp;|&nbsp; pavel@mindrock.capital &nbsp;|&nbsp; linkedin.com/in/pavelcherkashin &nbsp;|&nbsp; github.com/minutta &nbsp;|&nbsp; x.com/cherkashin", contact_style))
    
    # 2. Hero Callout Box
    hero_p = Paragraph(
        "<b>Operating Focus:</b> <i>\"Building resilient, full-stack GTM infrastructure that turns outbound signals into customer conversations. Grounded in foundational enterprise CRM architecture (Siebel Country Manager, Founder of #1 CRM integrator Eastern Europe, author of Russia's CRM textbook) paired with high-velocity modern full-stack shipping (TypeScript, React, Python, distributed agent meshes, and daily coding-agent fluency). 100% remote, 6 days/week 9am&ndash;6pm PT, shipping from Day 1.\"</i>",
        hero_style
    )
    hero_table = Table([[hero_p]], colWidths=[usable_width])
    hero_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg),
        ('BOX', (0,0), (-1,-1), 0.75, c_border),
        ('LINELEFT', (0,0), (-1,-1), 3.0, c_brand),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(hero_table)
    story.append(Spacer(1, 2.0))
    
    # 3. Core Technical Capabilities
    story.append(Paragraph("CORE TECHNICAL &amp; GTM PRODUCT CAPABILITIES", section_title_style))
    skills_text = (
        "&bull; <b>Outbound Multi-Channel Automation:</b> Architecting signal-to-sequence pipelines across LinkedIn, X, and Email; inbox reply aggregation, rate-limiting, sender reputation shielding, and webhook-driven event syncing.<br/>"
        "&bull; <b>Full-Stack Product Engineering:</b> Fluent development in TypeScript, React, Next.js, Node.js, and Python (FastAPI/Django); state management, interactive CRM tables, and resilient REST/GraphQL APIs.<br/>"
        "&bull; <b>High-Scale Data &amp; Queue Infrastructure:</b> PostgreSQL, Supabase, Redis queues, Celery/temporal job workflows, caching, and database query optimization for sub-second user queries under heavy load.<br/>"
        "&bull; <b>Autonomous Agent Meshes &amp; AI Workflows:</b> Architect of fleetd multi-agent daemon, slot concurrency (WIP=1), proactive backlog vacuuming, zero-trust git handoffs, and programmatic verification harnesses.<br/>"
        "&bull; <b>Frontier AI Coding Velocity:</b> Daily power user of Claude Code, Gemini CLI, Cursor, and OpenAI tool APIs; shipping clean, tested production code at extreme velocity with disciplined git workflows."
    )
    story.append(Paragraph(skills_text, bullet_style))
    story.append(Spacer(1, 2.0))
    
    # 4. Relevant Experience
    story.append(Paragraph("GTM PRODUCT &amp; SYSTEMS ENGINEERING EXPERIENCE", section_title_style))
    
    # Sputnik Labs
    sputnik_header = "<b>Sputnik Labs</b> &mdash; <i>Founder &amp; Chief Executive</i> <font color='#475569'>| Enterprise CRM &amp; Analytics</font>"
    story.append(Paragraph(sputnik_header, body_style))
    sputnik_bullets = (
        "&bull; Founded and scaled Eastern Europe's #1 CRM integration powerhouse (500+ professionals), designing customer data architectures, outbound sales automation, and enterprise marketing platforms.<br/>"
        "&bull; Led end-to-end CRM implementations for the 3 largest European banks and the third-largest mobile telecom operator, engineering real-time call-center analytics and high-volume customer pipeline engines.<br/>"
        "&bull; Authored the definitive Russian university textbook on CRM, establishing the foundational curriculum and enterprise practices for automated customer lifecycle management and sales workflows."
    )
    story.append(Paragraph(sputnik_bullets, bullet_style))
    story.append(Spacer(1, 2.0))
    
    # Siebel
    siebel_header = "<b>Siebel Systems</b> &mdash; <i>Country Manager &amp; Enterprise CRM Architect</i> <font color='#475569'>| Enterprise Systems</font>"
    story.append(Paragraph(siebel_header, body_style))
    siebel_bullets = (
        "&bull; Directed regional operations and enterprise solution architecture for the world's premier CRM software vendor; advised C-level executives on sales automation, pipeline hygiene, and multi-channel marketing infrastructure.<br/>"
        "&bull; Supervised complex system integrations connecting CRM backbones to distributed telecommunications switches, banking transactional databases, and legacy mainframes."
    )
    story.append(Paragraph(siebel_bullets, bullet_style))
    story.append(Spacer(1, 2.0))
    
    # Mindrock
    mindrock_header = "<b>Mindrock Autonomous Agent Mesh</b> &mdash; <i>Principal Systems Architect</i> <font color='#475569'>| 2024 &ndash; Present</font>"
    story.append(Paragraph(mindrock_header, body_style))
    mindrock_bullets = (
        "&bull; Built the monolithic fleetd daemon in Rust and Python, orchestrating concurrent autonomous coding agents across distributed nodes with proactive backlog vacuuming and zero-trust Git handoffs.<br/>"
        "&bull; Engineered real-time webhook dispatchers, Linear API connectors, and automated QA gates with programmatic layout verification and SHA-256 evidence sealing."
    )
    story.append(Paragraph(mindrock_bullets, bullet_style))
    story.append(Spacer(1, 2.0))
    
    # Vestor.in
    vestor_header = "<b>Vestor.in Distributed Deal Platform</b> &mdash; <i>Founding Architect</i> <font color='#475569'>| 2018 &ndash; 2024</font>"
    story.append(Paragraph(vestor_header, body_style))
    vestor_bullets = (
        "&bull; Built full-stack event-driven transaction platform managing $100M+ in deal volume, featuring automated investor-founder communication sequences, live portfolio dashboards, and sub-50ms API response times."
    )
    story.append(Paragraph(vestor_bullets, bullet_style))
    story.append(Spacer(1, 2.0))
    
    # 5. Operating Posture
    story.append(Paragraph("OPERATING POSTURE &amp; FOUNDER ALIGNMENT", section_title_style))
    posture_text = (
        "&bull; <b>High-Intensity Execution:</b> San Francisco-based (Pacific Time), committed to 6 days/week 9am&ndash;6pm PT schedule. Deep appreciation for YC work ethic and shipping rhythm.<br/>"
        "&bull; <b>Day-1 Autonomy:</b> Zero handholding required. Able to pull tickets from the backlog, diagnose full-stack bugs across frontend and backend, implement clean fixes, test thoroughly, and push PRs.<br/>"
        "&bull; <b>GTM Empathy:</b> Having built and sold enterprise CRM solutions for over two decades, I understand exactly why sales reps live in their inbox and what drives conversion in modern outbound sequences."
    )
    story.append(Paragraph(posture_text, bullet_style))
    story.append(Spacer(1, 2.0))
    
    # 6. Education
    story.append(Paragraph("EDUCATION &amp; FOUNDATION", section_title_style))
    edu_text = (
        "&bull; <b>B.S. / M.S. Applied Mathematics &amp; Computer Science:</b> Russian State University of Oil &amp; Gas (Systems programming, discrete mathematics, and quantitative algorithm design)."
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
    out_pdf = sys.argv[1] if len(sys.argv) > 1 else "cv-pavel-cherkashin-pumpgtm.pdf"
    out_png = sys.argv[2] if len(sys.argv) > 2 else "cv-pavel-cherkashin-pumpgtm-hd.png"
    build_pdf(out_pdf, out_png)
