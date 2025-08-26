# Overview

As a software engineer, I always seek ways to improve my skills in real applications and cloud systems. For this project, I built a Personal Finance Manager. It is a command line tool to help users track money coming in, money going out, and plans for spending. It uses a cloud database for safe, lasting storage.

The software lets users sign up, log in, add and handle transactions, set spending plans, and see summaries of their finances. User data is kept in Google Firestore, a flexible NoSQL cloud database. The program is made to be easy to use from the command line, with clear menus for each action.

My aim in making this software was to get experience with cloud database setup, user access, and building clean, easy to change Python applications. This project also helped me use good practices in code setup, managing settings, and keeping credentials safe.

[Software Demo Video](https://youtu.be/GTNCx3eHH3Y)

# Cloud Database

This project uses Google Firestore as its cloud database. Firestore is a flexible, scalable NoSQL database from Google Firebase. It allows for quick data storage and access.

The database has these collections:

- users: Stores user profiles with fields for email, name, and signup date.
- transactions: Stores each money transaction, with user ID, amount, category, description, type (income or expense), and date.
- budgets: Stores spending plans for users, with category, amount, month, and year.

All data is stored safely in the cloud. The application works with Firestore using the official Python tools.

# Development Environment

- Code Editor: Visual Studio Code
- Version Control: Git
- Operating System: macOS (Apple Silicon or M1)
- Programming Language: Python 3.9

**Key Libraries:**

- firebase admin (for Firestore access)
- python dotenv (for managing settings)
- tabulate (for showing tables in the command line)
- colorama (for colored command line output)

# Useful Websites

{Make a list of websites that you found helpful in this project}

- [Google Firestore Documentation](https://firebase.google.com/docs/firestore)
- [firebase admin Python SDK](https://firebase.google.com/docs/admin/setup)
- [Python Official Documentation](https://docs.python.org/3/)
- [Tabulate Library](https://pypi.org/project/tabulate/)
- [VS Code Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

# Future Work

- Add simple, easy to use transaction and budget IDs.
- Add user login with passwords for better security.
- Make a graphical user interface (GUI) for easier use.
- Add ways to export and import data (like CSV or Excel).
- Improve error handling and checking of user input.
- Add support for different currencies and languages.