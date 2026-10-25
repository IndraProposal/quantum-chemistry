#!/usr/bin/env python3
"""
build_gd_cv.py — Generates tailored 1-page executive CV for General Deployment (Vanessa Li)
Paradigm: 6-Month Automation Arc & Systems Architecture
Author: agy@wolfram (Mindrock Autonomous Network)
Linear Ticket: MIN-206
"""

import os
import sys
import pypdf
import fitz  # PyMuPDF
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)

def build_pdf(output_path="cv-pavel-cherkashin-gd.pdf"):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # Letter is 612 x 792 pt
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=34,
        rightMargin=34,
        topMargin=28,
        bottomMargin=24,
    )
    
    usable_width = 612 - 68  # 544 pt
    
    # Palette
    c_primary = colors.HexColor("#0F172A")    # Deep Slate
    c_accent = colors.HexColor("#0D9488")     # Tech Teal
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
        fontSize=10,
        leading=12,
        textColor=c_accent,
        spaceAfter=3
    )
    
    contact_style = ParagraphStyle(
        'DocContact',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=c_muted,
        spaceAfter=5
    )
    
    hero_style = ParagraphStyle(
        'HeroText',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=c_primary,
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=c_navy,
        spaceBefore=5,
        spaceAfter=3
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_body,
    )
    
    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_body,
        leftIndent=10,
        firstLineIndent=-10,
    )
    
    note_style = ParagraphStyle(
        'NoteText',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=c_muted,
    )

    story = []
    
    # 1. Header
    story.append(Paragraph("PAVEL CHERKASHIN", title_style))
    story.append(Paragraph("Systems Architecture &amp; Operational Execution &bull; 6-Month Automation Arc", subtitle_style))
    story.append(Paragraph("San Francisco, CA &nbsp;|&nbsp; pavel@mindrock.capital &nbsp;|&nbsp; linkedin.com/in/pavelcherkashin &nbsp;|&nbsp; github.com/minutta", contact_style))
    
    # 2. Hero Callout Box
    hero_p = Paragraph(
        "<b>Hero Statement:</b> <i>\"I don’t come to warm a chair. I build autonomous operational infrastructure, eliminate organizational drag, and automate myself out of repetitive execution within 6 months—leaving behind self-driving systems, codified playbooks, and high-uptime factory operations.\"</i>",
        hero_style
    )
    hero_table = Table([[hero_p]], colWidths=[usable_width])
    hero_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg),
        ('BOX', (0,0), (-1,-1), 0.75, c_border),
        ('LINELEFT', (0,0), (-1,-1), 3.0, c_accent),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(hero_table)
    story.append(Spacer(1, 5))
    
    # 3. Context & The SpaceX Starlink Refurb Hook
    story.append(Paragraph("STRATEGIC THESIS: DEPLOYING PHYSICAL AI ONTO THE FACTORY FLOOR", section_title_style))
    thesis_text = (
        "Vanessa Li proved at SpaceX that ruthless operational waste elimination—recovering and refurbishing Starlink user hardware rather than constantly manufacturing expensive PCBs—unlocks massive margin and engineering velocity. At General Deployment, the breakthrough is taking bimanual mobile manipulators out of academic benchmarks and making them <i>actually work</i> in manufacturing: 'site visit &rarr; running in 2 weeks' with '24/7 white-glove support' across kitting, machine tending, bin-to-tray transfer, and packing. As highlighted in Vanessa's <i>State of Robotics Data</i>, the real bottleneck is not model parameters, but physical deployment telemetry, edge adaptation, and zero-downtime reliability. I bring 20+ years of high-velocity systems engineering, venture scale ($100M+ deployed), and autonomous multi-agent mesh architecture to operationalize GD's 2-week deployment promise into a deterministic, zero-drag execution machine."
    )
    story.append(Paragraph(thesis_text, body_style))
    story.append(Spacer(1, 5))
    
    # 4. The 6-Month Automation Arc
    story.append(Paragraph("THE 6-MONTH AUTOMATION ARC (OPERATIONAL PRIORITIES &amp; MILESTONES)", section_title_style))
    
    arc_data = [
        [
            Paragraph("<b>Months 1–2</b><br/><font color='#0D9488'><b>Site &amp; Telemetry</b></font>", ParagraphStyle('H1', parent=body_style, fontName='Helvetica-Bold', fontSize=8, leading=10)),
            Paragraph("<b>Automated Site Scoping &amp; Geometry Ingestion:</b> Map the 2-week site-to-run pipeline into deterministic stages. Build automated intake pipelines for factory tooling constraints, CAD part geometries (kitting &amp; bin-to-tray), and MES API connectors to compress deployment lead times and eliminate site-visit ambiguities.", body_style)
        ],
        [
            Paragraph("<b>Months 3–4</b><br/><font color='#0D9488'><b>Fleet Watchdog</b></font>", ParagraphStyle('H2', parent=body_style, fontName='Helvetica-Bold', fontSize=8, leading=10)),
            Paragraph("<b>24/7 Autonomous Fleet Watchdog &amp; White-Glove Support:</b> Deploy an autonomous multi-agent monitoring mesh tracking robot fleet telemetry. Anomaly detection catches cycle time drift and pick-fail spikes in machine tending, triggering preemptive teleop assist before line halts occur.", body_style)
        ],
        [
            Paragraph("<b>Months 5–6</b><br/><font color='#0D9488'><b>Scale &amp; Hand-Off</b></font>", ParagraphStyle('H3', parent=body_style, fontName='Helvetica-Bold', fontSize=8, leading=10)),
            Paragraph("<b>Enterprise Scaling &amp; Autonomous Operational Hand-Off:</b> Codify factory MSA contracts, site safety certifications, and field deployment playbooks. Transition daily operational coordination to automated agent swarms and trained site leads, shifting into an ongoing advisory / expansion capacity.", body_style)
        ],
    ]
    arc_table = Table(arc_data, colWidths=[95, usable_width - 95])
    arc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, colors.HexColor("#E2E8F0")),
    ]))
    story.append(arc_table)
    story.append(Spacer(1, 5))
    
    # 5. Core Systems & Execution Capabilities
    story.append(Paragraph("CORE SYSTEMS &amp; EXECUTION CAPABILITIES", section_title_style))
    cap_data = [
        [
            Paragraph("&bull; <b>Physical AI &amp; Field Operations:</b> Real-world robot deployment lifecycles, teleoperation telemetry routing, factory cell integration (kitting, machine tending, bin-to-tray, packing), 24/7 high-uptime operations.", bullet_style),
            Paragraph("&bull; <b>Autonomous Infrastructure:</b> Distributed multi-agent swarms, event-driven pipelines, API/MES integration, Python/Rust telemetry tooling, deterministic triage protocols.", bullet_style),
        ],
        [
            Paragraph("&bull; <b>Enterprise Scale &amp; Capital:</b> $100M+ venture deployment across hardware and software; negotiated complex enterprise MSAs, closed factory pilots, built global partner networks.", bullet_style),
            Paragraph("&bull; <b>Hands-on Builder Ethos:</b> Zero-overhead operational discipline; rapid prototyping of tools and diagnostic harnesses without bureaucratic drag.", bullet_style),
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
    story.append(Spacer(1, 5))
    
    # 6. Selected Career Track Record
    story.append(Paragraph("SELECTED CAREER TRACK RECORD", section_title_style))
    
    story.append(Paragraph("<b>Managing Partner &amp; Systems Architect</b> &mdash; <i>Mindrock Capital / Vestor.In</i> (2016–Present)", ParagraphStyle('Exp1', parent=body_style, fontName='Helvetica-Bold', fontSize=8.5, leading=11)))
    story.append(Paragraph("&bull; Managed $100M+ in tech and hardware assets. Architected autonomous multi-agent operational mesh for fleet governance, financial audits, and real-time operational telemetry.", bullet_style))
    story.append(Spacer(1, 3))
    
    story.append(Paragraph("<b>CEO &amp; Founder</b> &mdash; <i>Startup Temple &amp; Global Innovation Platforms</i> (2012–2020)", ParagraphStyle('Exp2', parent=body_style, fontName='Helvetica-Bold', fontSize=8.5, leading=11)))
    story.append(Paragraph("&bull; Scaled physical acceleration centers and innovation hubs in San Francisco, connecting 500+ frontier tech companies with enterprise partners, manufacturing pilots, and venture syndicates.", bullet_style))
    story.append(Spacer(1, 3))
    
    story.append(Paragraph("<b>Serial Founder &amp; Systems Executive</b> &mdash; <i>Enterprise Software &amp; Tech Exits</i>", ParagraphStyle('Exp3', parent=body_style, fontName='Helvetica-Bold', fontSize=8.5, leading=11)))
    story.append(Paragraph("&bull; Founded and scaled multiple venture-backed software ventures through successful enterprise acquisitions; deep technical foundation in distributed systems, real-time protocols, and automated operations.", bullet_style))
    story.append(Spacer(1, 6))
    
    # 7. Disclaimers & Notes (Footer note)
    note_p = Paragraph(
        "<b>Transparency &amp; Mandate Note:</b> Founder-facing, role-agnostic application focused on accelerating General Deployment’s factory rollout velocity and building scalable operational machinery. Internal fleet agent metrics (&ge;20 issues/day, &ge;1 project/week) are omitted pending third-party verification.",
        note_style
    )
    note_table = Table([[note_p]], colWidths=[usable_width])
    note_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(note_table)
    
    doc.build(story)
    
    # Verification
    reader = pypdf.PdfReader(output_path)
    page_count = len(reader.pages)
    if page_count != 1:
        raise ValueError(f"CV is {page_count} pages; must be exactly 1 page!")
    
    print(f"Successfully generated 1-page CV: {output_path}")
    return output_path

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "cv-pavel-cherkashin-gd.pdf"
    build_pdf(out)
