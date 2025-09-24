"""
Seeder script for Insurance records in batches.

Usage:
  python seed_insurances.py
"""

import random

from datetime import datetime, timedelta
from faker import Faker
from app import create_app
from routes import db, Insurance, User

fake = Faker()

BATCH_SIZE = 500
TOTAL_RECORDS = 5

# Example policy types
POLICY_TYPES = [
    "Health",
    "Life",
    "Vehicle",
    "Home",
    "Travel",
    "Accident",
    "Business"
]

app = create_app()
providers = [
    "LIC", "HDFC Ergo", "ICICI Lombard", "SBI Life", "Max Bupa",
    "Bajaj Allianz", "Reliance General", "Star Health", "Tata AIG",
    "Future Generali", "Oriental Insurance"
]
def generate_random_insurance(user_ids):
    """Generate a random Insurance record."""
    provider = random.choice(providers)
    policy_type = random.choice(POLICY_TYPES)
    premium = round(random.uniform(2000, 50000), 2)
    renewal_date = datetime.utcnow().date() + timedelta(days=random.randint(30, 3 * 365))
    user_id = random.choice(user_ids)

    return Insurance(
        provider=provider,
        policy_type=policy_type,
        premium=premium,
        renewal_date=renewal_date,
        user_id=user_id,
    )

def seed_insurances():
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
                insurance = generate_random_insurance(user_ids)
                batch.append(insurance)

            db.session.bulk_save_objects(batch)
            db.session.commit()

            created_count += len(batch)
            print(f"Inserted {created_count}/{TOTAL_RECORDS} insurances...")

        print(f"Done! Inserted {TOTAL_RECORDS} Insurance records.")

if __name__ == "__main__":
    seed_insurances()
