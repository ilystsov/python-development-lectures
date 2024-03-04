import cowsay
from collections import Counter


def bullscows(guess: str, secret: str) -> (int, int):
    bulls, cows = 0, 0
    for i in range(len(secret)):
        if guess[i] == secret[i]:
            bulls += 1

    secret_letters_counter = Counter(secret)
    for i in range(len(guess)):
        letter = guess[i]
        if (
            letter in secret_letters_counter
            and secret_letters_counter[letter] > 0
            and letter != secret[i]
        ):
            secret_letters_counter[letter] -= 1
            cows += 1
    return bulls, cows


def ask(prompt: str, valid: list[str] = None) -> str:
    guess = input(prompt)
    while valid and guess not in valid:
        guess = input(prompt)
    return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))
