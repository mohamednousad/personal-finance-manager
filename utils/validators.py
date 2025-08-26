def validate_email(email):
    return '@' in email and '.' in email

def validate_amount(amount_str):
    try:
        amount = float(amount_str)
        if amount <= 0:
            return False, "Amount must be greater than 0"
        return True, amount
    except ValueError:
        return False, "Please enter a valid number"

def validate_category(category, valid_categories):
    return category.lower() in [c.lower() for c in valid_categories]

def validate_transaction_type(transaction_type):
    return transaction_type.lower() in ['income', 'expense']

def validate_month(month_str):
    try:
        month = int(month_str)
        if 1 <= month <= 12:
            return True, month
        return False, "Month must be between 1 and 12"
    except ValueError:
        return False, "Please enter a valid month number"

def validate_year(year_str):
    try:
        year = int(year_str)
        if 2020 <= year <= 2030:
            return True, year
        return False, "Year must be between 2020 and 2030"
    except ValueError:
        return False, "Please enter a valid year"