from tabulate import tabulate
from datetime import datetime

def format_currency(amount):
    return f"${amount:.2f}"

def format_date(date):
    if isinstance(date, datetime):
        return date.strftime("%Y-%m-%d %H:%M")
    return str(date)

def format_transactions_table(transactions):
    if not transactions:
        return "No transactions found."
    headers = ["Firestore ID", "Date", "Type", "Category", "Description", "Amount"]
    rows = []
    for transaction in transactions:
        rows.append([
            transaction.id,
            format_date(transaction.date),
            transaction.transaction_type.title(),
            transaction.category.title(),
            transaction.description[:30] + "..." if len(transaction.description) > 30 else transaction.description,
            format_currency(transaction.amount)
        ])
    return tabulate(rows, headers=headers, tablefmt="grid")

def format_budgets_table(budgets):
    if not budgets:
        return "No budgets found."
    headers = ["ID", "Category", "Amount", "Month", "Year"]
    rows = []
    for i, budget in enumerate(budgets, 1):
        rows.append([
            i,
            budget.category.title(),
            format_currency(budget.amount),
            budget.month,
            budget.year
        ])
    return tabulate(rows, headers=headers, tablefmt="grid")

def format_summary_report(summary):
    report = f"""
Monthly Summary for {summary['month']}/{summary['year']}
{'='*40}
Total Income:     {format_currency(summary['total_income'])}
Total Expenses:   {format_currency(summary['total_expenses'])}
Net Income:       {format_currency(summary['net_income'])}
Transactions:     {summary['transaction_count']}
"""
    return report

def format_category_report(category_totals):
    if not category_totals:
        return "No expense data found."
    headers = ["Category", "Total Spent"]
    rows = []
    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    for category, amount in sorted_categories:
        rows.append([category.title(), format_currency(amount)])
    total_spent = sum(category_totals.values())
    rows.append(["TOTAL", format_currency(total_spent)])
    return tabulate(rows, headers=headers, tablefmt="grid")