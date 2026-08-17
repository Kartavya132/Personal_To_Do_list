from sys import exit

# Command definitions with keywords
COMMANDS = {
    "create_account": {
        "keywords": [
            ("create", "account"),
            ("new", "account"),
            ("new", "acc"),
            ("create", "acc"),
            ("please", "create", "an", "account"),
        ],
        "description": "Create a new account",
        "action": "create_account",
    },
    "account_status": {
        "keywords": [
            ("account", "status"),
            ("my", "account"),
            ("show", "account"),
            ("view", "account"),
            ("show", "my", "account"),
            ("view", "account", "status"),
        ],
        "description": "View your account and account status",
        "action": "account_status",
    },
    "delete_account": {
        "keywords": [
            ("delete", "account"),
            ("delete", "acc"),
            ("please", "delete", "an", "account"),
        ],
        "description": "Delete your account",
        "action": "delete_account",
    },
    "exit": {
        "keywords": [("exit",), ("back",), ("end",), ("quit",), ("bye",)],
        "description": "Exit the application",
        "action": "exit",
    },
}


def parse_command(user_input):
    """
    Parse user input and identify the command.
    Returns a dictionary with command info or None if no match.
    """
    if user_input is None:
        return None

    cleaned = user_input.strip()
    if not cleaned or cleaned != cleaned.lower():
        return None

    user_input_lower = cleaned.lower()

    for cmd_name, cmd_info in COMMANDS.items():
        for keyword_set in cmd_info["keywords"]:
            if all(keyword in user_input_lower for keyword in keyword_set):
                return {
                    "command": cmd_name,
                    "action": cmd_info["action"],
                    "description": cmd_info["description"],
                }

    return None


def show_help():
    """Display available commands"""
    print("\n" + "╔" + "═" * 48 + "╗")
    print("║" + "📚 AVAILABLE COMMANDS 📚".center(48) + "║")
    print("╠" + "═" * 48 + "╣")

    cmd_count = 1
    for cmd_name, cmd_info in COMMANDS.items():
        examples = " | ".join([" ".join(kw) for kw in cmd_info["keywords"][:2]])
        print(f"║ {cmd_count}. {cmd_info['description'].title():<44} ║")
        print(f"║    Example: {examples:<39} ║")
        cmd_count += 1

    print("╚" + "═" * 48 + "╝" + "\n")


def prompts(user_input):
    """
    Main prompt handler that parses user input and processes commands.
    Returns None for valid commands, "exit" when quitting, or None for invalid.
    """
    if not user_input or not user_input.strip():
        print("Enter the invalid Input")
        return None

    if user_input.strip().lower() in ["help", "?", "h"]:
        show_help()
        return None

    result = parse_command(user_input)

    if result is None:
        print("Enter the invalid Input")
        return None

    action = result["action"]

    if action == "exit":
        print("\n" + "╔" + "═" * 48 + "╗")
        print("║" + "✨ Thank You For Using To-Do List! ✨".center(48) + "║")
        print("║" + "See you soon. Good Bye! 👋".center(48) + "║")
        print("╚" + "═" * 48 + "╝" + "\n")
        exit()

    return None


if __name__ == "__main__":
    print("Oops you come wrong file.")
