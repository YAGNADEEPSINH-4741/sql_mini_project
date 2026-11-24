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
        self.drawString(50, 802, "Smart Banking Management System - Oracle SQL & PL/SQL Database Engineering Report")
        self.setStrokeColor(colors.black)
        self.setLineWidth(0.75)
        self.line(50, 794, 545, 794)

        # Running Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(545, 34, page_str)
        self.drawString(50, 34, "Department of Computer Science & Engineering | RDBMS Mini Project 2026-2027")
        self.line(50, 44, 545, 44)
        self.restoreState()

def build_pdf():
    pdf_path = r"d:\college\RDBMS\mini_project\documentation\SMART_BANKING_MANAGEMENT_SYSTEM_REPORT.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=52,
        bottomMargin=52
    )

    styles = getSampleStyleSheet()
    
    # Monochrome Palette (Pure Black & White)
    c_black = colors.black
    c_white = colors.white

    # Typography Styles - Dense, Clean, Publication-Grade
    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=24, leading=29,
        textColor=c_black, alignment=1, spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=12, leading=16,
        textColor=c_black, alignment=1, spaceAfter=16
    )
    h1_style = ParagraphStyle(
        'SectionHeading', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=12, leading=15,
        textColor=c_black, spaceBefore=10, spaceAfter=5, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'SubSectionHeading', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=12.5,
        textColor=c_black, spaceBefore=7, spaceAfter=3, keepWithNext=True
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
    code_style = ParagraphStyle(
        'ReportCode', parent=styles['Normal'],
        fontName='Courier', fontSize=6.8, leading=8.5,
        textColor=c_black,
        backColor=colors.HexColor("#f8f8f8"),
        borderPadding=4, spaceAfter=5, keepWithNext=True
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
    # SECTION 1: COVER PAGE (STRICTLY PAGE 1)
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("SMART BANKING MANAGEMENT SYSTEM", title_style))
    story.append(Paragraph("A Comprehensive Oracle SQL & Advanced PL/SQL Relational Database Project", subtitle_style))
    story.append(HRFlowable(width="90%", thickness=1.5, color=c_black, spaceBefore=4, spaceAfter=14))
    
    story.append(Paragraph("<b>ACADEMIC GROUP PROJECT TEAM</b>", ParagraphStyle('GroupHead', parent=body_bold, alignment=1, fontSize=10.5, textColor=c_black, spaceAfter=6)))
    
    students_data = [
        [Paragraph("<b>Sr.</b>", table_cell_bold), Paragraph("<b>Student Full Name</b>", table_cell_bold), Paragraph("<b>Enrollment Number</b>", table_cell_bold), Paragraph("<b>Core Module Specialization</b>", table_cell_bold)],
        [Paragraph("1", table_cell), Paragraph("<b>Vaghela Yagnadeepsinh.C</b>", table_cell), Paragraph("260203030002", table_cell_bold), Paragraph("Project Architecture, 3NF Normalization & Master Deployment Script", table_cell)],
        [Paragraph("2", table_cell), Paragraph("<b>Chudasama Krishnadeepsinh .S</b>", table_cell), Paragraph("260203030001", table_cell_bold), Paragraph("PL/SQL Stored Procedures, Functions & Package Implementation", table_cell)],
        [Paragraph("3", table_cell), Paragraph("<b>Chauhan Jaydip. P</b>", table_cell), Paragraph("260203020035", table_cell_bold), Paragraph("Complex Analytical Queries, Relational Joins & Subquery Optimization", table_cell)],
        [Paragraph("4", table_cell), Paragraph("<b>Gohil Jignesh. P</b>", table_cell), Paragraph("260203020034", table_cell_bold), Paragraph("Autonomous Triggers, Security Audit Trail & 12-Case Test Suite", table_cell)]
    ]
    t_students = Table(students_data, colWidths=[25, 140, 95, 185])
    t_students.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f0f0f0")),
        ('BOX', (0,0), (-1,-1), 1, c_black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_black),
    ]))
    story.append(t_students)
    story.append(Spacer(1, 10))

    meta_data = [
        [Paragraph("<b>Course:</b>", table_cell_bold), Paragraph("Relational Database Management Systems (RDBMS)", table_cell)],
        [Paragraph("<b>Project Category:</b>", table_cell_bold), Paragraph("Oracle SQL & Advanced PL/SQL Database Engineering Mini Project", table_cell)],
        [Paragraph("<b>Department:</b>", table_cell_bold), Paragraph("Department of Computer Science & Engineering", table_cell)],
        [Paragraph("<b>Database Engine:</b>", table_cell_bold), Paragraph("Oracle Database 10g / 11g / 12c / 19c / 21c / 23ai with Oracle SQL*Plus CLI", table_cell)],
        [Paragraph("<b>Core Capabilities:</b>", table_cell_bold), Paragraph("11 Tables (3NF), Sequences, B-Tree Indexes, Stored Procedures, Functions, Triggers, Packages, Cursors, Bulk Processing, Dynamic SQL, Audit Trails", table_cell)],
        [Paragraph("<b>Academic Year:</b>", table_cell_bold), Paragraph("2026 - 2027", table_cell)]
    ]
    t_meta = Table(meta_data, colWidths=[110, 335])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('BOX', (0,0), (-1,-1), 1, c_black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_black),
    ]))
    story.append(t_meta)
    
    story.append(Spacer(1, 14))
    story.append(Paragraph("<b>Primary Architectural Focus:</b> Relational Schema 3NF Normalization, ACID Transactional Atomicity, Row-Level Locking (<code>FOR UPDATE</code>), Two-Phase Fund Transfers, Autonomous Audit Triggers, Explicit & Parameterized Cursors, and Modular PL/SQL Packages.", ParagraphStyle('CoverNote', parent=body_style, alignment=1, fontSize=7.5, textColor=c_black)))
    story.append(PageBreak())  # Only page break: after the cover page!

    # =========================================================================
    # SECTION 2: SYSTEM ARCHITECTURE & ER DIAGRAM
    # =========================================================================
    story.append(Paragraph("1. SYSTEM OVERVIEW & RELATIONAL ARCHITECTURE", h1_style))
    story.append(Paragraph(
        "The <b>Smart Banking Management System</b> is an industrial-grade Oracle relational database architecture designed "
        "to manage enterprise banking operations. Rather than relying on superficial application-level abstractions, "
        "all business logic, mathematical calculations, validation guards, and security controls are compiled and executed "
        "directly within the Oracle Database engine via PL/SQL objects.", body_style
    ))
    story.append(Paragraph(
        "<b>ACID Transactional Guarantees:</b> Financial consistency is maintained through explicit Transaction Control Language (TCL) "
        "primitives (<code>COMMIT</code>, <code>ROLLBACK</code>, <code>SAVEPOINT</code>) and pessimistic row-level locking (<code>FOR UPDATE</code>). "
        "Two-phase fund transfers guarantee zero partial debits. Autonomous database triggers capture all state transitions "
        "into an immutable audit ledger.", body_style
    ))

    story.append(Paragraph("2. ENTITY-RELATIONSHIP (ER) DIAGRAM", h1_style))
    story.append(Paragraph(
        "The diagram below defines the complete relational topology across all 11 normalized database entities (3NF), "
        "highlighting primary keys (PK), foreign keys (FK), and 1:N associative constraints:", body_style
    ))

    er_img_path = r"d:\college\RDBMS\mini_project\documentation\ER_DIAGRAM.png"
    if os.path.exists(er_img_path):
        img_er = Image(er_img_path, width=445, height=255)
        t_er = Table([[img_er]], colWidths=[445])
        t_er.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, c_black),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(t_er)
        story.append(Spacer(1, 4))

    # Cardinality Mapping Table
    er_card_data = [
        [Paragraph("<b>Parent Entity</b>", table_cell_bold), Paragraph("<b>Child Entity</b>", table_cell_bold), Paragraph("<b>Foreign Key Attribute</b>", table_cell_bold), Paragraph("<b>Cardinality</b>", table_cell_bold), Paragraph("<b>Business Integrity Rule</b>", table_cell_bold)],
        [Paragraph("BANK_BRANCHES", table_cell), Paragraph("EMPLOYEES", table_cell), Paragraph("BRANCH_ID", table_cell), Paragraph("1 : N", table_cell), Paragraph("Every employee belongs to an authorized physical branch", table_cell)],
        [Paragraph("BANK_BRANCHES", table_cell), Paragraph("BANK_ACCOUNTS", table_cell), Paragraph("BRANCH_ID", table_cell), Paragraph("1 : N", table_cell), Paragraph("Accounts are domiciled under specific branch IFSC codes", table_cell)],
        [Paragraph("CUSTOMERS", table_cell), Paragraph("BANK_ACCOUNTS", table_cell), Paragraph("CUSTOMER_ID", table_cell), Paragraph("1 : N", table_cell), Paragraph("A customer may hold multiple accounts across different tiers", table_cell)],
        [Paragraph("ACCOUNT_TYPES", table_cell), Paragraph("BANK_ACCOUNTS", table_cell), Paragraph("TYPE_ID", table_cell), Paragraph("1 : N", table_cell), Paragraph("Enforces minimum opening balance and overdraft privileges", table_cell)],
        [Paragraph("BANK_ACCOUNTS", table_cell), Paragraph("TRANSACTIONS", table_cell), Paragraph("ACCOUNT_ID", table_cell), Paragraph("1 : N", table_cell), Paragraph("Double-entry audit log of all deposits, withdrawals, and transfers", table_cell)],
        [Paragraph("CUSTOMERS", table_cell), Paragraph("BENEFICIARIES", table_cell), Paragraph("CUSTOMER_ID", table_cell), Paragraph("1 : N", table_cell), Paragraph("Registered counterparties with individual transaction limits", table_cell)],
        [Paragraph("CUSTOMERS", table_cell), Paragraph("LOANS", table_cell), Paragraph("CUSTOMER_ID", table_cell), Paragraph("1 : N", table_cell), Paragraph("Credit facilities linked to vetted customer KYC profiles", table_cell)],
        [Paragraph("LOANS", table_cell), Paragraph("LOAN_PAYMENTS", table_cell), Paragraph("LOAN_ID", table_cell), Paragraph("1 : N", table_cell), Paragraph("Amortized EMI installments reducing outstanding loan balances", table_cell)]
    ]
    t_er_card = Table(er_card_data, colWidths=[80, 80, 95, 45, 145])
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
    story.append(Paragraph("3. DATABASE SCHEMA DDL QUERIES (11 NORMALIZED TABLES)", h1_style))
    story.append(Paragraph(
        "Below are the complete Oracle DDL queries executed via <code>02_create_tables.sql</code> and <code>03_constraints.sql</code> "
        "to instantiate the 11 relational tables with declarative primary keys, foreign keys, unique constraints, and check conditions:", body_style
    ))

    ddl_queries = [
        ("BANK_BRANCHES Table DDL",
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
);"""),

        ("CUSTOMERS Table DDL",
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
);"""),

        ("EMPLOYEES Table DDL",
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
);"""),

        ("ACCOUNT_TYPES Table DDL",
"""CREATE TABLE ACCOUNT_TYPES (
    TYPE_ID             NUMBER(5)       CONSTRAINT PK_ACC_TYPES PRIMARY KEY,
    TYPE_NAME           VARCHAR2(50)    CONSTRAINT UQ_TYPE_NAME UNIQUE NOT NULL,
    MIN_BALANCE         NUMBER(12,2)    DEFAULT 1000.00 CONSTRAINT CK_TYPE_MIN_BAL CHECK (MIN_BALANCE >= 0),
    INTEREST_RATE       NUMBER(5,2)     DEFAULT 3.50 CONSTRAINT CK_TYPE_RATE CHECK (INTEREST_RATE >= 0),
    OVERDRAFT_ALLOWED   VARCHAR2(1)     DEFAULT 'N' CONSTRAINT CK_TYPE_OD CHECK (OVERDRAFT_ALLOWED IN ('Y','N')),
    DESCRIPTION         VARCHAR2(255)
);"""),

        ("BANK_ACCOUNTS Table DDL",
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
);"""),

        ("TRANSACTIONS Table DDL",
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
);"""),

        ("BENEFICIARIES Table DDL",
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
);"""),

        ("LOANS Table DDL",
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
);"""),

        ("LOAN_PAYMENTS Table DDL",
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
);"""),

        ("AUDIT_LOGS Table DDL",
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
);"""),

        ("ADMIN_USERS Table DDL",
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
);""")
    ]

    for title, code in ddl_queries:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    # =========================================================================
    # SECTION 4: DATA INSERTION & SAMPLE SEED RECORDS (DML)
    # =========================================================================
    story.append(Paragraph("4. SAMPLE RECORD INSERTION QUERIES (DML)", h1_style))
    story.append(Paragraph(
        "Realistic operational records were populated into all 11 tables via <code>06_seed_data.sql</code> to support comprehensive "
        "query execution and business logic validation. Sample insertion statements are shown below:", body_style
    ))

    dml_sample = """-- 1. Seeding Bank Branches
INSERT INTO BANK_BRANCHES (BRANCH_ID, BRANCH_NAME, BRANCH_CODE, IFSC_CODE, ADDRESS, CITY, STATE, PIN_CODE, PHONE, MANAGER_NAME)
VALUES (101, 'Nariman Point Corporate Branch', 'BR001', 'SMBL0001001', 'Tower 1, Free Press Journal Marg, Nariman Point', 'Mumbai', 'Maharashtra', '400021', '+91-22-22851234', 'Rajesh Verma');

INSERT INTO BANK_BRANCHES (BRANCH_ID, BRANCH_NAME, BRANCH_CODE, IFSC_CODE, ADDRESS, CITY, STATE, PIN_CODE, PHONE, MANAGER_NAME)
VALUES (102, 'Connaught Place Premier Branch', 'BR002', 'SMBL0001002', 'Block B, Radial Road 3, Inner Circle, CP', 'New Delhi', 'Delhi', '110001', '+91-11-23345678', 'Sunita Rao');

-- 2. Seeding Customers
INSERT INTO CUSTOMERS (CUSTOMER_ID, FIRST_NAME, LAST_NAME, EMAIL, PHONE, DATE_OF_BIRTH, GENDER, ADDRESS, CITY, STATE, PIN_CODE, KYC_STATUS)
VALUES (1001, 'Aarav', 'Sharma', 'aarav.sharma@example.com', '+91-9876543210', TO_DATE('1988-05-14','YYYY-MM-DD'), 'Male', 'Flat 402, Sea Green Apts, Worli', 'Mumbai', 'Maharashtra', '400018', 'Verified');

INSERT INTO CUSTOMERS (CUSTOMER_ID, FIRST_NAME, LAST_NAME, EMAIL, PHONE, DATE_OF_BIRTH, GENDER, ADDRESS, CITY, STATE, PIN_CODE, KYC_STATUS)
VALUES (1002, 'Diya', 'Patel', 'diya.patel@example.com', '+91-9876543211', TO_DATE('1992-09-21','YYYY-MM-DD'), 'Female', '12 Vasant Kunj Sector C', 'New Delhi', 'Delhi', '110070', 'Verified');

-- 3. Seeding Bank Accounts
INSERT INTO BANK_ACCOUNTS (ACCOUNT_ID, ACCOUNT_NUMBER, CUSTOMER_ID, BRANCH_ID, TYPE_ID, BALANCE, OVERDRAFT_LIMIT, ACCOUNT_STATUS)
VALUES (2001, 'SB1001002001', 1001, 101, 1, 48500.00, 0.00, 'Active');

INSERT INTO BANK_ACCOUNTS (ACCOUNT_ID, ACCOUNT_NUMBER, CUSTOMER_ID, BRANCH_ID, TYPE_ID, BALANCE, OVERDRAFT_LIMIT, ACCOUNT_STATUS)
VALUES (2002, 'CA1001002002', 1001, 101, 2, 125000.00, 50000.00, 'Active');

-- 4. Seeding Immutable Double-Entry Transactions
INSERT INTO TRANSACTIONS (TRANSACTION_ID, TRANSACTION_REF, ACCOUNT_ID, TRANSACTION_TYPE, AMOUNT, BALANCE_AFTER, TRANSACTION_DATE, DESCRIPTION, TRANSACTION_STATUS)
VALUES (3001, 'TXN-20261101-000001', 2001, 'Deposit', 20000.00, 48500.00, SYSTIMESTAMP - 20, 'Initial Account Opening Cash Deposit', 'Completed');

INSERT INTO TRANSACTIONS (TRANSACTION_ID, TRANSACTION_REF, ACCOUNT_ID, TRANSACTION_TYPE, AMOUNT, BALANCE_AFTER, TRANSACTION_DATE, DESCRIPTION, TRANSACTION_STATUS)
VALUES (3002, 'TXN-20261105-000002', 2001, 'Withdrawal', 5000.00, 43500.00, SYSTIMESTAMP - 15, 'ATM Cash Withdrawal Mumbai Branch', 'Completed');

-- 5. Seeding Loans & Credit Amortization
INSERT INTO LOANS (LOAN_ID, LOAN_NUMBER, CUSTOMER_ID, BRANCH_ID, LOAN_TYPE, LOAN_AMOUNT, INTEREST_RATE, TERM_MONTHS, MONTHLY_EMI, OUTSTANDING_BALANCE, LOAN_STATUS, APPLICATION_DATE, APPROVAL_DATE)
VALUES (4001, 'LN-2026-0001', 1001, 101, 'Home Loan', 2500000.00, 8.50, 240, 21696.52, 2350000.00, 'Active', SYSDATE - 120, SYSDATE - 110);
COMMIT;"""
    story.append(Paragraph(dml_sample.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    # =========================================================================
    # SECTION 5: RELATIONAL VIEWS & MATERIALIZED VIEWS
    # =========================================================================
    story.append(Paragraph("5. RELATIONAL VIEWS & MATERIALIZED VIEWS", h1_style))
    story.append(Paragraph(
        "Views abstract multi-table complexity, provide unified patron summaries, and precompute analytical metrics. "
        "Script <code>07_views.sql</code> and <code>08_materialized_views_synonyms.sql</code> define the following database objects:", body_style
    ))

    view_queries = [
        ("CUSTOMER_ACCOUNT_VIEW (360-Degree Financial Profile)",
"""CREATE OR REPLACE VIEW CUSTOMER_ACCOUNT_VIEW AS
SELECT 
    c.CUSTOMER_ID,
    c.FIRST_NAME || ' ' || c.LAST_NAME AS CUSTOMER_NAME,
    c.EMAIL, c.PHONE, c.KYC_STATUS,
    b.BRANCH_NAME, b.IFSC_CODE,
    a.ACCOUNT_ID, a.ACCOUNT_NUMBER,
    t.TYPE_NAME AS ACCOUNT_TYPE,
    a.BALANCE, a.OVERDRAFT_LIMIT, a.ACCOUNT_STATUS,
    a.OPENED_DATE
FROM CUSTOMERS c
JOIN BANK_ACCOUNTS a ON c.CUSTOMER_ID = a.CUSTOMER_ID
JOIN BANK_BRANCHES b ON a.BRANCH_ID = b.BRANCH_ID
JOIN ACCOUNT_TYPES t ON a.TYPE_ID = t.TYPE_ID;"""),

        ("TRANSACTION_HISTORY_VIEW (Complete Ledger Audit Detail)",
"""CREATE OR REPLACE VIEW TRANSACTION_HISTORY_VIEW AS
SELECT 
    t.TRANSACTION_ID, t.TRANSACTION_REF,
    a.ACCOUNT_NUMBER,
    c.FIRST_NAME || ' ' || c.LAST_NAME AS ACCOUNT_HOLDER,
    t.TRANSACTION_TYPE, t.AMOUNT, t.BALANCE_AFTER,
    t.TRANSACTION_DATE, t.DESCRIPTION, t.TRANSACTION_STATUS,
    b.BRANCH_NAME
FROM TRANSACTIONS t
JOIN BANK_ACCOUNTS a ON t.ACCOUNT_ID = a.ACCOUNT_ID
JOIN CUSTOMERS c ON a.CUSTOMER_ID = c.CUSTOMER_ID
JOIN BANK_BRANCHES b ON a.BRANCH_ID = b.BRANCH_ID;"""),

        ("MV_BRANCH_SUMMARY (Materialized View for Reporting)",
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
GROUP BY b.BRANCH_ID, b.BRANCH_NAME, b.CITY;""")
    ]

    for title, code in view_queries:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    # =========================================================================
    # SECTION 6: USER-DEFINED FUNCTIONS (PL/SQL)
    # =========================================================================
    story.append(Paragraph("6. USER-DEFINED FUNCTIONS (PL/SQL)", h1_style))
    story.append(Paragraph(
        "All 6 required user-defined functions were created in <code>09_functions.sql</code>, encapsulating financial formulas "
        "and balance inquiries directly on the server:", body_style
    ))

    func_queries = [
        ("CALCULATE_MONTHLY_EMI (Reducing-Balance Amortization)",
"""CREATE OR REPLACE FUNCTION CALCULATE_MONTHLY_EMI (
    p_principal     IN NUMBER,
    p_annual_rate   IN NUMBER,
    p_term_months   IN NUMBER
) RETURN NUMBER IS
    v_monthly_rate  NUMBER;
    v_emi           NUMBER;
BEGIN
    IF p_principal <= 0 OR p_annual_rate <= 0 OR p_term_months <= 0 THEN
        RETURN 0;
    END IF;
    -- Monthly Interest Rate = Annual Rate / (12 * 100)
    v_monthly_rate := p_annual_rate / 1200;
    -- Standard Reducing Balance Formula: EMI = [P * r * (1+r)^n] / [(1+r)^n - 1]
    v_emi := p_principal * v_monthly_rate * (POWER(1 + v_monthly_rate, p_term_months)) 
             / (POWER(1 + v_monthly_rate, p_term_months) - 1);
    RETURN ROUND(v_emi, 2);
EXCEPTION
    WHEN ZERO_DIVIDE THEN
        RETURN ROUND(p_principal / p_term_months, 2);
    WHEN OTHERS THEN
        RETURN 0;
END CALCULATE_MONTHLY_EMI;
/"""),

        ("GET_ACCOUNT_BALANCE (Real-Time Balance Inquiry)",
"""CREATE OR REPLACE FUNCTION GET_ACCOUNT_BALANCE (
    p_account_number IN VARCHAR2
) RETURN NUMBER IS
    v_balance NUMBER(15,2);
BEGIN
    SELECT BALANCE INTO v_balance
    FROM BANK_ACCOUNTS
    WHERE ACCOUNT_NUMBER = p_account_number;
    RETURN v_balance;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN -1; -- Returns -1 when account does not exist
    WHEN OTHERS THEN
        RETURN -999;
END GET_ACCOUNT_BALANCE;
/"""),

        ("CHECK_ACCOUNT_STATUS (Account Operational State Guard)",
"""CREATE OR REPLACE FUNCTION CHECK_ACCOUNT_STATUS (
    p_account_number IN VARCHAR2
) RETURN VARCHAR2 IS
    v_status VARCHAR2(20);
BEGIN
    SELECT ACCOUNT_STATUS INTO v_status
    FROM BANK_ACCOUNTS
    WHERE ACCOUNT_NUMBER = p_account_number;
    RETURN v_status;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN 'NOT_FOUND';
    WHEN OTHERS THEN
        RETURN 'ERROR';
END CHECK_ACCOUNT_STATUS;
/""")
    ]

    for title, code in func_queries:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    # =========================================================================
    # SECTION 7: CORE BANKING STORED PROCEDURES (PL/SQL)
    # =========================================================================
    story.append(Paragraph("7. CORE BANKING STORED PROCEDURES (PL/SQL)", h1_style))
    story.append(Paragraph(
        "Stored procedures encapsulate complex transactional logic with row-level locks, minimum balance validation, "
        "and exception handling in <code>10_procedures.sql</code>:", body_style
    ))

    proc_queries = [
        ("TRANSFER_MONEY (Two-Phase Atomic Fund Transfer with FOR UPDATE)",
"""CREATE OR REPLACE PROCEDURE TRANSFER_MONEY (
    p_from_acc          IN  VARCHAR2,
    p_to_acc            IN  VARCHAR2,
    p_amount            IN  NUMBER,
    p_description       IN  VARCHAR2,
    p_txn_ref           OUT VARCHAR2,
    p_status            OUT VARCHAR2,
    p_message           OUT VARCHAR2
) IS
    v_from_id       NUMBER(10);
    v_to_id         NUMBER(10);
    v_from_bal      NUMBER(15,2);
    v_from_od       NUMBER(12,2);
    v_from_status   VARCHAR2(20);
    v_to_status     VARCHAR2(20);
    v_ref           VARCHAR2(30);
    e_insufficient_funds EXCEPTION;
    e_invalid_account    EXCEPTION;
BEGIN
    IF p_amount <= 0 THEN
        p_status := 'ERROR';
        p_message := 'Transfer amount must be strictly greater than zero.';
        RETURN;
    END IF;

    IF p_from_acc = p_to_acc THEN
        p_status := 'ERROR';
        p_message := 'Sender and receiver accounts cannot be identical.';
        RETURN;
    END IF;

    -- Lock Sender Account Row (Pessimistic Concurrency Guard)
    BEGIN
        SELECT ACCOUNT_ID, BALANCE, OVERDRAFT_LIMIT, ACCOUNT_STATUS 
        INTO v_from_id, v_from_bal, v_from_od, v_from_status
        FROM BANK_ACCOUNTS WHERE ACCOUNT_NUMBER = p_from_acc FOR UPDATE;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN RAISE e_invalid_account;
    END;

    -- Lock Receiver Account Row
    BEGIN
        SELECT ACCOUNT_ID, ACCOUNT_STATUS INTO v_to_id, v_to_status
        FROM BANK_ACCOUNTS WHERE ACCOUNT_NUMBER = p_to_acc FOR UPDATE;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN RAISE e_invalid_account;
    END;

    -- Verify Operational Status
    IF v_from_status <> 'Active' OR v_to_status <> 'Active' THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'One or both accounts are not in Active operational status.';
        RETURN;
    END IF;

    -- Check Balance Sufficiency
    IF (v_from_bal + v_from_od) < p_amount THEN
        RAISE e_insufficient_funds;
    END IF;

    -- Perform Atomic Debit and Credit
    UPDATE BANK_ACCOUNTS SET BALANCE = BALANCE - p_amount, UPDATED_AT = SYSDATE WHERE ACCOUNT_ID = v_from_id;
    UPDATE BANK_ACCOUNTS SET BALANCE = BALANCE + p_amount, UPDATED_AT = SYSDATE WHERE ACCOUNT_ID = v_to_id;

    -- Generate Unique Transaction Reference
    v_ref := 'TRF-' || TO_CHAR(SYSDATE, 'YYYYMMDD') || '-' || LPAD(SEQ_TRANSACTIONS.NEXTVAL, 6, '0');

    -- Insert Twin Double-Entry Ledger Records
    INSERT INTO TRANSACTIONS (TRANSACTION_ID, TRANSACTION_REF, ACCOUNT_ID, TRANSACTION_TYPE, AMOUNT, BALANCE_AFTER, TRANSACTION_DATE, RELATED_ACCOUNT_ID, DESCRIPTION, TRANSACTION_STATUS)
    VALUES (SEQ_TRANSACTIONS.CURRVAL, v_ref, v_from_id, 'Transfer_Debit', p_amount, v_from_bal - p_amount, SYSTIMESTAMP, v_to_id, NVL(p_description, 'Fund Transfer to ' || p_to_acc), 'Completed');

    INSERT INTO TRANSACTIONS (TRANSACTION_ID, TRANSACTION_REF, ACCOUNT_ID, TRANSACTION_TYPE, AMOUNT, BALANCE_AFTER, TRANSACTION_DATE, RELATED_ACCOUNT_ID, DESCRIPTION, TRANSACTION_STATUS)
    VALUES (SEQ_TRANSACTIONS.NEXTVAL, v_ref || '-C', v_to_id, 'Transfer_Credit', p_amount, (SELECT BALANCE FROM BANK_ACCOUNTS WHERE ACCOUNT_ID = v_to_id), SYSTIMESTAMP, v_from_id, 'Fund Received from ' || p_from_acc, 'Completed');

    COMMIT; -- Atomic Commit upon full success
    p_txn_ref := v_ref;
    p_status := 'SUCCESS';
    p_message := 'Transfer of INR ' || TO_CHAR(p_amount, '999,999,990.00') || ' completed successfully.';
EXCEPTION
    WHEN e_insufficient_funds THEN
        ROLLBACK;
        p_status := 'FAIL';
        p_message := 'Transfer rejected: Insufficient funds in sender account.';
    WHEN e_invalid_account THEN
        ROLLBACK;
        p_status := 'FAIL';
        p_message := 'Transfer rejected: Specified account number does not exist.';
    WHEN OTHERS THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'Transfer aborted due to database exception: ' || SQLERRM;
END TRANSFER_MONEY;
/"""),

        ("DEPOSIT_MONEY (Validated Cash Credit)",
"""CREATE OR REPLACE PROCEDURE DEPOSIT_MONEY (
    p_account_number    IN  VARCHAR2,
    p_amount            IN  NUMBER,
    p_description       IN  VARCHAR2,
    p_txn_ref           OUT VARCHAR2,
    p_new_balance       OUT NUMBER,
    p_status            OUT VARCHAR2,
    p_message           OUT VARCHAR2
) IS
    v_acc_id        NUMBER(10);
    v_current_bal   NUMBER(15,2);
    v_acc_status    VARCHAR2(20);
    v_ref           VARCHAR2(30);
BEGIN
    IF p_amount <= 0 THEN
        p_status := 'ERROR';
        p_message := 'Deposit amount must be strictly positive.';
        RETURN;
    END IF;

    SELECT ACCOUNT_ID, BALANCE, ACCOUNT_STATUS INTO v_acc_id, v_current_bal, v_acc_status
    FROM BANK_ACCOUNTS WHERE ACCOUNT_NUMBER = p_account_number FOR UPDATE;

    IF v_acc_status <> 'Active' THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'Cannot deposit into account with status: ' || v_acc_status;
        RETURN;
    END IF;

    v_current_bal := v_current_bal + p_amount;
    v_ref := 'DEP-' || TO_CHAR(SYSDATE, 'YYYYMMDD') || '-' || LPAD(SEQ_TRANSACTIONS.NEXTVAL, 6, '0');

    UPDATE BANK_ACCOUNTS SET BALANCE = v_current_bal, UPDATED_AT = SYSDATE WHERE ACCOUNT_ID = v_acc_id;

    INSERT INTO TRANSACTIONS (TRANSACTION_ID, TRANSACTION_REF, ACCOUNT_ID, TRANSACTION_TYPE, AMOUNT, BALANCE_AFTER, TRANSACTION_DATE, DESCRIPTION, TRANSACTION_STATUS)
    VALUES (SEQ_TRANSACTIONS.CURRVAL, v_ref, v_acc_id, 'Deposit', p_amount, v_current_bal, SYSTIMESTAMP, NVL(p_description, 'Cash Deposit'), 'Completed');

    COMMIT;
    p_txn_ref := v_ref;
    p_new_balance := v_current_bal;
    p_status := 'SUCCESS';
    p_message := 'Deposit of INR ' || TO_CHAR(p_amount, '999,999,990.00') || ' completed.';
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'Account number ' || p_account_number || ' not found.';
    WHEN OTHERS THEN
        ROLLBACK;
        p_status := 'FAIL';
        p_message := 'Deposit failed: ' || SQLERRM;
END DEPOSIT_MONEY;
/"""),

        ("WITHDRAW_MONEY (Validated Cash Debit with Overdraft Guard)",
"""CREATE OR REPLACE PROCEDURE WITHDRAW_MONEY (
    p_account_number    IN  VARCHAR2,
    p_amount            IN  NUMBER,
    p_description       IN  VARCHAR2,
    p_txn_ref           OUT VARCHAR2,
    p_new_balance       OUT NUMBER,
    p_status            OUT VARCHAR2,
    p_message           OUT VARCHAR2
) IS
    v_acc_id        NUMBER(10);
    v_current_bal   NUMBER(15,2);
    v_od_limit      NUMBER(12,2);
    v_acc_status    VARCHAR2(20);
    v_ref           VARCHAR2(30);
    e_insufficient_funds EXCEPTION;
BEGIN
    IF p_amount <= 0 THEN
        p_status := 'ERROR';
        p_message := 'Withdrawal amount must be greater than zero.';
        RETURN;
    END IF;

    SELECT ACCOUNT_ID, BALANCE, OVERDRAFT_LIMIT, ACCOUNT_STATUS 
    INTO v_acc_id, v_current_bal, v_od_limit, v_acc_status
    FROM BANK_ACCOUNTS WHERE ACCOUNT_NUMBER = p_account_number FOR UPDATE;

    IF v_acc_status <> 'Active' THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'Cannot withdraw from ' || v_acc_status || ' account.';
        RETURN;
    END IF;

    IF (v_current_bal + v_od_limit) < p_amount THEN
        RAISE e_insufficient_funds;
    END IF;

    v_current_bal := v_current_bal - p_amount;
    v_ref := 'WTH-' || TO_CHAR(SYSDATE, 'YYYYMMDD') || '-' || LPAD(SEQ_TRANSACTIONS.NEXTVAL, 6, '0');

    UPDATE BANK_ACCOUNTS SET BALANCE = v_current_bal, UPDATED_AT = SYSDATE WHERE ACCOUNT_ID = v_acc_id;

    INSERT INTO TRANSACTIONS (TRANSACTION_ID, TRANSACTION_REF, ACCOUNT_ID, TRANSACTION_TYPE, AMOUNT, BALANCE_AFTER, TRANSACTION_DATE, DESCRIPTION, TRANSACTION_STATUS)
    VALUES (SEQ_TRANSACTIONS.CURRVAL, v_ref, v_acc_id, 'Withdrawal', p_amount, v_current_bal, SYSTIMESTAMP, NVL(p_description, 'ATM / Cash Withdrawal'), 'Completed');

    COMMIT;
    p_txn_ref := v_ref;
    p_new_balance := v_current_bal;
    p_status := 'SUCCESS';
    p_message := 'Withdrawal of INR ' || TO_CHAR(p_amount, '999,999,990.00') || ' completed.';
EXCEPTION
    WHEN e_insufficient_funds THEN
        ROLLBACK;
        p_status := 'FAIL';
        p_message := 'Insufficient funds. Available: INR ' || TO_CHAR(v_current_bal + v_od_limit, '999,990.00');
    WHEN NO_DATA_FOUND THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'Account number ' || p_account_number || ' not found.';
    WHEN OTHERS THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'Withdrawal error: ' || SQLERRM;
END WITHDRAW_MONEY;
/""")
    ]

    for title, code in proc_queries:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    # =========================================================================
    # SECTION 8: AUTONOMOUS DATABASE TRIGGERS (PL/SQL)
    # =========================================================================
    story.append(Paragraph("8. AUTONOMOUS DATABASE TRIGGERS (PL/SQL)", h1_style))
    story.append(Paragraph(
        "Triggers enforce automated data auditing, minimum balance rules, and timestamp tracking in <code>11_triggers.sql</code>:", body_style
    ))

    trigger_queries = [
        ("TRG_ACCOUNTS_AUDIT (Row-Level Balance Audit with :OLD & :NEW Pseudorecords)",
"""CREATE OR REPLACE TRIGGER TRG_ACCOUNTS_AUDIT
AFTER UPDATE OF BALANCE, ACCOUNT_STATUS ON BANK_ACCOUNTS
FOR EACH ROW
DECLARE
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    INSERT INTO AUDIT_LOGS (
        LOG_ID, TABLE_NAME, OPERATION_TYPE, RECORD_ID,
        OLD_VALUE, NEW_VALUE, CHANGED_BY, CHANGED_AT, CLIENT_IP
    ) VALUES (
        SEQ_AUDIT_LOGS.NEXTVAL,
        'BANK_ACCOUNTS',
        'UPDATE',
        TO_CHAR(:OLD.ACCOUNT_ID),
        'BAL=' || :OLD.BALANCE || ', STATUS=' || :OLD.ACCOUNT_STATUS,
        'BAL=' || :NEW.BALANCE || ', STATUS=' || :NEW.ACCOUNT_STATUS,
        USER,
        SYSTIMESTAMP,
        SYS_CONTEXT('USERENV', 'IP_ADDRESS')
    );
    COMMIT; -- Autonomous commit preserves audit even if outer transaction rolls back
END TRG_ACCOUNTS_AUDIT;
/"""),

        ("TRG_VALIDATE_ACCOUNT_MIN_BAL (Pre-Insert Minimum Balance Guard)",
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
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20003, 'Invalid account type specified for account.');
END TRG_VALIDATE_ACCOUNT_MIN_BAL;
/"""),

        ("TRG_CUSTOMERS_BIU (Automated Timestamp Touch)",
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
/""")
    ]

    for title, code in trigger_queries:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    # =========================================================================
    # SECTION 9: MODULAR PL/SQL PACKAGES
    # =========================================================================
    story.append(Paragraph("9. MODULAR PL/SQL PACKAGES (SPECIFICATION & BODY)", h1_style))
    story.append(Paragraph(
        "Related procedural routines are encapsulated inside packages <code>BANKING_PACKAGE</code> (<code>12_banking_package.sql</code>) "
        "and <code>LOAN_PACKAGE</code> (<code>13_loan_package.sql</code>):", body_style
    ))

    package_code = """-- BANKING_PACKAGE Specification
CREATE OR REPLACE PACKAGE BANKING_PACKAGE AS
    TYPE t_txn_cursor IS REF CURSOR;
    PROCEDURE DEPOSIT (p_acc_no IN VARCHAR2, p_amt IN NUMBER, p_desc IN VARCHAR2, p_ref OUT VARCHAR2, p_bal OUT NUMBER, p_status OUT VARCHAR2, p_msg OUT VARCHAR2);
    PROCEDURE WITHDRAW (p_acc_no IN VARCHAR2, p_amt IN NUMBER, p_desc IN VARCHAR2, p_ref OUT VARCHAR2, p_bal OUT NUMBER, p_status OUT VARCHAR2, p_msg OUT VARCHAR2);
    PROCEDURE TRANSFER (p_src_acc IN VARCHAR2, p_dest_acc IN VARCHAR2, p_amt IN NUMBER, p_desc IN VARCHAR2, p_ref OUT VARCHAR2, p_status OUT VARCHAR2, p_msg OUT VARCHAR2);
    FUNCTION GET_BALANCE (p_acc_no IN VARCHAR2) RETURN NUMBER;
    PROCEDURE GET_STATEMENT (p_acc_no IN VARCHAR2, p_limit IN NUMBER, p_cursor OUT t_txn_cursor);
END BANKING_PACKAGE;
/

-- LOAN_PACKAGE Specification
CREATE OR REPLACE PACKAGE LOAN_PACKAGE AS
    FUNCTION CALCULATE_EMI (p_principal IN NUMBER, p_rate IN NUMBER, p_months IN NUMBER) RETURN NUMBER;
    PROCEDURE APPLY_LOAN (p_cust_id IN NUMBER, p_branch_id IN NUMBER, p_type IN VARCHAR2, p_amt IN NUMBER, p_rate IN NUMBER, p_months IN NUMBER, p_loan_id OUT NUMBER, p_loan_num OUT VARCHAR2, p_status OUT VARCHAR2, p_msg OUT VARCHAR2);
    PROCEDURE APPROVE_LOAN (p_loan_id IN NUMBER, p_disburse_acc IN VARCHAR2, p_status OUT VARCHAR2, p_msg OUT VARCHAR2);
    PROCEDURE PROCESS_PAYMENT (p_loan_id IN NUMBER, p_pay_acc IN VARCHAR2, p_amt IN NUMBER, p_ref OUT VARCHAR2, p_new_bal OUT NUMBER, p_status OUT VARCHAR2, p_msg OUT VARCHAR2);
END LOAN_PACKAGE;
/"""
    story.append(Paragraph(package_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    # =========================================================================
    # SECTION 10: CURSORS & ADVANCED PL/SQL
    # =========================================================================
    story.append(Paragraph("10. PL/SQL CURSORS & ADVANCED PL/SQL CONCEPTS", h1_style))
    story.append(Paragraph(
        "Demonstrated in <code>14_cursors_demo.sql</code> and <code>15_advanced_plsql.sql</code>, including explicit cursors, "
        "cursor FOR loops, parameterized cursors, collections, and bulk collection processing:", body_style
    ))

    cursor_code = """-- Explicit Cursor with Attributes (%FOUND, %NOTFOUND, %ROWCOUNT)
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

-- High-Performance Bulk Processing with BULK COLLECT and FORALL
DECLARE
    TYPE t_acc_ids IS TABLE OF BANK_ACCOUNTS.ACCOUNT_ID%TYPE;
    TYPE t_balances IS TABLE OF BANK_ACCOUNTS.BALANCE%TYPE;
    v_ids  t_acc_ids;
    v_bals t_balances;
BEGIN
    -- Fetch thousands of rows in a single context switch
    SELECT ACCOUNT_ID, BALANCE BULK COLLECT INTO v_ids, v_bals
    FROM BANK_ACCOUNTS WHERE ACCOUNT_STATUS = 'Active';

    -- Batch update minimizing SQL/PLSQL engine context switches
    FORALL i IN 1..v_ids.COUNT
        UPDATE BANK_ACCOUNTS SET UPDATED_AT = SYSDATE WHERE ACCOUNT_ID = v_ids(i);
    COMMIT;
END;
/"""
    story.append(Paragraph(cursor_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    # =========================================================================
    # SECTION 11: COMPLEX ANALYTICAL SQL QUERIES (JOINS, SUBQUERIES, SETS)
    # =========================================================================
    story.append(Paragraph("11. COMPLEX ANALYTICAL SQL QUERIES", h1_style))
    story.append(Paragraph(
        "Demonstrated in <code>16_sql_concepts_demonstration.sql</code> across all 6 join categories, 9 subquery forms, "
        "and set operations:", body_style
    ))

    queries_code = """-- 1. INNER JOIN (Customers with Active Accounts)
SELECT c.FIRST_NAME || ' ' || c.LAST_NAME AS HOLDER, a.ACCOUNT_NUMBER, a.BALANCE
FROM CUSTOMERS c INNER JOIN BANK_ACCOUNTS a ON c.CUSTOMER_ID = a.CUSTOMER_ID;

-- 2. LEFT OUTER JOIN (All Customers, including those without loans)
SELECT c.CUSTOMER_ID, c.FIRST_NAME || ' ' || c.LAST_NAME AS NAME, NVL(SUM(l.LOAN_AMOUNT), 0) AS TOTAL_BORROWED
FROM CUSTOMERS c LEFT OUTER JOIN LOANS l ON c.CUSTOMER_ID = l.CUSTOMER_ID GROUP BY c.CUSTOMER_ID, c.FIRST_NAME, c.LAST_NAME;

-- 3. SELF JOIN (Employees and their Direct Branch Supervisors)
SELECT e1.FIRST_NAME || ' ' || e1.LAST_NAME AS EMPLOYEE, e1.ROLE, e2.FIRST_NAME || ' ' || e2.LAST_NAME AS MANAGER
FROM EMPLOYEES e1 LEFT JOIN EMPLOYEES e2 ON e1.BRANCH_ID = e2.BRANCH_ID AND e2.ROLE = 'Assistant Manager' AND e1.EMPLOYEE_ID <> e2.EMPLOYEE_ID;

-- 4. CORRELATED SUBQUERY (Accounts holding balances above their Branch Average)
SELECT a.ACCOUNT_NUMBER, a.BALANCE, a.BRANCH_ID
FROM BANK_ACCOUNTS a WHERE a.BALANCE > (SELECT AVG(b.BALANCE) FROM BANK_ACCOUNTS b WHERE b.BRANCH_ID = a.BRANCH_ID);

-- 5. SET OPERATORS (MINUS: Accounts with deposits but zero withdrawals)
SELECT ACCOUNT_ID FROM TRANSACTIONS WHERE TRANSACTION_TYPE = 'Deposit'
MINUS
SELECT ACCOUNT_ID FROM TRANSACTIONS WHERE TRANSACTION_TYPE = 'Withdrawal';"""
    story.append(Paragraph(queries_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

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
    t_test = Table(test_rows, colWidths=[18, 105, 125, 150, 47])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_black),
        ('TEXTCOLOR', (0,0), (-1,0), c_white),
        ('GRID', (0,0), (-1,-1), 0.5, c_black),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8f8f8")]),
    ]))
    story.append(t_test)

    # Master Execution Instructions
    story.append(Paragraph("13. SQL*PLUS MASTER EXECUTION INSTRUCTIONS", h1_style))
    story.append(Paragraph(
        "All database objects can be executed sequentially using the master script <code>RUN_ALL.SQL</code> or the "
        "automated administrator batch launcher <code>run_sqlplus_admin.bat</code>:<br/>"
        "• <b>Automated Administrator Execution:</b> Right-click <code>database/run_sqlplus_admin.bat</code> → <i>Run as administrator</i>.<br/>"
        "• <b>Direct SQL*Plus Command Line:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>cd /d d:\\college\\RDBMS\\mini_project\\database</code><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>sqlplus root/root@ORCLA @RUN_ALL.SQL</code><br/>"
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
    t_wbs = Table(wbs_data, colWidths=[20, 135, 90, 200])
    t_wbs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_black),
        ('TEXTCOLOR', (0,0), (-1,0), c_white),
        ('BOX', (0,0), (-1,-1), 1, c_black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_black),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8f8f8")]),
    ]))
    story.append(t_wbs)
    story.append(Spacer(1, 4))

    story.append(Paragraph("15. REFERENCES", h1_style))
    refs = [
        "1. Oracle Corporation. <i>Oracle Database SQL Language Reference, 10g/19c/23ai</i>.",
        "2. Oracle Corporation. <i>Oracle Database PL/SQL Packages and Types Reference</i>.",
        "3. Silberschatz, A., Korth, H. F., & Sudarshan, S. <i>Database System Concepts (7th Edition)</i>. McGraw-Hill.",
        "4. Feuerstein, S., & Pribyl, B. <i>Oracle PL/SQL Programming (6th Edition)</i>. O'Reilly Media."
    ]
    for ref in refs:
        story.append(Paragraph(ref, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF successfully generated at:", pdf_path)

if __name__ == "__main__":
    build_pdf()
