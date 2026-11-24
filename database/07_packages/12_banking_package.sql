-- ============================================================================
-- SCRIPT: 12_banking_package.sql
-- PROJECT: Smart Banking Management System
-- PURPOSE: BANKING_PACKAGE Specification & Body
--          Encapsulates deposit, withdrawal, transfer, balance enquiry,
--          and statement retrieval via REF CURSOR.
-- ORACLE DB COMPATIBILITY: Oracle 10g, 11g, 12c, 19c, 21c, 23ai
-- ============================================================================

PROMPT ====================================================================
PROMPT   Executing 12_banking_package.sql - Compiling BANKING_PACKAGE
PROMPT ====================================================================

-- 1. PACKAGE SPECIFICATION
CREATE OR REPLACE PACKAGE BANKING_PACKAGE AS
    -- Global Constants
    MIN_TRANSFER_AMOUNT CONSTANT NUMBER(10,2) := 1.00;
    MAX_DAILY_TRANSFER  CONSTANT NUMBER(15,2) := 500000.00;

    -- User-Defined Exceptions
    e_insufficient_funds    EXCEPTION;
    e_invalid_account       EXCEPTION;
    e_account_dormant       EXCEPTION;

    -- Custom Record Type for Account Summary
    TYPE t_account_summary IS RECORD (
        account_id      NUMBER(10),
        account_number  VARCHAR2(20),
        customer_name   VARCHAR2(100),
        balance         NUMBER(15,2),
        account_status  VARCHAR2(20)
    );

    -- Ref Cursor for returning statements
    TYPE t_ref_cursor IS REF CURSOR;

    -- Procedures & Functions
    PROCEDURE DEPOSIT (
        p_account_number    IN  VARCHAR2,
        p_amount            IN  NUMBER,
        p_description       IN  VARCHAR2,
        p_txn_ref           OUT VARCHAR2,
        p_new_balance       OUT NUMBER,
        p_status            OUT VARCHAR2,
        p_message           OUT VARCHAR2
    );

    PROCEDURE WITHDRAW (
        p_account_number    IN  VARCHAR2,
        p_amount            IN  NUMBER,
        p_description       IN  VARCHAR2,
        p_txn_ref           OUT VARCHAR2,
        p_new_balance       OUT NUMBER,
        p_status            OUT VARCHAR2,
        p_message           OUT VARCHAR2
    );

    PROCEDURE TRANSFER (
        p_sender_acc_no     IN  VARCHAR2,
        p_receiver_acc_no   IN  VARCHAR2,
        p_amount            IN  NUMBER,
        p_description       IN  VARCHAR2,
        p_txn_ref           OUT VARCHAR2,
        p_sender_balance    OUT NUMBER,
        p_status            OUT VARCHAR2,
        p_message           OUT VARCHAR2
    );

    FUNCTION GET_BALANCE (
        p_account_number IN VARCHAR2
    ) RETURN NUMBER;

    FUNCTION GET_ACCOUNT_SUMMARY (
        p_account_number IN VARCHAR2
    ) RETURN t_account_summary;

    PROCEDURE GET_STATEMENT_CURSOR (
        p_account_number IN  VARCHAR2,
        p_start_date     IN  DATE,
        p_end_date       IN  DATE,
        p_cursor         OUT t_ref_cursor
    );

END BANKING_PACKAGE;
/

-- 2. PACKAGE BODY
CREATE OR REPLACE PACKAGE BODY BANKING_PACKAGE AS

    PROCEDURE DEPOSIT (
        p_account_number    IN  VARCHAR2,
        p_amount            IN  NUMBER,
        p_description       IN  VARCHAR2,
        p_txn_ref           OUT VARCHAR2,
        p_new_balance       OUT NUMBER,
        p_status            OUT VARCHAR2,
        p_message           OUT VARCHAR2
    ) IS
    BEGIN
        DEPOSIT_MONEY(
            p_account_number, p_amount, p_description,
            p_txn_ref, p_new_balance, p_status, p_message
        );
    END DEPOSIT;

    PROCEDURE WITHDRAW (
        p_account_number    IN  VARCHAR2,
        p_amount            IN  NUMBER,
        p_description       IN  VARCHAR2,
        p_txn_ref           OUT VARCHAR2,
        p_new_balance       OUT NUMBER,
        p_status            OUT VARCHAR2,
        p_message           OUT VARCHAR2
    ) IS
    BEGIN
        WITHDRAW_MONEY(
            p_account_number, p_amount, p_description,
            p_txn_ref, p_new_balance, p_status, p_message
        );
    END WITHDRAW;

    PROCEDURE TRANSFER (
        p_sender_acc_no     IN  VARCHAR2,
        p_receiver_acc_no   IN  VARCHAR2,
        p_amount            IN  NUMBER,
        p_description       IN  VARCHAR2,
        p_txn_ref           OUT VARCHAR2,
        p_sender_balance    OUT NUMBER,
        p_status            OUT VARCHAR2,
        p_message           OUT VARCHAR2
    ) IS
    BEGIN
        TRANSFER_MONEY(
            p_sender_acc_no, p_receiver_acc_no, p_amount, p_description,
            p_txn_ref, p_sender_balance, p_status, p_message
        );
    END TRANSFER;

    FUNCTION GET_BALANCE (
        p_account_number IN VARCHAR2
    ) RETURN NUMBER IS
    BEGIN
        RETURN GET_ACCOUNT_BALANCE(p_account_number);
    END GET_BALANCE;

    FUNCTION GET_ACCOUNT_SUMMARY (
        p_account_number IN VARCHAR2
    ) RETURN t_account_summary IS
        v_summary t_account_summary;
    BEGIN
        SELECT 
            a.ACCOUNT_ID,
            a.ACCOUNT_NUMBER,
            c.FIRST_NAME || ' ' || c.LAST_NAME,
            a.BALANCE,
            a.ACCOUNT_STATUS
        INTO v_summary
        FROM BANK_ACCOUNTS a
        JOIN CUSTOMERS c ON a.CUSTOMER_ID = c.CUSTOMER_ID
        WHERE a.ACCOUNT_NUMBER = p_account_number;

        RETURN v_summary;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            v_summary.account_id := -1;
            v_summary.account_number := 'UNKNOWN';
            v_summary.balance := 0;
            RETURN v_summary;
    END GET_ACCOUNT_SUMMARY;

    PROCEDURE GET_STATEMENT_CURSOR (
        p_account_number IN  VARCHAR2,
        p_start_date     IN  DATE,
        p_end_date       IN  DATE,
        p_cursor         OUT t_ref_cursor
    ) IS
        v_acc_id NUMBER(10);
    BEGIN
        SELECT ACCOUNT_ID INTO v_acc_id
        FROM BANK_ACCOUNTS
        WHERE ACCOUNT_NUMBER = p_account_number;

        OPEN p_cursor FOR
            SELECT 
                TRANSACTION_REF,
                TRANSACTION_DATE,
                TRANSACTION_TYPE,
                AMOUNT,
                BALANCE_AFTER,
                DESCRIPTION,
                TRANSACTION_STATUS
            FROM TRANSACTIONS
            WHERE ACCOUNT_ID = v_acc_id
              AND TRUNC(CAST(TRANSACTION_DATE AS DATE)) BETWEEN p_start_date AND p_end_date
            ORDER BY TRANSACTION_DATE DESC;
    END GET_STATEMENT_CURSOR;

END BANKING_PACKAGE;
/

PROMPT [OK] BANKING_PACKAGE specification & body successfully compiled.
