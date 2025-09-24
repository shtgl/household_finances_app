"""
Seeder script for Expense records in batches.

Usage:
  python seed_expenses.py
"""

import random
from datetime import datetime, timedelta
from faker import Faker
from app import create_app
from routes import db, Expense, User, Category

fake = Faker()

BATCH_SIZE = 5
TOTAL_RECORDS = 5

app = create_app()

def generate_random_expense(user_ids, category_ids, existing_set):
    """Generate a unique random Expense."""
    while True:
        amount = round(random.uniform(10, 5000), 2)
        description = fake.sentence(nb_words=6)
        date = datetime.utcnow() - timedelta(days=random.randint(0, 5 * 365))
        user_id = random.choice(user_ids)
        category_id = random.choice(category_ids)

        # Key for uniqueness check
        key = (amount, description, date.date(), category_id)

        if key not in existing_set:
            existing_set.add(key)
            return Expense(
                amount=amount,
                description=description,
                date=date,
                user_id=user_id,
                category_id=category_id,
            )

def seed_expenses():
    with app.app_context():
        print("Fetching existing users and categories...")
        user_ids = [u.user_id for u in User.query.all()]
        category_ids = [c.category_id for c in Category.query.all()]

        if not user_ids or not category_ids:
            print("No users or categories found. Seed them first.")
            return

        print("Loading existing expenses to avoid duplicates...")
        existing_set = set(
            (e.amount, e.description, e.date.date(), e.category_id)
            for e in Expense.query.all()
        )

        created_count = 0
        while created_count < TOTAL_RECORDS:
            batch = []
            for _ in range(BATCH_SIZE):
                expense = generate_random_expense(user_ids, category_ids, existing_set)
                batch.append(expense)

            db.session.bulk_save_objects(batch)
            db.session.commit()

            created_count += len(batch)
            print(f"Inserted {created_count}/{TOTAL_RECORDS} expenses...")

        print(f"Done! Inserted {TOTAL_RECORDS} Expense records.")

if __name__ == "__main__":
    seed_expenses()
