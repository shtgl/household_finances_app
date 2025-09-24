import random
from datetime import datetime, timedelta
from faker import Faker
from app import create_app
from routes import db, Loan, User

fake = Faker()

BATCH_SIZE = 500
TOTAL_RECORDS = 5


app = create_app()

# Loan lenders
lenders = [
    "HDFC Bank", "ICICI Bank", "SBI", "Axis Bank", "Kotak Mahindra",
    "Bajaj Finance", "Paytm Loans", "IndusInd Bank", "Yes Bank", "HSBC",
    "Standard Chartered", "Personal Lender"
]

# Loan categories in India
loan_categories = [
    "Home Loan",
    "Personal Loan",
    "Education Loan",
    "Car Loan",
    "Gold Loan",
    "Business Loan",
    "Agriculture Loan"
]

def generate_random_loan(user_ids):
    """Generate a random Loan record with loan_category."""
    lender = random.choice(lenders)
    amount = round(random.uniform(1000, 100000), 2)
    interest_rate = round(random.uniform(2.5, 15.0), 2)
    due_date = datetime.utcnow().date() + timedelta(days=random.randint(30, 5 * 365))
    user_id = random.choice(user_ids)
    loan_category = random.choice(loan_categories)

    return Loan(
        lender=lender,
        amount=amount,
        interest_rate=interest_rate,
        due_date=due_date,
        loan_category=loan_category,
        user_id=user_id,
    )

def seed_loans():
    with app.app_context():
        print("Fetching existing users...")
        user_ids = [u.user_id for u in User.query.all()]

        if not user_ids:
            print("No users found. Seed users first.")
            return

        created_count = 0
        while created_count < TOTAL_RECORDS:
            batch = []
            for _ in range(min(BATCH_SIZE, TOTAL_RECORDS - created_count)):
                loan = generate_random_loan(user_ids)
                batch.append(loan)

            db.session.bulk_save_objects(batch)
            db.session.commit()

            created_count += len(batch)
            print(f"Inserted {created_count}/{TOTAL_RECORDS} loans...")

        print(f"Done! Inserted {TOTAL_RECORDS} Loan records.")

if __name__ == "__main__":
    seed_loans()
