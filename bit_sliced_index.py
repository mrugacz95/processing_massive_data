import random

import numpy as np


class BitSlicedIndex(object):
    DTYPE = np.uint8
    nbytes = np.dtype(DTYPE).itemsize * 8
    num_sets_bits = None

    def __init__(self):
        if self.num_sets_bits is None:
            BitSlicedIndex._init_num_set_bits()
        self.data = np.zeros(1, dtype=np.uint8)
        self.count = 0

    def add(self, bit):
        if self.count / 8 >= len(self.data):
            self.data.resize(len(self.data) * 2)
        item = self.count // 8
        pos = self.count % 8
        self.data[item] |= bit << pos
        self.count += 1

    def print(self):
        for item in self.data:
            for pos in range(self.nbytes):
                print((item & 1 << pos) >> pos, end='')
            print()

    def sum(self):
        return np.sum([BitSlicedIndex.num_sets_bits[byte] for byte in self.data])

    @staticmethod
    def count_ones(n):
        count = 0
        while n != 0:
            n &= (n - 1)
            count += 1
        return count

    @staticmethod
    def _init_num_set_bits():
        BitSlicedIndex.num_sets_bits = np.zeros(2 ** BitSlicedIndex.nbytes, dtype=np.uint8)
        for i in range(2 ** BitSlicedIndex.nbytes):
            BitSlicedIndex.num_sets_bits[i] = BitSlicedIndex.count_ones(i)


if __name__ == '__main__':
    bi = BitSlicedIndex()
    count = 0
    for i in range(200):
        bit = random.randint(0, 1)
        count += bit
        bi.add(bit)
    bit_count = bi.sum()
    assert bit_count == count, f'Not equal: {bit_count} != {count}'
    print('Ok')
