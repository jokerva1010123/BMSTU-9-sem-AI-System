from typing import Callable


def read_until(prompt: str, error: str, callback: Callable[[str], bool]) -> str:
    while True:
        value = input(prompt)
        if callback(value):
            return value
        print(error)
