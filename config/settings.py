import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID', 'personal-finance-manager')
    SERVICE_ACCOUNT_KEY_PATH = os.getenv('SERVICE_ACCOUNT_KEY_PATH', 'service-account-key.json')
    FIREBASE_WEB_API_KEY = os.getenv('FIREBASE_WEB_API_KEY')  # <-- Add this line
    APP_NAME = os.getenv('APP_NAME', 'Personal Finance Manager')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    USERS_COLLECTION = 'users'
    TRANSACTIONS_COLLECTION = 'transactions'
    BUDGETS_COLLECTION = 'budgets'
    TRANSACTION_TYPES = ['income', 'expense']
    INCOME_CATEGORIES = [
        'salary', 'freelance', 'investment', 'gift', 'bonus', 'other'
    ]
    EXPENSE_CATEGORIES = [
        'food', 'transportation', 'housing', 'utilities', 'entertainment',
        'healthcare', 'shopping', 'education', 'travel', 'other'
    ]
    @classmethod
    def validate_config(cls):
        if not os.path.exists(cls.SERVICE_ACCOUNT_KEY_PATH):
            raise FileNotFoundError(
                f"Service account key file not found: {cls.SERVICE_ACCOUNT_KEY_PATH}\n"
                "Please download your Firebase service account key and place it in the project root."
            )
        if not cls.FIREBASE_PROJECT_ID:
            raise ValueError("FIREBASE_PROJECT_ID must be set in environment variables")

settings = Settings()