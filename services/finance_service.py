from services.firebase_service import FirebaseService
from models.user import User
from models.transaction import Transaction
from models.budget import Budget

class FinanceService:
    def __init__(self):
        self.firebase = FirebaseService()
        self.current_user = None

    def create_user(self, email, name, user_id):
        user = User(email, name, user_id)
        self.firebase.add_document('users', user.to_dict(), doc_id=user_id)
        self.current_user = user
        return user

    def login_user(self, email, user_id):
        user_data = self.firebase.get_document('users', user_id)
        if user_data and user_data['email'] == email:
            user = User.from_dict(user_data)
            self.current_user = user
            return user
        return None

    def get_current_user(self):
        return self.current_user

    def add_transaction(self, amount, category, description, transaction_type):
        if not self.current_user:
            raise Exception("No user logged in")
        transaction = Transaction(
            self.current_user.id,
            amount,
            category,
            description,
            transaction_type
        )
        transaction_id = self.firebase.add_document('transactions', transaction.to_dict())
        transaction.id = transaction_id
        return transaction

    def get_user_transactions(self):
        if not self.current_user:
            return []
        transactions_data = self.firebase.query_documents(
            'transactions', 'user_id', '==', self.current_user.id
        )
        transactions = []
        for data in transactions_data:
            transaction = Transaction.from_dict(data, data['id'])
            transactions.append(transaction)
        transactions.sort(key=lambda x: x.date, reverse=True)
        return transactions

    def update_transaction(self, transaction_id, amount, category, description, transaction_type):
        update_data = {
            'amount': float(amount),
            'category': category,
            'description': description,
            'transaction_type': transaction_type
        }
        self.firebase.update_document('transactions', transaction_id, update_data)

    def delete_transaction(self, transaction_id):
        self.firebase.delete_document('transactions', transaction_id)

    def create_budget(self, category, amount, month, year):
        if not self.current_user:
            raise Exception("No user logged in")
        budget = Budget(self.current_user.id, category, amount, month, year)
        budget_id = self.firebase.add_document('budgets', budget.to_dict())
        budget.id = budget_id
        return budget

    def get_user_budgets(self):
        if not self.current_user:
            return []
        budgets_data = self.firebase.query_documents(
            'budgets', 'user_id', '==', self.current_user.id
        )
        budgets = []
        for data in budgets_data:
            budget = Budget.from_dict(data, data['id'])
            budgets.append(budget)
        return budgets

    def delete_budget(self, budget_id):
        self.firebase.delete_document('budgets', budget_id)

    def get_monthly_summary(self, month, year):
        transactions = self.get_user_transactions()
        monthly_transactions = [
            t for t in transactions
            if t.date.month == month and t.date.year == year
        ]
        total_income = sum(t.amount for t in monthly_transactions if t.transaction_type == 'income')
        total_expenses = sum(t.amount for t in monthly_transactions if t.transaction_type == 'expense')
        return {
            'month': month,
            'year': year,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_income': total_income - total_expenses,
            'transaction_count': len(monthly_transactions)
        }

    def get_category_summary(self):
        transactions = self.get_user_transactions()
        category_totals = {}
        for transaction in transactions:
            if transaction.transaction_type == 'expense':
                if transaction.category not in category_totals:
                    category_totals[transaction.category] = 0
                category_totals[transaction.category] += transaction.amount
        return category_totals