import random
from datetime import datetime

from . import data


def acc_account():
    print("\n" + "─" * 50)
    print("🔧 Starting Account Creation Process...")
    print("─" * 50 + "\n")
    acc_data = data.load_account()
    existing_accounts = set()
    if acc_data is not None and not acc_data.empty and "Account" in acc_data.columns:
        existing_accounts = set(acc_data["Account"].dropna().astype(str))

    while True:
        acnt = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", k=2)
        ) + str(random.randint(0, 9))
        if acnt not in existing_accounts:
            break

    name = input("👤 Enter your name: ").strip()
    email = input("📧 Enter your email: ").strip()

    while True:
        password = input("🔒 Enter your password: ")
        confirm_password = input("🔒 Re-enter your password: ")
        if password == confirm_password:
            break
        print("\n❌ Passwords do not match. Please try again.\n")

    account = {
        "Account": acnt,
        "Name": name,
        "Password": password,
        "email": email,
        "strike": 0,
        "total_todos": 0,
        "max_strike": 0,
    }

    # Save account and display it if successful
    if data.save_account(account):
        print(f"\n✅ Account saved successfully! Account #{acnt}\n")
        data.display_account(account)
        return account
    else:
        print("\n❌ Failed to save account. Please try again.\n")
        return None


def check_account(account=None, password=None):
    account_df = data.load_account()
    if account_df is None or account_df.empty:
        print("No account found in the system.")
        return None

    if account is None:
        account = input("Enter your account number: ").strip()
    if password is None:
        password = input("Enter your password: ").strip()

    account_value = str(account).strip()
    password_value = str(password).strip()

    match = account_df[account_df["Account"].astype(str).str.strip() == account_value]
    if match.empty:
        print("Account not found.")
        return None

    stored_password = str(match.iloc[0].get("Password", "")).strip()
    if stored_password != password_value:
        print("Incorrect password.")
        return None

    return match.iloc[0].to_dict()


def show_account_status(account):
    """Display the account currently signed in to the application."""
    if not account:
        print("Please sign in before viewing account status.")
        return None

    data.display_account(account)
    return account


def add_task(account):
    """Collect and save one task for the signed-in account."""
    if not account or not account.get("Account"):
        print("Please sign in before adding a task.")
        return None

    head = input("Task title: ").strip()
    if not head:
        print("A task title is required.")
        return None

    detail = input("Task details (optional): ").strip()
    task = {
        "acc_no": str(account["Account"]).strip(),
        "head": head,
        "detail": detail,
        "status": "pending",
        "created_date_time": datetime.now().isoformat(timespec="seconds"),
        "comp_date_time": "",
    }

    if data.save_list(task):
        print("Task added successfully!")
        return task

    print("Unable to save the task. Please try again.")
    return None


def dispatch_command(action, current_user=None):
    """Run a parsed prompt action and return its result.

    ``exit`` is intentionally handled by the application loop because it
    controls the lifetime of the program rather than a data operation.
    """
    handlers = {
        "create_account": lambda: acc_account(),
        "account_status": lambda: show_account_status(current_user),
        "add_task": lambda: add_task(current_user),
    }

    handler = handlers.get(action)
    if handler is None:
        print("That command is not available yet.")
        return None
    return handler()


if __name__ == "__main__":
    print("Oops you come wrong file.")
