import os
import random

import numpy as np
import progressbar
from sympy import nextprime

from bloom_filter import BloomFilter

DATA = os.path.join('data', 'facts.csv')


# bash
# tail -n +1 facts.csv | cut -d, -f1 | sort | uniq -c | wc
#  332124  664248 4944830

def read_data():
    size = os.path.getsize(DATA)
    with open(DATA, 'r') as file:
        next(file)
        current = 0
        with progressbar.ProgressBar(max_value=size) as pb:
            for line in file:
                yield int(line.split(',')[0])
                current += len(line)
                pb.update(current)


def simple_count():
    distinct = set()
    for song in read_data():
        if song not in distinct:
            distinct.add(song)
    # SimpleCount distinct:  332123
    print('SimpleCount distinct: ', len(distinct))


def bloom_count():
    size = 1000000
    k = 1
    bf = BloomFilter(k, size, 1000000)
    count = 0
    for song in read_data():
        if song not in bf:
            bf.add(song)
            count += 1
    print('BloomCount distinct: ', count)


def bloom_count_many_hash():
    size = 1000000
    k = 10
    bf = BloomFilter(k, size, 1000000)
    count = 0
    for song in read_data():
        if song not in bf:
            bf.add(song)
            count += 1
    # BloomCount distinct:  332122
    print('BloomCount distinct: ', count)


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


def flajolet_martin_count():
    fm = FlajoletMartin(2 ** 32, 5, 2)
    print('FlajoletMartin', fm.count(read_data()))
    # FlajoletMartin 262144


if __name__ == '__main__':
    simple_count()
    bloom_count()
    flajolet_martin_count()
