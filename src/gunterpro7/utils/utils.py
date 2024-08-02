def checkForNumber(numberString):
    newNumber = ""

    for c in numberString:
        if c.isdigit():
            newNumber += c

    return newNumber


def to_bool(string: str):
    return string.lower() == "true"


def to_int(string: str):
    number_string: str = ""

    for c in string:
        if c.isdigit():
            number_string += c

    return int(number_string)
