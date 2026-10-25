#!/usr/bin/env python3
"""
build_cartesia_cv.py — Generates tailored 1-page technical CV for Cartesia
Role: Software Engineer, Agent Harness (Managed Agents Platform)
Location: San Francisco, CA (In-Office)
Posting: https://jobs.ashbyhq.com/cartesia/16cd6cd7-454b-4e44-9a04-6a4677a3e920
Compensation: $180,000 - $250,000 + equity (Ashby JSON-LD & poster-reported)
Linear Ticket: MIN-213
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

def build_pdf(output_pdf="cv-pavel-cherkashin-cartesia.pdf", output_png="cv-pavel-cherkashin-cartesia-hd.png"):
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
    
    # Color palette tailored to Cartesia (Deep Indigo / Tech Slate / Electric Violet)
    c_primary = colors.HexColor("#0F172A")    # Deep Slate
    c_brand = colors.HexColor("#4F46E5")      # Cartesia Indigo / Violet
    c_accent = colors.HexColor("#0284C7")     # Ocean Blue
    c_body = colors.HexColor("#1E293B")       # Dark Charcoal
    c_muted = colors.HexColor("#475569")      # Muted Slate
    c_bg = colors.HexColor("#F8FAFC")         # Crisp Light Slate
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
        leading=11.2,
        textColor=c_brand,
        spaceAfter=2.0
    )
    
    contact_style = ParagraphStyle(
        'DocContact',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=8.0,
        leading=10.0,
        textColor=c_muted,
        spaceAfter=3.0
    )
    
    hero_style = ParagraphStyle(
        'HeroText',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.4,
        textColor=c_primary,
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.6,
        leading=10.8,
        textColor=c_brand,
        spaceBefore=2.5,
        spaceAfter=1.5
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.8,
        textColor=c_body,
    )
    
    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.4,
        leading=9.7,
        textColor=c_body,
        leftIndent=8,
        firstLineIndent=-8,
    )

    story = []
    
    # 1. Header
    story.append(Paragraph("PAVEL CHERKASHIN", title_style))
    story.append(Paragraph("Software Engineer &bull; Agent Harness &amp; Distributed Systems &bull; Managed Agents Platform", subtitle_style))
    story.append(Paragraph("San Francisco, CA (In-Office / Bay Area) &nbsp;|&nbsp; pavel@mindrock.capital &nbsp;|&nbsp; linkedin.com/in/pavelcherkashin &nbsp;|&nbsp; github.com/minutta", contact_style))
    
    # 2. Hero Callout Box
    hero_p = Paragraph(
        "<b>Operating Focus:</b> <i>\"Architecting the runtime platform behind real-time multimodal voice agents. Bridging low-latency transport engineering, autonomous agent harnesses (fleetd daemon, slot concurrency, zero-trust git handoffs), and automated eval suites (LLM-as-judge scoring, pipeline tracing, latency regression catching) to deliver sub-second, resilient voice agent deployments at production scale.\"</i>",
        hero_style
    )
    hero_table = Table([[hero_p]], colWidths=[usable_width])
    hero_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg),
        ('BOX', (0,0), (-1,-1), 0.75, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(hero_table)
    story.append(Spacer(1, 2.5))
    
    # 3. Core Technical Pillars
    story.append(Paragraph("CORE TECHNICAL CAPABILITIES &amp; AGENT HARNESS SUBSTRATE", section_title_style))
    skills_text = (
        "&bull; <b>Agent Harnesses &amp; Daemon Runtimes:</b> Custom multi-agent orchestrator architecture (fleetd Rust daemon), deterministic slot scheduling (WIP=1), proactive backlog vacuuming, zero-trust git handoffs, and process isolation.<br/>"
        "&bull; <b>Conversational Latency Optimization:</b> End-to-end tracing across STT &rarr; LLM &rarr; TTS pipelines; profiling Time-To-First-Token (TTFT), streaming chunk delivery, socket buffers, and turn-taking latency.<br/>"
        "&bull; <b>Eval Suites &amp; LLM-as-Judge Scoring:</b> Automated synthetic evaluation harnesses, semantic regression tracking, LLM-as-judge scoring pipelines, and formal verification substrates (Lean 4/Mathlib) for behavioral safety.<br/>"
        "&bull; <b>Deployment Resilience &amp; Systems Scale:</b> High-throughput streaming backends, zero-downtime hot reloading, cold-start reduction, circuit breakers, and fault-tolerant distributed queuing architectures.<br/>"
        "&bull; <b>Frontier Coding-Agent Velocity:</b> Fluent daily operation across modern agentic loops (Claude Code, Gemini CLI, OpenAI tools); disciplined spec-driven development, sharp PR reviews, and automated CI/CD gates."
    )
    story.append(Paragraph(skills_text, bullet_style))
    story.append(Spacer(1, 2.5))
    
    # 4. Relevant Systems Engineering Experience
    story.append(Paragraph("SYSTEMS ENGINEERING &amp; AGENT HARNESS EXPERIENCE", section_title_style))
    
    # Mindrock
    mindrock_header = "<b>Mindrock Autonomous Agent Mesh</b> &mdash; <i>Principal Systems Architect &amp; Harness Builder</i> <font color='#475569'>| 2024 &ndash; Present</font>"
    story.append(Paragraph(mindrock_header, body_style))
    mindrock_bullets = (
        "&bull; <b>fleetd Daemon &amp; Slot Concurrency:</b> Engineered the monolithic fleet daemon in Rust, coordinating distributed agent slots across macOS nodes (wolfram, darwin) with autonomous task-vacuum loops, rate-limiting, and strict WIP caps.<br/>"
        "&bull; <b>Protocol Phi &amp; Zero-Trust Coordination:</b> Created sealed JSON envelope transport (proto: phi-0.1) across Git repositories, enforcing cryptographically verifiable handoffs, isolated workspace lifecycles, and tamper-proof SHA-256 receipts.<br/>"
        "&bull; <b>Continuous Eval &amp; QA Gate Architecture:</b> Built automated multi-tier QA test suites (cross-agent verification between Gemini, Codex, and Claude) catching layout, functional, and semantic regressions prior to human gate approval.<br/>"
        "&bull; <b>Real-Time Event Telemetry:</b> Deployed structured telemetry pipes capturing turn latency, agent error recovery, and tool-call execution metrics, identifying runtime contention and latency regressions across distributed nodes."
    )
    story.append(Paragraph(mindrock_bullets, bullet_style))
    story.append(Spacer(1, 2.5))
    
    # Vestor.in / High-Throughput
    vestor_header = "<b>Vestor.in &amp; High-Throughput Distributed Platforms</b> &mdash; <i>Founding Architect</i> <font color='#475569'>| 2018 &ndash; 2024</font>"
    story.append(Paragraph(vestor_header, body_style))
    vestor_bullets = (
        "&bull; <b>Event-Driven Distributed Engines:</b> Architected fault-tolerant streaming backends and transaction processing engines operating with low-latency streaming bounds under burst traffic loads.<br/>"
        "&bull; <b>Resilient Transport &amp; Gateway Layer:</b> Implemented distributed webhook and websocket streaming dispatchers with automatic retry exponential backoff, jittered health checks, and zero-downtime rolling deploys.<br/>"
        "&bull; <b>Telemetry &amp; Regression Profiling:</b> Built distributed tracing pipelines identifying database locking and network queue contention, significantly reducing tail (p99) latency and operational jitter."
    )
    story.append(Paragraph(vestor_bullets, bullet_style))
    story.append(Spacer(1, 2.5))
    
    # Early Career / Microsoft / Enterprise
    early_header = "<b>Enterprise Systems &amp; Technology Leadership</b> &mdash; <i>Siebel Systems, Sputnik Labs, Microsoft</i> <font color='#475569'>| Prior</font>"
    story.append(Paragraph(early_header, body_style))
    early_bullets = (
        "&bull; Country Manager at Siebel Systems; Founder of Sputnik Labs (scaled to 500+ engineers executing mission-critical distributed systems and CRM integrations for telecom and banking leaders).<br/>"
        "&bull; Regional Director at Microsoft; authored authoritative university textbook on enterprise software and automated customer architectures; mentored hundreds of engineers on reliable system design."
    )
    story.append(Paragraph(early_bullets, bullet_style))
    story.append(Spacer(1, 2.5))
    
    # 5. Candidate Posture, Honest Alignment & Ramp Plan
    story.append(Paragraph("ROLE ALIGNMENT, TRANSPARENT GAPS &amp; OPERATING POSTURE", section_title_style))
    alignment_text = (
        "&bull; <b>Intentional IC Backend Focus:</b> Experienced founder/operator deliberately pursuing an individual contributor backend systems role to build foundational, high-leverage agent runtime infrastructure for Cartesia's Managed Agents.<br/>"
        "&bull; <b>First-Principles Ramp on Voice Protocols:</b> Direct mastery of agent harnesses, distributed queuing, and streaming sockets; transparently ramping on low-level WebRTC/SIP/RTP telephony protocols and voice frameworks (Pipecat/LiveKit).<br/>"
        "&bull; <b>Engineering Discipline &amp; Collaborative Presence:</b> Deeply committed to in-person San Francisco collaboration, sharp technical specifications, rigorous peer design reviews, and high-velocity shipping culture."
    )
    story.append(Paragraph(alignment_text, bullet_style))
    story.append(Spacer(1, 2.5))
    
    # 6. Education
    story.append(Paragraph("EDUCATION &amp; SYSTEMS FOUNDATION", section_title_style))
    edu_text = (
        "&bull; <b>B.S. / M.S. Applied Mathematics &amp; Computer Science:</b> Russian State University of Oil &amp; Gas (Quantitative algorithms, discrete mathematics, network theory, and systems programming)."
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
        standard_png = output_png.replace("-hd.png", ".png")
        if standard_png != output_png:
            img.save(standard_png, dpi=(300, 300))
            print(f"Successfully generated standard PNG alias: {standard_png}")
        doc_fitz.close()
    
    return output_pdf, output_png

if __name__ == "__main__":
    out_pdf = sys.argv[1] if len(sys.argv) > 1 else "cv-pavel-cherkashin-cartesia.pdf"
    out_png = sys.argv[2] if len(sys.argv) > 2 else "cv-pavel-cherkashin-cartesia-hd.png"
    build_pdf(out_pdf, out_png)
