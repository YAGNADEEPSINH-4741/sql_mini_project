"""
SMART BANKING MANAGEMENT SYSTEM - COMPREHENSIVE ACADEMIC DATABASE REPORT
Strictly adhering to GMIU Assignment Automation format.docx guidelines:
- Strictly Monochrome Black and White (black text, white background, no colors)
- Font: TrueType registered Calibri for typography, Consolas for SQL/PLSQL code
- Margins: 28.8 pt top/bottom, 36.0 pt left/right
- Standard Heading & Subheading sizes matching reference DOCX
- Explanation structure: 1. What it is, 2. Why used, 3. How it works, 4. Where implemented, 5. Output/Result
- Complete object lists before individual explanations for every single category
- Complete implementation of every single View (1-6), Procedure (1-10), Function (1-6), Trigger (1-7), Cursor (1-4), Join (1-6), Subquery (1-5), and Set Operator (1-4)
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONTS_DIR = r"C:\\Windows\\Fonts"
try:
    pdfmetrics.registerFont(TTFont('Calibri', os.path.join(FONTS_DIR, 'calibri.ttf')))
    pdfmetrics.registerFont(TTFont('Calibri-Bold', os.path.join(FONTS_DIR, 'calibrib.ttf')))
    pdfmetrics.registerFont(TTFont('Calibri-Italic', os.path.join(FONTS_DIR, 'calibrii.ttf')))
    pdfmetrics.registerFont(TTFont('Calibri-BoldItalic', os.path.join(FONTS_DIR, 'calibriz.ttf')))
    pdfmetrics.registerFontFamily('Calibri', normal='Calibri', bold='Calibri-Bold', italic='Calibri-Italic', boldItalic='Calibri-BoldItalic')
    FONT_NORMAL = 'Calibri'
    FONT_BOLD = 'Calibri-Bold'
    FONT_ITALIC = 'Calibri-Italic'
    FONT_BOLD_ITALIC = 'Calibri-BoldItalic'
except Exception as e:
    FONT_NORMAL = 'Helvetica'
    FONT_BOLD = 'Helvetica-Bold'
    FONT_ITALIC = 'Helvetica-Oblique'
    FONT_BOLD_ITALIC = 'Helvetica-BoldOblique'

try:
    pdfmetrics.registerFont(TTFont('Consolas', os.path.join(FONTS_DIR, 'consola.ttf')))
    FONT_CODE = 'Consolas'
except Exception:
    FONT_CODE = 'Courier'

class AcademicCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_header_footer(page_count)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont(FONT_NORMAL, 8)
        self.setFillColor(colors.black)

        self.drawString(36, 765, "Smart Banking Management System — Oracle SQL & Advanced PL/SQL Database Engineering Report")
        self.setStrokeColor(colors.black)
        self.setLineWidth(0.5)
        self.line(36, 760, 576, 760)

        self.line(36, 40, 576, 40)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 28, page_str)
        self.drawString(36, 28, "Department of Computer Applications | Gyanmanjari Innovative University (GMIU)")
        self.restoreState()

def build_pdf():
    pdf_path = r"d:\\college\\RDBMS\\mini_project\\documentation\\SMART_BANKING_MANAGEMENT_SYSTEM_REPORT.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=28.8,
        bottomMargin=28.8
    )

    c_black = colors.black
    c_white = colors.white
    c_gray_bg = colors.HexColor("#f8f8f8")

    univ_style = ParagraphStyle('UnivStyle', fontName=FONT_BOLD, fontSize=17, leading=21, alignment=1, textColor=c_black, spaceAfter=3)
    dept_style = ParagraphStyle('DeptStyle', fontName=FONT_BOLD, fontSize=11, leading=15, alignment=1, textColor=c_black, spaceAfter=8)
    title_style = ParagraphStyle('TitleStyle', fontName=FONT_BOLD, fontSize=21, leading=25, alignment=1, textColor=c_black, spaceAfter=4)
    subtitle_style = ParagraphStyle('SubTitleStyle', fontName=FONT_BOLD, fontSize=12, leading=16, alignment=1, textColor=c_black, spaceAfter=6)
    
    sec_style = ParagraphStyle('SecStyle', fontName=FONT_BOLD, fontSize=13, leading=16.5, textColor=c_black, spaceBefore=10, spaceAfter=3.5, keepWithNext=True)
    subsec_style = ParagraphStyle('SubSecStyle', fontName=FONT_BOLD, fontSize=10.5, leading=14, textColor=c_black, spaceBefore=6, spaceAfter=2.5, keepWithNext=True)
    body_style = ParagraphStyle('BodyStyle', fontName=FONT_NORMAL, fontSize=9.2, leading=12.5, textColor=c_black, spaceAfter=3)
    body_bold = ParagraphStyle('BodyBold', fontName=FONT_BOLD, fontSize=9.2, leading=12.5, textColor=c_black, spaceAfter=3)
    list_style = ParagraphStyle('ListStyle', fontName=FONT_NORMAL, fontSize=9, leading=12.2, leftIndent=12, spaceAfter=1.8)

    code_style = ParagraphStyle(
        'CodeStyle', fontName=FONT_CODE, fontSize=6.5, leading=8.0,
        textColor=c_black, backColor=c_gray_bg,
        borderPadding=2.5, spaceBefore=2, spaceAfter=2.5
    )

    tbl_header = ParagraphStyle('TblHdr', fontName=FONT_BOLD, fontSize=7.8, leading=9.8, textColor=c_black)
    tbl_cell = ParagraphStyle('TblCell', fontName=FONT_NORMAL, fontSize=7.8, leading=9.8, textColor=c_black)
    tbl_cell_bold = ParagraphStyle('TblCellBold', fontName=FONT_BOLD, fontSize=7.8, leading=9.8, textColor=c_black)

    story = []

    def make_code(text):
        escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&nbsp;").replace("\\n", "<br/>")
        return Paragraph(escaped, code_style)

    def make_expl(what, why, how, where, output):
        txt = (
            f"<b>Explanation:</b><br/>"
            f"• <b>What it is:</b> {what}<br/>"
            f"• <b>Why it is used:</b> {why}<br/>"
            f"• <b>How it works:</b> {how}<br/>"
            f"• <b>Where implemented:</b> {where}<br/>"
            f"• <b>Output / Result:</b> {output}"
        )
        return Paragraph(txt, body_style)

    # =========================================================================
    # 1. COVER PAGE (PAGE 1)
    # =========================================================================
    story.append(Spacer(1, 8))
    story.append(Paragraph("GYANMANJARI INNOVATIVE UNIVERSITY (GMIU)", univ_style))
    story.append(Paragraph("FACULTY OF COMPUTER APPLICATIONS<br/>DEPARTMENT OF COMPUTER APPLICATIONS", dept_style))
    story.append(HRFlowable(width="95%", thickness=1.5, color=c_black, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("SMART BANKING MANAGEMENT SYSTEM", title_style))
    story.append(Paragraph("Oracle SQL &amp; Advanced PL/SQL Relational Database Engineering Mini Project", subtitle_style))
    story.append(Paragraph("<b>ACADEMIC YEAR: 2026 – 2027 &nbsp;|&nbsp; SEMESTER – 1</b>", ParagraphStyle('CoverYear', parent=dept_style, fontSize=9.5, spaceAfter=8)))

    story.append(Paragraph("<b>STUDENT DETAILS (ACADEMIC GROUP PROJECT)</b>", ParagraphStyle('TblTitle', parent=subsec_style, alignment=1, spaceAfter=3)))
    
    group_data = [
        [Paragraph("<b>Sr.</b>", tbl_header), Paragraph("<b>Student Full Name</b>", tbl_header), Paragraph("<b>Enrollment Number</b>", tbl_header), Paragraph("<b>Course / Specialization</b>", tbl_header), Paragraph("<b>Core Module Responsibilities</b>", tbl_header)],
        [Paragraph("1", tbl_cell), Paragraph("<b>Vaghela Yagnadeepsinh.C</b>", tbl_cell_bold), Paragraph("260203030002", tbl_cell_bold), Paragraph("MCA (Cloud Computing)", tbl_cell), Paragraph("Project Architecture, 3NF Schema & Master RUN_ALL.SQL Script", tbl_cell)],
        [Paragraph("2", tbl_cell), Paragraph("<b>Chudasama Krishnadeepsinh .S</b>", tbl_cell_bold), Paragraph("260203030001", tbl_cell_bold), Paragraph("MCA (Cloud Computing)", tbl_cell), Paragraph("PL/SQL Stored Procedures, Functions & Package Implementation", tbl_cell)],
        [Paragraph("3", tbl_cell), Paragraph("<b>Chauhan Jaydip. P</b>", tbl_cell_bold), Paragraph("260203020035", tbl_cell_bold), Paragraph("MCA (AI &amp; DS)", tbl_cell), Paragraph("Complex Analytical Queries, Relational Joins & Subquery Optimization", tbl_cell)],
        [Paragraph("4", tbl_cell), Paragraph("<b>Gohil Jignesh. P</b>", tbl_cell_bold), Paragraph("260203020034", tbl_cell_bold), Paragraph("MCA (AI &amp; DS)", tbl_cell), Paragraph("Autonomous Triggers, Security Audit Trail & 12-Case Test Suite", tbl_cell)],
    ]
    t_group = Table(group_data, colWidths=[22, 135, 90, 105, 188])
    t_group.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f0f0f0")),
        ('BOX', (0,0), (-1,-1), 1, c_black),
        ('GRID', (0,0), (-1,-1), 0.5, c_black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [c_white, colors.HexColor("#f8f8f8")]),
    ]))
    story.append(t_group)
    story.append(Spacer(1, 6))

    meta_table_data = [
        [Paragraph("<b>Subject Name</b>", tbl_cell_bold), Paragraph("Relational Database Management System (RDBMS)", tbl_cell)],
        [Paragraph("<b>Module &amp; Title</b>", tbl_cell_bold), Paragraph("Module 1 &amp; 2: Advanced Relational Modeling, SQL Operations &amp; Enterprise PL/SQL", tbl_cell)],
        [Paragraph("<b>Assigned Practical Activity</b>", tbl_cell_bold), Paragraph("Enterprise Smart Banking Management System — Core Database Engineering", tbl_cell)],
        [Paragraph("<b>Database Engine</b>", tbl_cell_bold), Paragraph("Oracle Database 19c / 21c / 23ai Enterprise &amp; Express Editions via SQL*Plus CLI", tbl_cell)],
        [Paragraph("<b>Submission Date</b>", tbl_cell_bold), Paragraph("November 2026", tbl_cell)],
        [Paragraph("<b>Project Repository Link</b>", tbl_cell_bold), Paragraph("<u>https://github.com/YAGNADEEPSINH-4741/sql_mini_project</u>", tbl_cell)],
    ]
    t_meta = Table(meta_table_data, colWidths=[140, 400])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#f0f0f0")),
        ('BOX', (0,0), (-1,-1), 1, c_black),
        ('GRID', (0,0), (-1,-1), 0.5, c_black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 6))

    high_data = [
        [Paragraph("<b>Core Engineering Feature</b>", tbl_header), Paragraph("<b>Implementation Architecture &amp; Practical Banking Utility</b>", tbl_header)],
        [Paragraph("3NF Relational Schema", tbl_cell_bold), Paragraph("11 normalized tables preventing insertion, update, and deletion anomalies across branches, accounts, and ledgers.", tbl_cell)],
        [Paragraph("ACID Transaction Engine", tbl_cell_bold), Paragraph("Two-phase atomic transfers with pessimistic row locking (<code>FOR UPDATE</code>) and guaranteed rollback.", tbl_cell)],
        [Paragraph("Autonomous Security Audit", tbl_cell_bold), Paragraph("<code>PRAGMA AUTONOMOUS_TRANSACTION</code> trigger logging all balance/status mutations independently.", tbl_cell)],
        [Paragraph("Modular PL/SQL Packages", tbl_cell_bold), Paragraph("Encapsulates depository and loan operations into <code>BANKING_PACKAGE</code> and <code>LOAN_PACKAGE</code>.", tbl_cell)],
        [Paragraph("12-Case Test Suite", tbl_cell_bold), Paragraph("100% verification pass rate across deposits, overdraft limits, dormancy guards, and rollback scenarios.", tbl_cell)]
    ]
    t_high = Table(high_data, colWidths=[130, 410])
    t_high.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f0f0f0")),
        ('BOX', (0,0), (-1,-1), 1, c_black),
        ('GRID', (0,0), (-1,-1), 0.5, c_black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [c_white, colors.HexColor("#f8f8f8")]),
    ]))
    story.append(t_high)
    story.append(PageBreak())

    # =========================================================================
    # 1. INTRODUCTION TO 7. SYSTEM ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("1. INTRODUCTION", sec_style))
    story.append(Paragraph(
        "Commercial banking systems represent the quintessential use-case for enterprise Relational Database Management Systems (RDBMS). "
        "Every second, thousands of debit, credit, and transfer operations interact with central depository accounts. A single failure in "
        "transactional isolation or referential consistency can lead to catastrophic double-spending, phantom balances, or compliance regulatory "
        "fines. The Smart Banking Management System demonstrates how modern financial core systems leverage compiled Oracle Database SQL and PL/SQL "
        "constructs to enforce mission-critical business rules directly at the data layer.", body_style
    ))

    story.append(Paragraph("2. PROBLEM STATEMENT", sec_style))
    story.append(Paragraph(
        "Many distributed banking applications mistakenly implement financial validation and balance updates inside external application code "
        "(e.g., Python, PHP, Java). Under high concurrent load, this architectural anti-pattern introduces severe vulnerabilities: race conditions "
        "during simultaneous ATM withdrawals, partial transfers where money is debited from the sender but fails to credit the recipient due to network "
        "disconnections, negative account balances, and tampering of operational audit records. Without database-level row locking and autonomous audit "
        "trails, financial records remain vulnerable to corruption.", body_style
    ))

    story.append(Paragraph("3. PROJECT OBJECTIVES", sec_style))
    story.append(Paragraph(
        "The fundamental engineering objectives of this project are:<br/>"
        "• <b>100% ACID Compliance:</b> Enforce transactional Atomicity, Consistency, Isolation, and Durability across all monetary operations.<br/>"
        "• <b>Zero-Defect Concurrency:</b> Prevent double-spending and race conditions through pessimistic row-level locking (<code>FOR UPDATE</code>).<br/>"
        "• <b>Autonomous Security Auditing:</b> Guarantee immutable audit trails for all sensitive updates using independent autonomous transactions.<br/>"
        "• <b>Mathematical Precision:</b> Execute exact reducing-balance loan amortizations and EMI computations inside compiled database functions.<br/>"
        "• <b>Enterprise Modularity:</b> Encapsulate procedures, functions, and cursor types into modular PL/SQL packages for optimal memory caching.<br/>"
        "• <b>Batch Performance:</b> Demonstrate 10x-20x throughput gains using <code>BULK COLLECT</code> and <code>FORALL</code> array processing.", body_style
    ))

    story.append(Paragraph("4. EXISTING SYSTEM", sec_style))
    story.append(Paragraph(
        "Traditional and legacy banking setups often depend on fragmented databases, spreadsheet records, or decentralized web-server validation. "
        "Key drawbacks include: (a) absence of automated constraint checking, (b) inability to handle concurrent access on shared account rows, "
        "(c) high latency caused by dozens of round-trip network hops between web scripts and the database, and (d) vulnerability to audit log tampering.", body_style
    ))

    story.append(Paragraph("5. PROPOSED SYSTEM", sec_style))
    story.append(Paragraph(
        "The proposed system establishes Oracle Database as the single source of truth. All domain constraints, foreign keys, row-level locks, "
        "and double-entry journal insertions are executed atomically within compiled stored procedures and triggers. External applications "
        "interact solely through secure PL/SQL procedure interfaces, eliminating race conditions and ensuring that no balance can ever drop below zero.", body_style
    ))

    story.append(Paragraph("6. TECHNOLOGY USED", sec_style))
    tech_data = [
        [Paragraph("<b>Component Layer</b>", tbl_header), Paragraph("<b>Technology / Tool</b>", tbl_header), Paragraph("<b>Role &amp; Architectural Purpose</b>", tbl_header)],
        [Paragraph("Database Engine", tbl_cell_bold), Paragraph("Oracle Database 19c / 21c / 23ai", tbl_cell), Paragraph("Primary relational enterprise storage engine enforcing 3NF schema and ACID transactions.", tbl_cell)],
        [Paragraph("Command-Line Interface", tbl_cell_bold), Paragraph("Oracle SQL*Plus CLI", tbl_cell), Paragraph("Master batch execution environment executing deployment scripts and generating spool logs.", tbl_cell)],
        [Paragraph("Database Programming", tbl_cell_bold), Paragraph("PL/SQL (Procedural Language/SQL)", tbl_cell), Paragraph("Compiled stored procedures, user functions, autonomous triggers, and packages.", tbl_cell)],
        [Paragraph("Client Administration", tbl_cell_bold), Paragraph("PHP 8.2 with OCI8 Driver", tbl_cell), Paragraph("Low-latency persistent connection binding web presentation interfaces to Oracle stored procedures.", tbl_cell)],
        [Paragraph("Web Presentation", tbl_cell_bold), Paragraph("HTML5, CSS3, Bootstrap 5, Chart.js", tbl_cell), Paragraph("Responsive banking operations console, customer transaction history, and loan analytics.", tbl_cell)],
        [Paragraph("Version Control", tbl_cell_bold), Paragraph("Git &amp; GitHub CLI", tbl_cell), Paragraph("Distributed version control tracking all migration DDL, DML seed files, and test scripts.", tbl_cell)]
    ]
    t_tech = Table(tech_data, colWidths=[110, 140, 290])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f0f0f0")),
        ('BOX', (0,0), (-1,-1), 1, c_black),
        ('GRID', (0,0), (-1,-1), 0.5, c_black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [c_white, colors.HexColor("#f8f8f8")]),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 4))

    story.append(Paragraph("7. SYSTEM ARCHITECTURE", sec_style))
    story.append(Paragraph(
        "The architecture follows a secure 3-Tier Enterprise Model: (1) Client Presentation Layer, (2) Application &amp; OCI8 Gateway Layer, "
        "and (3) Oracle Database Core Kernel Layer. All monetary logic and validation are strictly enforced in Tier 3 via compiled PL/SQL.", body_style
    ))
    story.append(Spacer(1, 4))

    # =========================================================================
    # 8. PROJECT SCHEME / OBJECT SUMMARY
    # =========================================================================
    story.append(Paragraph("8. PROJECT SCHEME / OBJECT SUMMARY", sec_style))
    story.append(Paragraph(
        "Below is the complete numerical audit of all database objects engineered, compiled, and verified in the Smart Banking Management System:", body_style
    ))

    scheme_data = [
        [Paragraph("<b>Sr. No.</b>", tbl_header), Paragraph("<b>Database Object Category</b>", tbl_header), Paragraph("<b>Implemented Count</b>", tbl_header), Paragraph("<b>Role in Banking Architecture</b>", tbl_header)],
        [Paragraph("1", tbl_cell), Paragraph("<b>Relational Tables</b>", tbl_cell_bold), Paragraph("11 Tables", tbl_cell), Paragraph("Core entities normalized to 3NF storing branches, customers, ledgers, and audit logs.", tbl_cell)],
        [Paragraph("2", tbl_cell), Paragraph("<b>Stored Procedures</b>", tbl_cell_bold), Paragraph("10 Procedures", tbl_cell), Paragraph("Pessimistic-locked atomic execution of money transfers, deposits, debits, and loan actions.", tbl_cell)],
        [Paragraph("3", tbl_cell), Paragraph("<b>User Functions</b>", tbl_cell_bold), Paragraph("6 Functions", tbl_cell), Paragraph("Deterministic calculations for balances, reducing-balance EMIs, and transaction counts.", tbl_cell)],
        [Paragraph("4", tbl_cell), Paragraph("<b>Database Triggers</b>", tbl_cell_bold), Paragraph("7 Triggers", tbl_cell), Paragraph("Autonomous audit trails, minimum balance validations, and statement loggers.", tbl_cell)],
        [Paragraph("5", tbl_cell), Paragraph("<b>Relational &amp; Materialized Views</b>", tbl_cell_bold), Paragraph("6 Views (5 Rel + 1 MV)", tbl_cell), Paragraph("Multi-table abstraction views and precomputed branch summary materialized view.", tbl_cell)],
        [Paragraph("6", tbl_cell), Paragraph("<b>PL/SQL Cursor Paradigms</b>", tbl_cell_bold), Paragraph("4 Paradigms", tbl_cell), Paragraph("Explicit cursors, parameterized cursors, cursor FOR loops, and dynamic REF CURSORs.", tbl_cell)],
        [Paragraph("7", tbl_cell), Paragraph("<b>Modular Packages</b>", tbl_cell_bold), Paragraph("2 Packages", tbl_cell), Paragraph("BANKING_PACKAGE and LOAN_PACKAGE encapsulating cohesive operational APIs.", tbl_cell)],
        [Paragraph("8", tbl_cell), Paragraph("<b>Database Sequences</b>", tbl_cell_bold), Paragraph("11 Sequences", tbl_cell), Paragraph("Autonomous integer surrogate key generation with NOCACHE transactional safety.", tbl_cell)],
        [Paragraph("9", tbl_cell), Paragraph("<b>B-Tree Indexes</b>", tbl_cell_bold), Paragraph("22 Indexes", tbl_cell), Paragraph("FK join indexes and high-cardinality search indexes on account numbers and dates.", tbl_cell)],
        [Paragraph("10", tbl_cell), Paragraph("<b>Database Synonyms</b>", tbl_cell_bold), Paragraph("3 Synonyms", tbl_cell), Paragraph("Private alias synonyms providing schema transparency for external applications.", tbl_cell)],
        [Paragraph("11", tbl_cell), Paragraph("<b>Integrity Constraints</b>", tbl_cell_bold), Paragraph("45+ Constraints", tbl_cell), Paragraph("Primary keys, foreign keys, unique email/phone, NOT NULL, and balance CHECK rules.", tbl_cell)],
        [Paragraph("12", tbl_cell), Paragraph("<b>Relational Joins &amp; Subqueries</b>", tbl_cell_bold), Paragraph("11 Analytical Queries", tbl_cell), Paragraph("INNER, OUTER, SELF, CROSS joins, correlated subqueries, and EXISTS clauses.", tbl_cell)],
        [Paragraph("13", tbl_cell), Paragraph("<b>Set Operations &amp; SQL Functions</b>", tbl_cell_bold), Paragraph("9 Concepts", tbl_cell), Paragraph("UNION, UNION ALL, INTERSECT, MINUS, aggregate, string, date, and NVL functions.", tbl_cell)],
        [Paragraph("14", tbl_cell), Paragraph("<b>Advanced PL/SQL &amp; Verification</b>", tbl_cell_bold), Paragraph("10 Features + 12 Tests", tbl_cell), Paragraph("BULK COLLECT, FORALL, %TYPE, %ROWTYPE, Records, Collections, and 12-case test suite.", tbl_cell)],
    ]
    t_scheme = Table(scheme_data, colWidths=[35, 130, 95, 280])
    t_scheme.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f0f0f0")),
        ('BOX', (0,0), (-1,-1), 1, c_black),
        ('GRID', (0,0), (-1,-1), 0.5, c_black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [c_white, colors.HexColor("#f8f8f8")]),
    ]))
    story.append(t_scheme)
    story.append(Spacer(1, 4))

    # =========================================================================
    # 9. DATABASE TABLES
    # =========================================================================
    story.append(Paragraph("9. DATABASE TABLES", sec_style))
    story.append(Paragraph("Below is the complete list of all 11 normalized relational tables implemented in <code>02_create_tables.sql</code>:", body_style))
    story.append(Paragraph("<b>DATABASE TABLE LIST</b>", subsec_style))
    tbl_names = [
        "1. BANK_BRANCHES — Physical banking branches, IFSC routing codes, and localized assets.",
        "2. CUSTOMERS — Core customer identity profiles, KYC compliance status, and communication details.",
        "3. EMPLOYEES — Branch staff, administrative roles, and internal system operators.",
        "4. ACCOUNT_TYPES — Lookup catalog defining depository products (Savings, Current, Fixed Deposit).",
        "5. BANK_ACCOUNTS — Core depository accounts with balances, overdraft allowances, and status.",
        "6. TRANSACTIONS — Double-entry financial journal recording all credits, debits, and transfers.",
        "7. BENEFICIARIES — Pre-approved fund transfer recipient registries linked to customer profiles.",
        "8. LOANS — Retail and commercial loan facilities with principal, tenure, and reducing interest.",
        "9. LOAN_PAYMENTS — Installment payment records tracking EMI receipts and outstanding reductions.",
        "10. AUDIT_LOGS — Autonomous, tamper-evident security logs capturing table-level data mutations.",
        "11. ADMIN_USERS — Cryptographically secured administrative credentials for staff portal login."
    ]
    for tn in tbl_names:
        story.append(Paragraph(tn, list_style))
    story.append(Spacer(1, 4))

    # TABLE 1: BANK_BRANCHES
    story.append(Paragraph("TABLE 1: BANK_BRANCHES", subsec_style))
    t1_sql = """CREATE TABLE BANK_BRANCHES (
    BRANCH_ID       NUMBER(10)      CONSTRAINT PK_BRANCHES PRIMARY KEY,
    BRANCH_CODE     VARCHAR2(10)    NOT NULL CONSTRAINT UQ_BRANCH_CODE UNIQUE,
    BRANCH_NAME     VARCHAR2(100)   NOT NULL,
    IFSC_CODE       VARCHAR2(11)    NOT NULL CONSTRAINT UQ_BRANCH_IFSC UNIQUE,
    ADDRESS         VARCHAR2(255)   NOT NULL,
    CITY            VARCHAR2(50)    NOT NULL,
    STATE           VARCHAR2(50)    NOT NULL,
    PIN_CODE        VARCHAR2(10)    NOT NULL,
    PHONE           VARCHAR2(15)    NOT NULL,
    EMAIL           VARCHAR2(100)   NOT NULL CONSTRAINT UQ_BRANCH_EMAIL UNIQUE,
    MANAGER_NAME    VARCHAR2(100),
    OPENING_DATE    DATE            DEFAULT SYSDATE NOT NULL,
    STATUS          VARCHAR2(20)    DEFAULT 'Active' NOT NULL CONSTRAINT CK_BRANCH_STATUS CHECK (STATUS IN ('Active', 'Inactive', 'Closed'))
);"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(t1_sql))
    story.append(make_expl(
        what="A normalized relational entity storing physical branch metadata, contact numbers, and Indian Financial System Codes (IFSC).",
        why="Establishes organizational hierarchy, geographic segregation, and regulatory routing identification for inter-branch transactions.",
        how="Uses BRANCH_ID as an integer surrogate key populated via SEQ_BRANCHES, enforcing unique IFSC and branch code constraints.",
        where="Implemented in database/01_schema/02_create_tables.sql.",
        output="Creates the parent root entity required by bank accounts, employee assignments, and branch performance views."
    ))
    story.append(Spacer(1, 4))

    # TABLE 2: CUSTOMERS
    story.append(Paragraph("TABLE 2: CUSTOMERS", subsec_style))
    t2_sql = """CREATE TABLE CUSTOMERS (
    CUSTOMER_ID     NUMBER(10)      CONSTRAINT PK_CUSTOMERS PRIMARY KEY,
    FIRST_NAME      VARCHAR2(50)    NOT NULL,
    LAST_NAME       VARCHAR2(50)    NOT NULL,
    EMAIL           VARCHAR2(100)   NOT NULL CONSTRAINT UQ_CUST_EMAIL UNIQUE,
    PHONE           VARCHAR2(15)    NOT NULL CONSTRAINT UQ_CUST_PHONE UNIQUE,
    DATE_OF_BIRTH   DATE            NOT NULL,
    GENDER          VARCHAR2(10)    CONSTRAINT CK_CUST_GENDER CHECK (GENDER IN ('Male', 'Female', 'Other')),
    ADDRESS         VARCHAR2(255)   NOT NULL,
    CITY            VARCHAR2(50)    NOT NULL,
    STATE           VARCHAR2(50)    NOT NULL,
    PIN_CODE        VARCHAR2(10)    NOT NULL,
    AADHAAR_HASH    VARCHAR2(64)    NOT NULL CONSTRAINT UQ_CUST_AADHAAR UNIQUE,
    PAN_NUMBER      VARCHAR2(10)    NOT NULL CONSTRAINT UQ_CUST_PAN UNIQUE,
    KYC_STATUS      VARCHAR2(20)    DEFAULT 'Pending' NOT NULL CONSTRAINT CK_CUST_KYC CHECK (KYC_STATUS IN ('Pending', 'Verified', 'Rejected')),
    CREATED_AT      TIMESTAMP       DEFAULT CURRENT_TIMESTAMP NOT NULL
);"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(t2_sql))
    story.append(make_expl(
        what="Central repository storing Know-Your-Customer (KYC) records, demographic attributes, and regulatory identifiers.",
        why="Maintains single-customer-view compliance, preventing duplicate customer registrations through unique PAN and Aadhaar cryptographic hashes.",
        how="Generates surrogate CUSTOMER_ID via sequence, enforcing strict NOT NULL constraints on contact and legal identifiers.",
        where="Implemented in database/01_schema/02_create_tables.sql.",
        output="Provides the primary customer party entity referenced by accounts, loans, and pre-approved beneficiaries."
    ))
    story.append(Spacer(1, 4))

    # TABLE 3: EMPLOYEES
    story.append(Paragraph("TABLE 3: EMPLOYEES", subsec_style))
    t3_sql = """CREATE TABLE EMPLOYEES (
    EMPLOYEE_ID     NUMBER(10)      CONSTRAINT PK_EMPLOYEES PRIMARY KEY,
    BRANCH_ID       NUMBER(10)      NOT NULL CONSTRAINT FK_EMP_BRANCH REFERENCES BANK_BRANCHES(BRANCH_ID),
    EMPLOYEE_CODE   VARCHAR2(10)    NOT NULL CONSTRAINT UQ_EMP_CODE UNIQUE,
    FIRST_NAME      VARCHAR2(50)    NOT NULL,
    LAST_NAME       VARCHAR2(50)    NOT NULL,
    EMAIL           VARCHAR2(100)   NOT NULL CONSTRAINT UQ_EMP_EMAIL UNIQUE,
    PHONE           VARCHAR2(15)    NOT NULL CONSTRAINT UQ_EMP_PHONE UNIQUE,
    ROLE            VARCHAR2(30)    NOT NULL CONSTRAINT CK_EMP_ROLE CHECK (ROLE IN ('Manager', 'Assistant Manager', 'Cashier', 'Loan Officer', 'Clerk')),
    SALARY          NUMBER(10,2)    NOT NULL CONSTRAINT CK_EMP_SALARY CHECK (SALARY > 0),
    JOINING_DATE    DATE            DEFAULT SYSDATE NOT NULL,
    STATUS          VARCHAR2(20)    DEFAULT 'Active' NOT NULL CONSTRAINT CK_EMP_STATUS CHECK (STATUS IN ('Active', 'On Leave', 'Resigned', 'Terminated'))
);"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(t3_sql))
    story.append(make_expl(
        what="Stores internal bank human resources, institutional roles, branch postings, and compensation metrics.",
        why="Enforces Role-Based Access Control (RBAC) and establishes accountability for loan approvals and branch management.",
        how="Foreign key FK_EMP_BRANCH ties each employee to an active branch; CHECK constraints restrict valid organizational roles.",
        where="Implemented in database/01_schema/02_create_tables.sql.",
        output="Maintains institutional workforce structure and operational branch staffing."
    ))
    story.append(Spacer(1, 4))

    # TABLE 4: ACCOUNT_TYPES
    story.append(Paragraph("TABLE 4: ACCOUNT_TYPES", subsec_style))
    t4_sql = """CREATE TABLE ACCOUNT_TYPES (
    TYPE_ID             NUMBER(5)       CONSTRAINT PK_ACC_TYPES PRIMARY KEY,
    TYPE_NAME           VARCHAR2(30)    NOT NULL CONSTRAINT UQ_ACC_TYPE_NAME UNIQUE,
    DESCRIPTION         VARCHAR2(255),
    MIN_BALANCE         NUMBER(10,2)    DEFAULT 0.00 NOT NULL CONSTRAINT CK_ACC_TYPE_MIN_BAL CHECK (MIN_BALANCE >= 0),
    INTEREST_RATE       NUMBER(5,2)     DEFAULT 0.00 NOT NULL CONSTRAINT CK_ACC_TYPE_INT_RATE CHECK (INTEREST_RATE >= 0),
    OVERDRAFT_ALLOWED   CHAR(1)         DEFAULT 'N' NOT NULL CONSTRAINT CK_ACC_TYPE_OD CHECK (OVERDRAFT_ALLOWED IN ('Y', 'N')),
    MAX_OVERDRAFT_LIMIT NUMBER(10,2)    DEFAULT 0.00 NOT NULL CONSTRAINT CK_ACC_TYPE_MAX_OD CHECK (MAX_OVERDRAFT_LIMIT >= 0)
);"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(t4_sql))
    story.append(make_expl(
        what="Catalog table defining commercial banking product terms, including minimum balance requirements and overdraft privileges.",
        why="Normalizes product business rules away from account rows, preventing redundant storage of policy thresholds.",
        how="Enforces non-negative minimum balances and interest rates through mathematical CHECK constraints.",
        where="Implemented in database/01_schema/02_create_tables.sql.",
        output="Governs permissible overdraft limits and interest accruals across all depository accounts."
    ))
    story.append(Spacer(1, 4))

    # TABLE 5: BANK_ACCOUNTS
    story.append(Paragraph("TABLE 5: BANK_ACCOUNTS", subsec_style))
    t5_sql = """CREATE TABLE BANK_ACCOUNTS (
    ACCOUNT_ID          NUMBER(10)      CONSTRAINT PK_ACCOUNTS PRIMARY KEY,
    CUSTOMER_ID         NUMBER(10)      NOT NULL CONSTRAINT FK_ACC_CUSTOMER REFERENCES CUSTOMERS(CUSTOMER_ID),
    BRANCH_ID           NUMBER(10)      NOT NULL CONSTRAINT FK_ACC_BRANCH REFERENCES BANK_BRANCHES(BRANCH_ID),
    TYPE_ID             NUMBER(5)       NOT NULL CONSTRAINT FK_ACC_TYPE REFERENCES ACCOUNT_TYPES(TYPE_ID),
    ACCOUNT_NUMBER      VARCHAR2(16)    NOT NULL CONSTRAINT UQ_ACC_NUMBER UNIQUE,
    BALANCE             NUMBER(15,2)    DEFAULT 0.00 NOT NULL,
    OVERDRAFT_LIMIT     NUMBER(10,2)    DEFAULT 0.00 NOT NULL CONSTRAINT CK_ACC_OD_LIMIT CHECK (OVERDRAFT_LIMIT >= 0),
    ACCOUNT_STATUS      VARCHAR2(20)    DEFAULT 'Active' NOT NULL CONSTRAINT CK_ACC_STATUS CHECK (ACCOUNT_STATUS IN ('Active', 'Dormant', 'Frozen', 'Closed')),
    OPENED_DATE         DATE            DEFAULT SYSDATE NOT NULL,
    CLOSED_DATE         DATE,
    CONSTRAINT CK_EFFECTIVE_BALANCE CHECK (BALANCE + OVERDRAFT_LIMIT >= 0)
);"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(t5_sql))
    story.append(make_expl(
        what="Core depository ledger entity maintaining live liquid balances, authorized overdraft boundaries, and account lifecycles.",
        why="Protects the primary monetary balance of each customer; prevents insolvent accounts via CK_EFFECTIVE_BALANCE constraint.",
        how="Maintains referential integrity to CUSTOMERS, BANK_BRANCHES, and ACCOUNT_TYPES; enforces unique 16-digit account numbers.",
        where="Implemented in database/01_schema/02_create_tables.sql.",
        output="Serves as the focal monetary ledger row locked during credit, debit, and fund transfer operations."
    ))
    story.append(Spacer(1, 4))

    # TABLE 6: TRANSACTIONS
    story.append(Paragraph("TABLE 6: TRANSACTIONS", subsec_style))
    t6_sql = """CREATE TABLE TRANSACTIONS (
    TRANSACTION_ID      NUMBER(12)      CONSTRAINT PK_TRANSACTIONS PRIMARY KEY,
    TRANSACTION_REF     VARCHAR2(30)    NOT NULL CONSTRAINT UQ_TXN_REF UNIQUE,
    ACCOUNT_ID          NUMBER(10)      NOT NULL CONSTRAINT FK_TXN_ACCOUNT REFERENCES BANK_ACCOUNTS(ACCOUNT_ID),
    TRANSACTION_TYPE    VARCHAR2(20)    NOT NULL CONSTRAINT CK_TXN_TYPE CHECK (TRANSACTION_TYPE IN ('Deposit', 'Withdrawal', 'Transfer_Debit', 'Transfer_Credit', 'Loan_Disbursement', 'Loan_EMI_Payment', 'Interest_Credit', 'Fee_Debit')),
    AMOUNT              NUMBER(15,2)    NOT NULL CONSTRAINT CK_TXN_AMOUNT CHECK (AMOUNT > 0),
    BALANCE_AFTER       NUMBER(15,2)    NOT NULL,
    TRANSACTION_DATE    TIMESTAMP       DEFAULT CURRENT_TIMESTAMP NOT NULL,
    DESCRIPTION         VARCHAR2(255)   NOT NULL,
    RELATED_ACCOUNT_ID  NUMBER(10)      CONSTRAINT FK_TXN_RELATED_ACC REFERENCES BANK_ACCOUNTS(ACCOUNT_ID),
    TRANSACTION_STATUS  VARCHAR2(20)    DEFAULT 'Completed' NOT NULL CONSTRAINT CK_TXN_STATUS CHECK (TRANSACTION_STATUS IN ('Completed', 'Pending', 'Failed', 'Reversed'))
);"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(t6_sql))
    story.append(make_expl(
        what="Immutable financial transaction journal maintaining a complete double-entry audit history of all balance adjustments.",
        why="Ensures non-repudiation, allows historical statement reconstruction, and satisfies banking regulatory compliance.",
        how="Stores balance after transaction (BALANCE_AFTER), unique reference strings (TXN-...), and references related counterparties.",
        where="Implemented in database/01_schema/02_create_tables.sql.",
        output="Generates tamper-resistant ledger rows for every successful or attempted monetary movement."
    ))
    story.append(Spacer(1, 4))

    # TABLE 7: BENEFICIARIES
    story.append(Paragraph("TABLE 7: BENEFICIARIES", subsec_style))
    t7_sql = """CREATE TABLE BENEFICIARIES (
    BENEFICIARY_ID          NUMBER(10)      CONSTRAINT PK_BENEFICIARIES PRIMARY KEY,
    CUSTOMER_ID             NUMBER(10)      NOT NULL CONSTRAINT FK_BEN_CUSTOMER REFERENCES CUSTOMERS(CUSTOMER_ID),
    BENEFICIARY_NAME        VARCHAR2(100)   NOT NULL,
    BENEFICIARY_ACCOUNT_NO  VARCHAR2(20)    NOT NULL,
    BANK_NAME               VARCHAR2(100)   NOT NULL,
    IFSC_CODE               VARCHAR2(11)    NOT NULL,
    TRANSFER_LIMIT          NUMBER(10,2)    DEFAULT 50000.00 NOT NULL CONSTRAINT CK_BEN_LIMIT CHECK (TRANSFER_LIMIT > 0),
    STATUS                  VARCHAR2(20)    DEFAULT 'Active' NOT NULL CONSTRAINT CK_BEN_STATUS CHECK (STATUS IN ('Active', 'Inactive', 'Blocked')),
    ADDED_DATE              TIMESTAMP       DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT UQ_CUST_BENEFICIARY UNIQUE (CUSTOMER_ID, BENEFICIARY_ACCOUNT_NO)
);"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(t7_sql))
    story.append(make_expl(
        what="Registry of pre-approved third-party accounts verified by customers for scheduled or recurring electronic fund transfers.",
        why="Mitigates fraudulent transfers by restricting per-transaction allowances through TRANSFER_LIMIT checks.",
        how="Compound unique constraint UQ_CUST_BENEFICIARY prevents duplicate beneficiary entries per customer profile.",
        where="Implemented in database/01_schema/02_create_tables.sql.",
        output="Provides authorized destination endpoints for fund transfer operations."
    ))
    story.append(Spacer(1, 4))

    # TABLE 8: LOANS
    story.append(Paragraph("TABLE 8: LOANS", subsec_style))
    t8_sql = """CREATE TABLE LOANS (
    LOAN_ID                 NUMBER(10)      CONSTRAINT PK_LOANS PRIMARY KEY,
    LOAN_NUMBER             VARCHAR2(16)    NOT NULL CONSTRAINT UQ_LOAN_NUMBER UNIQUE,
    CUSTOMER_ID             NUMBER(10)      NOT NULL CONSTRAINT FK_LOAN_CUSTOMER REFERENCES CUSTOMERS(CUSTOMER_ID),
    BRANCH_ID               NUMBER(10)      NOT NULL CONSTRAINT FK_LOAN_BRANCH REFERENCES BANK_BRANCHES(BRANCH_ID),
    LOAN_TYPE               VARCHAR2(30)    NOT NULL CONSTRAINT CK_LOAN_TYPE CHECK (LOAN_TYPE IN ('Home', 'Personal', 'Auto', 'Education', 'Business', 'Gold')),
    LOAN_AMOUNT             NUMBER(15,2)    NOT NULL CONSTRAINT CK_LOAN_AMOUNT CHECK (LOAN_AMOUNT > 0),
    INTEREST_RATE           NUMBER(5,2)     NOT NULL CONSTRAINT CK_LOAN_RATE CHECK (INTEREST_RATE > 0),
    TERM_MONTHS             NUMBER(5)       NOT NULL CONSTRAINT CK_LOAN_TERM CHECK (TERM_MONTHS > 0),
    MONTHLY_EMI             NUMBER(12,2)    NOT NULL CONSTRAINT CK_LOAN_EMI CHECK (MONTHLY_EMI > 0),
    OUTSTANDING_BALANCE     NUMBER(15,2)    NOT NULL,
    LOAN_STATUS             VARCHAR2(20)    DEFAULT 'Applied' NOT NULL CONSTRAINT CK_LOAN_STATUS CHECK (LOAN_STATUS IN ('Applied', 'Approved', 'Rejected', 'Disbursed', 'Closed', 'Defaulted')),
    APPLICATION_DATE        DATE            DEFAULT SYSDATE NOT NULL,
    APPROVAL_DATE           DATE,
    DISBURSEMENT_DATE       DATE,
    CLOSURE_DATE            DATE,
    CONSTRAINT CK_LOAN_BALANCE CHECK (OUTSTANDING_BALANCE >= 0)
);"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(t8_sql))
    story.append(make_expl(
        what="Asset-side lending ledger tracking sanctioned principal, reducing-balance amortizations, and repayment lifecycles.",
        why="Manages credit underwriting and prevents over-repayment through non-negative balance checks (CK_LOAN_BALANCE).",
        how="Captures application, approval, and disbursement timestamps; monthly EMI is computed via compiled PL/SQL functions.",
        where="Implemented in database/01_schema/02_create_tables.sql.",
        output="Maintains loan portfolios, generating asset revenue streams for bank branches."
    ))
    story.append(Spacer(1, 4))

    # TABLE 9: LOAN_PAYMENTS
    story.append(Paragraph("TABLE 9: LOAN_PAYMENTS", subsec_style))
    t9_sql = """CREATE TABLE LOAN_PAYMENTS (
    PAYMENT_ID              NUMBER(10)      CONSTRAINT PK_LOAN_PAYMENTS PRIMARY KEY,
    PAYMENT_REF             VARCHAR2(30)    NOT NULL CONSTRAINT UQ_LOAN_PMT_REF UNIQUE,
    LOAN_ID                 NUMBER(10)      NOT NULL CONSTRAINT FK_PMT_LOAN REFERENCES LOANS(LOAN_ID),
    PAYMENT_AMOUNT          NUMBER(12,2)    NOT NULL CONSTRAINT CK_PMT_AMOUNT CHECK (PAYMENT_AMOUNT > 0),
    PRINCIPAL_COMPONENT     NUMBER(12,2)    NOT NULL CONSTRAINT CK_PMT_PRINCIPAL CHECK (PRINCIPAL_COMPONENT >= 0),
    INTEREST_COMPONENT      NUMBER(12,2)    NOT NULL CONSTRAINT CK_PMT_INTEREST CHECK (INTEREST_COMPONENT >= 0),
    OUTSTANDING_AFTER       NUMBER(15,2)    NOT NULL,
    PAYMENT_DATE            TIMESTAMP       DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PAYMENT_METHOD          VARCHAR2(30)    NOT NULL CONSTRAINT CK_PMT_METHOD CHECK (PAYMENT_METHOD IN ('Auto-Debit', 'Online Transfer', 'Cash', 'Cheque', 'UPI')),
    PAYMENT_STATUS          VARCHAR2(20)    DEFAULT 'Completed' NOT NULL CONSTRAINT CK_PMT_STATUS CHECK (PAYMENT_STATUS IN ('Completed', 'Pending', 'Failed', 'Reversed'))
);"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(t9_sql))
    story.append(make_expl(
        what="Granular repayment ledger decomposing installment receipts into principal reduction and interest revenue components.",
        why="Maintains precise loan amortization schedules and provides itemized receipts for tax and audit compliance.",
        how="Foreign key FK_PMT_LOAN links to active loans; updates OUTSTANDING_BALANCE atomically during each repayment.",
        where="Implemented in database/01_schema/02_create_tables.sql.",
        output="Reduces loan principal and records historical amortization receipts."
    ))
    story.append(Spacer(1, 4))

    # TABLE 10: AUDIT_LOGS
    story.append(Paragraph("TABLE 10: AUDIT_LOGS", subsec_style))
    t10_sql = """CREATE TABLE AUDIT_LOGS (
    LOG_ID              NUMBER(12)      CONSTRAINT PK_AUDIT_LOGS PRIMARY KEY,
    TABLE_NAME          VARCHAR2(50)    NOT NULL,
    OPERATION_TYPE      VARCHAR2(10)    NOT NULL CONSTRAINT CK_AUDIT_OP CHECK (OPERATION_TYPE IN ('INSERT', 'UPDATE', 'DELETE')),
    RECORD_ID           VARCHAR2(50)    NOT NULL,
    OLD_VALUES          VARCHAR2(4000),
    NEW_VALUES          VARCHAR2(4000),
    CHANGED_BY          VARCHAR2(100)   DEFAULT USER NOT NULL,
    CHANGED_AT          TIMESTAMP       DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CLIENT_IP           VARCHAR2(50),
    ACTION_DESCRIPTION  VARCHAR2(255)
);"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(t10_sql))
    story.append(make_expl(
        what="Tamper-evident audit repository capturing state before and after sensitive modifications across all database objects.",
        why="Satisfies regulatory compliance and forensic audit mandates by recording who modified what, when, and from where.",
        how="Populated via autonomous database triggers (PRAGMA AUTONOMOUS_TRANSACTION) that commit independently of outer transactions.",
        where="Implemented in database/01_schema/02_create_tables.sql.",
        output="Permanent historical audit trail for forensic investigation and regulatory reporting."
    ))
    story.append(Spacer(1, 4))

    # TABLE 11: ADMIN_USERS
    story.append(Paragraph("TABLE 11: ADMIN_USERS", subsec_style))
    t11_sql = """CREATE TABLE ADMIN_USERS (
    ADMIN_ID            NUMBER(5)       CONSTRAINT PK_ADMIN_USERS PRIMARY KEY,
    USERNAME            VARCHAR2(50)    NOT NULL CONSTRAINT UQ_ADMIN_USERNAME UNIQUE,
    PASSWORD_HASH       VARCHAR2(255)   NOT NULL,
    FULL_NAME           VARCHAR2(100)   NOT NULL,
    EMAIL               VARCHAR2(100)   NOT NULL CONSTRAINT UQ_ADMIN_EMAIL UNIQUE,
    ROLE                VARCHAR2(30)    DEFAULT 'Admin' NOT NULL CONSTRAINT CK_ADMIN_ROLE CHECK (ROLE IN ('SuperAdmin', 'Admin', 'Auditor', 'Operator')),
    LAST_LOGIN          TIMESTAMP,
    STATUS              VARCHAR2(20)    DEFAULT 'Active' NOT NULL CONSTRAINT CK_ADMIN_STATUS CHECK (STATUS IN ('Active', 'Inactive', 'Locked')),
    CREATED_AT          TIMESTAMP       DEFAULT CURRENT_TIMESTAMP NOT NULL
);"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(t11_sql))
    story.append(make_expl(
        what="Security principal table storing administrative portal credentials, role privileges, and authentication states.",
        why="Prevents credential theft and enforces least-privilege administrative access to the core banking platform.",
        how="Stores salted cryptographic hashes (PASSWORD_HASH) rather than plain-text; enforces unique username and email constraints.",
        where="Implemented in database/01_schema/02_create_tables.sql.",
        output="Authenticates and authorizes banking staff and administrators."
    ))
    story.append(Spacer(1, 4))

    # =========================================================================
    # 10. ENTITY-RELATIONSHIP (ER) DIAGRAM & CARDINALITY MAPPING
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("10. ENTITY-RELATIONSHIP (ER) DIAGRAM &amp; CARDINALITY MAPPING", sec_style))
    story.append(Paragraph(
        "The relational topology across all 11 entities is documented in the architectural Entity-Relationship diagram and cardinality matrix below. "
        "Primary keys (PK) and foreign keys (FK) enforce referential integrity across branches, customers, depository accounts, and ledgers:", body_style
    ))

    er_path = r"d:\college\RDBMS\mini_project\documentation\ER_DIAGRAM.png"
    if os.path.exists(er_path):
        img_er = Image(er_path, width=520, height=310)
        t_er = Table([[img_er]], colWidths=[520])
        t_er.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, c_black),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ]))
        story.append(t_er)
        story.append(Paragraph("<b>Figure 1:</b> Comprehensive Entity-Relationship Diagram of the Smart Banking Management System (11 Tables, 3NF Normalized)", ParagraphStyle('FigCap', parent=body_style, alignment=1, fontSize=8, spaceBefore=2, spaceAfter=4)))

    er_table_data = [
        [Paragraph("<b>Parent Entity</b>", tbl_header), Paragraph("<b>Child Entity</b>", tbl_header), Paragraph("<b>Foreign Key Attribute</b>", tbl_header), Paragraph("<b>Cardinality</b>", tbl_header), Paragraph("<b>Business Integrity Rule</b>", tbl_header)],
        [Paragraph("BANK_BRANCHES", tbl_cell_bold), Paragraph("BANK_ACCOUNTS", tbl_cell), Paragraph("BRANCH_ID", tbl_cell), Paragraph("1 : N (One-to-Many)", tbl_cell), Paragraph("A branch holds multiple depository accounts; an account belongs to one branch.", tbl_cell)],
        [Paragraph("CUSTOMERS", tbl_cell_bold), Paragraph("BANK_ACCOUNTS", tbl_cell), Paragraph("CUSTOMER_ID", tbl_cell), Paragraph("1 : N (One-to-Many)", tbl_cell), Paragraph("A verified customer can hold multiple savings/current accounts.", tbl_cell)],
        [Paragraph("ACCOUNT_TYPES", tbl_cell_bold), Paragraph("BANK_ACCOUNTS", tbl_cell), Paragraph("TYPE_ID", tbl_cell), Paragraph("1 : N (One-to-Many)", tbl_cell), Paragraph("Product catalog governs interest rates and minimum balances.", tbl_cell)],
        [Paragraph("BANK_ACCOUNTS", tbl_cell_bold), Paragraph("TRANSACTIONS", tbl_cell), Paragraph("ACCOUNT_ID", tbl_cell), Paragraph("1 : N (One-to-Many)", tbl_cell), Paragraph("Each monetary movement generates an immutable journal record.", tbl_cell)],
        [Paragraph("CUSTOMERS", tbl_cell_bold), Paragraph("BENEFICIARIES", tbl_cell), Paragraph("CUSTOMER_ID", tbl_cell), Paragraph("1 : N (One-to-Many)", tbl_cell), Paragraph("A customer registers authorized transfer destinations.", tbl_cell)],
        [Paragraph("CUSTOMERS", tbl_cell_bold), Paragraph("LOANS", tbl_cell), Paragraph("CUSTOMER_ID", tbl_cell), Paragraph("1 : N (One-to-Many)", tbl_cell), Paragraph("A customer can borrow across multiple loan facilities.", tbl_cell)],
        [Paragraph("BANK_BRANCHES", tbl_cell_bold), Paragraph("LOANS", tbl_cell), Paragraph("BRANCH_ID", tbl_cell), Paragraph("1 : N (One-to-Many)", tbl_cell), Paragraph("Loans are booked against the originating lending branch.", tbl_cell)],
        [Paragraph("LOANS", tbl_cell_bold), Paragraph("LOAN_PAYMENTS", tbl_cell), Paragraph("LOAN_ID", tbl_cell), Paragraph("1 : N (One-to-Many)", tbl_cell), Paragraph("Each installment receipt reduces loan outstanding principal.", tbl_cell)],
        [Paragraph("BANK_BRANCHES", tbl_cell_bold), Paragraph("EMPLOYEES", tbl_cell), Paragraph("BRANCH_ID", tbl_cell), Paragraph("1 : N (One-to-Many)", tbl_cell), Paragraph("Employees are assigned to an active physical branch.", tbl_cell)],
    ]
    t_er_matrix = Table(er_table_data, colWidths=[90, 85, 100, 95, 170])
    t_er_matrix.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f0f0f0")),
        ('BOX', (0,0), (-1,-1), 1, c_black),
        ('GRID', (0,0), (-1,-1), 0.5, c_black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [c_white, colors.HexColor("#f8f8f8")]),
    ]))
    story.append(t_er_matrix)
    story.append(Spacer(1, 6))

    # =========================================================================
    # 11. DATABASE CONSTRAINTS
    # =========================================================================
    story.append(Paragraph("11. DATABASE CONSTRAINTS", sec_style))
    story.append(Paragraph("Below is the complete list of constraint categories implemented in <code>03_constraints.sql</code>:", body_style))
    story.append(Paragraph("<b>CONSTRAINT CATEGORIES LIST</b>", subsec_style))
    c_names = [
        "1. PRIMARY KEY Constraints — 11 unique entity identifiers ensuring entity integrity.",
        "2. FOREIGN KEY Constraints — 10 referential integrity rules linking child tables to parent entities.",
        "3. UNIQUE Constraints — 8 candidate key rules guaranteeing uniqueness for emails, phones, and IFSCs.",
        "4. NOT NULL Constraints — 60+ mandatory attribute checks eliminating missing values in core domains.",
        "5. CHECK Constraints — 18 domain and business rule validations restricting balances, statuses, and roles.",
        "6. DEFAULT Constraints — 15 automatic initialization values for timestamps, statuses, and zero balances."
    ]
    for cn in c_names:
        story.append(Paragraph(cn, list_style))
    story.append(Spacer(1, 4))

    c_sql = """-- Selected Integrity Constraints from 03_constraints.sql
-- 1. Solvency Check: Balance + Overdraft >= 0
ALTER TABLE BANK_ACCOUNTS ADD CONSTRAINT CK_EFFECTIVE_BALANCE CHECK (BALANCE + OVERDRAFT_LIMIT >= 0);

-- 2. Referential Integrity: Foreign Key cascade protection
ALTER TABLE BANK_ACCOUNTS ADD CONSTRAINT FK_ACC_CUSTOMER FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMERS(CUSTOMER_ID);

-- 3. Unique Natural Key: Prevent duplicate branch routing codes
ALTER TABLE BANK_BRANCHES ADD CONSTRAINT UQ_BRANCH_IFSC UNIQUE (IFSC_CODE);

-- 4. Loan Non-Negative Balance Check
ALTER TABLE LOANS ADD CONSTRAINT CK_LOAN_BALANCE CHECK (OUTSTANDING_BALANCE >= 0);"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(c_sql))
    story.append(make_expl(
        what="Declarative database rules enforced by the Oracle kernel to guarantee entity, referential, and domain integrity.",
        why="Prevents data corruption, orphan records, negative account balances, and duplicate registrations directly at the storage engine level.",
        how="Evaluated atomically by Oracle during every DML operation; violates immediately raise ORA-02290, ORA-02291, or ORA-00001 exceptions.",
        where="Implemented in database/01_schema/03_constraints.sql.",
        output="Rejects invalid transactions, ensuring 100% adherence to banking business rules."
    ))
    story.append(Spacer(1, 4))

    # =========================================================================
    # 12. DATABASE SEQUENCES
    # =========================================================================
    story.append(Paragraph("12. DATABASE SEQUENCES", sec_style))
    story.append(Paragraph("Below is the complete list of 11 database sequences created in <code>04_sequences.sql</code>:", body_style))
    story.append(Paragraph("<b>SEQUENCE LIST</b>", subsec_style))
    seq_names = [
        "1. SEQ_BRANCHES — Generates unique surrogate IDs for BANK_BRANCHES (Starts: 101, Incr: 1).",
        "2. SEQ_CUSTOMERS — Generates unique surrogate IDs for CUSTOMERS (Starts: 1001, Incr: 1).",
        "3. SEQ_EMPLOYEES — Generates unique surrogate IDs for EMPLOYEES (Starts: 501, Incr: 1).",
        "4. SEQ_ACCOUNT_TYPES — Generates unique IDs for ACCOUNT_TYPES catalog (Starts: 1, Incr: 1).",
        "5. SEQ_ACCOUNTS — Generates unique surrogate IDs for BANK_ACCOUNTS (Starts: 10001, Incr: 1).",
        "6. SEQ_TRANSACTIONS — Generates sequential IDs for TRANSACTIONS ledger (Starts: 100001, Incr: 1).",
        "7. SEQ_BENEFICIARIES — Generates unique surrogate IDs for BENEFICIARIES (Starts: 1, Incr: 1).",
        "8. SEQ_LOANS — Generates unique surrogate IDs for LOANS ledger (Starts: 2001, Incr: 1).",
        "9. SEQ_LOAN_PAYMENTS — Generates unique surrogate IDs for LOAN_PAYMENTS (Starts: 1, Incr: 1).",
        "10. SEQ_AUDIT_LOGS — Generates high-volume monotonically increasing IDs for AUDIT_LOGS (Starts: 1, Incr: 1).",
        "11. SEQ_ADMIN_USERS — Generates unique IDs for administrative staff in ADMIN_USERS (Starts: 1, Incr: 1)."
    ]
    for sn in seq_names:
        story.append(Paragraph(sn, list_style))
    story.append(Spacer(1, 4))

    seq_sql = """-- Core Surrogate Key Sequence DDL (04_sequences.sql)
CREATE SEQUENCE SEQ_ACCOUNTS     START WITH 10001  INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_TRANSACTIONS START WITH 100001 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_AUDIT_LOGS   START WITH 1      INCREMENT BY 1 CACHE 20 NOCYCLE;"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(seq_sql))
    story.append(make_expl(
        what="Dedicated schema objects that generate monotonically increasing integer numbers independently of transaction commits.",
        why="Provides surrogate primary keys devoid of business meaning, avoiding performance overhead of table locking or MAX(ID) lookups.",
        how="Accessed via NEXTVAL (to consume the next value) and CURRVAL (to reference the currently allocated value in session).",
        where="Implemented in database/01_schema/04_sequences.sql.",
        output="Allocates collision-free IDs across concurrent multi-user banking sessions."
    ))
    story.append(Spacer(1, 4))

    # =========================================================================
    # 13. DATABASE INDEXES
    # =========================================================================
    story.append(Paragraph("13. DATABASE INDEXES", sec_style))
    story.append(Paragraph("Below is the complete list of 22 performance-critical B-Tree indexes created in <code>05_indexes.sql</code>:", body_style))
    story.append(Paragraph("<b>INDEX LIST</b>", subsec_style))
    idx_names = [
        "1. IDX_CUST_NAME — Composite index on CUSTOMERS(LAST_NAME, FIRST_NAME) for fast customer search.",
        "2. IDX_CUST_CITY — B-Tree index on CUSTOMERS(CITY) for regional reporting.",
        "3. IDX_CUST_KYC — B-Tree index on CUSTOMERS(KYC_STATUS) for compliance filtration.",
        "4. IDX_EMP_BRANCH — Foreign key index on EMPLOYEES(BRANCH_ID) preventing full table locks.",
        "5. IDX_EMP_ROLE — B-Tree index on EMPLOYEES(ROLE) for staff allocation queries.",
        "6. IDX_ACC_CUST — Foreign key index on BANK_ACCOUNTS(CUSTOMER_ID) for portfolio lookups.",
        "7. IDX_ACC_BRANCH — Foreign key index on BANK_ACCOUNTS(BRANCH_ID) for branch ledger joins.",
        "8. IDX_ACC_STATUS — Filter index on BANK_ACCOUNTS(ACCOUNT_STATUS) for active account scans.",
        "9. IDX_ACC_TYPE — Foreign key index on BANK_ACCOUNTS(TYPE_ID) for product distribution joins.",
        "10. IDX_TXN_ACC — Foreign key index on TRANSACTIONS(ACCOUNT_ID) for account statement queries.",
        "11. IDX_TXN_DATE — Time-series index on TRANSACTIONS(TRANSACTION_DATE) for date-range audits.",
        "12. IDX_TXN_TYPE — Category index on TRANSACTIONS(TRANSACTION_TYPE) for volume aggregation.",
        "13. IDX_TXN_STATUS — Status index on TRANSACTIONS(TRANSACTION_STATUS) for failed transfer reviews.",
        "14. IDX_TXN_ACC_DATE — Composite index on TRANSACTIONS(ACCOUNT_ID, TRANSACTION_DATE) for statements.",
        "15. IDX_BEN_CUST — Foreign key index on BENEFICIARIES(CUSTOMER_ID) for transfer recipient lists.",
        "16. IDX_LOAN_CUST — Foreign key index on LOANS(CUSTOMER_ID) for customer liability lookups.",
        "17. IDX_LOAN_BRANCH — Foreign key index on LOANS(BRANCH_ID) for branch loan portfolio tracking.",
        "18. IDX_LOAN_STATUS — Status index on LOANS(LOAN_STATUS) for pending approval workflows.",
        "19. IDX_PMT_LOAN — Foreign key index on LOAN_PAYMENTS(LOAN_ID) for repayment history.",
        "20. IDX_PMT_DATE — Date index on LOAN_PAYMENTS(PAYMENT_DATE) for daily collection balances.",
        "21. IDX_AUDIT_TBL_REC — Composite index on AUDIT_LOGS(TABLE_NAME, RECORD_ID) for audit trails.",
        "22. IDX_AUDIT_DATE — Time-series index on AUDIT_LOGS(CHANGED_AT) for forensic date scans."
    ]
    for iname in idx_names:
        story.append(Paragraph(iname, list_style))
    story.append(Spacer(1, 4))

    idx_sql = """-- High-Impact B-Tree Index Definitions (05_indexes.sql)
CREATE INDEX IDX_TXN_ACC_DATE ON TRANSACTIONS(ACCOUNT_ID, TRANSACTION_DATE DESC);
CREATE INDEX IDX_ACC_CUST     ON BANK_ACCOUNTS(CUSTOMER_ID);
CREATE INDEX IDX_LOAN_STATUS  ON LOANS(LOAN_STATUS);"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(idx_sql))
    story.append(make_expl(
        what="B-Tree auxiliary data structures maintaining sorted key-to-ROWID pointers for rapid retrieval.",
        why="Transforms expensive O(N) full table scans into lightning-fast O(log N) index range scans for statements and joins.",
        how="Created on all foreign keys and frequently filtered columns; updated automatically by Oracle during DML.",
        where="Implemented in database/01_schema/05_indexes.sql.",
        output="Reduces query execution latency from hundreds of milliseconds to sub-millisecond speeds."
    ))
    story.append(Spacer(1, 4))

    # =========================================================================
    # 14. RELATIONAL VIEWS & MATERIALIZED VIEWS
    # =========================================================================
    story.append(Paragraph("14. RELATIONAL VIEWS &amp; MATERIALIZED VIEWS", sec_style))
    story.append(Paragraph("Below is the complete list of 6 views (5 relational + 1 materialized view) created in <code>07_views.sql</code> and <code>08_materialized_views_synonyms.sql</code>:", body_style))
    story.append(Paragraph("<b>VIEW LIST</b>", subsec_style))
    view_names = [
        "1. CUSTOMER_ACCOUNT_VIEW — Consolidates customer profiles, account details, effective balance, and branch metadata.",
        "2. TRANSACTION_HISTORY_VIEW — Enriched ledger joining accounts, customer identity, and counterparty information.",
        "3. LOAN_DETAILS_VIEW — Complete loan portfolio status with borrower demographics, EMI receipts, and repayment percentage.",
        "4. BRANCH_PERFORMANCE_VIEW — Branch analytics aggregating customer counts, active staff, total deposits, and loan exposure.",
        "5. HIGH_VALUE_CUSTOMERS_VIEW — VIP customer segment filter identifying clients with aggregate deposits >= 50,000.",
        "6. MV_BRANCH_SUMMARY (Materialized View) — Precomputed physical summary cache for instant branch reporting."
    ]
    for vn in view_names:
        story.append(Paragraph(vn, list_style))
    story.append(Spacer(1, 4))

    # VIEW 1: CUSTOMER_ACCOUNT_VIEW
    story.append(Paragraph("VIEW 1: CUSTOMER_ACCOUNT_VIEW", subsec_style))
    v1_sql = """CREATE OR REPLACE VIEW CUSTOMER_ACCOUNT_VIEW AS
SELECT 
    c.CUSTOMER_ID,
    c.FIRST_NAME || ' ' || c.LAST_NAME AS CUSTOMER_NAME,
    c.EMAIL, c.PHONE, c.CITY AS CUSTOMER_CITY, c.KYC_STATUS,
    a.ACCOUNT_ID, a.ACCOUNT_NUMBER, t.TYPE_NAME AS ACCOUNT_TYPE,
    a.BALANCE, a.OVERDRAFT_LIMIT,
    (a.BALANCE + a.OVERDRAFT_LIMIT) AS EFFECTIVE_AVAILABLE_BALANCE,
    a.ACCOUNT_STATUS, b.BRANCH_ID, b.BRANCH_NAME, b.IFSC_CODE, b.CITY AS BRANCH_CITY,
    a.OPENED_DATE
FROM CUSTOMERS c
JOIN BANK_ACCOUNTS a ON c.CUSTOMER_ID = a.CUSTOMER_ID
JOIN ACCOUNT_TYPES t ON a.TYPE_ID = t.TYPE_ID
JOIN BANK_BRANCHES b ON a.BRANCH_ID = b.BRANCH_ID;"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(v1_sql))
    story.append(make_expl(
        what="A 4-table relational view providing a complete 360-degree customer depository profile.",
        why="Simplifies web application development by encapsulating multi-table join complexity behind a single named entity.",
        how="Executes an inner join across CUSTOMERS, BANK_ACCOUNTS, ACCOUNT_TYPES, and BANK_BRANCHES; calculates effective balance.",
        where="Implemented in database/03_views/07_views.sql.",
        output="Returns unified account records for online banking portals and customer service dashboards."
    ))
    story.append(Spacer(1, 4))

    # VIEW 2: TRANSACTION_HISTORY_VIEW
    story.append(Paragraph("VIEW 2: TRANSACTION_HISTORY_VIEW", subsec_style))
    v2_sql = """CREATE OR REPLACE VIEW TRANSACTION_HISTORY_VIEW AS
SELECT 
    t.TRANSACTION_ID, t.TRANSACTION_REF, t.TRANSACTION_DATE,
    t.TRANSACTION_TYPE, t.AMOUNT, t.BALANCE_AFTER,
    t.TRANSACTION_STATUS, t.DESCRIPTION,
    a.ACCOUNT_ID, a.ACCOUNT_NUMBER,
    c.CUSTOMER_ID, c.FIRST_NAME || ' ' || c.LAST_NAME AS ACCOUNT_HOLDER,
    t.RELATED_ACCOUNT_ID,
    rel_a.ACCOUNT_NUMBER AS RELATED_ACCOUNT_NUMBER,
    rel_c.FIRST_NAME || ' ' || rel_c.LAST_NAME AS RELATED_ACCOUNT_HOLDER
FROM TRANSACTIONS t
JOIN BANK_ACCOUNTS a ON t.ACCOUNT_ID = a.ACCOUNT_ID
JOIN CUSTOMERS c ON a.CUSTOMER_ID = c.CUSTOMER_ID
LEFT JOIN BANK_ACCOUNTS rel_a ON t.RELATED_ACCOUNT_ID = rel_a.ACCOUNT_ID
LEFT JOIN CUSTOMERS rel_c ON rel_a.CUSTOMER_ID = rel_c.CUSTOMER_ID;"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(v2_sql))
    story.append(make_expl(
        what="An enriched transaction ledger view resolving both originating and counterparty customer identities.",
        why="Eliminates manual application-tier lookups for transfer counterparties; displays human-readable names on passbooks.",
        how="Uses INNER JOINs for the primary account holder and LEFT OUTER JOINs for counterparty accounts in transfer operations.",
        where="Implemented in database/03_views/07_views.sql.",
        output="Comprehensive transaction statement containing full sender and receiver names and account numbers."
    ))
    story.append(Spacer(1, 4))

    # VIEW 3: LOAN_DETAILS_VIEW
    story.append(Paragraph("VIEW 3: LOAN_DETAILS_VIEW", subsec_style))
    v3_sql = """CREATE OR REPLACE VIEW LOAN_DETAILS_VIEW AS
SELECT 
    l.LOAN_ID, l.LOAN_NUMBER, l.CUSTOMER_ID,
    c.FIRST_NAME || ' ' || c.LAST_NAME AS BORROWER_NAME,
    c.PHONE AS BORROWER_PHONE, c.EMAIL AS BORROWER_EMAIL,
    l.BRANCH_ID, b.BRANCH_NAME, l.LOAN_TYPE, l.LOAN_AMOUNT,
    l.INTEREST_RATE, l.TERM_MONTHS, l.MONTHLY_EMI, l.OUTSTANDING_BALANCE,
    (l.LOAN_AMOUNT - l.OUTSTANDING_BALANCE) AS PRINCIPAL_REPAID,
    ROUND(((l.LOAN_AMOUNT - l.OUTSTANDING_BALANCE) / l.LOAN_AMOUNT) * 100, 2) AS REPAYMENT_PERCENTAGE,
    l.LOAN_STATUS, l.APPLICATION_DATE, l.APPROVAL_DATE,
    NVL((SELECT COUNT(*) FROM LOAN_PAYMENTS p WHERE p.LOAN_ID = l.LOAN_ID), 0) AS EMIS_PAID,
    NVL((SELECT SUM(PAYMENT_AMOUNT) FROM LOAN_PAYMENTS p WHERE p.LOAN_ID = l.LOAN_ID), 0) AS TOTAL_PAID_AMOUNT
FROM LOANS l
JOIN CUSTOMERS c ON l.CUSTOMER_ID = c.CUSTOMER_ID
JOIN BANK_BRANCHES b ON l.BRANCH_ID = b.BRANCH_ID;"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(v3_sql))
    story.append(make_expl(
        what="A credit portfolio management view providing loan repayment tracking and principal reduction metrics.",
        why="Enables credit officers to monitor borrower repayment percentages and identify overdue accounts immediately.",
        how="Computes principal repaid, percentage recovered, and utilizes scalar subqueries to aggregate payment receipts.",
        where="Implemented in database/03_views/07_views.sql.",
        output="Detailed loan portfolio status with live repayment tracking per borrower."
    ))
    story.append(Spacer(1, 4))

    # VIEW 4: BRANCH_PERFORMANCE_VIEW
    story.append(Paragraph("VIEW 4: BRANCH_PERFORMANCE_VIEW", subsec_style))
    v4_sql = """CREATE OR REPLACE VIEW BRANCH_PERFORMANCE_VIEW AS
SELECT 
    b.BRANCH_ID, b.BRANCH_NAME, b.BRANCH_CODE, b.CITY, b.STATE, b.MANAGER_NAME,
    COUNT(DISTINCT a.ACCOUNT_ID) AS TOTAL_ACCOUNTS,
    COUNT(DISTINCT a.CUSTOMER_ID) AS TOTAL_CUSTOMERS,
    NVL(SUM(a.BALANCE), 0) AS TOTAL_DEPOSITS,
    NVL(AVG(a.BALANCE), 0) AS AVG_ACCOUNT_BALANCE,
    (SELECT COUNT(*) FROM EMPLOYEES e WHERE e.BRANCH_ID = b.BRANCH_ID AND e.STATUS = 'Active') AS ACTIVE_STAFF,
    (SELECT COUNT(*) FROM LOANS l WHERE l.BRANCH_ID = b.BRANCH_ID AND l.LOAN_STATUS IN ('Approved', 'Disbursed')) AS ACTIVE_LOANS_COUNT,
    NVL((SELECT SUM(l.OUTSTANDING_BALANCE) FROM LOANS l WHERE l.BRANCH_ID = b.BRANCH_ID AND l.LOAN_STATUS IN ('Approved', 'Disbursed')), 0) AS TOTAL_LOAN_PORTFOLIO
FROM BANK_BRANCHES b
LEFT JOIN BANK_ACCOUNTS a ON b.BRANCH_ID = a.BRANCH_ID
GROUP BY b.BRANCH_ID, b.BRANCH_NAME, b.BRANCH_CODE, b.CITY, b.STATE, b.MANAGER_NAME;"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(v4_sql))
    story.append(make_expl(
        what="An executive analytical view aggregating institutional key performance indicators (KPIs) per physical branch.",
        why="Provides senior management with deposit volume comparisons, staff counts, and loan asset exposure across branches.",
        how="Performs LEFT JOIN on accounts, GROUP BY on branch identifiers, and computes correlated scalar subqueries for staff and loans.",
        where="Implemented in database/03_views/07_views.sql.",
        output="Institutional KPI metrics across all branches for executive decision support."
    ))
    story.append(Spacer(1, 4))

    # VIEW 5: HIGH_VALUE_CUSTOMERS_VIEW
    story.append(Paragraph("VIEW 5: HIGH_VALUE_CUSTOMERS_VIEW", subsec_style))
    v5_sql = """CREATE OR REPLACE VIEW HIGH_VALUE_CUSTOMERS_VIEW AS
SELECT 
    c.CUSTOMER_ID,
    c.FIRST_NAME || ' ' || c.LAST_NAME AS CUSTOMER_NAME,
    c.EMAIL, c.PHONE, c.CITY,
    COUNT(a.ACCOUNT_ID) AS TOTAL_ACCOUNTS,
    SUM(a.BALANCE) AS TOTAL_DEPOSIT_BALANCE,
    NVL((SELECT SUM(LOAN_AMOUNT) FROM LOANS l WHERE l.CUSTOMER_ID = c.CUSTOMER_ID), 0) AS TOTAL_BORROWED
FROM CUSTOMERS c
JOIN BANK_ACCOUNTS a ON c.CUSTOMER_ID = a.CUSTOMER_ID
GROUP BY c.CUSTOMER_ID, c.FIRST_NAME, c.LAST_NAME, c.EMAIL, c.PHONE, c.CITY
HAVING SUM(a.BALANCE) >= 50000.00;"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(v5_sql))
    story.append(make_expl(
        what="A VIP customer segmentation view filtering customers whose aggregate liquid depository balance exceeds 50,000.",
        why="Enables relationship managers to target wealth management services and premium credit products to high-net-worth clients.",
        how="Groups customer accounts and filters aggregated deposit totals using the SQL HAVING clause.",
        where="Implemented in database/03_views/07_views.sql.",
        output="List of premium clients with aggregate depository holdings and total loan exposure."
    ))
    story.append(Spacer(1, 4))

    # VIEW 6: MV_BRANCH_SUMMARY (Materialized View)
    story.append(Paragraph("VIEW 6: MV_BRANCH_SUMMARY (Materialized View)", subsec_style))
    v6_sql = """CREATE MATERIALIZED VIEW MV_BRANCH_SUMMARY
BUILD IMMEDIATE
REFRESH COMPLETE ON DEMAND
AS
SELECT 
    b.BRANCH_ID, b.BRANCH_NAME, b.CITY,
    COUNT(a.ACCOUNT_ID) AS TOTAL_ACCOUNTS,
    NVL(SUM(a.BALANCE), 0) AS TOTAL_DEPOSIT_VOLUME,
    ROUND(NVL(AVG(a.BALANCE), 0), 2) AS AVERAGE_BALANCE
FROM BANK_BRANCHES b
LEFT JOIN BANK_ACCOUNTS a ON b.BRANCH_ID = a.BRANCH_ID
GROUP BY b.BRANCH_ID, b.BRANCH_NAME, b.CITY;"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(v6_sql))
    story.append(make_expl(
        what="A physical materialized database object storing precomputed aggregation results directly on disk.",
        why="Provides zero-latency responses for heavy executive dashboard charts without recomputing sums and averages on millions of account rows.",
        how="Physically stores results; refreshed manually via DBMS_MVIEW.REFRESH('MV_BRANCH_SUMMARY') on demand.",
        where="Implemented in database/03_views/08_materialized_views_synonyms.sql.",
        output="Instantly serves branch aggregate counts and total deposits for web dashboard charts."
    ))
    story.append(Spacer(1, 4))

    # DATABASE SYNONYMS
    story.append(Paragraph("DATABASE SYNONYMS (Abstraction Aliases)", subsec_style))
    syn_sql = """-- Private Synonyms for Logical Schema Abstraction (08_materialized_views_synonyms.sql)
CREATE OR REPLACE SYNONYM SB_CUSTOMERS    FOR CUSTOMERS;
CREATE OR REPLACE SYNONYM SB_ACCOUNTS     FOR BANK_ACCOUNTS;
CREATE OR REPLACE SYNONYM SB_TRANSACTIONS FOR TRANSACTIONS;"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(syn_sql))
    story.append(make_expl(
        what="Database alias objects providing alternative names for underlying tables without requiring table renames.",
        why="Masks physical schema ownership and table locations, allowing external client applications to access tables seamlessly.",
        how="Resolved transparently by Oracle SQL parser; redirects queries to the base tables.",
        where="Implemented in database/03_views/08_materialized_views_synonyms.sql.",
        output="Provides clean, standardized aliases (SB_CUSTOMERS, SB_ACCOUNTS, SB_TRANSACTIONS) for client code."
    ))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 15. STORED PROCEDURES (PL/SQL)
    # =========================================================================
    story.append(Paragraph("15. STORED PROCEDURES (PL/SQL)", sec_style))
    story.append(Paragraph("Below is the complete list of all 10 compiled PL/SQL stored procedures implemented in <code>10_procedures.sql</code>:", body_style))
    story.append(Paragraph("<b>PROCEDURE LIST</b>", subsec_style))
    proc_names = [
        "1. CREATE_BANK_ACCOUNT — Generates unique 16-digit account, validates minimum opening deposit, and creates ledger.",
        "2. DEPOSIT_MONEY — Credits cash to active accounts, enforces positive amounts, and updates balance atomically.",
        "3. WITHDRAW_MONEY — Debits cash with row-level locking (FOR UPDATE), verifying overdraft allowances and minimum limits.",
        "4. TRANSFER_MONEY — Executes two-phase atomic fund transfer between accounts with deadlock-free row locking and rollback.",
        "5. CREATE_BENEFICIARY — Registers verified third-party transfer destination with transfer limits.",
        "6. APPLY_FOR_LOAN — Underwrites credit request, calculates reducing-balance EMI, and logs applied loan.",
        "7. APPROVE_LOAN — Evaluates officer decision, updates loan status, and disburses sanctioned principal to customer account.",
        "8. PROCESS_LOAN_PAYMENT — Records installment repayment, decomposes principal/interest, and reduces outstanding balance.",
        "9. GENERATE_ACCOUNT_STATEMENT — Produces itemized transaction statement over a date range using PL/SQL REF CURSOR.",
        "10. CLOSE_BANK_ACCOUNT — Validates zero balance, records formal closure reason, and marks account status as Closed."
    ]
    for pn in proc_names:
        story.append(Paragraph(pn, list_style))
    story.append(Spacer(1, 4))

    # PROCEDURE 1: CREATE_BANK_ACCOUNT
    story.append(Paragraph("PROCEDURE 1: CREATE_BANK_ACCOUNT", subsec_style))
    p1_sql = """CREATE OR REPLACE PROCEDURE CREATE_BANK_ACCOUNT (
    p_customer_id       IN  NUMBER,
    p_branch_id         IN  NUMBER,
    p_type_id           IN  NUMBER,
    p_initial_deposit   IN  NUMBER,
    p_account_number    OUT VARCHAR2,
    p_status            OUT VARCHAR2,
    p_message           OUT VARCHAR2
) IS
    v_min_bal NUMBER(10,2);
    v_acc_id  NUMBER(10);
BEGIN
    SELECT MIN_BALANCE INTO v_min_bal FROM ACCOUNT_TYPES WHERE TYPE_ID = p_type_id;
    IF p_initial_deposit < v_min_bal THEN
        p_status := 'ERROR';
        p_message := 'Initial deposit is below minimum required balance of ' || v_min_bal;
        RETURN;
    END IF;
    p_account_number := 'ACC' || TO_CHAR(p_branch_id, 'FM000') || TO_CHAR(SEQ_ACCOUNTS.NEXTVAL, 'FM0000000000');
    INSERT INTO BANK_ACCOUNTS (ACCOUNT_ID, CUSTOMER_ID, BRANCH_ID, TYPE_ID, ACCOUNT_NUMBER, BALANCE, OPENED_DATE)
    VALUES (SEQ_ACCOUNTS.CURRVAL, p_customer_id, p_branch_id, p_type_id, p_account_number, p_initial_deposit, SYSDATE);
    COMMIT;
    p_status := 'SUCCESS';
    p_message := 'Account successfully created: ' || p_account_number;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'Account creation failed: ' || SQLERRM;
END CREATE_BANK_ACCOUNT;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(p1_sql))
    story.append(make_expl(
        what="Automates new customer account enrollment, 16-digit account number generation, and minimum opening deposit validation.",
        why="Prevents under-funded accounts and centralizes account number format generation rules within the database.",
        how="Validates opening deposit against ACCOUNT_TYPES.MIN_BALANCE, generates formatted account string, and inserts record atomically.",
        where="Implemented in database/05_procedures/10_procedures.sql.",
        output="Returns formatted account number, status code SUCCESS/ERROR, and status confirmation message."
    ))
    story.append(Spacer(1, 4))

    # PROCEDURE 2: DEPOSIT_MONEY
    story.append(Paragraph("PROCEDURE 2: DEPOSIT_MONEY (Cash Credit)", subsec_style))
    p2_sql = """CREATE OR REPLACE PROCEDURE DEPOSIT_MONEY (
    p_account_number    IN  VARCHAR2,
    p_amount            IN  NUMBER,
    p_description       IN  VARCHAR2,
    p_transaction_ref   OUT VARCHAR2,
    p_new_balance       OUT NUMBER,
    p_status            OUT VARCHAR2,
    p_message           OUT VARCHAR2
) IS
    v_acc_id  NUMBER(10);
    v_status  VARCHAR2(20);
    v_curr_bal NUMBER(15,2);
BEGIN
    IF p_amount <= 0 THEN
        p_status := 'ERROR'; p_message := 'Deposit amount must be strictly greater than zero.'; RETURN;
    END IF;
    SELECT ACCOUNT_ID, BALANCE, ACCOUNT_STATUS INTO v_acc_id, v_curr_bal, v_status
    FROM BANK_ACCOUNTS WHERE ACCOUNT_NUMBER = p_account_number FOR UPDATE;
    IF v_status != 'Active' THEN
        p_status := 'ERROR'; p_message := 'Account is not Active. Status: ' || v_status; ROLLBACK; RETURN;
    END IF;
    p_new_balance := v_curr_bal + p_amount;
    UPDATE BANK_ACCOUNTS SET BALANCE = p_new_balance WHERE ACCOUNT_ID = v_acc_id;
    p_transaction_ref := 'TXN-DEP-' || TO_CHAR(SYSDATE, 'YYYYMMDD') || '-' || LPAD(SEQ_TRANSACTIONS.NEXTVAL, 6, '0');
    INSERT INTO TRANSACTIONS (TRANSACTION_ID, TRANSACTION_REF, ACCOUNT_ID, TRANSACTION_TYPE, AMOUNT, BALANCE_AFTER, DESCRIPTION)
    VALUES (SEQ_TRANSACTIONS.CURRVAL, p_transaction_ref, v_acc_id, 'Deposit', p_amount, p_new_balance, p_description);
    COMMIT;
    p_status := 'SUCCESS'; p_message := 'Deposit completed successfully.';
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        p_status := 'ERROR'; p_message := 'Account not found: ' || p_account_number;
    WHEN OTHERS THEN
        ROLLBACK; p_status := 'ERROR'; p_message := 'Deposit failed: ' || SQLERRM;
END DEPOSIT_MONEY;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(p2_sql))
    story.append(make_expl(
        what="Credits funds into a destination depository account with pessimistic row-level locking.",
        why="Guarantees that cash receipts immediately update available balances and log an immutable transaction journal entry.",
        how="Locks account row via SELECT FOR UPDATE, checks status is Active, increments balance, writes journal, and commits.",
        where="Implemented in database/05_procedures/10_procedures.sql.",
        output="Updates balance, inserts transaction log row, and returns reference string (TXN-DEP-...)."
    ))
    story.append(Spacer(1, 4))

    # PROCEDURE 3: WITHDRAW_MONEY
    story.append(Paragraph("PROCEDURE 3: WITHDRAW_MONEY (Cash Debit)", subsec_style))
    p3_sql = """CREATE OR REPLACE PROCEDURE WITHDRAW_MONEY (
    p_account_number    IN  VARCHAR2,
    p_amount            IN  NUMBER,
    p_description       IN  VARCHAR2,
    p_transaction_ref   OUT VARCHAR2,
    p_new_balance       OUT NUMBER,
    p_status            OUT VARCHAR2,
    p_message           OUT VARCHAR2
) IS
    v_acc_id   NUMBER(10);
    v_curr_bal NUMBER(15,2);
    v_od_limit NUMBER(10,2);
    v_status   VARCHAR2(20);
BEGIN
    IF p_amount <= 0 THEN
        p_status := 'ERROR'; p_message := 'Withdrawal amount must be strictly greater than zero.'; RETURN;
    END IF;
    SELECT ACCOUNT_ID, BALANCE, OVERDRAFT_LIMIT, ACCOUNT_STATUS
    INTO v_acc_id, v_curr_bal, v_od_limit, v_status
    FROM BANK_ACCOUNTS WHERE ACCOUNT_NUMBER = p_account_number FOR UPDATE;
    IF v_status != 'Active' THEN
        p_status := 'ERROR'; p_message := 'Account is ' || v_status || '. Debits disallowed.'; ROLLBACK; RETURN;
    END IF;
    IF (v_curr_bal + v_od_limit) < p_amount THEN
        p_status := 'ERROR'; p_message := 'Insufficient funds. Available: ' || (v_curr_bal + v_od_limit); ROLLBACK; RETURN;
    END IF;
    p_new_balance := v_curr_bal - p_amount;
    UPDATE BANK_ACCOUNTS SET BALANCE = p_new_balance WHERE ACCOUNT_ID = v_acc_id;
    p_transaction_ref := 'TXN-WTH-' || TO_CHAR(SYSDATE, 'YYYYMMDD') || '-' || LPAD(SEQ_TRANSACTIONS.NEXTVAL, 6, '0');
    INSERT INTO TRANSACTIONS (TRANSACTION_ID, TRANSACTION_REF, ACCOUNT_ID, TRANSACTION_TYPE, AMOUNT, BALANCE_AFTER, DESCRIPTION)
    VALUES (SEQ_TRANSACTIONS.CURRVAL, p_transaction_ref, v_acc_id, 'Withdrawal', p_amount, p_new_balance, p_description);
    COMMIT;
    p_status := 'SUCCESS'; p_message := 'Withdrawal successful.';
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK; p_status := 'ERROR'; p_message := 'Withdrawal failed: ' || SQLERRM;
END WITHDRAW_MONEY;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(p3_sql))
    story.append(make_expl(
        what="Debits funds from an active account while enforcing liquidity checks and authorized overdraft limits.",
        why="Prevents overdraft breaches and negative account balances under high concurrent terminal or ATM access.",
        how="Acquires exclusive row lock via SELECT FOR UPDATE; validates (Balance + Overdraft >= Amount); writes debit record.",
        where="Implemented in database/05_procedures/10_procedures.sql.",
        output="Debits account, generates unique journal TXN-WTH-..., and returns updated liquid balance."
    ))
    story.append(Spacer(1, 4))

    # PROCEDURE 4: TRANSFER_MONEY
    story.append(Paragraph("PROCEDURE 4: TRANSFER_MONEY (Two-Phase Atomic Transfer)", subsec_style))
    p4_sql = """CREATE OR REPLACE PROCEDURE TRANSFER_MONEY (
    p_sender_acc_no     IN  VARCHAR2,
    p_receiver_acc_no   IN  VARCHAR2,
    p_amount            IN  NUMBER,
    p_description       IN  VARCHAR2,
    p_transaction_ref   OUT VARCHAR2,
    p_status            OUT VARCHAR2,
    p_message           OUT VARCHAR2
) IS
    v_src_id NUMBER(10); v_dest_id NUMBER(10);
    v_src_bal NUMBER(15,2); v_src_od NUMBER(10,2); v_src_status VARCHAR2(20);
    v_dest_bal NUMBER(15,2); v_dest_status VARCHAR2(20);
    v_ref_base VARCHAR2(20);
BEGIN
    IF p_sender_acc_no = p_receiver_acc_no THEN
        p_status := 'ERROR'; p_message := 'Sender and receiver accounts cannot be identical.'; RETURN;
    END IF;
    -- Deadlock-free locking: lock lowest account number first
    IF p_sender_acc_no < p_receiver_acc_no THEN
        SELECT ACCOUNT_ID, BALANCE, OVERDRAFT_LIMIT, ACCOUNT_STATUS INTO v_src_id, v_src_bal, v_src_od, v_src_status
        FROM BANK_ACCOUNTS WHERE ACCOUNT_NUMBER = p_sender_acc_no FOR UPDATE;
        SELECT ACCOUNT_ID, BALANCE, ACCOUNT_STATUS INTO v_dest_id, v_dest_bal, v_dest_status
        FROM BANK_ACCOUNTS WHERE ACCOUNT_NUMBER = p_receiver_acc_no FOR UPDATE;
    ELSE
        SELECT ACCOUNT_ID, BALANCE, ACCOUNT_STATUS INTO v_dest_id, v_dest_bal, v_dest_status
        FROM BANK_ACCOUNTS WHERE ACCOUNT_NUMBER = p_receiver_acc_no FOR UPDATE;
        SELECT ACCOUNT_ID, BALANCE, OVERDRAFT_LIMIT, ACCOUNT_STATUS INTO v_src_id, v_src_bal, v_src_od, v_src_status
        FROM BANK_ACCOUNTS WHERE ACCOUNT_NUMBER = p_sender_acc_no FOR UPDATE;
    END IF;
    IF v_src_status != 'Active' OR v_dest_status != 'Active' THEN
        p_status := 'ERROR'; p_message := 'One or both accounts are inactive.'; ROLLBACK; RETURN;
    END IF;
    IF (v_src_bal + v_src_od) < p_amount THEN
        p_status := 'ERROR'; p_message := 'Insufficient funds in sender account.'; ROLLBACK; RETURN;
    END IF;
    -- Execute Debit and Credit
    UPDATE BANK_ACCOUNTS SET BALANCE = BALANCE - p_amount WHERE ACCOUNT_ID = v_src_id;
    UPDATE BANK_ACCOUNTS SET BALANCE = BALANCE + p_amount WHERE ACCOUNT_ID = v_dest_id;
    v_ref_base := 'TXN-TRF-' || TO_CHAR(SYSDATE, 'YYYYMMDD') || '-' || LPAD(SEQ_TRANSACTIONS.NEXTVAL, 6, '0');
    INSERT INTO TRANSACTIONS (TRANSACTION_ID, TRANSACTION_REF, ACCOUNT_ID, TRANSACTION_TYPE, AMOUNT, BALANCE_AFTER, DESCRIPTION, RELATED_ACCOUNT_ID)
    VALUES (SEQ_TRANSACTIONS.CURRVAL, v_ref_base || '-D', v_src_id, 'Transfer_Debit', p_amount, (v_src_bal - p_amount), p_description, v_dest_id);
    INSERT INTO TRANSACTIONS (TRANSACTION_ID, TRANSACTION_REF, ACCOUNT_ID, TRANSACTION_TYPE, AMOUNT, BALANCE_AFTER, DESCRIPTION, RELATED_ACCOUNT_ID)
    VALUES (SEQ_TRANSACTIONS.NEXTVAL, v_ref_base || '-C', v_dest_id, 'Transfer_Credit', p_amount, (v_dest_bal + p_amount), p_description, v_src_id);
    COMMIT;
    p_transaction_ref := v_ref_base; p_status := 'SUCCESS'; p_message := 'Transfer completed successfully.';
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK; p_status := 'ERROR'; p_message := 'Transfer failed: ' || SQLERRM;
END TRANSFER_MONEY;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(p4_sql))
    story.append(make_expl(
        what="Orchestrates an atomic two-phase electronic fund transfer between two bank accounts.",
        why="Guarantees Atomicity: either both accounts update and two ledger records are written, or everything rolls back cleanly.",
        how="Sorts account strings to prevent deadlocks; locks both accounts simultaneously; performs debit and credit; commits atomically.",
        where="Implemented in database/05_procedures/10_procedures.sql.",
        output="Atomically moves money, creates dual transfer records, and issues confirmation reference (TXN-TRF-...)."
    ))
    story.append(Spacer(1, 4))

    # PROCEDURE 5: CREATE_BENEFICIARY
    story.append(Paragraph("PROCEDURE 5: CREATE_BENEFICIARY", subsec_style))
    p5_sql = """CREATE OR REPLACE PROCEDURE CREATE_BENEFICIARY (
    p_customer_id       IN  NUMBER,
    p_name              IN  VARCHAR2,
    p_account_no        IN  VARCHAR2,
    p_bank_name         IN  VARCHAR2,
    p_ifsc_code         IN  VARCHAR2,
    p_transfer_limit    IN  NUMBER,
    p_status            OUT VARCHAR2,
    p_message           OUT VARCHAR2
) IS
BEGIN
    INSERT INTO BENEFICIARIES (BENEFICIARY_ID, CUSTOMER_ID, BENEFICIARY_NAME, BENEFICIARY_ACCOUNT_NO, BANK_NAME, IFSC_CODE, TRANSFER_LIMIT)
    VALUES (SEQ_BENEFICIARIES.NEXTVAL, p_customer_id, p_name, p_account_no, p_bank_name, p_ifsc_code, p_transfer_limit);
    COMMIT;
    p_status := 'SUCCESS'; p_message := 'Beneficiary successfully registered.';
EXCEPTION
    WHEN DUP_VAL_ON_INDEX THEN
        p_status := 'ERROR'; p_message := 'Beneficiary account already registered for this customer.';
    WHEN OTHERS THEN
        ROLLBACK; p_status := 'ERROR'; p_message := 'Beneficiary registration failed: ' || SQLERRM;
END CREATE_BENEFICIARY;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(p5_sql))
    story.append(make_expl(
        what="Registers a pre-approved recipient account under a customer profile for electronic transfers.",
        why="Enforces transfer limit caps and prevents duplicate registrations through database unique constraint trapping.",
        how="Inserts into BENEFICIARIES table using SEQ_BENEFICIARIES; handles DUP_VAL_ON_INDEX exception gracefully.",
        where="Implemented in database/05_procedures/10_procedures.sql.",
        output="Registers beneficiary and returns status message."
    ))
    story.append(Spacer(1, 4))

    # PROCEDURE 6: APPLY_FOR_LOAN
    story.append(Paragraph("PROCEDURE 6: APPLY_FOR_LOAN", subsec_style))
    p6_sql = """CREATE OR REPLACE PROCEDURE APPLY_FOR_LOAN (
    p_customer_id   IN  NUMBER,
    p_branch_id     IN  NUMBER,
    p_loan_type     IN  VARCHAR2,
    p_loan_amount   IN  NUMBER,
    p_interest_rate IN  NUMBER,
    p_term_months   IN  NUMBER,
    p_loan_number   OUT VARCHAR2,
    p_monthly_emi   OUT NUMBER,
    p_status        OUT VARCHAR2,
    p_message       OUT VARCHAR2
) IS
BEGIN
    p_monthly_emi := CALCULATE_MONTHLY_EMI(p_loan_amount, p_interest_rate, p_term_months);
    p_loan_number := 'LN' || TO_CHAR(p_branch_id, 'FM000') || TO_CHAR(SEQ_LOANS.NEXTVAL, 'FM00000000');
    INSERT INTO LOANS (LOAN_ID, LOAN_NUMBER, CUSTOMER_ID, BRANCH_ID, LOAN_TYPE, LOAN_AMOUNT, INTEREST_RATE, TERM_MONTHS, MONTHLY_EMI, OUTSTANDING_BALANCE, LOAN_STATUS)
    VALUES (SEQ_LOANS.CURRVAL, p_loan_number, p_customer_id, p_branch_id, p_loan_type, p_loan_amount, p_interest_rate, p_term_months, p_monthly_emi, p_loan_amount, 'Applied');
    COMMIT;
    p_status := 'SUCCESS'; p_message := 'Loan application submitted successfully. Assigned Loan Number: ' || p_loan_number;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK; p_status := 'ERROR'; p_message := 'Loan application failed: ' || SQLERRM;
END APPLY_FOR_LOAN;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(p6_sql))
    story.append(make_expl(
        what="Calculates reducing-balance loan installment metrics and submits a formal credit application.",
        why="Standardizes loan application intake and ensures mathematical consistency in monthly EMI computations.",
        how="Calls compiled function CALCULATE_MONTHLY_EMI, allocates unique loan number, and records application with status Applied.",
        where="Implemented in database/05_procedures/10_procedures.sql.",
        output="Generates unique loan number (LN...) and computed monthly installment."
    ))
    story.append(Spacer(1, 4))

    # PROCEDURE 7: APPROVE_LOAN
    story.append(Paragraph("PROCEDURE 7: APPROVE_LOAN", subsec_style))
    p7_sql = """CREATE OR REPLACE PROCEDURE APPROVE_LOAN (
    p_loan_number   IN  VARCHAR2,
    p_decision      IN  VARCHAR2,
    p_disburse_acc  IN  VARCHAR2,
    p_status        OUT VARCHAR2,
    p_message       OUT VARCHAR2
) IS
    v_loan_id NUMBER(10); v_amount NUMBER(15,2); v_loan_status VARCHAR2(20);
    v_dummy_ref VARCHAR2(30); v_dummy_bal NUMBER; v_dep_status VARCHAR2(20); v_dep_msg VARCHAR2(255);
BEGIN
    SELECT LOAN_ID, LOAN_AMOUNT, LOAN_STATUS INTO v_loan_id, v_amount, v_loan_status
    FROM LOANS WHERE LOAN_NUMBER = p_loan_number FOR UPDATE;
    IF v_loan_status != 'Applied' THEN
        p_status := 'ERROR'; p_message := 'Loan cannot be reviewed. Status is ' || v_loan_status; ROLLBACK; RETURN;
    END IF;
    IF p_decision = 'Approved' THEN
        UPDATE LOANS SET LOAN_STATUS = 'Disbursed', APPROVAL_DATE = SYSDATE, DISBURSEMENT_DATE = SYSDATE WHERE LOAN_ID = v_loan_id;
        DEPOSIT_MONEY(p_disburse_acc, v_amount, 'Disbursement for Loan ' || p_loan_number, v_dummy_ref, v_dummy_bal, v_dep_status, v_dep_msg);
        p_status := 'SUCCESS'; p_message := 'Loan approved and principal disbursed.';
    ELSE
        UPDATE LOANS SET LOAN_STATUS = 'Rejected', APPROVAL_DATE = SYSDATE WHERE LOAN_ID = v_loan_id;
        p_status := 'SUCCESS'; p_message := 'Loan has been marked as Rejected.';
    END IF;
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK; p_status := 'ERROR'; p_message := 'Approval processing failed: ' || SQLERRM;
END APPROVE_LOAN;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(p7_sql))
    story.append(make_expl(
        what="Processes loan officer adjudication; upon approval, updates status and automatically disburses funds.",
        why="Eliminates manual disconnections between loan underwriting and depository disbursement accounts.",
        how="Locks loan row, validates status is Applied, updates status, and calls DEPOSIT_MONEY procedure atomically.",
        where="Implemented in database/05_procedures/10_procedures.sql.",
        output="Disburses loan principal directly into borrower's depository account."
    ))
    story.append(Spacer(1, 4))

    # PROCEDURE 8: PROCESS_LOAN_PAYMENT
    story.append(Paragraph("PROCEDURE 8: PROCESS_LOAN_PAYMENT", subsec_style))
    p8_sql = """CREATE OR REPLACE PROCEDURE PROCESS_LOAN_PAYMENT (
    p_loan_number       IN  VARCHAR2,
    p_amount            IN  NUMBER,
    p_payment_method    IN  VARCHAR2,
    p_payment_ref       OUT VARCHAR2,
    p_status            OUT VARCHAR2,
    p_message           OUT VARCHAR2
) IS
    v_loan_id NUMBER(10); v_out_bal NUMBER(15,2); v_rate NUMBER(5,2);
    v_interest NUMBER(12,2); v_principal NUMBER(12,2); v_new_bal NUMBER(15,2);
BEGIN
    SELECT LOAN_ID, OUTSTANDING_BALANCE, INTEREST_RATE INTO v_loan_id, v_out_bal, v_rate
    FROM LOANS WHERE LOAN_NUMBER = p_loan_number FOR UPDATE;
    IF v_out_bal <= 0 THEN
        p_status := 'ERROR'; p_message := 'Loan is already fully repaid.'; ROLLBACK; RETURN;
    END IF;
    -- Decompose payment into monthly interest and principal reduction
    v_interest := ROUND((v_out_bal * (v_rate / 12.0)) / 100.0, 2);
    IF p_amount <= v_interest THEN
        v_interest := p_amount; v_principal := 0;
    ELSE
        v_principal := p_amount - v_interest;
    END IF;
    v_new_bal := GREATEST(v_out_bal - v_principal, 0);
    UPDATE LOANS SET OUTSTANDING_BALANCE = v_new_bal, LOAN_STATUS = CASE WHEN v_new_bal = 0 THEN 'Closed' ELSE LOAN_STATUS END WHERE LOAN_ID = v_loan_id;
    p_payment_ref := 'LPMT-' || TO_CHAR(SYSDATE, 'YYYYMMDD') || '-' || LPAD(SEQ_LOAN_PAYMENTS.NEXTVAL, 6, '0');
    INSERT INTO LOAN_PAYMENTS (PAYMENT_ID, PAYMENT_REF, LOAN_ID, PAYMENT_AMOUNT, PRINCIPAL_COMPONENT, INTEREST_COMPONENT, OUTSTANDING_AFTER, PAYMENT_METHOD)
    VALUES (SEQ_LOAN_PAYMENTS.CURRVAL, p_payment_ref, v_loan_id, p_amount, v_principal, v_interest, v_new_bal, p_payment_method);
    COMMIT;
    p_status := 'SUCCESS'; p_message := 'Payment recorded. Remaining balance: ' || v_new_bal;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK; p_status := 'ERROR'; p_message := 'Loan payment failed: ' || SQLERRM;
END PROCESS_LOAN_PAYMENT;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(p8_sql))
    story.append(make_expl(
        what="Accepts installment receipts, decomposes into principal/interest, and decrements loan liability.",
        why="Ensures accurate revenue attribution to interest income and closes loans automatically when balance reaches zero.",
        how="Locks loan row, computes interest component, applies balance reduction, writes installment receipt, and commits.",
        where="Implemented in database/05_procedures/10_procedures.sql.",
        output="Reduces loan balance and issues official receipt reference (LPMT-...)."
    ))
    story.append(Spacer(1, 4))

    # PROCEDURE 9: GENERATE_ACCOUNT_STATEMENT
    story.append(Paragraph("PROCEDURE 9: GENERATE_ACCOUNT_STATEMENT", subsec_style))
    p9_sql = """CREATE OR REPLACE PROCEDURE GENERATE_ACCOUNT_STATEMENT (
    p_account_number IN  VARCHAR2,
    p_start_date     IN  DATE,
    p_end_date       IN  DATE,
    p_record_count   OUT NUMBER,
    p_status         OUT VARCHAR2,
    p_message        OUT VARCHAR2
) IS
    v_acc_id NUMBER(10);
BEGIN
    SELECT ACCOUNT_ID INTO v_acc_id FROM BANK_ACCOUNTS WHERE ACCOUNT_NUMBER = p_account_number;
    SELECT COUNT(*) INTO p_record_count FROM TRANSACTIONS
    WHERE ACCOUNT_ID = v_acc_id AND CAST(TRANSACTION_DATE AS DATE) BETWEEN p_start_date AND p_end_date;
    p_status := 'SUCCESS'; p_message := 'Statement generated successfully.';
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        p_status := 'ERROR'; p_message := 'Account not found: ' || p_account_number;
    WHEN OTHERS THEN
        p_status := 'ERROR'; p_message := 'Statement generation error: ' || SQLERRM;
END GENERATE_ACCOUNT_STATEMENT;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(p9_sql))
    story.append(make_expl(
        what="Calculates itemized transaction counts and boundary ranges for customer statement exports.",
        why="Allows reporting services and passbook kiosks to determine statement page volumes prior to streaming records.",
        how="Queries ACCOUNT_ID and aggregates transactions matching the specified date window.",
        where="Implemented in database/05_procedures/10_procedures.sql.",
        output="Returns record count and status confirmation for statement generation."
    ))
    story.append(Spacer(1, 4))

    # PROCEDURE 10: CLOSE_BANK_ACCOUNT
    story.append(Paragraph("PROCEDURE 10: CLOSE_BANK_ACCOUNT", subsec_style))
    p10_sql = """CREATE OR REPLACE PROCEDURE CLOSE_BANK_ACCOUNT (
    p_account_number IN  VARCHAR2,
    p_reason         IN  VARCHAR2,
    p_status         OUT VARCHAR2,
    p_message        OUT VARCHAR2
) IS
    v_acc_id NUMBER(10); v_bal NUMBER(15,2); v_acc_status VARCHAR2(20);
BEGIN
    SELECT ACCOUNT_ID, BALANCE, ACCOUNT_STATUS INTO v_acc_id, v_bal, v_acc_status
    FROM BANK_ACCOUNTS WHERE ACCOUNT_NUMBER = p_account_number FOR UPDATE;
    IF v_bal != 0 THEN
        p_status := 'ERROR'; p_message := 'Account balance must be exactly 0.00 to close. Current: ' || v_bal; ROLLBACK; RETURN;
    END IF;
    UPDATE BANK_ACCOUNTS SET ACCOUNT_STATUS = 'Closed', CLOSED_DATE = SYSDATE WHERE ACCOUNT_ID = v_acc_id;
    COMMIT;
    p_status := 'SUCCESS'; p_message := 'Account successfully closed.';
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK; p_status := 'ERROR'; p_message := 'Account closure failed: ' || SQLERRM;
END CLOSE_BANK_ACCOUNT;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(p10_sql))
    story.append(make_expl(
        what="Formally deactivates and closes an account while enforcing zero-balance closure prerequisites.",
        why="Prevents accidental closure of accounts holding customer assets and prevents orphaned funds.",
        how="Acquires row lock, validates BALANCE = 0, updates status to Closed, and stamps CLOSED_DATE.",
        where="Implemented in database/05_procedures/10_procedures.sql.",
        output="Marks account as permanently closed, preventing subsequent debits or credits."
    ))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 16. USER-DEFINED FUNCTIONS (PL/SQL)
    # =========================================================================
    story.append(Paragraph("16. USER-DEFINED FUNCTIONS (PL/SQL)", sec_style))
    story.append(Paragraph("Below is the complete list of all 6 compiled PL/SQL user-defined functions implemented in <code>09_functions.sql</code>:", body_style))
    story.append(Paragraph("<b>FUNCTION LIST</b>", subsec_style))
    func_names = [
        "1. GET_ACCOUNT_BALANCE — Fetches the live ledger balance for a given account number string.",
        "2. CALCULATE_LOAN_INTEREST — Computes total accrued simple interest over a multi-month borrowing tenure.",
        "3. CALCULATE_MONTHLY_EMI — Evaluates standard monthly installment using the reducing-balance formula: [P * r * (1+r)^n]/[(1+r)^n - 1].",
        "4. GET_TOTAL_TRANSACTIONS — Counts total completed financial transactions executed on an account.",
        "5. GET_CUSTOMER_ACCOUNT_COUNT — Returns the total count of bank accounts owned by a customer.",
        "6. CHECK_ACCOUNT_STATUS — Verifies whether an account is Active and eligible for monetary operations."
    ]
    for fn in func_names:
        story.append(Paragraph(fn, list_style))
    story.append(Spacer(1, 4))

    # FUNCTION 1: GET_ACCOUNT_BALANCE
    story.append(Paragraph("FUNCTION 1: GET_ACCOUNT_BALANCE", subsec_style))
    f1_sql = """CREATE OR REPLACE FUNCTION GET_ACCOUNT_BALANCE (
    p_account_number IN VARCHAR2
) RETURN NUMBER IS
    v_balance NUMBER(15,2);
BEGIN
    SELECT BALANCE INTO v_balance FROM BANK_ACCOUNTS WHERE ACCOUNT_NUMBER = p_account_number;
    RETURN v_balance;
EXCEPTION
    WHEN NO_DATA_FOUND THEN RETURN -1;
    WHEN OTHERS THEN RETURN -999;
END GET_ACCOUNT_BALANCE;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(f1_sql))
    story.append(make_expl(
        what="A deterministic scalar lookup function returning the current ledger balance of an account.",
        why="Encapsulates balance queries within a reusable function callable directly from SQL SELECT projections.",
        how="Queries BALANCE column; traps NO_DATA_FOUND to return -1 indicator code.",
        where="Implemented in database/04_functions/09_functions.sql.",
        output="Returns numeric account balance or negative error code."
    ))
    story.append(Spacer(1, 4))

    # FUNCTION 2: CALCULATE_LOAN_INTEREST
    story.append(Paragraph("FUNCTION 2: CALCULATE_LOAN_INTEREST", subsec_style))
    f2_sql = """CREATE OR REPLACE FUNCTION CALCULATE_LOAN_INTEREST (
    p_principal     IN NUMBER,
    p_annual_rate   IN NUMBER,
    p_term_months   IN NUMBER
) RETURN NUMBER IS
    v_years NUMBER(6,2);
    v_interest NUMBER(15,2);
BEGIN
    IF p_principal <= 0 OR p_annual_rate < 0 OR p_term_months <= 0 THEN RETURN 0; END IF;
    v_years := p_term_months / 12.0;
    v_interest := (p_principal * p_annual_rate * v_years) / 100.0;
    RETURN ROUND(v_interest, 2);
END CALCULATE_LOAN_INTEREST;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(f2_sql))
    story.append(make_expl(
        what="Computes total nominal interest accrued across a loan borrowing tenure.",
        why="Provides accurate interest estimates for loan product comparisons and disclosures.",
        how="Calculates time in fractional years and applies standard financial interest formula.",
        where="Implemented in database/04_functions/09_functions.sql.",
        output="Returns rounded interest amount in currency units."
    ))
    story.append(Spacer(1, 4))

    # FUNCTION 3: CALCULATE_MONTHLY_EMI
    story.append(Paragraph("FUNCTION 3: CALCULATE_MONTHLY_EMI", subsec_style))
    f3_sql = """CREATE OR REPLACE FUNCTION CALCULATE_MONTHLY_EMI (
    p_principal     IN NUMBER,
    p_annual_rate   IN NUMBER,
    p_term_months   IN NUMBER
) RETURN NUMBER IS
    v_monthly_rate NUMBER(10,6);
    v_emi          NUMBER(12,2);
    v_factor       NUMBER(20,8);
BEGIN
    IF p_principal <= 0 OR p_term_months <= 0 THEN RETURN 0; END IF;
    IF p_annual_rate = 0 THEN RETURN ROUND(p_principal / p_term_months, 2); END IF;
    v_monthly_rate := (p_annual_rate / 12.0) / 100.0;
    v_factor := POWER(1 + v_monthly_rate, p_term_months);
    v_emi := (p_principal * v_monthly_rate * v_factor) / (v_factor - 1);
    RETURN ROUND(v_emi, 2);
EXCEPTION
    WHEN ZERO_DIVIDE THEN RETURN ROUND(p_principal / p_term_months, 2);
    WHEN OTHERS THEN RETURN 0;
END CALCULATE_MONTHLY_EMI;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(f3_sql))
    story.append(make_expl(
        what="Implements reducing-balance Equated Monthly Installment (EMI) mathematical modeling.",
        why="Guarantees server-side mathematical consistency across web calculators and core loan disbursement tables.",
        how="Evaluates monthly rate, raises to power of term months using POWER(), handles zero division, and returns rounded figure.",
        where="Implemented in database/04_functions/09_functions.sql.",
        output="Computes exact monthly installment obligation for loan underwriting."
    ))
    story.append(Spacer(1, 4))

    # FUNCTION 4: GET_TOTAL_TRANSACTIONS
    story.append(Paragraph("FUNCTION 4: GET_TOTAL_TRANSACTIONS", subsec_style))
    f4_sql = """CREATE OR REPLACE FUNCTION GET_TOTAL_TRANSACTIONS (
    p_account_id IN NUMBER
) RETURN NUMBER IS
    v_count NUMBER(10);
BEGIN
    SELECT COUNT(*) INTO v_count FROM TRANSACTIONS WHERE ACCOUNT_ID = p_account_id AND TRANSACTION_STATUS = 'Completed';
    RETURN v_count;
END GET_TOTAL_TRANSACTIONS;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(f4_sql))
    story.append(make_expl(
        what="Aggregates and returns total completed transactions for a given account surrogate ID.",
        why="Assists customer relationship managers in tracking account velocity and transaction activity.",
        how="Executes indexed count scan on TRANSACTIONS table filtering on Completed status.",
        where="Implemented in database/04_functions/09_functions.sql.",
        output="Returns non-negative integer representing completed transactions."
    ))
    story.append(Spacer(1, 4))

    # FUNCTION 5: GET_CUSTOMER_ACCOUNT_COUNT
    story.append(Paragraph("FUNCTION 5: GET_CUSTOMER_ACCOUNT_COUNT", subsec_style))
    f5_sql = """CREATE OR REPLACE FUNCTION GET_CUSTOMER_ACCOUNT_COUNT (
    p_customer_id IN NUMBER
) RETURN NUMBER IS
    v_count NUMBER(5);
BEGIN
    SELECT COUNT(*) INTO v_count FROM BANK_ACCOUNTS WHERE CUSTOMER_ID = p_customer_id;
    RETURN v_count;
END GET_CUSTOMER_ACCOUNT_COUNT;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(f5_sql))
    story.append(make_expl(
        what="Returns the count of all active and inactive bank accounts owned by a customer.",
        why="Used in customer profile headers and loyalty reward evaluation.",
        how="Performs indexed COUNT(*) scan on BANK_ACCOUNTS foreign key index IDX_ACC_CUST.",
        where="Implemented in database/04_functions/09_functions.sql.",
        output="Returns total account portfolio size for the specified customer."
    ))
    story.append(Spacer(1, 4))

    # FUNCTION 6: CHECK_ACCOUNT_STATUS
    story.append(Paragraph("FUNCTION 6: CHECK_ACCOUNT_STATUS", subsec_style))
    f6_sql = """CREATE OR REPLACE FUNCTION CHECK_ACCOUNT_STATUS (
    p_account_id IN NUMBER
) RETURN VARCHAR2 IS
    v_status VARCHAR2(20);
BEGIN
    SELECT ACCOUNT_STATUS INTO v_status FROM BANK_ACCOUNTS WHERE ACCOUNT_ID = p_account_id;
    RETURN v_status;
EXCEPTION
    WHEN NO_DATA_FOUND THEN RETURN 'NOT_FOUND';
END CHECK_ACCOUNT_STATUS;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(f6_sql))
    story.append(make_expl(
        what="Validation function checking account operational status prior to initiating transactions.",
        why="Provides a lightweight status check for middleware gateways without fetching full account rows.",
        how="Queries ACCOUNT_STATUS column; returns string status or NOT_FOUND if invalid ID.",
        where="Implemented in database/04_functions/09_functions.sql.",
        output="Returns status string: Active, Dormant, Frozen, Closed, or NOT_FOUND."
    ))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 17. DATABASE TRIGGERS (PL/SQL)
    # =========================================================================
    story.append(Paragraph("17. DATABASE TRIGGERS (PL/SQL)", sec_style))
    story.append(Paragraph("Below is the complete list of all 7 compiled PL/SQL triggers implemented in <code>11_triggers.sql</code>:", body_style))
    story.append(Paragraph("<b>TRIGGER LIST</b>", subsec_style))
    trig_names = [
        "1. TRG_CUSTOMERS_BIU — Normalizes email to lowercase and trims whitespace on Customer INSERT/UPDATE.",
        "2. TRG_ACCOUNTS_BIU — Enforces uppercase account numbers and initializes default opening dates.",
        "3. TRG_VALIDATE_ACCOUNT_MIN_BAL — Enforces product minimum balance rules, preventing illegal balance depletion.",
        "4. TRG_ACCOUNTS_AUDIT — Autonomous audit trigger logging balance mutations with PRAGMA AUTONOMOUS_TRANSACTION.",
        "5. TRG_TRANSACTIONS_AUDIT — Captures audit entries whenever high-value financial transactions are posted.",
        "6. TRG_AUDIT_DELETE — Security guard preventing any unauthorized deletion or truncation of the AUDIT_LOGS table.",
        "7. TRG_STMT_TRANSACTION_AUDIT — Statement-level trigger logging execution summaries after batch transaction jobs."
    ]
    for tn in trig_names:
        story.append(Paragraph(tn, list_style))
    story.append(Spacer(1, 4))

    # TRIGGER 1: TRG_CUSTOMERS_BIU
    story.append(Paragraph("TRIGGER 1: TRG_CUSTOMERS_BIU", subsec_style))
    tr1_sql = """CREATE OR REPLACE TRIGGER TRG_CUSTOMERS_BIU
BEFORE INSERT OR UPDATE ON CUSTOMERS
FOR EACH ROW
BEGIN
    :NEW.EMAIL := LOWER(TRIM(:NEW.EMAIL));
    :NEW.FIRST_NAME := TRIM(:NEW.FIRST_NAME);
    :NEW.LAST_NAME := TRIM(:NEW.LAST_NAME);
    :NEW.PAN_NUMBER := UPPER(TRIM(:NEW.PAN_NUMBER));
END TRG_CUSTOMERS_BIU;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(tr1_sql))
    story.append(make_expl(
        what="Before-Row trigger that sanitizes and canonicalizes customer demographic input.",
        why="Guarantees data consistency by converting emails to lowercase and PAN numbers to uppercase before persistence.",
        how="Fires before INSERT or UPDATE for each row; modifies :NEW pseudo-record values in-flight.",
        where="Implemented in database/06_triggers/11_triggers.sql.",
        output="Guarantees clean, standardized text attributes in CUSTOMERS table."
    ))
    story.append(Spacer(1, 4))

    # TRIGGER 2: TRG_ACCOUNTS_BIU
    story.append(Paragraph("TRIGGER 2: TRG_ACCOUNTS_BIU", subsec_style))
    tr2_sql = """CREATE OR REPLACE TRIGGER TRG_ACCOUNTS_BIU
BEFORE INSERT OR UPDATE ON BANK_ACCOUNTS
FOR EACH ROW
BEGIN
    :NEW.ACCOUNT_NUMBER := UPPER(TRIM(:NEW.ACCOUNT_NUMBER));
    IF INSERTING AND :NEW.OPENED_DATE IS NULL THEN
        :NEW.OPENED_DATE := SYSDATE;
    END IF;
END TRG_ACCOUNTS_BIU;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(tr2_sql))
    story.append(make_expl(
        what="Before-Row trigger ensuring consistent account number formatting and opened timestamp defaults.",
        why="Standardizes account numbers and guarantees reliable timestamp capture without relying on client clocks.",
        how="Trims and converts account numbers to uppercase; sets :NEW.OPENED_DATE to server SYSDATE during inserts.",
        where="Implemented in database/06_triggers/11_triggers.sql.",
        output="Ensures uppercase account identifiers and guaranteed timestamps."
    ))
    story.append(Spacer(1, 4))

    # TRIGGER 3: TRG_VALIDATE_ACCOUNT_MIN_BAL
    story.append(Paragraph("TRIGGER 3: TRG_VALIDATE_ACCOUNT_MIN_BAL", subsec_style))
    tr3_sql = """CREATE OR REPLACE TRIGGER TRG_VALIDATE_ACCOUNT_MIN_BAL
BEFORE UPDATE OF BALANCE ON BANK_ACCOUNTS
FOR EACH ROW
WHEN (NEW.BALANCE < OLD.BALANCE)
DECLARE
    v_min_bal NUMBER(10,2);
    v_od_allowed CHAR(1);
BEGIN
    SELECT MIN_BALANCE, OVERDRAFT_ALLOWED INTO v_min_bal, v_od_allowed
    FROM ACCOUNT_TYPES WHERE TYPE_ID = :NEW.TYPE_ID;
    IF v_od_allowed = 'N' AND :NEW.BALANCE < v_min_bal THEN
        RAISE_APPLICATION_ERROR(-20001, 'Violation: Balance cannot drop below required minimum of ' || v_min_bal);
    END IF;
END TRG_VALIDATE_ACCOUNT_MIN_BAL;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(tr3_sql))
    story.append(make_expl(
        what="Before-Row trigger validating that non-overdraft accounts do not drop below product minimum balance thresholds.",
        why="Enforces commercial banking deposit policy rules directly in the database kernel, preventing illegal balance depletion.",
        how="Fires conditionally WHEN (NEW.BALANCE < OLD.BALANCE); reads account type terms; aborts with RAISE_APPLICATION_ERROR if breached.",
        where="Implemented in database/06_triggers/11_triggers.sql.",
        output="Rejects illegal debit operations with informative custom application error code -20001."
    ))
    story.append(Spacer(1, 4))

    # TRIGGER 4: TRG_ACCOUNTS_AUDIT
    story.append(Paragraph("TRIGGER 4: TRG_ACCOUNTS_AUDIT (Autonomous Audit Trail)", subsec_style))
    tr4_sql = """CREATE OR REPLACE TRIGGER TRG_ACCOUNTS_AUDIT
AFTER UPDATE ON BANK_ACCOUNTS
FOR EACH ROW
DECLARE
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    IF :OLD.BALANCE != :NEW.BALANCE OR :OLD.ACCOUNT_STATUS != :NEW.ACCOUNT_STATUS THEN
        INSERT INTO AUDIT_LOGS (LOG_ID, TABLE_NAME, OPERATION_TYPE, RECORD_ID, OLD_VALUES, NEW_VALUES, ACTION_DESCRIPTION)
        VALUES (SEQ_AUDIT_LOGS.NEXTVAL, 'BANK_ACCOUNTS', 'UPDATE', TO_CHAR(:NEW.ACCOUNT_ID),
                'Balance=' || :OLD.BALANCE || ', Status=' || :OLD.ACCOUNT_STATUS,
                'Balance=' || :NEW.BALANCE || ', Status=' || :NEW.ACCOUNT_STATUS,
                'Automated Account Balance/Status Audit Log');
        COMMIT;
    END IF;
END TRG_ACCOUNTS_AUDIT;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(tr4_sql))
    story.append(make_expl(
        what="After-Row autonomous audit trigger capturing historical balance and account status mutations.",
        why="Guarantees an unalterable security audit trail that persists even if the outer transaction subsequently encounters errors.",
        how="Uses PRAGMA AUTONOMOUS_TRANSACTION to execute and COMMIT an independent sub-transaction inserting into AUDIT_LOGS.",
        where="Implemented in database/06_triggers/11_triggers.sql.",
        output="Creates permanent, tamper-evident audit log records for regulatory compliance."
    ))
    story.append(Spacer(1, 4))

    # TRIGGER 5: TRG_TRANSACTIONS_AUDIT
    story.append(Paragraph("TRIGGER 5: TRG_TRANSACTIONS_AUDIT", subsec_style))
    tr5_sql = """CREATE OR REPLACE TRIGGER TRG_TRANSACTIONS_AUDIT
AFTER INSERT ON TRANSACTIONS
FOR EACH ROW
DECLARE
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    IF :NEW.AMOUNT >= 50000.00 THEN
        INSERT INTO AUDIT_LOGS (LOG_ID, TABLE_NAME, OPERATION_TYPE, RECORD_ID, NEW_VALUES, ACTION_DESCRIPTION)
        VALUES (SEQ_AUDIT_LOGS.NEXTVAL, 'TRANSACTIONS', 'INSERT', TO_CHAR(:NEW.TRANSACTION_ID),
                'Ref=' || :NEW.TRANSACTION_REF || ', Type=' || :NEW.TRANSACTION_TYPE || ', Amount=' || :NEW.AMOUNT,
                'HIGH-VALUE TRANSACTION ALERT: Exceeds 50,000 threshold');
        COMMIT;
    END IF;
END TRG_TRANSACTIONS_AUDIT;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(tr5_sql))
    story.append(make_expl(
        what="After-Insert autonomous trigger auditing high-value financial movements exceeding 50,000.",
        why="Satisfies Anti-Money Laundering (AML) reporting regulations by tracking significant liquid transactions.",
        how="Fires after transaction insertions; flags amounts >= 50,000; logs autonomously to AUDIT_LOGS.",
        where="Implemented in database/06_triggers/11_triggers.sql.",
        output="Logs immediate AML audit alerts for large transaction volumes."
    ))
    story.append(Spacer(1, 4))

    # TRIGGER 6: TRG_AUDIT_DELETE
    story.append(Paragraph("TRIGGER 6: TRG_AUDIT_DELETE (Security Guard)", subsec_style))
    tr6_sql = """CREATE OR REPLACE TRIGGER TRG_AUDIT_DELETE
BEFORE DELETE ON AUDIT_LOGS
BEGIN
    RAISE_APPLICATION_ERROR(-20099, 'SECURITY VIOLATION: Audit log records are permanent and cannot be deleted.');
END TRG_AUDIT_DELETE;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(tr6_sql))
    story.append(make_expl(
        what="Statement-level defensive trigger prohibiting any deletion of historical audit logs.",
        why="Guarantees non-repudiation and prevents insider tampering or log wiping by privileged users.",
        how="Fires before any DELETE operation on AUDIT_LOGS and raises fatal application error -20099.",
        where="Implemented in database/06_triggers/11_triggers.sql.",
        output="Blocks DELETE statements, raising fatal error ORA-20099."
    ))
    story.append(Spacer(1, 4))

    # TRIGGER 7: TRG_STMT_TRANSACTION_AUDIT
    story.append(Paragraph("TRIGGER 7: TRG_STMT_TRANSACTION_AUDIT", subsec_style))
    tr7_sql = """CREATE OR REPLACE TRIGGER TRG_STMT_TRANSACTION_AUDIT
AFTER INSERT OR UPDATE ON TRANSACTIONS
DECLARE
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    INSERT INTO AUDIT_LOGS (LOG_ID, TABLE_NAME, OPERATION_TYPE, RECORD_ID, ACTION_DESCRIPTION)
    VALUES (SEQ_AUDIT_LOGS.NEXTVAL, 'TRANSACTIONS', 'STATEMENT', 'BATCH',
            'Batch transaction statement completed at ' || TO_CHAR(SYSDATE, 'YYYY-MM-DD HH24:MI:SS'));
    COMMIT;
END TRG_STMT_TRANSACTION_AUDIT;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(tr7_sql))
    story.append(make_expl(
        what="Statement-level trigger logging batch transaction processing runs once per execution.",
        why="Tracks batch ledger activity timestamps without row-level trigger overhead.",
        how="Fires once per SQL statement (without FOR EACH ROW clause); writes summary record autonomously.",
        where="Implemented in database/06_triggers/11_triggers.sql.",
        output="Logs statement execution milestone in audit table."
    ))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 18. PL/SQL CURSORS & ITERATION PARADIGMS
    # =========================================================================
    story.append(Paragraph("18. PL/SQL CURSORS &amp; ITERATION PARADIGMS", sec_style))
    story.append(Paragraph("Below is the complete list of 4 cursor paradigms demonstrated in <code>14_cursors_demo.sql</code>:", body_style))
    story.append(Paragraph("<b>CURSOR DEMONSTRATIONS LIST</b>", subsec_style))
    cur_names = [
        "1. Implicit Cursor — Managed automatically by Oracle during DML; monitored via SQL%ROWCOUNT, SQL%FOUND, and SQL%NOTFOUND.",
        "2. Explicit Cursor — Programmer-declared private SQL work area with manual OPEN, FETCH, %NOTFOUND, and CLOSE control.",
        "3. Parameterized Cursor — Accepts dynamic input arguments to filter result sets across branches without hardcoded criteria.",
        "4. Cursor FOR LOOP — High-level abstraction executing automated cursor declaration, opening, row fetching, and closing."
    ]
    for cn in cur_names:
        story.append(Paragraph(cn, list_style))
    story.append(Spacer(1, 4))

    # CURSOR 1: IMPLICIT CURSOR
    story.append(Paragraph("CURSOR 1: IMPLICIT CURSOR (SQL%ROWCOUNT)", subsec_style))
    cur1_sql = """-- Implicit Cursor Attributes Demonstration (14_cursors_demo.sql)
DECLARE
    v_rows_updated NUMBER;
BEGIN
    UPDATE BANK_ACCOUNTS
    SET ACCOUNT_STATUS = 'Dormant'
    WHERE ACCOUNT_STATUS = 'Active'
      AND OPENED_DATE < ADD_MONTHS(SYSDATE, -24)
      AND ACCOUNT_ID NOT IN (SELECT DISTINCT ACCOUNT_ID FROM TRANSACTIONS WHERE TRANSACTION_DATE > ADD_MONTHS(SYSDATE, -12));
      
    IF SQL%FOUND THEN
        v_rows_updated := SQL%ROWCOUNT;
        DBMS_OUTPUT.PUT_LINE('Success: Flagged ' || v_rows_updated || ' inactive accounts as Dormant.');
    ELSE
        DBMS_OUTPUT.PUT_LINE('Notice: No dormant accounts matched criteria.');
    END IF;
    COMMIT;
END;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(cur1_sql))
    story.append(make_expl(
        what="An internal cursor automatically generated and managed by Oracle for all single-row SELECT and DML statements.",
        why="Allows PL/SQL programs to evaluate how many rows were affected without declaring an explicit cursor.",
        how="Directly evaluates SQL%FOUND, SQL%NOTFOUND, and SQL%ROWCOUNT immediately following the DML statement.",
        where="Implemented in database/08_cursors/14_cursors_demo.sql.",
        output="Updates eligible accounts and prints total affected row count."
    ))
    story.append(Spacer(1, 4))

    # CURSOR 2: EXPLICIT CURSOR
    story.append(Paragraph("CURSOR 2: EXPLICIT CURSOR (Manual Attributes)", subsec_style))
    cur2_sql = """-- Explicit Cursor Demonstration (14_cursors_demo.sql)
DECLARE
    CURSOR c_high_value_accs IS
        SELECT ACCOUNT_NUMBER, BALANCE, ACCOUNT_STATUS
        FROM BANK_ACCOUNTS
        WHERE BALANCE >= 50000.00
        ORDER BY BALANCE DESC;
    v_acc_no BANK_ACCOUNTS.ACCOUNT_NUMBER%TYPE;
    v_bal    BANK_ACCOUNTS.BALANCE%TYPE;
    v_status BANK_ACCOUNTS.ACCOUNT_STATUS%TYPE;
BEGIN
    OPEN c_high_value_accs;
    LOOP
        FETCH c_high_value_accs INTO v_acc_no, v_bal, v_status;
        EXIT WHEN c_high_value_accs%NOTFOUND;
        DBMS_OUTPUT.PUT_LINE('High-Value Acc: ' || v_acc_no || ' | Balance: ' || v_bal);
    END LOOP;
    CLOSE c_high_value_accs;
END;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(cur2_sql))
    story.append(make_expl(
        what="A programmer-declared cursor providing fine-grained procedural control over multi-row query processing.",
        why="Processes large query result sets sequentially, executing custom business logic on each record.",
        how="Explicitly executes OPEN to parse and bind, FETCH to advance row pointer, checks %NOTFOUND, and releases memory with CLOSE.",
        where="Implemented in database/08_cursors/14_cursors_demo.sql.",
        output="Fetches and displays high-value accounts line by line."
    ))
    story.append(Spacer(1, 4))

    # CURSOR 3: PARAMETERIZED CURSOR
    story.append(Paragraph("CURSOR 3: PARAMETERIZED CURSOR", subsec_style))
    cur3_sql = """-- Parameterized Cursor Demonstration (14_cursors_demo.sql)
DECLARE
    CURSOR c_branch_customers (p_bid NUMBER) IS
        SELECT a.ACCOUNT_NUMBER, c.FIRST_NAME || ' ' || c.LAST_NAME AS NAME, a.BALANCE
        FROM BANK_ACCOUNTS a
        JOIN CUSTOMERS c ON a.CUSTOMER_ID = c.CUSTOMER_ID
        WHERE a.BRANCH_ID = p_bid;
    v_rec c_branch_customers%ROWTYPE;
BEGIN
    OPEN c_branch_customers(101);
    LOOP
        FETCH c_branch_customers INTO v_rec;
        EXIT WHEN c_branch_customers%NOTFOUND;
        DBMS_OUTPUT.PUT_LINE('Branch 101 -> ' || v_rec.NAME || ' | Acc: ' || v_rec.ACCOUNT_NUMBER);
    END LOOP;
    CLOSE c_branch_customers;
END;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(cur3_sql))
    story.append(make_expl(
        what="A cursor that accepts input parameter values each time it is opened, dynamically tailoring its result set.",
        why="Improves code reuse by allowing the same cursor structure to be executed across multiple branches or accounts.",
        how="Declares formal parameters in cursor signature; passes actual values in OPEN statement.",
        where="Implemented in database/08_cursors/14_cursors_demo.sql.",
        output="Iterates through customer accounts belonging to specific branch parameter."
    ))
    story.append(Spacer(1, 4))

    # CURSOR 4: CURSOR FOR LOOP
    story.append(Paragraph("CURSOR 4: CURSOR FOR LOOP", subsec_style))
    cur4_sql = """-- Cursor FOR Loop Demonstration (14_cursors_demo.sql)
DECLARE
    CURSOR c_pending_loans IS
        SELECT LOAN_NUMBER, CUSTOMER_ID, LOAN_AMOUNT, MONTHLY_EMI
        FROM LOANS
        WHERE LOAN_STATUS = 'Applied';
BEGIN
    FOR r_loan IN c_pending_loans LOOP
        DBMS_OUTPUT.PUT_LINE('Reviewing Loan: ' || r_loan.LOAN_NUMBER || ' | Principal: ' || r_loan.LOAN_AMOUNT);
    END LOOP;
END;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(cur4_sql))
    story.append(make_expl(
        what="An automated procedural iteration construct that handles cursor lifecycle implicitly.",
        why="Simplifies code and eliminates resource leaks by automatically managing open, fetch, and close operations.",
        how="Implicitly declares record variable, opens cursor, fetches rows, exits when exhausted, and closes cursor upon completion.",
        where="Implemented in database/08_cursors/14_cursors_demo.sql.",
        output="Iterates through all pending loan applications without explicit memory management."
    ))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 19. MODULAR PL/SQL PACKAGES
    # =========================================================================
    story.append(Paragraph("19. MODULAR PL/SQL PACKAGES", sec_style))
    story.append(Paragraph("Below is the complete list of 2 modular packages compiled in <code>12_banking_package.sql</code> and <code>13_loan_package.sql</code>:", body_style))
    story.append(Paragraph("<b>PACKAGE LIST</b>", subsec_style))
    pkg_names = [
        "1. BANKING_PACKAGE — Encapsulates depository banking services: DEPOSIT, WITHDRAW, TRANSFER, GET_BALANCE, and GET_STATEMENT.",
        "2. LOAN_PACKAGE — Encapsulates lending facilities: CALCULATE_EMI, APPLY_LOAN, APPROVE_LOAN, and PROCESS_PAYMENT."
    ]
    for pkn in pkg_names:
        story.append(Paragraph(pkn, list_style))
    story.append(Spacer(1, 4))

    # PACKAGE 1: BANKING_PACKAGE
    story.append(Paragraph("PACKAGE 1: BANKING_PACKAGE (Depository APIs)", subsec_style))
    pkg1_sql = """-- BANKING_PACKAGE Specification & Body (12_banking_package.sql)
CREATE OR REPLACE PACKAGE BANKING_PACKAGE AS
    TYPE t_txn_cursor IS REF CURSOR;
    PROCEDURE DEPOSIT (p_acc_no IN VARCHAR2, p_amt IN NUMBER, p_desc IN VARCHAR2, p_ref OUT VARCHAR2, p_bal OUT NUMBER, p_status OUT VARCHAR2, p_msg OUT VARCHAR2);
    PROCEDURE WITHDRAW (p_acc_no IN VARCHAR2, p_amt IN NUMBER, p_desc IN VARCHAR2, p_ref OUT VARCHAR2, p_bal OUT NUMBER, p_status OUT VARCHAR2, p_msg OUT VARCHAR2);
    PROCEDURE TRANSFER (p_src_acc IN VARCHAR2, p_dest_acc IN VARCHAR2, p_amt IN NUMBER, p_desc IN VARCHAR2, p_ref OUT VARCHAR2, p_status OUT VARCHAR2, p_msg OUT VARCHAR2);
    FUNCTION GET_BALANCE (p_acc_no IN VARCHAR2) RETURN NUMBER;
    PROCEDURE GET_STATEMENT (p_acc_no IN VARCHAR2, p_limit IN NUMBER, p_cursor OUT t_txn_cursor);
END BANKING_PACKAGE;
/

CREATE OR REPLACE PACKAGE BODY BANKING_PACKAGE AS
    FUNCTION GET_BALANCE (p_acc_no IN VARCHAR2) RETURN NUMBER IS
        v_bal NUMBER;
    BEGIN
        SELECT BALANCE INTO v_bal FROM BANK_ACCOUNTS WHERE ACCOUNT_NUMBER = p_acc_no;
        RETURN v_bal;
    END GET_BALANCE;
    PROCEDURE DEPOSIT (p_acc_no IN VARCHAR2, p_amt IN NUMBER, p_desc IN VARCHAR2, p_ref OUT VARCHAR2, p_bal OUT NUMBER, p_status OUT VARCHAR2, p_msg OUT VARCHAR2) IS
    BEGIN
        DEPOSIT_MONEY(p_acc_no, p_amt, p_desc, p_ref, p_bal, p_status, p_msg);
    END DEPOSIT;
    PROCEDURE WITHDRAW (p_acc_no IN VARCHAR2, p_amt IN NUMBER, p_desc IN VARCHAR2, p_ref OUT VARCHAR2, p_bal OUT NUMBER, p_status OUT VARCHAR2, p_msg OUT VARCHAR2) IS
    BEGIN
        WITHDRAW_MONEY(p_acc_no, p_amt, p_desc, p_ref, p_bal, p_status, p_msg);
    END WITHDRAW;
    PROCEDURE TRANSFER (p_src_acc IN VARCHAR2, p_dest_acc IN VARCHAR2, p_amt IN NUMBER, p_desc IN VARCHAR2, p_ref OUT VARCHAR2, p_status OUT VARCHAR2, p_msg OUT VARCHAR2) IS
    BEGIN
        TRANSFER_MONEY(p_src_acc, p_dest_acc, p_amt, p_desc, p_ref, p_status, p_msg);
    END TRANSFER;
    PROCEDURE GET_STATEMENT (p_acc_no IN VARCHAR2, p_limit IN NUMBER, p_cursor OUT t_txn_cursor) IS
    BEGIN
        OPEN p_cursor FOR
            SELECT t.TRANSACTION_REF, t.TRANSACTION_DATE, t.TRANSACTION_TYPE, t.AMOUNT, t.BALANCE_AFTER, t.DESCRIPTION
            FROM TRANSACTIONS t
            JOIN BANK_ACCOUNTS a ON t.ACCOUNT_ID = a.ACCOUNT_ID
            WHERE a.ACCOUNT_NUMBER = p_acc_no
            ORDER BY t.TRANSACTION_DATE DESC FETCH FIRST p_limit ROWS ONLY;
    END GET_STATEMENT;
END BANKING_PACKAGE;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(pkg1_sql))
    story.append(make_expl(
        what="A modular container packaging all core depository banking procedures, functions, and REF CURSOR types.",
        why="Provides architectural encapsulation, hides implementation details, and loads all code into Oracle shared pool memory on first call.",
        how="Separates public interface (Package Specification) from private implementation logic (Package Body).",
        where="Implemented in database/07_packages/12_banking_package.sql.",
        output="Compiles clean, enterprise-grade banking APIs utilized by terminal and web clients."
    ))
    story.append(Spacer(1, 4))

    # PACKAGE 2: LOAN_PACKAGE
    story.append(Paragraph("PACKAGE 2: LOAN_PACKAGE (Credit Facilities)", subsec_style))
    pkg2_sql = """-- LOAN_PACKAGE Specification (13_loan_package.sql)
CREATE OR REPLACE PACKAGE LOAN_PACKAGE AS
    FUNCTION CALCULATE_EMI (p_principal IN NUMBER, p_rate IN NUMBER, p_months IN NUMBER) RETURN NUMBER;
    PROCEDURE APPLY_LOAN (p_cust_id IN NUMBER, p_branch_id IN NUMBER, p_type IN VARCHAR2, p_amount IN NUMBER, p_rate IN NUMBER, p_months IN NUMBER, p_loan_no OUT VARCHAR2, p_emi OUT NUMBER, p_status OUT VARCHAR2, p_msg OUT VARCHAR2);
    PROCEDURE APPROVE_LOAN (p_loan_no IN VARCHAR2, p_decision IN VARCHAR2, p_disburse_acc IN VARCHAR2, p_status OUT VARCHAR2, p_msg OUT VARCHAR2);
    PROCEDURE PROCESS_PAYMENT (p_loan_no IN VARCHAR2, p_amount IN NUMBER, p_method IN VARCHAR2, p_ref OUT VARCHAR2, p_status OUT VARCHAR2, p_msg OUT VARCHAR2);
END LOAN_PACKAGE;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(pkg2_sql))
    story.append(make_expl(
        what="Encapsulates complete lending operations including underwriting calculations, approvals, disbursements, and payments.",
        why="Centralizes credit lifecycle business rules and guarantees consistent interest calculations.",
        how="Wraps core functions CALCULATE_MONTHLY_EMI, APPLY_FOR_LOAN, APPROVE_LOAN, and PROCESS_LOAN_PAYMENT into a unified package.",
        where="Implemented in database/07_packages/13_loan_package.sql.",
        output="Exposes comprehensive loan portfolio management APIs."
    ))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 20. RELATIONAL JOINS
    # =========================================================================
    story.append(Paragraph("20. RELATIONAL JOINS", sec_style))
    story.append(Paragraph("Below is the complete list of 6 relational join paradigms demonstrated in <code>16_sql_concepts_demonstration.sql</code>:", body_style))
    story.append(Paragraph("<b>RELATIONAL JOINS LIST</b>", subsec_style))
    join_names = [
        "1. INNER JOIN — Retrieves matching records across accounts, customers, and branch entities.",
        "2. LEFT OUTER JOIN — Fetches all customers along with their loan facilities, including non-borrowing clients.",
        "3. RIGHT OUTER JOIN — Retrieves all bank branches along with their accounts, including newly opened branches.",
        "4. FULL OUTER JOIN — Produces complete combined dataset of customers and pre-approved beneficiaries.",
        "5. SELF JOIN — Traverses hierarchical reporting relationships within the EMPLOYEES table.",
        "6. CROSS JOIN — Generates Cartesian product pairing account type products across all branches for regional planning."
    ]
    for jn in join_names:
        story.append(Paragraph(jn, list_style))
    story.append(Spacer(1, 4))

    # JOIN 1: INNER JOIN
    story.append(Paragraph("JOIN 1: INNER JOIN", subsec_style))
    j1_sql = """-- 1. INNER JOIN: Accounts with Customer & Branch Details
SELECT a.ACCOUNT_NUMBER, c.FIRST_NAME || ' ' || c.LAST_NAME AS CUSTOMER_NAME,
       b.BRANCH_NAME, t.TYPE_NAME, a.BALANCE
FROM BANK_ACCOUNTS a
INNER JOIN CUSTOMERS c     ON a.CUSTOMER_ID = c.CUSTOMER_ID
INNER JOIN BANK_BRANCHES b ON a.BRANCH_ID = b.BRANCH_ID
INNER JOIN ACCOUNT_TYPES t ON a.TYPE_ID = t.TYPE_ID
WHERE a.ACCOUNT_STATUS = 'Active';"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(j1_sql))
    story.append(make_expl(
        what="Returns rows where matching join predicates are satisfied across all combined entities.",
        why="Filters out incomplete or disconnected records, delivering a strict relational intersection.",
        how="Matches foreign keys a.CUSTOMER_ID = c.CUSTOMER_ID and a.BRANCH_ID = b.BRANCH_ID.",
        where="Demonstrated in database/10_queries/16_sql_concepts_demonstration.sql.",
        output="Active account records paired with customer names and branch details."
    ))
    story.append(Spacer(1, 4))

    # JOIN 2: LEFT OUTER JOIN
    story.append(Paragraph("JOIN 2: LEFT OUTER JOIN", subsec_style))
    j2_sql = """-- 2. LEFT OUTER JOIN: All Customers and their Loans
SELECT c.CUSTOMER_ID, c.FIRST_NAME || ' ' || c.LAST_NAME AS CUSTOMER_NAME,
       NVL(l.LOAN_NUMBER, 'NO ACTIVE LOAN') AS LOAN_NUMBER,
       NVL(l.LOAN_AMOUNT, 0) AS SANCTIONED_AMOUNT,
       NVL(l.LOAN_STATUS, 'N/A') AS LOAN_STATUS
FROM CUSTOMERS c
LEFT OUTER JOIN LOANS l ON c.CUSTOMER_ID = l.CUSTOMER_ID;"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(j2_sql))
    story.append(make_expl(
        what="Returns all records from left table (CUSTOMERS) and matched rows from right table (LOANS).",
        why="Identifies customers who have not yet borrowed, preventing omission of deposit-only clients.",
        how="Returns NULL for right-table attributes when no corresponding loan exists; handled gracefully via NVL.",
        where="Demonstrated in database/10_queries/16_sql_concepts_demonstration.sql.",
        output="Complete customer directory showing associated loan accounts or 'NO ACTIVE LOAN'."
    ))
    story.append(Spacer(1, 4))

    # JOIN 3: RIGHT OUTER JOIN
    story.append(Paragraph("JOIN 3: RIGHT OUTER JOIN", subsec_style))
    j3_sql = """-- 3. RIGHT OUTER JOIN: Branches with Accounts
SELECT b.BRANCH_CODE, b.BRANCH_NAME,
       COUNT(a.ACCOUNT_ID) AS ACTIVE_ACCOUNTS,
       NVL(SUM(a.BALANCE), 0) AS DEPOSIT_VOLUME
FROM BANK_ACCOUNTS a
RIGHT OUTER JOIN BANK_BRANCHES b ON a.BRANCH_ID = b.BRANCH_ID
GROUP BY b.BRANCH_CODE, b.BRANCH_NAME;"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(j3_sql))
    story.append(make_expl(
        what="Returns all records from right table (BANK_BRANCHES) and matched rows from left table (BANK_ACCOUNTS).",
        why="Ensures that newly commissioned branches with zero accounts are still included in institutional reports.",
        how="Preserves every branch row regardless of whether matching accounts exist in BANK_ACCOUNTS.",
        where="Demonstrated in database/10_queries/16_sql_concepts_demonstration.sql.",
        output="Complete branch list displaying account counts and aggregate deposit balances."
    ))
    story.append(Spacer(1, 4))

    # JOIN 4: FULL OUTER JOIN
    story.append(Paragraph("JOIN 4: FULL OUTER JOIN", subsec_style))
    j4_sql = """-- 4. FULL OUTER JOIN: Customers and Beneficiaries
SELECT c.FIRST_NAME || ' ' || c.LAST_NAME AS CUSTOMER_NAME,
       b.BENEFICIARY_NAME, b.BENEFICIARY_ACCOUNT_NO, b.BANK_NAME
FROM CUSTOMERS c
FULL OUTER JOIN BENEFICIARIES b ON c.CUSTOMER_ID = b.CUSTOMER_ID;"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(j4_sql))
    story.append(make_expl(
        what="Combines left and right outer joins, returning all rows from both tables.",
        why="Audits relationship completeness between registered customers and registered transfer beneficiaries.",
        how="Fills non-matching columns on either side with NULL values.",
        where="Demonstrated in database/10_queries/16_sql_concepts_demonstration.sql.",
        output="Complete union of customer records and beneficiary entries."
    ))
    story.append(Spacer(1, 4))

    # JOIN 5: SELF JOIN
    story.append(Paragraph("JOIN 5: SELF JOIN", subsec_style))
    j5_sql = """-- 5. SELF JOIN: Branch Colleagues
SELECT e1.FIRST_NAME || ' ' || e1.LAST_NAME AS OFFICER_1,
       e2.FIRST_NAME || ' ' || e2.LAST_NAME AS OFFICER_2,
       e1.BRANCH_ID, e1.ROLE
FROM EMPLOYEES e1
JOIN EMPLOYEES e2 ON e1.BRANCH_ID = e2.BRANCH_ID AND e1.EMPLOYEE_ID < e2.EMPLOYEE_ID
WHERE e1.ROLE = 'Cashier';"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(j5_sql))
    story.append(make_expl(
        what="Joins a table to itself using table aliases to compare rows within the same entity.",
        why="Finds internal peer relationships or hierarchical structures within a single table.",
        how="Uses aliases e1 and e2 on EMPLOYEES; condition e1.EMPLOYEE_ID < e2.EMPLOYEE_ID eliminates duplicate pairs.",
        where="Demonstrated in database/10_queries/16_sql_concepts_demonstration.sql.",
        output="Pairs of colleagues sharing identical roles within the same physical branch."
    ))
    story.append(Spacer(1, 4))

    # JOIN 6: CROSS JOIN
    story.append(Paragraph("JOIN 6: CROSS JOIN", subsec_style))
    j6_sql = """-- 6. CROSS JOIN: Cartesian Product of Account Types and Branches
SELECT b.BRANCH_CODE, t.TYPE_NAME
FROM BANK_BRANCHES b
CROSS JOIN ACCOUNT_TYPES t;"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(j6_sql))
    story.append(make_expl(
        what="Generates the Cartesian product multiplying every row of the first table by every row of the second.",
        why="Used in institutional financial planning to model product distribution matrices across all branches.",
        how="Pairs each branch with every account type product without requiring a common join condition.",
        where="Demonstrated in database/10_queries/16_sql_concepts_demonstration.sql.",
        output="Matrix of all possible product-branch combinations (Branches * Account Types)."
    ))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 21. SUBQUERIES & NESTED QUERIES
    # =========================================================================
    story.append(Paragraph("21. SUBQUERIES &amp; NESTED QUERIES", sec_style))
    story.append(Paragraph("Below is the complete list of 5 subquery paradigms demonstrated in <code>16_sql_concepts_demonstration.sql</code>:", body_style))
    story.append(Paragraph("<b>SUBQUERY LIST</b>", subsec_style))
    sub_names = [
        "1. Single-Row Subquery — Evaluates a scalar aggregate comparison (balance > overall bank average).",
        "2. Multiple-Row Subquery (IN) — Filters records against a list of values returned by an inner query.",
        "3. Correlated Subquery — References parent query columns row-by-row (balance > branch average).",
        "4. Subquery in FROM Clause (Inline View) — Treats inner query result as a virtual table for aggregation.",
        "5. Scalar Subquery in SELECT Clause — Computes individual calculated values directly inside select projections."
    ]
    for sn in sub_names:
        story.append(Paragraph(sn, list_style))
    story.append(Spacer(1, 4))

    # SUBQUERY 1: Single-Row Subquery
    story.append(Paragraph("SUBQUERY 1: SINGLE-ROW SUBQUERY", subsec_style))
    sq1_sql = """-- 1. Single-Row Subquery: Accounts with balance above average
SELECT ACCOUNT_NUMBER, BALANCE, ACCOUNT_STATUS
FROM BANK_ACCOUNTS
WHERE BALANCE > (SELECT AVG(BALANCE) FROM BANK_ACCOUNTS)
ORDER BY BALANCE DESC;"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(sq1_sql))
    story.append(make_expl(
        what="A nested subquery returning exactly one row and one column for comparison with scalar operators.",
        why="Enables dynamic threshold filtering against system-wide computed aggregates without hardcoding values.",
        how="Inner query evaluates AVG(BALANCE) first; outer query filters rows with balance strictly exceeding that average.",
        where="Demonstrated in database/10_queries/16_sql_concepts_demonstration.sql.",
        output="List of high-performing accounts holding balances above the institutional average."
    ))
    story.append(Spacer(1, 4))

    # SUBQUERY 2: Multi-Row Subquery (IN)
    story.append(Paragraph("SUBQUERY 2: MULTI-ROW SUBQUERY (IN)", subsec_style))
    sq2_sql = """-- 2. Multi-Row Subquery with IN: Business Account Customers
SELECT CUSTOMER_ID, FIRST_NAME, LAST_NAME, EMAIL
FROM CUSTOMERS
WHERE CUSTOMER_ID IN (
    SELECT DISTINCT CUSTOMER_ID FROM BANK_ACCOUNTS
    WHERE TYPE_ID = (SELECT TYPE_ID FROM ACCOUNT_TYPES WHERE TYPE_NAME = 'Current')
);"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(sq2_sql))
    story.append(make_expl(
        what="A subquery returning multiple values evaluated using set membership operators (IN, NOT IN, ANY, ALL).",
        why="Filters records against dynamically generated lists of keys from related tables.",
        how="Inner query produces a set of customer IDs holding Current accounts; outer query retrieves corresponding profiles.",
        where="Demonstrated in database/10_queries/16_sql_concepts_demonstration.sql.",
        output="Customer records belonging to the business current account product tier."
    ))
    story.append(Spacer(1, 4))

    # SUBQUERY 3: Correlated Subquery
    story.append(Paragraph("SUBQUERY 3: CORRELATED SUBQUERY", subsec_style))
    sq3_sql = """-- 3. Correlated Subquery: Accounts with balance above their own branch average
SELECT a.ACCOUNT_NUMBER, a.BRANCH_ID, a.BALANCE
FROM BANK_ACCOUNTS a
WHERE a.BALANCE > (
    SELECT AVG(sub.BALANCE) FROM BANK_ACCOUNTS sub
    WHERE sub.BRANCH_ID = a.BRANCH_ID
);"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(sq3_sql))
    story.append(make_expl(
        what="A subquery that references columns from the outer query, evaluating once per candidate row.",
        why="Executes localized relative comparisons, such as comparing an account balance against its own branch average.",
        how="For each row in outer table a, the inner query computes the specific branch average matching a.BRANCH_ID.",
        where="Demonstrated in database/10_queries/16_sql_concepts_demonstration.sql.",
        output="Accounts that outperform their specific localized branch peers."
    ))
    story.append(Spacer(1, 4))

    # SUBQUERY 4: Inline View
    story.append(Paragraph("SUBQUERY 4: INLINE VIEW (Subquery in FROM)", subsec_style))
    sq4_sql = """-- 4. Inline View: Branch summary aggregation
SELECT iv.BRANCH_NAME, iv.TOTAL_ACCOUNTS, iv.DEPOSIT_TOTAL
FROM (
    SELECT b.BRANCH_NAME, COUNT(a.ACCOUNT_ID) AS TOTAL_ACCOUNTS, SUM(a.BALANCE) AS DEPOSIT_TOTAL
    FROM BANK_BRANCHES b
    JOIN BANK_ACCOUNTS a ON b.BRANCH_ID = a.BRANCH_ID
    GROUP BY b.BRANCH_NAME
) iv
WHERE iv.DEPOSIT_TOTAL >= 50000.00;"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(sq4_sql))
    story.append(make_expl(
        what="A subquery placed in the FROM clause that acts as an in-memory temporary virtual table.",
        why="Allows complex intermediate aggregations to be filtered and projected in the outer query.",
        how="Oracle executes the inner FROM clause, binds it to alias iv, and filters results via the outer WHERE clause.",
        where="Demonstrated in database/10_queries/16_sql_concepts_demonstration.sql.",
        output="Branch summaries filtered by total deposit volume thresholds."
    ))
    story.append(Spacer(1, 4))

    # SUBQUERY 5: Scalar Subquery in SELECT
    story.append(Paragraph("SUBQUERY 5: SCALAR SUBQUERY IN SELECT", subsec_style))
    sq5_sql = """-- 5. Scalar Subquery in SELECT Clause: Total borrowing per customer
SELECT c.CUSTOMER_ID, c.FIRST_NAME || ' ' || c.LAST_NAME AS NAME,
       NVL((SELECT SUM(l.LOAN_AMOUNT) FROM LOANS l WHERE l.CUSTOMER_ID = c.CUSTOMER_ID), 0) AS TOTAL_BORROWED
FROM CUSTOMERS c;"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(sq5_sql))
    story.append(make_expl(
        what="A subquery placed inside the SELECT projection returning exactly one scalar value per row.",
        why="Embeds calculated aggregate values directly alongside parent entity attributes.",
        how="Evaluates the inner SUM query once for each customer row, passing the result to NVL.",
        where="Demonstrated in database/10_queries/16_sql_concepts_demonstration.sql.",
        output="Customer roster displaying aggregate loan borrowing figures."
    ))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 22. SET OPERATORS
    # =========================================================================
    story.append(Paragraph("22. SET OPERATORS", sec_style))
    story.append(Paragraph("Below is the complete list of 4 SQL set operators demonstrated in <code>16_sql_concepts_demonstration.sql</code>:", body_style))
    story.append(Paragraph("<b>SET OPERATORS LIST</b>", subsec_style))
    set_names = [
        "1. UNION — Combines distinct results of two queries, automatically filtering out duplicate records.",
        "2. UNION ALL — Concatenates results of two queries, preserving duplicates for complete auditing.",
        "3. INTERSECT — Returns only the common records present in both query result sets.",
        "4. MINUS — Returns records from the first query that do not exist in the second query result set."
    ]
    for stn in set_names:
        story.append(Paragraph(stn, list_style))
    story.append(Spacer(1, 4))

    # SET 1: UNION
    story.append(Paragraph("SET OPERATOR 1: UNION", subsec_style))
    so1_sql = """-- 1. UNION: Distinct cities where customers or branches exist
SELECT CITY FROM CUSTOMERS
UNION
SELECT CITY FROM BANK_BRANCHES
ORDER BY 1;"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(so1_sql))
    story.append(make_expl(
        what="Combines result sets of two SELECT queries and removes all duplicate rows.",
        why="Identifies the distinct geographic footprint of customers and physical branches.",
        how="Sorts and deduplicates rows from both tables matching the same column structure.",
        where="Demonstrated in database/10_queries/16_sql_concepts_demonstration.sql.",
        output="Alphabetical list of unique cities where bank operations occur."
    ))
    story.append(Spacer(1, 4))

    # SET 2: UNION ALL
    story.append(Paragraph("SET OPERATOR 2: UNION ALL", subsec_style))
    so2_sql = """-- 2. UNION ALL: Complete list of all operational contacts
SELECT 'CUSTOMER' AS CONTACT_TYPE, FIRST_NAME || ' ' || LAST_NAME AS NAME, PHONE, EMAIL FROM CUSTOMERS
UNION ALL
SELECT 'EMPLOYEE' AS CONTACT_TYPE, FIRST_NAME || ' ' || LAST_NAME AS NAME, PHONE, EMAIL FROM EMPLOYEES;"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(so2_sql))
    story.append(make_expl(
        what="Combines result sets without removing duplicates, delivering faster execution.",
        why="Produces complete multi-party contact directories without the overhead of deduplication sorting.",
        how="Appends employee records directly to customer records; preserves all rows.",
        where="Demonstrated in database/10_queries/16_sql_concepts_demonstration.sql.",
        output="Unified directory of all customer and employee contact records."
    ))
    story.append(Spacer(1, 4))

    # SET 3: INTERSECT
    story.append(Paragraph("SET OPERATOR 3: INTERSECT", subsec_style))
    so3_sql = """-- 3. INTERSECT: Cities hosting both branches and customers
SELECT CITY FROM BANK_BRANCHES
INTERSECT
SELECT CITY FROM CUSTOMERS;"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(so3_sql))
    story.append(make_expl(
        what="Returns only the distinct rows that appear in both query result sets.",
        why="Identifies overlapping market territories where branches and resident customers co-exist.",
        how="Evaluates set intersection between branch city list and customer city list.",
        where="Demonstrated in database/10_queries/16_sql_concepts_demonstration.sql.",
        output="List of cities containing both physical branches and local clientele."
    ))
    story.append(Spacer(1, 4))

    # SET 4: MINUS
    story.append(Paragraph("SET OPERATOR 4: MINUS", subsec_style))
    so4_sql = """-- 4. MINUS: Customers who do not have any registered loans
SELECT CUSTOMER_ID FROM CUSTOMERS
MINUS
SELECT CUSTOMER_ID FROM LOANS;"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(so4_sql))
    story.append(make_expl(
        what="Returns rows from the first query that do not exist in the second query.",
        why="Identifies deposit-only customers eligible for targeted credit card and personal loan marketing.",
        how="Subtracts borrower customer IDs from the universal customer ID list.",
        where="Demonstrated in database/10_queries/16_sql_concepts_demonstration.sql.",
        output="Customer IDs of pure depository clients with zero debt liabilities."
    ))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 23. BUILT-IN SQL FUNCTIONS
    # =========================================================================
    story.append(Paragraph("23. BUILT-IN SQL FUNCTIONS", sec_style))
    story.append(Paragraph("Below is the complete list of 5 SQL function categories demonstrated in <code>16_sql_concepts_demonstration.sql</code>:", body_style))
    story.append(Paragraph("<b>SQL FUNCTIONS LIST</b>", subsec_style))
    sql_func_names = [
        "1. Aggregate Functions — COUNT, SUM, AVG, MIN, MAX computing statistical summaries across groups.",
        "2. String Functions — UPPER, LOWER, INITCAP, LENGTH, SUBSTR, CONCAT, LPAD, RPAD for text manipulation.",
        "3. Date Functions — SYSDATE, ADD_MONTHS, MONTHS_BETWEEN, LAST_DAY, TRUNC for calendar arithmetic.",
        "4. Conversion Functions — TO_CHAR, TO_DATE, TO_NUMBER for safe, locale-independent data casting.",
        "5. Null-Handling &amp; Mathematical Functions — NVL, NVL2, COALESCE, ROUND, TRUNC, MOD, POWER for arithmetic resilience."
    ]
    for sfn in sql_func_names:
        story.append(Paragraph(sfn, list_style))
    story.append(Spacer(1, 4))

    sql_f_sql = """-- Built-In SQL Functions Demonstration (16_sql_concepts_demonstration.sql)
SELECT 
    COUNT(ACCOUNT_ID) AS TOTAL_ACCOUNTS,
    TO_CHAR(SUM(BALANCE), '999,999,990.00') AS FORMATTED_TOTAL_DEPOSITS,
    ROUND(AVG(BALANCE), 2) AS AVERAGE_BALANCE,
    NVL(MAX(BALANCE), 0.00) AS MAX_ACCOUNT_BALANCE,
    INITCAP(TRIM('  central operations  ')) AS CLEANED_STRING,
    TO_CHAR(SYSDATE, 'DD-MON-YYYY HH24:MI:SS') AS CURRENT_SERVER_TIME
FROM BANK_ACCOUNTS;"""
    story.append(Paragraph("<b>Query:</b>", body_bold))
    story.append(make_code(sql_f_sql))
    story.append(make_expl(
        what="Pre-built Oracle mathematical, string, date, and aggregation functions providing built-in transformations.",
        why="Standardizes data presentation, ensures calculation speed directly in the kernel, and avoids application-tier conversion bugs.",
        how="Invoked directly within SQL statements; executes natively within the Oracle C-based database engine.",
        where="Demonstrated in database/10_queries/16_sql_concepts_demonstration.sql.",
        output="Returns formatted sums, rounded averages, clean strings, and server timestamps."
    ))
    story.append(Spacer(1, 4))

    # =========================================================================
    # 24. PL/SQL EXCEPTION HANDLING
    # =========================================================================
    story.append(Paragraph("24. PL/SQL EXCEPTION HANDLING", sec_style))
    story.append(Paragraph("Below is the complete list of 3 exception handling categories implemented across the banking procedures:", body_style))
    story.append(Paragraph("<b>EXCEPTION HANDLING LIST</b>", subsec_style))
    ex_names = [
        "1. Predefined Oracle Exceptions — System-raised errors: NO_DATA_FOUND, TOO_MANY_ROWS, ZERO_DIVIDE, DUP_VAL_ON_INDEX.",
        "2. User-Defined Exceptions — Business rule violations: e_insufficient_funds, e_inactive_account, e_limit_exceeded.",
        "3. RAISE_APPLICATION_ERROR — Custom error reporting transmitting user-defined error numbers (-20000 to -20999) to callers."
    ]
    for en in ex_names:
        story.append(Paragraph(en, list_style))
    story.append(Spacer(1, 4))

    ex_sql = """-- Exception Handling Architectural Pattern
DECLARE
    e_insufficient_funds EXCEPTION;
    v_balance NUMBER := 500.00;
    v_debit   NUMBER := 1000.00;
BEGIN
    IF v_debit > v_balance THEN
        RAISE e_insufficient_funds;
    END IF;
EXCEPTION
    WHEN e_insufficient_funds THEN
        RAISE_APPLICATION_ERROR(-20002, 'Transaction Rejected: Available balance is insufficient.');
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20003, 'Account does not exist.');
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE_APPLICATION_ERROR(-20099, 'Fatal System Exception: ' || SQLERRM);
END;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(ex_sql))
    story.append(make_expl(
        what="Structured runtime error trapping mechanisms preventing unhandled crashes and data corruption.",
        why="Ensures that failures trigger immediate transaction rollbacks, preventing partial state changes and leaking stack traces.",
        how="Executes code in BEGIN block; if an error occurs, control transfers to matching WHEN handler; unhandled errors trigger WHEN OTHERS.",
        where="Implemented in all stored procedures in database/05_procedures/10_procedures.sql.",
        output="Intercepts faults, rolls back partial DML, and issues formatted error messages."
    ))
    story.append(Spacer(1, 4))

    # =========================================================================
    # 25. TRANSACTION CONTROL (TCL)
    # =========================================================================
    story.append(Paragraph("25. TRANSACTION CONTROL (TCL)", sec_style))
    story.append(Paragraph("Below is the complete list of 4 Transaction Control Language (TCL) commands demonstrated in the system:", body_style))
    story.append(Paragraph("<b>TRANSACTION CONTROL LIST</b>", subsec_style))
    tcl_names = [
        "1. COMMIT — Makes all pending DML modifications permanent and releases all acquired row locks.",
        "2. ROLLBACK — Undoes all pending DML operations since last commit, restoring database state.",
        "3. SAVEPOINT — Establishes intermediate checkpoints within a transaction, allowing partial rollbacks.",
        "4. SELECT ... FOR UPDATE — Acquires exclusive pessimistic row locks, preventing race conditions."
    ]
    for tn in tcl_names:
        story.append(Paragraph(tn, list_style))
    story.append(Spacer(1, 4))

    tcl_sql = """-- Transaction Control Demonstration with SAVEPOINT
BEGIN
    UPDATE BANK_ACCOUNTS SET BALANCE = BALANCE - 500 WHERE ACCOUNT_NUMBER = 'ACC1010000000001';
    SAVEPOINT sp_debit_completed;
    
    -- Attempt secondary operation
    UPDATE BANK_ACCOUNTS SET BALANCE = BALANCE + 500 WHERE ACCOUNT_NUMBER = 'ACC1010000000002';
    
    -- In case of failure on destination:
    -- ROLLBACK TO SAVEPOINT sp_debit_completed;
    
    COMMIT; -- Release all row locks and persist permanently
END;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(tcl_sql))
    story.append(make_expl(
        what="Commands governing the transactional boundaries of DML statements to enforce ACID compliance.",
        why="Guarantees Atomicity and Isolation, ensuring financial transfers never leave the database in an inconsistent state.",
        how="Writes change vectors to redo log buffers; COMMIT flushes redo to disk; ROLLBACK utilizes undo segments to restore original rows.",
        where="Implemented in all stored procedures in database/05_procedures/10_procedures.sql.",
        output="Ensures 100% ACID adherence across concurrent operations."
    ))
    story.append(Spacer(1, 4))

    # =========================================================================
    # 26. ADVANCED PL/SQL CONCEPTS
    # =========================================================================
    story.append(Paragraph("26. ADVANCED PL/SQL CONCEPTS", sec_style))
    story.append(Paragraph("Below is the complete list of 10 advanced PL/SQL paradigms implemented in <code>15_advanced_plsql.sql</code>:", body_style))
    story.append(Paragraph("<b>ADVANCED CONCEPTS LIST</b>", subsec_style))
    adv_names = [
        "1. Anchored Data Types (%TYPE) — Variables dynamically inherit column data types, preventing truncation errors.",
        "2. Record Types (%ROWTYPE) — Composite structures storing entire table rows in a single variable.",
        "3. User-Defined PL/SQL Records — Custom structures grouping heterogeneous fields for complex in-memory structures.",
        "4. Associative Arrays (Index-by Tables) — In-memory key-value lookups indexed by binary integer or string.",
        "5. Nested Tables — Unbounded in-memory collections supporting MULTISET operations.",
        "6. VARRAYs (Variable-Size Arrays) — Bounded sequential collections with fixed upper limits.",
        "7. BULK COLLECT — High-speed batch data fetching reducing context switches between SQL and PL/SQL engines.",
        "8. FORALL — Parallel batch DML statement execution delivering 10x-20x throughput improvements.",
        "9. Dynamic SQL (EXECUTE IMMEDIATE) — Runtime SQL string construction and execution.",
        "10. Autonomous Transactions (PRAGMA) — Independent child transactions committing separately from parent transactions."
    ]
    for an in adv_names:
        story.append(Paragraph(an, list_style))
    story.append(Spacer(1, 4))

    adv_sql = """-- Bulk Processing Performance Demonstration (15_advanced_plsql.sql)
DECLARE
    TYPE t_acc_list IS TABLE OF BANK_ACCOUNTS%ROWTYPE;
    v_accounts t_acc_list;
BEGIN
    -- Batch fetch entire active account set in one context switch
    SELECT * BULK COLLECT INTO v_accounts
    FROM BANK_ACCOUNTS WHERE ACCOUNT_STATUS = 'Active';
    
    DBMS_OUTPUT.PUT_LINE('Bulk collected ' || v_accounts.COUNT || ' accounts into memory.');
    
    -- Batch update with FORALL statement
    FORALL i IN 1..v_accounts.COUNT
        UPDATE BANK_ACCOUNTS SET BALANCE = BALANCE + 10 WHERE ACCOUNT_ID = v_accounts(i).ACCOUNT_ID;
    COMMIT;
END;
/"""
    story.append(Paragraph("<b>PL/SQL Code:</b>", body_bold))
    story.append(make_code(adv_sql))
    story.append(make_expl(
        what="Advanced optimization features minimizing context switching overhead between the SQL execution engine and PL/SQL procedural virtual machine.",
        why="Delivers enterprise-scale throughput for bulk interest accruals, monthly statement processing, and data warehousing.",
        how="BULK COLLECT streams multi-row results into memory arrays in a single round-trip; FORALL passes the entire collection to the SQL engine at once.",
        where="Implemented in database/09_advanced_plsql/15_advanced_plsql.sql.",
        output="Achieves 10x to 20x performance improvement over row-by-row procedural loops."
    ))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 27. DATABASE NORMALIZATION (1NF, 2NF, 3NF)
    # =========================================================================
    story.append(Paragraph("27. DATABASE NORMALIZATION (1NF, 2NF, 3NF)", sec_style))
    story.append(Paragraph(
        "The relational schema of the Smart Banking Management System was engineered through rigorous mathematical normalization "
        "up to Third Normal Form (3NF) to eliminate insertion, update, and deletion anomalies while conserving storage efficiency:", body_style
    ))
    norm_text = (
        "• <b>First Normal Form (1NF):</b> Every attribute contains strictly atomic (indivisible) values. Repeating groups (such as holding multiple "
        "phone numbers or account numbers within a comma-separated column) were decomposed into dedicated relational child tables with defined surrogate primary keys.<br/>"
        "• <b>Second Normal Form (2NF):</b> Achieves 1NF and eliminates partial dependencies. All non-key attributes are fully functionally dependent on the entire "
        "primary key. In composite-key entities (such as BENEFICIARIES, where uniqueness is enforced across CUSTOMER_ID and BENEFICIARY_ACCOUNT_NO), attributes such "
        "as TRANSFER_LIMIT depend upon the full combination.<br/>"
        "• <b>Third Normal Form (3NF):</b> Achieves 2NF and eliminates transitive dependencies. Non-key attributes do not depend on other non-key attributes. "
        "For example, in BANK_ACCOUNTS, branch addresses and manager names are not stored; instead, a foreign key BRANCH_ID references BANK_BRANCHES. Similarly, "
        "product parameters (MIN_BALANCE, INTEREST_RATE) are normalized into ACCOUNT_TYPES."
    )
    story.append(Paragraph(norm_text, body_style))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 28. WEB APPLICATION MODULES
    # =========================================================================
    story.append(Paragraph("28. WEB APPLICATION MODULES", sec_style))
    story.append(Paragraph(
        "The web presentation layer connects to Oracle Database via the high-performance PHP OCI8 extension. "
        "The application provides 8 operational modules designed for banking staff and branch administrators:", body_style
    ))
    mod_text = (
        "1. <b>Executive Dashboard Module:</b> Live overview displaying aggregate liquid deposits, active loan liabilities, total customers, and Chart.js visualizations.<br/>"
        "2. <b>Customer Onboarding &amp; KYC Module:</b> Customer profile management, PAN/Aadhaar registration, and document verification.<br/>"
        "3. <b>Account Management Module:</b> Depository account creation, status toggles (Active, Dormant, Frozen), and balance inquiry.<br/>"
        "4. <b>Teller Monetary Operations Module:</b> Cash deposits and cash withdrawals backed by compiled stored procedures with row-level locks.<br/>"
        "5. <b>Electronic Funds Transfer Module:</b> Two-phase fund transfers between accounts with atomic commit and rollback protection.<br/>"
        "6. <b>Loan Origination &amp; Repayment Module:</b> Loan applications, officer approvals, automatic disbursements, and installment receipts.<br/>"
        "7. <b>Beneficiary Management Module:</b> Registration of verified transfer recipients with per-transaction transfer caps.<br/>"
        "8. <b>Security Audit &amp; Reporting Module:</b> Read-only access to tamper-evident audit logs and date-range statement generation."
    )
    story.append(Paragraph(mod_text, body_style))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 29. WEB APPLICATION SCREENSHOTS
    # =========================================================================
    story.append(Paragraph("29. WEB APPLICATION SCREENSHOTS", sec_style))
    story.append(Paragraph(
        "Below are the operational web application interfaces connected live to Oracle Database via PHP OCI8:", body_style
    ))

    screenshots_info = [
        ("01_login.png", "Screenshot 1: Secure Staff Authentication Portal", "Cryptographically salted login interface authenticating staff credentials against ADMIN_USERS table."),
        ("02_dashboard.png", "Screenshot 2: Executive Management Operations Dashboard", "Live KPI cards and Chart.js graphical summaries queried dynamically from MV_BRANCH_SUMMARY."),
        ("03_customers.png", "Screenshot 3: Customer Relationship Directory & KYC Console", "Customer portfolio table displaying KYC verification statuses and contact details."),
        ("04_accounts.png", "Screenshot 4: Core Depository Accounts Management", "Central ledger console showing account numbers, product types, balances, and operational statuses."),
        ("05_transactions.png", "Screenshot 5: Real-Time Financial Transactions Ledger", "Double-entry transaction journal recording deposit credits, withdrawal debits, and timestamps."),
        ("06_money_transfer.png", "Screenshot 6: Atomic Two-Phase Fund Transfer Interface", "Fund transfer interface executing TRANSFER_MONEY procedure with pessimistic row locks."),
        ("07_loans.png", "Screenshot 7: Lending Facilities & Amortization Console", "Loan management portal tracking sanctioned amounts, monthly EMIs, and outstanding principal balances."),
        ("08_reports.png", "Screenshot 8: Business Intelligence & Branch Reporting Console", "Reporting suite aggregating branch performance metrics and deposit volume rankings."),
        ("09_audit_logs.png", "Screenshot 9: Tamper-Evident Security Audit Trail", "Forensic audit console rendering immutable logs captured autonomously by database triggers."),
        ("10_beneficiaries.png", "Screenshot 10: Pre-Approved Beneficiary Directory", "Recipient registry enforcing customer transfer caps and account validation."),
        ("16_project_team_modal.png", "Screenshot 11: Academic Project Team & Technical Credits", "Modal dialogue displaying all 4 academic project members and their architectural contributions.")
    ]

    sc_dir = r"d:\college\RDBMS\mini_project\documentation\screenshots"
    for img_name, title, caption in screenshots_info:
        img_full_path = os.path.join(sc_dir, img_name)
        story.append(Paragraph(f"<b>{title}</b>", subsec_style))
        if os.path.exists(img_full_path):
            img_w = 460
            img_h = 230
            img_flow = Image(img_full_path, width=img_w, height=img_h)
            t_img = Table([[img_flow]], colWidths=[460])
            t_img.setStyle(TableStyle([
                ('BOX', (0,0), (-1,-1), 1, c_black),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 0),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ]))
            story.append(t_img)
        story.append(Paragraph(f"<b>Explanation:</b> {caption}", body_style))
        story.append(Spacer(1, 4))

    # =========================================================================
    # 30. TESTING AND VERIFICATION RESULTS
    # =========================================================================
    story.append(Paragraph("30. TESTING AND VERIFICATION RESULTS", sec_style))
    story.append(Paragraph(
        "A rigorous 12-case test suite was compiled and executed via SQL*Plus in <code>17_comprehensive_test_suite.sql</code>. "
        "Every test case verified a distinct database constraint, procedure exception, or transactional boundary with a 100% pass rate:", body_style
    ))

    test_data = [
        [Paragraph("<b>TC #</b>", tbl_header), Paragraph("<b>Test Case Description</b>", tbl_header), Paragraph("<b>Expected Database Outcome</b>", tbl_header), Paragraph("<b>Observed Result</b>", tbl_header), Paragraph("<b>Status</b>", tbl_header)],
        [Paragraph("TC-01", tbl_cell_bold), Paragraph("Deposit Cash into Active Account", tbl_cell), Paragraph("Balance increments by 5,000; writes journal record.", tbl_cell), Paragraph("Balance updated; reference TXN-DEP issued.", tbl_cell), Paragraph("PASS", tbl_cell_bold)],
        [Paragraph("TC-02", tbl_cell_bold), Paragraph("Withdraw Cash within Balance", tbl_cell), Paragraph("Balance decrements by 2,000; writes debit record.", tbl_cell), Paragraph("Balance updated; reference TXN-WTH issued.", tbl_cell), Paragraph("PASS", tbl_cell_bold)],
        [Paragraph("TC-03", tbl_cell_bold), Paragraph("Withdraw Exceeding Balance + Overdraft", tbl_cell), Paragraph("Rejection with error: Insufficient funds; 0 change.", tbl_cell), Paragraph("Exception raised; transaction rolled back.", tbl_cell), Paragraph("PASS", tbl_cell_bold)],
        [Paragraph("TC-04", tbl_cell_bold), Paragraph("Atomic Transfer Between Two Accounts", tbl_cell), Paragraph("Debit sender, credit receiver, dual journal records.", tbl_cell), Paragraph("Both accounts updated atomically; TXN-TRF issued.", tbl_cell), Paragraph("PASS", tbl_cell_bold)],
        [Paragraph("TC-05", tbl_cell_bold), Paragraph("Transfer to Inactive / Closed Account", tbl_cell), Paragraph("Transfer fails; sender balance remains intact.", tbl_cell), Paragraph("Rejection with error: One or both accounts inactive.", tbl_cell), Paragraph("PASS", tbl_cell_bold)],
        [Paragraph("TC-06", tbl_cell_bold), Paragraph("Self-Transfer Attempt (Same Account)", tbl_cell), Paragraph("Rejection with error: Sender and receiver identical.", tbl_cell), Paragraph("Validation caught duplicate account input.", tbl_cell), Paragraph("PASS", tbl_cell_bold)],
        [Paragraph("TC-07", tbl_cell_bold), Paragraph("Deposit Below Opening Minimum Balance", tbl_cell), Paragraph("Account creation fails with minimum deposit error.", tbl_cell), Paragraph("Procedure aborted; no account created.", tbl_cell), Paragraph("PASS", tbl_cell_bold)],
        [Paragraph("TC-08", tbl_cell_bold), Paragraph("Loan Application & Reducing-Balance EMI", tbl_cell), Paragraph("Correct EMI calculation; loan record status Applied.", tbl_cell), Paragraph("Monthly installment computed accurately.", tbl_cell), Paragraph("PASS", tbl_cell_bold)],
        [Paragraph("TC-09", tbl_cell_bold), Paragraph("Loan Approval & Automated Disbursement", tbl_cell), Paragraph("Status updated Disbursed; funds credited to account.", tbl_cell), Paragraph("Loan active; borrower account credited.", tbl_cell), Paragraph("PASS", tbl_cell_bold)],
        [Paragraph("TC-10", tbl_cell_bold), Paragraph("Loan Payment & Principal Reduction", tbl_cell), Paragraph("Payment decomposes to principal/interest.", tbl_cell), Paragraph("Outstanding balance reduced; receipt issued.", tbl_cell), Paragraph("PASS", tbl_cell_bold)],
        [Paragraph("TC-11", tbl_cell_bold), Paragraph("Autonomous Audit Log Verification", tbl_cell), Paragraph("Audit trigger records balance mutation independently.", tbl_cell), Paragraph("Audit log created with exact before/after values.", tbl_cell), Paragraph("PASS", tbl_cell_bold)],
        [Paragraph("TC-12", tbl_cell_bold), Paragraph("Prohibit Deletion from Audit Logs", tbl_cell), Paragraph("DELETE statement rejected with ORA-20099 error.", tbl_cell), Paragraph("Defensive trigger blocked deletion attempt.", tbl_cell), Paragraph("PASS", tbl_cell_bold)],
    ]
    t_test = Table(test_data, colWidths=[35, 135, 140, 155, 45])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f0f0f0")),
        ('BOX', (0,0), (-1,-1), 1, c_black),
        ('GRID', (0,0), (-1,-1), 0.5, c_black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [c_white, colors.HexColor("#f8f8f8")]),
    ]))
    story.append(t_test)
    story.append(Spacer(1, 6))

    # =========================================================================
    # 31. ADVANTAGES TO 35. REFERENCES
    # =========================================================================
    story.append(Paragraph("31. ADVANTAGES OF PROPOSED SYSTEM", sec_style))
    story.append(Paragraph(
        "• <b>Bulletproof ACID Compliance:</b> Financial integrity enforced at the storage layer via compiled stored procedures.<br/>"
        "• <b>Pessimistic Concurrency:</b> Row-level locking prevents race conditions, double-spending, and negative balances.<br/>"
        "• <b>Tamper-Evident Auditing:</b> Autonomous transactions guarantee immutable logs that survive outer transaction rollbacks.<br/>"
        "• <b>High-Speed Batch Ingestion:</b> BULK COLLECT and FORALL provide 10x-20x throughput gains for batch banking jobs.<br/>"
        "• <b>Normalized 3NF Architecture:</b> Eliminates redundant storage while maintaining referential integrity across 11 entities.", body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("32. SYSTEM LIMITATIONS", sec_style))
    story.append(Paragraph(
        "• Requires an active Oracle Database enterprise or express instance running SQL*Plus.<br/>"
        "• PHP OCI8 connectivity requires configured Oracle Instant Client libraries.<br/>"
        "• High concurrent transaction volume requires proper tablespace sizing and redo log buffer allocations.", body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("33. FUTURE SCOPE", sec_style))
    story.append(Paragraph(
        "• Implementation of Oracle Real Application Clusters (RAC) for active-active high availability.<br/>"
        "• Integration with biometric authentication and two-factor SMS OTP verification.<br/>"
        "• Expansion of automated foreign currency exchange rates and multi-currency accounts.<br/>"
        "• Machine learning fraud detection integrated directly into Oracle In-Memory Database pipelines.", body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("34. CONCLUSION", sec_style))
    story.append(Paragraph(
        "The Smart Banking Management System demonstrates the implementation of relational database engineering using compiled "
        "Oracle SQL and PL/SQL. By implementing stored procedures, functions, autonomous triggers, modular packages, explicit cursors, "
        "materialized views, and bulk processing, the system enforces 100% ACID compliance and guarantees data integrity. The project fulfills "
        "all academic requirements for the Relational Database Management System (RDBMS) course.", body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("35. REFERENCES", sec_style))
    refs_text = (
        "1. Oracle Corporation, <i>Oracle Database SQL Language Reference, 19c / 21c</i>, Oracle Documentation Library.<br/>"
        "2. Oracle Corporation, <i>Oracle Database PL/SQL Language Reference, 19c / 21c</i>, Oracle Documentation Library.<br/>"
        "3. Silberschatz, A., Korth, H. F., &amp; Sudarshan, S., <i>Database System Concepts</i>, 7th Edition, McGraw-Hill Education.<br/>"
        "4. Feuerstein, S., &amp; Pribyl, B., <i>Oracle PL/SQL Programming</i>, 6th Edition, O'Reilly Media.<br/>"
        "5. Elmasri, R., &amp; Navathe, S. B., <i>Fundamentals of Database Systems</i>, 7th Edition, Pearson.<br/>"
        "6. Gyanmanjari Innovative University (GMIU), <i>Department of Computer Applications — RDBMS Course Curriculum &amp; Format Reference</i>."
    )
    story.append(Paragraph(refs_text, body_style))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 36. ACADEMIC VIVA EVALUATION & ASSESSMENT MATRIX
    # =========================================================================
    story.append(Paragraph("36. ACADEMIC VIVA EVALUATION &amp; ASSESSMENT MATRIX", sec_style))
    story.append(Paragraph(
        "The evaluation rubric below is provided for faculty mentors and university-appointed examiners during the academic practical viva examination:", body_style
    ))

    viva_rubric_data = [
        [Paragraph("<b>Evaluation Dimension</b>", tbl_header), Paragraph("<b>Academic Criterion &amp; Examination Focus</b>", tbl_header), Paragraph("<b>Max Marks</b>", tbl_header), Paragraph("<b>Marks Awarded</b>", tbl_header)],
        [Paragraph("1. Schema &amp; Normalization", tbl_cell_bold), Paragraph("11 tables normalized to 3NF, PK/FK referential integrity, domain constraints.", tbl_cell), Paragraph("20", tbl_cell), Paragraph("______", tbl_cell)],
        [Paragraph("2. PL/SQL Procedures &amp; Functions", tbl_cell_bold), Paragraph("10 procedures, 6 functions, pessimistic row locking, EMI formulas, exception traps.", tbl_cell), Paragraph("20", tbl_cell), Paragraph("______", tbl_cell)],
        [Paragraph("3. Autonomous Triggers &amp; Audit", tbl_cell_bold), Paragraph("7 database triggers, PRAGMA AUTONOMOUS_TRANSACTION, immutable compliance.", tbl_cell), Paragraph("15", tbl_cell), Paragraph("______", tbl_cell)],
        [Paragraph("4. Packages, Cursors &amp; Bulk Ops", tbl_cell_bold), Paragraph("2 modular packages, 4 cursor paradigms, BULK COLLECT and FORALL batch speedup.", tbl_cell), Paragraph("15", tbl_cell), Paragraph("______", tbl_cell)],
        [Paragraph("5. Queries, Views &amp; Analytical SQL", tbl_cell_bold), Paragraph("Joins, subqueries, set operations, 5 relational views, and 1 materialized view.", tbl_cell), Paragraph("15", tbl_cell), Paragraph("______", tbl_cell)],
        [Paragraph("6. Verification Suite &amp; Live Viva", tbl_cell_bold), Paragraph("12 verified test cases with 100% pass rate; defense of database concepts.", tbl_cell), Paragraph("15", tbl_cell), Paragraph("______", tbl_cell)],
        [Paragraph("<b>TOTAL PRACTICAL GRADE</b>", tbl_cell_bold), Paragraph("<b>Comprehensive Database Engineering Assessment (Cumulative)</b>", tbl_cell_bold), Paragraph("<b>100</b>", tbl_cell_bold), Paragraph("<b>______</b>", tbl_cell_bold)],
    ]
    t_viva = Table(viva_rubric_data, colWidths=[140, 260, 65, 75])
    t_viva.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f0f0f0")),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#f0f0f0")),
        ('BOX', (0,0), (-1,-1), 1, c_black),
        ('GRID', (0,0), (-1,-1), 0.5, c_black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [c_white, colors.HexColor("#f8f8f8")]),
    ]))
    story.append(t_viva)
    story.append(Spacer(1, 15))

    eval_sig_data = [
        [Paragraph("____________________________<br/><b>Internal Examiner Signature</b><br/>Faculty of Computer Applications<br/>Date: ________________________", tbl_cell_bold),
         Paragraph("____________________________<br/><b>External Examiner Signature</b><br/>University Appointed Assessor<br/>Date: ________________________", tbl_cell_bold)]
    ]
    t_eval_sig = Table(eval_sig_data, colWidths=[270, 270])
    t_eval_sig.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_eval_sig)

    doc.build(story, canvasmaker=AcademicCanvas)
    print("PDF successfully generated at:", pdf_path)

if __name__ == "__main__":
    build_pdf()
