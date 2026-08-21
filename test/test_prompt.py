import pytest

from func import prompt


@pytest.mark.parametrize(
    "value",
    [
        "create account",
        "new account",
        "new acc",
        "create acc",
        "please create an account",
    ],
)
def test_prompts_accepts_account_creation_phrases(value, capsys):
    assert prompt.prompts(value) == "create_account"
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize(
    "value", ["delete account", "delete acc", "please delete an account"]
)
def test_prompts_accepts_account_deletion_phrases(value, capsys):
    assert prompt.prompts(value) == "delete_account"
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize(
    "value", ["account status", "my account", "show account", "view account status"]
)
def test_prompts_accepts_account_status_phrases(value, capsys):
    assert prompt.prompts(value) == "account_status"
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize(
    "value",
    ["", "create", "account", "update account", "new password"],
)
def test_prompts_rejects_invalid_or_case_mismatched_phrases(value, capsys):
    assert prompt.prompts(value) is None
    assert "Invalid command" in capsys.readouterr().out


def test_prompts_accepts_case_insensitive_commands():
    assert prompt.prompts("CREATE ACCOUNT") == "create_account"
