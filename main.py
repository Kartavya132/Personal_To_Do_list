import func.function as fnf
import func.prompt as pt


def print_box(title, width=52):
    inner_width = width - 2
    border = "═" * inner_width
    print(f"╔{border}╗")
    print(f"║{str(title).center(inner_width)}║")
    print(f"╚{border}╝")


def print_header(title):
    print_box(title)


def print_separator():
    print("─" * 52)


def print_goodbye():
    print_box("✨ Thank You For Using To-Do List! ✨")
    print("See you soon. Good Bye! 👋")


def command_loop(current_user):
    """Run commands for a signed-in user until they choose to exit."""
    print("Type 'help' to see the available commands.")

    while True:
        try:
            user_command = input("\n👉 Command: ")
        except (EOFError, StopIteration):
            return

        action = pt.prompts(user_command)
        if action in (None, "help"):
            continue
        if action == "exit":
            print_goodbye()
            return

        fnf.dispatch_command(action, current_user)


def main():
    while True:
        print_box("Welcome to To-Do list")
        question = input("📋 Do you have an account? (yes/no): ").strip().lower()

        if question in ["y", "yes"]:
            print_separator()
            account_number = input("🔑 Account Number: ").strip()
            password = input("🔒 Password: ").strip()
            print_separator()
            user = fnf.check_account(account_number, password)

            if user is not None:
                print(f"✅ Welcome, {user['Name']}!")
                command_loop(user)
                return

            print("⚠️  Login failed. Try a command below or re-enter your account.")
            action = pt.prompts(input("👉 Command: "))
            if action == "exit":
                print_goodbye()
                return
            if action == "create_account":
                fnf.dispatch_command(action)
            continue

        elif question in ["n", "no"]:
            print_header("🎉 CREATE NEW ACCOUNT 🎉")
            fnf.acc_account()
            print("✨" * 25)
            print("  🎊 Account Successfully Created! 🎊")
            print("✨" * 25)
            return

        else:
            print("❌ Invalid input! Please enter 'yes' or 'no'.")
            choice = input("⚙️  Enter '0' to exit or '1' to try again: ").strip()
            if choice == "0":
                print_goodbye()
                return
            if choice == "1":
                continue


if __name__ == "__main__":
    main()
