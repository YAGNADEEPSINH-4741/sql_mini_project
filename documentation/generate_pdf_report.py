import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
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
        self.drawString(45, 804, "Smart Banking Management System - Oracle SQL & PL/SQL Database Engineering Report")
        self.setStrokeColor(colors.black)
        self.setLineWidth(0.75)
        self.line(45, 796, 550, 796)

        # Running Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(550, 32, page_str)
        self.drawString(45, 32, "Department of Computer Science & Engineering | RDBMS Mini Project 2026-2027")
        self.line(45, 42, 550, 42)
        self.restoreState()

def build_pdf():
    pdf_path = r"d:\college\RDBMS\mini_project\documentation\SMART_BANKING_MANAGEMENT_SYSTEM_REPORT.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    
    # Monochrome Palette (Pure Black & White)
    c_black = colors.black
    c_white = colors.white

    # Typography Styles - Dense, Clean, Publication-Grade
    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=24, leading=29,
        textColor=c_black, alignment=1, spaceAfter=8
    )
    subtitle_style = ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=12, leading=16,
        textColor=c_black, alignment=1, spaceAfter=14
    )
    h1_style = ParagraphStyle(
        'SectionHeading', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11.5, leading=15,
        textColor=c_black, spaceBefore=9, spaceAfter=4, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'SubSectionHeading', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=12.5,
        textColor=c_black, spaceBefore=6, spaceAfter=3, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'ReportBody', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=11.5,
        textColor=c_black, spaceAfter=4
    )
    body_bold = ParagraphStyle(
        'ReportBodyBold', parent=body_style,
        fontName='Helvetica-Bold'
    )
    expl_style = ParagraphStyle(
        'ExplText', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=7.8, leading=11,
        textColor=c_black, spaceBefore=2, spaceAfter=5
    )
    code_style = ParagraphStyle(
        'ReportCode', parent=styles['Normal'],
        fontName='Courier', fontSize=6.8, leading=8.3,
        textColor=c_black,
        backColor=colors.HexColor("#f8f8f8"),
        borderPadding=3.5, spaceAfter=3
    )
    table_cell = ParagraphStyle(
        'TableCell', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7, leading=9,
        textColor=c_black
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7, leading=9,
        textColor=c_black
    )

    story = []

    # =========================================================================
    # SECTION 1: COVER PAGE (STRICTLY ON PAGE 1)
    # =========================================================================
    story.append(Spacer(1, 14))
    story.append(Paragraph("SMART BANKING MANAGEMENT SYSTEM", title_style))
    story.append(Paragraph("A Comprehensive Oracle SQL & Advanced PL/SQL Relational Database Engineering Project", subtitle_style))
    story.append(HRFlowable(width="94%", thickness=1.5, color=c_black, spaceBefore=4, spaceAfter=14))
    
    story.append(Paragraph("<b>ACADEMIC GROUP PROJECT TEAM</b>", ParagraphStyle('GroupHead', parent=body_bold, alignment=1, fontSize=10, textColor=c_black, spaceAfter=6)))
    
    students_data = [
        [Paragraph("<b>Sr.</b>", table_cell_bold), Paragraph("<b>Student Full Name</b>", table_cell_bold), Paragraph("<b>Enrollment Number</b>", table_cell_bold), Paragraph("<b>Core Module Responsibilities</b>", table_cell_bold)],
        [Paragraph("1", table_cell), Paragraph("<b>Vaghela Yagnadeepsinh.C</b>", table_cell), Paragraph("260203030002", table_cell_bold), Paragraph("Project Architecture, 3NF Normalization & Master Deployment Script", table_cell)],
        [Paragraph("2", table_cell), Paragraph("<b>Chudasama Krishnadeepsinh .S</b>", table_cell), Paragraph("260203030001", table_cell_bold), Paragraph("PL/SQL Stored Procedures, Functions & Package Implementation", table_cell)],
        [Paragraph("3", table_cell), Paragraph("<b>Chauhan Jaydip. P</b>", table_cell), Paragraph("260203020035", table_cell_bold), Paragraph("Complex Analytical Queries, Relational Joins & Subquery Optimization", table_cell)],
        [Paragraph("4", table_cell), Paragraph("<b>Gohil Jignesh. P</b>", table_cell), Paragraph("260203020034", table_cell_bold), Paragraph("Autonomous Triggers, Security Audit Trail & 12-Case Test Suite", table_cell)]
    ]
    t_students = Table(students_data, colWidths=[25, 145, 95, 195])
    t_students.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f0f0f0")),
        ('BOX', (0,0), (-1,-1), 1, c_black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_black),
    ]))
    story.append(t_students)
    story.append(Spacer(1, 12))

    meta_data = [
        [Paragraph("<b>Course:</b>", table_cell_bold), Paragraph("Relational Database Management Systems (RDBMS)", table_cell)],
        [Paragraph("<b>Project Category:</b>", table_cell_bold), Paragraph("Oracle SQL & Advanced PL/SQL Database Engineering Mini Project", table_cell)],
        [Paragraph("<b>Department:</b>", table_cell_bold), Paragraph("Department of Computer Science & Engineering", table_cell)],
        [Paragraph("<b>Database Engine:</b>", table_cell_bold), Paragraph("Oracle Database 10g / 11g / 12c / 19c / 21c / 23ai with Oracle SQL*Plus CLI", table_cell)],
        [Paragraph("<b>Core Capabilities:</b>", table_cell_bold), Paragraph("11 Tables (3NF), Sequences, B-Tree Indexes, Stored Procedures, Functions, Triggers, Packages, Cursors, Bulk Processing, Dynamic SQL, Audit Trails", table_cell)],
        [Paragraph("<b>Academic Year:</b>", table_cell_bold), Paragraph("2026 - 2027", table_cell)]
    ]
    t_meta = Table(meta_data, colWidths=[110, 350])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('BOX', (0,0), (-1,-1), 1, c_black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.2),
        ('TOPPADDING', (0,0), (-1,-1), 4.2),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_black),
    ]))
    story.append(t_meta)
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>CORE ARCHITECTURAL MATRIX & ENGINEERING HIGHLIGHTS</b>", ParagraphStyle('SummHead', parent=body_bold, alignment=1, fontSize=8.5, textColor=c_black, spaceAfter=5)))
    
    highlights_data = [
        [Paragraph("<b>Engineering Domain</b>", table_cell_bold), Paragraph("<b>Implementation & Practical Banking Application</b>", table_cell_bold)],
        [Paragraph("<b>Relational Schema (3NF)</b>", table_cell), Paragraph("11 normalized tables preventing insertion, update, and deletion anomalies across branches, patrons, loans, and ledgers.", table_cell)],
        [Paragraph("<b>ACID Transaction Engine</b>", table_cell), Paragraph("Two-phase atomic transfers with pessimistic row locking (<code>FOR UPDATE</code>) and guaranteed rollback on balance deficiency.", table_cell)],
        [Paragraph("<b>Autonomous Audit Trail</b>", table_cell), Paragraph("<code>PRAGMA AUTONOMOUS_TRANSACTION</code> trigger logging all balance/status updates even if main transaction rolls back.", table_cell)],
        [Paragraph("<b>Modular PL/SQL Packages</b>", table_cell), Paragraph("Encapsulates transactional and loan accounting into cohesive packages (<code>BANKING_PACKAGE</code>, <code>LOAN_PACKAGE</code>).", table_cell)],
        [Paragraph("<b>High-Performance Cursors</b>", table_cell), Paragraph("Explicit cursors with %NOTFOUND/%ROWCOUNT and <code>BULK COLLECT / FORALL</code> batch processing for enterprise scalability.", table_cell)],
        [Paragraph("<b>12-Case Test Suite</b>", table_cell), Paragraph("12 verified academic test cases covering normal deposits, overdraft debits, duplicate guards, and dormancy restrictions.", table_cell)]
    ]
    t_high = Table(highlights_data, colWidths=[125, 335])
    t_high.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f0f0f0")),
        ('BOX', (0,0), (-1,-1), 1, c_black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.2),
        ('TOPPADDING', (0,0), (-1,-1), 3.2),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_black),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8f8f8")]),
    ]))
    story.append(t_high)
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Primary Architectural Focus:</b> Relational Schema 3NF Normalization, ACID Transactional Atomicity, Row-Level Locking (<code>FOR UPDATE</code>), Two-Phase Fund Transfers, Autonomous Audit Triggers, Explicit & Parameterized Cursors, and Modular PL/SQL Packages. GitHub Repository: <u>https://github.com/YAGNADEEPSINH-4741/sql_mini_project</u>", ParagraphStyle('CoverNote', parent=body_style, alignment=1, fontSize=7, textColor=c_black)))
    story.append(PageBreak())  # Only page break: after the cover page!

    # =========================================================================
    # SECTION 2: SYSTEM ARCHITECTURE & ER DIAGRAM
    # =========================================================================
    story.append(Paragraph("1. SYSTEM OVERVIEW & ACID TRANSACTION ARCHITECTURE", h1_style))
    story.append(Paragraph(
        "The <b>Smart Banking Management System</b> models an enterprise multi-branch banking operation using compiled Oracle Database "
        "objects. Rather than handling transaction consistency in external scripts, all data integrity, monetary movement, overdraft guards, "
        "and auditing rules are enforced directly on the Oracle database server.", body_style
    ))
    story.append(Paragraph(
        "<b>ACID Implementation Highlights:</b><br/>"
        "• <b>Atomicity:</b> In money transfers, funds are deducted from the sender and credited to the receiver inside one transaction. If any check fails, <code>ROLLBACK</code> restores both balances immediately.<br/>"
        "• <b>Consistency:</b> Check constraints prevent negative balances, while foreign keys guarantee referential integrity.<br/>"
        "• <b>Isolation:</b> Pessimistic row-level locks (<code>SELECT ... FOR UPDATE</code>) prevent race conditions when two transfers hit the same account simultaneously.<br/>"
        "• <b>Durability:</b> All completed transactions are written permanently to redologs upon explicit <code>COMMIT</code>.", body_style
    ))

    story.append(Paragraph("2. ENTITY-RELATIONSHIP (ER) DIAGRAM & CARDINALITY", h1_style))
    story.append(Paragraph(
        "The diagram below defines the complete relational topology across all 11 normalized database entities (3NF), "
        "highlighting primary keys (PK), foreign keys (FK), and 1:N associations:", body_style
    ))

    er_img_path = r"d:\college\RDBMS\mini_project\documentation\ER_DIAGRAM.png"
    if os.path.exists(er_img_path):
        img_er = Image(er_img_path, width=455, height=255)
        t_er = Table([[img_er]], colWidths=[455])
        t_er.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, c_black),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(t_er)
        story.append(Spacer(1, 4))

    er_card_data = [
        [Paragraph("<b>Parent Table</b>", table_cell_bold), Paragraph("<b>Child Table</b>", table_cell_bold), Paragraph("<b>Foreign Key</b>", table_cell_bold), Paragraph("<b>Card.</b>", table_cell_bold), Paragraph("<b>Simple Real-World Meaning</b>", table_cell_bold)],
        [Paragraph("BANK_BRANCHES", table_cell), Paragraph("EMPLOYEES", table_cell), Paragraph("BRANCH_ID", table_cell), Paragraph("1 : N", table_cell), Paragraph("One branch employs multiple staff members.", table_cell)],
        [Paragraph("BANK_BRANCHES", table_cell), Paragraph("BANK_ACCOUNTS", table_cell), Paragraph("BRANCH_ID", table_cell), Paragraph("1 : N", table_cell), Paragraph("One branch holds multiple customer bank accounts.", table_cell)],
        [Paragraph("CUSTOMERS", table_cell), Paragraph("BANK_ACCOUNTS", table_cell), Paragraph("CUSTOMER_ID", table_cell), Paragraph("1 : N", table_cell), Paragraph("One customer can open multiple accounts (Savings, Current, FD).", table_cell)],
        [Paragraph("ACCOUNT_TYPES", table_cell), Paragraph("BANK_ACCOUNTS", table_cell), Paragraph("TYPE_ID", table_cell), Paragraph("1 : N", table_cell), Paragraph("Defines minimum balance and interest rules for accounts.", table_cell)],
        [Paragraph("BANK_ACCOUNTS", table_cell), Paragraph("TRANSACTIONS", table_cell), Paragraph("ACCOUNT_ID", table_cell), Paragraph("1 : N", table_cell), Paragraph("Every deposit, withdrawal, or transfer creates a transaction record.", table_cell)],
        [Paragraph("CUSTOMERS", table_cell), Paragraph("BENEFICIARIES", table_cell), Paragraph("CUSTOMER_ID", table_cell), Paragraph("1 : N", table_cell), Paragraph("Customers can register pre-approved transfer recipients.", table_cell)],
        [Paragraph("CUSTOMERS", table_cell), Paragraph("LOANS", table_cell), Paragraph("CUSTOMER_ID", table_cell), Paragraph("1 : N", table_cell), Paragraph("Customers can apply for multiple loans (Home, Auto, Personal).", table_cell)],
        [Paragraph("LOANS", table_cell), Paragraph("LOAN_PAYMENTS", table_cell), Paragraph("LOAN_ID", table_cell), Paragraph("1 : N", table_cell), Paragraph("Each loan is repaid through multiple monthly EMI installments.", table_cell)]
    ]
    t_er_card = Table(er_card_data, colWidths=[80, 80, 90, 35, 175])
    t_er_card.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_black),
        ('TEXTCOLOR', (0,0), (-1,0), c_white),
        ('GRID', (0,0), (-1,-1), 0.5, c_black),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8f8f8")]),
    ]))
    story.append(t_er_card)

    # =========================================================================
    # SECTION 3: DATABASE SCHEMA DDL QUERIES (TABLE CREATION & CONSTRAINTS)
    # =========================================================================
    story.append(Paragraph("3. DATABASE SCHEMA DDL QUERIES WITH SIMPLE EXPLANATIONS", h1_style))
    story.append(Paragraph(
        "Below is every single table creation query executed in <code>02_create_tables.sql</code> and <code>03_constraints.sql</code>. "
        "Each query is followed by a clear, simple explanation of its purpose in the banking system:", body_style
    ))

    ddl_sections = [
        ("Table 1: BANK_BRANCHES (Branch Network)",
"""CREATE TABLE BANK_BRANCHES (
    BRANCH_ID       NUMBER(10)      CONSTRAINT PK_BRANCHES PRIMARY KEY,
    BRANCH_NAME     VARCHAR2(100)   NOT NULL,
    BRANCH_CODE     VARCHAR2(20)    CONSTRAINT UQ_BRANCH_CODE UNIQUE NOT NULL,
    IFSC_CODE       VARCHAR2(20)    CONSTRAINT UQ_BRANCH_IFSC UNIQUE NOT NULL,
    ADDRESS         VARCHAR2(255)   NOT NULL,
    CITY            VARCHAR2(50)    NOT NULL,
    STATE           VARCHAR2(50)    NOT NULL,
    PIN_CODE        VARCHAR2(10)    NOT NULL,
    PHONE           VARCHAR2(20),
    MANAGER_NAME    VARCHAR2(100),
    CREATED_AT      DATE            DEFAULT SYSDATE NOT NULL
);""",
         "💡 <b>In Simple Words:</b> This query creates the master table for all physical bank branches. <code>BRANCH_ID</code> uniquely identifies each branch, while <code>UNIQUE</code> constraints prevent two branches from sharing the same Branch Code or IFSC Code. <code>SYSDATE</code> automatically records when the branch was added."),

        ("Table 2: CUSTOMERS (Customer Profiles & KYC)",
"""CREATE TABLE CUSTOMERS (
    CUSTOMER_ID     NUMBER(10)      CONSTRAINT PK_CUSTOMERS PRIMARY KEY,
    FIRST_NAME      VARCHAR2(50)    NOT NULL,
    LAST_NAME       VARCHAR2(50)    NOT NULL,
    EMAIL           VARCHAR2(100)   CONSTRAINT UQ_CUST_EMAIL UNIQUE NOT NULL,
    PHONE           VARCHAR2(20)    CONSTRAINT UQ_CUST_PHONE UNIQUE NOT NULL,
    DATE_OF_BIRTH   DATE            NOT NULL,
    GENDER          VARCHAR2(10)    CONSTRAINT CK_CUST_GENDER CHECK (GENDER IN ('Male','Female','Other')),
    ADDRESS         VARCHAR2(255)   NOT NULL,
    CITY            VARCHAR2(50)    NOT NULL,
    STATE           VARCHAR2(50)    NOT NULL,
    PIN_CODE        VARCHAR2(10)    NOT NULL,
    KYC_STATUS      VARCHAR2(20)    DEFAULT 'Verified' CONSTRAINT CK_CUST_KYC CHECK (KYC_STATUS IN ('Verified','Pending','Rejected')),
    CREATED_AT      DATE            DEFAULT SYSDATE NOT NULL,
    UPDATED_AT      DATE            DEFAULT SYSDATE NOT NULL
);""",
         "💡 <b>In Simple Words:</b> Stores personal and contact details for all bank customers. <code>UNIQUE</code> constraints ensure no two customers have the same email or mobile number. <code>CHECK</code> constraints ensure that Gender and KYC Status only accept valid banking values."),

        ("Table 3: EMPLOYEES (Bank Staff)",
"""CREATE TABLE EMPLOYEES (
    EMPLOYEE_ID     NUMBER(10)      CONSTRAINT PK_EMPLOYEES PRIMARY KEY,
    BRANCH_ID       NUMBER(10)      CONSTRAINT FK_EMP_BRANCH REFERENCES BANK_BRANCHES(BRANCH_ID),
    FIRST_NAME      VARCHAR2(50)    NOT NULL,
    LAST_NAME       VARCHAR2(50)    NOT NULL,
    EMAIL           VARCHAR2(100)   CONSTRAINT UQ_EMP_EMAIL UNIQUE NOT NULL,
    PHONE           VARCHAR2(20)    NOT NULL,
    ROLE            VARCHAR2(50)    NOT NULL,
    SALARY          NUMBER(12,2)    CONSTRAINT CK_EMP_SALARY CHECK (SALARY > 0),
    HIRE_DATE       DATE            NOT NULL,
    STATUS          VARCHAR2(20)    DEFAULT 'Active' CONSTRAINT CK_EMP_STATUS CHECK (STATUS IN ('Active','Inactive','Terminated')),
    CREATED_AT      DATE            DEFAULT SYSDATE NOT NULL
);""",
         "💡 <b>In Simple Words:</b> Stores bank staff records (tellers, managers, loan officers). <code>FOREIGN KEY (BRANCH_ID)</code> guarantees that an employee is assigned to an existing branch. <code>CHECK (SALARY > 0)</code> stops zero or negative salaries from ever being entered."),

        ("Table 4: ACCOUNT_TYPES (Savings, Current, FD)",
"""CREATE TABLE ACCOUNT_TYPES (
    TYPE_ID             NUMBER(5)       CONSTRAINT PK_ACC_TYPES PRIMARY KEY,
    TYPE_NAME           VARCHAR2(50)    CONSTRAINT UQ_TYPE_NAME UNIQUE NOT NULL,
    MIN_BALANCE         NUMBER(12,2)    DEFAULT 1000.00 CONSTRAINT CK_TYPE_MIN_BAL CHECK (MIN_BALANCE >= 0),
    INTEREST_RATE       NUMBER(5,2)     DEFAULT 3.50 CONSTRAINT CK_TYPE_RATE CHECK (INTEREST_RATE >= 0),
    OVERDRAFT_ALLOWED   VARCHAR2(1)     DEFAULT 'N' CONSTRAINT CK_TYPE_OD CHECK (OVERDRAFT_ALLOWED IN ('Y','N')),
    DESCRIPTION         VARCHAR2(255)
);""",
         "💡 <b>In Simple Words:</b> A lookup catalog defining bank account categories (Savings, Current, Fixed Deposit). It defines the minimum balance requirement, default interest rate, and whether overdraft protection is permitted for each tier."),

        ("Table 5: BANK_ACCOUNTS (Customer Depository Accounts)",
"""CREATE TABLE BANK_ACCOUNTS (
    ACCOUNT_ID          NUMBER(10)      CONSTRAINT PK_ACCOUNTS PRIMARY KEY,
    ACCOUNT_NUMBER      VARCHAR2(20)    CONSTRAINT UQ_ACC_NUM UNIQUE NOT NULL,
    CUSTOMER_ID         NUMBER(10)      CONSTRAINT FK_ACC_CUST REFERENCES CUSTOMERS(CUSTOMER_ID),
    BRANCH_ID           NUMBER(10)      CONSTRAINT FK_ACC_BRANCH REFERENCES BANK_BRANCHES(BRANCH_ID),
    TYPE_ID             NUMBER(5)       CONSTRAINT FK_ACC_TYPE REFERENCES ACCOUNT_TYPES(TYPE_ID),
    BALANCE             NUMBER(15,2)    DEFAULT 0.00 CONSTRAINT CK_ACC_BAL CHECK (BALANCE >= 0),
    OVERDRAFT_LIMIT     NUMBER(12,2)    DEFAULT 0.00 CONSTRAINT CK_ACC_OD CHECK (OVERDRAFT_LIMIT >= 0),
    ACCOUNT_STATUS      VARCHAR2(20)    DEFAULT 'Active' CONSTRAINT CK_ACC_STATUS CHECK (ACCOUNT_STATUS IN ('Active','Inactive','Dormant','Frozen')),
    OPENED_DATE         DATE            DEFAULT SYSDATE NOT NULL,
    CREATED_AT          DATE            DEFAULT SYSDATE NOT NULL,
    UPDATED_AT          DATE            DEFAULT SYSDATE NOT NULL
);""",
         "💡 <b>In Simple Words:</b> The central financial table holding real-time balances for every account. Connects Customer, Branch, and Account Type via foreign keys. <code>CHECK (BALANCE >= 0)</code> ensures account balance cannot drop below zero unless covered by overdraft."),

        ("Table 6: TRANSACTIONS (Double-Entry Financial Ledger)",
"""CREATE TABLE TRANSACTIONS (
    TRANSACTION_ID      NUMBER(12)      CONSTRAINT PK_TRANSACTIONS PRIMARY KEY,
    TRANSACTION_REF     VARCHAR2(30)    CONSTRAINT UQ_TXN_REF UNIQUE NOT NULL,
    ACCOUNT_ID          NUMBER(10)      CONSTRAINT FK_TXN_ACC REFERENCES BANK_ACCOUNTS(ACCOUNT_ID),
    TRANSACTION_TYPE    VARCHAR2(25)    CONSTRAINT CK_TXN_TYPE CHECK (TRANSACTION_TYPE IN ('Deposit','Withdrawal','Transfer_Debit','Transfer_Credit','Interest','Loan_Disbursement','Loan_Repayment')),
    AMOUNT              NUMBER(15,2)    CONSTRAINT CK_TXN_AMOUNT CHECK (AMOUNT > 0),
    BALANCE_AFTER       NUMBER(15,2)    NOT NULL,
    TRANSACTION_DATE    TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,
    RELATED_ACCOUNT_ID  NUMBER(10),
    DESCRIPTION         VARCHAR2(255)   NOT NULL,
    TRANSACTION_STATUS  VARCHAR2(20)    DEFAULT 'Completed' CONSTRAINT CK_TXN_STATUS CHECK (TRANSACTION_STATUS IN ('Completed','Failed','Reversed','Pending'))
);""",
         "💡 <b>In Simple Words:</b> An immutable audit journal of every cash deposit, withdrawal, or transfer. It records the transaction type, amount, exact timestamp, and the ending balance after the operation. <code>CHECK (AMOUNT > 0)</code> rejects zero or negative transaction amounts."),

        ("Table 7: BENEFICIARIES (Pre-Approved Transfer Payees)",
"""CREATE TABLE BENEFICIARIES (
    BENEFICIARY_ID          NUMBER(10)      CONSTRAINT PK_BENEFICIARIES PRIMARY KEY,
    CUSTOMER_ID             NUMBER(10)      CONSTRAINT FK_BENEF_CUST REFERENCES CUSTOMERS(CUSTOMER_ID),
    BENEFICIARY_NAME        VARCHAR2(100)   NOT NULL,
    BENEFICIARY_ACCOUNT     VARCHAR2(20)    NOT NULL,
    BANK_NAME               VARCHAR2(100)   NOT NULL,
    IFSC_CODE               VARCHAR2(20)    NOT NULL,
    TRANSFER_LIMIT          NUMBER(12,2)    DEFAULT 50000.00 CONSTRAINT CK_BENEF_LIMIT CHECK (TRANSFER_LIMIT > 0),
    STATUS                  VARCHAR2(20)    DEFAULT 'Active' CONSTRAINT CK_BENEF_STATUS CHECK (STATUS IN ('Active','Inactive')),
    ADDED_DATE              DATE            DEFAULT SYSDATE NOT NULL
);""",
         "💡 <b>In Simple Words:</b> Stores pre-approved payee contacts added by customers for quick fund transfers. Sets a maximum per-transaction transfer limit (e.g. ₹50,000) to protect against unauthorized large withdrawals."),

        ("Table 8: LOANS (Credit Facilities & Amortization)",
"""CREATE TABLE LOANS (
    LOAN_ID                 NUMBER(10)      CONSTRAINT PK_LOANS PRIMARY KEY,
    LOAN_NUMBER             VARCHAR2(20)    CONSTRAINT UQ_LOAN_NUM UNIQUE NOT NULL,
    CUSTOMER_ID             NUMBER(10)      CONSTRAINT FK_LOAN_CUST REFERENCES CUSTOMERS(CUSTOMER_ID),
    BRANCH_ID               NUMBER(10)      CONSTRAINT FK_LOAN_BRANCH REFERENCES BANK_BRANCHES(BRANCH_ID),
    LOAN_TYPE               VARCHAR2(50)    NOT NULL,
    LOAN_AMOUNT             NUMBER(15,2)    CONSTRAINT CK_LOAN_AMT CHECK (LOAN_AMOUNT > 0),
    INTEREST_RATE           NUMBER(5,2)     CONSTRAINT CK_LOAN_RATE CHECK (INTEREST_RATE > 0),
    TERM_MONTHS             NUMBER(5)       CONSTRAINT CK_LOAN_TERM CHECK (TERM_MONTHS > 0),
    MONTHLY_EMI             NUMBER(12,2)    CONSTRAINT CK_LOAN_EMI CHECK (MONTHLY_EMI >= 0),
    OUTSTANDING_BALANCE     NUMBER(15,2)    CONSTRAINT CK_LOAN_BAL CHECK (OUTSTANDING_BALANCE >= 0),
    LOAN_STATUS             VARCHAR2(20)    DEFAULT 'Pending' CONSTRAINT CK_LOAN_STATUS CHECK (LOAN_STATUS IN ('Pending','Approved','Rejected','Active','Closed','Defaulted')),
    APPLICATION_DATE        DATE            DEFAULT SYSDATE NOT NULL,
    APPROVAL_DATE           DATE
);""",
         "💡 <b>In Simple Words:</b> Manages disbursed loans and credit facilities. Stores the total principal, annual interest rate, tenure in months, calculated monthly installment (EMI), and remaining unpaid balance. Tracks status from Pending to Approved or Closed."),

        ("Table 9: LOAN_PAYMENTS (EMI Installments Ledger)",
"""CREATE TABLE LOAN_PAYMENTS (
    PAYMENT_ID              NUMBER(10)      CONSTRAINT PK_LOAN_PAYMENTS PRIMARY KEY,
    PAYMENT_REF             VARCHAR2(30)    CONSTRAINT UQ_PAYMENT_REF UNIQUE NOT NULL,
    LOAN_ID                 NUMBER(10)      CONSTRAINT FK_PAY_LOAN REFERENCES LOANS(LOAN_ID),
    PAYMENT_AMOUNT          NUMBER(12,2)    CONSTRAINT CK_PAY_AMT CHECK (PAYMENT_AMOUNT > 0),
    PRINCIPAL_COMPONENT     NUMBER(12,2)    CONSTRAINT CK_PAY_PRIN CHECK (PRINCIPAL_COMPONENT >= 0),
    INTEREST_COMPONENT      NUMBER(12,2)    CONSTRAINT CK_PAY_INT CHECK (INTEREST_COMPONENT >= 0),
    PAYMENT_DATE            DATE            DEFAULT SYSDATE NOT NULL,
    PAYMENT_METHOD          VARCHAR2(50)    DEFAULT 'Online Transfer' NOT NULL,
    PAYMENT_STATUS          VARCHAR2(20)    DEFAULT 'Completed' CONSTRAINT CK_PAY_STATUS CHECK (PAYMENT_STATUS IN ('Completed','Pending','Failed'))
);""",
         "💡 <b>In Simple Words:</b> Records each monthly EMI repayment made by a borrower. It breaks down the installment into how much went toward reducing the principal loan balance and how much went to the bank as interest."),

        ("Table 10: AUDIT_LOGS (Autonomous Security Trail)",
"""CREATE TABLE AUDIT_LOGS (
    LOG_ID              NUMBER(12)      CONSTRAINT PK_AUDIT_LOGS PRIMARY KEY,
    TABLE_NAME          VARCHAR2(50)    NOT NULL,
    OPERATION_TYPE      VARCHAR2(10)    CONSTRAINT CK_LOG_OP CHECK (OPERATION_TYPE IN ('INSERT','UPDATE','DELETE')),
    RECORD_ID           VARCHAR2(50)    NOT NULL,
    OLD_VALUE           VARCHAR2(4000),
    NEW_VALUE           VARCHAR2(4000),
    CHANGED_BY          VARCHAR2(50)    DEFAULT USER NOT NULL,
    CHANGED_AT          TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,
    CLIENT_IP           VARCHAR2(50)    DEFAULT '127.0.0.1' NOT NULL
);""",
         "💡 <b>In Simple Words:</b> An immutable compliance log populated automatically by database triggers. Whenever an account balance or status changes, this table records who made the change, the old value, the new value, and the exact timestamp."),

        ("Table 11: ADMIN_USERS (Privileged Bank Staff Logins)",
"""CREATE TABLE ADMIN_USERS (
    ADMIN_ID            NUMBER(5)       CONSTRAINT PK_ADMIN_USERS PRIMARY KEY,
    USERNAME            VARCHAR2(50)    CONSTRAINT UQ_ADMIN_USER UNIQUE NOT NULL,
    PASSWORD_HASH       VARCHAR2(255)   NOT NULL,
    FULL_NAME           VARCHAR2(100)   NOT NULL,
    EMAIL               VARCHAR2(100)   CONSTRAINT UQ_ADMIN_EMAIL UNIQUE NOT NULL,
    ROLE                VARCHAR2(30)    DEFAULT 'Bank Manager' CONSTRAINT CK_ADMIN_ROLE CHECK (ROLE IN ('Super Admin','Bank Manager','Branch Auditor','Loan Officer')),
    STATUS              VARCHAR2(20)    DEFAULT 'Active' CONSTRAINT CK_ADMIN_STATUS CHECK (STATUS IN ('Active','Inactive')),
    LAST_LOGIN          DATE,
    CREATED_AT          DATE            DEFAULT SYSDATE NOT NULL
);""",
         "💡 <b>In Simple Words:</b> Stores privileged banking staff credentials. Uses secure password hashes (never plain text) and enforces Role-Based Access Control (RBAC) across managers, auditors, and tellers.")
    ]

    for title, code, expl in ddl_sections:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
        story.append(Paragraph(expl, expl_style))

    # =========================================================================
    # SECTION 4: DATA MANIPULATION (DML) - SEED DATA
    # =========================================================================
    story.append(Paragraph("4. SAMPLE RECORD INSERTION QUERIES (DML)", h1_style))
    story.append(Paragraph(
        "Realistic operational records were seeded across all 11 tables via <code>06_seed_data.sql</code> to demonstrate functioning data:", body_style
    ))

    dml_code = """-- 1. Inserting Bank Branches
INSERT INTO BANK_BRANCHES (BRANCH_ID, BRANCH_NAME, BRANCH_CODE, IFSC_CODE, ADDRESS, CITY, STATE, PIN_CODE, PHONE, MANAGER_NAME)
VALUES (101, 'Nariman Point Branch', 'BR001', 'SMBL0001001', 'Tower 1, Nariman Point', 'Mumbai', 'Maharashtra', '400021', '+91-22-22851234', 'Rajesh Verma');

-- 2. Inserting Verified Customer Profile
INSERT INTO CUSTOMERS (CUSTOMER_ID, FIRST_NAME, LAST_NAME, EMAIL, PHONE, DATE_OF_BIRTH, GENDER, ADDRESS, CITY, STATE, PIN_CODE, KYC_STATUS)
VALUES (1001, 'Aarav', 'Sharma', 'aarav.sharma@example.com', '+91-9876543210', TO_DATE('1988-05-14','YYYY-MM-DD'), 'Male', 'Worli Sea Face', 'Mumbai', 'Maharashtra', '400018', 'Verified');

-- 3. Provisioning Bank Accounts
INSERT INTO BANK_ACCOUNTS (ACCOUNT_ID, ACCOUNT_NUMBER, CUSTOMER_ID, BRANCH_ID, TYPE_ID, BALANCE, OVERDRAFT_LIMIT, ACCOUNT_STATUS)
VALUES (2001, 'SB1001002001', 1001, 101, 1, 48500.00, 0.00, 'Active');

-- 4. Recording Initial Cash Deposit Transaction
INSERT INTO TRANSACTIONS (TRANSACTION_ID, TRANSACTION_REF, ACCOUNT_ID, TRANSACTION_TYPE, AMOUNT, BALANCE_AFTER, TRANSACTION_DATE, DESCRIPTION, TRANSACTION_STATUS)
VALUES (3001, 'TXN-20261101-000001', 2001, 'Deposit', 20000.00, 48500.00, SYSTIMESTAMP - 20, 'Initial Account Opening Cash Deposit', 'Completed');

-- 5. Creating Active Loan Facility
INSERT INTO LOANS (LOAN_ID, LOAN_NUMBER, CUSTOMER_ID, BRANCH_ID, LOAN_TYPE, LOAN_AMOUNT, INTEREST_RATE, TERM_MONTHS, MONTHLY_EMI, OUTSTANDING_BALANCE, LOAN_STATUS)
VALUES (4001, 'LN-2026-0001', 1001, 101, 'Home Loan', 2500000.00, 8.50, 240, 21696.52, 2350000.00, 'Active');
COMMIT;"""
    story.append(Paragraph(dml_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
    story.append(Paragraph("💡 <b>In Simple Words:</b> These DML queries populate sample records so the bank has live data to work with. They create an active branch in Mumbai, register customer Aarav Sharma, open a Savings account with ₹48,500, log the opening deposit, disburse a Home Loan of ₹25 Lakhs, and issue a final <code>COMMIT</code> to save the changes permanently.", expl_style))

    # =========================================================================
    # SECTION 5: RELATIONAL VIEWS & MATERIALIZED VIEWS
    # =========================================================================
    story.append(Paragraph("5. RELATIONAL VIEWS & MATERIALIZED VIEWS", h1_style))
    story.append(Paragraph(
        "Views save complex join queries as reusable virtual tables. Script <code>07_views.sql</code> and <code>08_materialized_views_synonyms.sql</code> define:", body_style
    ))

    views_data = [
        ("CUSTOMER_ACCOUNT_VIEW (360-Degree Profile View)",
"""CREATE OR REPLACE VIEW CUSTOMER_ACCOUNT_VIEW AS
SELECT 
    c.CUSTOMER_ID,
    c.FIRST_NAME || ' ' || c.LAST_NAME AS CUSTOMER_NAME,
    c.EMAIL, c.PHONE, c.KYC_STATUS,
    b.BRANCH_NAME, b.IFSC_CODE,
    a.ACCOUNT_NUMBER, t.TYPE_NAME AS ACCOUNT_TYPE,
    a.BALANCE, a.OVERDRAFT_LIMIT, a.ACCOUNT_STATUS
FROM CUSTOMERS c
JOIN BANK_ACCOUNTS a ON c.CUSTOMER_ID = a.CUSTOMER_ID
JOIN BANK_BRANCHES b ON a.BRANCH_ID = b.BRANCH_ID
JOIN ACCOUNT_TYPES t ON a.TYPE_ID = t.TYPE_ID;""",
         "💡 <b>In Simple Words:</b> Instead of writing 4 separate joins every time you need a customer's banking summary, this view combines Customer, Account, Branch, and Account Type tables into one virtual table for instant reporting."),

        ("MV_BRANCH_SUMMARY (Materialized View for Fast Reporting)",
"""CREATE MATERIALIZED VIEW MV_BRANCH_SUMMARY
BUILD IMMEDIATE
REFRESH FORCE ON DEMAND
AS
SELECT 
    b.BRANCH_ID, b.BRANCH_NAME, b.CITY,
    COUNT(DISTINCT a.ACCOUNT_ID) AS TOTAL_ACCOUNTS,
    NVL(SUM(a.BALANCE), 0) AS TOTAL_DEPOSITS,
    COUNT(DISTINCT l.LOAN_ID) AS TOTAL_LOANS,
    NVL(SUM(l.OUTSTANDING_BALANCE), 0) AS TOTAL_LOAN_BOOK
FROM BANK_BRANCHES b
LEFT JOIN BANK_ACCOUNTS a ON b.BRANCH_ID = a.BRANCH_ID AND a.ACCOUNT_STATUS = 'Active'
LEFT JOIN LOANS l ON b.BRANCH_ID = l.BRANCH_ID AND l.LOAN_STATUS = 'Active'
GROUP BY b.BRANCH_ID, b.BRANCH_NAME, b.CITY;""",
         "💡 <b>In Simple Words:</b> Unlike a normal view that runs its query on every request, a <b>Materialized View</b> physically pre-computes and stores the summary totals (total deposits, total loans per branch) on disk. This gives instant reporting without slowing down the database.")
    ]

    for title, code, expl in views_data:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
        story.append(Paragraph(expl, expl_style))

    # =========================================================================
    # SECTION 6: USER-DEFINED FUNCTIONS (PL/SQL)
    # =========================================================================
    story.append(Paragraph("6. USER-DEFINED PL/SQL FUNCTIONS", h1_style))
    story.append(Paragraph(
        "User-defined functions perform calculations and return values directly inside SQL queries (<code>09_functions.sql</code>):", body_style
    ))

    func_data = [
        ("Function 1: CALCULATE_MONTHLY_EMI (Reducing-Balance Amortization)",
"""CREATE OR REPLACE FUNCTION CALCULATE_MONTHLY_EMI (
    p_principal   IN NUMBER,
    p_annual_rate IN NUMBER,
    p_term_months IN NUMBER
) RETURN NUMBER IS
    v_r NUMBER; -- Monthly Interest Rate
BEGIN
    IF p_principal <= 0 OR p_annual_rate <= 0 OR p_term_months <= 0 THEN RETURN 0; END IF;
    v_r := p_annual_rate / 1200;
    -- Standard Formula: EMI = [P * r * (1+r)^n] / [(1+r)^n - 1]
    RETURN ROUND(p_principal * v_r * POWER(1 + v_r, p_term_months) / (POWER(1 + v_r, p_term_months) - 1), 2);
EXCEPTION
    WHEN OTHERS THEN RETURN 0;
END CALCULATE_MONTHLY_EMI;
/""",
         "💡 <b>In Simple Words:</b> Calculates the exact monthly loan EMI payment for any given Principal amount, Annual Interest Rate, and Tenure in months using standard banking reducing-balance amortization formulas."),

        ("Function 2: GET_ACCOUNT_BALANCE (Balance Inquiry)",
"""CREATE OR REPLACE FUNCTION GET_ACCOUNT_BALANCE (p_account_number IN VARCHAR2) RETURN NUMBER IS
    v_balance NUMBER(15,2);
BEGIN
    SELECT BALANCE INTO v_balance FROM BANK_ACCOUNTS WHERE ACCOUNT_NUMBER = p_account_number;
    RETURN v_balance;
EXCEPTION
    WHEN NO_DATA_FOUND THEN RETURN -1; -- Returns -1 if account does not exist
END GET_ACCOUNT_BALANCE;
/""",
         "💡 <b>In Simple Words:</b> Takes an Account Number as input and immediately returns its live balance. If the account does not exist, it safely returns -1 instead of crashing the program."),

        ("Function 3: CHECK_ACCOUNT_STATUS (Account State Guard)",
"""CREATE OR REPLACE FUNCTION CHECK_ACCOUNT_STATUS (p_account_number IN VARCHAR2) RETURN VARCHAR2 IS
    v_status VARCHAR2(20);
BEGIN
    SELECT ACCOUNT_STATUS INTO v_status FROM BANK_ACCOUNTS WHERE ACCOUNT_NUMBER = p_account_number;
    RETURN v_status;
EXCEPTION
    WHEN NO_DATA_FOUND THEN RETURN 'NOT_FOUND';
END CHECK_ACCOUNT_STATUS;
/""",
         "💡 <b>In Simple Words:</b> Checks whether a given bank account is 'Active', 'Dormant', or 'Frozen'. Used to ensure inactive or frozen accounts cannot withdraw or transfer money.")
    ]

    for title, code, expl in func_data:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
        story.append(Paragraph(expl, expl_style))

    # =========================================================================
    # SECTION 7: CORE BANKING STORED PROCEDURES (PL/SQL)
    # =========================================================================
    story.append(Paragraph("7. CORE BANKING STORED PROCEDURES (PL/SQL)", h1_style))
    story.append(Paragraph(
        "Stored procedures encapsulate complete multi-step business transactions with row-level locks, minimum balance validation, "
        "and exception handling in <code>10_procedures.sql</code>:", body_style
    ))

    proc_data = [
        ("Procedure 1: TRANSFER_MONEY (Two-Phase Atomic Transfer with FOR UPDATE)",
"""CREATE OR REPLACE PROCEDURE TRANSFER_MONEY (
    p_from_acc IN VARCHAR2, p_to_acc IN VARCHAR2, p_amount IN NUMBER,
    p_txn_ref OUT VARCHAR2, p_status OUT VARCHAR2, p_message OUT VARCHAR2
) IS
    v_from_id NUMBER; v_to_id NUMBER; v_bal NUMBER; v_ref VARCHAR2(30);
    e_low_balance EXCEPTION;
BEGIN
    IF p_amount <= 0 THEN RAISE_APPLICATION_ERROR(-20001, 'Amount must be > 0'); END IF;
    -- Pessimistic locking prevents race conditions and concurrent double-spending
    SELECT ACCOUNT_ID, BALANCE INTO v_from_id, v_bal FROM BANK_ACCOUNTS WHERE ACCOUNT_NUMBER = p_from_acc FOR UPDATE;
    SELECT ACCOUNT_ID INTO v_to_id FROM BANK_ACCOUNTS WHERE ACCOUNT_NUMBER = p_to_acc FOR UPDATE;
    IF v_bal < p_amount THEN RAISE e_low_balance; END IF;
    -- Atomic debit and credit inside a single database transaction
    UPDATE BANK_ACCOUNTS SET BALANCE = BALANCE - p_amount WHERE ACCOUNT_ID = v_from_id;
    UPDATE BANK_ACCOUNTS SET BALANCE = BALANCE + p_amount WHERE ACCOUNT_ID = v_to_id;
    v_ref := 'TRF-' || TO_CHAR(SYSDATE, 'YYYYMMDD') || '-' || LPAD(SEQ_TRANSACTIONS.NEXTVAL, 6, '0');
    INSERT INTO TRANSACTIONS (TRANSACTION_ID, TRANSACTION_REF, ACCOUNT_ID, TRANSACTION_TYPE, AMOUNT, BALANCE_AFTER)
    VALUES (SEQ_TRANSACTIONS.CURRVAL, v_ref, v_from_id, 'Transfer_Debit', p_amount, v_bal - p_amount);
    INSERT INTO TRANSACTIONS (TRANSACTION_ID, TRANSACTION_REF, ACCOUNT_ID, TRANSACTION_TYPE, AMOUNT, BALANCE_AFTER)
    VALUES (SEQ_TRANSACTIONS.NEXTVAL, v_ref||'-C', v_to_id, 'Transfer_Credit', p_amount, (SELECT BALANCE FROM BANK_ACCOUNTS WHERE ACCOUNT_ID=v_to_id));
    COMMIT; -- Atomically commits both account updates and ledger entries
    p_txn_ref := v_ref; p_status := 'SUCCESS'; p_message := 'Transfer complete.';
EXCEPTION
    WHEN e_low_balance THEN ROLLBACK; p_status := 'FAIL'; p_message := 'Insufficient funds.';
    WHEN NO_DATA_FOUND THEN ROLLBACK; p_status := 'FAIL'; p_message := 'Invalid account.';
    WHEN OTHERS THEN ROLLBACK; p_status := 'ERROR'; p_message := SQLERRM;
END TRANSFER_MONEY;
/""",
         "💡 <b>In Simple Words:</b> This is the most critical procedure in the banking system. It transfers money between two accounts safely. First, it uses <code>FOR UPDATE</code> to lock both account rows so no other transaction can touch them at the same time. Then it checks if the sender has enough balance. It deducts the amount from the sender, adds it to the receiver, and writes two transaction records. If anything fails, it runs <code>ROLLBACK</code> so money is never lost or partially deducted."),

        ("Procedure 2: DEPOSIT_MONEY (Cash Credit with Row Locking)",
"""CREATE OR REPLACE PROCEDURE DEPOSIT_MONEY (
    p_account_number IN VARCHAR2, p_amount IN NUMBER,
    p_txn_ref OUT VARCHAR2, p_new_balance OUT NUMBER, p_status OUT VARCHAR2, p_message OUT VARCHAR2
) IS
    v_acc_id NUMBER; v_bal NUMBER; v_ref VARCHAR2(30);
BEGIN
    IF p_amount <= 0 THEN RAISE_APPLICATION_ERROR(-20002, 'Deposit must be > 0'); END IF;
    SELECT ACCOUNT_ID, BALANCE INTO v_acc_id, v_bal FROM BANK_ACCOUNTS WHERE ACCOUNT_NUMBER = p_account_number FOR UPDATE;
    v_bal := v_bal + p_amount;
    v_ref := 'DEP-' || TO_CHAR(SYSDATE, 'YYYYMMDD') || '-' || LPAD(SEQ_TRANSACTIONS.NEXTVAL, 6, '0');
    UPDATE BANK_ACCOUNTS SET BALANCE = v_bal, UPDATED_AT = SYSDATE WHERE ACCOUNT_ID = v_acc_id;
    INSERT INTO TRANSACTIONS (TRANSACTION_ID, TRANSACTION_REF, ACCOUNT_ID, TRANSACTION_TYPE, AMOUNT, BALANCE_AFTER)
    VALUES (SEQ_TRANSACTIONS.CURRVAL, v_ref, v_acc_id, 'Deposit', p_amount, v_bal);
    COMMIT;
    p_txn_ref := v_ref; p_new_balance := v_bal; p_status := 'SUCCESS'; p_message := 'Deposit successful.';
EXCEPTION
    WHEN NO_DATA_FOUND THEN ROLLBACK; p_status := 'ERROR'; p_message := 'Account not found.';
END DEPOSIT_MONEY;
/""",
         "💡 <b>In Simple Words:</b> Increases an account's balance by the deposit amount, inserts a 'Deposit' transaction record into the ledger, and permanently commits the changes. Validates that the deposit amount is greater than zero."),

        ("Procedure 3: WITHDRAW_MONEY (Cash Debit with Overdraft Checking)",
"""CREATE OR REPLACE PROCEDURE WITHDRAW_MONEY (
    p_account_number IN VARCHAR2, p_amount IN NUMBER,
    p_txn_ref OUT VARCHAR2, p_new_balance OUT NUMBER, p_status OUT VARCHAR2, p_message OUT VARCHAR2
) IS
    v_acc_id NUMBER; v_bal NUMBER; v_od NUMBER; v_ref VARCHAR2(30);
    e_low_balance EXCEPTION;
BEGIN
    IF p_amount <= 0 THEN RAISE_APPLICATION_ERROR(-20003, 'Withdrawal must be > 0'); END IF;
    SELECT ACCOUNT_ID, BALANCE, OVERDRAFT_LIMIT INTO v_acc_id, v_bal, v_od FROM BANK_ACCOUNTS WHERE ACCOUNT_NUMBER = p_account_number FOR UPDATE;
    IF (v_bal + v_od) < p_amount THEN RAISE e_low_balance; END IF;
    v_bal := v_bal - p_amount;
    v_ref := 'WTH-' || TO_CHAR(SYSDATE, 'YYYYMMDD') || '-' || LPAD(SEQ_TRANSACTIONS.NEXTVAL, 6, '0');
    UPDATE BANK_ACCOUNTS SET BALANCE = v_bal, UPDATED_AT = SYSDATE WHERE ACCOUNT_ID = v_acc_id;
    INSERT INTO TRANSACTIONS (TRANSACTION_ID, TRANSACTION_REF, ACCOUNT_ID, TRANSACTION_TYPE, AMOUNT, BALANCE_AFTER)
    VALUES (SEQ_TRANSACTIONS.CURRVAL, v_ref, v_acc_id, 'Withdrawal', p_amount, v_bal);
    COMMIT;
    p_txn_ref := v_ref; p_new_balance := v_bal; p_status := 'SUCCESS'; p_message := 'Withdrawal successful.';
EXCEPTION
    WHEN e_low_balance THEN ROLLBACK; p_status := 'FAIL'; p_message := 'Insufficient funds.';
    WHEN NO_DATA_FOUND THEN ROLLBACK; p_status := 'ERROR'; p_message := 'Account not found.';
END WITHDRAW_MONEY;
/""",
         "💡 <b>In Simple Words:</b> Checks if the account has enough money (including any overdraft limit). If yes, it reduces the balance, creates a 'Withdrawal' transaction record, and commits. If the balance is insufficient, it raises an exception and aborts without altering the balance.")
    ]

    for title, code, expl in proc_data:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
        story.append(Paragraph(expl, expl_style))

    # =========================================================================
    # SECTION 8: AUTONOMOUS DATABASE TRIGGERS (PL/SQL)
    # =========================================================================
    story.append(Paragraph("8. AUTONOMOUS DATABASE TRIGGERS (PL/SQL)", h1_style))
    story.append(Paragraph(
        "Triggers automatically fire in response to DML operations, enforcing business rules and capturing audit trails (<code>11_triggers.sql</code>):", body_style
    ))

    trigger_data = [
        ("Trigger 1: TRG_ACCOUNTS_AUDIT (Audit Trail with :OLD and :NEW Pseudorecords)",
"""CREATE OR REPLACE TRIGGER TRG_ACCOUNTS_AUDIT
AFTER UPDATE OF BALANCE, ACCOUNT_STATUS ON BANK_ACCOUNTS
FOR EACH ROW
DECLARE
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    INSERT INTO AUDIT_LOGS (
        LOG_ID, TABLE_NAME, OPERATION_TYPE, RECORD_ID,
        OLD_VALUE, NEW_VALUE, CHANGED_BY, CHANGED_AT
    ) VALUES (
        SEQ_AUDIT_LOGS.NEXTVAL,
        'BANK_ACCOUNTS',
        'UPDATE',
        TO_CHAR(:OLD.ACCOUNT_ID),
        'BAL=' || :OLD.BALANCE || ', STATUS=' || :OLD.ACCOUNT_STATUS,
        'BAL=' || :NEW.BALANCE || ', STATUS=' || :NEW.ACCOUNT_STATUS,
        USER,
        SYSTIMESTAMP
    );
    COMMIT; -- Autonomous commit preserves audit even if outer transaction rolls back
END TRG_ACCOUNTS_AUDIT;
/""",
         "💡 <b>In Simple Words:</b> Whenever an account balance or status is updated, this trigger automatically records the old balance (<code>:OLD.BALANCE</code>) and the new balance (<code>:NEW.BALANCE</code>) into the <code>AUDIT_LOGS</code> table. Because it uses <code>PRAGMA AUTONOMOUS_TRANSACTION</code>, this audit record is permanently saved even if the main transaction is later rolled back."),

        ("Trigger 2: TRG_VALIDATE_ACCOUNT_MIN_BAL (Minimum Balance Guard)",
"""CREATE OR REPLACE TRIGGER TRG_VALIDATE_ACCOUNT_MIN_BAL
BEFORE INSERT ON BANK_ACCOUNTS
FOR EACH ROW
DECLARE
    v_min_bal NUMBER(12,2);
BEGIN
    SELECT MIN_BALANCE INTO v_min_bal FROM ACCOUNT_TYPES WHERE TYPE_ID = :NEW.TYPE_ID;
    IF :NEW.BALANCE < v_min_bal THEN
        RAISE_APPLICATION_ERROR(-20002, 'Initial deposit INR ' || :NEW.BALANCE || ' is below minimum requirement of INR ' || v_min_bal);
    END IF;
END TRG_VALIDATE_ACCOUNT_MIN_BAL;
/""",
         "💡 <b>In Simple Words:</b> Before a new bank account row is inserted, this trigger checks if the opening deposit satisfies the minimum balance rule of that account type. If someone tries to open an account with less than the minimum balance, it raises an error (-20002) and cancels the insert."),

        ("Trigger 3: TRG_CUSTOMERS_BIU (Automated Timestamp Touch)",
"""CREATE OR REPLACE TRIGGER TRG_CUSTOMERS_BIU
BEFORE INSERT OR UPDATE ON CUSTOMERS
FOR EACH ROW
BEGIN
    IF INSERTING THEN
        :NEW.CREATED_AT := SYSDATE;
        :NEW.UPDATED_AT := SYSDATE;
    ELSIF UPDATING THEN
        :NEW.UPDATED_AT := SYSDATE;
    END IF;
END TRG_CUSTOMERS_BIU;
/""",
         "💡 <b>In Simple Words:</b> Automatically sets the creation date when a customer is added, and automatically updates the <code>UPDATED_AT</code> timestamp whenever any customer details (address, phone) are modified.")
    ]

    for title, code, expl in trigger_data:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
        story.append(Paragraph(expl, expl_style))

    # =========================================================================
    # SECTION 9: MODULAR PL/SQL PACKAGES
    # =========================================================================
    story.append(Paragraph("9. MODULAR PL/SQL PACKAGES (SPECIFICATION & BODY)", h1_style))
    story.append(Paragraph(
        "Packages group related procedures, functions, and cursor types together into a single compiled unit in the database:", body_style
    ))

    package_code = """-- BANKING_PACKAGE Specification (12_banking_package.sql)
CREATE OR REPLACE PACKAGE BANKING_PACKAGE AS
    TYPE t_txn_cursor IS REF CURSOR;
    PROCEDURE DEPOSIT (p_acc_no IN VARCHAR2, p_amt IN NUMBER, p_desc IN VARCHAR2, p_ref OUT VARCHAR2, p_bal OUT NUMBER, p_status OUT VARCHAR2, p_msg OUT VARCHAR2);
    PROCEDURE WITHDRAW (p_acc_no IN VARCHAR2, p_amt IN NUMBER, p_desc IN VARCHAR2, p_ref OUT VARCHAR2, p_bal OUT NUMBER, p_status OUT VARCHAR2, p_msg OUT VARCHAR2);
    PROCEDURE TRANSFER (p_src_acc IN VARCHAR2, p_dest_acc IN VARCHAR2, p_amt IN NUMBER, p_desc IN VARCHAR2, p_ref OUT VARCHAR2, p_status OUT VARCHAR2, p_msg OUT VARCHAR2);
    FUNCTION GET_BALANCE (p_acc_no IN VARCHAR2) RETURN NUMBER;
    PROCEDURE GET_STATEMENT (p_acc_no IN VARCHAR2, p_limit IN NUMBER, p_cursor OUT t_txn_cursor);
END BANKING_PACKAGE;
/

-- LOAN_PACKAGE Specification (13_loan_package.sql)
CREATE OR REPLACE PACKAGE LOAN_PACKAGE AS
    FUNCTION CALCULATE_EMI (p_principal IN NUMBER, p_rate IN NUMBER, p_months IN NUMBER) RETURN NUMBER;
    PROCEDURE APPLY_LOAN (p_cust_id IN NUMBER, p_branch_id IN NUMBER, p_type IN VARCHAR2, p_amt IN NUMBER, p_rate IN NUMBER, p_months IN NUMBER, p_loan_id OUT NUMBER, p_loan_num OUT VARCHAR2, p_status OUT VARCHAR2, p_msg OUT VARCHAR2);
    PROCEDURE APPROVE_LOAN (p_loan_id IN NUMBER, p_disburse_acc IN VARCHAR2, p_status OUT VARCHAR2, p_msg OUT VARCHAR2);
    PROCEDURE PROCESS_PAYMENT (p_loan_id IN NUMBER, p_pay_acc IN VARCHAR2, p_amt IN NUMBER, p_ref OUT VARCHAR2, p_new_bal OUT NUMBER, p_status OUT VARCHAR2, p_msg OUT VARCHAR2);
END LOAN_PACKAGE;
/"""
    story.append(Paragraph(package_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
    story.append(Paragraph("💡 <b>In Simple Words:</b> A PL/SQL <b>Package</b> is like an organized folder that holds related procedures and functions together. <code>BANKING_PACKAGE</code> groups all cash deposits, withdrawals, transfers, and account statements. <code>LOAN_PACKAGE</code> groups loan applications, credit approvals, and EMI payments. Packaging improves database memory caching and keeps code clean and modular.", expl_style))

    # =========================================================================
    # SECTION 10: CURSORS & ADVANCED PL/SQL
    # =========================================================================
    story.append(Paragraph("10. PL/SQL CURSORS & ADVANCED PL/SQL CONCEPTS", h1_style))
    story.append(Paragraph(
        "Demonstrates explicit cursors, parameterized cursors, collections, and bulk collection processing (<code>14_cursors_demo.sql</code> & <code>15_advanced_plsql.sql</code>):", body_style
    ))

    cursor_code = """-- 1. Explicit Cursor with Attributes (%FOUND, %NOTFOUND, %ROWCOUNT)
DECLARE
    CURSOR c_high_value_accs IS
        SELECT ACCOUNT_NUMBER, BALANCE FROM BANK_ACCOUNTS WHERE BALANCE >= 50000.00 ORDER BY BALANCE DESC;
    v_acc_no BANK_ACCOUNTS.ACCOUNT_NUMBER%TYPE;
    v_bal    BANK_ACCOUNTS.BALANCE%TYPE;
BEGIN
    OPEN c_high_value_accs;
    LOOP
        FETCH c_high_value_accs INTO v_acc_no, v_bal;
        EXIT WHEN c_high_value_accs%NOTFOUND;
        DBMS_OUTPUT.PUT_LINE('Row #' || c_high_value_accs%ROWCOUNT || ' | Account: ' || v_acc_no || ' | Balance: ' || v_bal);
    END LOOP;
    CLOSE c_high_value_accs;
END;
/

-- 2. High-Performance Bulk Processing with BULK COLLECT and FORALL
DECLARE
    TYPE t_acc_ids IS TABLE OF BANK_ACCOUNTS.ACCOUNT_ID%TYPE;
    TYPE t_balances IS TABLE OF BANK_ACCOUNTS.BALANCE%TYPE;
    v_ids  t_acc_ids;
    v_bals t_balances;
BEGIN
    -- Fetch thousands of rows in a single database context switch
    SELECT ACCOUNT_ID, BALANCE BULK COLLECT INTO v_ids, v_bals
    FROM BANK_ACCOUNTS WHERE ACCOUNT_STATUS = 'Active';

    -- Batch update minimizing SQL/PLSQL engine switches
    FORALL i IN 1..v_ids.COUNT
        UPDATE BANK_ACCOUNTS SET UPDATED_AT = SYSDATE WHERE ACCOUNT_ID = v_ids(i);
    COMMIT;
END;
/"""
    story.append(Paragraph(cursor_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
    story.append(Paragraph("💡 <b>In Simple Words:</b> Cursors allow PL/SQL to process query results row-by-row. The explicit cursor iterates through accounts holding over ₹50,000 using <code>%NOTFOUND</code> to detect the end. <code>BULK COLLECT</code> and <code>FORALL</code> are high-performance tools that fetch and update thousands of records at once in memory, making bulk batch updates 10x to 20x faster than traditional loops.", expl_style))

    # =========================================================================
    # SECTION 11: COMPLEX ANALYTICAL SQL QUERIES (JOINS, SUBQUERIES, SETS)
    # =========================================================================
    story.append(Paragraph("11. COMPLEX ANALYTICAL SQL QUERIES (JOINS, SUBQUERIES & SET OPERATORS)", h1_style))
    story.append(Paragraph(
        "Demonstrated in <code>16_sql_concepts_demonstration.sql</code> across all required SQL analytical forms:", body_style
    ))

    queries_data = [
        ("Query 1: INNER JOIN (Active Account Holders)",
"""SELECT c.FIRST_NAME || ' ' || c.LAST_NAME AS HOLDER, a.ACCOUNT_NUMBER, a.BALANCE
FROM CUSTOMERS c
INNER JOIN BANK_ACCOUNTS a ON c.CUSTOMER_ID = a.CUSTOMER_ID;""",
         "💡 <b>In Simple Words:</b> Matches records that exist in both tables: returns customers who currently hold at least one bank account."),

        ("Query 2: LEFT OUTER JOIN (All Customers, Including Those Without Loans)",
"""SELECT c.CUSTOMER_ID, c.FIRST_NAME || ' ' || c.LAST_NAME AS NAME, NVL(SUM(l.LOAN_AMOUNT), 0) AS TOTAL_BORROWED
FROM CUSTOMERS c
LEFT OUTER JOIN LOANS l ON c.CUSTOMER_ID = l.CUSTOMER_ID
GROUP BY c.CUSTOMER_ID, c.FIRST_NAME, c.LAST_NAME;""",
         "💡 <b>In Simple Words:</b> Lists every customer in the bank and their total borrowed loan amount. If a customer has never taken a loan, <code>NVL</code> neatly displays 0 instead of blank (NULL)."),

        ("Query 3: SELF JOIN (Employees and Branch Hierarchy)",
"""SELECT e1.FIRST_NAME || ' ' || e1.LAST_NAME AS EMPLOYEE, e1.ROLE,
       NVL(e2.FIRST_NAME || ' ' || e2.LAST_NAME, 'Branch Head') AS SUPERVISOR
FROM EMPLOYEES e1
LEFT JOIN EMPLOYEES e2 ON e1.BRANCH_ID = e2.BRANCH_ID AND e2.ROLE = 'Assistant Manager' AND e1.EMPLOYEE_ID <> e2.EMPLOYEE_ID;""",
         "💡 <b>In Simple Words:</b> Joins the <code>EMPLOYEES</code> table with itself to display each staff member alongside their branch supervisor."),

        ("Query 4: CORRELATED SUBQUERY (Accounts Above Branch Average)",
"""SELECT a.ACCOUNT_NUMBER, a.BALANCE, a.BRANCH_ID
FROM BANK_ACCOUNTS a
WHERE a.BALANCE > (
    SELECT AVG(b.BALANCE) FROM BANK_ACCOUNTS b WHERE b.BRANCH_ID = a.BRANCH_ID
);""",
         "💡 <b>In Simple Words:</b> For every account, the subquery calculates the average balance of its specific branch, and only returns accounts that hold more money than their branch average."),

        ("Query 5: SET OPERATORS (MINUS: Deposited But Never Withdrawn)",
"""SELECT ACCOUNT_ID FROM TRANSACTIONS WHERE TRANSACTION_TYPE = 'Deposit'
MINUS
SELECT ACCOUNT_ID FROM TRANSACTIONS WHERE TRANSACTION_TYPE = 'Withdrawal';""",
         "💡 <b>In Simple Words:</b> The <code>MINUS</code> operator compares two result sets and returns accounts that have received cash deposits but have never made any withdrawals.")
    ]

    for title, code, expl in queries_data:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
        story.append(Paragraph(expl, expl_style))

    # =========================================================================
    # SECTION 12: TESTING AND VERIFICATION RESULTS
    # =========================================================================
    story.append(Paragraph("12. TESTING AND VERIFICATION RESULTS (12 MANDATORY TEST CASES)", h1_style))
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
    t_test = Table(test_rows, colWidths=[18, 110, 125, 155, 47])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_black),
        ('TEXTCOLOR', (0,0), (-1,0), c_white),
        ('GRID', (0,0), (-1,-1), 0.5, c_black),
        ('TOPPADDING', (0,0), (-1,-1), 1.6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8f8f8")]),
    ]))
    story.append(t_test)
    story.append(Spacer(1, 3))
    story.append(Paragraph("💡 <b>In Simple Words:</b> This test suite proves that our banking database works correctly in all situations: money is credited and debited properly, overdraft limits and minimum balances are respected, invalid transfers are safely rejected without losing money, and every change is recorded in the audit logs.", expl_style))

    # Master Execution Instructions
    story.append(Paragraph("13. SQL*PLUS MASTER SCRIPT EXECUTION", h1_style))
    story.append(Paragraph(
        "All database objects can be executed sequentially using the master script <code>RUN_ALL.SQL</code> or the "
        "automated administrator batch launcher <code>run_sqlplus_admin.bat</code>:<br/>"
        "• <b>Automated Administrator Execution:</b> Right-click <code>database/run_sqlplus_admin.bat</code> → <i>Run as administrator</i>.<br/>"
        "• <b>Direct SQL*Plus Command Line:</b> <code>cd /d d:\\college\\RDBMS\\mini_project\\database</code> &amp;&amp; <code>sqlplus root/root@ORCLA @RUN_ALL.SQL</code>.<br/>"
        "All spool output is written to <code>SMART_BANKING_DEPLOYMENT.LOG</code>.", body_style
    ))

    # =========================================================================
    # SECTION 14: PROJECT TEAM & WORK BREAKDOWN STRUCTURE (WBS)
    # =========================================================================
    story.append(Paragraph("14. ACADEMIC PROJECT TEAM & WORK BREAKDOWN STRUCTURE (WBS)", h1_style))
    wbs_data = [
        [Paragraph("<b>Sr.</b>", table_cell_bold), Paragraph("<b>Student Full Name</b>", table_cell_bold), Paragraph("<b>Enrollment No.</b>", table_cell_bold), Paragraph("<b>Key Responsibilities & Project Modules</b>", table_cell_bold)],
        [Paragraph("1", table_cell), Paragraph("<b>Vaghela Yagnadeepsinh.C</b>", table_cell), Paragraph("260203030002", table_cell), Paragraph("Project Architecture, 3NF Relational Schema Design, Master Deployment Script (RUN_ALL.SQL), ER Diagram Modeling & Transaction Isolation.", table_cell)],
        [Paragraph("2", table_cell), Paragraph("<b>Chudasama Krishnadeepsinh .S</b>", table_cell), Paragraph("260203030001", table_cell), Paragraph("PL/SQL Stored Procedures (TRANSFER_MONEY, DEPOSIT, WITHDRAW), Mathematical Functions (EMI), BANKING_PACKAGE & LOAN_PACKAGE.", table_cell)],
        [Paragraph("3", table_cell), Paragraph("<b>Chauhan Jaydip. P</b>", table_cell), Paragraph("260203020035", table_cell), Paragraph("Complex Analytical Queries, Relational Joins (INNER, OUTER, SELF, CROSS), Subqueries (Correlated, EXISTS), and Relational Views.", table_cell)],
        [Paragraph("4", table_cell), Paragraph("<b>Gohil Jignesh. P</b>", table_cell), Paragraph("260203020034", table_cell), Paragraph("Autonomous Database Triggers (Audit & Min-Balance Guards), 12-Case Test Suite Verification & Technical Project Documentation.", table_cell)],
    ]
    t_wbs = Table(wbs_data, colWidths=[20, 135, 90, 210])
    t_wbs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_black),
        ('TEXTCOLOR', (0,0), (-1,0), c_white),
        ('BOX', (0,0), (-1,-1), 1, c_black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_black),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8f8f8")]),
    ]))
    story.append(t_wbs)
    story.append(Spacer(1, 3))

    story.append(Paragraph("15. REFERENCES", h1_style))
    refs = [
        "1. Oracle Corporation. <i>Oracle Database SQL Language Reference, 10g/19c/23ai</i>.",
        "2. Oracle Corporation. <i>Oracle Database PL/SQL Packages and Types Reference</i>.",
        "3. Silberschatz, A., Korth, H. F., & Sudarshan, S. <i>Database System Concepts (7th Edition)</i>. McGraw-Hill.",
        "4. Feuerstein, S., & Pribyl, B. <i>Oracle PL/SQL Programming (6th Edition)</i>. O'Reilly Media."
    ]
    for ref in refs:
        story.append(Paragraph(ref, body_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("16. ORACLE DATABASE CONCEPTS IMPLEMENTATION MATRIX", h1_style))
    matrix_rows = [
        [Paragraph("<b>Oracle SQL / PL/SQL Domain</b>", table_cell_bold), Paragraph("<b>Implementation Script / DB Object</b>", table_cell_bold), Paragraph("<b>Verification</b>", table_cell_bold)],
        [Paragraph("DDL (CREATE, ALTER, DROP, TRUNCATE)", table_cell), Paragraph("<code>02_create_tables.sql</code> (11 Relational Entities)", table_cell), Paragraph("<b>VERIFIED</b>", table_cell)],
        [Paragraph("Constraints (PK, FK, CHECK, UNIQUE, NOT NULL)", table_cell), Paragraph("<code>03_constraints.sql</code> (Domain & Referential Integrity)", table_cell), Paragraph("<b>VERIFIED</b>", table_cell)],
        [Paragraph("ACID Transactions (FOR UPDATE, COMMIT, ROLLBACK)", table_cell), Paragraph("<code>10_procedures.sql</code> (<code>TRANSFER_MONEY</code>)", table_cell), Paragraph("<b>VERIFIED</b>", table_cell)],
        [Paragraph("Database Objects (Views, MV, Sequences, Synonyms)", table_cell), Paragraph("<code>04_sequences.sql</code>, <code>07_views.sql</code>, <code>08_materialized_views_synonyms.sql</code>", table_cell), Paragraph("<b>VERIFIED</b>", table_cell)],
        [Paragraph("PL/SQL Procedures & Functions", table_cell), Paragraph("<code>09_functions.sql</code>, <code>10_procedures.sql</code>", table_cell), Paragraph("<b>VERIFIED</b>", table_cell)],
        [Paragraph("Autonomous Triggers (:OLD, :NEW, PRAGMA)", table_cell), Paragraph("<code>11_triggers.sql</code> (<code>TRG_ACCOUNTS_AUDIT</code>)", table_cell), Paragraph("<b>VERIFIED</b>", table_cell)],
        [Paragraph("Modular Packages (Spec & Body)", table_cell), Paragraph("<code>12_banking_package.sql</code>, <code>13_loan_package.sql</code>", table_cell), Paragraph("<b>VERIFIED</b>", table_cell)],
        [Paragraph("Cursors & Bulk Processing (BULK COLLECT, FORALL)", table_cell), Paragraph("<code>14_cursors_demo.sql</code>, <code>15_advanced_plsql.sql</code>", table_cell), Paragraph("<b>VERIFIED</b>", table_cell)],
        [Paragraph("Complex Queries (Joins, Correlated Subqueries, MINUS)", table_cell), Paragraph("<code>16_sql_concepts_demonstration.sql</code>", table_cell), Paragraph("<b>VERIFIED</b>", table_cell)],
    ]
    t_mat = Table(matrix_rows, colWidths=[150, 245, 60])
    t_mat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_black),
        ('TEXTCOLOR', (0,0), (-1,0), c_white),
        ('GRID', (0,0), (-1,-1), 0.5, c_black),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8f8f8")]),
    ]))
    story.append(t_mat)
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        "<b>Technical Conclusion:</b> The Smart Banking Management System successfully proves that all enterprise banking business rules "
        "— including concurrency locking, two-phase fund transfers, autonomous audit logging, and loan amortization — are most securely "
        "and efficiently executed within the compiled Oracle Database engine. All scripts are completely tested and verified via SQL*Plus.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF successfully generated at:", pdf_path)

if __name__ == "__main__":
    build_pdf()
