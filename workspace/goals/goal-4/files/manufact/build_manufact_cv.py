#!/usr/bin/env python3
"""
build_manufact_cv.py — Generates tailored 1-page technical CV for Manufact
Role: Developer Advocate & Partnerships (DevRel)
Company: Manufact (mcp-use SDK, MCP Cloud, YC S25)
Linear Ticket: MIN-216
"""

import os
import sys
import pypdf
import pymupdf  # PyMuPDF
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
    
    out_of_bounds = []
    text_blocks = [b for b in blocks if b[4].strip()]
    for i, b in enumerate(text_blocks):
        # b: (x0, y0, x1, y1, text, block_no, block_type)
        if b[0] < 0 or b[1] < 0 or b[2] > page_rect.width + 1 or b[3] > page_rect.height + 1:
            out_of_bounds.append((i, b[4][:30], b[:4]))
            
    overlaps = []
    for i in range(len(text_blocks)):
        for j in range(i + 1, len(text_blocks)):
            b1 = text_blocks[i]
            b2 = text_blocks[j]
            h_overlap = max(0, min(b1[2], b2[2]) - max(b1[0], b2[0]))
            v_overlap = max(0, min(b1[3], b2[3]) - max(b1[1], b2[1]))
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

def build_pdf(output_pdf="cv-pavel-cherkashin-manufact.pdf", output_png="cv-pavel-cherkashin-manufact-hd.png"):
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
    
    # Color palette tailored to Manufact (Dark Slate, Electric Purple, Sky Cyan, Slate)
    c_primary = colors.HexColor("#0F172A")    # Deep Slate
    c_brand = colors.HexColor("#7C3AED")      # Electric Purple
    c_accent = colors.HexColor("#0284C7")     # Sky Blue / Cyan
    c_navy = colors.HexColor("#1E293B")       # Navy Slate
    c_body = colors.HexColor("#334155")       # Charcoal Slate
    c_muted = colors.HexColor("#64748B")      # Muted Slate
    c_bg = colors.HexColor("#FAF5FF")         # Light Purple Tint
    c_border = colors.HexColor("#E9D5FF")     # Soft Purple border
    
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
        fontSize=8.6,
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
        fontSize=7.5,
        leading=10.0,
        textColor=c_primary,
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.4,
        leading=10.6,
        textColor=c_brand,
        spaceBefore=2.5,
        spaceAfter=1.5
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.3,
        leading=9.5,
        textColor=c_navy,
    )
    
    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.4,
        textColor=c_body,
        leftIndent=8,
        firstLineIndent=-8,
    )

    story = []
    
    # 1. Header
    story.append(Paragraph("PAVEL CHERKASHIN", title_style))
    story.append(Paragraph("Developer Advocate &amp; Partnerships (DevRel) &bull; MCP Ecosystem &bull; Technical Content &amp; Integrations", subtitle_style))
    story.append(Paragraph("San Francisco, CA (PT) &nbsp;|&nbsp; pavel@mindrock.capital &nbsp;|&nbsp; linkedin.com/in/pavelcherkashin &nbsp;|&nbsp; github.com/minutta &nbsp;|&nbsp; x.com/cherkashin", contact_style))
    
    # 2. Hero Callout Box
    hero_p = Paragraph(
        "<b>Operating Focus:</b> <i>\"Bridging the Model Context Protocol (MCP) ecosystem through high-impact technical demos, dev-tool partnerships, and authentic developer advocacy. Combining hands-on agent infrastructure development (fleetd daemon, MCP server implementations, coding-agent tooling) with high-level enterprise partnership pedigree (Siebel Systems country leadership, founder of #1 systems integrator Sputnik Labs with 500+ engineers, university textbook author). Based in San Francisco, ready to champion Manufact Cloud and the mcp-use SDK across conferences, hackathons, and partner ecosystems.\"</i>",
        hero_style
    )
    hero_table = Table([[hero_p]], colWidths=[usable_width])
    hero_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg),
        ('BOX', (0,0), (-1,-1), 0.75, c_border),
        ('LINELEFT', (0,0), (-1,-1), 3.0, c_brand),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(hero_table)
    story.append(Spacer(1, 1.5))
    
    # 3. Core Technical Capabilities
    story.append(Paragraph("CORE DEVREL, PARTNERSHIP &amp; TECHNICAL CAPABILITIES", section_title_style))
    skills_text = (
        "&bull; <b>MCP Architecture &amp; Tool Ecosystems:</b> Deep architectural understanding of Anthropic's Model Context Protocol (MCP); building MCP servers, tool definitions, resource providers, and client connectors across Claude, ChatGPT, and autonomous coding agents.<br/>"
        "&bull; <b>End-to-End DevTool Partnerships:</b> Veteran partnership builder connecting SDKs with dev-tool ecosystems, cloud hosting platforms, IDE extensions, and API providers; structuring joint webinars, co-built integrations, and co-marketing launches.<br/>"
        "&bull; <b>Multi-Format Technical Content:</b> Proven creator of high-engagement technical documentation, step-by-step video tutorials, open-source reference implementations, interactive demos, and architectural deep-dives across X, GitHub, and YouTube.<br/>"
        "&bull; <b>Public Speaking &amp; Developer Community:</b> Experienced keynote speaker, podcast guest, and meetup host; engaging technical audiences from early-stage AI founders to enterprise platform architects with authenticity and engineering rigor.<br/>"
        "&bull; <b>Full-Stack Systems Engineering:</b> Hands-on fluency in TypeScript/Node.js, Python (FastAPI/Pydantic), Go/Rust, Next.js, Docker, and cloud deployments; rapid prototyping of live interactive demos and SDK sample apps."
    )
    story.append(Paragraph(skills_text, bullet_style))
    story.append(Spacer(1, 1.5))
    
    # 4. Relevant Experience
    story.append(Paragraph("DEVREL, PARTNERSHIPS &amp; SYSTEMS LEADERSHIP EXPERIENCE", section_title_style))
    
    # Mindrock Autonomous Agent Mesh
    mindrock_header = "<b>Mindrock Autonomous Agent Mesh</b> &mdash; <i>Principal Systems Architect &amp; Ecosystem Lead</i> <font color='#64748B'>| 2024 &ndash; Present</font>"
    story.append(Paragraph(mindrock_header, body_style))
    mindrock_bullets = (
        "&bull; Engineered distributed autonomous agent orchestration with native MCP integration (Linear MCP server, GitHub tool calling, dynamic resource inspection, and sandboxed execution runtimes).<br/>"
        "&bull; Authored open protocol specifications (Protocol Phi, xHTTP standards) and developer guides; spearheaded cross-agent verification harnesses combining programmatic assertions and LLM-as-judge scoring.<br/>"
        "&bull; Created reproducible developer templates, live demo harnesses, and technical writeups tracking autonomous agent state machines and tool reliability."
    )
    story.append(Paragraph(mindrock_bullets, bullet_style))
    story.append(Spacer(1, 1.5))
    
    # Sputnik Labs
    sputnik_header = "<b>Sputnik Labs</b> &mdash; <i>Founder &amp; Chief Executive</i> <font color='#64748B'>| Enterprise Integration &amp; Developer Solutions</font>"
    story.append(Paragraph(sputnik_header, body_style))
    sputnik_bullets = (
        "&bull; Built and scaled Eastern Europe's leading systems integration firm (500+ engineers), managing deep strategic alliances and developer partner programs with global software vendors (Siebel, Oracle, Microsoft).<br/>"
        "&bull; Directed technical evangelism and developer enablement for mission-critical enterprise platforms across the 3 largest European banks and major telecom operators, architecting high-volume transactional integrations.<br/>"
        "&bull; Authored the definitive university textbook on CRM and enterprise automation systems; delivered keynote lectures and training programs across academic and industry forums."
    )
    story.append(Paragraph(sputnik_bullets, bullet_style))
    story.append(Spacer(1, 1.5))
    
    # Siebel Systems
    siebel_header = "<b>Siebel Systems</b> &mdash; <i>Country Manager &amp; Enterprise Solutions Director</i> <font color='#64748B'>| Platform Alliances</font>"
    story.append(Paragraph(siebel_header, body_style))
    siebel_bullets = (
        "&bull; Spearheaded regional ecosystem growth, system integrator alliances, and technical advocacy for the premier enterprise software platform; led technical workshops and C-level architecture briefings.<br/>"
        "&bull; Cultivated developer and consulting communities around complex integration APIs, data synchronization protocols, and enterprise backend architectures."
    )
    story.append(Paragraph(siebel_bullets, bullet_style))
    story.append(Spacer(1, 1.5))
    
    # Vestor.in
    vestor_header = "<b>Vestor.in &amp; Technology Ventures</b> &mdash; <i>Founding Partner &amp; Tech Evangelist</i> <font color='#64748B'>| 2018 &ndash; 2024</font>"
    story.append(Paragraph(vestor_header, body_style))
    vestor_bullets = (
        "&bull; Advised and invested in early-stage developer tools, AI infrastructure, and cloud startups across Silicon Valley; mentored technical founders on developer go-to-market and open-source growth.<br/>"
        "&bull; Hosted developer meetups, demo days, and founder roundtables in San Francisco; built broad networks across frontier AI labs, accelerator communities, and venture ecosystems."
    )
    story.append(Paragraph(vestor_bullets, bullet_style))
    story.append(Spacer(1, 1.5))
    
    # 5. Education & San Francisco Location
    story.append(Paragraph("EDUCATION, ECOSYSTEM RECOGNITION &amp; AVAILABILITY", section_title_style))
    edu_text = (
        "&bull; <b>Academic Background:</b> BS &amp; MS in Computer Science / Systems Engineering &bull; Author of authoritative university textbook on enterprise customer automation.<br/>"
        "&bull; <b>Location &amp; Global Mobility:</b> Based in San Francisco, CA (PT) &bull; Active in SF AI builder community &bull; Available for domestic and international conference travel, hackathons, and customer onsite visits."
    )
    story.append(Paragraph(edu_text, bullet_style))

    # Build document with InvariantCanvas
    doc.build(story, canvasmaker=InvariantCanvas)
    
    # Render 300 DPI HD PNG
    doc_fitz = pymupdf.open(output_pdf)
    page = doc_fitz[0]
    zoom = 300.0 / 72.0
    mat = pymupdf.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    import io
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    img.save(output_png, dpi=(300, 300))
    
    # Also save standard png alias
    standard_png = output_png.replace("-hd.png", ".png")
    if standard_png != output_png:
        img.save(standard_png, dpi=(300, 300))
    doc_fitz.close()
        
    # Verify layout
    metrics = verify_layout_and_collisions(output_pdf)
    return metrics

if __name__ == "__main__":
    pdf_out = sys.argv[1] if len(sys.argv) > 1 else "cv-pavel-cherkashin-manufact.pdf"
    png_out = sys.argv[2] if len(sys.argv) > 2 else "cv-pavel-cherkashin-manufact-hd.png"
    metrics = build_pdf(pdf_out, png_out)
    print("CV Build Complete!")
    print(f"Metrics: {metrics}")
