-- ============================================================================
-- SCRIPT: 10_procedures.sql
-- PROJECT: Smart Banking Management System
-- PURPOSE: Core Stored Procedures for Banking Operations, Loans, and Statements
--          Full parameter validation, atomic transactions, and exception handling.
-- ORACLE DB COMPATIBILITY: Oracle 10g, 11g, 12c, 19c, 21c, 23ai
-- ============================================================================

PROMPT ====================================================================
PROMPT   Executing 10_procedures.sql - Creating Banking Stored Procedures
PROMPT ====================================================================

-- 1. CREATE_BANK_ACCOUNT
CREATE OR REPLACE PROCEDURE CREATE_BANK_ACCOUNT (
    p_customer_id       IN  NUMBER,
    p_branch_id         IN  NUMBER,
    p_type_id           IN  NUMBER,
    p_initial_deposit   IN  NUMBER,
    p_account_number    OUT VARCHAR2,
    p_status            OUT VARCHAR2,
    p_message           OUT VARCHAR2
) IS
    v_min_bal       NUMBER(12,2);
    v_cust_exists   NUMBER;
    v_branch_exists NUMBER;
    v_acc_id        NUMBER(10);
    v_new_acc_no    VARCHAR2(20);
BEGIN
    -- Validate Customer
    SELECT COUNT(*) INTO v_cust_exists FROM CUSTOMERS WHERE CUSTOMER_ID = p_customer_id;
    IF v_cust_exists = 0 THEN
        p_status := 'ERROR';
        p_message := 'Customer ID does not exist.';
        RETURN;
    END IF;

    -- Validate Branch
    SELECT COUNT(*) INTO v_branch_exists FROM BANK_BRANCHES WHERE BRANCH_ID = p_branch_id;
    IF v_branch_exists = 0 THEN
        p_status := 'ERROR';
        p_message := 'Branch ID does not exist.';
        RETURN;
    END IF;

    -- Validate Minimum Balance for Type
    SELECT MIN_BALANCE INTO v_min_bal FROM ACCOUNT_TYPES WHERE TYPE_ID = p_type_id;
    IF p_initial_deposit < v_min_bal THEN
        p_status := 'ERROR';
        p_message := 'Initial deposit is below minimum balance requirement of INR ' || v_min_bal;
        RETURN;
    END IF;

    -- Generate ID & Unique Account Number
    SELECT SEQ_ACCOUNTS.NEXTVAL INTO v_acc_id FROM DUAL;
    v_new_acc_no := 'SB' || TO_CHAR(p_customer_id) || TO_CHAR(v_acc_id);

    INSERT INTO BANK_ACCOUNTS (
        ACCOUNT_ID, ACCOUNT_NUMBER, CUSTOMER_ID, BRANCH_ID, TYPE_ID, 
        BALANCE, OVERDRAFT_LIMIT, ACCOUNT_STATUS, OPENED_DATE
    ) VALUES (
        v_acc_id, v_new_acc_no, p_customer_id, p_branch_id, p_type_id,
        p_initial_deposit, 0.00, 'Active', SYSDATE
    );

    -- Log Initial Deposit Transaction
    IF p_initial_deposit > 0 THEN
        INSERT INTO TRANSACTIONS (
            TRANSACTION_ID, TRANSACTION_REF, ACCOUNT_ID, TRANSACTION_TYPE,
            AMOUNT, BALANCE_AFTER, TRANSACTION_DATE, RELATED_ACCOUNT_ID,
            DESCRIPTION, TRANSACTION_STATUS
        ) VALUES (
            SEQ_TRANSACTIONS.NEXTVAL,
            'TXN-' || TO_CHAR(SYSDATE, 'YYYYMMDD') || '-' || LPAD(SEQ_TRANSACTIONS.CURRVAL, 5, '0'),
            v_acc_id, 'Deposit', p_initial_deposit, p_initial_deposit,
            SYSTIMESTAMP, NULL, 'Account Opening Initial Deposit', 'Completed'
        );
    END IF;

    COMMIT;
    p_account_number := v_new_acc_no;
    p_status := 'SUCCESS';
    p_message := 'Account ' || v_new_acc_no || ' created successfully with balance INR ' || p_initial_deposit;

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_status := 'FAIL';
        p_message := 'Database error creating account: ' || SQLERRM;
END CREATE_BANK_ACCOUNT;
/

-- 2. DEPOSIT_MONEY
CREATE OR REPLACE PROCEDURE DEPOSIT_MONEY (
    p_account_number    IN  VARCHAR2,
    p_amount            IN  NUMBER,
    p_description       IN  VARCHAR2,
    p_txn_ref           OUT VARCHAR2,
    p_new_balance       OUT NUMBER,
    p_status            OUT VARCHAR2,
    p_message           OUT VARCHAR2
) IS
    v_acc_id        NUMBER(10);
    v_current_bal   NUMBER(15,2);
    v_acc_status    VARCHAR2(20);
    v_ref           VARCHAR2(30);
BEGIN
    IF p_amount <= 0 THEN
        p_status := 'ERROR';
        p_message := 'Deposit amount must be strictly greater than zero.';
        RETURN;
    END IF;

    -- Lock row for update
    SELECT ACCOUNT_ID, BALANCE, ACCOUNT_STATUS 
    INTO v_acc_id, v_current_bal, v_acc_status
    FROM BANK_ACCOUNTS
    WHERE ACCOUNT_NUMBER = p_account_number
    FOR UPDATE;

    IF v_acc_status <> 'Active' THEN
        p_status := 'ERROR';
        p_message := 'Cannot deposit into non-active account (Status: ' || v_acc_status || ').';
        ROLLBACK;
        RETURN;
    END IF;

    v_current_bal := v_current_bal + p_amount;
    v_ref := 'TXN-' || TO_CHAR(SYSDATE, 'YYYYMMDD') || '-' || LPAD(SEQ_TRANSACTIONS.NEXTVAL, 6, '0');

    UPDATE BANK_ACCOUNTS 
    SET BALANCE = v_current_bal, UPDATED_AT = SYSDATE 
    WHERE ACCOUNT_ID = v_acc_id;

    INSERT INTO TRANSACTIONS (
        TRANSACTION_ID, TRANSACTION_REF, ACCOUNT_ID, TRANSACTION_TYPE,
        AMOUNT, BALANCE_AFTER, TRANSACTION_DATE, RELATED_ACCOUNT_ID,
        DESCRIPTION, TRANSACTION_STATUS
    ) VALUES (
        SEQ_TRANSACTIONS.CURRVAL, v_ref, v_acc_id, 'Deposit',
        p_amount, v_current_bal, SYSTIMESTAMP, NULL,
        NVL(p_description, 'Cash / Online Deposit'), 'Completed'
    );

    COMMIT;
    p_txn_ref := v_ref;
    p_new_balance := v_current_bal;
    p_status := 'SUCCESS';
    p_message := 'Successfully deposited INR ' || p_amount || '. New balance: INR ' || v_current_bal;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'Account number ' || p_account_number || ' not found.';
    WHEN OTHERS THEN
        ROLLBACK;
        p_status := 'FAIL';
        p_message := 'Deposit failed: ' || SQLERRM;
END DEPOSIT_MONEY;
/

-- 3. WITHDRAW_MONEY
CREATE OR REPLACE PROCEDURE WITHDRAW_MONEY (
    p_account_number    IN  VARCHAR2,
    p_amount            IN  NUMBER,
    p_description       IN  VARCHAR2,
    p_txn_ref           OUT VARCHAR2,
    p_new_balance       OUT NUMBER,
    p_status            OUT VARCHAR2,
    p_message           OUT VARCHAR2
) IS
    v_acc_id        NUMBER(10);
    v_current_bal   NUMBER(15,2);
    v_od_limit      NUMBER(12,2);
    v_acc_status    VARCHAR2(20);
    v_ref           VARCHAR2(30);
    e_insufficient_funds EXCEPTION;
BEGIN
    IF p_amount <= 0 THEN
        p_status := 'ERROR';
        p_message := 'Withdrawal amount must be greater than zero.';
        RETURN;
    END IF;

    SELECT ACCOUNT_ID, BALANCE, OVERDRAFT_LIMIT, ACCOUNT_STATUS 
    INTO v_acc_id, v_current_bal, v_od_limit, v_acc_status
    FROM BANK_ACCOUNTS
    WHERE ACCOUNT_NUMBER = p_account_number
    FOR UPDATE;

    IF v_acc_status <> 'Active' THEN
        p_status := 'ERROR';
        p_message := 'Cannot withdraw from ' || v_acc_status || ' account.';
        ROLLBACK;
        RETURN;
    END IF;

    IF (v_current_bal + v_od_limit) < p_amount THEN
        RAISE e_insufficient_funds;
    END IF;

    v_current_bal := v_current_bal - p_amount;
    v_ref := 'TXN-' || TO_CHAR(SYSDATE, 'YYYYMMDD') || '-' || LPAD(SEQ_TRANSACTIONS.NEXTVAL, 6, '0');

    UPDATE BANK_ACCOUNTS 
    SET BALANCE = v_current_bal, UPDATED_AT = SYSDATE 
    WHERE ACCOUNT_ID = v_acc_id;

    INSERT INTO TRANSACTIONS (
        TRANSACTION_ID, TRANSACTION_REF, ACCOUNT_ID, TRANSACTION_TYPE,
        AMOUNT, BALANCE_AFTER, TRANSACTION_DATE, RELATED_ACCOUNT_ID,
        DESCRIPTION, TRANSACTION_STATUS
    ) VALUES (
        SEQ_TRANSACTIONS.CURRVAL, v_ref, v_acc_id, 'Withdrawal',
        p_amount, v_current_bal, SYSTIMESTAMP, NULL,
        NVL(p_description, 'Cash / ATM Withdrawal'), 'Completed'
    );

    COMMIT;
    p_txn_ref := v_ref;
    p_new_balance := v_current_bal;
    p_status := 'SUCCESS';
    p_message := 'Successfully withdrew INR ' || p_amount || '. Remaining balance: INR ' || v_current_bal;

EXCEPTION
    WHEN e_insufficient_funds THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'Insufficient funds. Available: INR ' || (v_current_bal + v_od_limit) || ', Requested: INR ' || p_amount;
    WHEN NO_DATA_FOUND THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'Account number ' || p_account_number || ' not found.';
    WHEN OTHERS THEN
        ROLLBACK;
        p_status := 'FAIL';
        p_message := 'Withdrawal failed: ' || SQLERRM;
END WITHDRAW_MONEY;
/

-- 4. TRANSFER_MONEY (ATOMIC MONEY TRANSFER WITH TCL)
CREATE OR REPLACE PROCEDURE TRANSFER_MONEY (
    p_sender_acc_no     IN  VARCHAR2,
    p_receiver_acc_no   IN  VARCHAR2,
    p_amount            IN  NUMBER,
    p_description       IN  VARCHAR2,
    p_txn_ref           OUT VARCHAR2,
    p_sender_balance    OUT NUMBER,
    p_status            OUT VARCHAR2,
    p_message           OUT VARCHAR2
) IS
    v_sender_id         NUMBER(10);
    v_receiver_id       NUMBER(10);
    v_sender_bal        NUMBER(15,2);
    v_receiver_bal      NUMBER(15,2);
    v_sender_od         NUMBER(12,2);
    v_sender_status     VARCHAR2(20);
    v_receiver_status   VARCHAR2(20);
    v_debit_ref         VARCHAR2(30);
    v_credit_ref        VARCHAR2(30);
    
    e_same_account      EXCEPTION;
    e_insufficient_funds EXCEPTION;
    e_invalid_amount    EXCEPTION;
    e_account_blocked   EXCEPTION;
BEGIN
    -- 1. Validation checks
    IF p_sender_acc_no = p_receiver_acc_no THEN
        RAISE e_same_account;
    END IF;

    IF p_amount <= 0 THEN
        RAISE e_invalid_amount;
    END IF;

    -- 2. Lock sender account
    BEGIN
        SELECT ACCOUNT_ID, BALANCE, OVERDRAFT_LIMIT, ACCOUNT_STATUS
        INTO v_sender_id, v_sender_bal, v_sender_od, v_sender_status
        FROM BANK_ACCOUNTS
        WHERE ACCOUNT_NUMBER = p_sender_acc_no
        FOR UPDATE;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            p_status := 'ERROR';
            p_message := 'Sender account ' || p_sender_acc_no || ' does not exist.';
            RETURN;
    END;

    IF v_sender_status <> 'Active' THEN
        RAISE e_account_blocked;
    END IF;

    IF (v_sender_bal + v_sender_od) < p_amount THEN
        RAISE e_insufficient_funds;
    END IF;

    -- 3. Lock receiver account
    BEGIN
        SELECT ACCOUNT_ID, BALANCE, ACCOUNT_STATUS
        INTO v_receiver_id, v_receiver_bal, v_receiver_status
        FROM BANK_ACCOUNTS
        WHERE ACCOUNT_NUMBER = p_receiver_acc_no
        FOR UPDATE;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            ROLLBACK;
            p_status := 'ERROR';
            p_message := 'Beneficiary account ' || p_receiver_acc_no || ' does not exist.';
            RETURN;
    END;

    IF v_receiver_status <> 'Active' THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'Beneficiary account is not active (Status: ' || v_receiver_status || ').';
        RETURN;
    END IF;

    -- 4. Deduct money from sender
    v_sender_bal := v_sender_bal - p_amount;
    UPDATE BANK_ACCOUNTS 
    SET BALANCE = v_sender_bal, UPDATED_AT = SYSDATE 
    WHERE ACCOUNT_ID = v_sender_id;

    -- 5. Credit money to receiver
    v_receiver_bal := v_receiver_bal + p_amount;
    UPDATE BANK_ACCOUNTS 
    SET BALANCE = v_receiver_bal, UPDATED_AT = SYSDATE 
    WHERE ACCOUNT_ID = v_receiver_id;

    -- 6. Insert sender debit transaction
    v_debit_ref := 'TXN-' || TO_CHAR(SYSDATE, 'YYYYMMDD') || '-' || LPAD(SEQ_TRANSACTIONS.NEXTVAL, 6, '0');
    INSERT INTO TRANSACTIONS (
        TRANSACTION_ID, TRANSACTION_REF, ACCOUNT_ID, TRANSACTION_TYPE,
        AMOUNT, BALANCE_AFTER, TRANSACTION_DATE, RELATED_ACCOUNT_ID,
        DESCRIPTION, TRANSACTION_STATUS
    ) VALUES (
        SEQ_TRANSACTIONS.CURRVAL, v_debit_ref, v_sender_id, 'Transfer_Debit',
        p_amount, v_sender_bal, SYSTIMESTAMP, v_receiver_id,
        'Transfer to ' || p_receiver_acc_no || ': ' || NVL(p_description, 'Fund Transfer'), 'Completed'
    );

    -- 7. Insert receiver credit transaction
    v_credit_ref := 'TXN-' || TO_CHAR(SYSDATE, 'YYYYMMDD') || '-' || LPAD(SEQ_TRANSACTIONS.NEXTVAL, 6, '0');
    INSERT INTO TRANSACTIONS (
        TRANSACTION_ID, TRANSACTION_REF, ACCOUNT_ID, TRANSACTION_TYPE,
        AMOUNT, BALANCE_AFTER, TRANSACTION_DATE, RELATED_ACCOUNT_ID,
        DESCRIPTION, TRANSACTION_STATUS
    ) VALUES (
        SEQ_TRANSACTIONS.CURRVAL, v_credit_ref, v_receiver_id, 'Transfer_Credit',
        p_amount, v_receiver_bal, SYSTIMESTAMP, v_sender_id,
        'Transfer from ' || p_sender_acc_no || ': ' || NVL(p_description, 'Fund Transfer'), 'Completed'
    );

    -- 8. Explicit COMMIT ensures atomicity
    COMMIT;

    p_txn_ref := v_debit_ref;
    p_sender_balance := v_sender_bal;
    p_status := 'SUCCESS';
    p_message := 'Transferred INR ' || p_amount || ' to ' || p_receiver_acc_no || ' successfully.';

EXCEPTION
    WHEN e_same_account THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'Sender and beneficiary accounts cannot be the same.';
    WHEN e_invalid_amount THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'Transfer amount must be strictly greater than zero.';
    WHEN e_insufficient_funds THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'Transfer failed: Insufficient balance in sender account.';
    WHEN e_account_blocked THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'Sender account is inactive, frozen, or closed.';
    WHEN OTHERS THEN
        ROLLBACK;
        p_status := 'FAIL';
        p_message := 'Transfer rolled back due to error: ' || SQLERRM;
END TRANSFER_MONEY;
/

-- 5. CREATE_BENEFICIARY
CREATE OR REPLACE PROCEDURE CREATE_BENEFICIARY (
    p_customer_id       IN  NUMBER,
    p_name              IN  VARCHAR2,
    p_account_no        IN  VARCHAR2,
    p_bank_name         IN  VARCHAR2,
    p_ifsc              IN  VARCHAR2,
    p_limit             IN  NUMBER,
    p_beneficiary_id    OUT NUMBER,
    p_status            OUT VARCHAR2,
    p_message           OUT VARCHAR2
) IS
    v_new_id NUMBER(10);
BEGIN
    SELECT SEQ_BENEFICIARIES.NEXTVAL INTO v_new_id FROM DUAL;

    INSERT INTO BENEFICIARIES (
        BENEFICIARY_ID, CUSTOMER_ID, BENEFICIARY_NAME, BENEFICIARY_ACCOUNT,
        BANK_NAME, IFSC_CODE, TRANSFER_LIMIT, STATUS, ADDED_DATE
    ) VALUES (
        v_new_id, p_customer_id, p_name, p_account_no,
        p_bank_name, p_ifsc, NVL(p_limit, 50000.00), 'Active', SYSDATE
    );

    COMMIT;
    p_beneficiary_id := v_new_id;
    p_status := 'SUCCESS';
    p_message := 'Beneficiary ' || p_name || ' added successfully.';
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'Failed to add beneficiary: ' || SQLERRM;
END CREATE_BENEFICIARY;
/

-- 6. APPLY_FOR_LOAN
CREATE OR REPLACE PROCEDURE APPLY_FOR_LOAN (
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
    v_loan_id   NUMBER(10);
    v_loan_no   VARCHAR2(20);
    v_emi       NUMBER(12,2);
BEGIN
    IF p_loan_amount <= 0 OR p_term_months <= 0 THEN
        p_status := 'ERROR';
        p_message := 'Loan amount and term months must be strictly positive.';
        RETURN;
    END IF;

    v_emi := CALCULATE_MONTHLY_EMI(p_loan_amount, p_interest_rate, p_term_months);
    SELECT SEQ_LOANS.NEXTVAL INTO v_loan_id FROM DUAL;
    v_loan_no := 'LN' || TO_CHAR(SYSDATE, 'YYYYMM') || TO_CHAR(v_loan_id);

    INSERT INTO LOANS (
        LOAN_ID, LOAN_NUMBER, CUSTOMER_ID, BRANCH_ID, LOAN_TYPE,
        LOAN_AMOUNT, INTEREST_RATE, TERM_MONTHS, MONTHLY_EMI,
        OUTSTANDING_BALANCE, LOAN_STATUS, APPLICATION_DATE
    ) VALUES (
        v_loan_id, v_loan_no, p_customer_id, p_branch_id, p_loan_type,
        p_loan_amount, p_interest_rate, p_term_months, v_emi,
        p_loan_amount, 'Pending', SYSDATE
    );

    COMMIT;
    p_loan_number := v_loan_no;
    p_monthly_emi := v_emi;
    p_status := 'SUCCESS';
    p_message := 'Loan application ' || v_loan_no || ' submitted for approval. EMI: INR ' || v_emi;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_status := 'FAIL';
        p_message := 'Loan application failed: ' || SQLERRM;
END APPLY_FOR_LOAN;
/

-- 7. APPROVE_LOAN
CREATE OR REPLACE PROCEDURE APPROVE_LOAN (
    p_loan_number   IN  VARCHAR2,
    p_decision      IN  VARCHAR2, -- 'Approved' or 'Rejected'
    p_disburse_acc  IN  VARCHAR2, -- optional account to credit if approved
    p_status        OUT VARCHAR2,
    p_message       OUT VARCHAR2
) IS
    v_loan_id       NUMBER(10);
    v_amount        NUMBER(15,2);
    v_current_stat  VARCHAR2(20);
    v_acc_id        NUMBER(10);
    v_acc_bal       NUMBER(15,2);
    v_ref           VARCHAR2(30);
BEGIN
    SELECT LOAN_ID, LOAN_AMOUNT, LOAN_STATUS
    INTO v_loan_id, v_amount, v_current_stat
    FROM LOANS
    WHERE LOAN_NUMBER = p_loan_number
    FOR UPDATE;

    IF v_current_stat <> 'Pending' THEN
        p_status := 'ERROR';
        p_message := 'Loan is already in status ' || v_current_stat;
        ROLLBACK;
        RETURN;
    END IF;

    IF p_decision = 'Approved' THEN
        UPDATE LOANS 
        SET LOAN_STATUS = 'Approved', APPROVAL_DATE = SYSDATE 
        WHERE LOAN_ID = v_loan_id;

        -- If disbursement account provided, credit loan proceeds
        IF p_disburse_acc IS NOT NULL THEN
            SELECT ACCOUNT_ID, BALANCE 
            INTO v_acc_id, v_acc_bal 
            FROM BANK_ACCOUNTS 
            WHERE ACCOUNT_NUMBER = p_disburse_acc 
            FOR UPDATE;

            v_acc_bal := v_acc_bal + v_amount;
            UPDATE BANK_ACCOUNTS SET BALANCE = v_acc_bal WHERE ACCOUNT_ID = v_acc_id;

            v_ref := 'TXN-' || TO_CHAR(SYSDATE, 'YYYYMMDD') || '-' || LPAD(SEQ_TRANSACTIONS.NEXTVAL, 6, '0');
            INSERT INTO TRANSACTIONS (
                TRANSACTION_ID, TRANSACTION_REF, ACCOUNT_ID, TRANSACTION_TYPE,
                AMOUNT, BALANCE_AFTER, TRANSACTION_DATE, RELATED_ACCOUNT_ID,
                DESCRIPTION, TRANSACTION_STATUS
            ) VALUES (
                SEQ_TRANSACTIONS.CURRVAL, v_ref, v_acc_id, 'Loan_Disbursement',
                v_amount, v_acc_bal, SYSTIMESTAMP, NULL,
                'Disbursement for Loan ' || p_loan_number, 'Completed'
            );
            
            UPDATE LOANS SET LOAN_STATUS = 'Disbursed' WHERE LOAN_ID = v_loan_id;
        END IF;

        COMMIT;
        p_status := 'SUCCESS';
        p_message := 'Loan ' || p_loan_number || ' approved successfully.';
    ELSE
        UPDATE LOANS SET LOAN_STATUS = 'Rejected', APPROVAL_DATE = SYSDATE WHERE LOAN_ID = v_loan_id;
        COMMIT;
        p_status := 'SUCCESS';
        p_message := 'Loan ' || p_loan_number || ' was rejected.';
    END IF;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'Loan ' || p_loan_number || ' not found.';
    WHEN OTHERS THEN
        ROLLBACK;
        p_status := 'FAIL';
        p_message := 'Loan decision error: ' || SQLERRM;
END APPROVE_LOAN;
/

-- 8. PROCESS_LOAN_PAYMENT
CREATE OR REPLACE PROCEDURE PROCESS_LOAN_PAYMENT (
    p_loan_number       IN  VARCHAR2,
    p_amount            IN  NUMBER,
    p_payment_method    IN  VARCHAR2,
    p_payment_ref       OUT VARCHAR2,
    p_remaining_bal     OUT NUMBER,
    p_status            OUT VARCHAR2,
    p_message           OUT VARCHAR2
) IS
    v_loan_id       NUMBER(10);
    v_out_bal       NUMBER(15,2);
    v_rate          NUMBER(5,2);
    v_monthly_rate  NUMBER(10,6);
    v_interest_comp NUMBER(12,2);
    v_prin_comp     NUMBER(12,2);
    v_pay_ref       VARCHAR2(30);
    v_pay_id        NUMBER(10);
BEGIN
    IF p_amount <= 0 THEN
        p_status := 'ERROR';
        p_message := 'Payment amount must be greater than zero.';
        RETURN;
    END IF;

    SELECT LOAN_ID, OUTSTANDING_BALANCE, INTEREST_RATE
    INTO v_loan_id, v_out_bal, v_rate
    FROM LOANS
    WHERE LOAN_NUMBER = p_loan_number
    FOR UPDATE;

    IF v_out_bal <= 0 THEN
        p_status := 'ERROR';
        p_message := 'Loan is already fully repaid.';
        ROLLBACK;
        RETURN;
    END IF;

    v_monthly_rate := (v_rate / 12.0) / 100.0;
    v_interest_comp := ROUND(v_out_bal * v_monthly_rate, 2);

    IF p_amount < v_interest_comp THEN
        v_interest_comp := p_amount;
        v_prin_comp := 0;
    ELSE
        v_prin_comp := p_amount - v_interest_comp;
    END IF;

    IF v_prin_comp > v_out_bal THEN
        v_prin_comp := v_out_bal;
        v_out_bal := 0;
    ELSE
        v_out_bal := v_out_bal - v_prin_comp;
    END IF;

    SELECT SEQ_LOAN_PAYMENTS.NEXTVAL INTO v_pay_id FROM DUAL;
    v_pay_ref := 'LP' || TO_CHAR(SYSDATE, 'YYYYMMDD') || '-' || LPAD(v_pay_id, 5, '0');

    INSERT INTO LOAN_PAYMENTS (
        PAYMENT_ID, PAYMENT_REF, LOAN_ID, PAYMENT_AMOUNT,
        PRINCIPAL_COMPONENT, INTEREST_COMPONENT, PAYMENT_DATE,
        PAYMENT_METHOD, PAYMENT_STATUS
    ) VALUES (
        v_pay_id, v_pay_ref, v_loan_id, p_amount,
        v_prin_comp, v_interest_comp, SYSDATE,
        NVL(p_payment_method, 'Online Transfer'), 'Completed'
    );

    UPDATE LOANS 
    SET OUTSTANDING_BALANCE = v_out_bal,
        LOAN_STATUS = CASE WHEN v_out_bal = 0 THEN 'Closed' ELSE LOAN_STATUS END
    WHERE LOAN_ID = v_loan_id;

    COMMIT;
    p_payment_ref := v_pay_ref;
    p_remaining_bal := v_out_bal;
    p_status := 'SUCCESS';
    p_message := 'Payment recorded. Principal: INR ' || v_prin_comp || ', Interest: INR ' || v_interest_comp || '. Remaining: INR ' || v_out_bal;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'Loan number ' || p_loan_number || ' not found.';
    WHEN OTHERS THEN
        ROLLBACK;
        p_status := 'FAIL';
        p_message := 'Payment processing failed: ' || SQLERRM;
END PROCESS_LOAN_PAYMENT;
/

-- 9. GENERATE_ACCOUNT_STATEMENT (Using Explicit Cursor and DBMS_OUTPUT)
CREATE OR REPLACE PROCEDURE GENERATE_ACCOUNT_STATEMENT (
    p_account_number IN VARCHAR2,
    p_start_date     IN DATE,
    p_end_date       IN DATE
) IS
    v_acc_id        NUMBER(10);
    v_cust_name     VARCHAR2(100);
    v_balance       NUMBER(15,2);
    
    CURSOR c_txns IS
        SELECT TRANSACTION_REF, TRANSACTION_DATE, TRANSACTION_TYPE, AMOUNT, BALANCE_AFTER, DESCRIPTION
        FROM TRANSACTIONS
        WHERE ACCOUNT_ID = v_acc_id
          AND TRUNC(CAST(TRANSACTION_DATE AS DATE)) BETWEEN p_start_date AND p_end_date
        ORDER BY TRANSACTION_DATE ASC;
        
    v_rec c_txns%ROWTYPE;
BEGIN
    SELECT a.ACCOUNT_ID, c.FIRST_NAME || ' ' || c.LAST_NAME, a.BALANCE
    INTO v_acc_id, v_cust_name, v_balance
    FROM BANK_ACCOUNTS a
    JOIN CUSTOMERS c ON a.CUSTOMER_ID = c.CUSTOMER_ID
    WHERE a.ACCOUNT_NUMBER = p_account_number;

    DBMS_OUTPUT.PUT_LINE('========================================================================');
    DBMS_OUTPUT.PUT_LINE('                     SMART BANK ACCOUNT STATEMENT                       ');
    DBMS_OUTPUT.PUT_LINE('========================================================================');
    DBMS_OUTPUT.PUT_LINE('Account Number : ' || p_account_number);
    DBMS_OUTPUT.PUT_LINE('Customer Name  : ' || v_cust_name);
    DBMS_OUTPUT.PUT_LINE('Period         : ' || TO_CHAR(p_start_date, 'DD-Mon-YYYY') || ' to ' || TO_CHAR(p_end_date, 'DD-Mon-YYYY'));
    DBMS_OUTPUT.PUT_LINE('Current Balance: INR ' || TO_CHAR(v_balance, '999,999,990.00'));
    DBMS_OUTPUT.PUT_LINE('------------------------------------------------------------------------');
    DBMS_OUTPUT.PUT_LINE(RPAD('REF #', 20) || RPAD('DATE', 12) || RPAD('TYPE', 16) || RPAD('AMOUNT', 14) || 'BALANCE');
    DBMS_OUTPUT.PUT_LINE('------------------------------------------------------------------------');

    OPEN c_txns;
    LOOP
        FETCH c_txns INTO v_rec;
        EXIT WHEN c_txns%NOTFOUND;
        DBMS_OUTPUT.PUT_LINE(
            RPAD(v_rec.TRANSACTION_REF, 20) ||
            RPAD(TO_CHAR(v_rec.TRANSACTION_DATE, 'DD-Mon-YY'), 12) ||
            RPAD(v_rec.TRANSACTION_TYPE, 16) ||
            RPAD(TO_CHAR(v_rec.AMOUNT, '999,990.00'), 14) ||
            TO_CHAR(v_rec.BALANCE_AFTER, '999,999,990.00')
        );
    END LOOP;
    
    DBMS_OUTPUT.PUT_LINE('------------------------------------------------------------------------');
    DBMS_OUTPUT.PUT_LINE('Total transactions fetched: ' || c_txns%ROWCOUNT);
    CLOSE c_txns;
    DBMS_OUTPUT.PUT_LINE('========================================================================');

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('Error: Account ' || p_account_number || ' not found.');
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error generating statement: ' || SQLERRM);
END GENERATE_ACCOUNT_STATEMENT;
/

-- 10. CLOSE_BANK_ACCOUNT
CREATE OR REPLACE PROCEDURE CLOSE_BANK_ACCOUNT (
    p_account_number IN  VARCHAR2,
    p_reason         IN  VARCHAR2,
    p_status         OUT VARCHAR2,
    p_message        OUT VARCHAR2
) IS
    v_acc_id    NUMBER(10);
    v_balance   NUMBER(15,2);
    v_status    VARCHAR2(20);
BEGIN
    SELECT ACCOUNT_ID, BALANCE, ACCOUNT_STATUS
    INTO v_acc_id, v_balance, v_status
    FROM BANK_ACCOUNTS
    WHERE ACCOUNT_NUMBER = p_account_number
    FOR UPDATE;

    IF v_status = 'Closed' THEN
        p_status := 'ERROR';
        p_message := 'Account is already closed.';
        ROLLBACK;
        RETURN;
    END IF;

    IF v_balance > 0 THEN
        p_status := 'ERROR';
        p_message := 'Cannot close account with positive balance (INR ' || v_balance || '). Please withdraw or transfer funds first.';
        ROLLBACK;
        RETURN;
    END IF;

    UPDATE BANK_ACCOUNTS 
    SET ACCOUNT_STATUS = 'Closed', UPDATED_AT = SYSDATE 
    WHERE ACCOUNT_ID = v_acc_id;

    COMMIT;
    p_status := 'SUCCESS';
    p_message := 'Account ' || p_account_number || ' closed successfully. Reason: ' || NVL(p_reason, 'Customer Request');

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'Account ' || p_account_number || ' not found.';
    WHEN OTHERS THEN
        ROLLBACK;
        p_status := 'FAIL';
        p_message := 'Error closing account: ' || SQLERRM;
END CLOSE_BANK_ACCOUNT;
/

PROMPT [OK] All 10 stored procedures compiled successfully.
