-- ============================================================================
-- SCRIPT: 15_advanced_plsql.sql
-- PROJECT: Smart Banking Management System
-- PURPOSE: Exhaustive demonstration of Advanced PL/SQL capabilities:
--          1. Anonymous PL/SQL Block with DECLARE, BEGIN, EXCEPTION
--          2. Variables, Constants, and Data Types
--          3. %TYPE and %ROWTYPE Attribute Usage
--          4. User-Defined RECORD Types
--          5. Collections: VARRAY, Nested Tables, Associative Arrays (INDEX BY)
--          6. Bulk Operations: BULK COLLECT and FORALL
--          7. Dynamic SQL via EXECUTE IMMEDIATE
--          8. Exception Handling: Predefined and User-Defined with RAISE_APPLICATION_ERROR
--          9. Control Structures: IF-THEN-ELSIF, CASE, FOR, WHILE, Basic LOOP
-- ORACLE DB COMPATIBILITY: Oracle 10g, 11g, 12c, 19c, 21c, 23ai
-- ============================================================================

SET SERVEROUTPUT ON
SET LINESIZE 300

PROMPT ====================================================================
PROMPT   Executing 15_advanced_plsql.sql - Advanced PL/SQL Showcase
PROMPT ====================================================================

-- 1. ANONYMOUS BLOCK WITH VARIABLES, CONSTANTS, %TYPE, %ROWTYPE & RECORD
PROMPT --------------------------------------------------------------------
PROMPT 1. Variables, Constants, %TYPE, %ROWTYPE, and Custom RECORD
PROMPT --------------------------------------------------------------------
DECLARE
    -- Constants
    c_tax_rate CONSTANT NUMBER(4,2) := 0.18; -- 18% GST on fees
    c_bank_name CONSTANT VARCHAR2(50) := 'Smart Banking System';

    -- %TYPE Variables
    v_acc_num       BANK_ACCOUNTS.ACCOUNT_NUMBER%TYPE;
    v_balance       BANK_ACCOUNTS.BALANCE%TYPE;

    -- %ROWTYPE Variable
    v_branch_row    BANK_BRANCHES%ROWTYPE;

    -- User-Defined RECORD Type
    TYPE t_financial_profile IS RECORD (
        customer_id     NUMBER(10),
        full_name       VARCHAR2(100),
        total_balance   NUMBER(15,2),
        credit_score    NUMBER(4),
        vip_tier        VARCHAR2(20)
    );
    v_profile t_financial_profile;
BEGIN
    SELECT ACCOUNT_NUMBER, BALANCE INTO v_acc_num, v_balance
    FROM BANK_ACCOUNTS WHERE ACCOUNT_ID = 2001;

    SELECT * INTO v_branch_row
    FROM BANK_BRANCHES WHERE BRANCH_ID = 101;

    v_profile.customer_id := 1001;
    v_profile.full_name := 'Aarav Sharma';
    v_profile.total_balance := v_balance;
    v_profile.credit_score := 780;

    -- Conditional Structure (IF-THEN-ELSIF)
    IF v_profile.credit_score >= 750 THEN
        v_profile.vip_tier := 'Platinum Elite';
    ELSIF v_profile.credit_score >= 650 THEN
        v_profile.vip_tier := 'Gold Preferred';
    ELSE
        v_profile.vip_tier := 'Silver Standard';
    END IF;

    DBMS_OUTPUT.PUT_LINE('Bank              : ' || c_bank_name);
    DBMS_OUTPUT.PUT_LINE('Branch            : ' || v_branch_row.BRANCH_NAME || ' (' || v_branch_row.IFSC_CODE || ')');
    DBMS_OUTPUT.PUT_LINE('Account #         : ' || v_acc_num || ' | Balance: INR ' || v_balance);
    DBMS_OUTPUT.PUT_LINE('Customer Profile  : ' || v_profile.full_name || ' | Tier: ' || v_profile.vip_tier);
END;
/

-- 2. CONTROL STRUCTURES & LOOPS (CASE, FOR, WHILE, BASIC LOOP, NESTED LOOPS)
PROMPT --------------------------------------------------------------------
PROMPT 2. Control Structures: CASE, FOR Loop, WHILE Loop, and Nested Loops
PROMPT --------------------------------------------------------------------
DECLARE
    v_counter NUMBER := 1;
    v_grade   VARCHAR2(20);
    v_tier_id NUMBER := 2;
BEGIN
    -- CASE Statement
    v_grade := CASE v_tier_id
        WHEN 1 THEN 'Retail Basic'
        WHEN 2 THEN 'Commercial Silver'
        WHEN 3 THEN 'Corporate Gold'
        ELSE 'General Account'
    END;
    DBMS_OUTPUT.PUT_LINE('Case evaluated grade: ' || v_grade);

    -- WHILE Loop: Interest rate progression test
    DBMS_OUTPUT.PUT_LINE('--- WHILE Loop (Interest rate compounding simulation) ---');
    WHILE v_counter <= 3 LOOP
        DBMS_OUTPUT.PUT_LINE('  Year ' || v_counter || ' projected multiplier: ' || (1 + (0.05 * v_counter)));
        v_counter := v_counter + 1;
    END LOOP;

    -- Basic LOOP with EXIT WHEN
    DBMS_OUTPUT.PUT_LINE('--- Basic LOOP with EXIT WHEN ---');
    v_counter := 1;
    LOOP
        DBMS_OUTPUT.PUT_LINE('  Basic iteration #' || v_counter);
        v_counter := v_counter + 1;
        EXIT WHEN v_counter > 2;
    END LOOP;

    -- Nested FOR Loops: 2x2 Interest Matrix
    DBMS_OUTPUT.PUT_LINE('--- Nested FOR Loops (Tenure x Risk matrix) ---');
    FOR tenure IN 1..2 LOOP
        FOR risk_factor IN 1..2 LOOP
            DBMS_OUTPUT.PUT_LINE('    Tenure Yr ' || tenure || ' * Risk ' || risk_factor || ' = Index ' || (tenure * risk_factor));
        END LOOP;
    END LOOP;
END;
/

-- 3. COLLECTIONS DEMONSTRATION: VARRAY, NESTED TABLES, ASSOCIATIVE ARRAYS
PROMPT --------------------------------------------------------------------
PROMPT 3. Collections Showcase: VARRAY, Nested Table & Associative Array
PROMPT --------------------------------------------------------------------
DECLARE
    -- A. VARRAY (Fixed maximum size)
    TYPE t_branch_codes IS VARRAY(5) OF VARCHAR2(10);
    v_codes t_branch_codes := t_branch_codes('BR001', 'BR002', 'BR003', 'BR004', 'BR005');

    -- B. Nested Table (Dynamically sized collection)
    TYPE t_acc_list IS TABLE OF VARCHAR2(20);
    v_accounts t_acc_list := t_acc_list('SB1001002001', 'SB1001002002', 'SB1002002003');

    -- C. Associative Array (INDEX BY VARCHAR2 / Integer - Key-Value Map)
    TYPE t_rates_map IS TABLE OF NUMBER(5,2) INDEX BY VARCHAR2(30);
    v_rates t_rates_map;
    v_key VARCHAR2(30);
BEGIN
    DBMS_OUTPUT.PUT_LINE('VARRAY count: ' || v_codes.COUNT || ' | First element: ' || v_codes(1));

    -- Nested Table manipulation
    v_accounts.EXTEND;
    v_accounts(4) := 'SB1003002004';
    DBMS_OUTPUT.PUT_LINE('Nested Table count: ' || v_accounts.COUNT || ' | Last element: ' || v_accounts(v_accounts.LAST));

    -- Associative Array population & traversal
    v_rates('Home Loan') := 8.50;
    v_rates('Auto Loan') := 9.25;
    v_rates('Personal Loan') := 12.00;
    v_rates('Education Loan') := 9.00;

    v_key := v_rates.FIRST;
    DBMS_OUTPUT.PUT_LINE('Associative Array Rates Table:');
    WHILE v_key IS NOT NULL LOOP
        DBMS_OUTPUT.PUT_LINE('  ' || RPAD(v_key, 16) || ' -> ' || v_rates(v_key) || '% APR');
        v_key := v_rates.NEXT(v_key);
    END LOOP;
END;
/

-- 4. HIGH-PERFORMANCE BULK OPERATIONS (BULK COLLECT & FORALL)
PROMPT --------------------------------------------------------------------
PROMPT 4. Bulk Processing: BULK COLLECT and FORALL Demonstration
PROMPT --------------------------------------------------------------------
DECLARE
    -- Types for bulk processing
    TYPE t_acc_ids IS TABLE OF BANK_ACCOUNTS.ACCOUNT_ID%TYPE;
    TYPE t_balances IS TABLE OF BANK_ACCOUNTS.BALANCE%TYPE;

    v_ids   t_acc_ids;
    v_bals  t_balances;
BEGIN
    -- BULK COLLECT: Fetches entire result set in a single context switch!
    SELECT ACCOUNT_ID, BALANCE
    BULK COLLECT INTO v_ids, v_bals
    FROM BANK_ACCOUNTS
    WHERE ACCOUNT_STATUS = 'Active';

    DBMS_OUTPUT.PUT_LINE('BULK COLLECT fetched ' || v_ids.COUNT || ' accounts into memory at once.');

    FOR i IN 1..v_ids.COUNT LOOP
        DBMS_OUTPUT.PUT_LINE('  Bulk Record [' || i || '] -> Account ID: ' || v_ids(i) || ' | Balance: INR ' || v_bals(i));
    END LOOP;

    -- FORALL: High performance bulk DML execution
    -- Updates multiple rows in a single SQL engine call
    FORALL i IN 1..v_ids.COUNT
        UPDATE BANK_ACCOUNTS
        SET UPDATED_AT = SYSDATE
        WHERE ACCOUNT_ID = v_ids(i);

    DBMS_OUTPUT.PUT_LINE('FORALL successfully executed bulk touch update on ' || SQL%ROWCOUNT || ' accounts.');
    COMMIT;
END;
/

-- 5. DYNAMIC SQL USING EXECUTE IMMEDIATE
PROMPT --------------------------------------------------------------------
PROMPT 5. Dynamic SQL: EXECUTE IMMEDIATE Demonstration
PROMPT --------------------------------------------------------------------
DECLARE
    v_table_name    VARCHAR2(30) := 'BANK_ACCOUNTS';
    v_column_name   VARCHAR2(30) := 'BALANCE';
    v_min_threshold NUMBER := 50000;
    v_sql_stmt      VARCHAR2(1000);
    v_result_count  NUMBER;
    v_total_sum     NUMBER;
BEGIN
    -- Dynamic query construction with bind variables
    v_sql_stmt := 'SELECT COUNT(*), NVL(SUM(' || v_column_name || '), 0) FROM ' || 
                  v_table_name || ' WHERE ' || v_column_name || ' >= :threshold AND ACCOUNT_STATUS = :status';

    EXECUTE IMMEDIATE v_sql_stmt 
    INTO v_result_count, v_total_sum 
    USING v_min_threshold, 'Active';

    DBMS_OUTPUT.PUT_LINE('Dynamic SQL statement executed:');
    DBMS_OUTPUT.PUT_LINE('  Query: ' || v_sql_stmt);
    DBMS_OUTPUT.PUT_LINE('  Accounts with balance >= ' || v_min_threshold || ': ' || v_result_count);
    DBMS_OUTPUT.PUT_LINE('  Total aggregate balance: INR ' || TO_CHAR(v_total_sum, '999,999,990.00'));
END;
/

-- 6. EXCEPTION HANDLING DEMO: PREDEFINED & USER-DEFINED EXCEPTIONS
PROMPT --------------------------------------------------------------------
PROMPT 6. Exception Handling: Predefined and User-Defined Banking Errors
PROMPT --------------------------------------------------------------------
DECLARE
    v_num NUMBER;
    -- User-defined exception
    e_unauthorized_access EXCEPTION;
    PRAGMA EXCEPTION_INIT(e_unauthorized_access, -20050);
BEGIN
    -- 6.1 Predefined: ZERO_DIVIDE handling
    BEGIN
        v_num := 100 / 0;
    EXCEPTION
        WHEN ZERO_DIVIDE THEN
            DBMS_OUTPUT.PUT_LINE('[CAUGHT] ZERO_DIVIDE caught gracefully: Attempted division by zero.');
    END;

    -- 6.2 Predefined: NO_DATA_FOUND handling
    BEGIN
        SELECT BALANCE INTO v_num FROM BANK_ACCOUNTS WHERE ACCOUNT_ID = 999999;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            DBMS_OUTPUT.PUT_LINE('[CAUGHT] NO_DATA_FOUND caught gracefully: Queried non-existent account.');
    END;

    -- 6.3 User-Defined Exception using RAISE
    BEGIN
        RAISE e_unauthorized_access;
    EXCEPTION
        WHEN e_unauthorized_access THEN
            DBMS_OUTPUT.PUT_LINE('[CAUGHT] User-Defined Exception e_unauthorized_access caught successfully.');
    END;
END;
/

PROMPT [OK] All advanced PL/SQL concepts demonstrated and verified.
