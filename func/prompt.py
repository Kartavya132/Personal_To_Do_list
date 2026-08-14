from sys import exit


def prompts(prompt):
    if (
        ("create" in prompt and "account" in prompt)
        or ("new" in prompt and "account" in prompt)
        or ("new" in prompt and "acc" in prompt)
        or ("create" in prompt and "acc" in prompt)
    ):
        pass
    elif ("delete" in prompt and "account" in prompt) or (
        "delete" in prompt and "acc" in prompt
    ):
        pass
    else:
        print("Enter the invalid Input")


if __name__ == "__main__":
    print("Oops you come wrong file.")
