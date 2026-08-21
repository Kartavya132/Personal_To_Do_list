import os
from datetime import datetime

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

    result = pd.DataFrame(index=df.index)
    for expected in expected_columns:
        matching_columns = [
            column
            for column in df.columns
            if alias_map.get(str(column).strip(), str(column)) == expected
        ]

        if matching_columns:
            merged = df[matching_columns[0]].copy()
            for column in matching_columns[1:]:
                merged = merged.combine_first(df[column])
            result[expected] = merged
        else:
            result[expected] = pd.NA

    for extra_column in df.columns:
        final_name = alias_map.get(str(extra_column).strip(), str(extra_column))
        if final_name not in expected_columns and final_name not in result.columns:
            result[final_name] = df[extra_column]

    return result


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
        return _normalise_columns(
            df,
            LIST_COLUMNS,
            aliases={"Account": "acc_no", "acc": "acc_no", "account": "acc_no"},
        )

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=LIST_COLUMNS)
    except Exception:
        return None


def complete_task(account, series):
    """Mark one account task as completed using its displayed series number."""
    try:
        task_df = load_list()
        if task_df is None or task_df.empty or "acc_no" not in task_df.columns:
            return None

        account_id = str(account).strip()
        series_number = int(series)
        if series_number < 1:
            return None

        account_tasks = task_df[task_df["acc_no"].astype(str).str.strip() == account_id]
        if series_number > len(account_tasks):
            return None

        task_index = account_tasks.index[series_number - 1]
        task_df.loc[task_index, "status"] = "completed"
        task_df.loc[task_index, "comp_date_time"] = datetime.now().isoformat(
            timespec="seconds"
        )
        task_df.to_csv(DATA_LIST, index=False)
        return task_df.loc[task_index].to_dict()
    except (TypeError, ValueError, KeyError):
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
            existing_df = pd.read_csv(DATA_ACC)
            existing_df = _normalise_columns(existing_df, ACCOUNT_COLUMNS)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            combined_df = combined_df.reindex(columns=ACCOUNT_COLUMNS)
            combined_df.to_csv(DATA_ACC, index=False)
        else:
            new_df = new_df.reindex(columns=ACCOUNT_COLUMNS)
            new_df.to_csv(DATA_ACC, index=False)

        print("Account saved successfully!")
        return True
    except Exception as e:
        print(f"Error saving account: {e}")
        return False


def delete_account(account):
    """Delete an account and its tasks from the CSV data stores."""
    account_id = str(account).strip()
    if not account_id:
        return False

    account_df = load_account()
    if account_df is None or "Account" not in account_df.columns:
        return False

    matches = account_df["Account"].astype(str).str.strip() == account_id
    if not matches.any():
        return False

    remaining_accounts = account_df.loc[~matches].reindex(columns=ACCOUNT_COLUMNS)
    remaining_accounts.to_csv(DATA_ACC, index=False)

    task_df = load_list()
    if task_df is not None and "acc_no" in task_df.columns:
        task_matches = task_df["acc_no"].astype(str).str.strip() == account_id
        task_df.loc[~task_matches].to_csv(DATA_LIST, index=False)

    return True


def save_list(list_data):
    try:
        if isinstance(list_data, dict):
            new_df = pd.DataFrame([list_data])
        else:
            new_df = list_data.copy()

        def _normalise_list_frame(frame):
            frame = frame.copy()
            frame.columns = [str(col).strip() for col in frame.columns]
            rename_map = {
                "acc_no": "Account",
                "acc": "Account",
                "account": "Account",
            }
            frame = frame.rename(columns=rename_map)
            if "Account" not in frame.columns:
                frame["Account"] = pd.NA

            for field in [
                "head",
                "detail",
                "status",
                "created_date_time",
                "comp_date_time",
            ]:
                if field not in frame.columns:
                    frame[field] = pd.NA

            return frame[
                ["Account"]
                + [
                    field
                    for field in [
                        "head",
                        "detail",
                        "status",
                        "created_date_time",
                        "comp_date_time",
                    ]
                    if field in frame.columns
                ]
            ]

        new_df = _normalise_list_frame(new_df)

        directory = os.path.dirname(DATA_LIST)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        file_exists = os.path.exists(DATA_LIST) and os.path.getsize(DATA_LIST) > 0

        if file_exists:
            existing_df = pd.read_csv(DATA_LIST)
            if existing_df.empty:
                existing_df = pd.DataFrame(
                    columns=[
                        "Account",
                        "head",
                        "detail",
                        "status",
                        "created_date_time",
                        "comp_date_time",
                    ]
                )
            else:
                existing_df = _normalise_list_frame(existing_df)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            combined_df = _normalise_list_frame(combined_df)
            combined_df.to_csv(DATA_LIST, index=False)
        else:
            new_df.to_csv(DATA_LIST, index=False)

        return True
    except Exception as e:
        print(f"Error saving list item: {e}")
        return False


def display_account(account_data):
    if account_data is None or (isinstance(account_data, dict) and not account_data):
        print("\n⚠️  No account data to display.\n")
        return

    print("\n" + "╔" + "═" * 49 + "╗")
    print("║" + "👤 ACCOUNT INFORMATION 👤".center(47) + "║")
    print("╠" + "═" * 49 + "╣")
    account_fields = [
        ("🆔 Account Number", account_data.get("Account", "N/A")),
        ("👤 Name", account_data.get("Name", "N/A")),
        ("📧 Email", account_data.get("email", "N/A")),
        ("📝 Total TODOs", account_data.get("total_todos", 0)),
        ("⚡ Strikes", account_data.get("strike", 0)),
        ("🔥 Max Strikes", account_data.get("max_strike", 0)),
    ]

    for label, value in account_fields[:3]:
        print(f"║ {label:<18}: {str(value):<26} ║")

    print("╠" + "═" * 49 + "╣")
    for label, value in account_fields[3:]:
        print(f"║ {label:<18}: {str(value):<26} ║")

    print("╚" + "═" * 49 + "╝" + "\n")


if __name__ == "__main__":
    print("Oops you come wrong file.")
