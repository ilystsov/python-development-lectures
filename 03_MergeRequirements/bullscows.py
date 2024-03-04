import random
import sys
import argparse
import cowsay
from collections import Counter
import requests

word_length = 5

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


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    filtered_words = [word for word in words if len(word) == word_length]
    if not filtered_words:
        print(f"В словаре нет слов длиной {word_length} символов.")
        sys.exit(1)
    secret = random.choice(filtered_words)

    print(secret)
    guess = None
    attempts_number = 0
    while guess != secret:
        attempts_number += 1
        guess = ask("Введите слово: ", words)
        bulls, cows = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", bulls, cows)
    return attempts_number


def ask(prompt: str, valid: list[str] = None) -> str:
    guess = input(prompt)
    while valid and (guess not in valid) or (len(guess) != word_length):
        guess = input(prompt)
    return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Python version of the classic Bulls and Cows game."
    )
    parser.add_argument("dictionary", type=str, help="File name or URL")
    parser.add_argument("length", type=int, help="The length of words", default=5, nargs='?')
    args = parser.parse_args()
    word_length = args.length
    if args.dictionary.startswith(('http://', 'https://')):
        try:
            response = requests.get(args.dictionary)
            response.raise_for_status()
            word_list = response.text.split()
        except requests.RequestException as e:
            print(f"Ошибка при загрузке словаря из URL: {e}")
            sys.exit(1)
    else:
        try:
            with open(args.dictionary, 'r') as file:
                word_list = file.read().split()
        except Exception as e:
            print(f"Ошибка при открытии файла: {e}")
            sys.exit(1)

    attempts_number = gameplay(ask, inform, word_list)
    print('Суммарное число попыток:', attempts_number)