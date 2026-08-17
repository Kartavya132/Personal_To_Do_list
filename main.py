import func.function as fnf
import func.prompt as pt
import func.data as data
from sys import exit


def print_header(title):
    """Print a formatted header"""
    width = 50
    print("\n" + "═" * width)
    print(title.center(width))
    print("═" * width + "\n")


def print_separator():
    """Print a separator line"""
    print("─" * 50)


def main():
    current_user = None

    while True:
        print("\n" + "╔" + "═" * 48 + "╗")
        print("║" + "Welcome to To-Do List".center(48) + "║")
        print("╚" + "═" * 48 + "╝" + "\n")

        question = input("📋 Do you have an account? (yes/no): ").strip().lower()

        if question in ["y", "yes"]:
            print_separator()
            account_number = input("🔑 Account Number: ").strip()
            password = input("🔒 Password: ").strip()
            print_separator()
            user = fnf.check_account(account_number, password)

            if user is not None:
                current_user = user
                print(f"\n✅ Welcome back, {user['Name']}!\n")
                data.display_account(user)

                # Main menu loop for logged-in user
                while True:
                    print("─" * 50)
                    print("💡 Tip: Type 'help' for available commands")
                    print("─" * 50)
                    user_command = input("\n👉 Command: ").strip()

                    if not user_command:
                        continue

                    result = pt.prompts(user_command)

                    if result == "help":
                        continue
                    elif result == "exit":
                        return
                    elif result == "invalid":
                        continue

        elif question in ["n", "no"]:
            print_header("🎉 CREATE NEW ACCOUNT 🎉")
            new_account = fnf.acc_account()
            if new_account:
                print("\n" + "✨" * 25)
                print("\n  🎊 Account Successfully Created! 🎊\n")
                print("✨" * 25 + "\n")
                break

        else:
            print("\n❌ Invalid input! Please enter 'yes' or 'no'.")
            choice = input("\n⚙️  Enter '0' to exit or '1' to try again: ").strip()
            if choice == "0":
                print_header("👋 THANK YOU FOR USING TO-DO LIST 👋")
                exit()


if __name__ == "__main__":
    main()
