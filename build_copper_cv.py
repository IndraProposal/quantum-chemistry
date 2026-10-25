#!/usr/bin/env python3
"""
build_copper_cv.py — Generates tailored 1-page executive CV for Copperlane (Veronica Garg / Athan Zhang / Brianna Lin)
Paradigm: 6-Month Automation Arc & Autonomous Mortgage Verification (Penny)
Author: agy@wolfram (Mindrock Autonomous Network)
Linear Ticket: MIN-207
"""

import os
import sys
import pypdf
import pymupdf  # fitz
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)

def build_pdf(output_pdf="cv-pavel-cherkashin-copper.pdf", output_png="cv-pavel-cherkashin-copper-hd.png"):
    pdf_dir = os.path.dirname(os.path.abspath(output_pdf))
    if pdf_dir:
        os.makedirs(pdf_dir, exist_ok=True)
    
    # Letter is 612 x 792 pt
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        leftMargin=34,
        rightMargin=34,
        topMargin=26,
        bottomMargin=22,
    )
    
    usable_width = 612 - 68  # 544 pt
    
    # Palette
    c_primary = colors.HexColor("#0F172A")    # Deep Slate
    c_copper = colors.HexColor("#C25E00")     # Warm Copper Accent
    c_navy = colors.HexColor("#1E3A8A")       # Industrial Navy
    c_body = colors.HexColor("#1E293B")       # Dark Charcoal
    c_muted = colors.HexColor("#475569")      # Muted Slate
    c_bg = colors.HexColor("#F8FAFC")         # Very light slate
    c_border = colors.HexColor("#CBD5E1")     # Light border
    
    base_styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=22,
        textColor=c_primary,
        spaceAfter=2
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=c_copper,
        spaceAfter=3
    )
    
    contact_style = ParagraphStyle(
        'DocContact',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=c_muted,
        spaceAfter=4
    )
    
    hero_style = ParagraphStyle(
        'HeroText',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_primary,
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=c_navy,
        spaceBefore=4,
        spaceAfter=2.5
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11,
        textColor=c_body,
    )
    
    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11,
        textColor=c_body,
        leftIndent=10,
        firstLineIndent=-10,
    )
    
    note_style = ParagraphStyle(
        'NoteText',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.2,
        textColor=c_muted,
    )

    story = []
    
    # 1. Header
    story.append(Paragraph("PAVEL CHERKASHIN", title_style))
    story.append(Paragraph("AI Systems Architecture &amp; Mortgage Automation &bull; 6-Month Automation Arc", subtitle_style))
    story.append(Paragraph("San Francisco, CA (On-Site) &nbsp;|&nbsp; pavel@mindrock.capital &nbsp;|&nbsp; linkedin.com/in/pavelcherkashin &nbsp;|&nbsp; github.com/minutta", contact_style))
    
    # 2. Hero Callout Box
    hero_p = Paragraph(
        "<b>Hero Statement:</b> <i>\"I don’t come to warm a chair. I build autonomous operational infrastructure, eliminate friction, and automate myself out of repetitive execution within 6 months—leaving behind self-driving verification systems, codified playbooks, and high-uptime underwriting pipelines.\"</i>",
        hero_style
    )
    hero_table = Table([[hero_p]], colWidths=[usable_width])
    hero_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg),
        ('BOX', (0,0), (-1,-1), 0.75, c_border),
        ('LINELEFT', (0,0), (-1,-1), 3.0, c_copper),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(hero_table)
    story.append(Spacer(1, 4))
    
    # 3. Context & The Mortgage Origination Hook (Penny)
    story.append(Paragraph("STRATEGIC THESIS: AI-NATIVE MORTGAGE OPS &amp; UNDERWRITING AUTOMATION", section_title_style))
    thesis_text = (
        "Mortgage origination is the ultimate proving ground for autonomous AI systems: reviewing borrower loan files spans thousands of pages (W-2s, 1040 tax returns, paystubs, asset statements, disclosures), taking 4+ hours per loan file and creating massive operational drag. Copperlane's breakthrough with Penny—an autonomous AI loan officer compressing hours of manual review into minutes while maintaining strict human-in-the-loop underwriting approvals—is exactly where agentic architecture creates non-linear enterprise value. As a seasoned builder who has deployed $100M+ in tech/venture capital, architected autonomous multi-agent meshes, and engineered high-stakes compliance pipelines, I bridge the gap between foundation models and deterministic, production-grade mortgage ops. I operate on-site in SF on a dedicated 6-month arc to harden Penny's verification engines, build regression harnesses, and automate underwriting friction out of existence."
    )
    story.append(Paragraph(thesis_text, body_style))
    story.append(Spacer(1, 4))
    
    # 4. The 6-Month Automation Arc
    story.append(Paragraph("THE 6-MONTH AUTOMATION ARC (OPERATIONAL PRIORITIES &amp; MILESTONES)", section_title_style))
    
    arc_data = [
        [
            Paragraph("<b>Months 1–2</b><br/><font color='#C25E00'><b>Verification &amp; Eval</b></font>", ParagraphStyle('H1', parent=body_style, fontName='Helvetica-Bold', fontSize=8, leading=10)),
            Paragraph("<b>Deterministic Document Verification &amp; Eval Harness:</b> Engineer synthetic and historical regression suites across multi-thousand-page borrower packets (1040 schedules, W-2s, P&amp;L statements, paystubs). Implement deterministic discrepancy detection for DTI ratios, unverified debt obligations, and income stability to eliminate hallucination risks.", body_style)
        ],
        [
            Paragraph("<b>Months 3–4</b><br/><font color='#C25E00'><b>Borrower Comms Mesh</b></font>", ParagraphStyle('H2', parent=body_style, fontName='Helvetica-Bold', fontSize=8, leading=10)),
            Paragraph("<b>Autonomous Borrower Interactions &amp; Discrepancy Mesh:</b> Scale Penny's interactive borrower communication workflows: real-time missing-document chases, automated drafting of letters of explanation (LOE), and discrepancy reconciliation. Enforce strict human-in-the-loop checkpoints for licensed loan officers before external dispatch.", body_style)
        ],
        [
            Paragraph("<b>Months 5–6</b><br/><font color='#C25E00'><b>LOS Scale &amp; Hand-Off</b></font>", ParagraphStyle('H3', parent=body_style, fontName='Helvetica-Bold', fontSize=8, leading=10)),
            Paragraph("<b>Enterprise LOS Integrations &amp; Autonomous Hand-Off:</b> Codify bi-directional connectors into core Loan Origination Systems (Encompass, LendingPad, Byte). Deploy end-to-end observability and underwriting compliance telemetry. Transition day-to-day coordination to automated agent swarms and trained underwriting leads, shifting into an ongoing advisory capacity.", body_style)
        ],
    ]
    arc_table = Table(arc_data, colWidths=[95, usable_width - 95])
    arc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, colors.HexColor("#E2E8F0")),
    ]))
    story.append(arc_table)
    story.append(Spacer(1, 4))
    
    # 5. Core Systems & Execution Capabilities
    story.append(Paragraph("CORE SYSTEMS &amp; EXECUTION CAPABILITIES", section_title_style))
    cap_data = [
        [
            Paragraph("&bull; <b>High-Stakes Document Verification:</b> OCR/VLM ingestion, complex tax return parsing, multi-page financial statement reconciliation, deterministic discrepancy extraction.", bullet_style),
            Paragraph("&bull; <b>Autonomous Multi-Agent Swarms:</b> Event-driven workflows, agentic error-watchdogs, distributed queue orchestration, Python/Rust systems engineering.", bullet_style),
        ],
        [
            Paragraph("&bull; <b>Enterprise Scale &amp; Capital:</b> $100M+ deployed across venture and tech assets; negotiated enterprise partner contracts, managed cap tables, institutional governance.", bullet_style),
            Paragraph("&bull; <b>Production Builder Ethos:</b> On-site in San Francisco; zero-drag builder mindset; rapid prototyping of evaluation harnesses and LOS integrations without bureaucratic overhead.", bullet_style),
        ]
    ]
    cap_table = Table(cap_data, colWidths=[usable_width/2.0, usable_width/2.0])
    cap_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(cap_table)
    story.append(Spacer(1, 4))
    
    # 6. Selected Career Track Record
    story.append(Paragraph("SELECTED CAREER TRACK RECORD", section_title_style))
    
    story.append(Paragraph("<b>Managing Partner &amp; Systems Architect</b> &mdash; <i>Mindrock Capital / Vestor.In</i> (2016–Present)", ParagraphStyle('Exp1', parent=body_style, fontName='Helvetica-Bold', fontSize=8.3, leading=11)))
    story.append(Paragraph("&bull; Managed $100M+ in tech and enterprise assets. Architected autonomous multi-agent operational mesh for automated verification, financial audit workflows, and real-time operational telemetry.", bullet_style))
    story.append(Spacer(1, 2.5))
    
    story.append(Paragraph("<b>CEO &amp; Founder</b> &mdash; <i>Startup Temple &amp; Global Innovation Platforms</i> (2012–2020)", ParagraphStyle('Exp2', parent=body_style, fontName='Helvetica-Bold', fontSize=8.3, leading=11)))
    story.append(Paragraph("&bull; Scaled physical acceleration hubs and innovation centers in San Francisco, connecting 500+ frontier tech companies with enterprise partners, institutional investors, and capital syndicates.", bullet_style))
    story.append(Spacer(1, 2.5))
    
    story.append(Paragraph("<b>Serial Founder &amp; Systems Executive</b> &mdash; <i>Enterprise Software &amp; Tech Exits</i>", ParagraphStyle('Exp3', parent=body_style, fontName='Helvetica-Bold', fontSize=8.3, leading=11)))
    story.append(Paragraph("&bull; Founded and scaled multiple venture-backed software ventures through successful enterprise M&amp;A exits; deep technical expertise in distributed systems, real-time protocols, and automated operations.", bullet_style))
    story.append(Spacer(1, 5))
    
    # 7. Disclaimers & Notes (Footer note)
    note_p = Paragraph(
        "<b>Transparency &amp; Mandate Note:</b> Founder-facing application for Copperlane (YC W26) on-site in SF. Positioned as a builder leveraging autonomous multi-agent systems and shipped code rather than a conventional junior IC. Internal agent fleet throughput figures are omitted pending third-party audit. External MiniMax M3.1 Flash benchmark figures are excluded.",
        note_style
    )
    note_table = Table([[note_p]], colWidths=[usable_width])
    note_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(note_table)
    
    doc.build(story)
    
    # Verification
    reader = pypdf.PdfReader(output_pdf)
    page_count = len(reader.pages)
    if page_count != 1:
        raise ValueError(f"CV is {page_count} pages; must be exactly 1 page!")
    
    print(f"Successfully generated 1-page CV: {output_pdf}")
    
    # Export 300 DPI HD PNG
    if output_png:
        doc_fitz = pymupdf.open(output_pdf)
        page = doc_fitz[0]
        zoom = 300 / 72  # 300 DPI
        mat = pymupdf.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        pix.save(output_png)
        png_size = os.path.getsize(output_png)
        print(f"Successfully generated 300 DPI HD PNG: {output_png} ({png_size} bytes, ~{png_size / (1024*1024):.2f} MB)")
        doc_fitz.close()
    
    return output_pdf, output_png

if __name__ == "__main__":
    out_pdf = sys.argv[1] if len(sys.argv) > 1 else "cv-pavel-cherkashin-copper.pdf"
    out_png = sys.argv[2] if len(sys.argv) > 2 else "cv-pavel-cherkashin-copper-hd.png"
    build_pdf(out_pdf, out_png)
