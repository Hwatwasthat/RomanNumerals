class Numeral:
    NUMERALS = "MDCLXVI"
    REPLACEMENTS = (
        ("IV", "IIII"),
        ("IX", "VIIII"),
        ("IL", "XXXXVIIII"),
        ("XL", "XXXX"),
        ("IC", "LXXXXVIIII"),
        ("XC", "LXXXX"),
        ("XD", "CCCCLXXXX"),
        ("ID", "CCCCLXXXXVIIII"),
        ("CD", "CCCC"),
        ("XM", "DCCCCLXXXX"),
        ("CM", "DCCCC"),
        ("IM", "DCCCCLXXXXVIIII"),
    )

    def __init__(self, value):
        self.value = self.canonicalise(value)

    def __add__(self, other):
        return Numeral(self.add(self.value, other.value))

    def __sub__(self, other):
        return Numeral(self.subtract(self.value, other.value))

    def __mul__(self, other):
        if type(other) == str and all(x in self.NUMERALS for x in other):
            return Numeral(self.multiply(self.value, (Numeral(other)).value))
        elif type(other) == Numeral:
            return Numeral(self.multiply(self.value, other.value))
        else:
            raise ValueError("Roman Numerals can only interact with Roman Numerals")

    def __rmul__(self, other):
        if type(other) == str and all(x in self.NUMERALS for x in other):
            return Numeral(self.multiply(self.value, (Numeral(other)).value))
        else:
            raise ValueError("Roman Numerals can only interact with Roman Numerals")

    def __truediv__(self, other):
        return self.divide(self.value, other.value)

    def __pow__(self, other, modulo=None):
        return Numeral(self.power(self.value, other.value))

    def __repr__(self):
        return self.value

    def add(self, arg1, arg2):
        return self.canonicalise(self.sort_descending(self.decanonicalise(arg1)
                                                      + self.decanonicalise(arg2)))

    def subtract(self, arg1, arg2):

        while arg1 and arg2:
            arg1 = self.decrement(arg1)
            arg2 = self.decrement(arg2)

        if arg2:
            raise NegativeError("Numbers cannot be below zero")

        if not arg1:
            raise ZeroError("Zero isn't a thing here")

        return arg1

    def multiply(self, arg1, arg2):
        total = ""
        while arg2:
            total = self.add(total, arg1)
            arg2 = self.decrement(arg2)

        return total

    def divide(self, arg1, arg2):
        count = ""
        while True:
            try:
                arg1 = self.subtract(arg1, arg2)
                count = self.add(count, "I")

            except NegativeError:
                if not count:
                    raise FractionError("Can't have fractions in Roman Numerals")
                return Numeral(count), Numeral(arg1)
            except ZeroError:
                return Numeral(self.add(count, "I"))

    def power(self, arg1, arg2):
        total = "I"
        while arg2:
            total = self.multiply(total, arg1)
            arg2 = self.decrement(arg2)

        return total

    def sort_descending(self, unsorted):
        return "".join(sorted(unsorted, key=self.NUMERALS.index))

    def decanonicalise(self, num):

        while True:
            old = num
            for needle, replacement in self.REPLACEMENTS:
                num = num.replace(needle, replacement)
            if old == num:
                break
        return num

    def canonicalise(self, num):

        num = num.replace("IIIII", "V")
        num = num.replace("VV", "X")
        num = num.replace("XXXXX", "L")
        num = num.replace("LL", "C")
        num = num.replace("CCCCC", "D")
        num = num.replace("DD", "M")

        while True:
            old = num
            for replacement, needle in reversed(self.REPLACEMENTS):
                num = num.replace(needle, replacement)
            if old == num:
                break
        return num

    def decrement(self, arg):
        num = self.decanonicalise(arg)
        last = num[-1]
        rest = num[:-1]
        if last == "I":
            num = rest
        elif last == "V":
            num = rest + "IIII"
        elif last == "X":
            num = rest + "VIIII"
        elif last == "L":
            num = rest + "XXXXVIIII"
        elif last == "C":
            num = rest + "LXXXXVIIII"
        elif last == "D":
            num = rest + "CCCCLXXXXVIIII"
        elif last == "M":
            num = rest + "DCCCCLXXXXVIIII"

        return num


class ZeroError(ValueError):
    pass


class NegativeError(ValueError):
    pass


class FractionError(ValueError):
    pass


class Convert:

    @staticmethod
    def roman_to_int(roman):
        rome_dict = {
            "M": 1000,
            "D": 500,
            "C": 100,
            "L": 50,
            "X": 10,
            "V": 5,
            "I": 1
        }
        result = []
        for letter in roman.value:
            result.append(rome_dict.get(letter, 0))

        return sum(result)

    @staticmethod
    def int_to_roman(integer):
        list_i = []

        while True:

            if integer > 1000:
                list_i.append("M")
                integer -= 1000

            elif integer > 100:
                list_i.append("C")
                integer -= 100

            elif integer > 10:
                list_i.append("X")
                integer -= 10

            elif integer >= 1:
                list_i.append("I")
                integer -= 1

            elif not integer:
                return Numeral("".join(list_i))
=======
    pass
>>>>>>> 4b89f7592e3364da3049a51cae6c5e3246a106d5
