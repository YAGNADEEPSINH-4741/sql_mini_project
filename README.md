# Smart Banking Management System
### Oracle SQL & Advanced PL/SQL Relational Database Project

A comprehensive, production-grade **Smart Banking Management System** designed strictly to demonstrate advanced **Oracle SQL** and **PL/SQL** database engineering concepts. The system implements multi-branch banking operations, atomic two-phase fund transfers, reducing-balance loan underwriting, automated KYC compliance, and real-time security audit trails.

---

## 👥 Academic Project Team

**Department:** Department of Computer Science & Engineering  
**Course:** Relational Database Management Systems (RDBMS)  
**Academic Year:** 2026 - 2027  

| Sr. No. | Student Full Name | Enrollment Number | Role & Contribution Area |
| :---: | :--- | :---: | :--- |
| **1** | **Vaghela Yagnadeepsinh.C** | `260203030002` | Project Architecture, Database Design (3NF) & Master Script Deployment |
| **2** | **Chudasama Krishnadeepsinh .S** | `260203030001` | PL/SQL Stored Procedures, Functions & Packages (Banking & Loan Packages) |
| **3** | **Chauhan Jaydip. P** | `260203020035` | Complex Analytical Queries, Relational Joins & Subquery Optimization |
| **4** | **Gohil Jignesh. P** | `260203020034` | Autonomous Triggers, Audit Security, Test Suite & Technical Documentation |

---

## 📌 Database Architecture Highlights

- **Database Engine:** Oracle Database 10g / 11g / 12c / 19c / 21c / 23ai with Oracle SQL*Plus.
- **Relational Normalization:** 11 normalized database tables (3NF) with declarative primary, foreign, unique, and check constraints.
- **Transactional Atomicity (ACID):** Two-phase fund transfers executed inside isolated Oracle transactions using row-level exclusive locks (`FOR UPDATE`) with automated `ROLLBACK` on error.
- **Autonomous Database Triggers:** Row-level triggers capturing audit events with `:OLD` and `:NEW` pseudorecords into `AUDIT_LOGS` using `PRAGMA AUTONOMOUS_TRANSACTION`.
- **Modular PL/SQL Packages:** Enterprise banking logic encapsulated within `BANKING_PACKAGE` and `LOAN_PACKAGE`.
- **Performance Optimizations:** B-Tree indexes on foreign keys and transaction timestamps, materialized view (`MV_BRANCH_SUMMARY`), bulk processing with `BULK COLLECT` and `FORALL`.

---

## 📂 Project Directory Structure

```text
sql_mini_project/
├── database/
│   ├── 01_schema/
│   │   ├── 01_cleanup.sql                     # Safe teardown of all schema objects
│   │   ├── 02_create_tables.sql               # 11 normalized relational tables (3NF)
│   │   ├── 03_constraints.sql                 # PK, FK, UQ, and CHECK constraints
│   │   ├── 04_sequences.sql                   # Sequences for surrogate keys
│   │   └── 05_indexes.sql                     # B-Tree performance indexes
│   ├── 02_sample_data/
│   │   └── 06_seed_data.sql                   # Comprehensive realistic seed dataset
│   ├── 03_views/
│   │   ├── 07_views.sql                       # Relational views (Customer, Txn, Loan, Branch)
│   │   └── 08_materialized_views_synonyms.sql # Materialized view (MV_BRANCH_SUMMARY) & synonyms
│   ├── 04_functions/
│   │   └── 09_functions.sql                   # User-defined functions (EMI, Balance, Interest)
│   ├── 05_procedures/
│   │   └── 10_procedures.sql                  # Stored procedures (Transfer, Deposit, Withdraw, Loan)
│   ├── 06_triggers/
│   │   └── 11_triggers.sql                    # Row & statement triggers (Audit, Validation, Timestamp)
│   ├── 07_packages/
│   │   ├── 12_banking_package.sql             # BANKING_PACKAGE spec & body
│   │   └── 13_loan_package.sql                # LOAN_PACKAGE spec & body
│   ├── 08_cursors/
│   │   └── 14_cursors_demo.sql                # Explicit, parameterized, and cursor FOR loops
│   ├── 09_advanced_plsql/
│   │   └── 15_advanced_plsql.sql              # Collections, Bulk Collect, FORALL & Dynamic SQL
│   ├── 10_queries/
│   │   └── 16_sql_concepts_demonstration.sql  # DDL, DML, DQL, 6 Joins, 9 Subqueries, Set Operators
│   ├── 11_test_scripts/
│   │   └── 17_comprehensive_test_suite.sql    # 12 automated verification test cases
│   ├── RUN_ALL.SQL                            # Master SQL*Plus deployment runner script
│   └── run_sqlplus_admin.bat                  # One-click Windows UAC elevated batch launcher
│
└── documentation/
    ├── ER_DIAGRAM.png                         # 300 DPI high-resolution relational ER diagram
    ├── generate_er_diagram.py                 # Matplotlib Python script for ER generation
    ├── generate_pdf_report.py                 # ReportLab Python script for academic PDF report
    └── SMART_BANKING_MANAGEMENT_SYSTEM_REPORT.pdf # 14-page comprehensive academic PDF report
```

---

## 🗄️ Relational Database Schema (11 Tables in 3NF)

| Table Name | Description | Primary Key | Foreign Keys | Key Constraints & Rules |
|---|---|---|---|---|
| `BANK_BRANCHES` | Bank branch locations, IFSC codes, and cities | `BRANCH_ID` | None | `UQ(BRANCH_CODE), UQ(IFSC_CODE)` |
| `CUSTOMERS` | Customer demographics and KYC status | `CUSTOMER_ID` | None | `UQ(EMAIL), UQ(PHONE), CK(GENDER), CK(KYC_STATUS)` |
| `EMPLOYEES` | Staff roster, roles, and branch assignment | `EMPLOYEE_ID` | `BRANCH_ID` | `UQ(EMAIL), CK(SALARY > 0), CK(STATUS)` |
| `ACCOUNT_TYPES` | Account catalog (Savings, Current, FD) | `TYPE_ID` | None | `UQ(TYPE_NAME), CK(MIN_BALANCE >= 0)` |
| `BANK_ACCOUNTS` | Deposit accounts and real-time balances | `ACCOUNT_ID` | `CUSTOMER_ID, BRANCH_ID, TYPE_ID` | `UQ(ACCOUNT_NUMBER), CK(BALANCE >= 0)` |
| `TRANSACTIONS` | Double-entry financial audit journal | `TRANSACTION_ID` | `ACCOUNT_ID, RELATED_ACCOUNT_ID` | `UQ(TRANSACTION_REF), CK(AMOUNT > 0)` |
| `BENEFICIARIES` | Registered counterparty recipients | `BENEFICIARY_ID` | `CUSTOMER_ID` | `CK(TRANSFER_LIMIT > 0), CK(STATUS)` |
| `LOANS` | Credit facilities and outstanding balances | `LOAN_ID` | `CUSTOMER_ID, BRANCH_ID` | `UQ(LOAN_NUMBER), CK(LOAN_AMOUNT > 0)` |
| `LOAN_PAYMENTS` | Amortized EMI installments | `PAYMENT_ID` | `LOAN_ID` | `UQ(PAYMENT_REF), CK(PAYMENT_AMOUNT > 0)` |
| `AUDIT_LOGS` | Autonomous trigger security journal | `LOG_ID` | None | `CK(OPERATION_TYPE IN ('INSERT','UPDATE','DELETE'))` |
| `ADMIN_USERS` | Privileged role-based administrator access | `ADMIN_ID` | None | `UQ(USERNAME), UQ(EMAIL), CK(ROLE)` |

---

## ⚡ SQL & PL/SQL Concept Implementation Matrix

| Concept | Implementation Target | File Location | Functional Purpose |
|---|---|---|---|
| **DDL** | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` | `02_create_tables.sql` | Defines relational schema and column constraints |
| **Constraints** | `PK`, `FK`, `UQ`, `CHECK`, `NOT NULL` | `03_constraints.sql` | Enforces referential integrity, positive balance, and KYC |
| **Sequences** | `SEQ_CUSTOMERS`, `SEQ_ACCOUNTS`, etc. | `04_sequences.sql` | Generates collision-free surrogate primary keys |
| **B-Tree Indexes** | Indexes on foreign keys and dates | `05_indexes.sql` | Accelerates transaction queries and eliminates full table scans |
| **Relational Views** | `CUSTOMER_ACCOUNT_VIEW`, etc. | `07_views.sql` | Joins 4 tables for complete customer financial profile |
| **Materialized Views** | `MV_BRANCH_SUMMARY` | `08_materialized_views_synonyms.sql` | Precomputes summary analytics for instant reporting |
| **Synonyms** | `SB_CUSTOMERS`, `SB_ACCOUNTS` | `08_materialized_views_synonyms.sql` | Provides logical object abstraction |
| **Stored Procedure** | `TRANSFER_MONEY` | `10_procedures.sql` | Atomic fund transfer with sender debit & receiver credit |
| **Stored Procedure** | `DEPOSIT_MONEY` / `WITHDRAW_MONEY` | `10_procedures.sql` | Performs validated cash operations with row-level locks |
| **Stored Procedure** | `CREATE_BANK_ACCOUNT` | `10_procedures.sql` | Enforces min balance and generates unique account # |
| **User Function** | `CALCULATE_MONTHLY_EMI` | `09_functions.sql` | Reducing-balance loan amortization calculation |
| **User Function** | `GET_ACCOUNT_BALANCE` | `09_functions.sql` | Queries live account balance by account number |
| **Package** | `BANKING_PACKAGE` | `12_banking_package.sql` | Groups banking transfers, balance inquiries, and REF CURSORs |
| **Package** | `LOAN_PACKAGE` | `13_loan_package.sql` | Groups loan underwriting, approval, and payments |
| **Explicit Cursor** | `c_high_balances` (`OPEN`, `FETCH`, `CLOSE`) | `14_cursors_demo.sql` | Iterates high-value accounts with %NOTFOUND & %ROWCOUNT |
| **Parameterized Cursor** | `c_branch_loans(branch, min_amt)` | `14_cursors_demo.sql` | Dynamic filtering of loan portfolios |
| **Cursor FOR Loop** | `c_customer_activity` | `14_cursors_demo.sql` | Automated traversal of customer transactions |
| **Trigger (Audit)** | `TRG_ACCOUNTS_AUDIT` | `11_triggers.sql` | Logs balance changes to `AUDIT_LOGS` with `:OLD` & `:NEW` |
| **Trigger (Validation)** | `TRG_VALIDATE_ACCOUNT_MIN_BAL` | `11_triggers.sql` | Prevents below-minimum balance account creations |
| **Bulk Processing** | `BULK COLLECT` & `FORALL` | `15_advanced_plsql.sql` | High-performance batch updates minimizing context switches |
| **Dynamic SQL** | `EXECUTE IMMEDIATE ... USING` | `15_advanced_plsql.sql` | Runtime dynamic query construction |
| **Exception Handling** | `e_insufficient_funds`, `ZERO_DIVIDE` | `10_procedures.sql` | Graceful error handling with transaction rollback |

---

## 🚀 Execution Instructions (Oracle SQL*Plus)

### 1. Automated Administrator Execution (Windows)
1. Navigate to the `database` folder:
   ```cmd
   cd /d d:\college\RDBMS\mini_project\database
   ```
2. Double-click or run:
   ```cmd
   run_sqlplus_admin.bat
   ```
   *(This automatically elevates privileges with `SeCreateGlobalPrivilege`, runs SQL\*Plus against `root/root@ORCLA`, executes all 17 scripts in order, and writes the log to `SMART_BANKING_DEPLOYMENT.LOG`).*

### 2. Direct SQL*Plus Command Line Execution
```cmd
cd /d d:\college\RDBMS\mini_project\database
sqlplus root/root@ORCLA @RUN_ALL.SQL
```

---

## 📄 Academic Project Report & ER Diagram

- **PDF Academic Report:** [documentation/SMART_BANKING_MANAGEMENT_SYSTEM_REPORT.pdf](documentation/SMART_BANKING_MANAGEMENT_SYSTEM_REPORT.pdf)
  - 14 dense, publication-grade pages with zero blank spaces, featuring:
    - Complete DDL queries for all 11 tables
    - ER Diagram & Relational Cardinality mapping
    - Sample DML insert queries
    - Views & Materialized View DDL
    - Full PL/SQL code for procedures (`TRANSFER_MONEY`, `DEPOSIT_MONEY`, `WITHDRAW_MONEY`)
    - Functions (`CALCULATE_MONTHLY_EMI`, `GET_ACCOUNT_BALANCE`)
    - Triggers (`TRG_ACCOUNTS_AUDIT`, `TRG_VALIDATE_ACCOUNT_MIN_BAL`)
    - Packages (`BANKING_PACKAGE`, `LOAN_PACKAGE`)
    - Cursors & Bulk Processing
    - 12-Case Test Suite with verification results
    - Project Team WBS table with all 4 students
- **Entity-Relationship Diagram:** [documentation/ER_DIAGRAM.png](documentation/ER_DIAGRAM.png)
