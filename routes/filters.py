from datetime import datetime
from collections import defaultdict
from sqlalchemy import extract, func
from .schema import Expense, Loan, Insurance, Category, db


def get_filtered_expenses(user_id, selected_categories, start_date, end_date):
    """
    Filter out expenses based on categories, start and end date
    """
    expense_query = Expense.query.filter_by(user_id=user_id)

    if selected_categories:
        expense_query = expense_query.filter(Expense.category.has(Category.name.in_(selected_categories)))
    if start_date:
        expense_query = expense_query.filter(Expense.date >= start_date)
    if end_date:
        expense_query = expense_query.filter(Expense.date <= end_date)

    expenses = expense_query.all()
    total_expenses = sum(e.amount for e in expenses) if expenses else 0

    # Monthly Chart
    monthly_expenses_query = (
        db.session.query(
            extract("year", Expense.date).label("year"),
            extract("month", Expense.date).label("month"),
            func.sum(Expense.amount).label("total")
        )
        .filter(Expense.user_id == user_id)
    )
    if selected_categories:
        monthly_expenses_query = monthly_expenses_query.join(Category).filter(Category.name.in_(selected_categories))
    if start_date:
        monthly_expenses_query = monthly_expenses_query.filter(Expense.date >= start_date)
    if end_date:
        monthly_expenses_query = monthly_expenses_query.filter(Expense.date <= end_date)

    monthly_expenses = monthly_expenses_query.group_by("year", "month").order_by("year", "month").all()
    expense_chart_data = [
        {"label": f"{int(row.year)}-{int(row.month):02d}", "value": float(row.total)}
        for row in monthly_expenses
    ] if monthly_expenses else []

    # Category Chart
    category_query = (
        db.session.query(
            Category.name,
            func.sum(Expense.amount).label("total"),
        )
        .join(Category, Expense.category_id == Category.category_id)
        .filter(Expense.user_id == user_id)
    )
    if selected_categories:
        category_query = category_query.filter(Category.name.in_(selected_categories))
    if start_date:
        category_query = category_query.filter(Expense.date >= start_date)
    if end_date:
        category_query = category_query.filter(Expense.date <= end_date)

    category_results = category_query.group_by(Category.name).order_by(Category.name).all()
    category_chart_data = [
        {"label": row.name, "value": float(row.total)}
        for row in category_results
    ] if category_results else []

    return expenses, total_expenses, expense_chart_data, category_chart_data


def get_filtered_loans(user_id, selected_lenders, selected_categories, start_date, end_date):
    """
    Filter out loans based on lenders, categories, start and end date
    """
    loan_query = Loan.query.filter_by(user_id=user_id)

    if selected_lenders:
        loan_query = loan_query.filter(Loan.lender.in_(selected_lenders))
    if selected_categories:
        loan_query = loan_query.filter(Loan.loan_category.in_(selected_categories))
    if start_date:
        loan_query = loan_query.filter(Loan.due_date >= start_date)
    if end_date:
        loan_query = loan_query.filter(Loan.due_date <= end_date)

    loans = loan_query.all()

    # Loan Chart
    loan_chart_query = (
        db.session.query(
            extract("year", Loan.due_date).label("year"),
            func.sum(Loan.amount).label("total")
        )
        .filter(Loan.user_id == user_id, Loan.due_date.isnot(None))
    )
    if selected_lenders:
        loan_chart_query = loan_chart_query.filter(Loan.lender.in_(selected_lenders))
    if selected_categories:
        loan_chart_query = loan_chart_query.filter(Loan.loan_category.in_(selected_categories))
    if start_date:
        loan_chart_query = loan_chart_query.filter(Loan.due_date >= start_date)
    if end_date:
        loan_chart_query = loan_chart_query.filter(Loan.due_date <= end_date)

    loan_chart_results = loan_chart_query.group_by("year").order_by("year").all()
    loan_chart_data = [
        {"label": str(int(r.year)), "value": float(r.total)}
        for r in loan_chart_results
    ]
    total_loans = sum(float(r.total) for r in loan_chart_results)

    return loans, total_loans, loan_chart_data


def get_filtered_insurances(user_id, selected_providers, selected_types, start_date, end_date):
    """
    Filter out insurances based on providers and types
    """
    insurance_query = Insurance.query.filter_by(user_id=user_id)

    if selected_providers:
        insurance_query = insurance_query.filter(Insurance.provider.in_(selected_providers))
    if selected_types:
        insurance_query = insurance_query.filter(Insurance.policy_type.in_(selected_types))
    if start_date:
        insurance_query = insurance_query.filter(Insurance.renewal_date >= start_date)
    if end_date:
        insurance_query = insurance_query.filter(Insurance.renewal_date <= end_date)

    insurances = insurance_query.all()
    total_premium = sum(i.premium for i in insurances) if insurances else 0

    # Chart
    insurance_chart_query = (
        db.session.query(
            extract("year", Insurance.renewal_date).label("year"),
            extract("month", Insurance.renewal_date).label("month"),
            func.sum(Insurance.premium).label("total")
        )
        .filter(Insurance.user_id == user_id, Insurance.renewal_date.isnot(None))
    )
    if selected_providers:
        insurance_chart_query = insurance_chart_query.filter(Insurance.provider.in_(selected_providers))
    if selected_types:
        insurance_chart_query = insurance_chart_query.filter(Insurance.policy_type.in_(selected_types))
    if start_date:
        insurance_chart_query = insurance_chart_query.filter(Insurance.renewal_date >= start_date)
    if end_date:
        insurance_chart_query = insurance_chart_query.filter(Insurance.renewal_date <= end_date)

    insurance_chart_results = insurance_chart_query.group_by("year", "month").order_by("year", "month").all()
    monthly_insurance = defaultdict(float)
    for row in insurance_chart_results:
        label = f"{int(row.year)}-{int(row.month):02d}"
        monthly_insurance[label] = float(row.total)

    insurance_chart_data = [
        {"label": label, "value": monthly_insurance[label]}
        for label in sorted(monthly_insurance)
    ] if monthly_insurance else []

    return insurances, total_premium, insurance_chart_data