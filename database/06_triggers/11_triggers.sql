-- ============================================================================
-- SCRIPT: 11_triggers.sql
-- PROJECT: Smart Banking Management System
-- PURPOSE: Row-level and Statement-level Triggers for Automated Timestamping,
--          Data Validation, and Comprehensive Audit Trail Logging.
-- ORACLE DB COMPATIBILITY: Oracle 10g, 11g, 12c, 19c, 21c, 23ai
-- ============================================================================

PROMPT ====================================================================
PROMPT   Executing 11_triggers.sql - Creating Database Triggers
PROMPT ====================================================================

-- 1. BEFORE INSERT TRIGGER ON CUSTOMERS
-- Automatically populates primary key via sequence if null and sets created timestamp
CREATE OR REPLACE TRIGGER TRG_CUSTOMERS_BIU
BEFORE INSERT OR UPDATE ON CUSTOMERS
FOR EACH ROW
BEGIN
    IF INSERTING THEN
        IF :NEW.CUSTOMER_ID IS NULL THEN
            SELECT SEQ_CUSTOMERS.NEXTVAL INTO :NEW.CUSTOMER_ID FROM DUAL;
        END IF;
        :NEW.CREATED_AT := SYSDATE;
        :NEW.UPDATED_AT := SYSDATE;
    ELSIF UPDATING THEN
        :NEW.UPDATED_AT := SYSDATE;
    END IF;
END;
/

-- 2. BEFORE UPDATE TRIGGER ON BANK_ACCOUNTS
-- Automatically updates the UPDATED_AT timestamp on any account modifications
CREATE OR REPLACE TRIGGER TRG_ACCOUNTS_BIU
BEFORE INSERT OR UPDATE ON BANK_ACCOUNTS
FOR EACH ROW
BEGIN
    IF INSERTING THEN
        IF :NEW.ACCOUNT_ID IS NULL THEN
            SELECT SEQ_ACCOUNTS.NEXTVAL INTO :NEW.ACCOUNT_ID FROM DUAL;
        END IF;
        :NEW.CREATED_AT := SYSDATE;
        :NEW.UPDATED_AT := SYSDATE;
    ELSIF UPDATING THEN
        :NEW.UPDATED_AT := SYSDATE;
    END IF;
END;
/

-- 3. BEFORE INSERT TRIGGER FOR ACCOUNT VALIDATION (Data Validation Guard)
-- Ensures account creation satisfies minimum balance for the specific account type
CREATE OR REPLACE TRIGGER TRG_VALIDATE_ACCOUNT_MIN_BAL
BEFORE INSERT ON BANK_ACCOUNTS
FOR EACH ROW
DECLARE
    v_min_bal NUMBER(12,2);
BEGIN
    SELECT MIN_BALANCE INTO v_min_bal 
    FROM ACCOUNT_TYPES 
    WHERE TYPE_ID = :NEW.TYPE_ID;

    IF :NEW.BALANCE < v_min_bal THEN
        RAISE_APPLICATION_ERROR(-20001, 'Account creation rejected: Balance INR ' || :NEW.BALANCE || ' is below required minimum of INR ' || v_min_bal);
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20002, 'Invalid Account Type ID: ' || :NEW.TYPE_ID);
END;
/

-- 4. AFTER UPDATE TRIGGER ON BANK_ACCOUNTS (Row-Level Audit Logging)
-- Logs every change in account balance or status to the AUDIT_LOGS table
CREATE OR REPLACE TRIGGER TRG_ACCOUNTS_AUDIT
AFTER UPDATE ON BANK_ACCOUNTS
FOR EACH ROW
BEGIN
    -- Log balance updates
    IF :OLD.BALANCE <> :NEW.BALANCE THEN
        INSERT INTO AUDIT_LOGS (
            LOG_ID, TABLE_NAME, OPERATION_TYPE, RECORD_ID,
            OLD_VALUE, NEW_VALUE, CHANGED_BY, CHANGED_AT, CLIENT_IP
        ) VALUES (
            SEQ_AUDIT_LOGS.NEXTVAL, 'BANK_ACCOUNTS', 'UPDATE',
            TO_CHAR(:NEW.ACCOUNT_ID),
            'BALANCE=' || TO_CHAR(:OLD.BALANCE),
            'BALANCE=' || TO_CHAR(:NEW.BALANCE),
            USER, SYSTIMESTAMP, '127.0.0.1'
        );
    END IF;

    -- Log status changes (e.g. Active -> Dormant / Frozen / Closed)
    IF :OLD.ACCOUNT_STATUS <> :NEW.ACCOUNT_STATUS THEN
        INSERT INTO AUDIT_LOGS (
            LOG_ID, TABLE_NAME, OPERATION_TYPE, RECORD_ID,
            OLD_VALUE, NEW_VALUE, CHANGED_BY, CHANGED_AT, CLIENT_IP
        ) VALUES (
            SEQ_AUDIT_LOGS.NEXTVAL, 'BANK_ACCOUNTS', 'UPDATE',
            TO_CHAR(:NEW.ACCOUNT_ID),
            'STATUS=' || :OLD.ACCOUNT_STATUS,
            'STATUS=' || :NEW.ACCOUNT_STATUS,
            USER, SYSTIMESTAMP, '127.0.0.1'
        );
    END IF;
END;
/

-- 5. AFTER INSERT TRIGGER ON TRANSACTIONS (Row-Level Audit Logging)
-- Records every financial transaction in the immutable AUDIT_LOGS
CREATE OR REPLACE TRIGGER TRG_TRANSACTIONS_AUDIT
AFTER INSERT ON TRANSACTIONS
FOR EACH ROW
BEGIN
    INSERT INTO AUDIT_LOGS (
        LOG_ID, TABLE_NAME, OPERATION_TYPE, RECORD_ID,
        OLD_VALUE, NEW_VALUE, CHANGED_BY, CHANGED_AT, CLIENT_IP
    ) VALUES (
        SEQ_AUDIT_LOGS.NEXTVAL, 'TRANSACTIONS', 'INSERT',
        TO_CHAR(:NEW.TRANSACTION_ID),
        NULL,
        'REF=' || :NEW.TRANSACTION_REF || ', ACC=' || TO_CHAR(:NEW.ACCOUNT_ID) || 
        ', TYPE=' || :NEW.TRANSACTION_TYPE || ', AMOUNT=' || TO_CHAR(:NEW.AMOUNT),
        USER, SYSTIMESTAMP, '127.0.0.1'
    );
END;
/

-- 6. AFTER DELETE TRIGGER ON BENEFICIARIES (Audit Deleted Records)
CREATE OR REPLACE TRIGGER TRG_AUDIT_DELETE
AFTER DELETE ON BENEFICIARIES
FOR EACH ROW
BEGIN
    INSERT INTO AUDIT_LOGS (
        LOG_ID, TABLE_NAME, OPERATION_TYPE, RECORD_ID,
        OLD_VALUE, NEW_VALUE, CHANGED_BY, CHANGED_AT, CLIENT_IP
    ) VALUES (
        SEQ_AUDIT_LOGS.NEXTVAL, 'BENEFICIARIES', 'DELETE',
        TO_CHAR(:OLD.BENEFICIARY_ID),
        'NAME=' || :OLD.BENEFICIARY_NAME || ', ACC=' || :OLD.BENEFICIARY_ACCOUNT || ', BANK=' || :OLD.BANK_NAME,
        NULL,
        USER, SYSTIMESTAMP, '127.0.0.1'
    );
END;
/

-- 7. STATEMENT-LEVEL TRIGGER DEMONSTRATION
-- Fires once per SQL statement (e.g. bulk transaction inserts) to log batch execution
CREATE OR REPLACE TRIGGER TRG_STMT_TRANSACTION_AUDIT
AFTER INSERT ON TRANSACTIONS
BEGIN
    DBMS_OUTPUT.PUT_LINE('STATEMENT TRIGGER: A batch of transactions was processed at ' || TO_CHAR(SYSDATE, 'YYYY-MM-DD HH24:MI:SS'));
END;
/

PROMPT [OK] All 7 database triggers compiled successfully.
