from string import ascii_letters as letters
from string import ascii_lowercase as lower
from string import ascii_uppercase as upper
from string import digits
from string import punctuation as special_symbols
from secrets import choice


class Password:

    letters = ''
    lower = ''
    upper = ''
    digits = ''
    special_symbols = ''

    def __init__(self, parameters):
        try:
            self.count = int(parameters.get('count'))
        except TypeError:
            raise Exception('The count must be an integer number')
        except ValueError:
            raise Exception('The count value were not given')

        if self.count < 4 or self.count > 50:
            raise Exception('The count value must be bigger than 4 and lower than 50')

        for parameter, value in parameters.items():
            self.__setattr__(parameter, value)

    @property
    def pool(self):
        symbols_pool = []
        if self.letters == 'on':
            symbols_pool += [letters]
        elif self.letters.isalpha():
            symbols_pool += [self.letters]
        else:
            if self.upper == 'on':
                symbols_pool += [upper]
            if self.lower == 'on':
                symbols_pool += [lower]

        if self.digits == 'on':
            symbols_pool += [digits]
        elif self.digits.isdigit():
            symbols_pool += [self.digits]

        if self.special_symbols == 'on':
            symbols_pool += [special_symbols]
        elif self.__is_special_symbols():
            symbols_pool += [self.special_symbols]

        if not symbols_pool:
            raise Exception('Permitted characters were not given')

        return symbols_pool

    @property
    def value(self):
        password = ''
        for i in range(int(self.count)):
            symbols = list(map(choice, self.pool))
            password += choice(symbols)
        return password

    def __is_special_symbols(self):
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
        'count': 14,
        'letters': 'on',
        'digits': 'on',
        'special_symbols': '!@$%^'
    }

    p = Password(parameters)
    print(p.pool)
    print(p.__dict__)

