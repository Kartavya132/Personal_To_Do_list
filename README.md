<h1 align="center">✅ Personal To-Do List</h1>
<p align="center"><b>A command-line to-do app with accounts, streak tracking, and activity graphs.</b></p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white">
  <img alt="pandas" src="https://img.shields.io/badge/pandas-CSV%20persistence-150458?logo=pandas&logoColor=white">
  <img alt="matplotlib" src="https://img.shields.io/badge/matplotlib-activity%20graphs-11557c?logo=plotly&logoColor=white">
  <img alt="pytest" src="https://img.shields.io/badge/tested%20with-pytest-0A9EDC?logo=pytest&logoColor=white">
  <img alt="CLI" src="https://img.shields.io/badge/interface-CLI-black?logo=gnometerminal&logoColor=white">
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-demo">Demo</a> •
  <a href="#️-project-structure">Structure</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-commands">Commands</a> •
  <a href="#-testing">Testing</a>
</p>

---

## ✨ Features

| | |
|---|---|
| 🔐 **Accounts** | Create an account or sign in with an account number + password |
| ✅ **Per-user tasks** | Add, view, and complete daily tasks, scoped to the signed-in user |
| 🔥 **Streaks** | Daily completion streaks tracked automatically |
| 📊 **Activity graphs** | Generate a PNG graph of task history on demand |
| 🗑️ **Safe deletion** | Account deletion requires typing `delete` to confirm |
| 🧠 **Forgiving input** | Commands are parsed case-insensitively |
| 💾 **Zero-setup storage** | Plain CSV files — no database server to install or manage |

## 🎬 Demo

<details open>
<summary><b>Click to expand a sample session</b></summary>

```text
╔══════════════════════════════════════════════╗
║              Welcome to To-Do list            ║
╚══════════════════════════════════════════════╝
📋 Do you have an account? (yes/no): yes
────────────────────────────────────────────────
🔑 Account Number: 1024
🔒 Password: ********
────────────────────────────────────────────────
✅ Welcome, Prince!
Type 'help' to see the available commands.

👉 Command: add task
👉 Command: view task
👉 Command: complete task
👉 Command: view task graph
👉 Command: account status
👉 Command: exit
╔══════════════════════════════════════════════╗
║       ✨ Thank You For Using To-Do List! ✨      ║
╚══════════════════════════════════════════════╝
See you soon. Good Bye! 👋
```

</details>

### Try the sample data

The repository includes safe demo records so the app is useful immediately:

| Account | Password | Tasks | Best streak |
|---|---|---:|---:|
| `A123` | `secret` | 3 | 2 |
| `B456` | `daily` | 2 | 2 |
| `C789` | `welcome` | 1 | 0 |

These are demonstration credentials only. Replace the sample CSV files before
using the project for real personal data.

## 🗂️ Project Structure

```text
.
├── main.py            # Entry point — login/account-creation flow, command loop
├── func/               # Application logic (account handling, commands, prompts)
├── data/               # Persisted CSV data (account.csv, list.csv)
├── image/               # Generated task activity graphs (PNG)
├── test/               # Pytest test suite
└── requirements.txt    # Python dependencies
```

## ⚙️ Requirements

- Python 3.10 or newer
- [`pandas`](https://pandas.pydata.org/) — CSV persistence and statistics
- [`matplotlib`](https://matplotlib.org/) — task activity graphs

## 🚀 Installation

```bash
# 1. Move into the project directory
cd Personal_To_Do_list

# 2. Install dependencies
python -m pip install -r requirements.txt
```

## ▶️ Usage

```bash
python main.py
```

For a first run, sign in with `A123` and `secret`, then try `view task`,
`account status`, or `view task graph`.

On startup you'll be asked whether you already have an account:

- **Yes** → enter your account number and password to sign in. A failed login
  lets you retry or exit.
- **No** → you'll be walked through creating a new account.

Once signed in, you land in the command menu. Data paths are resolved
relative to the project, so the app can be launched from any working
directory:

| Data | Location |
|---|---|
| Account records | `data/account.csv` |
| Task records | `data/list.csv` |
| Activity graphs | `image/` |

## 🧭 Commands

Type `help` at any time to see this menu in-app.

| Command | Purpose |
|---|---|
| `account status` | Show the signed-in account and statistics |
| `add task` | Add a daily task |
| `view task` | List the signed-in user's tasks |
| `complete task` | Mark a selected task as completed |
| `view task graph` | Generate a PNG activity graph |
| `delete account` | Permanently delete the account and its tasks |
| `exit` | Leave the application |

> Commands are case-insensitive. Account deletion requires typing `delete` as
> an extra confirmation step.

## 🧪 Testing

```bash
python -m pytest -q
```

Tests use temporary CSV files wherever persistence is involved, so running
the suite never touches the sample data in `data/`.

To restore the bundled demo data after experimenting, restore
`data/account.csv` and `data/list.csv` from version control.

## 🤝 Contributing

Issues and pull requests are welcome — fork the repo, create a feature
branch, and open a PR describing your change.

## 📄 License

_No license file is currently included in this project. Add a `LICENSE`
file (MIT, Apache-2.0, etc.) if you'd like others to know how they can use
this code — happy to generate one if you tell me which license you want._