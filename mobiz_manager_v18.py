# ==============================
# MoBiz Manager v18 - Stable Version
# ==============================

import os
import csv
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# Try to import matplotlib (for charts)
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except:
    MATPLOTLIB_AVAILABLE = False

VERSION = "v18"

INCOME_FILE = f"income_log_{VERSION}.txt"
EXPENSE_FILE = f"expense_log_{VERSION}.txt"
CSV_FILE = f"mobiz_export_{VERSION}.csv"

README_TEXT = """
MoBiz Manager v18 - Stable Version

Features:
- Dashboard Overview
- Add / View Income
- Add / View Expenses
- Profit Summary
- Monthly / Yearly Summary
- Project / Job Calculator
- Export to CSV
- Income vs Expense Chart
- Expense Category Pie Chart
"""

# -----------------------------
# Helpers
# -----------------------------
def safe_float(value):
    try:
        return float(value)
    except:
        return None

def read_log(file):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        return [line.strip().split("|") for line in f.readlines()]

def append_log(file, data):
    with open(file, "a") as f:
        f.write("|".join(data) + "\n")

# -----------------------------
# Main App
# -----------------------------
class MoBizApp:

    def __init__(self, root):
        self.root = root
        self.root.title("MoBiz Manager v18 - Stable")
        self.root.geometry("600x700")
        self.create_widgets()
        self.update_dashboard()

    def create_widgets(self):

        # Dashboard
        dash = ttk.LabelFrame(self.root, text="Dashboard")
        dash.pack(fill="x", padx=10, pady=10)

        self.income_label = ttk.Label(dash, text="Income: 0.00")
        self.income_label.pack(anchor="w", padx=10)

        self.expense_label = ttk.Label(dash, text="Expenses: 0.00")
        self.expense_label.pack(anchor="w", padx=10)

        self.profit_label = ttk.Label(dash, text="Net Profit: 0.00")
        self.profit_label.pack(anchor="w", padx=10)

        # Buttons
        actions = ttk.LabelFrame(self.root, text="Actions")
        actions.pack(fill="x", padx=10, pady=10)

        buttons = [
            ("Add Income", self.add_income),
            ("View Income", self.view_income),
            ("Add Expense", self.add_expense),
            ("View Expenses", self.view_expenses),
            ("Profit Summary", self.profit_summary),
            ("Monthly/Yearly Summary", self.monthly_summary),
            ("Project Calculator", self.project_calculator),
            ("Export CSV", self.export_csv),
            ("Income vs Expense Chart", self.line_chart),
            ("Expense Pie Chart", self.pie_chart),
            ("View README", self.show_readme),
            ("Exit", self.safe_exit),
        ]

        for text, command in buttons:
            ttk.Button(actions, text=text, command=command).pack(fill="x", pady=2)

    # -----------------------------
    # Dashboard Update
    # -----------------------------
    def update_dashboard(self):
        incomes = read_log(INCOME_FILE)
        expenses = read_log(EXPENSE_FILE)

        total_income = sum(float(i[2]) for i in incomes) if incomes else 0
        total_expense = sum(float(e[3]) for e in expenses) if expenses else 0
        net = total_income - total_expense

        self.income_label.config(text=f"Income: {total_income:.2f}")
        self.expense_label.config(text=f"Expenses: {total_expense:.2f}")
        self.profit_label.config(text=f"Net Profit: {net:.2f}")

    # -----------------------------
    # Income
    # -----------------------------
    def add_income(self):
        win = tk.Toplevel(self.root)
        win.title("Add Income")

        ttk.Label(win, text="Description").pack()
        desc = ttk.Entry(win)
        desc.pack()

        ttk.Label(win, text="Amount").pack()
        amt = ttk.Entry(win)
        amt.pack()

        def save():
            d = desc.get()
            a = safe_float(amt.get())
            if d and a is not None:
                date = datetime.now().strftime("%Y-%m-%d")
                append_log(INCOME_FILE, [date, d, str(a)])
                self.update_dashboard()
                messagebox.showinfo("Success", "Income Added")
                win.destroy()
            else:
                messagebox.showerror("Error", "Invalid Input")

        ttk.Button(win, text="Save", command=save).pack(pady=5)

    def view_income(self):
        self.show_records("Income Records", INCOME_FILE)

    # -----------------------------
    # Expense
    # -----------------------------
    def add_expense(self):
        win = tk.Toplevel(self.root)
        win.title("Add Expense")

        ttk.Label(win, text="Category").pack()
        cat = ttk.Entry(win)
        cat.pack()

        ttk.Label(win, text="Description").pack()
        desc = ttk.Entry(win)
        desc.pack()

        ttk.Label(win, text="Amount").pack()
        amt = ttk.Entry(win)
        amt.pack()

        def save():
            c = cat.get()
            d = desc.get()
            a = safe_float(amt.get())
            if c and d and a is not None:
                date = datetime.now().strftime("%Y-%m-%d")
                append_log(EXPENSE_FILE, [date, c, d, str(a)])
                self.update_dashboard()
                messagebox.showinfo("Success", "Expense Added")
                win.destroy()
            else:
                messagebox.showerror("Error", "Invalid Input")

        ttk.Button(win, text="Save", command=save).pack(pady=5)

    def view_expenses(self):
        self.show_records("Expense Records", EXPENSE_FILE)

    def show_records(self, title, file):
        win = tk.Toplevel(self.root)
        win.title(title)
        text = tk.Text(win, width=70, height=20)
        text.pack()
        records = read_log(file)
        for r in records:
            text.insert("end", " | ".join(r) + "\n")

    # -----------------------------
    # Profit Summary
    # -----------------------------
    def profit_summary(self):
        incomes = read_log(INCOME_FILE)
        expenses = read_log(EXPENSE_FILE)

        total_income = sum(float(i[2]) for i in incomes) if incomes else 0
        total_expense = sum(float(e[3]) for e in expenses) if expenses else 0
        net = total_income - total_expense

        messagebox.showinfo(
            "Profit Summary",
            f"Total Income: {total_income:.2f}\n"
            f"Total Expense: {total_expense:.2f}\n"
            f"Net Profit: {net:.2f}"
        )

    # -----------------------------
    # Monthly Summary
    # -----------------------------
    def monthly_summary(self):
        incomes = read_log(INCOME_FILE)
        expenses = read_log(EXPENSE_FILE)
        summary = {}

        for i in incomes:
            month = i[0][:7]
            summary.setdefault(month, [0, 0])
            summary[month][0] += float(i[2])

        for e in expenses:
            month = e[0][:7]
            summary.setdefault(month, [0, 0])
            summary[month][1] += float(e[3])

        result = ""
        for m, v in summary.items():
            result += f"{m} → Income: {v[0]:.2f}, Expense: {v[1]:.2f}, Net: {v[0]-v[1]:.2f}\n"

        messagebox.showinfo("Monthly Summary", result or "No Data")

    # -----------------------------
    # Project Calculator
    # -----------------------------
    def project_calculator(self):
        win = tk.Toplevel(self.root)
        win.title("Project Calculator")

        ttk.Label(win, text="Base Cost").pack()
        base = ttk.Entry(win)
        base.pack()

        ttk.Label(win, text="Profit %").pack()
        profit = ttk.Entry(win)
        profit.pack()

        ttk.Label(win, text="Tax %").pack()
        tax = ttk.Entry(win)
        tax.pack()

        def calculate():
            b = safe_float(base.get())
            p = safe_float(profit.get())
            t = safe_float(tax.get())
            if None in (b, p, t):
                messagebox.showerror("Error", "Invalid Input")
                return
            final = b + (b*p/100) + (b*t/100)
            messagebox.showinfo("Final Price", f"{final:.2f}")

        ttk.Button(win, text="Calculate", command=calculate).pack(pady=5)

    # -----------------------------
    # CSV Export
    # -----------------------------
    def export_csv(self):
        incomes = read_log(INCOME_FILE)
        expenses = read_log(EXPENSE_FILE)

        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Type", "Date", "Category", "Description", "Amount"])
            for i in incomes:
                writer.writerow(["Income", i[0], "", i[1], i[2]])
            for e in expenses:
                writer.writerow(["Expense", e[0], e[1], e[2], e[3]])

        messagebox.showinfo("Exported", f"Saved as {CSV_FILE}")

    # -----------------------------
    # Charts
    # -----------------------------
    def line_chart(self):
        if not MATPLOTLIB_AVAILABLE:
            messagebox.showerror("Error", "Matplotlib not installed")
            return

        incomes = read_log(INCOME_FILE)
        expenses = read_log(EXPENSE_FILE)

        total_income = sum(float(i[2]) for i in incomes) if incomes else 0
        total_expense = sum(float(e[3]) for e in expenses) if expenses else 0

        plt.bar(["Income", "Expense"], [total_income, total_expense])
        plt.title("Income vs Expense")
        plt.show()

    def pie_chart(self):
        if not MATPLOTLIB_AVAILABLE:
            messagebox.showerror("Error", "Matplotlib not installed")
            return

        expenses = read_log(EXPENSE_FILE)
        categories = {}

        for e in expenses:
            categories.setdefault(e[1], 0)
            categories[e[1]] += float(e[3])

        if not categories:
            messagebox.showinfo("Info", "No Expenses")
            return

        plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
        plt.title("Expense Categories")
        plt.show()

    # -----------------------------
    # README
    # -----------------------------
    def show_readme(self):
        win = tk.Toplevel(self.root)
        win.title("README")
        text = tk.Text(win, width=80, height=25)
        text.pack(expand=True, fill="both")
        text.insert("1.0", README_TEXT)

    # -----------------------------
    # Safe Exit
    # -----------------------------
    def safe_exit(self):
        if messagebox.askyesno("Exit", "Close MoBiz Manager?"):
            self.root.destroy()

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MoBizApp(root)
    root.mainloop()