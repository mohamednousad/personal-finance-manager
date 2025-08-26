from datetime import datetime

class Transaction:
    def __init__(self, user_id, amount, category, description, transaction_type, transaction_id=None):
        self.id = transaction_id
        self.user_id = user_id
        self.amount = float(amount)
        self.category = category
        self.description = description
        self.transaction_type = transaction_type  # 'income' or 'expense'
        self.date = datetime.now()

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'transaction_type': self.transaction_type,
            'date': self.date
        }

    @staticmethod
    def from_dict(data, transaction_id=None):
        transaction = Transaction(
            data['user_id'],
            data['amount'],
            data['category'],
            data['description'],
            data['transaction_type'],
            transaction_id
        )
        if 'date' in data:
            transaction.date = data['date']
        return transaction