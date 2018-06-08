import random
import numpy as np
from sympy import nextprime

from bitmap import Bitmap
import progressbar

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
    n = 10000
    num_range = 100000000
    factor = 10
    m = round(factor * n)
    k = 1
    bf = BloomFilter(k, m)
    full_set = set()

    for _ in range(n):
        num = random.randint(0, num_range)
        bf.add(num)
        full_set.add(num)
    tp = tn = fn = fp = 0
    bar = progressbar.ProgressBar()
    for key in bar(range(num_range)):
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
