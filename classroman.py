class Numeral:
    """
    Class for Roman Numerals. Can add, multiply, flat divide, modulo and raise
    to powers. Has capability to change from integers and back again, and accepts
    strings and integers as arguments.
    """
    _NUMERALS = "MDCLXVI"
    _REPLACEMENTS = (
        ("IV", "IIII"),
        ("IX", "VIIII"),
        ("XL", "XXXX"),
        ("XC", "LXXXX"),
        ("CD", "CCCC"),
        ("CM", "DCCCC"),
    )

    def __init__(self, value):
        """
        Only accepts strings and integers, returns a Numeral object.
        :param value: str or int.
        """
        if type(value) == str:
            self.value = self._canonicalise(self._sort_descending(value.upper()))
        elif type(value) == int:
            self.value = self.from_int(value).value
        else:
            raise TypeError("Expected str or int")

    def __add__(self, other):
        """
        Add values. Accepts str, int or Numeral object.
        :param other: value to add.
        :return: Numeral object with added value.
        """
        return Numeral(self._add(*self._checker(other)))

    def __radd__(self, other):
        """
        Add Numeral to integer.
        :param other: value to add to.
        :return: integer.
        """
        return other + self.to_int()

    def __sub__(self, other):
        """
        subtract a value. Accepts str, int or Numeral object.
        :param other: value to subtract.
        :return: Numeral object.
        """
        return Numeral(self._subtract(*self._checker(other)))

    def __rsub__(self, other):
        """
        Subtract Numeral from an integer.
        :param other: int to subtract.
        :return: integer.
        """
        return other - self.to_int()

    def __mul__(self, other):
        return Numeral(self._multiply(*self._checker(other)))

    def __rmul__(self, other):
        return other * self.to_int()

    def __truediv__(self, other):
        return self._divide(*self._checker(other))

    def __rtruediv__(self, other: int):
        """
        Divide integer by Numeral value.
        :param other: integer.
        :return: integer.
        """
        return other / self.to_int()

    def __rfloordiv__(self, other: int):
        """
        Floor divide integer by Numeral value.
        :param other: integer.
        :return: integer.
        """
        return other // self.to_int()

    def __pow__(self, other, modulo=None):
        return Numeral(self._power(*self._checker(other)))

    def __rpow__(self, other):
        return other ** self.to_int()

    def __mod__(self, other):
        return Numeral(self._modulo(*self._checker(other)))

    def __rmod__(self, other):
        return other % self.to_int()

    def __repr__(self):
        return self.value

    def _checker(self, other):
        """
        checks type of value to be used as other side of argument. returns
        a Numeral objects value for computation against.
        :param other: str, int or Numeral object for calculation against.
        :return: Numeral objects value.
        """
        if type(other) == str and all(x in self._NUMERALS for x in other):
            return self.value, Numeral(other).value

        elif type(other) == int:
            return self.value, self.from_int(other).value

        elif type(other) == Numeral:
            return self.value, other.value

        else:
            raise ValueError("Expected Numeral, str or int")

    def _add(self, arg1, arg2):
        """
        Internal method for addition.
        :param arg1: Numeral object value.
        :param arg2: Numeral object value.
        :return: Ordered str for placement in new Numeral object.
        """
        return self._canonicalise(self._sort_descending(self._decanonicalise(arg1)
                                                        + self._decanonicalise(arg2)))

    def _subtract(self, arg1, arg2):
        """
        Internal method for subtraction.
        :param arg1: Numeral object value.
        :param arg2: Numeral object value.
        :return: Ordered str for placement in new Numeral object.
        """
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

    def _modulo(self, arg1, arg2):
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
        """
        Internal method to sort string into order from greatest to least.
        :param unsorted: str to be sorted.
        :return: a str sorted by the NUMERAL str order.
        """
        return "".join(sorted(unsorted, key=self._NUMERALS.index))

    def _decanonicalise(self, num):
        """
        Internal method, breaks down compacted values to longer strings
        for computation (eg. VIIII from IX).
        :param num: str to be decomposed.
        :return: decomposed string.
        """
        while True:
            old = num
            for needle, replacement in self._REPLACEMENTS:
                num = num.replace(needle, replacement)
            if old == num:
                break
        return num

    def _canonicalise(self, num):
        """
        Internal method to replace values with their next greater, or appropriate
        shortening (e.g. IX instead of VIIII).
        :param num: decomposed str.
        :return:
        """
        num = num.replace("IIIII", "V")
        num = num.replace("VV", "X")
        num = num.replace("XXXXX", "L")
        num = num.replace("LL", "C")
        num = num.replace("CCCCC", "D")
        num = num.replace("DD", "M")

        while True:
            old = num
            for replacement, needle in reversed(self._REPLACEMENTS):
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

    def to_int(self):
        """
        Returns the current Numeral objects integer value.
        :return: int.
        """
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
        decanon = self._decanonicalise(self.value)
        for letter in decanon:
            result.append(rome_dict.get(letter, 0))

        return sum(result)

    @staticmethod
    def from_int(integer: int):
        """
        Turns any integer value into a Numeral object.
        :param integer: int to be changed.
        :return:
        """
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


class ZeroError(ValueError):
    pass


class NegativeError(ValueError):
    pass


class FractionError(ValueError):
    pass
