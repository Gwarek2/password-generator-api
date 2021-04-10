from string import punctuation
from secrets import choice


def is_special_symbols(char_pool: str) -> bool:
    """
    Checks if string contains special symbols
    """
    if not char_pool:
        return False
    for symbol in char_pool:
        if symbol not in punctuation:
            return False
    return True


def diversify_pool(letters: str, numbers: str, special_symbols: str) -> list:
    """
    Unites pool of all types of characters into the list and gives each type a definite chance of choosing
    """
    char_pool = []
    if letters:
        char_pool += 2 * [letters]
    if numbers:
        char_pool += 2 * [numbers]
    if special_symbols:
        char_pool += [special_symbols]
    return char_pool


def generate_password(permitted_chars, length):
    password = ''
    for i in range(length):
        iteration_pool = list(map(choice, permitted_chars))
        password += choice(iteration_pool)
    return password