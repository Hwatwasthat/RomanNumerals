NUMERALS = "MDCLXVI"

REPLACEMENTS = (
    ("IV", "IIII"),
    ("IX", "VIIII"),
    ("IL", "XXXXVIIII"),
    ("IC", "LXXXXVIIII"),
    ("ID", "CCCCLXXXXVIIII"),
    ("XL", "XXXX"),
    ("XC", "LXXXX"),
    ("XD", "CCCCLXXXX"),
    ("XM", "DCCCCLXXXX"),
    ("CD", "CCCC"),
    ("CM", "DCCCC"),
    ("IM", "DCCCCLXXXXVIIII"),
)


def sort_descending(unsorted):
    return "".join(sorted(unsorted, key=NUMERALS.index))


def add(arg1, arg2):
    return canonicalise(sort_descending(decanonicalise(arg1) + decanonicalise(arg2)))


def decanonicalise(num):

    while True:
        old = num
        for needle, replacement in REPLACEMENTS:
            num = num.replace(needle, replacement)
        if old == num:
            break
    return num


def canonicalise(num):

    num = num.replace("IIIII", "V")
    num = num.replace("VV", "X")
    num = num.replace("XXXXX", "L")
    num = num.replace("LL", "C")
    num = num.replace("CCCCC", "D")
    num = num.replace("DD", "M")

    while True:
        old = num
        for replacement, needle in reversed(REPLACEMENTS):
            num = num.replace(needle, replacement)
        if old == num:
            break
    return num


def demos():
    print_add("V", "IV")
    print_add("I", "IV")
    print_add("MIM", "I")
    print()
    print_subtract("M", "DC")
    print_subtract("C", "XIV")
    print_subtract("DIX", "XL")
    print()
    print_multiply("IX", "IX")
    print_multiply("X", "IX")
    print_multiply("III", "IV")
    print()
    print_divide("IX", "V")
    print_divide("X", "V")
    print_divide("XI", "V")
    print()
    print_power("V", "II")
    print_power("X", "III")
    print_power("IX", "III")


def decrement(arg1):
    num = decanonicalise(arg1)
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

    return canonicalise(num)


class ZeroError(ValueError):
    pass


class NegativeError(ValueError):
    pass


def subtract(arg1, arg2):

    while arg1 and arg2:
        arg1 = decrement(arg1)
        arg2 = decrement(arg2)

    if arg2:
        raise NegativeError("absurd impossibility detected (numbers cannot be below zero!)")

    if not arg1:
        raise ZeroError("or zero for that matter")

    return arg1


def multiply(arg1, arg2):
    total = ""
    while arg2:
        total = add(total, arg1)
        arg2 = decrement(arg2)

    return total


def divide(arg1, arg2):
    count = ""
    while True:
        try:
            arg1 = subtract(arg1, arg2)
            count = add(count, "I")
        except NegativeError:
            return count, arg1
        except ZeroError:
            return add(count, "I"), ""


def power(arg1, arg2):
    total = "I"
    while arg2:
        total = multiply(total, arg1)
        arg2 = decrement(arg2)

    return total


def print_add(arg1, arg2):
    print(arg1, "+", arg2, "=", add(arg1, arg2))
    assert(add(arg1, arg2) == add(arg2, arg1))


def print_subtract(arg1, arg2):
    print(arg1, "-", arg2, "=", subtract(arg1, arg2))


def print_multiply(arg1, arg2):
    print(arg1, "\u00d7", arg2, "=", multiply(arg1, arg2))
    assert(multiply(arg1, arg2) == multiply(arg2, arg1))


def print_divide(arg1, arg2):
    print(arg1, "\u00f7", arg2, "=", divide(arg1, arg2))


def print_power(arg1, arg2):
    print(arg1, "\u2191", arg2, "=", power(arg1, arg2))


demos()
