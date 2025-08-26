import os
from colorama import init, Fore, Style
from services.finance_service import FinanceService
from services.auth_service import AuthService
from utils.validators import validate_email, validate_amount
from utils.formatters import format_currency, format_date, format_transactions_table, format_budgets_table
from config.settings import settings

init()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPress Enter to continue...")

def print_header():
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Style.BRIGHT}{settings.APP_NAME}")
    print(f"{'='*60}{Style.RESET_ALL}")

def print_menu():
    print(f"\n{Fore.YELLOW}Main Menu:{Style.RESET_ALL}")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

def print_user_menu():
    print(f"\n{Fore.YELLOW}User Menu:{Style.RESET_ALL}")
    print("1. Add Transaction")
    print("2. View Transactions")
    print("3. Update Transaction")
    print("4. Delete Transaction")
    print("5. Create Budget")
    print("6. View Budgets")
    print("7. Delete Budget")
    print("8. Monthly Summary")
    print("9. Category Summary")
    print("10. Logout")

def register_user(auth, finance):
    print(f"\n{Fore.GREEN}User Registration{Style.RESET_ALL}")
    email = input("Enter email: ").strip()
    
    if not validate_email(email):
        print(f"{Fore.RED}Invalid email format{Style.RESET_ALL}")
        return
    
    password = input("Enter password: ").strip()
    if len(password) < 6:
        print(f"{Fore.RED}Password must be at least 6 characters{Style.RESET_ALL}")
        return
        
    name = input("Enter name: ").strip()
    if not name:
        print(f"{Fore.RED}Name cannot be empty{Style.RESET_ALL}")
        return
    
    print("Creating account...")
    result = auth.signup(email, password)
    
    if "error" in result:
        print(f"{Fore.RED}Registration failed: {result['error']}{Style.RESET_ALL}")
    else:
        user_id = result["localId"]
        user = finance.create_user(email, name, user_id)
        print(f"{Fore.GREEN}User registered successfully!{Style.RESET_ALL}")
        print(f"Welcome, {user.name}!")

def login_user(auth, finance):
    print(f"\n{Fore.GREEN}User Login{Style.RESET_ALL}")
    email = input("Enter email: ").strip()
    
    if not validate_email(email):
        print(f"{Fore.RED}Invalid email format{Style.RESET_ALL}")
        return False
    
    password = input("Enter password: ").strip()
    
    print("Signing in...")
    result = auth.signin(email, password)
    
    if "error" in result:
        print(f"{Fore.RED}Login failed: {result['error']}{Style.RESET_ALL}")
        return False
    else:
        user_id = result["localId"]
        user = finance.login_user(email, user_id)
        if user:
            print(f"{Fore.GREEN}Login successful!{Style.RESET_ALL}")
            print(f"Welcome back, {user.name}!")
            return True
        else:
            print(f"{Fore.RED}User not found in database{Style.RESET_ALL}")
            return False

def add_transaction(finance):
    print(f"\n{Fore.GREEN}Add Transaction{Style.RESET_ALL}")
    
    # Get transaction type
    print("Transaction Types:")
    for i, t_type in enumerate(settings.TRANSACTION_TYPES, 1):
        print(f"{i}. {t_type.title()}")
    
    try:
        type_choice = int(input("Select transaction type: "))
        transaction_type = settings.TRANSACTION_TYPES[type_choice - 1]
    except (ValueError, IndexError):
        print(f"{Fore.RED}Invalid transaction type{Style.RESET_ALL}")
        return
    
    # Get amount
    amount_str = input("Enter amount: $")
    is_valid, amount_or_msg = validate_amount(amount_str)
    if not is_valid:
        print(f"{Fore.RED}{amount_or_msg}{Style.RESET_ALL}")
        return
    amount = amount_or_msg
    
    # Get category
    categories = settings.INCOME_CATEGORIES if transaction_type == 'income' else settings.EXPENSE_CATEGORIES
    print(f"\n{transaction_type.title()} Categories:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category.title()}")
    
    try:
        cat_choice = int(input("Select category: "))
        category = categories[cat_choice - 1]
    except (ValueError, IndexError):
        print(f"{Fore.RED}Invalid category{Style.RESET_ALL}")
        return
    
    # Get description
    description = input("Enter description (optional): ").strip()
    if not description:
        description = f"{transaction_type.title()} - {category.title()}"
    
    try:
        transaction = finance.add_transaction(amount, category, description, transaction_type)
        print(f"{Fore.GREEN}Transaction added successfully!{Style.RESET_ALL}")
        print(f"ID: {transaction.id}")
        print(f"Amount: {format_currency(transaction.amount)}")
        print(f"Type: {transaction.transaction_type.title()}")
        print(f"Category: {transaction.category.title()}")
    except Exception as e:
        print(f"{Fore.RED}Error adding transaction: {e}{Style.RESET_ALL}")

def view_transactions(finance):
    print(f"\n{Fore.GREEN}Your Transactions{Style.RESET_ALL}")
    transactions = finance.get_user_transactions()
    
    if not transactions:
        print("No transactions found.")
        return
    
    print(format_transactions_table(transactions))

def update_transaction(finance):
    print(f"\n{Fore.GREEN}Update Transaction{Style.RESET_ALL}")
    
    # Show current transactions
    transactions = finance.get_user_transactions()
    if not transactions:
        print("No transactions found.")
        return
    
    print("Current transactions:")
    print(format_transactions_table(transactions))
    
    transaction_id = input("\nEnter the Firestore ID of the transaction to update: ").strip()
    
    # Get new values
    print("\nEnter new values (press Enter to keep current value):")
    
    # Get transaction type
    print("Transaction Types:")
    for i, t_type in enumerate(settings.TRANSACTION_TYPES, 1):
        print(f"{i}. {t_type.title()}")
    
    try:
        type_choice = int(input("Select transaction type: "))
        transaction_type = settings.TRANSACTION_TYPES[type_choice - 1]
    except (ValueError, IndexError):
        print(f"{Fore.RED}Invalid transaction type{Style.RESET_ALL}")
        return
    
    # Get amount
    amount_str = input("Enter new amount: $")
    if not validate_amount(amount_str):
        print(f"{Fore.RED}Invalid amount{Style.RESET_ALL}")
        return
    amount = float(amount_str)
    
    # Get category
    categories = settings.INCOME_CATEGORIES if transaction_type == 'income' else settings.EXPENSE_CATEGORIES
    print(f"\n{transaction_type.title()} Categories:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category.title()}")
    
    try:
        cat_choice = int(input("Select category: "))
        category = categories[cat_choice - 1]
    except (ValueError, IndexError):
        print(f"{Fore.RED}Invalid category{Style.RESET_ALL}")
        return
    
    description = input("Enter new description: ").strip()
    
    try:
        finance.update_transaction(transaction_id, amount, category, description, transaction_type)
        print(f"{Fore.GREEN}Transaction updated successfully!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error updating transaction: {e}{Style.RESET_ALL}")

def delete_transaction(finance):
    print(f"\n{Fore.GREEN}Delete Transaction{Style.RESET_ALL}")
    
    # Show current transactions
    transactions = finance.get_user_transactions()
    if not transactions:
        print("No transactions found.")
        return
    
    print("Current transactions:")
    print(format_transactions_table(transactions))
    
    transaction_id = input("\nEnter the Firestore ID of the transaction to delete: ").strip()
    
    confirm = input(f"Are you sure you want to delete transaction {transaction_id}? (Y/N): ").strip().lower()
    if confirm == 'y':
        try:
            finance.delete_transaction(transaction_id)
            print(f"{Fore.GREEN}Transaction deleted successfully!{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error deleting transaction: {e}{Style.RESET_ALL}")
    else:
        print("Delete cancelled.")

def create_budget(finance):
    print(f"\n{Fore.GREEN}Create Budget{Style.RESET_ALL}")
    
    # Get category
    print("Expense Categories:")
    for i, category in enumerate(settings.EXPENSE_CATEGORIES, 1):
        print(f"{i}. {category.title()}")
    
    try:
        cat_choice = int(input("Select category: "))
        category = settings.EXPENSE_CATEGORIES[cat_choice - 1]
    except (ValueError, IndexError):
        print(f"{Fore.RED}Invalid category{Style.RESET_ALL}")
        return
    
    # Get amount
    amount_str = input("Enter budget amount: $")
    if not validate_amount(amount_str):
        print(f"{Fore.RED}Invalid amount{Style.RESET_ALL}")
        return
    amount = float(amount_str)
    
    # Get month and year
    try:
        month = int(input("Enter month (1-12): "))
        if month < 1 or month > 12:
            raise ValueError
    except ValueError:
        print(f"{Fore.RED}Invalid month{Style.RESET_ALL}")
        return
    
    try:
        year = int(input("Enter year (e.g., 2024): "))
        if year < 2020 or year > 2030:
            raise ValueError
    except ValueError:
        print(f"{Fore.RED}Invalid year{Style.RESET_ALL}")
        return
    
    try:
        budget = finance.create_budget(category, amount, month, year)
        print(f"{Fore.GREEN}Budget created successfully!{Style.RESET_ALL}")
        print(f"Category: {budget.category.title()}")
        print(f"Amount: {format_currency(budget.amount)}")
        print(f"Period: {budget.month}/{budget.year}")
    except Exception as e:
        print(f"{Fore.RED}Error creating budget: {e}{Style.RESET_ALL}")

def view_budgets(finance):
    print(f"\n{Fore.GREEN}Your Budgets{Style.RESET_ALL}")
    budgets = finance.get_user_budgets()
    
    if not budgets:
        print("No budgets found.")
        return
    
    print(format_budgets_table(budgets))

def delete_budget(finance):
    print(f"\n{Fore.GREEN}Delete Budget{Style.RESET_ALL}")
    
    budgets = finance.get_user_budgets()
    if not budgets:
        print("No budgets found.")
        return
    
    print("Current budgets:")
    print(format_budgets_table(budgets))
    
    budget_id = input("\nEnter the ID of the budget to delete: ").strip()
    
    confirm = input(f"Are you sure you want to delete budget {budget_id}? (y/N): ").strip().lower()
    if confirm == 'y':
        try:
            finance.delete_budget(budget_id)
            print(f"{Fore.GREEN}Budget deleted successfully!{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error deleting budget: {e}{Style.RESET_ALL}")
    else:
        print("Delete cancelled.")

def monthly_summary(finance):
    print(f"\n{Fore.GREEN}Monthly Summary{Style.RESET_ALL}")
    
    try:
        month = int(input("Enter month (1-12): "))
        if month < 1 or month > 12:
            raise ValueError
    except ValueError:
        print(f"{Fore.RED}Invalid month{Style.RESET_ALL}")
        return
    
    try:
        year = int(input("Enter year (e.g., 2024): "))
        if year < 2020 or year > 2030:
            raise ValueError
    except ValueError:
        print(f"{Fore.RED}Invalid year{Style.RESET_ALL}")
        return
    
    summary = finance.get_monthly_summary(month, year)
    
    print(f"\n{Fore.CYAN}Summary for {month}/{year}:{Style.RESET_ALL}")
    print(f"Total Income: {format_currency(summary['total_income'])}")
    print(f"Total Expenses: {format_currency(summary['total_expenses'])}")
    print(f"Net Income: {format_currency(summary['net_income'])}")
    print(f"Transaction Count: {summary['transaction_count']}")

def category_summary(finance):
    print(f"\n{Fore.GREEN}Category Summary{Style.RESET_ALL}")
    
    summary = finance.get_category_summary()
    
    if not summary:
        print("No expense data found.")
        return
    
    print(f"\n{Fore.CYAN}Expenses by Category:{Style.RESET_ALL}")
    for category, amount in sorted(summary.items(), key=lambda x: x[1], reverse=True):
        print(f"{category.title()}: {format_currency(amount)}")

def main():
    # Initialize services
    finance = FinanceService()
    auth = AuthService()
    
    while True:
        clear_screen()
        print_header()
        
        if not finance.get_current_user():
            print_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                register_user(auth, finance)
                pause()
            elif choice == '2':
                if login_user(auth, finance):
                    pause()
            elif choice == '3':
                print(f"{Fore.YELLOW}Thank you for using {settings.APP_NAME}!{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
                pause()
        else:
            current_user = finance.get_current_user()
            print(f"\n{Fore.GREEN}Logged in as: {current_user.name} ({current_user.email}){Style.RESET_ALL}")
            
            print_user_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                add_transaction(finance)
                pause()
            elif choice == '2':
                view_transactions(finance)
                pause()
            elif choice == '3':
                update_transaction(finance)
                pause()
            elif choice == '4':
                delete_transaction(finance)
                pause()
            elif choice == '5':
                create_budget(finance)
                pause()
            elif choice == '6':
                view_budgets(finance)
                pause()
            elif choice == '7':
                delete_budget(finance)
                pause()
            elif choice == '8':
                monthly_summary(finance)
                pause()
            elif choice == '9':
                category_summary(finance)
                pause()
            elif choice == '10':
                finance.current_user = None
                print(f"{Fore.YELLOW}Logged out successfully!{Style.RESET_ALL}")
                pause()
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
                pause()

if __name__ == "__main__":
    try:
        settings.validate_config()
        main()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        input("Press Enter to exit...")