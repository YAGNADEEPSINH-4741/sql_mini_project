-- ============================================================================
-- SCRIPT: 04_sequences.sql
-- PROJECT: Smart Banking Management System
-- PURPOSE: Create Oracle Sequences for Surrogate Key Generation
-- ORACLE DB COMPATIBILITY: Oracle 10g, 11g, 12c, 19c, 21c, 23ai
-- ============================================================================

PROMPT ====================================================================
PROMPT   Executing 04_sequences.sql - Creating Sequences for Primary Keys
PROMPT ====================================================================

CREATE SEQUENCE SEQ_BRANCHES
    START WITH 101
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE SEQUENCE SEQ_CUSTOMERS
    START WITH 1001
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE SEQUENCE SEQ_EMPLOYEES
    START WITH 501
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE SEQUENCE SEQ_ACCOUNT_TYPES
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE SEQUENCE SEQ_ACCOUNTS
    START WITH 2001
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE SEQUENCE SEQ_TRANSACTIONS
    START WITH 100001
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE SEQUENCE SEQ_BENEFICIARIES
    START WITH 3001
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE SEQUENCE SEQ_LOANS
    START WITH 4001
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE SEQUENCE SEQ_LOAN_PAYMENTS
    START WITH 5001
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE SEQUENCE SEQ_AUDIT_LOGS
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE SEQUENCE SEQ_ADMIN_USERS
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

PROMPT [OK] All 11 sequences successfully created.
