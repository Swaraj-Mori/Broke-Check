<img width="330" height="200" alt="logo" src="https://github.com/Swaraj-Mori/Broke-Check/blob/main/website/static/logo.png" />

# Broke-Check

A full-stack personal expense and budget tracking web application built with Flask. Broke-Check lets users manage their expenses, track income and spending, create category-specific budgets, and visualize their spending over time.

## Features

### User Authentication

* User registration and login
* Password hashing for stored credentials
* "Remember me" login option
* Session-based authentication
* Protected application pages
* Logout functionality
* Validation for email, name, and password during registration

### Dashboard

* Personalized dashboard for each user
* Total spending compared with total budget
* Visual budget progress indicator
* 30-day expense history
* Interactive spending chart powered by Chart.js

### Expense Tracking

* Record debits and credits
* Add a description to each transaction
* Assign transactions to categories
* View transaction history with date and time
* Delete individual transactions
* Expenses are associated with the logged-in user

### Budget Management

* Set an overall budget through category budgets
* Create custom spending categories
* Assign an individual budget to each category
* Track spending against each category's budget
* Edit category names and budgets
* Delete categories
* Existing expenses are moved to `General` when a category is deleted
* Category budgets are displayed with visual progress bars

## Tech Stack

| Technology       | Purpose                                    |
| ---------------- | ------------------------------------------ |
| Python           | Backend programming                        |
| Flask            | Web framework                              |
| Flask-SQLAlchemy | Database ORM                               |
| SQLite           | Database                                   |
| Flask-Login      | User authentication and session management |
| Werkzeug         | Password hashing                           |
| Jinja2           | Server-side HTML templating                |
| HTML             | Page structure                             |
| Bootstrap        | UI and responsive styling                  |
| JavaScript       | Client-side functionality                  |
| Chart.js         | Expense visualization                      |

## How It Works

Broke-Check uses Flask blueprints to separate authentication functionality from the main application views.

The application initializes Flask, SQLAlchemy, and Flask-Login, then registers separate `views` and `auth` blueprints.

### Application Structure

```text
Broke-Check/
│
├── main.py
├── requirements.txt
├── testing.ipynb
│
└── website/
    ├── __init__.py
    ├── auth.py
    ├── views.py
    ├── models.py
    │
    ├── templates/
    │   ├── base.html
    │   ├── login.html
    │   ├── signup.html
    │   ├── dashboard.html
    │   ├── expense.html
    │   └── budget.html
    │
    └── static/
        ├── index.js
        └── ...
```

## Database

Broke-Check uses SQLite with SQLAlchemy.

There are two primary models:

### User

Stores:

* User ID
* Email
* First name
* Hashed password
* Categories
* Category budgets
* Relationship to expenses

### Expense

Stores:

* Expense ID
* User ID
* Date and time
* Debit
* Credit
* Description
* Category

Each expense is linked to the user who created it.

## Expense Calculation

Broke-Check treats spending as the difference between debits and credits:

```text
Total spending = Total debits - Total credits
```

The calculation is explicitly filtered using the currently authenticated user's ID, ensuring users only contribute their own transactions to their totals.

The dashboard's 30-day chart similarly filters transactions by the logged-in user and groups them by date.

## Budget Tracking

Budgets are organized around user-defined categories.

For each category, Broke-Check displays:

```text
Amount spent / Category budget
```

along with a progress bar. Categories below their budget are displayed with a success indicator, while categories that reach or exceed their budget use a danger indicator.

The dashboard also provides an overall view:

```text
Total spending / Total budget
```

with a corresponding progress bar.

## Pages

### `/login`

Allows existing users to authenticate using their email and password. Users can optionally enable the "Remember me" option.

### `/signup`

Allows new users to create an account with:

* Email
* First name
* Password
* Password confirmation

The application validates the submitted information before creating the account.

### `/`

The main dashboard displaying:

* Greeting
* Overall budget usage
* Spending progress
* 30-day expense chart

The chart is generated using Chart.js from date and spending data supplied by Flask.

### `/expense`

Provides an interface to add and manage transactions.

Users can enter:

* Debit
* Credit
* Description
* Category

The page also displays existing transactions with their date, amounts, description, and category.

### `/budget`

Provides category and budget management.

Users can:

* Add categories
* Assign budgets
* View category spending
* Edit categories
* Edit budgets
* Delete categories

Editing is handled through Bootstrap modal dialogs.

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/Swaraj-Mori/Broke-Check.git
cd Broke-Check
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

Run the project's main Python entry point:

```bash
python main.py
```

The application creates the SQLite database when it does not already exist.

Then open the local address shown by Flask in your browser.

## Frontend

The application uses Jinja templates with a shared `base.html` layout. Authenticated users receive a navigation bar linking to the Dashboard, Budget, Expense, and Logout pages.

Bootstrap is used for the interface components, including forms, navigation, progress bars, alerts, and modals.

Chart.js is used specifically for the dashboard's 30-day expense visualization.

## Authentication & Security

Passwords are not stored directly. During registration, passwords are passed through Werkzeug's password hashing functionality before being stored in the database. During login, the submitted password is checked against the stored hash.
Application pages that require an authenticated user are protected using Flask-Login's `login_required` decorator.

## Future Improvements

Possible areas for future development include:

* More detailed spending analytics
* Monthly and yearly reports
* Expense editing
* Recurring expenses
* Improved category and budget storage
* More advanced filtering and search
* Exporting financial data
* Improved mobile UI
* Additional visualization options
* More granular budget periods
* Deployment-oriented production configuration

## Project Status

Broke-Check is a functional full-stack expense tracking application built as a practical project using Flask, SQLAlchemy, authentication, server-side templating, and client-side data visualization.

## Author

**Swaraj Mori**

GitHub: [@Swaraj-Mori](https://github.com/Swaraj-Mori)

## License

No license is currently specified for this repository.
