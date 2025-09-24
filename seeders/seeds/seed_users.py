"""
Generate unique User records in batches with Faker.
Ensures no duplicate emails are inserted.
"""

import random
from faker import Faker
from app import create_app
from routes import db, bcrypt, User

fake = Faker()

app = create_app()
with app.app_context():
    total_to_generate = 100000   # adjust as needed
    batch_size = 500
    inserted_count = 0

    # Precompute one hashed password for all fake users
    shared_password_hash = bcrypt.generate_password_hash("password123").decode("utf-8")

    while inserted_count < total_to_generate:
        batch = []
        for _ in range(batch_size):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()  # ensures uniqueness within Faker session

            # Check DB for existing email (important across multiple runs)
            if User.query.filter_by(email=email).first():
                continue  # skip duplicates

            is_verified = random.choice([True, False])

            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password_hash=shared_password_hash,
                is_verified=is_verified,
            )
            batch.append(user)

        if batch:
            db.session.bulk_save_objects(batch)
            db.session.commit()
            inserted_count += len(batch)
            print(f"✅ Inserted {inserted_count}/{total_to_generate} users so far...")

    print(f"🎉 Done: Inserted {inserted_count} unique users")
    print("ℹ️ All users have password: 'password123'")
