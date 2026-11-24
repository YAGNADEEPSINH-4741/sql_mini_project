@echo off
setlocal EnableDelayedExpansion

title Smart Banking Management System - Oracle Database Setup
color 0B
cls

echo ==============================================================================
echo       SMART BANKING MANAGEMENT SYSTEM - AUTOMATED SQL*PLUS INSTALLER
echo                        Oracle SQL & PL/SQL Mini Project
echo ==============================================================================
echo.

:: Check for Administrator elevation
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Requesting Administrator privileges required by Oracle 10g client on Windows...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

set "ORACLE_HOME=C:\oracle\product\10.2.0\db_1"
set "ORACLE_SID=orclA"
set "PATH=%ORACLE_HOME%\bin;%PATH%"

cd /d "%~dp0"

echo [*] Target Database Service : ORCLA (127.0.0.1:1521)
echo [*] Database User           : root
echo [*] Executing Master Script : RUN_ALL.SQL
echo.
echo ------------------------------------------------------------------------------
echo Launching SQL*Plus... Please wait while all tables, procedures, triggers, 
echo packages, and test cases are deployed and verified.
echo ------------------------------------------------------------------------------
echo.

sqlplus root/root@ORCLA @"%~dp0RUN_ALL.SQL"

echo.
echo ==============================================================================
echo   DEPLOYMENT FINISHED!
echo   Execution log saved to: %~dp0SMART_BANKING_DEPLOYMENT.LOG
echo ==============================================================================
echo.
pause
