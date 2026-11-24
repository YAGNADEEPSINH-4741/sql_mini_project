<?php
/**
 * ORACLE DATABASE LOCAL SIMULATION & DATA STORE BRIDGE
 * Provides instant fallback simulation of Oracle 10g schema, stored procedures,
 * triggers, and audit logs when PHP OCI8 instant client is being configured.
 */

class OracleBridge {
    private static $instance = null;
    private $dataFile;
    private $data = [];

    private function __construct() {
        $this->dataFile = __DIR__ . '/bridge_data.json';
        if (file_exists($this->dataFile)) {
            $this->data = json_decode(file_get_contents($this->dataFile), true);
        }
        if (empty($this->data) || !isset($this->data['CUSTOMERS'])) {
            $this->seedInitialData();
        }
    }

    public static function getInstance() {
        if (self::$instance === null) {
            self::$instance = new OracleBridge();
        }
        return self::$instance;
    }

    private function save() {
        file_put_contents($this->dataFile, json_encode($this->data, JSON_PRETTY_PRINT));
    }

    public function getData($table) {
        return isset($this->data[$table]) ? $this->data[$table] : [];
    }

    public function executeSelect($sql, $params = []) {
        $sqlClean = strtoupper(trim($sql));

        // Route Views
        if (strpos($sqlClean, 'FROM CUSTOMER_ACCOUNT_VIEW') !== false) {
            return $this->viewCustomerAccounts();
        }
        if (strpos($sqlClean, 'FROM TRANSACTION_HISTORY_VIEW') !== false) {
            return $this->viewTransactions();
        }
        if (strpos($sqlClean, 'FROM LOAN_DETAILS_VIEW') !== false) {
            return $this->viewLoans();
        }
        if (strpos($sqlClean, 'FROM BRANCH_PERFORMANCE_VIEW') !== false) {
            return $this->viewBranches();
        }

        // Direct table selects
        if (strpos($sqlClean, 'FROM CUSTOMERS') !== false) {
            return $this->data['CUSTOMERS'];
        }
        if (strpos($sqlClean, 'FROM BANK_ACCOUNTS') !== false) {
            return $this->data['BANK_ACCOUNTS'];
        }
        if (strpos($sqlClean, 'FROM TRANSACTIONS') !== false) {
            return $this->data['TRANSACTIONS'];
        }
        if (strpos($sqlClean, 'FROM LOANS') !== false) {
            return $this->data['LOANS'];
        }
        if (strpos($sqlClean, 'FROM BENEFICIARIES') !== false) {
            return $this->data['BENEFICIARIES'];
        }
        if (strpos($sqlClean, 'FROM AUDIT_LOGS') !== false) {
            return array_reverse($this->data['AUDIT_LOGS']);
        }
        if (strpos($sqlClean, 'FROM ADMIN_USERS') !== false) {
            return $this->data['ADMIN_USERS'];
        }
        if (strpos($sqlClean, 'FROM BANK_BRANCHES') !== false) {
            return $this->data['BANK_BRANCHES'];
        }
        if (strpos($sqlClean, 'FROM ACCOUNT_TYPES') !== false) {
            return $this->data['ACCOUNT_TYPES'];
        }

        return [];
    }

    public function executeDML($sql, $params = []) {
        return true;
    }

    public function callProcedure($procName, &$bindParams) {
        $proc = strtoupper(trim($procName));

        // 1. CREATE_BANK_ACCOUNT
        if ($proc === 'CREATE_BANK_ACCOUNT') {
            $custId = $bindParams['p_customer_id']['value'];
            $branchId = $bindParams['p_branch_id']['value'];
            $typeId = $bindParams['p_type_id']['value'];
            $initDep = (float)$bindParams['p_initial_deposit']['value'];

            $newId = 2000 + count($this->data['BANK_ACCOUNTS']) + 1;
            $newAccNo = "SB{$custId}{$newId}";

            $newAcc = [
                'ACCOUNT_ID' => $newId,
                'ACCOUNT_NUMBER' => $newAccNo,
                'CUSTOMER_ID' => $custId,
                'BRANCH_ID' => $branchId,
                'TYPE_ID' => $typeId,
                'BALANCE' => $initDep,
                'OVERDRAFT_LIMIT' => 0.00,
                'ACCOUNT_STATUS' => 'Active',
                'OPENED_DATE' => date('Y-m-d')
            ];
            $this->data['BANK_ACCOUNTS'][] = $newAcc;

            if ($initDep > 0) {
                $this->addTransaction($newId, 'Deposit', $initDep, $initDep, null, 'Account Opening Initial Deposit');
            }

            $this->logAudit('BANK_ACCOUNTS', 'INSERT', (string)$newId, null, "ACCOUNT_NUMBER={$newAccNo}, BALANCE={$initDep}");
            $this->save();

            $bindParams['p_account_number']['value'] = $newAccNo;
            $bindParams['p_status']['value'] = 'SUCCESS';
            $bindParams['p_message']['value'] = "Account {$newAccNo} created successfully.";
            return true;
        }

        // 2. DEPOSIT_MONEY
        if ($proc === 'DEPOSIT_MONEY' || $proc === 'BANKING_PACKAGE.DEPOSIT') {
            $accNo = $bindParams['p_account_number']['value'];
            $amount = (float)$bindParams['p_amount']['value'];
            $desc = $bindParams['p_description']['value'] ?? 'Cash Deposit';

            if ($amount <= 0) {
                $bindParams['p_status']['value'] = 'ERROR';
                $bindParams['p_message']['value'] = 'Deposit amount must be positive.';
                return false;
            }

            foreach ($this->data['BANK_ACCOUNTS'] as &$acc) {
                if ($acc['ACCOUNT_NUMBER'] === $accNo) {
                    if ($acc['ACCOUNT_STATUS'] !== 'Active') {
                        $bindParams['p_status']['value'] = 'ERROR';
                        $bindParams['p_message']['value'] = 'Cannot deposit to non-active account.';
                        return false;
                    }
                    $oldBal = $acc['BALANCE'];
                    $acc['BALANCE'] += $amount;
                    $newBal = $acc['BALANCE'];
                    
                    $ref = $this->addTransaction($acc['ACCOUNT_ID'], 'Deposit', $amount, $newBal, null, $desc);
                    $this->logAudit('BANK_ACCOUNTS', 'UPDATE', (string)$acc['ACCOUNT_ID'], "BALANCE={$oldBal}", "BALANCE={$newBal}");
                    $this->save();

                    $bindParams['p_txn_ref']['value'] = $ref;
                    $bindParams['p_new_balance']['value'] = $newBal;
                    $bindParams['p_status']['value'] = 'SUCCESS';
                    $bindParams['p_message']['value'] = "Successfully deposited INR {$amount}. New balance: INR {$newBal}";
                    return true;
                }
            }
            $bindParams['p_status']['value'] = 'ERROR';
            $bindParams['p_message']['value'] = "Account {$accNo} not found.";
            return false;
        }

        // 3. WITHDRAW_MONEY
        if ($proc === 'WITHDRAW_MONEY' || $proc === 'BANKING_PACKAGE.WITHDRAW') {
            $accNo = $bindParams['p_account_number']['value'];
            $amount = (float)$bindParams['p_amount']['value'];
            $desc = $bindParams['p_description']['value'] ?? 'Cash Withdrawal';

            if ($amount <= 0) {
                $bindParams['p_status']['value'] = 'ERROR';
                $bindParams['p_message']['value'] = 'Withdrawal amount must be positive.';
                return false;
            }

            foreach ($this->data['BANK_ACCOUNTS'] as &$acc) {
                if ($acc['ACCOUNT_NUMBER'] === $accNo) {
                    if ($acc['ACCOUNT_STATUS'] !== 'Active') {
                        $bindParams['p_status']['value'] = 'ERROR';
                        $bindParams['p_message']['value'] = 'Cannot withdraw from non-active account.';
                        return false;
                    }
                    $avail = $acc['BALANCE'] + $acc['OVERDRAFT_LIMIT'];
                    if ($avail < $amount) {
                        $bindParams['p_status']['value'] = 'ERROR';
                        $bindParams['p_message']['value'] = "Insufficient funds. Available: INR {$avail}, Requested: INR {$amount}";
                        return false;
                    }
                    $oldBal = $acc['BALANCE'];
                    $acc['BALANCE'] -= $amount;
                    $newBal = $acc['BALANCE'];

                    $ref = $this->addTransaction($acc['ACCOUNT_ID'], 'Withdrawal', $amount, $newBal, null, $desc);
                    $this->logAudit('BANK_ACCOUNTS', 'UPDATE', (string)$acc['ACCOUNT_ID'], "BALANCE={$oldBal}", "BALANCE={$newBal}");
                    $this->save();

                    $bindParams['p_txn_ref']['value'] = $ref;
                    $bindParams['p_new_balance']['value'] = $newBal;
                    $bindParams['p_status']['value'] = 'SUCCESS';
                    $bindParams['p_message']['value'] = "Successfully withdrew INR {$amount}. Remaining balance: INR {$newBal}";
                    return true;
                }
            }
            $bindParams['p_status']['value'] = 'ERROR';
            $bindParams['p_message']['value'] = "Account {$accNo} not found.";
            return false;
        }

        // 4. TRANSFER_MONEY
        if ($proc === 'TRANSFER_MONEY' || $proc === 'BANKING_PACKAGE.TRANSFER') {
            $senderAccNo = $bindParams['p_sender_acc_no']['value'];
            $recAccNo = $bindParams['p_receiver_acc_no']['value'];
            $amount = (float)$bindParams['p_amount']['value'];
            $desc = $bindParams['p_description']['value'] ?? 'Fund Transfer';

            if ($senderAccNo === $recAccNo) {
                $bindParams['p_status']['value'] = 'ERROR';
                $bindParams['p_message']['value'] = 'Sender and receiver accounts cannot be identical.';
                return false;
            }

            $senderIdx = null;
            $recIdx = null;
            foreach ($this->data['BANK_ACCOUNTS'] as $idx => $a) {
                if ($a['ACCOUNT_NUMBER'] === $senderAccNo) $senderIdx = $idx;
                if ($a['ACCOUNT_NUMBER'] === $recAccNo) $recIdx = $idx;
            }

            if ($senderIdx === null) {
                $bindParams['p_status']['value'] = 'ERROR';
                $bindParams['p_message']['value'] = "Sender account {$senderAccNo} does not exist.";
                return false;
            }
            if ($recIdx === null) {
                $bindParams['p_status']['value'] = 'ERROR';
                $bindParams['p_message']['value'] = "Beneficiary account {$recAccNo} does not exist.";
                return false;
            }

            $sender = &$this->data['BANK_ACCOUNTS'][$senderIdx];
            $receiver = &$this->data['BANK_ACCOUNTS'][$recIdx];

            if ($sender['ACCOUNT_STATUS'] !== 'Active') {
                $bindParams['p_status']['value'] = 'ERROR';
                $bindParams['p_message']['value'] = 'Sender account is not active.';
                return false;
            }
            if ($receiver['ACCOUNT_STATUS'] !== 'Active') {
                $bindParams['p_status']['value'] = 'ERROR';
                $bindParams['p_message']['value'] = 'Beneficiary account is not active.';
                return false;
            }

            $avail = $sender['BALANCE'] + $sender['OVERDRAFT_LIMIT'];
            if ($avail < $amount) {
                $bindParams['p_status']['value'] = 'ERROR';
                $bindParams['p_message']['value'] = 'Insufficient funds in sender account.';
                return false;
            }

            // Execute Atomic Transfer
            $sender['BALANCE'] -= $amount;
            $receiver['BALANCE'] += $amount;

            $debitRef = $this->addTransaction($sender['ACCOUNT_ID'], 'Transfer_Debit', $amount, $sender['BALANCE'], $receiver['ACCOUNT_ID'], "Transfer to {$recAccNo}: {$desc}");
            $creditRef = $this->addTransaction($receiver['ACCOUNT_ID'], 'Transfer_Credit', $amount, $receiver['BALANCE'], $sender['ACCOUNT_ID'], "Transfer from {$senderAccNo}: {$desc}");

            $this->logAudit('BANK_ACCOUNTS', 'UPDATE', (string)$sender['ACCOUNT_ID'], "BALANCE", "BALANCE={$sender['BALANCE']}");
            $this->logAudit('BANK_ACCOUNTS', 'UPDATE', (string)$receiver['ACCOUNT_ID'], "BALANCE", "BALANCE={$receiver['BALANCE']}");
            $this->save();

            $bindParams['p_txn_ref']['value'] = $debitRef;
            $bindParams['p_sender_balance']['value'] = $sender['BALANCE'];
            $bindParams['p_status']['value'] = 'SUCCESS';
            $bindParams['p_message']['value'] = "Transferred INR {$amount} to {$recAccNo} successfully.";
            return true;
        }

        // 5. APPLY_FOR_LOAN
        if ($proc === 'APPLY_FOR_LOAN' || $proc === 'LOAN_PACKAGE.APPLY_LOAN') {
            $custId = $bindParams['p_customer_id']['value'];
            $branchId = $bindParams['p_branch_id']['value'];
            $type = $bindParams['p_loan_type']['value'];
            $amount = (float)$bindParams['p_loan_amount']['value'];
            $rate = (float)$bindParams['p_interest_rate']['value'];
            $term = (int)$bindParams['p_term_months']['value'];

            $emi = $this->calcEMI($amount, $rate, $term);
            $loanId = 4000 + count($this->data['LOANS']) + 1;
            $loanNo = "LN" . date('Ym') . $loanId;

            $newLoan = [
                'LOAN_ID' => $loanId,
                'LOAN_NUMBER' => $loanNo,
                'CUSTOMER_ID' => $custId,
                'BRANCH_ID' => $branchId,
                'LOAN_TYPE' => $type,
                'LOAN_AMOUNT' => $amount,
                'INTEREST_RATE' => $rate,
                'TERM_MONTHS' => $term,
                'MONTHLY_EMI' => $emi,
                'OUTSTANDING_BALANCE' => $amount,
                'LOAN_STATUS' => 'Pending',
                'APPLICATION_DATE' => date('Y-m-d'),
                'APPROVAL_DATE' => null
            ];
            $this->data['LOANS'][] = $newLoan;
            $this->save();

            $bindParams['p_loan_number']['value'] = $loanNo;
            $bindParams['p_monthly_emi']['value'] = $emi;
            $bindParams['p_status']['value'] = 'SUCCESS';
            $bindParams['p_message']['value'] = "Loan application {$loanNo} submitted. EMI: INR {$emi}";
            return true;
        }

        // 6. APPROVE_LOAN
        if ($proc === 'APPROVE_LOAN' || $proc === 'LOAN_PACKAGE.APPROVE_LOAN_REQUEST') {
            $loanNo = $bindParams['p_loan_number']['value'];
            $decision = $bindParams['p_decision']['value'];
            $disburseAcc = $bindParams['p_disburse_acc']['value'] ?? null;

            foreach ($this->data['LOANS'] as &$l) {
                if ($l['LOAN_NUMBER'] === $loanNo) {
                    if ($decision === 'Approved') {
                        $l['LOAN_STATUS'] = 'Approved';
                        $l['APPROVAL_DATE'] = date('Y-m-d');
                        if ($disburseAcc) {
                            foreach ($this->data['BANK_ACCOUNTS'] as &$a) {
                                if ($a['ACCOUNT_NUMBER'] === $disburseAcc) {
                                    $a['BALANCE'] += $l['LOAN_AMOUNT'];
                                    $this->addTransaction($a['ACCOUNT_ID'], 'Loan_Disbursement', $l['LOAN_AMOUNT'], $a['BALANCE'], null, "Disbursement for {$loanNo}");
                                    $l['LOAN_STATUS'] = 'Disbursed';
                                    break;
                                }
                            }
                        }
                        $bindParams['p_status']['value'] = 'SUCCESS';
                        $bindParams['p_message']['value'] = "Loan {$loanNo} approved successfully.";
                    } else {
                        $l['LOAN_STATUS'] = 'Rejected';
                        $l['APPROVAL_DATE'] = date('Y-m-d');
                        $bindParams['p_status']['value'] = 'SUCCESS';
                        $bindParams['p_message']['value'] = "Loan {$loanNo} rejected.";
                    }
                    $this->save();
                    return true;
                }
            }
            $bindParams['p_status']['value'] = 'ERROR';
            $bindParams['p_message']['value'] = "Loan {$loanNo} not found.";
            return false;
        }

        // 7. PROCESS_LOAN_PAYMENT
        if ($proc === 'PROCESS_LOAN_PAYMENT' || $proc === 'LOAN_PACKAGE.MAKE_PAYMENT') {
            $loanNo = $bindParams['p_loan_number']['value'];
            $amount = (float)$bindParams['p_amount']['value'];
            $method = $bindParams['p_payment_method']['value'] ?? 'Online Transfer';

            foreach ($this->data['LOANS'] as &$l) {
                if ($l['LOAN_NUMBER'] === $loanNo) {
                    $outBal = $l['OUTSTANDING_BALANCE'];
                    $monthlyRate = ($l['INTEREST_RATE'] / 12.0) / 100.0;
                    $intComp = round($outBal * $monthlyRate, 2);
                    $prinComp = max(0, $amount - $intComp);
                    $newOut = max(0, $outBal - $prinComp);

                    $l['OUTSTANDING_BALANCE'] = $newOut;
                    if ($newOut <= 0) $l['LOAN_STATUS'] = 'Closed';

                    $payId = 5000 + count($this->data['LOAN_PAYMENTS']) + 1;
                    $payRef = "LP" . date('Ymd') . "-" . str_pad($payId, 5, '0', STR_PAD_LEFT);

                    $this->data['LOAN_PAYMENTS'][] = [
                        'PAYMENT_ID' => $payId,
                        'PAYMENT_REF' => $payRef,
                        'LOAN_ID' => $l['LOAN_ID'],
                        'PAYMENT_AMOUNT' => $amount,
                        'PRINCIPAL_COMPONENT' => $prinComp,
                        'INTEREST_COMPONENT' => $intComp,
                        'PAYMENT_DATE' => date('Y-m-d'),
                        'PAYMENT_METHOD' => $method,
                        'PAYMENT_STATUS' => 'Completed'
                    ];
                    $this->save();

                    $bindParams['p_payment_ref']['value'] = $payRef;
                    $bindParams['p_remaining_bal']['value'] = $newOut;
                    $bindParams['p_status']['value'] = 'SUCCESS';
                    $bindParams['p_message']['value'] = "Payment recorded. Outstanding: INR {$newOut}";
                    return true;
                }
            }
            $bindParams['p_status']['value'] = 'ERROR';
            $bindParams['p_message']['value'] = "Loan {$loanNo} not found.";
            return false;
        }

        return false;
    }

    private function addTransaction($accId, $type, $amount, $balAfter, $relAccId, $desc) {
        $id = 100000 + count($this->data['TRANSACTIONS']) + 1;
        $ref = "TXN-" . date('Ymd') . "-" . str_pad($id, 6, '0', STR_PAD_LEFT);
        $this->data['TRANSACTIONS'][] = [
            'TRANSACTION_ID' => $id,
            'TRANSACTION_REF' => $ref,
            'ACCOUNT_ID' => $accId,
            'TRANSACTION_TYPE' => $type,
            'AMOUNT' => $amount,
            'BALANCE_AFTER' => $balAfter,
            'TRANSACTION_DATE' => date('Y-m-d H:i:s'),
            'RELATED_ACCOUNT_ID' => $relAccId,
            'DESCRIPTION' => $desc,
            'TRANSACTION_STATUS' => 'Completed'
        ];
        return $ref;
    }

    private function logAudit($table, $op, $recordId, $oldVal, $newVal) {
        $id = count($this->data['AUDIT_LOGS']) + 1;
        $this->data['AUDIT_LOGS'][] = [
            'LOG_ID' => $id,
            'TABLE_NAME' => $table,
            'OPERATION_TYPE' => $op,
            'RECORD_ID' => $recordId,
            'OLD_VALUE' => $oldVal,
            'NEW_VALUE' => $newVal,
            'CHANGED_BY' => 'ADMIN',
            'CHANGED_AT' => date('Y-m-d H:i:s'),
            'CLIENT_IP' => '127.0.0.1'
        ];
    }

    public function calcEMI($p, $r, $n) {
        if ($p <= 0 || $n <= 0) return 0;
        if ($r == 0) return round($p / $n, 2);
        $mr = ($r / 12.0) / 100.0;
        $f = pow(1 + $mr, $n);
        return round(($p * $mr * $f) / ($f - 1), 2);
    }

    private function viewCustomerAccounts() {
        $rows = [];
        $branches = [];
        foreach ($this->data['BANK_BRANCHES'] as $b) $branches[$b['BRANCH_ID']] = $b;
        $types = [];
        foreach ($this->data['ACCOUNT_TYPES'] as $t) $types[$t['TYPE_ID']] = $t;
        $custs = [];
        foreach ($this->data['CUSTOMERS'] as $c) $custs[$c['CUSTOMER_ID']] = $c;

        foreach ($this->data['BANK_ACCOUNTS'] as $a) {
            $c = $custs[$a['CUSTOMER_ID']] ?? [];
            $b = $branches[$a['BRANCH_ID']] ?? [];
            $t = $types[$a['TYPE_ID']] ?? [];
            $rows[] = [
                'CUSTOMER_ID' => $a['CUSTOMER_ID'],
                'CUSTOMER_NAME' => ($c['FIRST_NAME'] ?? '') . ' ' . ($c['LAST_NAME'] ?? ''),
                'EMAIL' => $c['EMAIL'] ?? '',
                'PHONE' => $c['PHONE'] ?? '',
                'CUSTOMER_CITY' => $c['CITY'] ?? '',
                'KYC_STATUS' => $c['KYC_STATUS'] ?? 'Verified',
                'ACCOUNT_ID' => $a['ACCOUNT_ID'],
                'ACCOUNT_NUMBER' => $a['ACCOUNT_NUMBER'],
                'ACCOUNT_TYPE' => $t['TYPE_NAME'] ?? 'Savings',
                'BALANCE' => $a['BALANCE'],
                'OVERDRAFT_LIMIT' => $a['OVERDRAFT_LIMIT'],
                'EFFECTIVE_AVAILABLE_BALANCE' => $a['BALANCE'] + $a['OVERDRAFT_LIMIT'],
                'ACCOUNT_STATUS' => $a['ACCOUNT_STATUS'],
                'BRANCH_ID' => $a['BRANCH_ID'],
                'BRANCH_NAME' => $b['BRANCH_NAME'] ?? '',
                'IFSC_CODE' => $b['IFSC_CODE'] ?? '',
                'BRANCH_CITY' => $b['CITY'] ?? '',
                'OPENED_DATE' => $a['OPENED_DATE']
            ];
        }
        return $rows;
    }

    private function viewTransactions() {
        $accs = [];
        foreach ($this->data['BANK_ACCOUNTS'] as $a) $accs[$a['ACCOUNT_ID']] = $a;
        $custs = [];
        foreach ($this->data['CUSTOMERS'] as $c) $custs[$c['CUSTOMER_ID']] = $c;

        $rows = [];
        foreach ($this->data['TRANSACTIONS'] as $t) {
            $a = $accs[$t['ACCOUNT_ID']] ?? [];
            $c = $custs[$a['CUSTOMER_ID'] ?? 0] ?? [];
            $relA = $accs[$t['RELATED_ACCOUNT_ID'] ?? 0] ?? [];
            $relC = $custs[$relA['CUSTOMER_ID'] ?? 0] ?? [];

            $rows[] = [
                'TRANSACTION_ID' => $t['TRANSACTION_ID'],
                'TRANSACTION_REF' => $t['TRANSACTION_REF'],
                'TRANSACTION_DATE' => $t['TRANSACTION_DATE'],
                'TRANSACTION_TYPE' => $t['TRANSACTION_TYPE'],
                'AMOUNT' => $t['AMOUNT'],
                'BALANCE_AFTER' => $t['BALANCE_AFTER'],
                'TRANSACTION_STATUS' => $t['TRANSACTION_STATUS'],
                'DESCRIPTION' => $t['DESCRIPTION'],
                'ACCOUNT_ID' => $t['ACCOUNT_ID'],
                'ACCOUNT_NUMBER' => $a['ACCOUNT_NUMBER'] ?? '',
                'CUSTOMER_ID' => $c['CUSTOMER_ID'] ?? 0,
                'ACCOUNT_HOLDER' => ($c['FIRST_NAME'] ?? '') . ' ' . ($c['LAST_NAME'] ?? ''),
                'RELATED_ACCOUNT_ID' => $t['RELATED_ACCOUNT_ID'],
                'RELATED_ACCOUNT_NUMBER' => $relA['ACCOUNT_NUMBER'] ?? '',
                'RELATED_ACCOUNT_HOLDER' => ($relC['FIRST_NAME'] ?? '') . ' ' . ($relC['LAST_NAME'] ?? '')
            ];
        }
        return array_reverse($rows);
    }

    private function viewLoans() {
        $custs = [];
        foreach ($this->data['CUSTOMERS'] as $c) $custs[$c['CUSTOMER_ID']] = $c;
        $branches = [];
        foreach ($this->data['BANK_BRANCHES'] as $b) $branches[$b['BRANCH_ID']] = $b;

        $rows = [];
        foreach ($this->data['LOANS'] as $l) {
            $c = $custs[$l['CUSTOMER_ID']] ?? [];
            $b = $branches[$l['BRANCH_ID']] ?? [];
            $rows[] = [
                'LOAN_ID' => $l['LOAN_ID'],
                'LOAN_NUMBER' => $l['LOAN_NUMBER'],
                'CUSTOMER_ID' => $l['CUSTOMER_ID'],
                'BORROWER_NAME' => ($c['FIRST_NAME'] ?? '') . ' ' . ($c['LAST_NAME'] ?? ''),
                'BORROWER_PHONE' => $c['PHONE'] ?? '',
                'BORROWER_EMAIL' => $c['EMAIL'] ?? '',
                'BRANCH_ID' => $l['BRANCH_ID'],
                'BRANCH_NAME' => $b['BRANCH_NAME'] ?? '',
                'LOAN_TYPE' => $l['LOAN_TYPE'],
                'LOAN_AMOUNT' => $l['LOAN_AMOUNT'],
                'INTEREST_RATE' => $l['INTEREST_RATE'],
                'TERM_MONTHS' => $l['TERM_MONTHS'],
                'MONTHLY_EMI' => $l['MONTHLY_EMI'],
                'OUTSTANDING_BALANCE' => $l['OUTSTANDING_BALANCE'],
                'LOAN_STATUS' => $l['LOAN_STATUS'],
                'APPLICATION_DATE' => $l['APPLICATION_DATE'],
                'APPROVAL_DATE' => $l['APPROVAL_DATE']
            ];
        }
        return $rows;
    }

    private function viewBranches() {
        return $this->data['BANK_BRANCHES'];
    }

    private function seedInitialData() {
        $this->data = [
            'ADMIN_USERS' => [
                ['ADMIN_ID' => 1, 'USERNAME' => 'admin', 'PASSWORD_HASH' => password_hash('admin123', PASSWORD_BCRYPT), 'FULL_NAME' => 'Yagnadeepsinh Vaghela', 'EMAIL' => 'admin@smartbank.com', 'ROLE' => 'Super Admin', 'STATUS' => 'Active']
            ],
            'BANK_BRANCHES' => [
                ['BRANCH_ID' => 101, 'BRANCH_NAME' => 'Nariman Point Corporate Branch', 'BRANCH_CODE' => 'BR001', 'IFSC_CODE' => 'SMBL0001001', 'ADDRESS' => 'Free Press Marg, Nariman Point', 'CITY' => 'Mumbai', 'STATE' => 'Maharashtra', 'PIN_CODE' => '400021', 'PHONE' => '+91-22-22851234', 'MANAGER_NAME' => 'Rajesh Verma'],
                ['BRANCH_ID' => 102, 'BRANCH_NAME' => 'Connaught Place Premier Branch', 'BRANCH_CODE' => 'BR002', 'IFSC_CODE' => 'SMBL0001002', 'ADDRESS' => 'Inner Circle, CP', 'CITY' => 'New Delhi', 'STATE' => 'Delhi', 'PIN_CODE' => '110001', 'PHONE' => '+91-11-23345678', 'MANAGER_NAME' => 'Sunita Rao'],
                ['BRANCH_ID' => 103, 'BRANCH_NAME' => 'Koramangala Tech Hub Branch', 'BRANCH_CODE' => 'BR003', 'IFSC_CODE' => 'SMBL0001003', 'ADDRESS' => '80 Feet Road, 4th Block', 'CITY' => 'Bengaluru', 'STATE' => 'Karnataka', 'PIN_CODE' => '560034', 'PHONE' => '+91-80-25539876', 'MANAGER_NAME' => 'Vikramaditya Hegde'],
                ['BRANCH_ID' => 104, 'BRANCH_NAME' => 'Ashram Road Financial Branch', 'BRANCH_CODE' => 'BR004', 'IFSC_CODE' => 'SMBL0001004', 'ADDRESS' => 'Ashram Road', 'CITY' => 'Ahmedabad', 'STATE' => 'Gujarat', 'PIN_CODE' => '380009', 'PHONE' => '+91-79-26581122', 'MANAGER_NAME' => 'Kiritbhai Solanki'],
                ['BRANCH_ID' => 105, 'BRANCH_NAME' => 'Banjara Hills Elite Branch', 'BRANCH_CODE' => 'BR005', 'IFSC_CODE' => 'SMBL0001005', 'ADDRESS' => 'Road No. 12, Banjara Hills', 'CITY' => 'Hyderabad', 'STATE' => 'Telangana', 'PIN_CODE' => '500034', 'PHONE' => '+91-40-23314567', 'MANAGER_NAME' => 'Kavitha Reddy']
            ],
            'ACCOUNT_TYPES' => [
                ['TYPE_ID' => 1, 'TYPE_NAME' => 'Standard Savings Account', 'MIN_BALANCE' => 1000.00, 'INTEREST_RATE' => 3.50, 'OVERDRAFT_ALLOWED' => 'N'],
                ['TYPE_ID' => 2, 'TYPE_NAME' => 'Premium Privilege Savings', 'MIN_BALANCE' => 10000.00, 'INTEREST_RATE' => 4.25, 'OVERDRAFT_ALLOWED' => 'N'],
                ['TYPE_ID' => 3, 'TYPE_NAME' => 'Current Business Account', 'MIN_BALANCE' => 5000.00, 'INTEREST_RATE' => 0.00, 'OVERDRAFT_ALLOWED' => 'Y'],
                ['TYPE_ID' => 4, 'TYPE_NAME' => 'Fixed Deposit Account', 'MIN_BALANCE' => 5000.00, 'INTEREST_RATE' => 7.10, 'OVERDRAFT_ALLOWED' => 'N'],
                ['TYPE_ID' => 5, 'TYPE_NAME' => 'Corporate Salary Account', 'MIN_BALANCE' => 0.00, 'INTEREST_RATE' => 3.75, 'OVERDRAFT_ALLOWED' => 'Y']
            ],
            'CUSTOMERS' => [
                ['CUSTOMER_ID' => 1001, 'FIRST_NAME' => 'Aarav', 'LAST_NAME' => 'Sharma', 'EMAIL' => 'aarav.sharma@gmail.com', 'PHONE' => '+91-9876543210', 'DATE_OF_BIRTH' => '1990-05-14', 'GENDER' => 'Male', 'ADDRESS' => 'Flat 402, Bandra West', 'CITY' => 'Mumbai', 'STATE' => 'Maharashtra', 'PIN_CODE' => '400050', 'KYC_STATUS' => 'Verified'],
                ['CUSTOMER_ID' => 1002, 'FIRST_NAME' => 'Diya', 'LAST_NAME' => 'Kapoor', 'EMAIL' => 'diya.kapoor@outlook.com', 'PHONE' => '+91-9876543211', 'DATE_OF_BIRTH' => '1994-08-22', 'GENDER' => 'Female', 'ADDRESS' => 'Golf Links', 'CITY' => 'New Delhi', 'STATE' => 'Delhi', 'PIN_CODE' => '110003', 'KYC_STATUS' => 'Verified'],
                ['CUSTOMER_ID' => 1003, 'FIRST_NAME' => 'Siddharth', 'LAST_NAME' => 'Narayanan', 'EMAIL' => 'sid.narayan@yahoo.com', 'PHONE' => '+91-9876543212', 'DATE_OF_BIRTH' => '1988-11-30', 'GENDER' => 'Male', 'ADDRESS' => 'Indiranagar', 'CITY' => 'Bengaluru', 'STATE' => 'Karnataka', 'PIN_CODE' => '560038', 'KYC_STATUS' => 'Verified'],
                ['CUSTOMER_ID' => 1004, 'FIRST_NAME' => 'Rhea', 'LAST_NAME' => 'Chowdhury', 'EMAIL' => 'rhea.c@gmail.com', 'PHONE' => '+91-9876543213', 'DATE_OF_BIRTH' => '1996-03-19', 'GENDER' => 'Female', 'ADDRESS' => 'Southern Avenue', 'CITY' => 'Kolkata', 'STATE' => 'West Bengal', 'PIN_CODE' => '700029', 'KYC_STATUS' => 'Verified'],
                ['CUSTOMER_ID' => 1005, 'FIRST_NAME' => 'Aditya', 'LAST_NAME' => 'Patel', 'EMAIL' => 'aditya.patel@techcorp.in', 'PHONE' => '+91-9876543214', 'DATE_OF_BIRTH' => '1985-07-08', 'GENDER' => 'Male', 'ADDRESS' => 'CG Road', 'CITY' => 'Ahmedabad', 'STATE' => 'Gujarat', 'PIN_CODE' => '380006', 'KYC_STATUS' => 'Verified'],
                ['CUSTOMER_ID' => 1006, 'FIRST_NAME' => 'Kavya', 'LAST_NAME' => 'Menon', 'EMAIL' => 'kavya.m@icloud.com', 'PHONE' => '+91-9876543215', 'DATE_OF_BIRTH' => '1992-12-05', 'GENDER' => 'Female', 'ADDRESS' => 'Panampilly Nagar', 'CITY' => 'Kochi', 'STATE' => 'Kerala', 'PIN_CODE' => '682036', 'KYC_STATUS' => 'Verified'],
                ['CUSTOMER_ID' => 1007, 'FIRST_NAME' => 'Varun', 'LAST_NAME' => 'Singhania', 'EMAIL' => 'varun.s@singhania.co', 'PHONE' => '+91-9876543216', 'DATE_OF_BIRTH' => '1982-01-25', 'GENDER' => 'Male', 'ADDRESS' => 'Jubilee Hills', 'CITY' => 'Hyderabad', 'STATE' => 'Telangana', 'PIN_CODE' => '500033', 'KYC_STATUS' => 'Verified'],
                ['CUSTOMER_ID' => 1008, 'FIRST_NAME' => 'Neha', 'LAST_NAME' => 'Bose', 'EMAIL' => 'neha.bose@gmail.com', 'PHONE' => '+91-9876543217', 'DATE_OF_BIRTH' => '1998-09-11', 'GENDER' => 'Female', 'ADDRESS' => 'Bellandur', 'CITY' => 'Bengaluru', 'STATE' => 'Karnataka', 'PIN_CODE' => '560103', 'KYC_STATUS' => 'Pending']
            ],
            'BANK_ACCOUNTS' => [
                ['ACCOUNT_ID' => 2001, 'ACCOUNT_NUMBER' => 'SB1001002001', 'CUSTOMER_ID' => 1001, 'BRANCH_ID' => 101, 'TYPE_ID' => 1, 'BALANCE' => 48500.00, 'OVERDRAFT_LIMIT' => 0.00, 'ACCOUNT_STATUS' => 'Active', 'OPENED_DATE' => '2022-01-11'],
                ['ACCOUNT_ID' => 2002, 'ACCOUNT_NUMBER' => 'SB1001002002', 'CUSTOMER_ID' => 1001, 'BRANCH_ID' => 101, 'TYPE_ID' => 4, 'BALANCE' => 150000.00, 'OVERDRAFT_LIMIT' => 0.00, 'ACCOUNT_STATUS' => 'Active', 'OPENED_DATE' => '2022-06-01'],
                ['ACCOUNT_ID' => 2003, 'ACCOUNT_NUMBER' => 'SB1002002003', 'CUSTOMER_ID' => 1002, 'BRANCH_ID' => 102, 'TYPE_ID' => 2, 'BALANCE' => 92450.00, 'OVERDRAFT_LIMIT' => 0.00, 'ACCOUNT_STATUS' => 'Active', 'OPENED_DATE' => '2022-02-16'],
                ['ACCOUNT_ID' => 2004, 'ACCOUNT_NUMBER' => 'SB1003002004', 'CUSTOMER_ID' => 1003, 'BRANCH_ID' => 103, 'TYPE_ID' => 3, 'BALANCE' => 320000.00, 'OVERDRAFT_LIMIT' => 50000.00, 'ACCOUNT_STATUS' => 'Active', 'OPENED_DATE' => '2022-03-06'],
                ['ACCOUNT_ID' => 2005, 'ACCOUNT_NUMBER' => 'SB1004002005', 'CUSTOMER_ID' => 1004, 'BRANCH_ID' => 101, 'TYPE_ID' => 1, 'BALANCE' => 12800.00, 'OVERDRAFT_LIMIT' => 0.00, 'ACCOUNT_STATUS' => 'Active', 'OPENED_DATE' => '2022-04-15'],
                ['ACCOUNT_ID' => 2006, 'ACCOUNT_NUMBER' => 'SB1005002006', 'CUSTOMER_ID' => 1005, 'BRANCH_ID' => 104, 'TYPE_ID' => 3, 'BALANCE' => 540000.00, 'OVERDRAFT_LIMIT' => 100000.00, 'ACCOUNT_STATUS' => 'Active', 'OPENED_DATE' => '2022-05-22'],
                ['ACCOUNT_ID' => 2007, 'ACCOUNT_NUMBER' => 'SB1006002007', 'CUSTOMER_ID' => 1006, 'BRANCH_ID' => 103, 'TYPE_ID' => 1, 'BALANCE' => 65200.00, 'OVERDRAFT_LIMIT' => 0.00, 'ACCOUNT_STATUS' => 'Active', 'OPENED_DATE' => '2022-06-20'],
                ['ACCOUNT_ID' => 2008, 'ACCOUNT_NUMBER' => 'SB1007002008', 'CUSTOMER_ID' => 1007, 'BRANCH_ID' => 105, 'TYPE_ID' => 2, 'BALANCE' => 850000.00, 'OVERDRAFT_LIMIT' => 0.00, 'ACCOUNT_STATUS' => 'Active', 'OPENED_DATE' => '2022-07-25'],
                ['ACCOUNT_ID' => 2009, 'ACCOUNT_NUMBER' => 'SB1008002009', 'CUSTOMER_ID' => 1008, 'BRANCH_ID' => 103, 'TYPE_ID' => 5, 'BALANCE' => 25000.00, 'OVERDRAFT_LIMIT' => 15000.00, 'ACCOUNT_STATUS' => 'Active', 'OPENED_DATE' => '2023-01-16'],
                ['ACCOUNT_ID' => 2010, 'ACCOUNT_NUMBER' => 'SB1003002010', 'CUSTOMER_ID' => 1003, 'BRANCH_ID' => 103, 'TYPE_ID' => 1, 'BALANCE' => 3500.00, 'OVERDRAFT_LIMIT' => 0.00, 'ACCOUNT_STATUS' => 'Dormant', 'OPENED_DATE' => '2022-04-01']
            ],
            'TRANSACTIONS' => [
                ['TRANSACTION_ID' => 100001, 'TRANSACTION_REF' => 'TXN-20261101-0001', 'ACCOUNT_ID' => 2001, 'TRANSACTION_TYPE' => 'Deposit', 'AMOUNT' => 25000.00, 'BALANCE_AFTER' => 25000.00, 'TRANSACTION_DATE' => '2026-11-01 10:15:00', 'RELATED_ACCOUNT_ID' => null, 'DESCRIPTION' => 'Initial Cash Deposit at Nariman Point', 'TRANSACTION_STATUS' => 'Completed'],
                ['TRANSACTION_ID' => 100002, 'TRANSACTION_REF' => 'TXN-20261102-0002', 'ACCOUNT_ID' => 2001, 'TRANSACTION_TYPE' => 'Deposit', 'AMOUNT' => 30000.00, 'BALANCE_AFTER' => 55000.00, 'TRANSACTION_DATE' => '2026-11-04 11:30:00', 'RELATED_ACCOUNT_ID' => null, 'DESCRIPTION' => 'Cheque Clearance #440129', 'TRANSACTION_STATUS' => 'Completed'],
                ['TRANSACTION_ID' => 100003, 'TRANSACTION_REF' => 'TXN-20261105-0003', 'ACCOUNT_ID' => 2001, 'TRANSACTION_TYPE' => 'Withdrawal', 'AMOUNT' => 6500.00, 'BALANCE_AFTER' => 48500.00, 'TRANSACTION_DATE' => '2026-11-09 16:45:00', 'RELATED_ACCOUNT_ID' => null, 'DESCRIPTION' => 'ATM Cash Withdrawal Mumbai Airport', 'TRANSACTION_STATUS' => 'Completed'],
                ['TRANSACTION_ID' => 100004, 'TRANSACTION_REF' => 'TXN-20261108-0004', 'ACCOUNT_ID' => 2003, 'TRANSACTION_TYPE' => 'Deposit', 'AMOUNT' => 100000.00, 'BALANCE_AFTER' => 100000.00, 'TRANSACTION_DATE' => '2026-11-06 09:00:00', 'RELATED_ACCOUNT_ID' => null, 'DESCRIPTION' => 'Salary Credit from Global Media Corp', 'TRANSACTION_STATUS' => 'Completed'],
                ['TRANSACTION_ID' => 100005, 'TRANSACTION_REF' => 'TXN-20261110-0005', 'ACCOUNT_ID' => 2003, 'TRANSACTION_TYPE' => 'Withdrawal', 'AMOUNT' => 7550.00, 'BALANCE_AFTER' => 92450.00, 'TRANSACTION_DATE' => '2026-11-12 14:20:00', 'RELATED_ACCOUNT_ID' => null, 'DESCRIPTION' => 'Online Shopping E-Commerce payment', 'TRANSACTION_STATUS' => 'Completed'],
                ['TRANSACTION_ID' => 100006, 'TRANSACTION_REF' => 'TXN-20261112-0006', 'ACCOUNT_ID' => 2004, 'TRANSACTION_TYPE' => 'Deposit', 'AMOUNT' => 350000.00, 'BALANCE_AFTER' => 350000.00, 'TRANSACTION_DATE' => '2026-11-10 11:10:00', 'RELATED_ACCOUNT_ID' => null, 'DESCRIPTION' => 'Client invoice payment wire transfer', 'TRANSACTION_STATUS' => 'Completed'],
                ['TRANSACTION_ID' => 100007, 'TRANSACTION_REF' => 'TXN-20261114-0007', 'ACCOUNT_ID' => 2004, 'TRANSACTION_TYPE' => 'Transfer_Debit', 'AMOUNT' => 30000.00, 'BALANCE_AFTER' => 320000.00, 'TRANSACTION_DATE' => '2026-11-14 15:30:00', 'RELATED_ACCOUNT_ID' => 2007, 'DESCRIPTION' => 'Vendor payment to Kavya Menon Services', 'TRANSACTION_STATUS' => 'Completed'],
                ['TRANSACTION_ID' => 100008, 'TRANSACTION_REF' => 'TXN-20261114-0008', 'ACCOUNT_ID' => 2007, 'TRANSACTION_TYPE' => 'Transfer_Credit', 'AMOUNT' => 30000.00, 'BALANCE_AFTER' => 65200.00, 'TRANSACTION_DATE' => '2026-11-14 15:30:00', 'RELATED_ACCOUNT_ID' => 2004, 'DESCRIPTION' => 'Credit received from Siddharth Narayanan', 'TRANSACTION_STATUS' => 'Completed'],
                ['TRANSACTION_ID' => 100009, 'TRANSACTION_REF' => 'TXN-20261118-0009', 'ACCOUNT_ID' => 2006, 'TRANSACTION_TYPE' => 'Deposit', 'AMOUNT' => 600000.00, 'BALANCE_AFTER' => 600000.00, 'TRANSACTION_DATE' => '2026-11-18 10:00:00', 'RELATED_ACCOUNT_ID' => null, 'DESCRIPTION' => 'Business revenue deposit', 'TRANSACTION_STATUS' => 'Completed'],
                ['TRANSACTION_ID' => 100010, 'TRANSACTION_REF' => 'TXN-20261120-0010', 'ACCOUNT_ID' => 2006, 'TRANSACTION_TYPE' => 'Withdrawal', 'AMOUNT' => 60000.00, 'BALANCE_AFTER' => 540000.00, 'TRANSACTION_DATE' => '2026-11-20 17:05:00', 'RELATED_ACCOUNT_ID' => null, 'DESCRIPTION' => 'Office rent and utility payment', 'TRANSACTION_STATUS' => 'Completed'],
                ['TRANSACTION_ID' => 100011, 'TRANSACTION_REF' => 'TXN-20261122-0011', 'ACCOUNT_ID' => 2008, 'TRANSACTION_TYPE' => 'Deposit', 'AMOUNT' => 850000.00, 'BALANCE_AFTER' => 850000.00, 'TRANSACTION_DATE' => '2026-11-22 13:40:00', 'RELATED_ACCOUNT_ID' => null, 'DESCRIPTION' => 'Investment dividend liquidation', 'TRANSACTION_STATUS' => 'Completed']
            ],
            'LOANS' => [
                ['LOAN_ID' => 4001, 'LOAN_NUMBER' => 'LN2022014001', 'CUSTOMER_ID' => 1001, 'BRANCH_ID' => 101, 'LOAN_TYPE' => 'Home Loan', 'LOAN_AMOUNT' => 4500000.00, 'INTEREST_RATE' => 8.50, 'TERM_MONTHS' => 240, 'MONTHLY_EMI' => 39052.28, 'OUTSTANDING_BALANCE' => 4210000.00, 'LOAN_STATUS' => 'Approved', 'APPLICATION_DATE' => '2022-01-20', 'APPROVAL_DATE' => '2022-01-28'],
                ['LOAN_ID' => 4002, 'LOAN_NUMBER' => 'LN2022034002', 'CUSTOMER_ID' => 1003, 'BRANCH_ID' => 103, 'LOAN_TYPE' => 'Auto Loan', 'LOAN_AMOUNT' => 850000.00, 'INTEREST_RATE' => 9.25, 'TERM_MONTHS' => 60, 'MONTHLY_EMI' => 17743.82, 'OUTSTANDING_BALANCE' => 580000.00, 'LOAN_STATUS' => 'Approved', 'APPLICATION_DATE' => '2022-03-10', 'APPROVAL_DATE' => '2022-03-15'],
                ['LOAN_ID' => 4003, 'LOAN_NUMBER' => 'LN2022054003', 'CUSTOMER_ID' => 1005, 'BRANCH_ID' => 104, 'LOAN_TYPE' => 'Business Loan', 'LOAN_AMOUNT' => 2500000.00, 'INTEREST_RATE' => 11.50, 'TERM_MONTHS' => 84, 'MONTHLY_EMI' => 43501.12, 'OUTSTANDING_BALANCE' => 1950000.00, 'LOAN_STATUS' => 'Approved', 'APPLICATION_DATE' => '2022-05-25', 'APPROVAL_DATE' => '2022-06-02'],
                ['LOAN_ID' => 4004, 'LOAN_NUMBER' => 'LN2023024004', 'CUSTOMER_ID' => 1006, 'BRANCH_ID' => 103, 'LOAN_TYPE' => 'Personal Loan', 'LOAN_AMOUNT' => 300000.00, 'INTEREST_RATE' => 12.00, 'TERM_MONTHS' => 36, 'MONTHLY_EMI' => 9964.29, 'OUTSTANDING_BALANCE' => 215000.00, 'LOAN_STATUS' => 'Approved', 'APPLICATION_DATE' => '2023-02-10', 'APPROVAL_DATE' => '2023-02-14'],
                ['LOAN_ID' => 4005, 'LOAN_NUMBER' => 'LN2023054005', 'CUSTOMER_ID' => 1004, 'BRANCH_ID' => 101, 'LOAN_TYPE' => 'Education Loan', 'LOAN_AMOUNT' => 1200000.00, 'INTEREST_RATE' => 9.00, 'TERM_MONTHS' => 120, 'MONTHLY_EMI' => 15200.57, 'OUTSTANDING_BALANCE' => 1200000.00, 'LOAN_STATUS' => 'Pending', 'APPLICATION_DATE' => '2023-05-01', 'APPROVAL_DATE' => null]
            ],
            'LOAN_PAYMENTS' => [
                ['PAYMENT_ID' => 5001, 'PAYMENT_REF' => 'LP202610-001', 'LOAN_ID' => 4001, 'PAYMENT_AMOUNT' => 39052.28, 'PRINCIPAL_COMPONENT' => 10250.00, 'INTEREST_COMPONENT' => 28802.28, 'PAYMENT_DATE' => '2026-10-05', 'PAYMENT_METHOD' => 'Auto Debit', 'PAYMENT_STATUS' => 'Completed'],
                ['PAYMENT_ID' => 5002, 'PAYMENT_REF' => 'LP202611-002', 'LOAN_ID' => 4001, 'PAYMENT_AMOUNT' => 39052.28, 'PRINCIPAL_COMPONENT' => 10322.00, 'INTEREST_COMPONENT' => 28730.28, 'PAYMENT_DATE' => '2026-11-05', 'PAYMENT_METHOD' => 'Auto Debit', 'PAYMENT_STATUS' => 'Completed']
            ],
            'BENEFICIARIES' => [
                ['BENEFICIARY_ID' => 3001, 'CUSTOMER_ID' => 1001, 'BENEFICIARY_NAME' => 'Diya Kapoor', 'BENEFICIARY_ACCOUNT' => 'SB1002002003', 'BANK_NAME' => 'Smart Bank', 'IFSC_CODE' => 'SMBL0001002', 'TRANSFER_LIMIT' => 75000.00, 'STATUS' => 'Active'],
                ['BENEFICIARY_ID' => 3002, 'CUSTOMER_ID' => 1003, 'BENEFICIARY_NAME' => 'Kavya Menon', 'BENEFICIARY_ACCOUNT' => 'SB1006002007', 'BANK_NAME' => 'Smart Bank', 'IFSC_CODE' => 'SMBL0001003', 'TRANSFER_LIMIT' => 100000.00, 'STATUS' => 'Active'],
                ['BENEFICIARY_ID' => 3003, 'CUSTOMER_ID' => 1005, 'BENEFICIARY_NAME' => 'Varun Singhania', 'BENEFICIARY_ACCOUNT' => 'SB1007002008', 'BANK_NAME' => 'Smart Bank', 'IFSC_CODE' => 'SMBL0001005', 'TRANSFER_LIMIT' => 200000.00, 'STATUS' => 'Active']
            ],
            'AUDIT_LOGS' => [
                ['LOG_ID' => 1, 'TABLE_NAME' => 'BANK_ACCOUNTS', 'OPERATION_TYPE' => 'INSERT', 'RECORD_ID' => '2001', 'OLD_VALUE' => null, 'NEW_VALUE' => 'ACCOUNT_NUMBER=SB1001002001, BALANCE=25000', 'CHANGED_BY' => 'SYSTEM', 'CHANGED_AT' => '2026-11-01 10:15:00', 'CLIENT_IP' => '127.0.0.1'],
                ['LOG_ID' => 2, 'TABLE_NAME' => 'BANK_ACCOUNTS', 'OPERATION_TYPE' => 'UPDATE', 'RECORD_ID' => '2001', 'OLD_VALUE' => 'BALANCE=25000', 'NEW_VALUE' => 'BALANCE=55000', 'CHANGED_BY' => 'ADMIN', 'CHANGED_AT' => '2026-11-04 11:30:00', 'CLIENT_IP' => '127.0.0.1'],
                ['LOG_ID' => 3, 'TABLE_NAME' => 'BANK_ACCOUNTS', 'OPERATION_TYPE' => 'UPDATE', 'RECORD_ID' => '2001', 'OLD_VALUE' => 'BALANCE=55000', 'NEW_VALUE' => 'BALANCE=48500', 'CHANGED_BY' => 'ADMIN', 'CHANGED_AT' => '2026-11-09 16:45:00', 'CLIENT_IP' => '127.0.0.1']
            ]
        ];
        $this->save();
    }
}
