#!/usr/bin/env python3
"""
build_tastelabs_cv.py — Generates tailored 1-page CV for Taste Labs
Role: AI Engineer, RL & Evals (Technical Staff)
Company: Taste Labs (tastelabs.com, Thais Castello Branco @thaiscbranco_)
Location: San Francisco, CA (SF on-site, full-time)
Linear Ticket: MIN-235
"""

import os
import sys
import shutil
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

def build_pdf(output_pdf="cv-pavel-cherkashin-tastelabs.pdf", output_png="cv-pavel-cherkashin-tastelabs-hd.png", sync_to_mirror=True):
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
        topMargin=18,
        bottomMargin=16,
    )
    
    usable_width = 612 - 68  # 544 pt
    
    # Refined palette tailored to Taste Labs (Midnight Obsidian, Indigo Violet Accent, Crisp Soft Tint)
    c_primary = colors.HexColor("#1E1B4B")    # Deep Midnight Indigo
    c_title = colors.HexColor("#0F172A")      # Rich Slate Black
    c_brand = colors.HexColor("#4338CA")      # Taste Indigo Brand
    c_accent = colors.HexColor("#6366F1")     # Vibrant Electric Indigo
    c_body = colors.HexColor("#1F2937")       # Charcoal Body
    c_muted = colors.HexColor("#475569")      # Muted Slate
    c_bg = colors.HexColor("#F5F3FF")         # Soft Violet/Lavender Tint
    c_border = colors.HexColor("#C7D2FE")     # Subtle Indigo Border
    
    base_styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=22,
        textColor=c_title,
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.2,
        leading=11.2,
        textColor=c_brand,
    )
    
    contact_style = ParagraphStyle(
        'ContactLine',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=c_muted,
        alignment=2,  # Right-aligned
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.3,
        leading=10.3,
        textColor=c_primary,
        spaceAfter=2,
        spaceBefore=3,
        borderPadding=(0, 0, 1, 0),
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.4,
        leading=9.3,
        textColor=c_body,
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.1,
        leading=8.9,
        textColor=c_body,
    )
    
    callout_style = ParagraphStyle(
        'Callout',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.1,
        leading=8.7,
        textColor=c_primary,
    )
    
    story = []
    
    # 1. Header (Name, Title, Contact)
    header_left = [
        Paragraph("<b>PAVEL CHERKASHIN</b>", title_style),
        Spacer(1, 2),
        Paragraph("TASTE LABS &mdash; AI ENGINEER, RL &amp; EVALS (TECHNICAL STAFF)", subtitle_style),
    ]
    header_right = [
        Paragraph("San Francisco, CA &bull; In-Person SF", contact_style),
        Paragraph("pavel@mindrock.capital &bull; linkedin.com/in/cherkashin", contact_style),
        Paragraph("github.com/pashamango &bull; @pashamango", contact_style),
    ]
    
    header_table = Table(
        [[header_left, header_right]],
        colWidths=[350, 194],
        style=[
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]
    )
    story.append(header_table)
    story.append(Spacer(1, 3))
    
    # 2. Executive Positioning Callout (Cracking Subjective Domains & Ending AI Slop)
    posture_text = (
        "<b>ROLE SEAT &amp; POSTURE:</b> Evals-focused systems architect applying rigorous empirical evaluation harnesses, decomposition grading, and "
        "multi-model taste rubrics to end &ldquo;AI slop&rdquo; in subjective domains. Targeting <b>AI Engineer, RL &amp; Evals</b> at Taste Labs to take "
        "end-to-end ownership of <b>grading methods &amp; rubrics, task design for taste, agent harnesses &amp; context layers, and deterministic evaluation gates</b>. "
        "<i>Transparent alignment:</i> deep strength in evals harnesses, rubrics decomposition, agent context layers, backend infrastructure, and data indexing; "
        "transparently recognizing scalable RL cluster infra and distributed training pipelines as an active growth edge rather than core depth."
    )
    posture_table = Table(
        [[Paragraph(posture_text, callout_style)]],
        colWidths=[usable_width],
        style=[
            ('BACKGROUND', (0,0), (-1,-1), c_bg),
            ('BOX', (0,0), (-1,-1), 0.75, c_border),
            ('TOPPADDING', (0,0), (-1,-1), 3.0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3.0),
            ('LEFTPADDING', (0,0), (-1,-1), 5.0),
            ('RIGHTPADDING', (0,0), (-1,-1), 5.0),
        ]
    )
    story.append(posture_table)
    story.append(Spacer(1, 3))
    
    # 3. Core Competencies Grid
    story.append(Paragraph("CORE COMPETENCIES &amp; TASTE EVALS ARCHITECTURE", section_title_style))
    col1 = [
        Paragraph("<b>Subjective Domain Evals &amp; Taste Rubrics</b>", ParagraphStyle('C1', parent=body_style, fontName='Helvetica-Bold', textColor=c_primary)),
        Paragraph("&bull; Decomposing design, tone &amp; aesthetics into granular, testable rubrics<br/>"
                  "&bull; Multi-model LLM-as-judge scoring &amp; pairwise Bradley-Terry Elo ranking<br/>"
                  "&bull; Held-out private verifiers to prevent reward hacking &amp; benchmark memorization<br/>"
                  "&bull; Empirical failure-mode taxonomies &amp; programmatic anti-slop boundary assertions", bullet_style),
        Spacer(1, 2),
        Paragraph("<b>Backend Infrastructure &amp; Data Pipelines</b>", ParagraphStyle('C2', parent=body_style, fontName='Helvetica-Bold', textColor=c_primary)),
        Paragraph("&bull; High-throughput distributed backends &amp; event-driven architecture<br/>"
                  "&bull; Deterministic test harnesses, isolated worktrees &amp; CI/CD verification gates<br/>"
                  "&bull; Tamper-evident cryptographic manifests (SHA-256) &amp; zero-trust verification<br/>"
                  "&bull; Large-scale dataset ingestion, feature extraction &amp; telemetry streaming", bullet_style),
    ]
    col2 = [
        Paragraph("<b>Agent Harnesses &amp; Context Layers</b>", ParagraphStyle('C3', parent=body_style, fontName='Helvetica-Bold', textColor=c_primary)),
        Paragraph("&bull; Autonomous agent runtime orchestration &amp; daemon architecture (<i>fleetd</i>)<br/>"
                  "&bull; Dynamic context layering, memory injection &amp; prompt state management<br/>"
                  "&bull; Model Context Protocol (MCP) tool integration &amp; sandbox isolation<br/>"
                  "&bull; Strict concurrency gating (WIP=1), state auditability &amp; crash recovery", bullet_style),
        Spacer(1, 2),
        Paragraph("<b>Technical Pedagogy &amp; Creative Systems</b>", ParagraphStyle('C4', parent=body_style, fontName='Helvetica-Bold', textColor=c_primary)),
        Paragraph("&bull; Published textbook author: <i>CRM Strategy</i> (INTUIT/BINOM, Moscow, 384 pp.)<br/>"
                  "&bull; Turning fuzzy human taste and design guidelines into structured engineering specs<br/>"
                  "&bull; Clear public benchmark documentation, research notes &amp; anti-gaming disclosures<br/>"
                  "&bull; Enterprise solution architecture, executive communication &amp; partner alignment", bullet_style),
    ]
    
    comp_table = Table(
        [[col1, col2]],
        colWidths=[268, 276],
        style=[
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 2),
            ('RIGHTPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 1),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ]
    )
    story.append(comp_table)
    story.append(Spacer(1, 3))
    
    # 4. Systems & Leadership Experience
    story.append(Paragraph("SYSTEMS &amp; LEADERSHIP EXPERIENCE", section_title_style))
    
    # Experience Entry 1: Mindrock Autonomous Agent Fleet
    exp1_title = Paragraph("<b>Mindrock Autonomous Agent Fleet</b> &mdash; <i>Principal Systems Architect &amp; Harness Builder</i>", ParagraphStyle('E1T', parent=body_style, fontName='Helvetica-Bold', fontSize=7.6, textColor=c_title))
    exp1_date = Paragraph("2024 &ndash; Present | San Francisco, CA", contact_style)
    story.append(Table([[exp1_title, exp1_date]], colWidths=[380, 164], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0)]))
    story.append(Paragraph(
        "&bull; <b>Agent Runtime Architecture:</b> Architect of <i>fleetd</i>, a monolithic daemon in Rust managing multi-agent concurrency, slot leasing (WIP=1), deterministic task dispatch, and autonomous backlog vacuum loops across distributed macOS nodes.<br/>"
        "&bull; <b>Deterministic Evals &amp; QA Gates:</b> Built Protocol Phi (&Phi;-0.1), establishing structured, tamper-evident handoffs and cross-agent evaluation loops between builder and independent QA agents, enforcing programmatic assertions before human gate review.<br/>"
        "&bull; <b>Multi-Model Verification &amp; Anti-Slop:</b> Engineered automated evaluation harnesses combining geometric layout assertions, multi-model consensus, and LLM-as-judge scoring, eliminating subjective drift, visual collisions, and synthetic hallucination.<br/>"
        "&bull; <b>Model Context Protocol (MCP):</b> Integrated native MCP servers with lazy schema resolution, sandboxed execution, and token-efficient tool streaming.",
        bullet_style
    ))
    story.append(Spacer(1, 2))
    
    # Experience Entry 2: Vestor.in & Venture Advisory
    exp2_title = Paragraph("<b>Vestor.in &amp; Technology Advisory</b> &mdash; <i>Founding Partner &amp; Systems Architect</i>", ParagraphStyle('E2T', parent=body_style, fontName='Helvetica-Bold', fontSize=7.6, textColor=c_title))
    exp2_date = Paragraph("2018 &ndash; 2024 | San Francisco, CA", contact_style)
    story.append(Table([[exp2_title, exp2_date]], colWidths=[380, 164], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0)]))
    story.append(Paragraph(
        "&bull; <b>Platform Architecture:</b> Designed high-concurrency event routing and data platforms for technology investments; evaluated early-stage AI architectures and product-market fit across generative AI, autonomous agents, and enterprise automation.<br/>"
        "&bull; <b>Startup Coaching &amp; Systems Strategy:</b> Advised founders on technical roadmap design, automated verification pipelines, and scalable backend infrastructure.",
        bullet_style
    ))
    story.append(Spacer(1, 2))
    
    # Experience Entry 3: Sputnik Labs
    exp3_title = Paragraph("<b>Sputnik Labs</b> &mdash; <i>Founder &amp; Chief Executive Officer</i> (Acquired by Technoserv, 2008)", ParagraphStyle('E3T', parent=body_style, fontName='Helvetica-Bold', fontSize=7.6, textColor=c_title))
    exp3_date = Paragraph("2001 &ndash; 2008 | Moscow &amp; European Hubs", contact_style)
    story.append(Table([[exp3_title, exp3_date]], colWidths=[380, 164], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0)]))
    story.append(Paragraph(
        "&bull; <b>Founding &amp; Enterprise Scale:</b> Founded and scaled the pioneering enterprise CRM and workflow systems integration firm in Eastern Europe; built engineering organization to 500+ employees and led successful acquisition by Technoserv.<br/>"
        "&bull; <b>Customer Rubrics &amp; Predictive Scoring:</b> Architected large-scale customer interaction rubrics, automated data indexing pipelines, and real-time behavioral scoring systems for tier-1 telecom and banking enterprises in strategic partnership with Siebel, Oracle, and Microsoft.",
        bullet_style
    ))
    story.append(Spacer(1, 2))
    
    # Experience Entry 4: Siebel Systems & Microsoft
    exp4_title = Paragraph("<b>Siebel Systems &amp; Microsoft</b> &mdash; <i>Country Manager, Russia &amp; CIS / Platform Strategy Director</i>", ParagraphStyle('E4T', parent=body_style, fontName='Helvetica-Bold', fontSize=7.6, textColor=c_title))
    exp4_date = Paragraph("1999 &ndash; 2006 | Regional Executive Roles", contact_style)
    story.append(Table([[exp4_title, exp4_date]], colWidths=[380, 164], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0)]))
    story.append(Paragraph(
        "&bull; <b>Platform Leadership:</b> Directed enterprise software platforms, developer evangelism, and integration architectures for mission-critical enterprise systems, establishing regional technology leadership and partner integration frameworks.",
        bullet_style
    ))
    story.append(Spacer(1, 3))
    
    # 5. Education & Published Author
    story.append(Paragraph("EDUCATION &amp; PUBLISHED AUTHOR", section_title_style))
    edu1_title = Paragraph("<b>Lomonosov Moscow State University (MSU)</b> &mdash; <i>B.S. in Computer Science in Global Ecology</i>", ParagraphStyle('ED1', parent=body_style, fontName='Helvetica-Bold', fontSize=7.6, textColor=c_title))
    edu1_date = Paragraph("1995 | Moscow, RU", contact_style)
    story.append(Table([[edu1_title, edu1_date]], colWidths=[380, 164], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0)]))
    story.append(Paragraph(
        "&bull; Mathematical modeling, computational data structures, satellite telemetry analysis. Research fellowship at the International Institute for Applied Systems Analysis (IIASA, Laxenburg, Austria, 1994&ndash;1995).",
        bullet_style
    ))
    story.append(Spacer(1, 2))
    
    pub_title = Paragraph("<b>Published University Textbook:</b> <i>Customer Relationship Management Strategy</i> (*Стратегия управления взаимоотношениями с клиентами (CRM)*)", ParagraphStyle('PUB', parent=body_style, fontName='Helvetica-Bold', fontSize=7.5, textColor=c_brand))
    story.append(pub_title)
    story.append(Paragraph(
        "&bull; INTUIT / BINOM, Moscow, 2007, 384 pp., <b>ISBN 978-5-94774-643-3</b>. Cataloged in the Russian State Library (RSL Official Record: <code>01003185368</code>). Definitive academic text on automated customer data modeling, enterprise rubrics, and systematic interaction design.",
        bullet_style
    ))
    
    # Build Document
    doc.build(story, canvasmaker=InvariantCanvas)
    
    # Verify Layout and Collisions
    metrics = verify_layout_and_collisions(output_pdf)
    print(f"Layout Verification: {metrics}")
    
    # Generate High-Resolution PNG via PyMuPDF and Pillow
    doc_fitz = pymupdf.open(output_pdf)
    page = doc_fitz[0]
    pix = page.get_pixmap(dpi=300)
    pix.save(output_png)
    doc_fitz.close()
    
    # Ensure exact 300 DPI metadata in image file
    im = Image.open(output_png)
    im.save(output_png, dpi=(300, 300))
    
    # Standard PNG alias
    base_png = output_png.replace("-hd.png", ".png")
    if base_png != output_png:
        shutil.copy2(output_png, base_png)
        
    print(f"Generated: {output_pdf} and {output_png} (300 DPI)")
    
    if sync_to_mirror:
        # Sync to repo workspace goals mirror and system workspace goals mirror
        mirrors = [
            os.path.join(script_dir, "..", "workspace", "goals", "goal-4", "files", "tastelabs"),
            os.path.expanduser("~/workspace/goals/goal-4/files/tastelabs"),
        ]
        for m in mirrors:
            m_abs = os.path.abspath(m)
            if os.path.exists(m_abs) and m_abs != script_dir:
                for fname in [os.path.basename(output_pdf), os.path.basename(output_png), os.path.basename(base_png)]:
                    src = os.path.join(script_dir, fname)
                    dst = os.path.join(m_abs, fname)
                    if os.path.exists(src):
                        shutil.copy2(src, dst)
                        print(f"Synced {fname} to {m_abs}")

if __name__ == "__main__":
    out_pdf = "cv-pavel-cherkashin-tastelabs.pdf"
    out_png = "cv-pavel-cherkashin-tastelabs-hd.png"
    if len(sys.argv) > 1:
        out_pdf = sys.argv[1]
    if len(sys.argv) > 2:
        out_png = sys.argv[2]
    build_pdf(out_pdf, out_png)
