import random
import numpy as np
from sympy import nextprime


class BloomFilter:
    def __init__(self, k, size):
        self.k = k
        self.size = size
        self.p = nextprime(self.size)
        self.hash_functions = []
        for _ in range(k):
            self.hash_functions.append(self._random_hash_function())
        self.vector = np.zeros(self.size, dtype='i4')

    def _random_hash_function(self):
        a = random.randint(1, self.p - 1)
        b = random.randint(1, self.p - 1)
        return lambda x: ((a * x + b) % self.p) % self.size

    def add(self, item):
        for i in range(self.k):
            print(f'hash{i}(x)={self.hash_functions[i](item)}')
            self.vector[self.hash_functions[i](item)] = 1
        print(self.vector)

    def __contains__(self, item):
        print(self.vector)
        for i in range(self.k):
            print(f'hash{i}(x)={self.hash_functions[i](item)}')
            if self.vector[self.hash_functions[i](item)] == 0:
                return False
        return True


def main():
    # n = 10000
    # range = 100000000
    # factor = 10
    # size = round(factor * n)
    bf = BloomFilter(3, 11)
    # bf.add(7)
    bf.add(25)

    bf.add(70)
    print(70 in bf)
    print(7 in bf)
    print(25 in bf)
    print(5 in bf)


if __name__ == '__main__':
    main()
