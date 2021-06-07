from string import ascii_letters as letters
from string import ascii_lowercase as lower
from string import ascii_uppercase as upper
from string import digits
from string import punctuation as special_symbols
from secrets import choice


class Password:
    """
    Handles password generation
    """

    letters = ''
    lower = ''
    upper = ''
    digits = ''
    special_symbols = ''

    def __init__(self, parameters):
        self.__pool = []
        self.__value = ''
        for parameter, value in parameters.items():
            if parameter == 'count':
                value = int(value)
                if value < 4 or value > 50:
                    raise ArithmeticError
            self.__setattr__(parameter, value)

    @property
    def pool(self) -> list:
        return self.__pool

    @pool.setter
    def pool(self, pool_chances: tuple) -> None:
        """
        Creates pool with given chances for each type of symbols.
        Receives chances in tuple with 3 values:
        (<letters_chances>, <digits_chances>, <special_symbol_chances>)
        """
        letters_chance, digits_chance, special_symbols_chance = pool_chances
        symbols_pool = []
        if self.letters == 'on':
            symbols_pool += letters_chance * [letters]
        elif self.letters.isalpha():
            symbols_pool += letters_chance * [self.letters]
        else:
            if self.upper == 'on':
                symbols_pool += letters_chance * [upper]
            if self.lower == 'on':
                symbols_pool += letters_chance * [lower]

        if self.digits == 'on':
            symbols_pool += digits_chance * [digits]
        elif self.digits.isdigit():
            symbols_pool += digits_chance * [self.digits]

        if self.special_symbols == 'on':
            symbols_pool += [special_symbols]
        elif self.__is_special_symbols():
            symbols_pool += [self.special_symbols]

        if not symbols_pool:
            raise IndexError

        self.__pool = symbols_pool

    @pool.deleter
    def pool(self):
        del self.__pool

    @property
    def value(self) -> str:
        password = ''
        for i in range(int(self.count)):
            symbols = list(map(choice, self.pool))
            password += choice(symbols)
        return password

    def __is_special_symbols(self) -> bool:
        if not self.special_symbols:
            return False
        for symbol in self.special_symbols:
            if symbol not in special_symbols:
                return False
        return True

    def __repr__(self):
        return self.value


if __name__ == '__main__':
    parameters = {
        'count': '',
        'letters': 'on',
        'digits': 'on',
        'special_symbols': '!@$%^'
    }

    p = Password(parameters)
    p.pool = (2, 2, 1)
    print(p)

