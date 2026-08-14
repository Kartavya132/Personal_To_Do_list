from func import *
from sys import exit


def main():
    while True:
        question = input("Enter do you have any account (y/n): ")
        if question == "y":
            pass
        elif question == "n":
            pass
        else:
            print("Enter the valid")
            choice = input("0 : Exit and 1 : stay :- ")
            if choice == "0":
                exit()


if __name__ == "__main__":
    main()
