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
        account_stats = data.update_account_stats(account["Account"])
        if account_stats:
            account.update(account_stats)
        print("Task added successfully!")
        return task

    print("Unable to save the task. Please try again.")
    return None


def view_task(account):
    """Display all tasks and activity belonging to the signed-in user."""
    if not account or not account.get("Account"):
        print("Please sign in before viewing your tasks.")
        return None

    task_df = data.load_list()
    if task_df is None or task_df.empty or "acc_no" not in task_df.columns:
        print("You do not have any tasks yet.")
        return None

    account_id = str(account["Account"]).strip()
    account_tasks = task_df[task_df["acc_no"].astype(str).str.strip() == account_id]
    if account_tasks.empty:
        print("You do not have any tasks yet.")
        return None

    print("\nYour tasks and activity:")
    for series, (_, task) in enumerate(account_tasks.iterrows(), start=1):
        print(f"\n{series}. {task.get('head', 'Untitled')}")
        print(f"   Details: {task.get('detail', '')}")
        print(f"   Status: {task.get('status', 'pending')}")
        print(f"   Created: {task.get('created_date_time', '')}")
        print(f"   Completed: {task.get('comp_date_time', '')}")

    return account_tasks.to_dict("records")


def complete_task(account):
    """Let the signed-in user select a task and mark it as completed."""
    if not account or not account.get("Account"):
        print("Please sign in before completing a task.")
        return None

    task_df = data.load_list()
    if task_df is None or task_df.empty or "acc_no" not in task_df.columns:
        print("You do not have any tasks yet.")
        return None

    account_id = str(account["Account"]).strip()
    account_tasks = task_df[task_df["acc_no"].astype(str).str.strip() == account_id]
    if account_tasks.empty:
        print("You do not have any tasks yet.")
        return None

    print("\nYour tasks:")
    for series, (_, task) in enumerate(account_tasks.iterrows(), start=1):
        print(
            f"{series}. {task.get('head', 'Untitled')} "
            f"[{task.get('status', 'pending')}]"
        )

    selected_series = input("Enter the task series to complete: ").strip()
    try:
        series_number = int(selected_series)
    except (TypeError, ValueError):
        print("Please enter a valid task series number.")
        return None

    if series_number < 1 or series_number > len(account_tasks):
        print("Please enter a task series number from the list.")
        return None

    completed = data.complete_task(account_id, series_number)
    if completed is None:
        print("Unable to complete that task. Please try again.")
        return None

    account_stats = completed.pop("account_stats", None)
    already_completed = completed.pop("already_completed", False)
    if account_stats:
        account.update(account_stats)
    if already_completed:
        print(f"Task {series_number} was already completed.")
        return completed
    print(f"Task {series_number} completed successfully!")
    return completed


def delete_account(account):
    """Delete the signed-in account after explicit confirmation."""
    if not account or not account.get("Account"):
        print("Please sign in before deleting your account.")
        return False

    confirmation = (
        input("Type 'delete' to permanently delete your account: ").strip().lower()
    )
    if confirmation != "delete":
        print("Account deletion cancelled.")
        return False

    if data.delete_account(account["Account"]):
        print("Account and its tasks deleted successfully.")
        return True

    print("Unable to delete the account. Please try again.")
    return False


ACTION_HANDLERS = {}


def register_action(action, handler):
    """Register the function that should run for a parsed prompt action."""
    ACTION_HANDLERS[action] = handler


register_action("create_account", lambda _account=None: acc_account())
register_action("account_status", show_account_status)
register_action("add_task", add_task)
register_action("view_task", view_task)
register_action("complete_task", complete_task)
register_action("delete_account", delete_account)


def dispatch_command(action, current_user=None):
    """Run a parsed prompt action and return its result.

    ``exit`` is intentionally handled by the application loop because it
    controls the lifetime of the program rather than a data operation.
    """
    handler = ACTION_HANDLERS.get(action)
    if handler is None:
        print("That command is not available yet.")
        return None
    return handler(current_user)


if __name__ == "__main__":
    print("Oops you come wrong file.")
