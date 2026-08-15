import pandas as pd
import os

DATA_ACC = "data/account.csv"
DATA_LIST = "data/list.csv"


def load_account():
    try:
        if not os.path.exists(DATA_ACC):
            raise FileNotFoundError("account.csv not found in data/ directory")

        df = pd.read_csv(DATA_ACC)
        if df.empty:
            return pd.DataFrame()
        return df

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None
    except pd.errors.EmptyDataError:
        print("Error: account.csv is empty or corrupted")
        return None
    except Exception as e:
        print(f"Unexpected error loading account.csv: {e}")
        return None


def load_list():
    try:
        if not os.path.exists(DATA_LIST):
            raise FileNotFoundError("list.csv not found in data/ directory")

        df = pd.read_csv(DATA_LIST)
        if df.empty:
            print("Warning: list.csv is empty")
        return df

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None
    except pd.errors.EmptyDataError:
        print("Error: list.csv is empty or corrupted")
        return None
    except Exception as e:
        print(f"Unexpected error loading list.csv: {e}")
        return None


def save_account(account_data):
    """Save account data to CSV file."""
    try:
        if isinstance(account_data, dict):
            df = pd.DataFrame([account_data])
        else:
            df = account_data

        df.to_csv(DATA_ACC, index=False, mode="a", header=not os.path.exists(DATA_ACC))
        print("Account saved successfully!")
        return True
    except Exception as e:
        print(f"Error saving account: {e}")
        return False


def save_list(list_data):
    """Save list data to CSV file."""
    try:
        if isinstance(list_data, dict):
            df = pd.DataFrame([list_data])
        else:
            df = list_data

        df.to_csv(
            DATA_LIST, index=False, mode="a", header=not os.path.exists(DATA_LIST)
        )
        print("List item saved successfully!")
        return True
    except Exception as e:
        print(f"Error saving list: {e}")
        return False


if __name__ == "__main__":
    print("Oops you come wrong file.")
