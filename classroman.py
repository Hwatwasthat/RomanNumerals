class Numeral:
    NUMERALS = "MDCLXVI"
    REPLACEMENTS = (
        ("IV", "IIII"),
        ("IX", "VIIII"),
        ("XL", "XXXX"),
        ("XC", "LXXXX"),
        ("CD", "CCCC"),
        ("CM", "DCCCC"),
    )

    def __init__(self, value):
        self.value = self._canonicalise(value)

    def __add__(self, other):
        if type(other) == str and all(x in self.NUMERALS for x in other):
            return Numeral(self._add(self.value, (Numeral(other)).value))

        elif type(other) == int:
            return Numeral(self._add(self.value, (Convert.int_to_roman(other)).value))

        elif type(other) == Numeral:
            return Numeral(self._add(self.value, other.value))

        else:
            raise ValueError("Roman Numerals can only interact with Roman Numerals and integers")

    def __sub__(self, other):
        if type(other) == str and all(x in self.NUMERALS for x in other):
            return Numeral(self._subtract(self.value, (Numeral(other)).value))

        elif type(other) == int:
            return Numeral(self._subtract(self.value, (Convert.int_to_roman(other)).value))

        elif type(other) == Numeral:
            return Numeral(self._subtract(self.value, other.value))

        else:
            raise ValueError("Roman Numerals can only interact with Roman Numerals and integers")

    def __mul__(self, other):
        if type(other) == str and all(x in self.NUMERALS for x in other):
            return Numeral(self._multiply(self.value, (Numeral(other)).value))

        elif type(other) == int:
            return Numeral(self._multiply(self.value, (Convert.int_to_roman(other)).value))

        elif type(other) == Numeral:
            return Numeral(self._multiply(self.value, other.value))

        else:
            raise ValueError("Roman Numerals can only interact with Roman Numerals and integers")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        """
        Divides by a Roman Numeral, string with Roman Numeral characters or an integer.
        Only returns whole numbers, as Roman fractions only exist in /12 format.
        If partial division is necessary, returns a remainder value.
        :param other: Object to divide by. May be a Roman Numeral object, string or integer.
        :return: Returns a Roman Numeral object, or two if their is a remainder.
        """
        if type(other) == str and all(x in self.NUMERALS for x in other):
            return self._divide(self.value, (Numeral(other)).value)

        elif type(other) == int:
            return self._divide(self.value, (Convert.int_to_roman(other)).value)

        elif type(other) == Numeral:
            return self._divide(self.value, other.value)

        else:
            raise ValueError("Roman Numerals can only interact with Roman Numerals and integers")

    def __pow__(self, other, modulo=None):
        if type(other) == str and all(x in self.NUMERALS for x in other):
            return Numeral(self._power(self.value, (Numeral(other)).value))

        elif type(other) == int:
            return Numeral(self._power(self.value, (Convert.int_to_roman(other)).value))

        elif type(other) == Numeral:
            return Numeral(self._power(self.value, other.value))

        else:
            raise ValueError("Roman Numerals can only interact with Roman Numerals and integers")

    def __mod__(self, other):
        if type(other) == str and all(x in self.NUMERALS for x in other):
            return Numeral(self.modulo(self.value, (Numeral(other)).value))

        elif type(other) == int:
            return Numeral(self.modulo(self.value, (Convert.int_to_roman(other)).value))

        elif type(other) == Numeral:
            return Numeral(self.modulo(self.value, other.value))

        else:
            raise ValueError("Roman Numerals can only interact with Roman Numerals and integers")

    def __repr__(self):
        return self.value

    def _add(self, arg1, arg2):
        return self._canonicalise(self._sort_descending(self._decanonicalise(arg1)
                                                        + self._decanonicalise(arg2)))

    def _subtract(self, arg1, arg2):

        while arg1 and arg2:
            arg1 = self._decrement(arg1)
            arg2 = self._decrement(arg2)

        if arg2:
            raise NegativeError("Numbers cannot be below zero")

        if not arg1:
            raise ZeroError("Zero isn't a thing here")

        return arg1

    def _multiply(self, arg1, arg2):
        total = ""
        while arg2:
            total = self._add(total, arg1)
            arg2 = self._decrement(arg2)

        return total

    def _divide(self, arg1, arg2):
        count = ""
        while True:
            try:
                arg1 = self._subtract(arg1, arg2)
                count = self._add(count, "I")

            except NegativeError:
                if not count:
                    raise FractionError("Can't have fractions in Roman Numerals")
                return Numeral(count), Numeral(arg1)
            except ZeroError:
                return Numeral(self._add(count, "I"))

    def _power(self, arg1, arg2):
        total = "I"
        while arg2:
            total = self._multiply(total, arg1)
            arg2 = self._decrement(arg2)

        return total

    def modulo(self, arg1, arg2):
        while True:
            res = arg1
            try:
                arg1 = self._subtract(arg1, arg2)
            except ZeroError:
                res = ""
                break
            except NegativeError:
                break
        return res

    def _sort_descending(self, unsorted):
        return "".join(sorted(unsorted, key=self.NUMERALS.index))

    def _decanonicalise(self, num):

        while True:
            old = num
            for needle, replacement in self.REPLACEMENTS:
                num = num.replace(needle, replacement)
            if old == num:
                break
        return num

    def _canonicalise(self, num):
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

    def _decrement(self, arg):
        num = self._decanonicalise(arg)
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
