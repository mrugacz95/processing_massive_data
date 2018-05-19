import random

import numpy as np

from timing import timing


class Bitmap(object):
    num_sets_bits = None
    nbytes = None

    def __init__(self, dtype, size=8):
        if self.num_sets_bits is None:
            Bitmap.dtype = dtype
            Bitmap.nbytes = np.dtype(dtype).itemsize * 8
            Bitmap._init_num_set_bits()
        self.data = np.zeros(np.ceil(size / 8).astype(int), dtype=Bitmap.dtype)
        self.count = 0

    def add(self, bit):
        if self.count / self.nbytes >= len(self.data):
            self.resize(len(self.data) * 2)
        self.set(self.count, bit)
        self.count += 1

    def get(self, n):
        if n >= len(self.data) * 8:
            self.resize(np.ceil(n / 8 + 1).astype(int))
        item = n // self.nbytes
        pos = n % self.nbytes
        return self.data[item] >> pos & 1

    def set(self, n, val):
        if n >= len(self.data) * 8:
            self.resize(np.ceil(n / 8 + 1).astype(int))
        item = n // self.nbytes
        pos = n % self.nbytes
        if val == 0:
            self.data[item] &= ~(1 << pos)
        else:
            self.data[item] |= 1 << pos

    def resize(self, new_size):
        self.data.resize(new_size)

    def print(self):
        for item in self.data:
            for pos in range(Bitmap.nbytes):
                print((item >> pos & 1), end='')
            print()

    def sum(self):
        return np.sum([Bitmap.num_sets_bits[byte] for byte in self.data])

    @staticmethod
    def count_ones(n):
        count = 0
        while n != 0:
            n &= (n - 1)
            count += 1
        return count

    @staticmethod
    def _init_num_set_bits():
        Bitmap.num_sets_bits = np.zeros(2 ** Bitmap.nbytes, dtype=np.uint8)
        for i in range(2 ** Bitmap.nbytes):
            Bitmap.num_sets_bits[i] = Bitmap.count_ones(i)


if __name__ == '__main__':
    bi = Bitmap(np.uint16)
    for i in range(5):
        bi.add(1)
    count = 5
    for i in range(20):
        bit = random.randint(0, 1)
        count += bit
        bi.add(bit)
    bi.print()
    bit_count = bi.sum()
    assert bit_count == count, f'Not equal: {bit_count} != {count}'
    for i in range(5):
        assert bi.get(i) == 1, f'Bit not set'
    print('Ok')
