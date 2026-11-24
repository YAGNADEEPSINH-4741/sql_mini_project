-- ============================================================================
-- MASTER SCRIPT: RUN_ALL.SQL
-- PROJECT: Smart Banking Management System
-- PURPOSE: Master SQL*Plus execution script deploying complete database objects
--          in exact dependency order with spooling and verification summary.
-- USAGE IN SQL*PLUS:
--   sqlplus root/root@ORCLA @RUN_ALL.SQL
-- ORACLE DB COMPATIBILITY: Oracle 10g, 11g, 12c, 19c, 21c, 23ai
-- ============================================================================

-- SQL*Plus Formatting and Environment Directives
SET SERVEROUTPUT ON SIZE 1000000;
SET FEEDBACK ON;
SET VERIFY OFF;
SET ECHO OFF;
SET TERMOUT ON;
SET LINESIZE 350;
SET PAGESIZE 50;
SET TIMING ON;

-- Spool all output to a persistent log file for verification and academic records
SPOOL SMART_BANKING_DEPLOYMENT.LOG;

PROMPT ==============================================================================
PROMPT   ==========================================================================
PROMPT            SMART BANKING MANAGEMENT SYSTEM - MASTER DATABASE INSTALLER
PROMPT                           ORACLE SQL & PL/SQL MINI PROJECT
PROMPT   ==========================================================================
PROMPT ==============================================================================
PROMPT Starting deployment at:
SELECT TO_CHAR(SYSDATE, 'YYYY-MM-DD HH24:MI:SS') AS START_TIME FROM DUAL;
PROMPT ==============================================================================

-- STEP 1: CLEANUP PREVIOUS INSTALLATION
PROMPT >>> Step 1 of 12: Dropping existing schema objects...
@01_schema/01_cleanup.sql;

-- STEP 2: CREATE CORE NORMALIZED TABLES
PROMPT >>> Step 2 of 12: Creating 11 normalized database tables...
@01_schema/02_create_tables.sql;

-- STEP 3: APPLY CONSTRAINTS
PROMPT >>> Step 3 of 12: Applying Primary, Foreign, Unique, and Check constraints...
@01_schema/03_constraints.sql;

-- STEP 4: CREATE SEQUENCES
PROMPT >>> Step 4 of 12: Creating surrogate key sequences...
@01_schema/04_sequences.sql;

-- STEP 5: CREATE B-TREE INDEXES
PROMPT >>> Step 5 of 12: Creating performance B-Tree indexes...
@01_schema/05_indexes.sql;

-- STEP 6: SEED REALISTIC SAMPLE DATA
PROMPT >>> Step 6 of 12: Populating branches, customers, accounts, loans, and admin...
@02_sample_data/06_seed_data.sql;

-- STEP 7: CREATE RELATIONAL & MATERIALIZED VIEWS
PROMPT >>> Step 7 of 12: Compiling views, materialized view, and synonyms...
@03_views/07_views.sql;
@03_views/08_materialized_views_synonyms.sql;

-- STEP 8: USER-DEFINED FUNCTIONS
PROMPT >>> Step 8 of 12: Compiling user-defined functions...
@04_functions/09_functions.sql;

-- STEP 9: STORED PROCEDURES
PROMPT >>> Step 9 of 12: Compiling banking & loan stored procedures...
@05_procedures/10_procedures.sql;

-- STEP 10: DATABASE TRIGGERS
PROMPT >>> Step 10 of 12: Compiling row & statement triggers for validation & audit...
@06_triggers/11_triggers.sql;

-- STEP 11: PL/SQL PACKAGES
PROMPT >>> Step 11 of 12: Compiling BANKING_PACKAGE and LOAN_PACKAGE specifications & bodies...
@07_packages/12_banking_package.sql;
@07_packages/13_loan_package.sql;

-- STEP 12: CURSORS & ADVANCED PL/SQL DEMONSTRATION
PROMPT >>> Step 12 of 12: Executing cursors and advanced PL/SQL showcase...
@08_cursors/14_cursors_demo.sql;
@09_advanced_plsql/15_advanced_plsql.sql;
@10_queries/16_sql_concepts_demonstration.sql;

-- STEP 13: COMPREHENSIVE TEST SUITE
PROMPT ==============================================================================
PROMPT >>> Running Comprehensive 12-Point Test Suite...
PROMPT ==============================================================================
@11_test_scripts/17_comprehensive_test_suite.sql;

PROMPT ==============================================================================
PROMPT   DEPLOYMENT AND VERIFICATION SUMMARY
PROMPT ==============================================================================
SELECT 'TABLES' AS OBJECT_TYPE, COUNT(*) AS TOTAL_COUNT FROM USER_TABLES
UNION ALL
SELECT 'VIEWS', COUNT(*) FROM USER_VIEWS
UNION ALL
SELECT 'INDEXES', COUNT(*) FROM USER_INDEXES WHERE INDEX_TYPE = 'NORMAL'
UNION ALL
SELECT 'SEQUENCES', COUNT(*) FROM USER_SEQUENCES
UNION ALL
SELECT 'PROCEDURES', COUNT(*) FROM USER_PROCEDURES WHERE OBJECT_TYPE = 'PROCEDURE'
UNION ALL
SELECT 'FUNCTIONS', COUNT(*) FROM USER_PROCEDURES WHERE OBJECT_TYPE = 'FUNCTION'
UNION ALL
SELECT 'PACKAGES', COUNT(*) FROM USER_OBJECTS WHERE OBJECT_TYPE = 'PACKAGE'
UNION ALL
SELECT 'TRIGGERS', COUNT(*) FROM USER_TRIGGERS;

PROMPT ==============================================================================
PROMPT Finished deployment at:
SELECT TO_CHAR(SYSDATE, 'YYYY-MM-DD HH24:MI:SS') AS END_TIME FROM DUAL;
PROMPT Log successfully written to: SMART_BANKING_DEPLOYMENT.LOG
PROMPT ==============================================================================

SPOOL OFF;
