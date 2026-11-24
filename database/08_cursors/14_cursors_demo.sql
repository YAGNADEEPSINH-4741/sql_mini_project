-- ============================================================================
-- SCRIPT: 14_cursors_demo.sql
-- PROJECT: Smart Banking Management System
-- PURPOSE: Exhaustive demonstration of Oracle Cursors:
--          1. Implicit Cursor (SQL%FOUND, SQL%NOTFOUND, SQL%ROWCOUNT)
--          2. Explicit Cursor (OPEN, FETCH, CLOSE, %FOUND, %NOTFOUND, %ROWCOUNT, %ISOPEN)
--          3. Parameterized Cursor
--          4. Cursor FOR LOOP
--          5. Practical Banking Procedures with Cursors
-- ORACLE DB COMPATIBILITY: Oracle 10g, 11g, 12c, 19c, 21c, 23ai
-- ============================================================================

SET SERVEROUTPUT ON
SET LINESIZE 300

PROMPT ====================================================================
PROMPT   Executing 14_cursors_demo.sql - Cursors Demonstration
PROMPT ====================================================================

-- 1. IMPLICIT CURSOR DEMONSTRATION (SQL%ROWCOUNT, SQL%FOUND, SQL%NOTFOUND)
PROMPT --------------------------------------------------------------------
PROMPT 1. Implicit Cursor Demo: Bulk Interest Increment Evaluation
PROMPT --------------------------------------------------------------------
DECLARE
    v_rows_affected NUMBER;
BEGIN
    -- Implicit cursor created automatically for this DML
    UPDATE BANK_ACCOUNTS
    SET BALANCE = BALANCE + 0
    WHERE ACCOUNT_STATUS = 'Active' AND BALANCE >= 100000;

    IF SQL%FOUND THEN
        v_rows_affected := SQL%ROWCOUNT;
        DBMS_OUTPUT.PUT_LINE('Implicit Cursor: Active high-value accounts found: ' || v_rows_affected);
    ELSE
        DBMS_OUTPUT.PUT_LINE('Implicit Cursor: No matching accounts found (SQL%NOTFOUND = TRUE).');
    END IF;
    
    COMMIT;
END;
/

-- 2. EXPLICIT CURSOR WITH MANUAL ATTRIBUTES (OPEN, FETCH, %NOTFOUND, %ROWCOUNT, CLOSE, %ISOPEN)
PROMPT --------------------------------------------------------------------
PROMPT 2. Explicit Cursor Demo: Inspecting Accounts Above Specified Balance
PROMPT --------------------------------------------------------------------
DECLARE
    -- Explicit Cursor Declaration
    CURSOR c_high_balances IS
        SELECT a.ACCOUNT_NUMBER, c.FIRST_NAME || ' ' || c.LAST_NAME AS HOLDER_NAME, a.BALANCE, b.BRANCH_NAME
        FROM BANK_ACCOUNTS a
        JOIN CUSTOMERS c ON a.CUSTOMER_ID = c.CUSTOMER_ID
        JOIN BANK_BRANCHES b ON a.BRANCH_ID = b.BRANCH_ID
        WHERE a.BALANCE >= 50000.00
        ORDER BY a.BALANCE DESC;

    v_acc_no    BANK_ACCOUNTS.ACCOUNT_NUMBER%TYPE;
    v_holder    VARCHAR2(100);
    v_bal       BANK_ACCOUNTS.BALANCE%TYPE;
    v_branch    BANK_BRANCHES.BRANCH_NAME%TYPE;
BEGIN
    -- Check %ISOPEN before opening
    IF NOT c_high_balances%ISOPEN THEN
        OPEN c_high_balances;
        DBMS_OUTPUT.PUT_LINE('Explicit cursor c_high_balances successfully OPENED.');
    END IF;

    DBMS_OUTPUT.PUT_LINE(RPAD('ACC NUMBER', 16) || RPAD('HOLDER', 25) || RPAD('BRANCH', 30) || 'BALANCE');
    DBMS_OUTPUT.PUT_LINE('--------------------------------------------------------------------------------');

    LOOP
        FETCH c_high_balances INTO v_acc_no, v_holder, v_bal, v_branch;
        EXIT WHEN c_high_balances%NOTFOUND;

        DBMS_OUTPUT.PUT_LINE(
            RPAD(v_acc_no, 16) ||
            RPAD(v_holder, 25) ||
            RPAD(v_branch, 30) ||
            'INR ' || TO_CHAR(v_bal, '999,999,990.00')
        );
    END LOOP;

    DBMS_OUTPUT.PUT_LINE('--------------------------------------------------------------------------------');
    DBMS_OUTPUT.PUT_LINE('Explicit Cursor %ROWCOUNT: Total qualifying accounts = ' || c_high_balances%ROWCOUNT);

    CLOSE c_high_balances;
    IF NOT c_high_balances%ISOPEN THEN
        DBMS_OUTPUT.PUT_LINE('Explicit cursor successfully CLOSED.');
    END IF;
END;
/

-- 3. PARAMETERIZED CURSOR DEMONSTRATION
PROMPT --------------------------------------------------------------------
PROMPT 3. Parameterized Cursor Demo: Querying Loans by Branch and Minimum Amount
PROMPT --------------------------------------------------------------------
DECLARE
    -- Parameterized Cursor with default branch parameter
    CURSOR c_branch_loans (p_branch_id NUMBER, p_min_loan NUMBER) IS
        SELECT l.LOAN_NUMBER, c.FIRST_NAME || ' ' || c.LAST_NAME AS BORROWER, l.LOAN_TYPE, l.LOAN_AMOUNT, l.OUTSTANDING_BALANCE
        FROM LOANS l
        JOIN CUSTOMERS c ON l.CUSTOMER_ID = c.CUSTOMER_ID
        WHERE l.BRANCH_ID = p_branch_id
          AND l.LOAN_AMOUNT >= p_min_loan;

    v_loan_rec c_branch_loans%ROWTYPE;
BEGIN
    DBMS_OUTPUT.PUT_LINE('Querying Loans for Branch 101 with Min Amount INR 1,000,000:');
    DBMS_OUTPUT.PUT_LINE('------------------------------------------------------------------------');

    OPEN c_branch_loans(101, 1000000);
    LOOP
        FETCH c_branch_loans INTO v_loan_rec;
        EXIT WHEN c_branch_loans%NOTFOUND;

        DBMS_OUTPUT.PUT_LINE(
            'Loan #' || v_loan_rec.LOAN_NUMBER || ' | ' ||
            RPAD(v_loan_rec.BORROWER, 20) || ' | ' ||
            RPAD(v_loan_rec.LOAN_TYPE, 15) || ' | Sanctioned: INR ' ||
            TO_CHAR(v_loan_rec.LOAN_AMOUNT, '99,99,990.00')
        );
    END LOOP;
    CLOSE c_branch_loans;
END;
/

-- 4. CURSOR FOR LOOP DEMONSTRATION (Automatic OPEN, FETCH, EXIT WHEN NOTFOUND, and CLOSE)
PROMPT --------------------------------------------------------------------
PROMPT 4. Cursor FOR LOOP Demo: Customer Transaction Activity Digest
PROMPT --------------------------------------------------------------------
DECLARE
    CURSOR c_customer_activity IS
        SELECT c.CUSTOMER_ID, c.FIRST_NAME || ' ' || c.LAST_NAME AS FULL_NAME,
               COUNT(t.TRANSACTION_ID) AS TOTAL_TXNS,
               NVL(SUM(CASE WHEN t.TRANSACTION_TYPE LIKE '%Deposit%' OR t.TRANSACTION_TYPE LIKE '%Credit%' THEN t.AMOUNT ELSE 0 END), 0) AS TOTAL_INFLOW,
               NVL(SUM(CASE WHEN t.TRANSACTION_TYPE LIKE '%Withdraw%' OR t.TRANSACTION_TYPE LIKE '%Debit%' THEN t.AMOUNT ELSE 0 END), 0) AS TOTAL_OUTFLOW
        FROM CUSTOMERS c
        JOIN BANK_ACCOUNTS a ON c.CUSTOMER_ID = a.CUSTOMER_ID
        LEFT JOIN TRANSACTIONS t ON a.ACCOUNT_ID = t.ACCOUNT_ID
        GROUP BY c.CUSTOMER_ID, c.FIRST_NAME, c.LAST_NAME
        ORDER BY TOTAL_TXNS DESC;
BEGIN
    DBMS_OUTPUT.PUT_LINE(RPAD('ID', 6) || RPAD('NAME', 24) || RPAD('TXNS', 8) || RPAD('TOTAL INFLOW', 18) || 'TOTAL OUTFLOW');
    DBMS_OUTPUT.PUT_LINE('-------------------------------------------------------------------------------');

    -- Cursor FOR loop automatically handles open, fetch, and close
    FOR rec IN c_customer_activity LOOP
        DBMS_OUTPUT.PUT_LINE(
            RPAD(TO_CHAR(rec.CUSTOMER_ID), 6) ||
            RPAD(rec.FULL_NAME, 24) ||
            RPAD(TO_CHAR(rec.TOTAL_TXNS), 8) ||
            RPAD('INR ' || TO_CHAR(rec.TOTAL_INFLOW, '999,990.00'), 18) ||
            'INR ' || TO_CHAR(rec.TOTAL_OUTFLOW, '999,990.00')
        );
    END LOOP;
    DBMS_OUTPUT.PUT_LINE('-------------------------------------------------------------------------------');
END;
/

PROMPT [OK] All cursor demonstrations executed successfully.
