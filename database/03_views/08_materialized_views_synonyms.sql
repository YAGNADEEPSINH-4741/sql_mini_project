-- ============================================================================
-- SCRIPT: 08_materialized_views_synonyms.sql
-- PROJECT: Smart Banking Management System
-- PURPOSE: Create Materialized Views and Synonyms for Database Abstraction
-- ORACLE DB COMPATIBILITY: Oracle 10g, 11g, 12c, 19c, 21c, 23ai
-- ============================================================================

PROMPT ====================================================================
PROMPT   Executing 08_materialized_views_synonyms.sql
PROMPT ====================================================================

-- 1. MATERIALIZED VIEW: MV_BRANCH_SUMMARY
-- Precomputed summary for heavy reporting queries (refreshes on demand)
CREATE MATERIALIZED VIEW MV_BRANCH_SUMMARY
BUILD IMMEDIATE
REFRESH COMPLETE ON DEMAND
AS
SELECT 
    b.BRANCH_ID,
    b.BRANCH_NAME,
    b.CITY,
    COUNT(a.ACCOUNT_ID) AS TOTAL_ACCOUNTS,
    NVL(SUM(a.BALANCE), 0) AS TOTAL_DEPOSIT_VOLUME,
    ROUND(NVL(AVG(a.BALANCE), 0), 2) AS AVERAGE_BALANCE
FROM BANK_BRANCHES b
LEFT JOIN BANK_ACCOUNTS a ON b.BRANCH_ID = a.BRANCH_ID
GROUP BY b.BRANCH_ID, b.BRANCH_NAME, b.CITY;

-- 2. PRIVATE SYNONYMS FOR LOGICAL NAMING & ABSTRACTION
CREATE OR REPLACE SYNONYM SB_CUSTOMERS FOR CUSTOMERS;
CREATE OR REPLACE SYNONYM SB_ACCOUNTS FOR BANK_ACCOUNTS;
CREATE OR REPLACE SYNONYM SB_TRANSACTIONS FOR TRANSACTIONS;

PROMPT [OK] Materialized view and synonyms successfully created.
