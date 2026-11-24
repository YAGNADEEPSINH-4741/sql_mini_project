import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Skip cover page

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.black)

        # Running Header
        self.drawString(54, 800, "Smart Banking Management System - Oracle SQL & PL/SQL Project Report")
        self.setStrokeColor(colors.black)
        self.setLineWidth(0.75)
        self.line(54, 792, 541, 792)

        # Running Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(541, 35, page_str)
        self.drawString(54, 35, "Department of Computer Science & Engineering | Academic Year 2026-2027")
        self.line(54, 45, 541, 45)
        self.restoreState()

def build_pdf():
    pdf_path = r"d:\college\RDBMS\mini_project\documentation\SMART_BANKING_MANAGEMENT_SYSTEM_REPORT.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Monochrome Palette (Pure White & Black)
    c_black = colors.black
    c_white = colors.white
    c_border = colors.black
    c_grid = colors.HexColor("#333333")
    c_header_bg = colors.black
    c_sub_bg = colors.HexColor("#f2f2f2")

    # Typography Styles - Pure Black Text
    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=24, leading=30,
        textColor=c_black, alignment=1, spaceAfter=12
    )
    subtitle_style = ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=13, leading=17,
        textColor=c_black, alignment=1, spaceAfter=20
    )
    h1_style = ParagraphStyle(
        'SectionHeading', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=14, leading=18,
        textColor=c_black, spaceBefore=14, spaceAfter=8, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'SubSectionHeading', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=14,
        textColor=c_black, spaceBefore=10, spaceAfter=5, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'ReportBody', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13.5,
        textColor=c_black, spaceAfter=7
    )
    body_bold = ParagraphStyle(
        'ReportBodyBold', parent=body_style,
        fontName='Helvetica-Bold'
    )
    code_style = ParagraphStyle(
        'ReportCode', parent=styles['Normal'],
        fontName='Courier', fontSize=7.5, leading=9.5,
        textColor=c_black,
        backColor=colors.HexColor("#f8f8f8"),
        borderPadding=5, spaceAfter=6, keepWithNext=True
    )
    table_cell = ParagraphStyle(
        'TableCell', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.5, leading=10,
        textColor=c_black
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7.5, leading=10,
        textColor=c_black
    )

    story = []

    # =========================================================================
    # SECTION 1: COVER PAGE (WHITE & BLACK THEME)
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("SMART BANKING MANAGEMENT SYSTEM", title_style))
    story.append(Paragraph("A Comprehensive Relational Database Architecture & PL/SQL Application", subtitle_style))
    story.append(HRFlowable(width="85%", thickness=2, color=c_black, spaceBefore=6, spaceAfter=16))
    
    story.append(Paragraph("<b>ACADEMIC GROUP PROJECT TEAM</b>", ParagraphStyle('GroupHead', parent=body_bold, alignment=1, fontSize=11, textColor=c_black, spaceAfter=8)))
    
    students_data = [
        [Paragraph("<b>Sr.</b>", table_cell_bold), Paragraph("<b>Student Full Name</b>", table_cell_bold), Paragraph("<b>Enrollment Number</b>", table_cell_bold)],
        [Paragraph("1", table_cell), Paragraph("<b>Vaghela Yagnadeepsinh.C</b>", table_cell), Paragraph("260203030002", table_cell_bold)],
        [Paragraph("2", table_cell), Paragraph("<b>Chudasama Krishnadeepsinh .S</b>", table_cell), Paragraph("260203030001", table_cell_bold)],
        [Paragraph("3", table_cell), Paragraph("<b>Chauhan Jaydip. P</b>", table_cell), Paragraph("260203020035", table_cell_bold)],
        [Paragraph("4", table_cell), Paragraph("<b>Gohil Jignesh. P</b>", table_cell), Paragraph("260203020034", table_cell_bold)]
    ]
    t_students = Table(students_data, colWidths=[35, 250, 165])
    t_students.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f0f0f0")),
        ('BOX', (0,0), (-1,-1), 1, c_black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_black),
    ]))
    story.append(t_students)
    story.append(Spacer(1, 14))

    meta_data = [
        [Paragraph("<b>Course:</b>", table_cell_bold), Paragraph("Relational Database Management Systems (RDBMS)", table_cell)],
        [Paragraph("<b>Project Category:</b>", table_cell_bold), Paragraph("Oracle SQL & Advanced PL/SQL Group Mini Project", table_cell)],
        [Paragraph("<b>Department:</b>", table_cell_bold), Paragraph("Department of Computer Science & Engineering", table_cell)],
        [Paragraph("<b>Technology Stack:</b>", table_cell_bold), Paragraph("Oracle Database 10g/19c/23ai, SQL*Plus, PL/SQL, PHP (OCI8), Bootstrap 5, Chart.js", table_cell)],
        [Paragraph("<b>Academic Year:</b>", table_cell_bold), Paragraph("2026 - 2027", table_cell)]
    ]
    t_meta = Table(meta_data, colWidths=[120, 330])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('BOX', (0,0), (-1,-1), 1, c_black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_black),
    ]))
    story.append(t_meta)
    
    story.append(Spacer(1, 18))
    story.append(Paragraph("<b>Primary Architectural Focus:</b> Oracle Relational Schema, ACID Transactions, Atomic Transfers, Autonomous Triggers, Explicit & Parameterized Cursors, Package Architecture, and Audit Trails.", ParagraphStyle('CoverNote', parent=body_style, alignment=1, fontSize=8, textColor=c_black)))
    story.append(PageBreak())

    # =========================================================================
    # SECTION 2: INTRODUCTION & SYSTEM ARCHITECTURE (STARTS IMMEDIATELY AFTER COVER)
    # (Certificate, Acknowledgement, and Abstract have been removed as requested)
    # =========================================================================
    story.append(Paragraph("1. INTRODUCTION", h1_style))
    story.append(Paragraph(
        "In modern financial engineering, database reliability, transactional integrity, and strict concurrency controls "
        "form the bedrock of core banking solutions (CBS). Relational Database Management Systems like Oracle Database provide "
        "industrial-grade capabilities including declarative constraints, row-level locking, sequence generators, packages, and "
        "triggers. This project implements a fully functional banking simulation that rigorously validates these concepts in a "
        "realistic operational context.", body_style
    ))

    story.append(Paragraph("2. PROBLEM STATEMENT", h1_style))
    story.append(Paragraph(
        "Many academic software projects implement financial operations naively in client-side script code, leading to race conditions, "
        "inconsistent balances during transfer failures (lack of atomicity), vulnerability to duplicate identity collisions, and "
        "absence of immutable audit trails. A robust banking management system must delegate business invariants directly to the "
        "database engine via compiled PL/SQL objects.", body_style
    ))

    story.append(Paragraph("3. PROJECT OBJECTIVES", h1_style))
    objs = [
        "Architect an 11-table 3NF normalized relational schema enforcing declarative constraints.",
        "Implement atomic, two-phase fund transfers with row-level locks (<code>FOR UPDATE</code>) and strict TCL rollback safety.",
        "Demonstrate all cursor types (implicit, explicit, parameterized, cursor FOR loops) for financial ledger parsing.",
        "Create database triggers for automated timestamping, minimum balance validation, and security audit logging.",
        "Group related business logic into modular PL/SQL packages (<code>BANKING_PACKAGE</code>, <code>LOAN_PACKAGE</code>).",
        "Deliver a modern fintech SaaS dashboard with real-time analytics and CSV export."
    ]
    for obj in objs:
        story.append(Paragraph(f"• {obj}", body_style))

    story.append(Paragraph("4. EXISTING SYSTEM VS PROPOSED SYSTEM", h1_style))
    comp_data = [
        [Paragraph("<b>Parameter</b>", table_cell_bold), Paragraph("<b>Existing / Traditional Systems</b>", table_cell_bold), Paragraph("<b>Proposed Smart Banking System</b>", table_cell_bold)],
        [Paragraph("Business Logic Location", table_cell), Paragraph("Client-side PHP or JavaScript", table_cell), Paragraph("Database-level Oracle PL/SQL Procedures & Packages", table_cell)],
        [Paragraph("Transfer Atomicity", table_cell), Paragraph("High risk of partial debits on script crash", table_cell), Paragraph("Strict ACID atomicity; automatic ROLLBACK on failure", table_cell)],
        [Paragraph("Audit Logging", table_cell), Paragraph("Manual application-level log calls (bypassable)", table_cell), Paragraph("Automated Row-Level Oracle Triggers (Immutable)", table_cell)],
        [Paragraph("Concurrency Control", table_cell), Paragraph("Table-level locks or no locking (race conditions)", table_cell), Paragraph("Granular row-level locks via <code>FOR UPDATE</code>", table_cell)],
        [Paragraph("Performance", table_cell), Paragraph("Multiple round-trip network queries", table_cell), Paragraph("Pre-compiled PL/SQL packages and Views", table_cell)]
    ]
    t_comp = Table(comp_data, colWidths=[100, 180, 200])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_black),
        ('TEXTCOLOR', (0,0), (-1,0), c_white),
        ('GRID', (0,0), (-1,-1), 0.5, c_black),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_comp)
    story.append(PageBreak())

    # =========================================================================
    # SECTION 5: TECH STACK, ARCHITECTURE, DATABASE DESIGN
    # =========================================================================
    story.append(Paragraph("5. TECHNOLOGY STACK & ARCHITECTURE", h1_style))
    story.append(Paragraph(
        "<b>Database Engine:</b> Oracle Database 10g / 19c Enterprise Edition with SQL*Plus command line environment.<br/>"
        "<b>Backend Layer:</b> PHP 8.2 with native PHP OCI8 extension and Oracle connection manager.<br/>"
        "<b>Frontend Presentation:</b> HTML5, CSS3 (Custom Fintech Design System), JavaScript (ES6+), Bootstrap 5, Chart.js 4.x.<br/>"
        "<b>Operating Environment:</b> Windows 11 x64, XAMPP Apache Server, Oracle TNS Listener on port 1521.", body_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("6. RELATIONAL DATABASE DESIGN & 11-TABLE SCHEMA", h1_style))
    story.append(Paragraph(
        "The relational schema is partitioned into 11 specialized tables modeled to 3rd Normal Form (3NF) to eliminate data redundancy "
        "and update anomalies. Primary keys are managed via sequence generators (<code>SEQ_*</code>) and constraints enforce referential integrity.", body_style
    ))

    # =========================================================================
    # SECTION 7: ER DIAGRAM
    # =========================================================================
    story.append(Paragraph("7. ENTITY-RELATIONSHIP (ER) DIAGRAM", h1_style))
    story.append(Paragraph(
        "The following high-resolution diagram illustrates the relational topology, foreign key associations (1:N), and key attributes:", body_style
    ))
    er_img_path = r"d:\college\RDBMS\mini_project\documentation\ER_DIAGRAM.png"
    if os.path.exists(er_img_path):
        story.append(Image(er_img_path, width=480, height=336))
    story.append(PageBreak())

    # =========================================================================
    # SECTION 8: TABLE STRUCTURE EXPLANATION
    # =========================================================================
    story.append(Paragraph("8. DETAILED TABLE STRUCTURE SPECIFICATIONS", h1_style))
    tables_meta = [
        ("CUSTOMERS", "Stores primary demographic, contact, residential, and KYC identity details for bank patrons.", "CUSTOMER_ID", "None", "UQ on EMAIL, PHONE; CHECK on GENDER, KYC_STATUS"),
        ("BANK_BRANCHES", "Physical bank branch locations, IFSC codes, city hubs, and assigned general managers.", "BRANCH_ID", "None", "UQ on BRANCH_CODE, IFSC_CODE"),
        ("EMPLOYEES", "Banking personnel, cashiers, auditors, branch staff, and salary bands.", "EMPLOYEE_ID", "BRANCH_ID -> BANK_BRANCHES", "UQ on EMAIL; CHECK on SALARY > 0, STATUS"),
        ("ACCOUNT_TYPES", "Deposit account catalog (Savings, Current, Fixed Deposit, Corporate Salary) with rules.", "TYPE_ID", "None", "UQ on TYPE_NAME; CHECK on MIN_BALANCE, OVERDRAFT_ALLOWED"),
        ("BANK_ACCOUNTS", "Customer financial depository accounts, real-time balances, overdraft limits, and statuses.", "ACCOUNT_ID", "CUSTOMER_ID, BRANCH_ID, TYPE_ID", "UQ on ACCOUNT_NUMBER; CHECK on BALANCE >= 0, STATUS"),
        ("TRANSACTIONS", "Immutable double-entry transaction ledger tracking all deposits, withdrawals, and transfers.", "TRANSACTION_ID", "ACCOUNT_ID, RELATED_ACCOUNT_ID", "UQ on TRANSACTION_REF; CHECK on AMOUNT > 0, STATUS"),
        ("BENEFICIARIES", "Registered third-party and intra-bank transfer recipients linked to patron accounts.", "BENEFICIARY_ID", "CUSTOMER_ID -> CUSTOMERS", "CHECK on TRANSFER_LIMIT > 0, STATUS"),
        ("LOANS", "Credit facilities, disbursed loans, reducing interest rates, tenure, and amortized EMIs.", "LOAN_ID", "CUSTOMER_ID, BRANCH_ID", "UQ on LOAN_NUMBER; CHECK on AMOUNT > 0, STATUS"),
        ("LOAN_PAYMENTS", "Individual EMI installments dissected into principal and interest components.", "PAYMENT_ID", "LOAN_ID -> LOANS", "UQ on PAYMENT_REF; CHECK on PAYMENT_AMOUNT > 0"),
        ("AUDIT_LOGS", "Autonomous security trail populated by database triggers tracking DML operations.", "LOG_ID", "None", "CHECK on OPERATION_TYPE in ('INSERT','UPDATE','DELETE')"),
        ("ADMIN_USERS", "Privileged administrative credentials with BCrypt password hashes and role RBAC.", "ADMIN_ID", "None", "UQ on USERNAME, EMAIL; CHECK on ROLE, STATUS")
    ]
    for t_name, t_desc, t_pk, t_fk, t_ck in tables_meta:
        story.append(Paragraph(f"<b>Table: {t_name}</b>", h2_style))
        story.append(Paragraph(f"<b>Purpose:</b> {t_desc}<br/><b>Primary Key:</b> <code>{t_pk}</code> | <b>Foreign Keys:</b> <code>{t_fk}</code><br/><b>Rules & Constraints:</b> {t_ck}", body_style))
    story.append(PageBreak())

    # =========================================================================
    # SECTIONS 9 & 10: SQL & PL/SQL CONCEPTS IMPLEMENTED
    # =========================================================================
    story.append(Paragraph("9. ORACLE SQL CONCEPTS IMPLEMENTED", h1_style))
    story.append(Paragraph(
        "The project rigorously applies all core categories of Structured Query Language within <code>16_sql_concepts_demonstration.sql</code>:", body_style
    ))
    sql_concepts = [
        ("DDL (Data Definition Language)", "CREATE TABLE, ALTER TABLE (ADD, MODIFY), DROP TABLE, TRUNCATE TABLE.", "Defines and evolves structural schema objects."),
        ("DML (Data Manipulation Language)", "INSERT INTO, UPDATE ... SET, DELETE FROM with WHERE predicates.", "Manages operational state changes across records."),
        ("DQL (Data Query Language)", "SELECT queries utilizing arithmetic, logical, BETWEEN, IN, LIKE, and IS NULL.", "Extracts and filters data for application consumption."),
        ("TCL (Transaction Control)", "COMMIT, ROLLBACK, SAVEPOINT (e.g. <code>SAVEPOINT SP_AFTER_INSERT</code>).", "Guarantees database consistency across multi-step operations."),
        ("Aggregate Functions", "COUNT(), SUM(), AVG(), MIN(), MAX() with GROUP BY and HAVING clauses.", "Computes executive portfolio balances, deposits, and loan counts."),
        ("String & Date Functions", "UPPER(), LOWER(), INITCAP(), SUBSTR(), CONCAT(), SYSDATE, ADD_MONTHS(), MONTHS_BETWEEN().", "Cleans customer identity and computes loan maturity schedules."),
        ("Conversion & Null Functions", "TO_CHAR(), TO_DATE(), TO_NUMBER(), NVL(), NVL2(), COALESCE().", "Formats currency display and handles null loan approval timestamps."),
        ("Relational Joins", "INNER JOIN, LEFT OUTER JOIN, RIGHT OUTER JOIN, FULL OUTER JOIN, SELF JOIN, CROSS JOIN.", "Correlates accounts, counterparties, branches, and loan applicants."),
        ("Subqueries", "Single-row, Multi-row (IN, ANY, ALL), Correlated subqueries, EXISTS and NOT EXISTS.", "Identifies accounts above branch average and customers without loans."),
        ("Set Operators", "UNION, UNION ALL, INTERSECT, MINUS.", "Determines geographical footprint and branch distribution gaps.")
    ]
    for c_title, c_code, c_purp in sql_concepts:
        story.append(Paragraph(f"• <b>{c_title}:</b> {c_purp} (<i>Examples: {c_code}</i>)", body_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph("10. PL/SQL CONCEPTS IMPLEMENTED", h1_style))
    story.append(Paragraph(
        "Procedural Language extensions are central to this project, encapsulating business rules directly on the server:", body_style
    ))
    plsql_blocks = [
        ("Stored Procedures (10 Created)", "<code>TRANSFER_MONEY</code>, <code>DEPOSIT_MONEY</code>, <code>WITHDRAW_MONEY</code>, <code>CREATE_BANK_ACCOUNT</code>, <code>APPLY_FOR_LOAN</code>, <code>APPROVE_LOAN</code>, <code>PROCESS_LOAN_PAYMENT</code>, <code>CLOSE_BANK_ACCOUNT</code>, etc. Features <code>FOR UPDATE</code> locking and parameter binding."),
        ("User-Defined Functions (6 Created)", "<code>CALCULATE_MONTHLY_EMI</code> (reducing balance amortization), <code>GET_ACCOUNT_BALANCE</code>, <code>CALCULATE_LOAN_INTEREST</code>, <code>GET_TOTAL_TRANSACTIONS</code>, <code>GET_CUSTOMER_ACCOUNT_COUNT</code>, <code>CHECK_ACCOUNT_STATUS</code>."),
        ("Cursors (4 Variations Demonstrated)", "Implicit cursors (<code>SQL%FOUND, SQL%ROWCOUNT</code>), Explicit cursors (<code>OPEN, FETCH, CLOSE, %NOTFOUND</code>), Parameterized cursors (filtering by branch), and Cursor FOR Loops."),
        ("Database Triggers (7 Created)", "BEFORE INSERT (sequence generation & min balance check <code>TRG_VALIDATE_ACCOUNT_MIN_BAL</code>), BEFORE UPDATE (timestamp touch), AFTER UPDATE (account balance audit), AFTER INSERT (transaction audit), AFTER DELETE (beneficiary deletion log), and Statement-level triggers."),
        ("Packages (2 Implemented)", "<code>BANKING_PACKAGE</code> (spec & body encapsulating financial transfers and ref cursors) and <code>LOAN_PACKAGE</code> (spec & body handling loan underwriting and payments)."),
        ("Advanced PL/SQL Features", "<code>%TYPE</code>, <code>%ROWTYPE</code>, user-defined <code>RECORD</code>, Collections (<code>VARRAY</code>, Nested Tables, Associative Arrays), <code>BULK COLLECT</code>, <code>FORALL</code>, and Dynamic SQL via <code>EXECUTE IMMEDIATE</code>.")
    ]
    for p_title, p_desc in plsql_blocks:
        story.append(Paragraph(f"• <b>{p_title}:</b> {p_desc}", body_style))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 11: CONCEPT MAPPING TABLE
    # =========================================================================
    story.append(Paragraph("11. SQL & PL/SQL CONCEPT MAPPING TABLE", h1_style))
    story.append(Paragraph(
        "The following master table provides an exact mapping of every database concept to its concrete script file, "
        "syntactical implementation, and business purpose:", body_style
    ))

    mapping_rows = [
        [Paragraph("<b>Concept</b>", table_cell_bold), Paragraph("<b>Implementation Name</b>", table_cell_bold), Paragraph("<b>File Name</b>", table_cell_bold), Paragraph("<b>Functional Purpose in Banking System</b>", table_cell_bold)],
        [Paragraph("DDL", table_cell), Paragraph("CREATE / ALTER / TRUNCATE", table_cell), Paragraph("02_create_tables.sql", table_cell), Paragraph("Defines 11 normalized tables and column attributes", table_cell)],
        [Paragraph("Constraints", table_cell), Paragraph("PK, FK, UQ, CHECK, NOT NULL", table_cell), Paragraph("03_constraints.sql", table_cell), Paragraph("Enforces referential integrity, positive balance, and KYC rules", table_cell)],
        [Paragraph("Sequences", table_cell), Paragraph("SEQ_CUSTOMERS, SEQ_ACCOUNTS", table_cell), Paragraph("04_sequences.sql", table_cell), Paragraph("Generates collision-free surrogate primary keys", table_cell)],
        [Paragraph("Indexes", table_cell), Paragraph("B-Tree on Foreign Keys & Dates", table_cell), Paragraph("05_indexes.sql", table_cell), Paragraph("Accelerates transaction queries and prevents full table scans", table_cell)],
        [Paragraph("Views", table_cell), Paragraph("CUSTOMER_ACCOUNT_VIEW", table_cell), Paragraph("07_views.sql", table_cell), Paragraph("Joins 4 tables for 360-degree customer financial profile", table_cell)],
        [Paragraph("Materialized View", table_cell), Paragraph("MV_BRANCH_SUMMARY", table_cell), Paragraph("08_materialized_views.sql", table_cell), Paragraph("Pre-computes heavy branch analytics for instant reporting", table_cell)],
        [Paragraph("Synonyms", table_cell), Paragraph("SB_CUSTOMERS, SB_ACCOUNTS", table_cell), Paragraph("08_materialized_views.sql", table_cell), Paragraph("Logical object abstraction and schema encapsulation", table_cell)],
        [Paragraph("Procedure", table_cell), Paragraph("TRANSFER_MONEY", table_cell), Paragraph("10_procedures.sql", table_cell), Paragraph("Atomic fund transfer with sender debit and receiver credit", table_cell)],
        [Paragraph("Procedure", table_cell), Paragraph("DEPOSIT_MONEY / WITHDRAW_MONEY", table_cell), Paragraph("10_procedures.sql", table_cell), Paragraph("Performs validated cash credit/debit with row-level locks", table_cell)],
        [Paragraph("Procedure", table_cell), Paragraph("CREATE_BANK_ACCOUNT", table_cell), Paragraph("10_procedures.sql", table_cell), Paragraph("Validates minimum balance and provisions unique account #", table_cell)],
        [Paragraph("Procedure", table_cell), Paragraph("APPLY_FOR_LOAN / APPROVE_LOAN", table_cell), Paragraph("10_procedures.sql", table_cell), Paragraph("Underwriting workflow with automatic disbursement credit", table_cell)],
        [Paragraph("Function", table_cell), Paragraph("CALCULATE_MONTHLY_EMI", table_cell), Paragraph("09_functions.sql", table_cell), Paragraph("Computes reducing balance loan installment formula", table_cell)],
        [Paragraph("Function", table_cell), Paragraph("GET_ACCOUNT_BALANCE", table_cell), Paragraph("09_functions.sql", table_cell), Paragraph("Queries current available account balance by number", table_cell)],
        [Paragraph("Package", table_cell), Paragraph("BANKING_PACKAGE", table_cell), Paragraph("12_banking_package.sql", table_cell), Paragraph("Encapsulates transfers, balance inquiry, and Ref Cursors", table_cell)],
        [Paragraph("Package", table_cell), Paragraph("LOAN_PACKAGE", table_cell), Paragraph("13_loan_package.sql", table_cell), Paragraph("Encapsulates loan application, payments, and payoff quotes", table_cell)],
        [Paragraph("Explicit Cursor", table_cell), Paragraph("c_high_balances (OPEN, FETCH)", table_cell), Paragraph("14_cursors_demo.sql", table_cell), Paragraph("Iterates high-value accounts with %NOTFOUND & %ROWCOUNT", table_cell)],
        [Paragraph("Parameterized Cursor", table_cell), Paragraph("c_branch_loans(branch, min_amt)", table_cell), Paragraph("14_cursors_demo.sql", table_cell), Paragraph("Fetches loan portfolios dynamically based on branch filters", table_cell)],
        [Paragraph("Cursor FOR Loop", table_cell), Paragraph("c_customer_activity", table_cell), Paragraph("14_cursors_demo.sql", table_cell), Paragraph("Automatically opens, iterates, and closes transaction digest", table_cell)],
        [Paragraph("Trigger (Audit)", table_cell), Paragraph("TRG_ACCOUNTS_AUDIT", table_cell), Paragraph("11_triggers.sql", table_cell), Paragraph("Logs old and new balance values to AUDIT_LOGS table", table_cell)],
        [Paragraph("Trigger (Validation)", table_cell), Paragraph("TRG_VALIDATE_ACCOUNT_MIN_BAL", table_cell), Paragraph("11_triggers.sql", table_cell), Paragraph("BEFORE INSERT trigger preventing below-minimum balance accounts", table_cell)],
        [Paragraph("TCL & Savepoint", table_cell), Paragraph("SAVEPOINT SP_AFTER_INSERT", table_cell), Paragraph("16_sql_concepts_demo.sql", table_cell), Paragraph("Demonstrates partial rollback to savepoint during transactions", table_cell)],
        [Paragraph("Bulk Operations", table_cell), Paragraph("BULK COLLECT & FORALL", table_cell), Paragraph("15_advanced_plsql.sql", table_cell), Paragraph("Minimizes context switches during bulk account maintenance", table_cell)],
        [Paragraph("Dynamic SQL", table_cell), Paragraph("EXECUTE IMMEDIATE ... USING", table_cell), Paragraph("15_advanced_plsql.sql", table_cell), Paragraph("Constructs dynamic SQL queries with bind variables at runtime", table_cell)],
        [Paragraph("Exception Handling", table_cell), Paragraph("e_insufficient_funds, ZERO_DIVIDE", table_cell), Paragraph("10_procedures.sql", table_cell), Paragraph("Catches overdrafts and unexpected errors with clean ROLLBACK", table_cell)]
    ]
    t_map = Table(mapping_rows, colWidths=[80, 110, 100, 190])
    t_map.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_black),
        ('TEXTCOLOR', (0,0), (-1,0), c_white),
        ('GRID', (0,0), (-1,-1), 0.5, c_black),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8f8f8")]),
    ]))
    story.append(t_map)
    story.append(PageBreak())

    # =========================================================================
    # SECTION 12: APPLICATION MODULES & ACTUAL SCREENSHOTS
    # =========================================================================
    story.append(Paragraph("12. WEB APPLICATION MODULES & REAL SCREENSHOTS", h1_style))
    story.append(Paragraph(
        "The following screenshots depict the live, fully functional Smart Banking Management System interface "
        "captured in real time from the running local application environment:", body_style
    ))

    screenshot_files = [
        ("01_login.png", "1. Administrative Sign-In Portal (Secure Session & Role-Based Access)"),
        ("02_dashboard.png", "2. Fintech Executive Dashboard (KPI Metrics, Cash Flow Chart & Ledger)"),
        ("03_customers.png", "3. Customer Directory & KYC Registry (CUSTOMERS Table)"),
        ("04_accounts.png", "4. Bank Accounts Portfolio & Procedure-Driven Provisioning"),
        ("05_transactions.png", "5. Real-Time Transaction Ledger (Double-Entry Bookkeeping)"),
        ("06_money_transfer.png", "6. Atomic Fund Transfer Modal (ACID Enforced via TRANSFER_MONEY)"),
        ("07_loans.png", "7. Credit Underwriting, Interactive EMI Calculator & Repayment Ledger"),
        ("08_reports.png", "8. Analytical Branch Performance & High-Net-Worth Depositor View"),
        ("09_audit_logs.png", "9. Immutable Database Trigger Audit Trail (AUDIT_LOGS Table)")
    ]

    for fname, caption in screenshot_files:
        fpath = os.path.join(r"d:\college\RDBMS\mini_project\documentation\screenshots", fname)
        if os.path.exists(fpath):
            story.append(Paragraph(f"<b>{caption}</b>", h2_style))
            story.append(Image(fpath, width=470, height=292))
            story.append(Spacer(1, 8))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 13: TESTING AND VERIFICATION RESULTS
    # =========================================================================
    story.append(Paragraph("13. TESTING AND VERIFICATION RESULTS", h1_style))
    story.append(Paragraph(
        "All 12 mandatory academic test cases were executed against the Oracle Database engine via <code>17_comprehensive_test_suite.sql</code>. "
        "Every single test case yielded 100% expected results with zero discrepancies:", body_style
    ))

    test_rows = [
        [Paragraph("<b>#</b>", table_cell_bold), Paragraph("<b>Test Case Name</b>", table_cell_bold), Paragraph("<b>Input Condition</b>", table_cell_bold), Paragraph("<b>Expected Result</b>", table_cell_bold), Paragraph("<b>Status</b>", table_cell_bold)],
        [Paragraph("1", table_cell), Paragraph("Successful Deposit", table_cell), Paragraph("Acc: SB1001002001, Amt: ₹5,000", table_cell), Paragraph("Balance increases by ₹5,000; Txn logged", table_cell), Paragraph("<b>PASS</b>", table_cell)],
        [Paragraph("2", table_cell), Paragraph("Successful Withdrawal", table_cell), Paragraph("Acc: SB1001002001, Amt: ₹2,000", table_cell), Paragraph("Balance reduces by ₹2,000; Txn logged", table_cell), Paragraph("<b>PASS</b>", table_cell)],
        [Paragraph("3", table_cell), Paragraph("Insufficient Balance", table_cell), Paragraph("Acc: SB1001002001, Amt: ₹1,000,000", table_cell), Paragraph("Rejected with INSUFFICIENT_FUNDS error", table_cell), Paragraph("<b>PASS</b>", table_cell)],
        [Paragraph("4", table_cell), Paragraph("Atomic Money Transfer", table_cell), Paragraph("Transfer ₹3,500 between 2 accounts", table_cell), Paragraph("Sender debited, receiver credited; 2 ledger entries", table_cell), Paragraph("<b>PASS</b>", table_cell)],
        [Paragraph("5", table_cell), Paragraph("Invalid Account Transfer", table_cell), Paragraph("Beneficiary: 'NON_EXISTENT_ACC'", table_cell), Paragraph("Transfer rejected; zero funds deducted", table_cell), Paragraph("<b>PASS</b>", table_cell)],
        [Paragraph("6", table_cell), Paragraph("Duplicate Account No.", table_cell), Paragraph("Insert duplicate 'SB1001002001'", table_cell), Paragraph("Blocked by ORA-00001 (Unique constraint)", table_cell), Paragraph("<b>PASS</b>", table_cell)],
        [Paragraph("7", table_cell), Paragraph("Account Dormancy Guard", table_cell), Paragraph("Debit on Dormant Acc SB1003002010", table_cell), Paragraph("Withdrawal blocked due to dormant status", table_cell), Paragraph("<b>PASS</b>", table_cell)],
        [Paragraph("8", table_cell), Paragraph("Loan Approval & Credit", table_cell), Paragraph("Apply ₹100,000 loan & approve", table_cell), Paragraph("Loan approved; ₹100k credited to patron account", table_cell), Paragraph("<b>PASS</b>", table_cell)],
        [Paragraph("9", table_cell), Paragraph("EMI Formula Precision", table_cell), Paragraph("₹1,000,000 @ 10% APR over 120 mos", table_cell), Paragraph("Exact monthly EMI = ₹13,215.07", table_cell), Paragraph("<b>PASS</b>", table_cell)],
        [Paragraph("10", table_cell), Paragraph("Trigger Timestamp Touch", table_cell), Paragraph("UPDATE on BANK_ACCOUNTS", table_cell), Paragraph("TRG_ACCOUNTS_BIU updates UPDATED_AT", table_cell), Paragraph("<b>PASS</b>", table_cell)],
        [Paragraph("11", table_cell), Paragraph("Trigger Audit Capture", table_cell), Paragraph("DML executed on financial tables", table_cell), Paragraph("AUDIT_LOGS table captures user, IP, and values", table_cell), Paragraph("<b>PASS</b>", table_cell)],
        [Paragraph("12", table_cell), Paragraph("Transaction Rollback", table_cell), Paragraph("Failure during multi-step operation", table_cell), Paragraph("ROLLBACK executed; zero phantom side effects", table_cell), Paragraph("<b>PASS</b>", table_cell)]
    ]
    t_test = Table(test_rows, colWidths=[20, 110, 130, 160, 60])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_black),
        ('TEXTCOLOR', (0,0), (-1,0), c_white),
        ('GRID', (0,0), (-1,-1), 0.5, c_black),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8f8f8")]),
    ]))
    story.append(t_test)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTIONS 14-18: ADVANTAGES, LIMITATIONS, CONCLUSION, WBS, REFERENCES
    # =========================================================================
    story.append(Paragraph("14. ADVANTAGES OF THE SYSTEM", h1_style))
    advs = [
        "<b>Engine-Level Integrity:</b> Financial logic resides in pre-compiled Oracle PL/SQL, immune to client tampering.",
        "<b>Atomic ACID Protection:</b> Multi-party transactions guarantee zero partial transfers or phantom balance states.",
        "<b>Automated Audit Security:</b> Row-level triggers ensure every state alteration is permanently archived.",
        "<b>High Scalability & Performance:</b> B-Tree indexes, views, and bulk processing minimize server I/O overhead."
    ]
    for adv in advs:
        story.append(Paragraph(f"• {adv}", body_style))

    story.append(Paragraph("15. LIMITATIONS & FUTURE SCOPE", h1_style))
    story.append(Paragraph(
        "<b>Limitations:</b> This system is designed as an academic banking simulation and does not integrate real SWIFT/NEFT payment gateways. "
        "Branch operations currently operate under unified administrative authentication.<br/>"
        "<b>Future Scope:</b> Implementation of multi-factor biometric authentication (MFA/OTP), customer-facing self-service portals, "
        "automated recurring deposits (RD), and Oracle Advanced Queuing (AQ) for asynchronous event streaming.", body_style
    ))

    story.append(Paragraph("16. CONCLUSION", h1_style))
    story.append(Paragraph(
        "The <b>Smart Banking Management System</b> fulfills and surpasses all academic objectives for an advanced Oracle SQL "
        "and PL/SQL mini project. By incorporating 11 normalized tables, 10 stored procedures, 6 user-defined functions, 7 triggers, "
        "2 modular packages, multiple cursor implementations, and a modern responsive fintech frontend, the project serves as an "
        "exemplary blueprint of industrial relational database engineering.", body_style
    ))

    story.append(Paragraph("17. PROJECT TEAM & WORK BREAKDOWN STRUCTURE (WBS)", h1_style))
    story.append(Paragraph(
        "This project was collaboratively designed, engineered, and verified by the following team of students:", body_style
    ))
    wbs_data = [
        [Paragraph("<b>Sr.</b>", table_cell_bold), Paragraph("<b>Student Full Name</b>", table_cell_bold), Paragraph("<b>Enrollment No.</b>", table_cell_bold), Paragraph("<b>Key Responsibilities & Modules</b>", table_cell_bold)],
        [Paragraph("1", table_cell), Paragraph("<b>Vaghela Yagnadeepsinh.C</b>", table_cell), Paragraph("260203030002", table_cell), Paragraph("Database Architecture, 3NF Normalization, Master Deployment Script (RUN_ALL.SQL), ER Modeling & Transaction Isolation.", table_cell)],
        [Paragraph("2", table_cell), Paragraph("<b>Chudasama Krishnadeepsinh .S</b>", table_cell), Paragraph("260203030001", table_cell), Paragraph("PL/SQL Stored Procedures, User-Defined Functions, BANKING_PACKAGE & LOAN_PACKAGE Implementation.", table_cell)],
        [Paragraph("3", table_cell), Paragraph("<b>Chauhan Jaydip. P</b>", table_cell), Paragraph("260203020035", table_cell), Paragraph("Fintech Frontend UI/UX, Bootstrap 5 Layouts, Chart.js Visualizations & AJAX API Routing.", table_cell)],
        [Paragraph("4", table_cell), Paragraph("<b>Gohil Jignesh. P</b>", table_cell), Paragraph("260203020034", table_cell), Paragraph("Automated Triggers, Audit Security Trail, Comprehensive 12-Case Test Suite & Academic Report Documentation.", table_cell)],
    ]
    t_wbs = Table(wbs_data, colWidths=[25, 140, 95, 190])
    t_wbs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_black),
        ('TEXTCOLOR', (0,0), (-1,0), c_white),
        ('BOX', (0,0), (-1,-1), 1, c_black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_black),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8f8f8")]),
    ]))
    story.append(t_wbs)
    story.append(Spacer(1, 10))

    story.append(Paragraph("18. REFERENCES", h1_style))
    refs = [
        "1. Oracle Corporation. <i>Oracle Database SQL Language Reference, 10g/19c/23ai</i>.",
        "2. Oracle Corporation. <i>Oracle Database PL/SQL Packages and Types Reference</i>.",
        "3. Silberschatz, A., Korth, H. F., & Sudarshan, S. <i>Database System Concepts (7th Edition)</i>. McGraw-Hill.",
        "4. Feuerstein, S., & Pribyl, B. <i>Oracle PL/SQL Programming (6th Edition)</i>. O'Reilly Media.",
        "5. The PHP Group. <i>PHP OCI8 Documentation & Oracle Database Connectivity Manual</i>."
    ]
    for ref in refs:
        story.append(Paragraph(ref, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF successfully generated at:", pdf_path)

if __name__ == "__main__":
    build_pdf()
