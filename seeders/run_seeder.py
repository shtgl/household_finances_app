import os
import sys
import subprocess

# Get absolute path to project root (one level above this script)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir))

# Add project root to sys.path to ensure imports work properly
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Ensure we're running from the project root
os.chdir(project_root)

options = {
    "1": "Users",
    "2": "Loans",
    "3": "Expenses",
    "4": "Insurance"
}

modules = {
    "1": "seeders.seeds.seed_users",
    "2": "seeders.seeds.seed_loan",
    "3": "seeders.seeds.seed_expense",
    "4": "seeders.seeds.seed_insurance"
}

# -----------------------------
# Helper Functions
# -----------------------------
def print_menu():
    print("\n===== Available Seeders =====")
    for key, value in options.items():
        print(f"{key:3} : {value:10}")
    print("=============================\n")


def confirm(prompt="Are you sure? (y/n)> "):
    return input(prompt).strip().lower() == "y"


# -----------------------------
# Main Seeder Runner
# -----------------------------
def run_seeder():
    running = True

    while running:
        print_menu()
        choice = input("Enter a valid item to seed> ").strip()

        if choice not in options:
            print("❌ Invalid choice. Please try again.\n")
            continue

        if confirm(f"Seed {options[choice]} data? (y/n)> "):
            module_to_run = modules[choice]
            print(f"\n🚀 Running seeder: {module_to_run}\n")

            # Run the seeder as a module
            subprocess.run([sys.executable, "-m", module_to_run], check=False)
        else:
            print("⚠️  Skipped.\n")
            continue

        # Ask if user wants to continue
        if not confirm("Add more items? (y/n)> "):
            running = False

    print("\n✅ Thanks for adding value to your dashboard!")


if __name__ == "__main__":
    run_seeder()
