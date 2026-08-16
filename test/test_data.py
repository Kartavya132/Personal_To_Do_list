import pandas as pd
import pytest

from func import data


def test_normalise_columns_handles_none_and_adds_schema_columns():
    result = data._normalise_columns(None, data.ACCOUNT_COLUMNS)

    assert result.empty
    assert list(result.columns) == data.ACCOUNT_COLUMNS


def test_normalise_columns_maps_aliases_and_preserves_extra_columns():
    source = pd.DataFrame([{" acc ": "A1", "name": "Alex", "pass": "pw", "custom": 7}])

    result = data._normalise_columns(source, data.ACCOUNT_COLUMNS)

    assert result.loc[0, "Account"] == "A1"
    assert result.loc[0, "Name"] == "Alex"
    assert result.loc[0, "Password"] == "pw"
    assert result.loc[0, "custom"] == 7
    assert set(data.ACCOUNT_COLUMNS).issubset(result.columns)


@pytest.mark.parametrize(
    ("loader", "path_name"),
    [(data.load_account, "DATA_ACC"), (data.load_list, "DATA_LIST")],
)
def test_loaders_return_none_for_missing_files(
    loader, path_name, tmp_path, monkeypatch, capsys
):
    missing = tmp_path / "missing.csv"
    monkeypatch.setattr(data, path_name, str(missing))

    result = loader()

    assert result is None
    assert "not found" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("loader", "path_name", "columns"),
    [
        (data.load_account, "DATA_ACC", data.ACCOUNT_COLUMNS),
        (data.load_list, "DATA_LIST", data.LIST_COLUMNS),
    ],
)
def test_loaders_return_empty_schema_for_empty_files(
    loader, path_name, columns, tmp_path, monkeypatch
):
    empty = tmp_path / "empty.csv"
    empty.write_text("", encoding="utf-8")
    monkeypatch.setattr(data, path_name, str(empty))

    result = loader()

    assert result is not None
    assert result.empty
    assert list(result.columns) == columns


def test_load_account_normalises_legacy_column_names(tmp_path, monkeypatch):
    account_file = tmp_path / "account.csv"
    account_file.write_text(
        "acc,name,pass,email\n A7 ,Ada,pw,ada@example.com\n", encoding="utf-8"
    )
    monkeypatch.setattr(data, "DATA_ACC", str(account_file))

    result = data.load_account()

    assert result.loc[0, "Account"] == " A7 "
    assert result.loc[0, "Password"] == "pw"
    assert pd.isna(result.loc[0, "strike"])


@pytest.mark.parametrize(
    ("loader", "path_name", "columns"),
    [
        (data.load_account, "DATA_ACC", data.ACCOUNT_COLUMNS),
        (data.load_list, "DATA_LIST", data.LIST_COLUMNS),
    ],
)
def test_loaders_return_schema_for_header_only_csv(loader, path_name, columns, tmp_path, monkeypatch):
    header_only = tmp_path / "header-only.csv"
    header_only.write_text(",".join(columns) + "\n", encoding="utf-8")
    monkeypatch.setattr(data, path_name, str(header_only))

    result = loader()

    assert result.empty
    assert list(result.columns) == columns


@pytest.mark.parametrize("loader", [data.load_account, data.load_list])
def test_loaders_convert_unexpected_read_errors_to_none(loader, monkeypatch):
    monkeypatch.setattr(data.os.path, "exists", lambda _: True)
    monkeypatch.setattr(
        data.pd, "read_csv", lambda _: (_ for _ in ()).throw(OSError("boom"))
    )

    assert loader() is None


def test_save_account_dict_creates_parent_and_schema(tmp_path, monkeypatch, capsys):
    target = tmp_path / "nested" / "account.csv"
    monkeypatch.setattr(data, "DATA_ACC", str(target))

    assert data.save_account({"acc": "A1", "name": "Alex", "pass": "pw"}) is True

    saved = pd.read_csv(target)
    assert saved.loc[0, "Account"] == "A1"
    assert saved.loc[0, "Name"] == "Alex"
    assert list(saved.columns) == [
        "Account",
        "Name",
        "Password",
        "email",
        "strike",
        "total_todos",
        "max_strike",
    ]
    assert "Account saved successfully!" in capsys.readouterr().out


def test_save_account_appends_without_duplicate_header(tmp_path, monkeypatch):
    target = tmp_path / "account.csv"
    target.write_text(
        ",".join(data.ACCOUNT_COLUMNS) + "\nA1,Alex,pw,a@example.com,0,0,0\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(data, "DATA_ACC", str(target))

    assert data.save_account(pd.DataFrame([{"Account": "A2", "Name": "Bea"}])) is True

    saved = pd.read_csv(target)
    assert list(saved["Account"]) == ["A1", "A2"]
    assert target.read_text(encoding="utf-8").count("Account,Name") == 1


def test_save_list_writes_dict_and_empty_file_is_treated_as_new(tmp_path, monkeypatch):
    target = tmp_path / "list.csv"
    target.write_text("", encoding="utf-8")
    monkeypatch.setattr(data, "DATA_LIST", str(target))

    assert data.save_list({"acc_no": "A1", "head": "Study"}) is True

    saved = pd.read_csv(target)
    assert saved.loc[0, "Account"] == "A1"
    assert saved.loc[0, "head"] == "Study"
    assert saved.columns[0] == "Account"
    assert set(data.LIST_COLUMNS[2:]).issubset(saved.columns)


def test_save_list_appends_to_existing_file_without_header(tmp_path, monkeypatch):
    target = tmp_path / "list.csv"
    monkeypatch.setattr(data, "DATA_LIST", str(target))

    assert data.save_list({"acc_no": "A1", "head": "Read"}) is True
    assert data.save_list({"acc_no": "A2", "head": "Write"}) is True

    assert target.read_text(encoding="utf-8").count("Account,head") == 1
    assert list(pd.read_csv(target)["Account"]) == ["A1", "A2"]


@pytest.mark.parametrize(
    ("saver", "path_name"),
    [(data.save_account, "DATA_ACC"), (data.save_list, "DATA_LIST")],
)
def test_savers_return_false_for_invalid_input(
    saver, path_name, tmp_path, monkeypatch, capsys
):
    monkeypatch.setattr(data, path_name, str(tmp_path / "output.csv"))

    assert saver(object()) is False
    assert "Error saving" in capsys.readouterr().out
