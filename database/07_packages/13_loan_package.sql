-- ============================================================================
-- SCRIPT: 13_loan_package.sql
-- PROJECT: Smart Banking Management System
-- PURPOSE: LOAN_PACKAGE Specification & Body
--          Encapsulates loan application, credit rating check, EMI calculator,
--          approval workflow, payment processing, and payoff quotes.
-- ORACLE DB COMPATIBILITY: Oracle 10g, 11g, 12c, 19c, 21c, 23ai
-- ============================================================================

PROMPT ====================================================================
PROMPT   Executing 13_loan_package.sql - Compiling LOAN_PACKAGE
PROMPT ====================================================================

-- 1. PACKAGE SPECIFICATION
CREATE OR REPLACE PACKAGE LOAN_PACKAGE AS

    -- Public Package Procedures & Functions
    PROCEDURE APPLY_LOAN (
        p_customer_id   IN  NUMBER,
        p_branch_id     IN  NUMBER,
        p_loan_type     IN  VARCHAR2,
        p_loan_amount   IN  NUMBER,
        p_interest_rate IN  NUMBER,
        p_term_months   IN  NUMBER,
        p_loan_number   OUT VARCHAR2,
        p_monthly_emi   OUT NUMBER,
        p_status        OUT VARCHAR2,
        p_message       OUT VARCHAR2
    );

    PROCEDURE APPROVE_LOAN_REQUEST (
        p_loan_number   IN  VARCHAR2,
        p_decision      IN  VARCHAR2,
        p_disburse_acc  IN  VARCHAR2,
        p_status        OUT VARCHAR2,
        p_message       OUT VARCHAR2
    );

    PROCEDURE MAKE_PAYMENT (
        p_loan_number       IN  VARCHAR2,
        p_amount            IN  NUMBER,
        p_payment_method    IN  VARCHAR2,
        p_payment_ref       OUT VARCHAR2,
        p_remaining_bal     OUT NUMBER,
        p_status            OUT VARCHAR2,
        p_message           OUT VARCHAR2
    );

    FUNCTION CALCULATE_EMI (
        p_principal     IN NUMBER,
        p_annual_rate   IN NUMBER,
        p_term_months   IN NUMBER
    ) RETURN NUMBER;

    FUNCTION GET_LOAN_OUTSTANDING (
        p_loan_number IN VARCHAR2
    ) RETURN NUMBER;

    FUNCTION GET_EARLY_PAYOFF_QUOTE (
        p_loan_number IN VARCHAR2
    ) RETURN NUMBER;

END LOAN_PACKAGE;
/

-- 2. PACKAGE BODY
CREATE OR REPLACE PACKAGE BODY LOAN_PACKAGE AS

    PROCEDURE APPLY_LOAN (
        p_customer_id   IN  NUMBER,
        p_branch_id     IN  NUMBER,
        p_loan_type     IN  VARCHAR2,
        p_loan_amount   IN  NUMBER,
        p_interest_rate IN  NUMBER,
        p_term_months   IN  NUMBER,
        p_loan_number   OUT VARCHAR2,
        p_monthly_emi   OUT NUMBER,
        p_status        OUT VARCHAR2,
        p_message       OUT VARCHAR2
    ) IS
    BEGIN
        APPLY_FOR_LOAN(
            p_customer_id, p_branch_id, p_loan_type,
            p_loan_amount, p_interest_rate, p_term_months,
            p_loan_number, p_monthly_emi, p_status, p_message
        );
    END APPLY_LOAN;

    PROCEDURE APPROVE_LOAN_REQUEST (
        p_loan_number   IN  VARCHAR2,
        p_decision      IN  VARCHAR2,
        p_disburse_acc  IN  VARCHAR2,
        p_status        OUT VARCHAR2,
        p_message       OUT VARCHAR2
    ) IS
    BEGIN
        APPROVE_LOAN(
            p_loan_number, p_decision, p_disburse_acc,
            p_status, p_message
        );
    END APPROVE_LOAN_REQUEST;

    PROCEDURE MAKE_PAYMENT (
        p_loan_number       IN  VARCHAR2,
        p_amount            IN  NUMBER,
        p_payment_method    IN  VARCHAR2,
        p_payment_ref       OUT VARCHAR2,
        p_remaining_bal     OUT NUMBER,
        p_status            OUT VARCHAR2,
        p_message           OUT VARCHAR2
    ) IS
    BEGIN
        PROCESS_LOAN_PAYMENT(
            p_loan_number, p_amount, p_payment_method,
            p_payment_ref, p_remaining_bal, p_status, p_message
        );
    END MAKE_PAYMENT;

    FUNCTION CALCULATE_EMI (
        p_principal     IN NUMBER,
        p_annual_rate   IN NUMBER,
        p_term_months   IN NUMBER
    ) RETURN NUMBER IS
    BEGIN
        RETURN CALCULATE_MONTHLY_EMI(p_principal, p_annual_rate, p_term_months);
    END CALCULATE_EMI;

    FUNCTION GET_LOAN_OUTSTANDING (
        p_loan_number IN VARCHAR2
    ) RETURN NUMBER IS
        v_out NUMBER(15,2);
    BEGIN
        SELECT OUTSTANDING_BALANCE INTO v_out
        FROM LOANS
        WHERE LOAN_NUMBER = p_loan_number;
        
        RETURN v_out;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RETURN -1;
    END GET_LOAN_OUTSTANDING;

    FUNCTION GET_EARLY_PAYOFF_QUOTE (
        p_loan_number IN VARCHAR2
    ) RETURN NUMBER IS
        v_out           NUMBER(15,2);
        v_rate          NUMBER(5,2);
        v_accrued_int   NUMBER(12,2);
    BEGIN
        SELECT OUTSTANDING_BALANCE, INTEREST_RATE
        INTO v_out, v_rate
        FROM LOANS
        WHERE LOAN_NUMBER = p_loan_number;

        -- Accrued 15-day interest + outstanding principal
        v_accrued_int := ROUND((v_out * (v_rate / 100.0) * (15.0 / 365.0)), 2);
        RETURN (v_out + v_accrued_int);
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RETURN 0;
    END GET_EARLY_PAYOFF_QUOTE;

END LOAN_PACKAGE;
/

PROMPT [OK] LOAN_PACKAGE specification & body successfully compiled.
