import pandas as pd
import seaborn as sns
import random
import matplotlib.pyplot as plt
from . import data


def acc_account():
    acc_data = data.load_account()
    while True:
        acnt = random.choices(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", k=2
        ) + str(random.randint(0, 9))
        if acnt == acc_data["acc"]:
            continue
        break


if __name__ == "__main__":
    print("Oops you come wrong file.")
