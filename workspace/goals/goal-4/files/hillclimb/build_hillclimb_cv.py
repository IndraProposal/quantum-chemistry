#!/usr/bin/env python3
"""
build_hillclimb_cv.py — Generates tailored 1-page CV for Hillclimb AI
Role: Employee #5 — Evals & Environments for RSI (Evals Research & Writing Lead)
Company: Hillclimb AI (@hillclimbai, Jun Park @jparkjmc, Ibrakhim Ustelbay)
Location: San Francisco, CA (In-Person SF)
Linear Ticket: MIN-222
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

def build_pdf(output_pdf="cv-pavel-cherkashin-hillclimb.pdf", output_png="cv-pavel-cherkashin-hillclimb-hd.png"):
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
    
    # Color palette tailored to Hillclimb AI (Deep Forest Slate, Emerald Accent, Crisp White/Mint tint)
    c_primary = colors.HexColor("#064E3B")    # Deep Forest Pine
    c_title = colors.HexColor("#0F172A")      # Near Black Slate
    c_brand = colors.HexColor("#0D7A5F")      # Hillclimb Mountain Jade
    c_accent = colors.HexColor("#059669")     # Vibrant Emerald
    c_body = colors.HexColor("#1E293B")       # Dark Charcoal
    c_muted = colors.HexColor("#475569")      # Muted Slate
    c_bg = colors.HexColor("#F0FDF4")         # Very Soft Mint Tint
    c_border = colors.HexColor("#A7F3D0")     # Soft Jade Border
    
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
        fontSize=9.5,
        leading=11.5,
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
        fontSize=8.5,
        leading=10.5,
        textColor=c_primary,
        spaceAfter=2,
        spaceBefore=3,
        borderPadding=(0, 0, 1, 0),
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=c_body,
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.0,
        textColor=c_body,
    )
    
    callout_style = ParagraphStyle(
        'Callout',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=8.8,
        textColor=c_primary,
    )
    
    story = []
    
    # 1. Header (Name, Title, Contact)
    header_left = [
        Paragraph("<b>PAVEL CHERKASHIN</b>", title_style),
        Spacer(1, 2),
        Paragraph("HILLCLIMB AI &mdash; EMPLOYEE #5: EVALS RESEARCH &amp; TECHNICAL SYSTEMS WRITING", subtitle_style),
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
    
    # 2. Executive Positioning Callout (Evals + Writing as the exact seat)
    posture_text = (
        "<b>ROLE SEAT &amp; POSTURE:</b> Evals-focused systems architect applying rigorous empirical evaluation harnesses to autonomous "
        "frontier workflows. Targeting <b>Employee #5</b> at Hillclimb AI to take end-to-end ownership of <b>Evals Research and Technical Writing</b>, "
        "turning proprietary research runs and DeepRSI 48-hour benchmarks into reproducible evaluation assets, held-out verifiers, and high-signal research publications. "
        "<i>Transparent alignment:</i> deep strength in evals harnesses, held-out verifier integrity, and technical writing; transparently leaving deep RL environments and large-scale training infra to domain specialists."
    )
    posture_table = Table(
        [[Paragraph(posture_text, callout_style)]],
        colWidths=[usable_width],
        style=[
            ('BACKGROUND', (0,0), (-1,-1), c_bg),
            ('BOX', (0,0), (-1,-1), 0.75, c_border),
            ('TOPPADDING', (0,0), (-1,-1), 3.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
            ('LEFTPADDING', (0,0), (-1,-1), 5.5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5.5),
        ]
    )
    story.append(posture_table)
    story.append(Spacer(1, 3))
    
    # 3. Core Competencies Grid
    story.append(Paragraph("CORE COMPETENCIES &amp; RESEARCH ARCHITECTURE", section_title_style))
    col1 = [
        Paragraph("<b>Evals Research &amp; Harness Architecture</b>", ParagraphStyle('C1', parent=body_style, fontName='Helvetica-Bold', textColor=c_primary)),
        Paragraph("&bull; Multi-agent evaluation loops &amp; cross-model QA gates<br/>&bull; Private held-out verifiers &amp; anti-gaming assertions<br/>&bull; Bradley-Terry Elo estimation &amp; ranking telemetry<br/>&bull; Empirical failure-mode taxonomies &amp; regression tests", bullet_style),
        Spacer(1, 2),
        Paragraph("<b>Benchmark Reproducibility &amp; Integrity</b>", ParagraphStyle('C2', parent=body_style, fontName='Helvetica-Bold', textColor=c_primary)),
        Paragraph("&bull; Deterministic test harnesses &amp; isolated worktrees<br/>&bull; Tamper-evident manifest verification (SHA-256)<br/>&bull; Long-horizon execution tracing &amp; state auditability<br/>&bull; Zero-trust verification between builder &amp; QA agents", bullet_style),
    ]
    col2 = [
        Paragraph("<b>Systems Engineering &amp; Orchestration</b>", ParagraphStyle('C3', parent=body_style, fontName='Helvetica-Bold', textColor=c_primary)),
        Paragraph("&bull; Monolithic fleet daemon in Rust (fleetd)<br/>&bull; Slot leasing &amp; strict concurrency gating (WIP=1)<br/>&bull; Model Context Protocol (MCP) tool integration<br/>&bull; Autonomous backlog vacuum loops &amp; crash recovery", bullet_style),
        Spacer(1, 2),
        Paragraph("<b>Technical Writing &amp; Research Communication</b>", ParagraphStyle('C4', parent=body_style, fontName='Helvetica-Bold', textColor=c_primary)),
        Paragraph("&bull; Textbook author: <i>CRM Strategy</i> (INTUIT/BINOM, 384 pp.)<br/>&bull; Deep technical specifications &amp; architecture reports<br/>&bull; Clear public benchmark documentation &amp; research notes<br/>&bull; Structured agent communication protocols (Protocol Phi)", bullet_style),
    ]
    grid_table = Table(
        [[col1, col2]],
        colWidths=[270, 274],
        style=[
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 2),
            ('RIGHTPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]
    )
    story.append(grid_table)
    story.append(Spacer(1, 3))
    
    # 4. Systems & Evals Engineering Experience
    story.append(Paragraph("SYSTEMS, EVALS &amp; AGENT HARNESS EXPERIENCE", section_title_style))
    
    # Mindrock
    mindrock_header = "<b>Mindrock Autonomous Agent Mesh</b> &mdash; <i>Principal Systems Architect &amp; Harness Builder</i> <font color='#475569'>| 2024 &ndash; Present</font>"
    story.append(Paragraph(mindrock_header, body_style))
    mindrock_bullets = (
        "&bull; <b>Multi-Agent Evaluation &amp; QA Gate Architecture:</b> Built automated multi-tier QA test suites (cross-agent verification between Gemini, Codex, Claude) executing programmatic layout assertions, functional unit tests, and regression verification scripts prior to Principal human gate approval.<br/>"
        "&bull; <b>fleetd Daemon &amp; Slot Concurrency:</b> Engineered monolithic fleet daemon in Rust, coordinating distributed agent slots across macOS nodes (wolfram, darwin) with autonomous task-vacuum loops, rate limiting, and strict WIP=1 concurrency.<br/>"
        "&bull; <b>Protocol Phi &amp; Zero-Trust Coordination:</b> Created sealed JSON envelope transport (proto: phi-0.1) across Git repositories, enforcing cryptographically verifiable handoffs, isolated workspace lifecycles, and tamper-proof SHA-256 receipts.<br/>"
        "&bull; <b>Execution Telemetry &amp; Failure Analysis:</b> Deployed structured telemetry logging capturing task claim timestamps, execution durations, agent exit codes, and automated error recoveries across distributed fleet nodes."
    )
    story.append(Paragraph(mindrock_bullets, bullet_style))
    story.append(Spacer(1, 2.5))
    
    # Vestor.in
    vestor_header = "<b>Vestor.in &amp; High-Growth Venture Platforms</b> &mdash; <i>Founding Partner &amp; Technical Systems Architect</i> <font color='#475569'>| 2018 &ndash; 2024</font>"
    story.append(Paragraph(vestor_header, body_style))
    vestor_bullets = (
        "&bull; <b>Distributed Systems Architecture:</b> Architectural focus on event-driven platforms, API gateway resilience, and high-concurrency data streaming across portfolio technology platforms.<br/>"
        "&bull; <b>Resilient Transport &amp; Integrations:</b> Technical leadership on distributed webhook/websocket integrations, retry mechanisms with exponential backoff, and robust service availability.<br/>"
        "&bull; <b>Performance &amp; Observability Focus:</b> Technical guidance on latency profiling, distributed queue contention monitoring, and database scalability across high-growth systems."
    )
    story.append(Paragraph(vestor_bullets, bullet_style))
    story.append(Spacer(1, 2.5))
    
    # Enterprise
    early_header = "<b>Enterprise Systems &amp; Technology Leadership</b> &mdash; <i>Siebel Systems, Sputnik Labs, Microsoft</i> <font color='#475569'>| Prior</font>"
    story.append(Paragraph(early_header, body_style))
    early_bullets = (
        "&bull; Country Manager at Siebel Systems (Russia &amp; CIS); Founder &amp; Director of Sputnik Labs (pioneer CRM systems integrator in Russia/CIS, scaling to 110+ engineers and specialists, acquired by Technoserv).<br/>"
        "&bull; Platform Director at Microsoft; author of university textbook <i>Customer Relationship Management Strategy</i> (INTUIT / BINOM, 2007, 384 pp., ISBN 978-5-94774-643-3); systems design mentor."
    )
    story.append(Paragraph(early_bullets, bullet_style))
    story.append(Spacer(1, 2.5))
    
    # 5. Role Alignment & Transparent Boundary
    story.append(Paragraph("ROLE ALIGNMENT &amp; TRANSPARENT OPERATIONAL BOUNDARIES", section_title_style))
    align_text = (
        "&bull; <b>Evals &amp; Writing as the Core Seat:</b> Experienced technical builder deliberately taking an IC seat to turn proprietary research data into standardized, reproducible benchmarks, held-out private test suites, and transparent technical documentation.<br/>"
        "&bull; <b>Honest Boundary on RL Environments &amp; Training Infra:</b> Deep RL environments and large-scale training infra are NOT his depth; value comes from rigorous evaluation methodology, test harness verification, and research communication.<br/>"
        "&bull; <b>In-Person SF Collaboration:</b> Deeply committed to full in-person collaboration in San Francisco with Jun Park, Ibrakhim Ustelbay, DeepMind alumni, and quant researchers."
    )
    story.append(Paragraph(align_text, bullet_style))
    story.append(Spacer(1, 2.5))
    
    # 6. Education
    story.append(Paragraph("EDUCATION &amp; SYSTEMS FOUNDATION", section_title_style))
    edu_text = (
        "&bull; <b>B.S. Computer Science in Global Ecology:</b> Lomonosov Moscow State University (MSU), 1995 (Computational analysis of satellite data, mathematical modeling; research fellowship at IIASA Austria)."
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
        zoom = 300 / 72  # 300 DPI: zoom factor = 4.16666667
        mat = pymupdf.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        pix.save(output_png)
        doc_fitz.close()
        
        # Ensure explicit 300 DPI metadata
        pix_img = Image.open(output_png)
        pix_img.save(output_png, dpi=(300, 300))
        png_size = os.path.getsize(output_png)
        print(f"Successfully generated 300 DPI HD PNG: {output_png} ({png_size} bytes, ~{png_size / (1024*1024):.2f} MB)")
        
        standard_png = output_png.replace("-hd.png", ".png")
        if standard_png != output_png:
            pix_img.save(standard_png, dpi=(300, 300))
            print(f"Successfully generated standard PNG alias: {standard_png}")

    # Auto-synchronize generated artifacts to workspace mirror
    mirror_candidates = [
        "/Users/pavelcherkashin/workspace/goals/goal-4/files/hillclimb",
        "workspace/goals/goal-4/files/hillclimb",
        "../workspace/goals/goal-4/files/hillclimb",
        "../../workspace/goals/goal-4/files/hillclimb"
    ]
    for mc in mirror_candidates:
        if os.path.exists(mc) and os.path.isdir(mc):
            abs_mc = os.path.abspath(mc)
            if abs_mc != os.path.abspath(pdf_dir or "."):
                shutil.copy2(output_pdf, os.path.join(abs_mc, os.path.basename(output_pdf)))
                shutil.copy2(output_png, os.path.join(abs_mc, os.path.basename(output_png)))
                standard_png = output_png.replace("-hd.png", ".png")
                if standard_png != output_png:
                    shutil.copy2(standard_png, os.path.join(abs_mc, os.path.basename(standard_png)))
                print(f"Auto-synchronized compiled PDF and PNG to mirror: {abs_mc}")
            break

    return report

if __name__ == "__main__":
    pdf_out = sys.argv[1] if len(sys.argv) > 1 else "cv-pavel-cherkashin-hillclimb.pdf"
    png_out = sys.argv[2] if len(sys.argv) > 2 else "cv-pavel-cherkashin-hillclimb-hd.png"
    result = build_pdf(pdf_out, png_out)
    print(f"Verified 1-page CV build: {result}")
