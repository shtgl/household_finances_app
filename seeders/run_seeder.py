import os
import subprocess

# Absolute or relative path to your finance_management folder
project_path = os.path.abspath(".")  # or use full path if needed
running = True
choice = ("1", "2", "3", "4")
options = {1: 'Users', 2: 'Loans', 3: 'Expenses', 4: 'Insurance'}

# Change directory to finance_management
os.chdir(project_path)

print("===== Options =====")
for key, value in options.items():
    print(f"{key:3} : {value:10}")
print("===================")

while running:  
    user_choice = None

    while user_choice not in choice:
        user_choice = input("Enter a valid item to seed> ")
    
    if user_choice == "1":
        if input("Are you sure? (y/n)> ").lower() == "y":
            module_to_run = "seeders.seeds.seed_users"
            subprocess.run(["python", "-m", module_to_run])
        else:
            continue
    
    elif user_choice == "2":
        if input("Are you sure? (y/n)> ").lower() == "y":
            module_to_run = "seeders.seeds.seed_loan"
            subprocess.run(["python", "-m", module_to_run])
        else:
            continue
    
    elif user_choice == "3":
        if input("Are you sure? (y/n)> ").lower() == "y":
            module_to_run = "seeders.seeds.seed_expense"
            subprocess.run(["python", "-m", module_to_run])
        else:
            continue
    
    else:
        if input("Are you sure? (y/n)> ").lower() == "y":
            module_to_run = "seeders.seeds.seed_insurance"
            subprocess.run(["python", "-m", module_to_run])
        else:
            continue

    if not input("Add more items? (y/n)> ").lower() == "y":
        running = False

print("Thanks for adding value to your dashboard")