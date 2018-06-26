import random

import numpy as np
from sympy import nextprime


class FlajoletMartin(object):
    def __init__(self, size, k, l):
        self.l = l
        self.k = k
        self.size = size
        self.p = nextprime(self.size)

    def _random_hash_function(self):
        a = random.randint(1, self.p - 1)
        b = random.randint(1, self.p - 1)
        return lambda x: ((a * x + b) % self.p) % self.size

    def count(self, iterable):
        hash_functions = [[self._random_hash_function() for _ in range(self.l)] for _ in range(self.k)]
        max_zeros = np.zeros((self.k, self.l))
        for item in iterable:
            for i, group in enumerate(hash_functions):
                for j, fun in enumerate(group):
                    max_zeros[i, j] = max(self.count_trailing_zero(hash_functions[i][j](item)), max_zeros[i, j])
        max_zeros = 2 ** max_zeros
        return np.average(np.median(max_zeros, axis=1))

    def count_trailing_zero(self, num):
        num = bin(num)
        return len(num) - len(num.rstrip('0'))