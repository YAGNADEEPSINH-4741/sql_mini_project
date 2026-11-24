<?php
/**
 * UNIFIED BACKEND API ROUTER
 * Handles all AJAX endpoints for Dashboard, Customers, Accounts, Transactions,
 * Loans, Beneficiaries, Reports, and Audit Logs.
 * All financial actions invoke Oracle Stored Procedures and Packages.
 */

header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With");
header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

require_once __DIR__ . '/config/database.php';
require_once __DIR__ . '/config/oracle_bridge.php';
require_once __DIR__ . '/includes/auth.php';
require_once __DIR__ . '/includes/response.php';

$action = $_GET['action'] ?? $_POST['action'] ?? '';
$input = getJsonInput();
$db = Database::getInstance();

// Public Action: Login
if ($action === 'login') {
    $username = trim($input['username'] ?? '');
    $password = trim($input['password'] ?? '');

    if (empty($username) || empty($password)) {
        jsonError('Please provide both username and password.');
    }

    if (Auth::login($username, $password)) {
        jsonSuccess(['user' => Auth::user()], 'Login successful.');
    } else {
        jsonError('Invalid username or password.', 401);
    }
}

// Public Action: Logout
if ($action === 'logout') {
    Auth::logout();
    jsonSuccess([], 'Logged out successfully.');
}

// Public Action: Auth Check
if ($action === 'check_auth') {
    if (Auth::check()) {
        jsonSuccess(['user' => Auth::user(), 'driver' => $db->getDriver()]);
    } else {
        jsonError('Not authenticated.', 401);
    }
}

// Protected Routes Guard
if (!Auth::check()) {
    jsonError('Authentication required to access this resource.', 401);
}

// ----------------------------------------------------------------------------
// DASHBOARD METRICS & CHARTS
// ----------------------------------------------------------------------------
if ($action === 'dashboard_summary') {
    try {
        $customers = $db->query("SELECT * FROM CUSTOMERS");
        $accounts = $db->query("SELECT * FROM BANK_ACCOUNTS");
        $txns = $db->query("SELECT * FROM TRANSACTIONS");
        $loans = $db->query("SELECT * FROM LOANS");

        $totalCustomers = count($customers);
        $totalAccounts = count($accounts);
        
        $totalDeposits = 0;
        $totalWithdrawals = 0;
        foreach ($txns as $t) {
            $amt = (float)$t['AMOUNT'];
            $type = $t['TRANSACTION_TYPE'];
            if ($type === 'Deposit' || strpos($type, 'Credit') !== false) {
                $totalDeposits += $amt;
            } elseif ($type === 'Withdrawal' || strpos($type, 'Debit') !== false) {
                $totalWithdrawals += $amt;
            }
        }

        $activeLoansCount = 0;
        $totalLoanPortfolio = 0;
        foreach ($loans as $l) {
            if (in_array($l['LOAN_STATUS'], ['Approved', 'Disbursed'])) {
                $activeLoansCount++;
                $totalLoanPortfolio += (float)$l['OUTSTANDING_BALANCE'];
            }
        }

        // Account Types Distribution
        $accTypeCount = ['Savings' => 0, 'Current' => 0, 'Fixed Deposit' => 0, 'Salary' => 0];
        foreach ($accounts as $a) {
            $tid = (int)$a['TYPE_ID'];
            if ($tid === 1 || $tid === 2) $accTypeCount['Savings']++;
            elseif ($tid === 3) $accTypeCount['Current']++;
            elseif ($tid === 4) $accTypeCount['Fixed Deposit']++;
            elseif ($tid === 5) $accTypeCount['Salary']++;
        }

        // Monthly Trend Simulation
        $monthlyStats = [
            'labels' => ['Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov'],
            'deposits' => [125000, 240000, 310000, 480000, 520000, round($totalDeposits / 2, 2)],
            'withdrawals' => [45000, 80000, 110000, 140000, 195000, round($totalWithdrawals / 2, 2)]
        ];

        // Recent 5 transactions
        $recentTxns = array_slice($db->query("SELECT * FROM TRANSACTION_HISTORY_VIEW"), 0, 8);

        jsonSuccess([
            'metrics' => [
                'total_customers' => $totalCustomers,
                'total_accounts' => $totalAccounts,
                'total_deposits' => $totalDeposits,
                'total_withdrawals' => $totalWithdrawals,
                'total_transactions' => count($txns),
                'active_loans' => $activeLoansCount,
                'loan_amount' => $totalLoanPortfolio,
                'oracle_driver' => $db->getDriver()
            ],
            'charts' => [
                'account_types' => $accTypeCount,
                'monthly_stats' => $monthlyStats
            ],
            'recent_transactions' => $recentTxns
        ]);
    } catch (Exception $e) {
        jsonError($e->getMessage());
    }
}

// ----------------------------------------------------------------------------
// CUSTOMER MANAGEMENT
// ----------------------------------------------------------------------------
if ($action === 'list_customers') {
    try {
        $customers = $db->query("SELECT * FROM CUSTOMERS ORDER BY CUSTOMER_ID DESC");
        jsonSuccess($customers);
    } catch (Exception $e) {
        jsonError($e->getMessage());
    }
}

if ($action === 'create_customer') {
    $first = trim($input['first_name'] ?? '');
    $last = trim($input['last_name'] ?? '');
    $email = trim($input['email'] ?? '');
    $phone = trim($input['phone'] ?? '');
    $dob = trim($input['dob'] ?? '1995-01-01');
    $gender = trim($input['gender'] ?? 'Male');
    $address = trim($input['address'] ?? '');
    $city = trim($input['city'] ?? '');
    $state = trim($input['state'] ?? '');
    $pincode = trim($input['pincode'] ?? '');

    if (empty($first) || empty($last) || empty($email) || empty($phone)) {
        jsonError('First name, last name, email, and phone are mandatory.');
    }

    try {
        // Fallback for simulation / direct insert
        $bridge = OracleBridge::getInstance();
        $data = $bridge->getData('CUSTOMERS');
        $newId = 1000 + count($data) + 1;
        $row = [
            'CUSTOMER_ID' => $newId,
            'FIRST_NAME' => $first,
            'LAST_NAME' => $last,
            'EMAIL' => $email,
            'PHONE' => $phone,
            'DATE_OF_BIRTH' => $dob,
            'GENDER' => $gender,
            'ADDRESS' => $address,
            'CITY' => $city,
            'STATE' => $state,
            'PIN_CODE' => $pincode,
            'KYC_STATUS' => 'Verified',
            'CREATED_AT' => date('Y-m-d')
        ];
        
        // Save to bridge data store
        $ref = new ReflectionProperty('OracleBridge', 'data');
        $ref->setAccessible(true);
        $fullData = $ref->getValue($bridge);
        $fullData['CUSTOMERS'][] = $row;
        $ref->setValue($bridge, $fullData);
        $saveMethod = new ReflectionMethod('OracleBridge', 'save');
        $saveMethod->setAccessible(true);
        $saveMethod->invoke($bridge);

        jsonSuccess($row, "Customer {$first} {$last} registered successfully.");
    } catch (Exception $e) {
        jsonError($e->getMessage());
    }
}

// ----------------------------------------------------------------------------
// ACCOUNT MANAGEMENT
// ----------------------------------------------------------------------------
if ($action === 'list_accounts') {
    try {
        $accounts = $db->query("SELECT * FROM CUSTOMER_ACCOUNT_VIEW ORDER BY ACCOUNT_ID DESC");
        jsonSuccess($accounts);
    } catch (Exception $e) {
        jsonError($e->getMessage());
    }
}

if ($action === 'create_account') {
    $custId = (int)($input['customer_id'] ?? 0);
    $branchId = (int)($input['branch_id'] ?? 101);
    $typeId = (int)($input['type_id'] ?? 1);
    $initDeposit = (float)($input['initial_deposit'] ?? 1000);

    if ($custId <= 0) {
        jsonError('Valid customer must be selected.');
    }

    try {
        $binds = [
            'p_customer_id'     => ['value' => $custId],
            'p_branch_id'       => ['value' => $branchId],
            'p_type_id'         => ['value' => $typeId],
            'p_initial_deposit' => ['value' => $initDeposit],
            'p_account_number'  => ['value' => null, 'length' => 20],
            'p_status'          => ['value' => null, 'length' => 20],
            'p_message'         => ['value' => null, 'length' => 255]
        ];

        $db->callProcedure('CREATE_BANK_ACCOUNT', $binds);

        if ($binds['p_status']['value'] === 'SUCCESS') {
            jsonSuccess([
                'account_number' => $binds['p_account_number']['value']
            ], $binds['p_message']['value']);
        } else {
            jsonError($binds['p_message']['value']);
        }
    } catch (Exception $e) {
        jsonError($e->getMessage());
    }
}

// ----------------------------------------------------------------------------
// TRANSACTION OPERATIONS (PROCEDURE DRIVEN)
// ----------------------------------------------------------------------------
if ($action === 'list_transactions') {
    try {
        $txns = $db->query("SELECT * FROM TRANSACTION_HISTORY_VIEW");
        jsonSuccess($txns);
    } catch (Exception $e) {
        jsonError($e->getMessage());
    }
}

if ($action === 'deposit') {
    $accNo = trim($input['account_number'] ?? '');
    $amount = (float)($input['amount'] ?? 0);
    $desc = trim($input['description'] ?? 'Cash Deposit');

    if (empty($accNo) || $amount <= 0) {
        jsonError('Valid account number and positive amount required.');
    }

    try {
        $binds = [
            'p_account_number' => ['value' => $accNo],
            'p_amount'         => ['value' => $amount],
            'p_description'    => ['value' => $desc],
            'p_txn_ref'        => ['value' => null, 'length' => 30],
            'p_new_balance'    => ['value' => null],
            'p_status'         => ['value' => null, 'length' => 20],
            'p_message'        => ['value' => null, 'length' => 255]
        ];

        $db->callProcedure('BANKING_PACKAGE.DEPOSIT', $binds);

        if ($binds['p_status']['value'] === 'SUCCESS') {
            jsonSuccess([
                'reference' => $binds['p_txn_ref']['value'],
                'new_balance' => $binds['p_new_balance']['value']
            ], $binds['p_message']['value']);
        } else {
            jsonError($binds['p_message']['value']);
        }
    } catch (Exception $e) {
        jsonError($e->getMessage());
    }
}

if ($action === 'withdraw') {
    $accNo = trim($input['account_number'] ?? '');
    $amount = (float)($input['amount'] ?? 0);
    $desc = trim($input['description'] ?? 'Cash Withdrawal');

    if (empty($accNo) || $amount <= 0) {
        jsonError('Valid account number and positive amount required.');
    }

    try {
        $binds = [
            'p_account_number' => ['value' => $accNo],
            'p_amount'         => ['value' => $amount],
            'p_description'    => ['value' => $desc],
            'p_txn_ref'        => ['value' => null, 'length' => 30],
            'p_new_balance'    => ['value' => null],
            'p_status'         => ['value' => null, 'length' => 20],
            'p_message'        => ['value' => null, 'length' => 255]
        ];

        $db->callProcedure('BANKING_PACKAGE.WITHDRAW', $binds);

        if ($binds['p_status']['value'] === 'SUCCESS') {
            jsonSuccess([
                'reference' => $binds['p_txn_ref']['value'],
                'new_balance' => $binds['p_new_balance']['value']
            ], $binds['p_message']['value']);
        } else {
            jsonError($binds['p_message']['value']);
        }
    } catch (Exception $e) {
        jsonError($e->getMessage());
    }
}

if ($action === 'transfer') {
    $senderAcc = trim($input['sender_account'] ?? '');
    $receiverAcc = trim($input['receiver_account'] ?? '');
    $amount = (float)($input['amount'] ?? 0);
    $desc = trim($input['description'] ?? 'Fund Transfer');

    if (empty($senderAcc) || empty($receiverAcc) || $amount <= 0) {
        jsonError('Sender account, receiver account, and positive amount are required.');
    }

    try {
        $binds = [
            'p_sender_acc_no'   => ['value' => $senderAcc],
            'p_receiver_acc_no' => ['value' => $receiverAcc],
            'p_amount'          => ['value' => $amount],
            'p_description'     => ['value' => $desc],
            'p_txn_ref'         => ['value' => null, 'length' => 30],
            'p_sender_balance'  => ['value' => null],
            'p_status'          => ['value' => null, 'length' => 20],
            'p_message'         => ['value' => null, 'length' => 255]
        ];

        $db->callProcedure('BANKING_PACKAGE.TRANSFER', $binds);

        if ($binds['p_status']['value'] === 'SUCCESS') {
            jsonSuccess([
                'reference' => $binds['p_txn_ref']['value'],
                'sender_balance' => $binds['p_sender_balance']['value']
            ], $binds['p_message']['value']);
        } else {
            jsonError($binds['p_message']['value']);
        }
    } catch (Exception $e) {
        jsonError($e->getMessage());
    }
}

// ----------------------------------------------------------------------------
// LOAN MANAGEMENT (PROCEDURE DRIVEN)
// ----------------------------------------------------------------------------
if ($action === 'list_loans') {
    try {
        $loans = $db->query("SELECT * FROM LOAN_DETAILS_VIEW");
        jsonSuccess($loans);
    } catch (Exception $e) {
        jsonError($e->getMessage());
    }
}

if ($action === 'apply_loan') {
    $custId = (int)($input['customer_id'] ?? 0);
    $branchId = (int)($input['branch_id'] ?? 101);
    $loanType = trim($input['loan_type'] ?? 'Personal Loan');
    $amount = (float)($input['loan_amount'] ?? 0);
    $rate = (float)($input['interest_rate'] ?? 10.5);
    $term = (int)($input['term_months'] ?? 12);

    if ($custId <= 0 || $amount <= 0 || $term <= 0) {
        jsonError('Valid customer, loan amount, and term months are required.');
    }

    try {
        $binds = [
            'p_customer_id'   => ['value' => $custId],
            'p_branch_id'     => ['value' => $branchId],
            'p_loan_type'     => ['value' => $loanType],
            'p_loan_amount'   => ['value' => $amount],
            'p_interest_rate' => ['value' => $rate],
            'p_term_months'   => ['value' => $term],
            'p_loan_number'   => ['value' => null, 'length' => 20],
            'p_monthly_emi'   => ['value' => null],
            'p_status'        => ['value' => null, 'length' => 20],
            'p_message'       => ['value' => null, 'length' => 255]
        ];

        $db->callProcedure('LOAN_PACKAGE.APPLY_LOAN', $binds);

        if ($binds['p_status']['value'] === 'SUCCESS') {
            jsonSuccess([
                'loan_number' => $binds['p_loan_number']['value'],
                'monthly_emi' => $binds['p_monthly_emi']['value']
            ], $binds['p_message']['value']);
        } else {
            jsonError($binds['p_message']['value']);
        }
    } catch (Exception $e) {
        jsonError($e->getMessage());
    }
}

if ($action === 'decide_loan') {
    $loanNo = trim($input['loan_number'] ?? '');
    $decision = trim($input['decision'] ?? 'Approved');
    $disburseAcc = trim($input['disburse_account'] ?? '');

    try {
        $binds = [
            'p_loan_number'  => ['value' => $loanNo],
            'p_decision'     => ['value' => $decision],
            'p_disburse_acc' => ['value' => !empty($disburseAcc) ? $disburseAcc : null],
            'p_status'       => ['value' => null, 'length' => 20],
            'p_message'      => ['value' => null, 'length' => 255]
        ];

        $db->callProcedure('LOAN_PACKAGE.APPROVE_LOAN_REQUEST', $binds);

        if ($binds['p_status']['value'] === 'SUCCESS') {
            jsonSuccess([], $binds['p_message']['value']);
        } else {
            jsonError($binds['p_message']['value']);
        }
    } catch (Exception $e) {
        jsonError($e->getMessage());
    }
}

if ($action === 'loan_payment') {
    $loanNo = trim($input['loan_number'] ?? '');
    $amount = (float)($input['amount'] ?? 0);
    $method = trim($input['method'] ?? 'Online Transfer');

    if (empty($loanNo) || $amount <= 0) {
        jsonError('Valid loan number and positive payment amount required.');
    }

    try {
        $binds = [
            'p_loan_number'    => ['value' => $loanNo],
            'p_amount'         => ['value' => $amount],
            'p_payment_method' => ['value' => $method],
            'p_payment_ref'    => ['value' => null, 'length' => 30],
            'p_remaining_bal'  => ['value' => null],
            'p_status'         => ['value' => null, 'length' => 20],
            'p_message'        => ['value' => null, 'length' => 255]
        ];

        $db->callProcedure('LOAN_PACKAGE.MAKE_PAYMENT', $binds);

        if ($binds['p_status']['value'] === 'SUCCESS') {
            jsonSuccess([
                'payment_ref' => $binds['p_payment_ref']['value'],
                'remaining_balance' => $binds['p_remaining_bal']['value']
            ], $binds['p_message']['value']);
        } else {
            jsonError($binds['p_message']['value']);
        }
    } catch (Exception $e) {
        jsonError($e->getMessage());
    }
}

if ($action === 'calculate_emi') {
    $p = (float)($input['principal'] ?? 100000);
    $r = (float)($input['rate'] ?? 10.0);
    $n = (int)($input['months'] ?? 12);

    $bridge = OracleBridge::getInstance();
    $emi = $bridge->calcEMI($p, $r, $n);
    $totalPayable = round($emi * $n, 2);
    $totalInterest = round($totalPayable - $p, 2);

    jsonSuccess([
        'monthly_emi' => $emi,
        'total_interest' => $totalInterest,
        'total_payable' => $totalPayable
    ]);
}

// ----------------------------------------------------------------------------
// BENEFICIARIES MANAGEMENT
// ----------------------------------------------------------------------------
if ($action === 'list_beneficiaries') {
    try {
        $bens = $db->query("SELECT * FROM BENEFICIARIES");
        jsonSuccess($bens);
    } catch (Exception $e) {
        jsonError($e->getMessage());
    }
}

if ($action === 'create_beneficiary') {
    $custId = (int)($input['customer_id'] ?? 1001);
    $name = trim($input['name'] ?? '');
    $accNo = trim($input['account_number'] ?? '');
    $bank = trim($input['bank_name'] ?? 'Smart Bank');
    $ifsc = trim($input['ifsc'] ?? 'SMBL0001001');
    $limit = (float)($input['limit'] ?? 50000);

    if (empty($name) || empty($accNo)) {
        jsonError('Beneficiary name and account number are required.');
    }

    try {
        $bridge = OracleBridge::getInstance();
        $ref = new ReflectionProperty('OracleBridge', 'data');
        $ref->setAccessible(true);
        $fullData = $ref->getValue($bridge);

        $newId = 3000 + count($fullData['BENEFICIARIES']) + 1;
        $row = [
            'BENEFICIARY_ID' => $newId,
            'CUSTOMER_ID' => $custId,
            'BENEFICIARY_NAME' => $name,
            'BENEFICIARY_ACCOUNT' => $accNo,
            'BANK_NAME' => $bank,
            'IFSC_CODE' => $ifsc,
            'TRANSFER_LIMIT' => $limit,
            'STATUS' => 'Active'
        ];
        $fullData['BENEFICIARIES'][] = $row;
        $ref->setValue($bridge, $fullData);
        $saveMethod = new ReflectionMethod('OracleBridge', 'save');
        $saveMethod->setAccessible(true);
        $saveMethod->invoke($bridge);

        jsonSuccess($row, "Beneficiary {$name} added successfully.");
    } catch (Exception $e) {
        jsonError($e->getMessage());
    }
}

// ----------------------------------------------------------------------------
// AUDIT LOGS
// ----------------------------------------------------------------------------
if ($action === 'list_audit_logs') {
    try {
        $logs = $db->query("SELECT * FROM AUDIT_LOGS");
        jsonSuccess($logs);
    } catch (Exception $e) {
        jsonError($e->getMessage());
    }
}

// ----------------------------------------------------------------------------
// METADATA LOOKUPS (BRANCHES, ACCOUNT TYPES)
// ----------------------------------------------------------------------------
if ($action === 'get_branches') {
    jsonSuccess($db->query("SELECT * FROM BANK_BRANCHES"));
}

if ($action === 'get_account_types') {
    jsonSuccess($db->query("SELECT * FROM ACCOUNT_TYPES"));
}

jsonError("Unrecognized action: {$action}", 404);
