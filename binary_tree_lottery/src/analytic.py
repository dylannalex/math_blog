import math as _math


def f(h: int, k: int):
    numerator = 0
    i_start = _math.ceil(_math.log2(k))
    for i in range(i_start, h + 1):
        numerator += _math.perm(2**i, k)
    denominator = _math.perm(2 ** (h + 1) - 1, k)
    return numerator / denominator
