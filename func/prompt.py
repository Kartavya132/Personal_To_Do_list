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
    "add_task": {
        "keywords": [
            ("add", "task"),
            ("new", "task"),
            ("please", "add", "task"),
            ("renew", "task"),
            ("make", "task"),
        ],
        "description": "Adding a new task",
        "action": "add_task",
    },
    "view_task": {
        "keywords": [
            ("view", "task"),
            ("see", "task"),
            ("see", "all", "task"),
            ("watch", "task"),
            ("check", "task"),
        ],
        "description": "See all all the task",
        "action": "view_task",
    },
    "complete_task": {
        "keywords": [
            ("complete", "task"),
            ("end", "task"),
            ("please", "completed", "task"),
            ("over", "task"),
            ("comp", "task"),
        ],
        "description": "complete a task task",
        "action": "complete_task",
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
    if not cleaned:
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
    print("\n" + "╔" + "═" * 48 + "╗")
    print("║" + "📚 AVAILABLE COMMANDS 📚".center(45) + " ║")
    print("╠" + "═" * 48 + "╣")

    cmd_count = 1
    for cmd_name, cmd_info in COMMANDS.items():
        examples = " | ".join([" ".join(kw) for kw in cmd_info["keywords"][:2]])
        print(f"║ {cmd_count}. {cmd_info['description'].title():<43} ║")
        print(f"║    Example: {examples:<34} ║")
        cmd_count += 1

    print("╚" + "═" * 48 + "╝" + "\n")


def prompts(user_input):
    """Convert a user command into an action for the application to run.

    This module only handles command parsing and display.  ``main`` dispatches
    the returned action to the matching function, where account and data work
    belongs.
    """
    if not user_input or not user_input.strip():
        print("Invalid command. Type 'help' to see the available commands.")
        return None

    if user_input.strip().lower() in ["help", "?", "h"]:
        show_help()
        return "help"

    result = parse_command(user_input)

    if result is None:
        print("Invalid command. Type 'help' to see the available commands.")
        return None

    return result["action"]


if __name__ == "__main__":
    print("Oops you come wrong file.")
