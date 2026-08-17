from sys import exit

# Command definitions with keywords
COMMANDS = {
    "create_account": {
        "keywords": [
            ("create", "account"),
            ("new", "account"),
            ("new", "acc"),
            ("create", "acc"),
        ],
        "description": "Create a new account",
        "action": "create_account",
    },
    "delete_account": {
        "keywords": [("delete", "account"), ("delete", "acc")],
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
    user_input_lower = user_input.lower().strip()

    for cmd_name, cmd_info in COMMANDS.items():
        for keyword_set in cmd_info["keywords"]:
            # Check if all keywords in the set are present in the input
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
    Returns the command action or "invalid" if no command matched.
    """
    if not user_input or not user_input.strip():
        print(
            "\n⚠️  Please enter a valid command. Type 'help' to see available commands.\n"
        )
        return "invalid"

    # Check for help command
    if user_input.lower().strip() in ["help", "?", "h"]:
        show_help()
        return "help"

    # Parse the user input
    result = parse_command(user_input)

    if result is None:
        print("\n❌ Command not recognized. Type 'help' for available commands.\n")
        return "invalid"

    # Execute the matched command
    action = result["action"]

    if action == "create_account":
        print("\n✅ Command recognized: Create Account\n")
        # Placeholder - actual account creation handled in main flow
        return "create_account"

    elif action == "delete_account":
        print("\n✅ Command recognized: Delete Account\n")
        # Placeholder - actual deletion would be handled elsewhere
        return "delete_account"

    elif action == "exit":
        print("\n" + "╔" + "═" * 48 + "╗")
        print("║" + "✨ Thank You For Using To-Do List! ✨".center(48) + "║")
        print("║" + "See you soon. Good Bye! 👋".center(48) + "║")
        print("╚" + "═" * 48 + "╝" + "\n")
        exit()

    return action


if __name__ == "__main__":
    print("Oops you come wrong file.")
