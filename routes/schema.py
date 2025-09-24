from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager
from flask_mail import Mail

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()


class User(db.Model, UserMixin):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    is_verified = db.Column(db.Boolean, nullable=False, server_default="false")
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    expenses = db.relationship("Expense", backref="user", lazy=True)
    loans = db.relationship("Loan", backref="user", lazy=True)
    insurances = db.relationship("Insurance", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.user_id)


class Category(db.Model):
    __tablename__ = "categories"
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class Expense(db.Model):
    __tablename__ = "expenses"
    expense_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"), nullable=False)

    category = db.relationship("Category", backref="expenses")


class Loan(db.Model):
    __tablename__ = "loans"
    loan_id = db.Column(db.Integer, primary_key=True)
    lender = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float)
    due_date = db.Column(db.Date)
    loan_category = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)


class Insurance(db.Model):
    __tablename__ = "insurances"
    insurance_id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(100), nullable=False)
    policy_type = db.Column(db.String(50), nullable=False)
    premium = db.Column(db.Float, nullable=False)
    renewal_date = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)


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

def create_schema(app):
    """Create database structure and seed default categories if not already present."""
    with app.app_context():
        db.create_all()
        for name in DEFAULT_CATEGORIES:
            if not Category.query.filter_by(name=name).first():
                print(f"Seeding default category: {name}")
                db.session.add(Category(name=name))
        db.session.commit()
