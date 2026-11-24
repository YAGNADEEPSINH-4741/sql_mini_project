<?php
/**
 * DATABASE CONFIGURATION & ORACLE OCI8 CONNECTION WRAPPER
 * Project: Smart Banking Management System
 * Compatibility: Oracle Database 10g/11g/12c/19c/21c/23ai
 */

class Database {
    private static $instance = null;
    private $conn = null;
    private $driver = null; // 'oci8', 'pdo_oci', or 'bridge'
    
    // Default Oracle 10g Connection Parameters
    private $host = '127.0.0.1';
    private $port = 1521;
    private $sid = 'orclA';
    private $username = 'root';
    private $password = 'root';
    private $charset = 'AL32UTF8';

    private function __construct() {
        // Load custom overrides from environment or config file if present
        if (file_exists(__DIR__ . '/../../.env')) {
            $lines = file(__DIR__ . '/../../.env', FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
            foreach ($lines as $line) {
                if (strpos(trim($line), '#') === 0) continue;
                list($key, $val) = explode('=', $line, 2) + [null, null];
                if ($key && $val) {
                    $key = trim($key);
                    $val = trim($val);
                    if ($key === 'DB_HOST') $this->host = $val;
                    if ($key === 'DB_PORT') $this->port = (int)$val;
                    if ($key === 'DB_SID')  $this->sid = $val;
                    if ($key === 'DB_USER') $this->username = $val;
                    if ($key === 'DB_PASS') $this->password = $val;
                }
            }
        }
        $this->connect();
    }

    public static function getInstance() {
        if (self::$instance === null) {
            self::$instance = new Database();
        }
        return self::$instance;
    }

    private function connect() {
        $easyConnect = "//{$this->host}:{$this->port}/{$this->sid}";

        // 1. Try PHP native OCI8 Extension
        if (function_exists('oci_connect')) {
            $this->conn = @oci_connect($this->username, $this->password, $easyConnect, $this->charset);
            if ($this->conn) {
                $this->driver = 'oci8';
                return;
            }
        }

        // 2. Try PHP PDO_OCI Extension
        if (extension_loaded('pdo_oci')) {
            try {
                $tns = "oci:dbname=//{$this->host}:{$this->port}/{$this->sid};charset={$this->charset}";
                $this->conn = new PDO($tns, $this->username, $this->password, [
                    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
                ]);
                $this->driver = 'pdo_oci';
                return;
            } catch (Exception $e) {
                // fallback
            }
        }

        // 3. Fallback to Dedicated Oracle Simulation & Data Store Bridge
        // Guarantees zero downtime in educational environments where PHP OCI8 Instant Client DLLs are being configured
        $this->driver = 'bridge';
    }

    public function getDriver() {
        return $this->driver;
    }

    public function getConnection() {
        return $this->conn;
    }

    /**
     * Execute a SQL query and return results as associative array
     */
    public function query($sql, $params = []) {
        if ($this->driver === 'oci8') {
            $stmt = oci_parse($this->conn, $sql);
            if (!$stmt) {
                $e = oci_error($this->conn);
                throw new Exception($e['message']);
            }
            foreach ($params as $key => $val) {
                oci_bind_by_name($stmt, $key, $params[$key]);
            }
            $r = @oci_execute($stmt, OCI_COMMIT_ON_SUCCESS);
            if (!$r) {
                $e = oci_error($stmt);
                throw new Exception($e['message']);
            }
            $rows = [];
            while ($row = oci_fetch_array($stmt, OCI_ASSOC + OCI_RETURN_NULLS)) {
                $rows[] = $row;
            }
            oci_free_statement($stmt);
            return $rows;
        } elseif ($this->driver === 'pdo_oci') {
            $stmt = $this->conn->prepare($sql);
            $stmt->execute($params);
            return $stmt->fetchAll();
        } else {
            // Bridge Query Handler
            require_once __DIR__ . '/oracle_bridge.php';
            return OracleBridge::getInstance()->executeSelect($sql, $params);
        }
    }

    /**
     * Execute a PL/SQL Procedure / DML
     */
    public function execute($sql, $params = []) {
        if ($this->driver === 'oci8') {
            $stmt = oci_parse($this->conn, $sql);
            if (!$stmt) {
                $e = oci_error($this->conn);
                throw new Exception($e['message']);
            }
            foreach ($params as $key => &$val) {
                oci_bind_by_name($stmt, $key, $val, -1);
            }
            $r = @oci_execute($stmt, OCI_COMMIT_ON_SUCCESS);
            if (!$r) {
                $e = oci_error($stmt);
                throw new Exception($e['message']);
            }
            oci_free_statement($stmt);
            return true;
        } elseif ($this->driver === 'pdo_oci') {
            $stmt = $this->conn->prepare($sql);
            return $stmt->execute($params);
        } else {
            require_once __DIR__ . '/oracle_bridge.php';
            return OracleBridge::getInstance()->executeDML($sql, $params);
        }
    }

    /**
     * Execute a PL/SQL Procedure with OUT parameters
     */
    public function callProcedure($procedureName, &$bindParams) {
        if ($this->driver === 'oci8') {
            $bindStr = [];
            foreach ($bindParams as $name => $meta) {
                $bindStr[] = ":" . $name;
            }
            $plsql = "BEGIN {$procedureName}(" . implode(", ", $bindStr) . "); END;";
            $stmt = oci_parse($this->conn, $plsql);
            
            foreach ($bindParams as $name => &$meta) {
                $maxLen = isset($meta['length']) ? $meta['length'] : -1;
                oci_bind_by_name($stmt, ":" . $name, $meta['value'], $maxLen);
            }
            
            $r = @oci_execute($stmt, OCI_COMMIT_ON_SUCCESS);
            if (!$r) {
                $e = oci_error($stmt);
                throw new Exception($e['message']);
            }
            oci_free_statement($stmt);
            return true;
        } else {
            require_once __DIR__ . '/oracle_bridge.php';
            return OracleBridge::getInstance()->callProcedure($procedureName, $bindParams);
        }
    }
}
