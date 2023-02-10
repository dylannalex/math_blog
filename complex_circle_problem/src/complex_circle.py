from functools import reduce
import operator
import cmath
import math


def get_z_list(n: int, theta0: float) -> list[complex]:
    """Returns the list of the 'n' complex number tha-t that represent the \
    'n' equal parts into which the circle is divided, rotated by the angle\
    'theta0'.
    """
    da = 2 * math.pi / n
    return [cmath.rect(1, a * da + theta0) for a in range(1, n + 1)]


def complex_circle_product(z_list: list[complex]) -> complex:
    """Returns the product of the complex number sequence."""
    return reduce(operator.mul, z_list, 1)


def complex_circle_reduced_formula(n: int, theta0: float) -> complex:
    """Returns the product of the complex number sequence by computing \
    its reduced formula."""
    angle = n * (math.pi + theta0) + math.pi
    return cmath.rect(1, angle)
