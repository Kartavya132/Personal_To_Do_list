import pytest

from func import prompt


@pytest.mark.parametrize(
    "value", ["create account", "new account", "new acc", "create acc", "please create an account"]
)
def test_prompts_accepts_account_creation_phrases(value, capsys):
    assert prompt.prompts(value) is None
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize("value", ["delete account", "delete acc", "please delete an account"])
def test_prompts_accepts_account_deletion_phrases(value, capsys):
    assert prompt.prompts(value) is None
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize(
    "value", ["", "create", "account", "update account", "CREATE ACCOUNT", "new password"]
)
def test_prompts_rejects_invalid_or_case_mismatched_phrases(value, capsys):
    assert prompt.prompts(value) is None
    assert capsys.readouterr().out == "Enter the invalid Input\n"
