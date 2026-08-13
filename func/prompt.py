from sys import exit


def prompts(prompt):
    if (
        ("create" in prompt and "account" in prompt)
        or ("new" in prompt and "account" in prompt)
        or ("new" in prompt and "acc" in prompt)
        or ("create" in prompt and "acc" in prompt)
    ):
        pass
