def checkForNumber(numberString):
    newNumber = ""

    for c in numberString:
        if c.isdigit():
            newNumber += c

    return newNumber


def to_bool(string: str):
    return string.lower() == "true"
