-- ============================================================================
-- SCRIPT: 09_functions.sql
-- PROJECT: Smart Banking Management System
-- PURPOSE: User-Defined Functions for Calculations, Validations & Lookups
-- ORACLE DB COMPATIBILITY: Oracle 10g, 11g, 12c, 19c, 21c, 23ai
-- ============================================================================

PROMPT ====================================================================
PROMPT   Executing 09_functions.sql - Creating User-Defined Functions
PROMPT ====================================================================

-- 1. GET_ACCOUNT_BALANCE
-- Returns current balance of an account by Account Number
CREATE OR REPLACE FUNCTION GET_ACCOUNT_BALANCE (
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
        RETURN -1; -- Indicates account not found
    WHEN OTHERS THEN
        RETURN -999;
END GET_ACCOUNT_BALANCE;
/

-- 2. CALCULATE_LOAN_INTEREST
-- Calculates total simple or compound interest over a specified tenure
CREATE OR REPLACE FUNCTION CALCULATE_LOAN_INTEREST (
    p_principal     IN NUMBER,
    p_annual_rate   IN NUMBER,
    p_term_months   IN NUMBER
) RETURN NUMBER IS
    v_years NUMBER(6,2);
    v_interest NUMBER(15,2);
BEGIN
    IF p_principal <= 0 OR p_annual_rate < 0 OR p_term_months <= 0 THEN
        RETURN 0;
    END IF;
    
    v_years := p_term_months / 12.0;
    -- Simple interest formula: (P * R * T) / 100
    v_interest := (p_principal * p_annual_rate * v_years) / 100.0;
    
    RETURN ROUND(v_interest, 2);
END CALCULATE_LOAN_INTEREST;
/

-- 3. CALCULATE_MONTHLY_EMI
-- Computes standard reducing balance monthly Equated Monthly Installment (EMI)
-- EMI = [P * r * (1 + r)^n] / [(1 + r)^n - 1]
CREATE OR REPLACE FUNCTION CALCULATE_MONTHLY_EMI (
    p_principal     IN NUMBER,
    p_annual_rate   IN NUMBER,
    p_term_months   IN NUMBER
) RETURN NUMBER IS
    v_monthly_rate  NUMBER(10,6);
    v_emi           NUMBER(12,2);
    v_factor        NUMBER(20,8);
BEGIN
    IF p_principal <= 0 OR p_term_months <= 0 THEN
        RETURN 0;
    END IF;
    
    IF p_annual_rate = 0 THEN
        RETURN ROUND(p_principal / p_term_months, 2);
    END IF;
    
    v_monthly_rate := (p_annual_rate / 12.0) / 100.0;
    v_factor := POWER(1 + v_monthly_rate, p_term_months);
    
    v_emi := (p_principal * v_monthly_rate * v_factor) / (v_factor - 1);
    
    RETURN ROUND(v_emi, 2);
EXCEPTION
    WHEN ZERO_DIVIDE THEN
        RETURN ROUND(p_principal / p_term_months, 2);
    WHEN OTHERS THEN
        RETURN 0;
END CALCULATE_MONTHLY_EMI;
/

-- 4. GET_TOTAL_TRANSACTIONS
-- Returns the total count of completed transactions for an account
CREATE OR REPLACE FUNCTION GET_TOTAL_TRANSACTIONS (
    p_account_id IN NUMBER
) RETURN NUMBER IS
    v_count NUMBER(10);
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM TRANSACTIONS
    WHERE ACCOUNT_ID = p_account_id
      AND TRANSACTION_STATUS = 'Completed';
      
    RETURN v_count;
END GET_TOTAL_TRANSACTIONS;
/

-- 5. GET_CUSTOMER_ACCOUNT_COUNT
-- Returns the total number of bank accounts registered under a customer
CREATE OR REPLACE FUNCTION GET_CUSTOMER_ACCOUNT_COUNT (
    p_customer_id IN NUMBER
) RETURN NUMBER IS
    v_count NUMBER(5);
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM BANK_ACCOUNTS
    WHERE CUSTOMER_ID = p_customer_id;
    
    RETURN v_count;
END GET_CUSTOMER_ACCOUNT_COUNT;
/

-- 6. CHECK_ACCOUNT_STATUS
-- Validates whether an account is Active and eligible for debits/credits
CREATE OR REPLACE FUNCTION CHECK_ACCOUNT_STATUS (
    p_account_id IN NUMBER
) RETURN VARCHAR2 IS
    v_status VARCHAR2(20);
BEGIN
    SELECT ACCOUNT_STATUS INTO v_status
    FROM BANK_ACCOUNTS
    WHERE ACCOUNT_ID = p_account_id;
    
    RETURN v_status;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN 'NOT_FOUND';
END CHECK_ACCOUNT_STATUS;
/

PROMPT [OK] All 6 user-defined functions compiled successfully.
