import random
from app import base_logger
from datetime import datetime

from .context import get_dashboard_context
from .schema import Expense, Loan, Insurance, Category, db

from sqlalchemy import extract, func
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint("dashboard", __name__)


def _add_item_to_db(item):
    base_logger.info(f"Adding {item} to database")
    try:
        db.session.add(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

@bp.route("/")
def home():
    base_logger.info(f"Welcome to home page")
    return render_template("home.html")


@bp.route("/dashboard")
@login_required
def dashboard():
    base_logger.info(f"On Dashboard page")
    context = get_dashboard_context(current_user.user_id, request.args)
    context["user"] = current_user  # add current_user to context here
    return render_template("dashboard.html", **context)



@bp.route("/expenses/add", methods=["POST"])
@login_required
def add_expense():
    amount = float(request.form.get("amount", 0) or 0)
    description = request.form.get("description")
    date_str = request.form.get("date")
    category_id = request.form.get("category_id")
    date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

    expense = Expense(
        amount=amount,
        description=description,
        date=date,
        user_id=current_user.user_id,
        category_id=int(category_id) if category_id else None,
    )
    _add_item_to_db(expense)
    return redirect(url_for("dashboard.dashboard"))


@bp.route("/loans/add", methods=["POST"])
@login_required
def add_loan():
    lender = request.form.get("lender")
    amount = float(request.form.get("amount", 0) or 0)
    interest_rate = request.form.get("interest_rate")
    due_date_str = request.form.get("due_date")
    loan_category = request.form.get("loan_category") or random.choice(LOAN_CATEGORIES)
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date() if due_date_str else None

    loan = Loan(
        lender=lender,
        amount=amount,
        interest_rate=float(interest_rate) if interest_rate else None,
        due_date=due_date,
        loan_category=loan_category,
        user_id=current_user.user_id,
    )
    _add_item_to_db(loan)
    return redirect(url_for("dashboard.dashboard"))


@bp.route("/insurances/add", methods=["POST"])
@login_required
def add_insurance():
    provider = request.form.get("provider")
    policy_type = request.form.get("policy_type")
    premium = float(request.form.get("premium", 0) or 0)
    renewal_date_str = request.form.get("renewal_date")
    renewal_date = datetime.strptime(renewal_date_str, "%Y-%m-%d").date() if renewal_date_str else None

    insurance = Insurance(
        provider=provider,
        policy_type=policy_type,
        premium=premium,
        renewal_date=renewal_date,
        user_id=current_user.user_id,
    )
    _add_item_to_db(insurance)
    return redirect(url_for("dashboard.dashboard"))



