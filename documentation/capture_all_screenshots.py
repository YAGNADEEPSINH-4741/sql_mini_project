import subprocess
import time
import os
from playwright.sync_api import sync_playwright

def main():
    screenshots_dir = r"d:\college\RDBMS\mini_project\documentation\screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    # Launch PHP server from project root
    php_exe = r"C:\xampp\php\php.exe"
    php_proc = subprocess.Popen([php_exe, "-S", "127.0.0.1:8088", "-t", r"d:\college\RDBMS\mini_project"])
    time.sleep(2)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1280, "height": 800})

            # 1. Login Page
            print("Capturing 01_login.png...")
            page.goto("http://127.0.0.1:8088/frontend/pages/login.php")
            page.wait_for_timeout(1000)
            page.screenshot(path=os.path.join(screenshots_dir, "01_login.png"))

            # 2. Dashboard
            print("Capturing 02_dashboard.png...")
            page.goto("http://127.0.0.1:8088/frontend/pages/dashboard.php?demo_auth=1")
            page.wait_for_timeout(1500)
            page.screenshot(path=os.path.join(screenshots_dir, "02_dashboard.png"))

            # Project Team Modal
            print("Capturing 16_project_team_modal.png...")
            btn = page.query_selector("button[data-bs-target='#projectTeamModal']")
            if btn:
                btn.click()
                page.wait_for_timeout(800)
                page.screenshot(path=os.path.join(screenshots_dir, "16_project_team_modal.png"))
                page.keyboard.press("Escape")
                page.wait_for_timeout(400)

            # 3. Customers
            print("Capturing 03_customers.png...")
            page.goto("http://127.0.0.1:8088/frontend/pages/customers.php?demo_auth=1")
            page.wait_for_timeout(1200)
            page.screenshot(path=os.path.join(screenshots_dir, "03_customers.png"))

            # Customer Modal
            print("Capturing 04_customer_modal.png...")
            btn = page.query_selector("button[data-bs-target='#newCustomerModal']")
            if btn:
                btn.click()
                page.wait_for_timeout(800)
                page.screenshot(path=os.path.join(screenshots_dir, "04_customer_modal.png"))
                page.keyboard.press("Escape")
                page.wait_for_timeout(400)

            # 4. Accounts
            print("Capturing 05_accounts.png...")
            page.goto("http://127.0.0.1:8088/frontend/pages/accounts.php?demo_auth=1")
            page.wait_for_timeout(1200)
            page.screenshot(path=os.path.join(screenshots_dir, "05_accounts.png"))

            # Account Modal
            print("Capturing 06_account_modal.png...")
            btn = page.query_selector("button[data-bs-target='#newAccountModal']")
            if btn:
                btn.click()
                page.wait_for_timeout(800)
                page.screenshot(path=os.path.join(screenshots_dir, "06_account_modal.png"))
                page.keyboard.press("Escape")
                page.wait_for_timeout(400)

            # 5. Transactions
            print("Capturing 07_transactions.png...")
            page.goto("http://127.0.0.1:8088/frontend/pages/transactions.php?demo_auth=1")
            page.wait_for_timeout(1200)
            page.screenshot(path=os.path.join(screenshots_dir, "07_transactions.png"))

            # Deposit Modal
            print("Capturing 08_deposit_modal.png...")
            btn = page.query_selector("button[data-bs-target='#depositModal']")
            if btn:
                btn.click()
                page.wait_for_timeout(800)
                page.screenshot(path=os.path.join(screenshots_dir, "08_deposit_modal.png"))
                page.keyboard.press("Escape")
                page.wait_for_timeout(400)

            # Transfer Modal
            print("Capturing 09_money_transfer.png...")
            btn = page.query_selector("button[data-bs-target='#transferModal']")
            if btn:
                btn.click()
                page.wait_for_timeout(800)
                page.screenshot(path=os.path.join(screenshots_dir, "09_money_transfer.png"))
                page.keyboard.press("Escape")
                page.wait_for_timeout(400)

            # 6. Beneficiaries
            print("Capturing 10_beneficiaries.png...")
            page.goto("http://127.0.0.1:8088/frontend/pages/beneficiaries.php?demo_auth=1")
            page.wait_for_timeout(1200)
            page.screenshot(path=os.path.join(screenshots_dir, "10_beneficiaries.png"))

            # Beneficiary Modal
            print("Capturing 11_beneficiary_modal.png...")
            btn = page.query_selector("button[data-bs-target='#newBeneficiaryModal']")
            if btn:
                btn.click()
                page.wait_for_timeout(800)
                page.screenshot(path=os.path.join(screenshots_dir, "11_beneficiary_modal.png"))
                page.keyboard.press("Escape")
                page.wait_for_timeout(400)

            # 7. Loans
            print("Capturing 12_loans.png...")
            page.goto("http://127.0.0.1:8088/frontend/pages/loans.php?demo_auth=1")
            page.wait_for_timeout(1200)
            page.screenshot(path=os.path.join(screenshots_dir, "12_loans.png"))

            # Loan Modal
            print("Capturing 13_loan_modal.png...")
            btn = page.query_selector("button[data-bs-target='#newLoanModal']")
            if btn:
                btn.click()
                page.wait_for_timeout(800)
                page.screenshot(path=os.path.join(screenshots_dir, "13_loan_modal.png"))
                page.keyboard.press("Escape")
                page.wait_for_timeout(400)

            # 8. Reports
            print("Capturing 14_reports.png...")
            page.goto("http://127.0.0.1:8088/frontend/pages/reports.php?demo_auth=1")
            page.wait_for_timeout(1200)
            page.screenshot(path=os.path.join(screenshots_dir, "14_reports.png"))

            # 9. Audit Logs
            print("Capturing 15_audit_logs.png...")
            page.goto("http://127.0.0.1:8088/frontend/pages/audit_logs.php?demo_auth=1")
            page.wait_for_timeout(1200)
            page.screenshot(path=os.path.join(screenshots_dir, "15_audit_logs.png"))

            browser.close()
            print("All screenshots successfully captured!")
    finally:
        php_proc.terminate()

if __name__ == "__main__":
    main()
