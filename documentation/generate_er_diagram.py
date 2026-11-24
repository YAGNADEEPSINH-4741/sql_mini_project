import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def create_er_diagram():
    fig, ax = plt.subplots(figsize=(20, 14), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Color Palette
    bg_color = "#f8fafc"
    header_color = "#1e293b"
    pk_color = "#dc2626"
    fk_color = "#2563eb"
    normal_color = "#334155"
    border_color = "#cbd5e1"
    box_bg = "#ffffff"

    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    # Title Banner
    ax.text(50, 97, "SMART BANKING MANAGEMENT SYSTEM - RELATIONAL ER DIAGRAM", 
            ha='center', va='center', fontsize=20, fontweight='bold', color='#0f172a', fontfamily='sans-serif')
    ax.text(50, 94.5, "Oracle Database 10g/11g/19c/23ai Schema Architecture (3NF Normalized Relational Model)", 
            ha='center', va='center', fontsize=12, color='#64748b', fontfamily='sans-serif')

    # Tables definition: [name, x, y, width, height, columns]
    tables = [
        {
            "name": "CUSTOMERS", "x": 5, "y": 62, "w": 22, "h": 26,
            "cols": [
                ("PK", "CUSTOMER_ID", "NUMBER(10)"),
                (" ", "FIRST_NAME", "VARCHAR2(50)"),
                (" ", "LAST_NAME", "VARCHAR2(50)"),
                ("UQ", "EMAIL", "VARCHAR2(100)"),
                ("UQ", "PHONE", "VARCHAR2(20)"),
                (" ", "DATE_OF_BIRTH", "DATE"),
                (" ", "GENDER", "VARCHAR2(10)"),
                (" ", "ADDRESS", "VARCHAR2(255)"),
                (" ", "CITY", "VARCHAR2(50)"),
                (" ", "STATE", "VARCHAR2(50)"),
                (" ", "PIN_CODE", "VARCHAR2(10)"),
                (" ", "KYC_STATUS", "VARCHAR2(20)"),
                (" ", "CREATED_AT", "DATE")
            ]
        },
        {
            "name": "BANK_BRANCHES", "x": 38, "y": 70, "w": 22, "h": 20,
            "cols": [
                ("PK", "BRANCH_ID", "NUMBER(10)"),
                (" ", "BRANCH_NAME", "VARCHAR2(100)"),
                ("UQ", "BRANCH_CODE", "VARCHAR2(20)"),
                ("UQ", "IFSC_CODE", "VARCHAR2(20)"),
                (" ", "ADDRESS", "VARCHAR2(255)"),
                (" ", "CITY", "VARCHAR2(50)"),
                (" ", "STATE", "VARCHAR2(50)"),
                (" ", "MANAGER_NAME", "VARCHAR2(100)"),
                (" ", "CREATED_AT", "DATE")
            ]
        },
        {
            "name": "EMPLOYEES", "x": 72, "y": 72, "w": 22, "h": 18,
            "cols": [
                ("PK", "EMPLOYEE_ID", "NUMBER(10)"),
                ("FK", "BRANCH_ID", "NUMBER(10)"),
                (" ", "FIRST_NAME", "VARCHAR2(50)"),
                (" ", "LAST_NAME", "VARCHAR2(50)"),
                ("UQ", "EMAIL", "VARCHAR2(100)"),
                (" ", "ROLE", "VARCHAR2(50)"),
                (" ", "SALARY", "NUMBER(12,2)"),
                (" ", "STATUS", "VARCHAR2(20)")
            ]
        },
        {
            "name": "ACCOUNT_TYPES", "x": 72, "y": 42, "w": 22, "h": 16,
            "cols": [
                ("PK", "TYPE_ID", "NUMBER(5)"),
                ("UQ", "TYPE_NAME", "VARCHAR2(50)"),
                (" ", "MIN_BALANCE", "NUMBER(12,2)"),
                (" ", "INTEREST_RATE", "NUMBER(5,2)"),
                (" ", "OVERDRAFT_ALLOWED", "VARCHAR2(1)"),
                (" ", "DESCRIPTION", "VARCHAR2(255)")
            ]
        },
        {
            "name": "BANK_ACCOUNTS", "x": 38, "y": 36, "w": 23, "h": 24,
            "cols": [
                ("PK", "ACCOUNT_ID", "NUMBER(10)"),
                ("UQ", "ACCOUNT_NUMBER", "VARCHAR2(20)"),
                ("FK", "CUSTOMER_ID", "NUMBER(10)"),
                ("FK", "BRANCH_ID", "NUMBER(10)"),
                ("FK", "TYPE_ID", "NUMBER(5)"),
                (" ", "BALANCE", "NUMBER(15,2)"),
                (" ", "OVERDRAFT_LIMIT", "NUMBER(12,2)"),
                (" ", "ACCOUNT_STATUS", "VARCHAR2(20)"),
                (" ", "OPENED_DATE", "DATE"),
                (" ", "UPDATED_AT", "DATE")
            ]
        },
        {
            "name": "BENEFICIARIES", "x": 5, "y": 34, "w": 22, "h": 18,
            "cols": [
                ("PK", "BENEFICIARY_ID", "NUMBER(10)"),
                ("FK", "CUSTOMER_ID", "NUMBER(10)"),
                (" ", "BENEFICIARY_NAME", "VARCHAR2(100)"),
                (" ", "BENEFICIARY_ACCOUNT", "VARCHAR2(20)"),
                (" ", "BANK_NAME", "VARCHAR2(100)"),
                (" ", "IFSC_CODE", "VARCHAR2(20)"),
                (" ", "TRANSFER_LIMIT", "NUMBER(12,2)"),
                (" ", "STATUS", "VARCHAR2(20)")
            ]
        },
        {
            "name": "TRANSACTIONS", "x": 38, "y": 4, "w": 23, "h": 23,
            "cols": [
                ("PK", "TRANSACTION_ID", "NUMBER(12)"),
                ("UQ", "TRANSACTION_REF", "VARCHAR2(30)"),
                ("FK", "ACCOUNT_ID", "NUMBER(10)"),
                (" ", "TRANSACTION_TYPE", "VARCHAR2(25)"),
                (" ", "AMOUNT", "NUMBER(15,2)"),
                (" ", "BALANCE_AFTER", "NUMBER(15,2)"),
                ("FK", "RELATED_ACCOUNT_ID", "NUMBER(10)"),
                (" ", "TRANSACTION_DATE", "TIMESTAMP"),
                (" ", "DESCRIPTION", "VARCHAR2(255)"),
                (" ", "TRANSACTION_STATUS", "VARCHAR2(20)")
            ]
        },
        {
            "name": "LOANS", "x": 5, "y": 4, "w": 22, "h": 22,
            "cols": [
                ("PK", "LOAN_ID", "NUMBER(10)"),
                ("UQ", "LOAN_NUMBER", "VARCHAR2(20)"),
                ("FK", "CUSTOMER_ID", "NUMBER(10)"),
                ("FK", "BRANCH_ID", "NUMBER(10)"),
                (" ", "LOAN_TYPE", "VARCHAR2(50)"),
                (" ", "LOAN_AMOUNT", "NUMBER(15,2)"),
                (" ", "INTEREST_RATE", "NUMBER(5,2)"),
                (" ", "TERM_MONTHS", "NUMBER(5)"),
                (" ", "MONTHLY_EMI", "NUMBER(12,2)"),
                (" ", "OUTSTANDING_BALANCE", "NUMBER(15,2)"),
                (" ", "LOAN_STATUS", "VARCHAR2(20)")
            ]
        },
        {
            "name": "LOAN_PAYMENTS", "x": 72, "y": 4, "w": 22, "h": 18,
            "cols": [
                ("PK", "PAYMENT_ID", "NUMBER(10)"),
                ("UQ", "PAYMENT_REF", "VARCHAR2(30)"),
                ("FK", "LOAN_ID", "NUMBER(10)"),
                (" ", "PAYMENT_AMOUNT", "NUMBER(12,2)"),
                (" ", "PRINCIPAL_COMPONENT", "NUMBER(12,2)"),
                (" ", "INTEREST_COMPONENT", "NUMBER(12,2)"),
                (" ", "PAYMENT_DATE", "DATE"),
                (" ", "PAYMENT_STATUS", "VARCHAR2(20)")
            ]
        },
        {
            "name": "AUDIT_LOGS", "x": 72, "y": 24, "w": 22, "h": 15,
            "cols": [
                ("PK", "LOG_ID", "NUMBER(12)"),
                (" ", "TABLE_NAME", "VARCHAR2(50)"),
                (" ", "OPERATION_TYPE", "VARCHAR2(10)"),
                (" ", "RECORD_ID", "VARCHAR2(50)"),
                (" ", "CHANGED_BY", "VARCHAR2(50)"),
                (" ", "CHANGED_AT", "TIMESTAMP"),
                (" ", "CLIENT_IP", "VARCHAR2(50)")
            ]
        }
    ]

    # Draw Each Table Box
    for t in tables:
        x, y, w, h = t["x"], t["y"], t["w"], t["h"]
        # Outer box
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4", 
                                      facecolor=box_bg, edgecolor=border_color, linewidth=1.5, zorder=2)
        ax.add_patch(rect)

        # Header box
        header_h = 2.6
        header_rect = patches.FancyBboxPatch((x, y + h - header_h), w, header_h, boxstyle="round,pad=0.2", 
                                            facecolor=header_color, edgecolor=header_color, zorder=3)
        ax.add_patch(header_rect)
        ax.text(x + w/2, y + h - header_h/2, t["name"], color="#ffffff", 
                ha='center', va='center', fontsize=11, fontweight='bold', zorder=4)

        # Columns
        col_y = y + h - header_h - 1.2
        step = (h - header_h - 1) / max(len(t["cols"]), 1)
        for key_type, col_name, data_type in t["cols"]:
            # Key Tag
            if key_type == "PK":
                k_col = pk_color
            elif key_type == "FK":
                k_col = fk_color
            elif key_type == "UQ":
                k_col = "#d97706"
            else:
                k_col = "#94a3b8"

            ax.text(x + 1.2, col_y, key_type, color=k_col, fontsize=7.5, fontweight='bold', va='center', zorder=4)
            ax.text(x + 3.8, col_y, col_name, color=normal_color, fontsize=8, fontweight='bold' if key_type in ['PK', 'FK'] else 'normal', va='center', zorder=4)
            ax.text(x + w - 1.2, col_y, data_type, color="#64748b", fontsize=7.2, ha='right', va='center', zorder=4)
            col_y -= step

    # Relationships Connectors (Arrows / Lines)
    def draw_rel(x1, y1, x2, y2, label="1 : N"):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#3b82f6", lw=1.6, 
                                    connectionstyle="arc3,rad=0.08"), zorder=1)
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.text(mx, my + 0.6, label, fontsize=7.5, color="#1e40af", fontweight='bold', 
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#dbeafe", edgecolor="none"), zorder=5)

    # 1. CUSTOMERS (1) -> BANK_ACCOUNTS (N)
    draw_rel(27, 72, 38, 55, "1 : N")

    # 2. BANK_BRANCHES (1) -> BANK_ACCOUNTS (N)
    draw_rel(49, 70, 49, 60, "1 : N")

    # 3. ACCOUNT_TYPES (1) -> BANK_ACCOUNTS (N)
    draw_rel(72, 50, 61, 50, "1 : N")

    # 4. BANK_ACCOUNTS (1) -> TRANSACTIONS (N)
    draw_rel(49, 36, 49, 27, "1 : N")

    # 5. CUSTOMERS (1) -> BENEFICIARIES (N)
    draw_rel(16, 62, 16, 52, "1 : N")

    # 6. CUSTOMERS (1) -> LOANS (N)
    draw_rel(10, 62, 10, 26, "1 : N")

    # 7. LOANS (1) -> LOAN_PAYMENTS (N)
    draw_rel(27, 14, 72, 14, "1 : N")

    # 8. BANK_BRANCHES (1) -> EMPLOYEES (N)
    draw_rel(60, 80, 72, 80, "1 : N")

    # Legend at bottom right
    leg_x, leg_y = 6, 92
    ax.text(leg_x, leg_y, "Key Types: ", fontsize=9, fontweight='bold', color="#0f172a")
    ax.text(leg_x + 6, leg_y, "PK = Primary Key", fontsize=8.5, color=pk_color, fontweight='bold')
    ax.text(leg_x + 18, leg_y, "FK = Foreign Key", fontsize=8.5, color=fk_color, fontweight='bold')
    ax.text(leg_x + 30, leg_y, "UQ = Unique Key", fontsize=8.5, color="#d97706", fontweight='bold')
    ax.text(leg_x + 42, leg_y, "Lines = 1:N Referential Integrity (FK)", fontsize=8.5, color="#2563eb", fontweight='bold')

    plt.tight_layout()
    out_file = r'd:\college\RDBMS\mini_project\documentation\ER_DIAGRAM.png'
    plt.savefig(out_file, dpi=300, facecolor=bg_color, bbox_inches='tight')
    plt.close()
    print("ER Diagram successfully generated at:", out_file)

if __name__ == "__main__":
    create_er_diagram()
