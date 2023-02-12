from functools import reduce
import operator
import cmath
import math


class ComplexCircle:
    def __init__(self, n: int, theta0: float):
        self.n = n
        self.theta0 = theta0

    def get_z_list(self) -> list[complex]:
        """Returns the list of the 'n' complex number tha-t that represent the \
        'n' equal parts into which the circle is divided, rotated by the angle\
        'theta0'.
        """
        n, theta0 = self.n, self.theta0
        da = 2 * math.pi / n
        return [cmath.rect(1, a * da + theta0) for a in range(1, n + 1)]

    def complex_circle_product(self) -> complex:
        """Returns the product of the complex number sequence."""
        return reduce(operator.mul, self.get_z_list(), 1)

    def complex_circle_reduced_formula(self) -> complex:
        """Returns the product of the complex number sequence by computing \
        its reduced formula."""
        n, theta0 = self.n, self.theta0
        angle = n * (math.pi + theta0) + math.pi
        return cmath.rect(1, angle)
