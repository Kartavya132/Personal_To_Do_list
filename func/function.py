import random

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


if __name__ == "__main__":
    print("Oops you come wrong file.")
