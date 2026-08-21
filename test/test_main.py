import pytest

import main


def test_main_logs_in_and_stops(monkeypatch, capsys):
    answers = iter(["y", "A123", "secret"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(
        main.fnf, "check_account", lambda account, password: {"Name": "Jane"}
    )

    main.main()

    assert "Welcome, Jane!" in capsys.readouterr().out


def test_main_creates_account_when_user_has_no_account(monkeypatch):
    answers = iter(["n"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    created = []
    monkeypatch.setattr(main.fnf, "acc_account", lambda: created.append(True))

    main.main()

    assert created == [True]


def test_main_invalid_choice_zero_returns_cleanly(monkeypatch):
    answers = iter(["maybe", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    main.main()


def test_main_invalid_choice_one_returns_to_menu(monkeypatch, capsys):
    answers = iter(["maybe", "1", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(main.fnf, "acc_account", lambda: None)

    main.main()

    assert capsys.readouterr().out.count("Welcome to To-Do list") == 2


def test_main_failed_login_dispatches_prompts(monkeypatch):
    answers = iter(["y", "bad", "pw", "delete account"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(main.fnf, "check_account", lambda *_args: None)

    called = []

    def stop_after_prompt(value):
        called.append(value)
        raise RuntimeError("stop prompt loop")

    monkeypatch.setattr(main.pt, "prompts", stop_after_prompt)

    with pytest.raises(RuntimeError, match="stop prompt loop"):
        main.main()

    assert called == ["delete account"]


def test_main_output_uses_stable_spacing(monkeypatch, capsys):
    answers = iter(["n"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(main.fnf, "acc_account", lambda: None)

    main.main()

    output = capsys.readouterr().out
    assert "\n\n\n" not in output
    assert output.count("Welcome to To-Do list") == 1


def test_authenticated_command_is_dispatched(monkeypatch):
    answers = iter(["y", "A123", "secret", "account status", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(main.fnf, "check_account", lambda *_: {"Account": "A123", "Name": "Jane"})

    dispatched = []
    monkeypatch.setattr(
        main.fnf,
        "dispatch_command",
        lambda action, user: dispatched.append((action, user)),
    )

    main.main()

    assert dispatched == [("account_status", {"Account": "A123", "Name": "Jane"})]
