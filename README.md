# Smart Banking Management System
### Oracle SQL & PL/SQL College Mini Project

A comprehensive, fully functional **Smart Banking Management System** designed to demonstrate advanced **Oracle SQL** and **PL/SQL** architectural concepts. The system implements multi-branch operations, atomic two-phase fund transfers, reducing-balance loan underwriting, automated KYC compliance, and real-time security audit trails.

---

## 📌 Architecture Highlights

- **Database Engine:** Oracle Database 10g / 11g / 19c / 23ai with SQL*Plus.
- **Data Normalization:** 11 normalized relational tables (3NF) with complete declarative integrity constraints.
- **Atomicity & Concurrency:** Two-phase money transfers executing inside isolated Oracle transactions using row-level locks (`FOR UPDATE`) with automatic `ROLLBACK` on failure.
- **Database Automation:** Autonomous row-level and statement-level triggers capturing audit events to `AUDIT_LOGS`.
- **Modular Packaging:** Enterprise logic encapsulated in `BANKING_PACKAGE` and `LOAN_PACKAGE`.
- **Full-Stack Interface:** Web application built with PHP (OCI8 extension), modern Fintech CSS, Bootstrap 5, and Chart.js 4.x.

---

## 📂 Project Directory Structure

```text
sql_mini_project/
├── database/
│   ├── 01_schema/
│   │   ├── 01_cleanup.sql                  # Safe drop script
│   │   ├── 02_create_tables.sql            # 11 normalized relational tables
│   │   ├── 03_constraints.sql              # PK, FK, UQ, and CHECK constraints
│   │   ├── 04_sequences.sql                # Sequences for surrogate keys
│   │   └── 05_indexes.sql                  # B-Tree performance indexes
│   ├── 02_sample_data/
│   │   └── 06_seed_data.sql                # Realistic seed data
│   ├── 03_views/
│   │   ├── 07_views.sql                    # Relational views
│   │   └── 08_materialized_views_synonyms.sql # Materialized view & synonyms
│   ├── 04_functions/
│   │   └── 09_functions.sql                # User-defined functions
│   ├── 05_procedures/
│   │   └── 10_procedures.sql               # Stored procedures
│   ├── 06_triggers/
│   │   └── 11_triggers.sql                 # Row & statement triggers
│   ├── 07_packages/
│   │   ├── 12_banking_package.sql          # BANKING_PACKAGE spec & body
│   │   └── 13_loan_package.sql             # LOAN_PACKAGE spec & body
│   ├── 08_cursors/
│   │   └── 14_cursors_demo.sql             # Cursor demonstrations
│   ├── 09_advanced_plsql/
│   │   └── 15_advanced_plsql.sql           # Collections, Bulk Collect & Dynamic SQL
│   ├── 10_queries/
│   │   └── 16_sql_concepts_demonstration.sql # DDL, DML, DQL, Joins & Subqueries
│   ├── 11_test_scripts/
│   │   └── 17_comprehensive_test_suite.sql # 12 mandatory test cases
│   ├── RUN_ALL.SQL                         # Master SQL*Plus deployment script
│   └── run_sqlplus_admin.bat               # Windows Administrator launcher
│
├── backend/
│   ├── config/
│   │   ├── database.php                    # Oracle OCI8 connection wrapper
│   │   └── oracle_bridge.php               # Data abstraction bridge
│   ├── includes/
│   │   ├── auth.php                        # Session & RBAC security
│   │   └── response.php                    # JSON response helpers
│   └── api.php                             # Unified backend API router
│
├── frontend/
│   ├── assets/
│   │   ├── css/style.css                   # Custom Fintech design system
│   │   └── js/
│   │       ├── app.js                      # Toast, modal, and table handlers
│   │       └── charts.js                   # Chart.js analytics engine
│   ├── pages/
│   │   ├── login.php                       # Secure administrator portal
│   │   ├── dashboard.php                   # Executive financial dashboard
│   │   ├── customers.php                   # Customer management
│   │   ├── accounts.php                    # Bank account provisioning
│   │   ├── transactions.php                # Deposit, withdrawal & transfer
│   │   ├── beneficiaries.php               # Beneficiary registry
│   │   ├── loans.php                       # Credit underwriting & EMI calculator
│   │   ├── reports.php                     # Analytical views & CSV export
│   │   └── audit_logs.php                  # Database trigger audit ledger
│   └── index.php                           # Application gateway
│
├── documentation/
│   ├── SMART_BANKING_MANAGEMENT_SYSTEM_REPORT.pdf # 25-section academic report
│   ├── ER_DIAGRAM.png                      # High-resolution 300 DPI ER diagram
│   └── screenshots/                        # Real application screenshots
│
├── .env.example                            # Configuration environment template
├── .gitignore                              # Git exclusion rules
└── README.md                               # Project documentation
```

---

## 🗄️ Database Tables Overview

| Table Name | Description | Primary Key | Foreign Keys | Key Constraints |
|---|---|---|---|---|
| `BANK_BRANCHES` | Physical branch offices and IFSC codes | `BRANCH_ID` | None | `UQ(BRANCH_CODE, IFSC_CODE)` |
| `CUSTOMERS` | Customer demographics and KYC status | `CUSTOMER_ID` | None | `UQ(EMAIL, PHONE), CK(KYC_STATUS)` |
| `EMPLOYEES` | Branch workforce and role assignments | `EMPLOYEE_ID` | `BRANCH_ID` | `UQ(EMAIL), CK(SALARY > 0)` |
| `ACCOUNT_TYPES` | Product categories (Savings, Current, FD) | `TYPE_ID` | None | `UQ(TYPE_NAME), CK(MIN_BALANCE)` |
| `BANK_ACCOUNTS` | Deposit accounts and live balances | `ACCOUNT_ID` | `CUSTOMER_ID, BRANCH_ID, TYPE_ID` | `UQ(ACCOUNT_NUMBER), CK(BALANCE >= 0)` |
| `TRANSACTIONS` | Double-entry financial audit journal | `TRANSACTION_ID` | `ACCOUNT_ID, RELATED_ACCOUNT_ID` | `UQ(TRANSACTION_REF), CK(AMOUNT > 0)` |
| `BENEFICIARIES` | Registered counterparty recipients | `BENEFICIARY_ID` | `CUSTOMER_ID` | `CK(TRANSFER_LIMIT > 0)` |
| `LOANS` | Credit facilities and outstanding balances | `LOAN_ID` | `CUSTOMER_ID, BRANCH_ID` | `UQ(LOAN_NUMBER), CK(LOAN_AMOUNT > 0)` |
| `LOAN_PAYMENTS` | Amortized EMI installments | `PAYMENT_ID` | `LOAN_ID` | `UQ(PAYMENT_REF), CK(AMOUNT > 0)` |
| `AUDIT_LOGS` | Autonomous trigger security journal | `LOG_ID` | None | `CK(OPERATION_TYPE)` |
| `ADMIN_USERS` | Privileged role-based administrator access | `ADMIN_ID` | None | `UQ(USERNAME, EMAIL)` |

---

## ⚡ SQL & PL/SQL Concept Mapping

| Concept | Implementation Target | File Location | Functional Purpose |
|---|---|---|---|
| **DDL** | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` | `02_create_tables.sql` | Defines relational schema and column constraints |
| **Constraints** | `PK`, `FK`, `UQ`, `CHECK`, `NOT NULL` | `03_constraints.sql` | Enforces referential integrity and valid amounts |
| **Sequences** | `SEQ_CUSTOMERS`, `SEQ_ACCOUNTS` | `04_sequences.sql` | Generates unique numeric identifiers |
| **B-Tree Indexes** | Indexes on foreign keys and dates | `05_indexes.sql` | Accelerates transaction queries |
| **Relational Views** | `CUSTOMER_ACCOUNT_VIEW` | `07_views.sql` | Multi-table join for complete customer profile |
| **Materialized Views** | `MV_BRANCH_SUMMARY` | `08_materialized_views_synonyms.sql` | Precomputes summary analytics for reporting |
| **Synonyms** | `SB_CUSTOMERS`, `SB_ACCOUNTS` | `08_materialized_views_synonyms.sql` | Provides logical object abstraction |
| **Stored Procedure** | `TRANSFER_MONEY` | `10_procedures.sql` | Atomic fund transfer with sender debit & credit |
| **Stored Procedure** | `DEPOSIT_MONEY` / `WITHDRAW_MONEY` | `10_procedures.sql` | Performs validated cash operations with row locks |
| **Stored Procedure** | `CREATE_BANK_ACCOUNT` | `10_procedures.sql` | Enforces min balance and generates account # |
| **User Function** | `CALCULATE_MONTHLY_EMI` | `09_functions.sql` | Reducing balance loan amortization calculation |
| **User Function** | `GET_ACCOUNT_BALANCE` | `09_functions.sql` | Look up live account balance |
| **Package** | `BANKING_PACKAGE` | `12_banking_package.sql` | Groups banking transfers and REF CURSORs |
| **Package** | `LOAN_PACKAGE` | `13_loan_package.sql` | Groups loan underwriting, approval and payments |
| **Explicit Cursor** | `c_high_balances` (`OPEN`, `FETCH`, `CLOSE`) | `14_cursors_demo.sql` | Iterates through high-value accounts |
| **Parameterized Cursor** | `c_branch_loans(branch, min_amt)` | `14_cursors_demo.sql` | Dynamic filtering of loan portfolios |
| **Cursor FOR Loop** | `c_customer_activity` | `14_cursors_demo.sql` | Automated traversal of customer transactions |
| **Trigger (Audit)** | `TRG_ACCOUNTS_AUDIT` | `11_triggers.sql` | Logs balance changes to `AUDIT_LOGS` |
| **Trigger (Validation)** | `TRG_VALIDATE_ACCOUNT_MIN_BAL` | `11_triggers.sql` | Prevents below-minimum balance accounts |
| **Bulk Processing** | `BULK COLLECT` & `FORALL` | `15_advanced_plsql.sql` | High-performance batch updates |
| **Dynamic SQL** | `EXECUTE IMMEDIATE ... USING` | `15_advanced_plsql.sql` | Runtime dynamic query construction |
| **Exception Handling** | `e_insufficient_funds`, `ZERO_DIVIDE` | `10_procedures.sql` | Graceful error handling with transaction rollback |

---

## 🚀 Setup & Execution Instructions

### 1. Database Deployment (Oracle SQL*Plus)

1. Open Command Prompt as **Administrator** (required by Oracle on Windows).
2. Navigate to the `database` folder:
   ```bash
   cd d:\college\RDBMS\mini_project\database
   ```
3. Execute the automated master script:
   ```bash
   run_sqlplus_admin.bat
   ```
   Or directly in SQL*Plus:
   ```sql
   sqlplus root/root@ORCLA @RUN_ALL.SQL
   ```
4. All 11 tables, constraints, sequences, procedures, packages, triggers, demonstration queries, and test cases will execute sequentially. An execution log is spooled to `SMART_BANKING_DEPLOYMENT.LOG`.

---

### 2. Web Application Deployment (PHP / Apache)

1. Ensure **XAMPP Apache** is running with PHP 8.x.
2. In `C:\xampp\php\php.ini`, ensure `extension=oci8_19` or `extension=oci8` is enabled.
3. Start the PHP server or point XAMPP document root to this folder:
   ```bash
   php -S 127.0.0.1:8088 -t d:\college\RDBMS\mini_project
   ```
4. Open your browser and navigate to:
   ```text
   http://127.0.0.1:8088/frontend/pages/login.php
   ```

---

## 🔑 Demo Administrator Credentials

- **Username:** `admin`
- **Password:** `admin123`
- **Role:** Super Admin / Bank Manager
