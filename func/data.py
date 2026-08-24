import os
from datetime import datetime

import pandas as pd

# Store paths are based on this project, not on the directory from which the
# program was started.  This keeps the application from silently reading or
# creating a different pair of CSV files when it is launched elsewhere.
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
DATA_ACC = os.path.join(PROJECT_DIR, "data", "account.csv")
DATA_LIST = os.path.join(PROJECT_DIR, "data", "list.csv")

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
    "todo_daily",
    "task_date",
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
        "todo_totals": "total_todos",
        "max_strike": "max_strike",
        "sr_no": "sr_no",
        "head": "head",
        "detail": "detail",
        "status": "status",
        "created_date_time": "created_date_time",
        "comp_date_time": "comp_date_time",
        "todo_daily": "todo_daily",
        "daily": "todo_daily",
        "task_date": "task_date",
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
            aliases={
                "Account": "acc_no",
                "acc_no": "acc_no",
                "acc": "acc_no",
                "account": "acc_no",
            },
        )

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=LIST_COLUMNS)
    except Exception:
        return None


def update_account_stats(account):
    """Recalculate and save task counters for one account."""
    account_id = str(account).strip()
    account_df = load_account()
    task_df = load_list()
    if account_df is None or "Account" not in account_df.columns:
        return None
    if task_df is None:
        task_df = pd.DataFrame(columns=LIST_COLUMNS)

    account_matches = account_df["Account"].astype(str).str.strip() == account_id
    if not account_matches.any():
        return None

    if "acc_no" in task_df.columns:
        account_tasks = task_df[task_df["acc_no"].astype(str).str.strip() == account_id]
    else:
        account_tasks = task_df.iloc[0:0]

    total_todos = len(account_tasks)
    completed_todos = int(
        account_tasks.get("status", pd.Series(dtype=str))
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("completed")
        .sum()
    )
    daily_tasks = account_tasks[
        account_tasks.get("todo_daily", pd.Series(False, index=account_tasks.index))
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "1", "yes", "y"])
    ]
    daily_dates = pd.to_datetime(
        daily_tasks.get("task_date", pd.Series(dtype=str)), errors="coerce"
    )
    fallback_dates = pd.to_datetime(
        daily_tasks.get("created_date_time", pd.Series(dtype=str)), errors="coerce"
    )
    daily_dates = daily_dates.fillna(fallback_dates).dt.date.dropna()

    if daily_tasks.empty:
        # Preserve the completed-count behavior for legacy accounts.
        current_strike = completed_todos
        calculated_max = completed_todos
    else:
        completed_dates = set(daily_dates)
        current_day = datetime.now().date()
        current_strike = 0
        while current_day in completed_dates:
            current_strike += 1
            current_day = current_day.fromordinal(current_day.toordinal() - 1)

        calculated_max = 0
        for completed_day in sorted(completed_dates):
            streak = 1
            previous_day = completed_day.fromordinal(completed_day.toordinal() - 1)
            while previous_day in completed_dates:
                streak += 1
                previous_day = previous_day.fromordinal(previous_day.toordinal() - 1)
            calculated_max = max(calculated_max, streak)

    account_index = account_df.index[account_matches][0]
    previous_max = pd.to_numeric(
        (
            account_df.loc[account_index, "max_strike"]
            if "max_strike" in account_df.columns
            else 0
        ),
        errors="coerce",
    )
    max_strike = max(calculated_max, int(previous_max) if pd.notna(previous_max) else 0)
    account_df.loc[account_index, "total_todos"] = total_todos
    account_df.loc[account_index, "strike"] = current_strike
    account_df.loc[account_index, "max_strike"] = max_strike
    account_df.reindex(columns=ACCOUNT_COLUMNS).to_csv(DATA_ACC, index=False)

    return {
        "total_todos": total_todos,
        "strike": current_strike,
        "max_strike": max_strike,
    }


def complete_task(account, series):
    """Mark one account task as completed using its displayed series number."""
    try:
        task_df = load_list()
        if task_df is None or task_df.empty or "acc_no" not in task_df.columns:
            return None

        account_id = str(account).strip()
        series_number = int(series)
        if not account_id or series_number < 1:
            return None

        account_tasks = task_df[task_df["acc_no"].astype(str).str.strip() == account_id]
        if series_number > len(account_tasks):
            return None

        task_index = account_tasks.index[series_number - 1]
        was_completed = (
            str(task_df.loc[task_index, "status"]).strip().lower() == "completed"
        )
        # Completing an already completed task must not overwrite its original
        # completion time.  We still refresh account statistics so legacy CSV
        # data is repaired if necessary.
        if not was_completed:
            task_df.loc[task_index, "status"] = "completed"
            task_df.loc[task_index, "comp_date_time"] = datetime.now().isoformat(
                timespec="seconds"
            )
            # The existing CSV format uses ``Account``.  Keep that format on
            # disk, while ``load_list`` exposes it as ``acc_no`` internally.
            saved = task_df.drop(columns="sr_no", errors="ignore").rename(
                columns={"acc_no": "Account"}
            )
            saved.to_csv(DATA_LIST, index=False)
        account_stats = update_account_stats(account_id)
        completed_task = task_df.loc[task_index].to_dict()
        completed_task["account_stats"] = account_stats
        completed_task["already_completed"] = was_completed
        return completed_task
    except (OSError, TypeError, ValueError, KeyError):
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
                "todo_daily",
                "task_date",
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
                        "todo_daily",
                        "task_date",
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
