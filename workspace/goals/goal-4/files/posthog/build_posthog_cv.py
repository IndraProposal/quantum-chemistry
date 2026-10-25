#!/usr/bin/env python3
"""
build_posthog_cv.py — Generates tailored 1-page CV for PostHog
Role: Partnership Wrangler (Remote)
Company: PostHog (Open-source product analytics, remote-first)
Linear Ticket: MIN-217
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

def build_pdf(output_pdf="cv-pavel-cherkashin-posthog.pdf", output_png="cv-pavel-cherkashin-posthog-hd.png"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isabs(output_pdf) and not os.path.dirname(output_pdf):
        output_pdf = os.path.join(script_dir, output_pdf)
    if not os.path.isabs(output_png) and not os.path.dirname(output_png):
        output_png = os.path.join(script_dir, output_png)

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
    
    # Color palette tailored to PostHog (Deep Charcoal, PostHog Orange/Amber, Amber Tint, Warm Slate)
    c_primary = colors.HexColor("#111827")    # Deep Charcoal
    c_brand = colors.HexColor("#F54E00")      # PostHog Orange
    c_accent = colors.HexColor("#D97706")     # Amber / Warm Gold
    c_navy = colors.HexColor("#1F2937")       # Dark Slate
    c_body = colors.HexColor("#374151")       # Body Charcoal
    c_muted = colors.HexColor("#6B7280")      # Muted Gray
    c_bg = colors.HexColor("#FFF7ED")         # Warm Orange Tint
    c_border = colors.HexColor("#FED7AA")     # Soft Orange Border
    
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
        fontSize=7.4,
        leading=9.8,
        textColor=c_primary,
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.3,
        leading=10.5,
        textColor=c_brand,
        spaceBefore=2.2,
        spaceAfter=1.2
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.4,
        textColor=c_navy,
    )
    
    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.1,
        leading=9.2,
        textColor=c_body,
        leftIndent=8,
        firstLineIndent=-8,
    )

    story = []
    
    # 1. Header
    story.append(Paragraph("PAVEL CHERKASHIN", title_style))
    story.append(Paragraph("Partnership Wrangler (Remote) &bull; Commercial Partner Channels &bull; Systems Integration Ecosystems &bull; Developer Tooling", subtitle_style))
    story.append(Paragraph("San Francisco, CA (PT) / Remote &nbsp;|&nbsp; pavel@mindrock.capital &nbsp;|&nbsp; linkedin.com/in/pavelcherkashin &nbsp;|&nbsp; github.com/minutta &nbsp;|&nbsp; x.com/cherkashin", contact_style))
    
    # 2. Hero Callout Box
    hero_p = Paragraph(
        "<b>Operating Focus:</b> <i>\"Unlocking net-new commercial channels from the ground up for PostHog. Pragmatic, autonomous builder combining executive leadership in enterprise software distribution and partner alliances (Country Manager at Siebel Systems, Founder &amp; CEO of systems integration agency Sputnik Labs) with hands-on technical proficiency in modern APIs, data stacks, and developer tooling ecosystems. Grounded in enterprise software distribution models, agency partner incentives, and developer enablement to turn technical platforms into high-velocity revenue channels. Built for small autonomous teams, zero bureaucracy, and rapid execution.\"</i>",
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
    story.append(Spacer(1, 1.2))
    
    # 3. Core Capabilities
    story.append(Paragraph("CORE PARTNERSHIP, COMMERCIAL &amp; TECHNICAL CAPABILITIES", section_title_style))
    skills_text = (
        "&bull; <b>Ground-Up Channel Development:</b> Designing and executing partner-led commercial motions; establishing clear commercial terms, commission/referral frameworks, and co-selling workflows without administrative bloat.<br/>"
        "&bull; <b>Commercial Partner Models:</b> Structuring reseller frameworks, multi-tier referral models, and joint go-to-market alignment to streamline enterprise evaluation, procurement, and onboarding cycles.<br/>"
        "&bull; <b>Developer &amp; Platform Integrations:</b> Technical evaluation of integrations with modern developer platforms (e.g. Vercel, Supabase) and data stacks (ClickHouse, PostgreSQL), aligning developer utility with partner incentives.<br/>"
        "&bull; <b>Agency &amp; Implementation Ecosystems:</b> Direct systems integration domain expertise; designing practical, developer-oriented partner enablement and first-build technical verification workflows.<br/>"
        "&bull; <b>Commercial Agreement Architecture:</b> Drafting, contract structuring, multi-party revenue-share terms, and enterprise software distribution models with clear legal and operational boundaries."
    )
    story.append(Paragraph(skills_text, bullet_style))
    story.append(Spacer(1, 1.2))
    
    # 4. Relevant Experience
    story.append(Paragraph("PARTNERSHIP, COMMERCIAL &amp; SYSTEMS LEADERSHIP EXPERIENCE", section_title_style))
    
    # Mindrock Autonomous Agent Mesh / Venture
    mindrock_header = "<b>Mindrock Capital &amp; Autonomous Systems Mesh</b> &mdash; <i>Managing Partner &amp; Lead Architect</i> <font color='#6B7280'>| 2020 &ndash; Present</font>"
    story.append(Paragraph(mindrock_header, body_style))
    mindrock_bullets = (
        "&bull; Architected autonomous agent orchestration mesh (`fleetd`, Model Context Protocol integrations, Linear API, GitHub CI) connecting multi-agent developer workflows with zero manual overhead.<br/>"
        "&bull; Structured cross-ecosystem technical collaborations and commercial frameworks for AI infrastructure, data engineering, and developer tooling startups.<br/>"
        "&bull; Formulated enterprise software licensing terms, co-development agreements, and distribution models for autonomous systems."
    )
    story.append(Paragraph(mindrock_bullets, bullet_style))
    story.append(Spacer(1, 1.2))
    
    # Founder Institute / Decile Group
    fi_header = "<b>Founder Institute / Decile Group</b> &mdash; <i>Venture Partner &amp; Ecosystem Architect</i> <font color='#6B7280'>| 2018 &ndash; 2024</font>"
    story.append(Paragraph(fi_header, body_style))
    fi_bullets = (
        "&bull; Collaborated across accelerator cohorts and venture syndicates, advising B2B software founders on commercial channel strategy and enterprise sales.<br/>"
        "&bull; Advised early-stage software companies on infrastructure partner programs, developer ecosystem collaboration, and commercial alignment.<br/>"
        "&bull; Mentored founders on enterprise customer acquisition, partner agreement mechanics, and commercial distribution channels."
    )
    story.append(Paragraph(fi_bullets, bullet_style))
    story.append(Spacer(1, 1.2))
    
    # Sputnik Labs
    sputnik_header = "<b>Sputnik Labs</b> &mdash; <i>Founder &amp; Chief Executive</i> <font color='#6B7280'>| Enterprise Integration &amp; Implementation Agency</font>"
    story.append(Paragraph(sputnik_header, body_style))
    sputnik_bullets = (
        "&bull; Founded and led enterprise systems integration agency Sputnik Labs, managing implementation alliances with enterprise software vendors (Siebel, Oracle, Microsoft).<br/>"
        "&bull; Structured and managed enterprise software implementation contracts and delivery programs across premier banking and telecommunications clients.<br/>"
        "&bull; Authored publications and professional materials on enterprise customer automation, analytics, and data architectures."
    )
    story.append(Paragraph(sputnik_bullets, bullet_style))
    story.append(Spacer(1, 1.2))
    
    # Siebel Systems
    siebel_header = "<b>Siebel Systems</b> &mdash; <i>Country Manager &amp; Enterprise Solutions Director</i> <font color='#6B7280'>| Platform Alliances</font>"
    story.append(Paragraph(siebel_header, body_style))
    siebel_bullets = (
        "&bull; Directed regional customer solutions and systems integrator alliances, aligning implementation partners around the enterprise CRM product suite.<br/>"
        "&bull; Oversaw partner-led enterprise delivery and customer engagement frameworks across high-value accounts."
    )
    story.append(Paragraph(siebel_bullets, bullet_style))
    story.append(Spacer(1, 1.2))
    
    # 5. Education & Technical Foundations
    story.append(Paragraph("EDUCATION, FOUNDATIONS &amp; PARTNER CERTIFICATION PLAYBOOK", section_title_style))
    edu_text = (
        "&bull; <b>M.S. in Computer Science &amp; Applied Mathematics</b> &bull; Technical proficiencies: Python, TypeScript, SQL, Git, Model Context Protocol &bull; Publications on Enterprise CRM &amp; Automation Systems.<br/>"
        "&bull; <b>Partner Certification &amp; Enablement Playbook (First-Build Mandate):</b> Approaching PostHog's partner certification not as a legacy bureaucracy, but as a lean, developer-first first-build track: open-source reference implementations, ClickHouse/PostHog integration sandboxes, and self-serve technical verification badges."
    )
    story.append(Paragraph(edu_text, bullet_style))
    
    doc.build(story, canvasmaker=InvariantCanvas)
    
    # Verify layout and collisions
    verification = verify_layout_and_collisions(output_pdf)
    
    # Render 300 DPI HD PNG using PyMuPDF and Pillow
    doc_fitz = pymupdf.open(output_pdf)
    page = doc_fitz[0]
    # 300 DPI: zoom factor = 300 / 72 = 4.16666667
    zoom = 300 / 72
    mat = pymupdf.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    pix.save(output_png)
    doc_fitz.close()
    
    # Ensure explicit 300 DPI metadata on both images
    pix_img = Image.open(output_png)
    pix_img.save(output_png, dpi=(300, 300))
    
    standard_png = output_png.replace("-hd.png", ".png")
    if standard_png != output_png:
        pix_img.save(standard_png, dpi=(300, 300))
        
    # Auto-synchronize generated artifacts to workspace mirror if present
    mirror_candidates = [
        "workspace/goals/goal-4/files/posthog",
        "../workspace/goals/goal-4/files/posthog",
        "../../workspace/goals/goal-4/files/posthog"
    ]
    for mc in mirror_candidates:
        if os.path.exists(mc) and os.path.isdir(mc):
            abs_mc = os.path.abspath(mc)
            if abs_mc != os.path.abspath(pdf_dir or "."):
                import shutil
                shutil.copy2(output_pdf, os.path.join(abs_mc, os.path.basename(output_pdf)))
                shutil.copy2(output_png, os.path.join(abs_mc, os.path.basename(output_png)))
                if standard_png != output_png:
                    shutil.copy2(standard_png, os.path.join(abs_mc, os.path.basename(standard_png)))
            break

    return verification

if __name__ == "__main__":
    pdf_out = sys.argv[1] if len(sys.argv) > 1 else "cv-pavel-cherkashin-posthog.pdf"
    png_out = sys.argv[2] if len(sys.argv) > 2 else "cv-pavel-cherkashin-posthog-hd.png"
    result = build_pdf(pdf_out, png_out)
    print(f"Verified 1-page CV: {result}")
