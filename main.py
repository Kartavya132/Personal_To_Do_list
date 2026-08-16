import func.function as fnf
import func.prompt as pt
from sys import exit


def main():
    while True:
        print("=======================")
        print(" Welcome to To-Do list ")
        print("=======================\n")
        question = input("Enter do you have any account (y/n): ")
        if question == "y":
            account_number = input("Enter your account number: ").strip()
            password = input("Enter your password: ").strip()
            user = fnf.check_account(account_number, password)
            if user is not None:
                print(f"Welcome, {user['Name']}!")
                break
            while True:
                prompt = input("Enter what do you want : ")
                pt.prompts(prompt)
        elif question == "n":
            fnf.acc_account()
            break
        else:
            print("Enter the valid")
            choice = input("0 : Exit and 1 : stay :- ")
            if choice == "0":
                exit()


if __name__ == "__main__":
    main()
