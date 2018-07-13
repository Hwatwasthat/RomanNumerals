import argparse
from classroman import Numeral


def main():
    args = parse()
    print(choose_method(args.arg1, args.arg2, args.operation))


def parse():
    parser = argparse.ArgumentParser(description="Taking in Integers or Strings, performs"
                                                 "an operation that returns Roman Numerals.")
    parser.add_argument("operation", help="Operation to be performed "
                                          "(add, sub, mul, div, pow, mod or convert), "
                                          "defaults to add. \nNote: if using convert,"
                                          " only 1 argument is required.",
                        nargs="?", default="add")
    parser.add_argument("arg1", help="First argument, int or str")
    parser.add_argument("arg2", help="Second argument, int or str", nargs="?")

    return parser.parse_args()

def choose_method(arg1, arg2, operation):
    operation = operation.lower()
    op_dict = {"add": Numeral.__add__,
               "sub": Numeral.__sub__,
               "mul": Numeral.__mul__,
               "div": Numeral.__truediv__,
               "pow": Numeral.__pow__,
               "mod": Numeral.__mod__,
               }
    try:
        arg1 = int(arg1)
    except ValueError:
        pass
    try:
        arg2 = int(arg2)
    except (ValueError, TypeError):
        pass
    operation = operation[:3]
    if operation == "con":
        try:
            arg1 = int(arg1)
            return Numeral(arg1)
        except ValueError:
            return Numeral(arg1).to_int()
    else:
        return op_dict[(operation).lower()](Numeral(arg1), Numeral(arg2))

if __name__ == "__main__":
    main()