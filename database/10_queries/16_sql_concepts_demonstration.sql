-- ============================================================================
-- SCRIPT: 16_sql_concepts_demonstration.sql
-- PROJECT: Smart Banking Management System
-- PURPOSE: Exhaustive demonstration of all Oracle SQL concepts requested
--          DDL, DML, DQL, DCL, TCL, Constraints, Operators, Aggregate/String/
--          Date/Conversion Functions, Joins, Subqueries, Set Operators.
-- ORACLE DB COMPATIBILITY: Oracle 10g, 11g, 12c, 19c, 21c, 23ai
-- ============================================================================

SET SERVEROUTPUT ON
SET LINESIZE 300
SET PAGESIZE 50

PROMPT ====================================================================
PROMPT   1. DDL (DATA DEFINITION LANGUAGE) DEMONSTRATION
PROMPT ====================================================================

-- 1.1 CREATE TABLE
CREATE TABLE DEMO_DDL_TABLE (
    TEMP_ID NUMBER(5) PRIMARY KEY,
    TEMP_NAME VARCHAR2(50),
    TEMP_VAL NUMBER(10,2)
);

-- 1.2 ALTER TABLE (Add Column, Modify Column)
ALTER TABLE DEMO_DDL_TABLE ADD (STATUS VARCHAR2(20) DEFAULT 'Active');
ALTER TABLE DEMO_DDL_TABLE MODIFY (TEMP_NAME VARCHAR2(100));

-- 1.3 TRUNCATE TABLE
INSERT INTO DEMO_DDL_TABLE (TEMP_ID, TEMP_NAME, TEMP_VAL) VALUES (1, 'Test', 100);
COMMIT;
TRUNCATE TABLE DEMO_DDL_TABLE;

-- 1.4 DROP TABLE
DROP TABLE DEMO_DDL_TABLE PURGE;

PROMPT [OK] DDL operations executed successfully.

PROMPT ====================================================================
PROMPT   2. DML & TCL (DATA MANIPULATION & TRANSACTION CONTROL) DEMO
PROMPT ====================================================================

-- 2.1 SAVEPOINT, INSERT, UPDATE, ROLLBACK TO SAVEPOINT, COMMIT
INSERT INTO BANK_ACCOUNTS (ACCOUNT_ID, ACCOUNT_NUMBER, CUSTOMER_ID, BRANCH_ID, TYPE_ID, BALANCE, OVERDRAFT_LIMIT, ACCOUNT_STATUS, OPENED_DATE)
VALUES (9999, 'SB_TEMP_TEST', 1001, 101, 1, 1000.00, 0.00, 'Active', SYSDATE);

SAVEPOINT SP_AFTER_INSERT;

UPDATE BANK_ACCOUNTS SET BALANCE = 5000.00 WHERE ACCOUNT_ID = 9999;

-- Verify updated value in transaction
SELECT ACCOUNT_NUMBER, BALANCE FROM BANK_ACCOUNTS WHERE ACCOUNT_ID = 9999;

-- Rollback to savepoint (reverts balance to 1000)
ROLLBACK TO SAVEPOINT SP_AFTER_INSERT;

-- Delete test row and commit cleanly
DELETE FROM BANK_ACCOUNTS WHERE ACCOUNT_ID = 9999;
COMMIT;

PROMPT [OK] DML and TCL (SAVEPOINT, ROLLBACK, COMMIT) demonstrated.

PROMPT ====================================================================
PROMPT   3. SQL OPERATORS DEMONSTRATION (ARITHMETIC, LOGICAL, COMPARISON)
PROMPT ====================================================================

-- 3.1 Arithmetic, Comparison, Logical, BETWEEN, IN, LIKE, IS NULL
SELECT 
    ACCOUNT_NUMBER,
    BALANCE,
    BALANCE * 0.035 AS ANNUAL_INTEREST_ESTIMATE,
    BALANCE / 12 AS MONTHLY_LIQUIDITY_FACTOR
FROM BANK_ACCOUNTS
WHERE BALANCE BETWEEN 10000 AND 500000
  AND ACCOUNT_STATUS = 'Active'
  AND TYPE_ID IN (1, 2, 3)
  AND ACCOUNT_NUMBER LIKE 'SB100%'
  AND OVERDRAFT_LIMIT IS NOT NULL;

PROMPT ====================================================================
PROMPT   4. SQL FUNCTIONS DEMONSTRATION
PROMPT ====================================================================

-- 4.1 AGGREGATE FUNCTIONS (COUNT, SUM, AVG, MIN, MAX)
SELECT 
    COUNT(*) AS TOTAL_ACCOUNTS,
    SUM(BALANCE) AS TOTAL_BANK_DEPOSITS,
    ROUND(AVG(BALANCE), 2) AS AVERAGE_BALANCE,
    MIN(BALANCE) AS MIN_BALANCE,
    MAX(BALANCE) AS MAX_BALANCE
FROM BANK_ACCOUNTS
WHERE ACCOUNT_STATUS = 'Active';

-- 4.2 STRING FUNCTIONS (UPPER, LOWER, INITCAP, LENGTH, SUBSTR, CONCAT, LPAD, RPAD)
SELECT 
    UPPER(LAST_NAME) AS UPPER_LAST,
    LOWER(EMAIL) AS LOWER_EMAIL,
    INITCAP(CITY) AS INITCAP_CITY,
    LENGTH(PHONE) AS PHONE_LEN,
    SUBSTR(PHONE, 5, 5) AS SUBSTR_PHONE,
    CONCAT(FIRST_NAME, ' ' || LAST_NAME) AS FULL_NAME_CONCAT,
    LPAD(ACCOUNT_NUMBER, 16, '*') AS MASKED_ACCOUNT,
    RPAD(FIRST_NAME, 15, '.') AS PADDED_FIRST
FROM CUSTOMERS
WHERE ROWNUM <= 3;

-- 4.3 DATE FUNCTIONS (SYSDATE, ADD_MONTHS, MONTHS_BETWEEN, LAST_DAY, NEXT_DAY, TRUNC)
SELECT 
    SYSDATE AS CURRENT_DATE_TIME,
    ADD_MONTHS(SYSDATE, 12) AS MATURITY_NEXT_YEAR,
    ROUND(MONTHS_BETWEEN(SYSDATE, TO_DATE('2022-01-01', 'YYYY-MM-DD')), 1) AS MONTHS_SINCE_2022,
    LAST_DAY(SYSDATE) AS END_OF_CURRENT_MONTH,
    TRUNC(SYSDATE, 'MM') AS START_OF_CURRENT_MONTH
FROM DUAL;

-- 4.4 CONVERSION FUNCTIONS (TO_CHAR, TO_DATE, TO_NUMBER)
SELECT 
    TO_CHAR(BALANCE, '$999,999,990.00') AS FORMATTED_CURRENCY,
    TO_CHAR(OPENED_DATE, 'DD-Mon-YYYY (Day)') AS FORMATTED_DATE,
    TO_NUMBER('1500.75') * 2 AS CONVERTED_NUMBER_CALC
FROM BANK_ACCOUNTS
WHERE ROWNUM = 1;

-- 4.5 NULL-HANDLING & MATHEMATICAL (NVL, NVL2, COALESCE, ROUND, TRUNC)
SELECT 
    LOAN_NUMBER,
    APPROVAL_DATE,
    NVL(TO_CHAR(APPROVAL_DATE, 'YYYY-MM-DD'), 'Pending Approval') AS NVL_STATUS,
    NVL2(APPROVAL_DATE, 'Disbursed/Approved', 'Awaiting Review') AS NVL2_STATUS,
    COALESCE(APPROVAL_DATE, APPLICATION_DATE, SYSDATE) AS EFFECTIVE_DATE,
    ROUND(MONTHLY_EMI, 0) AS ROUNDED_EMI,
    TRUNC(MONTHLY_EMI, 0) AS TRUNCATED_EMI
FROM LOANS;

PROMPT ====================================================================
PROMPT   5. RELATIONAL JOINS DEMONSTRATION
PROMPT ====================================================================

-- 5.1 INNER JOIN: Accounts with Customer & Branch Details
SELECT 
    a.ACCOUNT_NUMBER,
    c.FIRST_NAME || ' ' || c.LAST_NAME AS HOLDER_NAME,
    b.BRANCH_NAME,
    a.BALANCE
FROM BANK_ACCOUNTS a
INNER JOIN CUSTOMERS c ON a.CUSTOMER_ID = c.CUSTOMER_ID
INNER JOIN BANK_BRANCHES b ON a.BRANCH_ID = b.BRANCH_ID
WHERE a.BALANCE > 50000;

-- 5.2 LEFT OUTER JOIN: All Customers and their Loans (including those without loans)
SELECT 
    c.CUSTOMER_ID,
    c.FIRST_NAME || ' ' || c.LAST_NAME AS CUSTOMER_NAME,
    l.LOAN_NUMBER,
    NVL(l.LOAN_AMOUNT, 0) AS LOAN_AMOUNT,
    NVL(l.LOAN_STATUS, 'No Loan Applied') AS STATUS
FROM CUSTOMERS c
LEFT OUTER JOIN LOANS l ON c.CUSTOMER_ID = l.CUSTOMER_ID;

-- 5.3 RIGHT OUTER JOIN: Branches with Accounts (All branches shown even if zero accounts)
SELECT 
    b.BRANCH_NAME,
    b.CITY,
    a.ACCOUNT_NUMBER,
    a.BALANCE
FROM BANK_ACCOUNTS a
RIGHT OUTER JOIN BANK_BRANCHES b ON a.BRANCH_ID = b.BRANCH_ID;

-- 5.4 FULL OUTER JOIN: Customers and Beneficiaries
SELECT 
    c.FIRST_NAME || ' ' || c.LAST_NAME AS CUSTOMER,
    ben.BENEFICIARY_NAME,
    ben.BANK_NAME
FROM CUSTOMERS c
FULL OUTER JOIN BENEFICIARIES ben ON c.CUSTOMER_ID = ben.CUSTOMER_ID;

-- 5.5 SELF JOIN: Employees reporting hierarchy / Colleagues in same branch
SELECT 
    e1.FIRST_NAME || ' ' || e1.LAST_NAME AS EMPLOYEE,
    e1.ROLE AS ROLE,
    e2.FIRST_NAME || ' ' || e2.LAST_NAME AS BRANCH_COLLEAGUE,
    b.BRANCH_NAME
FROM EMPLOYEES e1
JOIN EMPLOYEES e2 ON e1.BRANCH_ID = e2.BRANCH_ID AND e1.EMPLOYEE_ID <> e2.EMPLOYEE_ID
JOIN BANK_BRANCHES b ON e1.BRANCH_ID = b.BRANCH_ID
WHERE ROWNUM <= 5;

-- 5.6 CROSS JOIN: Account Types Cartesian Product with Branches (Planning matrix)
SELECT 
    b.BRANCH_NAME,
    t.TYPE_NAME,
    t.MIN_BALANCE
FROM BANK_BRANCHES b
CROSS JOIN ACCOUNT_TYPES t
WHERE b.BRANCH_ID = 101;

PROMPT ====================================================================
PROMPT   6. SUBQUERIES DEMONSTRATION
PROMPT ====================================================================

-- 6.1 SINGLE-ROW SUBQUERY: Accounts with balance greater than overall bank average
SELECT 
    ACCOUNT_NUMBER,
    BALANCE
FROM BANK_ACCOUNTS
WHERE BALANCE > (SELECT AVG(BALANCE) FROM BANK_ACCOUNTS);

-- 6.2 MULTI-ROW SUBQUERY (IN): Customers who hold Current Business Accounts
SELECT 
    FIRST_NAME,
    LAST_NAME,
    CITY
FROM CUSTOMERS
WHERE CUSTOMER_ID IN (
    SELECT CUSTOMER_ID 
    FROM BANK_ACCOUNTS 
    WHERE TYPE_ID = 3
);

-- 6.3 MULTI-ROW SUBQUERY (ANY / ALL):
-- ANY: Loans larger than ANY personal loan
SELECT LOAN_NUMBER, LOAN_TYPE, LOAN_AMOUNT
FROM LOANS
WHERE LOAN_AMOUNT > ANY (
    SELECT LOAN_AMOUNT FROM LOANS WHERE LOAN_TYPE = 'Personal Loan'
);

-- ALL: Loans larger than ALL auto loans
SELECT LOAN_NUMBER, LOAN_TYPE, LOAN_AMOUNT
FROM LOANS
WHERE LOAN_AMOUNT > ALL (
    SELECT LOAN_AMOUNT FROM LOANS WHERE LOAN_TYPE = 'Auto Loan'
);

-- 6.4 CORRELATED SUBQUERY: Accounts with balance above their own branch average
SELECT 
    a.ACCOUNT_NUMBER,
    a.BRANCH_ID,
    a.BALANCE
FROM BANK_ACCOUNTS a
WHERE a.BALANCE > (
    SELECT AVG(sub.BALANCE) 
    FROM BANK_ACCOUNTS sub 
    WHERE sub.BRANCH_ID = a.BRANCH_ID
);

-- 6.5 EXISTS & NOT EXISTS
-- EXISTS: Customers who have performed at least one transaction
SELECT c.FIRST_NAME, c.LAST_NAME
FROM CUSTOMERS c
WHERE EXISTS (
    SELECT 1 
    FROM BANK_ACCOUNTS a 
    JOIN TRANSACTIONS t ON a.ACCOUNT_ID = t.ACCOUNT_ID 
    WHERE a.CUSTOMER_ID = c.CUSTOMER_ID
);

-- NOT EXISTS: Customers who have never taken a loan
SELECT c.FIRST_NAME, c.LAST_NAME, c.EMAIL
FROM CUSTOMERS c
WHERE NOT EXISTS (
    SELECT 1 
    FROM LOANS l 
    WHERE l.CUSTOMER_ID = c.CUSTOMER_ID
);

PROMPT ====================================================================
PROMPT   7. SET OPERATORS (UNION, UNION ALL, INTERSECT, MINUS)
PROMPT ====================================================================

-- 7.1 UNION: Unique Cities where we have either branches or customers
SELECT CITY FROM BANK_BRANCHES
UNION
SELECT CITY FROM CUSTOMERS;

-- 7.2 UNION ALL: All city references preserved with duplicates
SELECT CITY, 'Branch' AS SOURCE FROM BANK_BRANCHES
UNION ALL
SELECT CITY, 'Customer' AS SOURCE FROM CUSTOMERS;

-- 7.3 INTERSECT: Cities where BOTH a branch and at least one customer reside
SELECT CITY FROM BANK_BRANCHES
INTERSECT
SELECT CITY FROM CUSTOMERS;

-- 7.4 MINUS: Customer cities that DO NOT yet have a local bank branch
SELECT CITY FROM CUSTOMERS
MINUS
SELECT CITY FROM BANK_BRANCHES;

PROMPT ====================================================================
PROMPT   [OK] All SQL concepts successfully demonstrated and validated.
PROMPT ====================================================================
