import os

import pandas as pd

DATA_ACC = "data/account.csv"
DATA_LIST = "data/list.csv"

ACCOUNT_COLUMNS = [
    "Account",
    "Name",
    "Password",
    "email",
    "strike",
    "total_todos",
    "max_strike",
]
LIST_COLUMNS = [
    "sr_no",
    "acc_no",
    "head",
    "detail",
    "status",
    "created_date_time",
    "comp_date_time",
]


def _normalise_columns(df, expected_columns, aliases=None):
    if df is None:
        return pd.DataFrame(columns=expected_columns)

    alias_map = {
        "acc": "Account",
        "acc_no": "Account",
        "account": "Account",
        "Account": "Account",
        "name": "Name",
        "Name": "Name",
        "password": "Password",
        "Password": "Password",
        "pass": "Password",
        "email": "email",
        "strike": "strike",
        "total_todos": "total_todos",
        "max_strike": "max_strike",
        "sr_no": "sr_no",
        "head": "head",
        "detail": "detail",
        "status": "status",
        "created_date_time": "created_date_time",
        "comp_date_time": "comp_date_time",
    }
    if aliases:
        alias_map.update(aliases)

    df = df.rename(
        columns={
            str(col): alias_map.get(str(col).strip(), str(col)) for col in df.columns
        }
    )

    for column in expected_columns:
        if column not in df.columns:
            df[column] = None

    return df


def load_account():
    try:
        if not os.path.exists(DATA_ACC):
            raise FileNotFoundError("account.csv not found in data/ directory")

        df = pd.read_csv(DATA_ACC)
        if df.empty:
            return pd.DataFrame(columns=ACCOUNT_COLUMNS)
        return _normalise_columns(df, ACCOUNT_COLUMNS)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=ACCOUNT_COLUMNS)
    except Exception:
        return None


def load_list():
    try:
        if not os.path.exists(DATA_LIST):
            raise FileNotFoundError("list.csv not found in data/ directory")

        df = pd.read_csv(DATA_LIST)
        if df.empty:
            return pd.DataFrame(columns=LIST_COLUMNS)
        return _normalise_columns(df, LIST_COLUMNS)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=LIST_COLUMNS)
    except Exception:
        return None


def save_account(account_data):
    try:
        if isinstance(account_data, dict):
            new_df = pd.DataFrame([account_data])
        else:
            new_df = account_data.copy()

        new_df = _normalise_columns(new_df, ACCOUNT_COLUMNS)

        directory = os.path.dirname(DATA_ACC)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        file_exists = os.path.exists(DATA_ACC) and os.path.getsize(DATA_ACC) > 0

        if file_exists:
            # Read existing data and append new data
            existing_df = pd.read_csv(DATA_ACC)
            existing_df = _normalise_columns(existing_df, ACCOUNT_COLUMNS)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            combined_df.to_csv(DATA_ACC, index=False)
        else:
            # Create new file with header and data
            new_df.to_csv(DATA_ACC, index=False)

        return True
    except Exception as e:
        print(f"Error saving account: {e}")
        return False


def save_list(list_data):
    try:
        if isinstance(list_data, dict):
            new_df = pd.DataFrame([list_data])
        else:
            new_df = list_data.copy()

        new_df = _normalise_columns(new_df, LIST_COLUMNS)

        directory = os.path.dirname(DATA_LIST)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        file_exists = os.path.exists(DATA_LIST) and os.path.getsize(DATA_LIST) > 0

        if file_exists:
            # Read existing data and append new data
            existing_df = pd.read_csv(DATA_LIST)
            existing_df = _normalise_columns(existing_df, LIST_COLUMNS)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            combined_df.to_csv(DATA_LIST, index=False)
        else:
            # Create new file with header and data
            new_df.to_csv(DATA_LIST, index=False)

        return True
    except Exception as e:
        print(f"Error saving list item: {e}")
        return False


def display_account(account_data):
    if account_data is None or (isinstance(account_data, dict) and not account_data):
        print("\n⚠️  No account data to display.\n")
        return

    print("\n" + "╔" + "═" * 48 + "╗")
    print("║" + "👤 ACCOUNT INFORMATION 👤".center(48) + "║")
    print("╠" + "═" * 48 + "╣")
    print(f"║ 🆔 Account Number: {str(account_data.get('Account', 'N/A')):<34} ║")
    print(f"║ 👤 Name:          {str(account_data.get('Name', 'N/A')):<34} ║")
    print(f"║ 📧 Email:         {str(account_data.get('email', 'N/A')):<34} ║")
    print("╠" + "═" * 48 + "╣")
    print(f"║ 📝 Total TODOs:    {str(account_data.get('total_todos', 0)):<34} ║")
    print(f"║ ⚡ Strikes:        {str(account_data.get('strike', 0)):<34} ║")
    print(f"║ 🔥 Max Strikes:    {str(account_data.get('max_strike', 0)):<34} ║")
    print("╚" + "═" * 48 + "╝" + "\n")


if __name__ == "__main__":
    print("Oops you come wrong file.")
