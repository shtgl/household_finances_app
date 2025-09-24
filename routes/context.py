from datetime import datetime
from collections import defaultdict
from sqlalchemy import extract, func
from .schema import Expense, Loan, Insurance, Category
from .filters import get_filtered_expenses, get_filtered_loans, get_filtered_insurances

providers = [
    "LIC", "HDFC Ergo", "ICICI Lombard", "SBI Life", "Max Bupa",
    "Bajaj Allianz", "Reliance General", "Star Health", "Tata AIG",
    "Future Generali", "Oriental Insurance"
]

LENDERS = [
    "HDFC Bank", "ICICI Bank", "SBI", "Axis Bank", "Kotak Mahindra",
    "Bajaj Finance", "Paytm Loans", "IndusInd Bank", "Yes Bank", "HSBC",
    "Standard Chartered", "Personal Lender"
]

LOAN_CATEGORIES = [
    "Home Loan",
    "Personal Loan",
    "Education Loan",
    "Car Loan",
    "Gold Loan",
    "Business Loan",
    "Agriculture Loan",
]

POLICY_TYPES = [
    "Health",
    "Life",
    "Vehicle",
    "Home",
    "Travel",
    "Accident",
    "Business"
]
DEFAULT_CATEGORIES = [
    "Groceries",
    "Electricity",
    "Gas",
    "Medicines",
    "Vehicle Maintenance",
    "Clothes",
    "Trips/Vacations",
    "Housekeeping",
    "Loan",
    "Insurance",
    "House Maintenance"
]

def get_dashboard_context(user_id, args):
    # Parse filter parameters
    selected_expense_categories = args.getlist("expense_category") or []
    selected_insurance_providers = args.getlist("insurance_provider") or []
    selected_insurance_types = args.getlist("insurance_type") or []
    selected_loan_lenders = args.getlist("loan_lender") or []
    selected_loan_categories = args.getlist("loan_category") or []

    start_date_str = args.get("start_date")
    end_date_str = args.get("end_date")
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None

    # Get data using helpers
    expenses, total_expenses, expense_chart_data, category_chart_data = get_filtered_expenses(
        user_id, selected_expense_categories, start_date, end_date
    )

    loans, total_loans, loan_chart_data = get_filtered_loans(
        user_id, selected_loan_lenders, selected_loan_categories, start_date, end_date
    )

    insurances, total_premium, insurance_chart_data = get_filtered_insurances(
        user_id, selected_insurance_providers, selected_insurance_types, start_date, end_date
    )

    # Query categories for dropdown
    categories = Category.query.order_by(Category.name.asc()).all()

    # Build context dict
    context = {
        "total_expenses": total_expenses,
        "total_loans": total_loans,
        "total_premium": total_premium,
        "expenses": expenses,
        "loans": loans,
        "insurances": insurances,
        "categories": categories,
        "lenders": LENDERS,
        "providers": providers,
        "POLICY_TYPES": POLICY_TYPES,
        "loan_categories": LOAN_CATEGORIES,
        "DEFAULT_CATEGORIES": DEFAULT_CATEGORIES,
        "selected_expense_categories": selected_expense_categories,
        "selected_loan_lenders": selected_loan_lenders,
        "selected_loan_categories": selected_loan_categories,
        "selected_insurance_providers": selected_insurance_providers,
        "selected_insurance_types": selected_insurance_types,
        "start_date": start_date_str,
        "end_date": end_date_str,
        "expense_chart_data": expense_chart_data,
        "loan_chart_data": loan_chart_data,
        "insurance_chart_data": insurance_chart_data,
        "category_chart_data": category_chart_data,
    }

    return context