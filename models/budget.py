from datetime import datetime

class Budget:
    def __init__(self, user_id, category, amount, month, year, budget_id=None):
        self.id = budget_id
        self.user_id = user_id
        self.category = category
        self.amount = float(amount)
        self.month = month
        self.year = year
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'category': self.category,
            'amount': self.amount,
            'month': self.month,
            'year': self.year,
            'created_at': self.created_at
        }

    @staticmethod
    def from_dict(data, budget_id=None):
        budget = Budget(
            data['user_id'],
            data['category'],
            data['amount'],
            data['month'],
            data['year'],
            budget_id
        )
        if 'created_at' in data:
            budget.created_at = data['created_at']
        return budget