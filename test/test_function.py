from datetime import datetime

import pandas as pd
import pytest

from func import data, function


def account_frame(password="secret"):
    return pd.DataFrame(
        [
            {
                "Account": " A123 ",
                "Name": "Jane Doe",
                "Password": f" {password} ",
                "email": "jane@example.com",
                "strike": 0,
                "total_todos": 0,
                "max_strike": 0,
            }
        ]
    )


def test_check_account_accepts_trimmed_credentials(monkeypatch):
    monkeypatch.setattr(data, "load_account", lambda: account_frame())
    monkeypatch.setattr(data, "update_account_stats", lambda _account: None)

    result = function.check_account("  A123 ", " secret ")

    assert result["Name"] == "Jane Doe"
    assert result["Account"] == " A123 "


@pytest.mark.parametrize(
    "loaded", [None, pd.DataFrame(), pd.DataFrame(columns=data.ACCOUNT_COLUMNS)]
)
def test_check_account_handles_missing_or_empty_account_store(
    loaded, monkeypatch, capsys
):
    monkeypatch.setattr(data, "load_account", lambda: loaded)

    assert function.check_account("A123", "secret") is None
    assert "No account found" in capsys.readouterr().out


def test_check_account_reads_credentials_interactively(monkeypatch):
    monkeypatch.setattr(data, "load_account", lambda: account_frame())
    monkeypatch.setattr(data, "update_account_stats", lambda _account: None)
    answers = iter(["A123", "secret"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert function.check_account()["Account"] == " A123 "


def test_check_account_rejects_unknown_account(monkeypatch, capsys):
    monkeypatch.setattr(data, "load_account", lambda: account_frame())

    assert function.check_account("unknown", "secret") is None
    assert "Account not found" in capsys.readouterr().out


def test_check_account_rejects_wrong_password(monkeypatch, capsys):
    monkeypatch.setattr(data, "load_account", lambda: account_frame())

    assert function.check_account("A123", "wrong") is None
    assert "Incorrect password" in capsys.readouterr().out


def test_check_account_handles_row_without_password(monkeypatch, capsys):
    monkeypatch.setattr(
        data,
        "load_account",
        lambda: pd.DataFrame([{"Account": "A123", "Name": "Jane"}]),
    )

    assert function.check_account("A123", "") == {"Account": "A123", "Name": "Jane"}
    assert capsys.readouterr().out == ""


def test_acc_account_retries_password_and_saves_new_account(monkeypatch):
    monkeypatch.setattr(data, "load_account", lambda: account_frame())
    generated = iter(["Ab", "Ab"])
    monkeypatch.setattr(
        function.random, "choices", lambda *_args, **_kwargs: list(next(generated))
    )
    monkeypatch.setattr(function.random, "randint", lambda *_args: 4)
    saved = []
    monkeypatch.setattr(
        data, "save_account", lambda account: saved.append(account) or True
    )
    answers = iter(
        ["  Alice  ", " alice@example.com ", "first", "mismatch", "correct", "correct"]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    result = function.acc_account()

    assert result == saved[0]
    assert result == {
        "Account": "Ab4",
        "Name": "Alice",
        "Password": "correct",
        "email": "alice@example.com",
        "strike": 0,
        "total_todos": 0,
        "max_strike": 0,
    }


def test_acc_account_regenerates_when_candidate_already_exists(monkeypatch):
    monkeypatch.setattr(
        data, "load_account", lambda: pd.DataFrame({"Account": ["Ab4"]})
    )
    candidates = iter(["Ab", "Cd"])
    monkeypatch.setattr(
        function.random, "choices", lambda *_args, **_kwargs: list(next(candidates))
    )
    monkeypatch.setattr(function.random, "randint", lambda *_args: 4)
    monkeypatch.setattr(data, "save_account", lambda account: True)
    answers = iter(["Name", "email", "pw", "pw"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert function.acc_account()["Account"] == "Cd4"


@pytest.mark.parametrize(
    "loaded", [None, pd.DataFrame(), pd.DataFrame(columns=["Name"])]
)
def test_acc_account_supports_unavailable_or_unrecognised_account_data(
    loaded, monkeypatch
):
    monkeypatch.setattr(data, "load_account", lambda: loaded)
    monkeypatch.setattr(
        function.random, "choices", lambda *_args, **_kwargs: list("Qz")
    )
    monkeypatch.setattr(function.random, "randint", lambda *_args: 9)
    monkeypatch.setattr(data, "save_account", lambda account: True)
    answers = iter(["Name", "email", "pw", "pw"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert function.acc_account()["Account"] == "Qz9"


def test_complete_task_selects_series_and_updates_task(monkeypatch):
    account = {"Account": "A123"}
    tasks = pd.DataFrame(
        [
            {
                "acc_no": "A123",
                "head": "Study",
                "status": "pending",
                "comp_date_time": "",
            },
            {
                "acc_no": "A123",
                "head": "Exercise",
                "status": "pending",
                "comp_date_time": "",
            },
            {
                "acc_no": "B456",
                "head": "Other",
                "status": "pending",
                "comp_date_time": "",
            },
        ]
    )
    monkeypatch.setattr(function.data, "load_list", lambda: tasks)
    monkeypatch.setattr(
        function.data,
        "complete_task",
        lambda account_id, series: {
            "acc_no": account_id,
            "head": "Exercise",
            "status": "completed",
            "comp_date_time": "2026-08-21T12:00:00",
        },
    )
    monkeypatch.setattr("builtins.input", lambda _: "2")

    result = function.complete_task(account)

    assert result["head"] == "Exercise"
    assert result["status"] == "completed"
    assert result["comp_date_time"]


def test_view_task_shows_only_signed_in_users_tasks_and_activity(monkeypatch, capsys):
    account = {"Account": "A123"}
    tasks = pd.DataFrame(
        [
            {
                "acc_no": "A123",
                "head": "Study",
                "detail": "Read chapter 1",
                "status": "pending",
                "created_date_time": "2026-08-21T10:00:00",
                "comp_date_time": "",
            },
            {
                "acc_no": "A123",
                "head": "Exercise",
                "detail": "Run 5 km",
                "status": "completed",
                "created_date_time": "2026-08-20T08:00:00",
                "comp_date_time": "2026-08-21T12:00:00",
            },
            {"acc_no": "B456", "head": "Private task", "status": "pending"},
        ]
    )
    monkeypatch.setattr(function.data, "load_list", lambda: tasks)

    result = function.view_task(account)

    output = capsys.readouterr().out
    assert [task["head"] for task in result] == ["Study", "Exercise"]
    assert "Your tasks and activity:" in output
    assert "Read chapter 1" in output
    assert "completed" in output
    assert "2026-08-21T12:00:00" in output
    assert "Private task" not in output


def test_view_task_graph_saves_counts_with_axis_labels(tmp_path, monkeypatch):
    tasks = pd.DataFrame(
        [
            {"acc_no": "A123", "status": "pending", "task_date": "2026-08-24"},
            {"acc_no": "A123", "status": "completed", "task_date": "2026-08-24"},
            {"acc_no": "B456", "status": "completed", "task_date": "2026-08-24"},
        ]
    )
    monkeypatch.setattr(function.data, "load_list", lambda: tasks)
    monkeypatch.setattr(function, "IMAGE_DIR", str(tmp_path))
    figure = function.view_task_graph({"Account": "A123"})

    assert figure.endswith("task_graph_A123.png")
    assert (tmp_path / "task_graph_A123.png").is_file()


def test_generate_all_task_graphs_creates_one_graph_per_account(monkeypatch):
    accounts = pd.DataFrame(
        [
            {"Account": "A123", "Name": "Alice"},
            {"Account": "B456", "Name": "Bob"},
        ]
    )
    monkeypatch.setattr(function.data, "load_account", lambda: accounts)
    monkeypatch.setattr(
        function,
        "view_task_graph",
        lambda account: f"/graphs/task_graph_{account['Account']}.png",
    )

    assert function.generate_all_task_graphs() == {
        "A123": "/graphs/task_graph_A123.png",
        "B456": "/graphs/task_graph_B456.png",
    }


@pytest.mark.parametrize("account", [None, {}])
def test_view_task_graph_handles_missing_account(account, capsys):
    assert function.view_task_graph(account) is None
    assert "sign in" in capsys.readouterr().out


def test_add_task_persists_incremented_todo_total(tmp_path, monkeypatch):
    account_file = tmp_path / "account.csv"
    task_file = tmp_path / "list.csv"
    account_file.write_text(
        "Account,Name,Password,email,strike,total_todos,max_strike\n"
        "A123,Jane,pw,jane@example.com,0,0,0\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(data, "DATA_ACC", str(account_file))
    monkeypatch.setattr(data, "DATA_LIST", str(task_file))
    monkeypatch.setattr("builtins.input", lambda _prompt: "Study")

    account = {"Account": "A123", "total_todos": 0, "strike": 0}
    result = function.add_task(account)

    saved_account = pd.read_csv(account_file)
    assert result["head"] == "Study"
    assert result["todo_daily"] is True
    assert result["task_date"] == datetime.now().date().isoformat()
    assert saved_account.loc[0, "total_todos"] == 1
    assert saved_account.loc[0, "strike"] == 0
    assert account["total_todos"] == 1
    assert pd.read_csv(task_file).loc[0, "todo_daily"]


def test_add_daily_task_persists_daily_marker_and_date(tmp_path, monkeypatch):
    account_file = tmp_path / "account.csv"
    task_file = tmp_path / "list.csv"
    account_file.write_text(
        "Account,Name,Password,email,strike,total_todos,max_strike\n"
        "A123,Jane,pw,jane@example.com,0,0,0\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(data, "DATA_ACC", str(account_file))
    monkeypatch.setattr(data, "DATA_LIST", str(task_file))
    answers = iter(["Exercise", "Daily movement"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    result = function.add_daily_task({"Account": "A123"})

    saved_task = pd.read_csv(task_file)
    assert result["todo_daily"] is True
    assert bool(saved_task.loc[0, "todo_daily"]) is True
    assert saved_task.loc[0, "task_date"] == datetime.now().date().isoformat()
