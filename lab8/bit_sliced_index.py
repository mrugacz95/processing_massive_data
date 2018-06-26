import numpy as np

from lab8.bitmap import Bitmap
from lab8.timing import timing


class BitSlicedIndex(object):
    def __init__(self, dtype):
        self.nbytes = np.dtype(dtype).itemsize * 8
        self.bitmaps = []
        for _ in range(self.nbytes):
            self.bitmaps.append(Bitmap(dtype))

    @timing
    def sum(self):
        mask = np.fromfunction(lambda x: 2**x, (self.nbytes,), dtype=np.uint32)
        ones = np.array([bitmap.sum() for idx, bitmap in enumerate(self.bitmaps)])
        return np.sum(mask * ones)

    def add(self, n):
        for i in range(self.nbytes):
            self.bitmaps[i].add(n >> i & 1)


@timing
def standard_sum(data):
    std_sum = 0
    for number in data:
        std_sum += number
    return std_sum


@timing
def python_sum(data):
    return sum(data)


@timing
def numpy_sum(data):
    return np.sum(data.astype(np.uint64))


def main():
    NUM = 10000
    dtype = np.uint16  # or np.uint8
    data = np.random.randint(0, np.iinfo(dtype).max, NUM, dtype=dtype)
    bsi = BitSlicedIndex(dtype)
    [bsi.add(x) for x in data]
    idx_sum = bsi.sum()
    np_sum = numpy_sum(data)
    p_sum = python_sum(data)
    std_sum = standard_sum(data)
    assert idx_sum == np_sum == p_sum == std_sum, f'Wrong sum {idx_sum} != {np_sum}'
    print('Ok')


if __name__ == '__main__':
    main()
