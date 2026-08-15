import pandas as pd
import seaborn as sns
import random
import matplotlib.pyplot as plt
from . import data


def acc_account():
    """Create a new account with unique account number."""
    acc_data = data.load_account()
    existing_accounts = set()
    if acc_data is not None and "acc" in acc_data.columns:
        existing_accounts = set(acc_data["acc"].dropna().astype(str))

    # Generate unique account number
    while True:
        acnt = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", k=2)
        ) + str(random.randint(0, 9))
        if acnt not in existing_accounts:
            break

    # Get user information
    name = input("Enter your name: ").strip()
    email = input("Enter your email: ").strip()

    # Get and confirm password
    while True:
        password = input("Enter your password: ")
        confirm_password = input("Re-enter your password: ")
        if password == confirm_password:
            break
        print("Passwords do not match. Please try again.")

    account = {
        "acc": acnt,
        "name": name,
        "email": email,
        "password": password,
    }

    # Save the account
    data.save_account(account)
    return account


if __name__ == "__main__":
    print("Oops you come wrong file.")
