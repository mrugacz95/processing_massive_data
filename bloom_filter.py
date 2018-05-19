import random
import numpy as np
from sympy import nextprime

from bitmap import Bitmap


class BloomFilter:
    DEBUG = False

    def __init__(self, k, size):
        self.k = k
        self.size = size
        self.p = nextprime(self.size)
        self.hash_functions = []
        for _ in range(k):
            self.hash_functions.append(self._random_hash_function())
        self.bitmap = Bitmap(np.uint8)

    def _random_hash_function(self):
        a = random.randint(1, self.p - 1)
        b = random.randint(1, self.p - 1)
        return lambda x: ((a * x + b) % self.p) % self.size

    def add(self, item):
        for i in range(self.k):
            if BloomFilter.DEBUG:
                print(f'hash{i}(x)={self.hash_functions[i](item)}')
            self.bitmap.set(self.hash_functions[i](item), 1)
        if BloomFilter.DEBUG:
            self.bitmap.print()

    def __contains__(self, item):
        if BloomFilter.DEBUG:
            self.bitmap.print()
        for i in range(self.k):
            if BloomFilter.DEBUG:
                print(f'hash{i}(x)={self.hash_functions[i](item)}')
            if self.bitmap.get(self.hash_functions[i](item)) == 0:
                return False
        return True


def main():
    # n = 10000
    n = 1000
    # num_range = 100000000
    num_range = 100000
    # factor = 10
    p = 0.1
    # m = round(factor * n)
    m = np.ceil(-n * np.log(p) / (np.log(2) ** 2)).astype(int)
    k = np.ceil(m / n * np.log(2)).astype(int)
    bf = BloomFilter(k, m)
    full_set = set()

    for _ in range(n):
        num = random.randint(0, num_range)
        bf.add(num)
        full_set.add(num)
    tp = tn = fn = fp = 0
    for key in range(num_range + 1):
        # key = random.randint(1,num_range)
        containsBF = key in bf
        containsHS = key in full_set
        if containsBF and containsHS:
            tp += 1
        elif not containsBF and not containsHS:
            tn += 1
        elif (not containsBF) and containsHS:
            fn += 1
        elif containsBF and (not containsHS):
            fp += 1
    print(f'TP: {tp}')
    print(f'TN: {tn}')
    print(f'FN: {fn}')
    print(f'FP: {fp}')


if __name__ == '__main__':
    main()
