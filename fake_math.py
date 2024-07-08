from math import inf
def divide (a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return inf
