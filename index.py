import numpy as np
import time


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms result is %d' % (f.__name__, (time2 - time1) * 1000.0, ret))
        return ret

    return wrap


num_sets_bits = np.zeros(256, dtype=np.uint8)


def count_ones(n):
    count = 0
    while n != 0:
        n &= (n - 1)
        count += 1
    return count


def init_num_set_bits():
    for i in range(256):
        num_sets_bits[i] = count_ones(i)


@timing
def bit_sliced_index(index, dtype):

    nbytes = np.dtype(dtype).itemsize * 8
    def sum_ones(index):
        ones = np.zeros(nbytes, dtype=np.uint64)
        for idx, bitmap in enumerate(index):
            ones[idx] = np.sum([num_sets_bits[number] for number in bitmap])
        return ones

    ones = sum_ones(index)
    # ones = data.sum(axis=1)
    idx_sum = 0
    multiplier = 1 << (nbytes - 1)
    for idx, sum_of_ones in enumerate(ones):
        idx_sum += sum_of_ones * multiplier
        multiplier >>= 1
    return idx_sum


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
    # np.random.seed(1)
    NUM = 800  # muliple of 8 number
    DTYPE = np.uint8
    init_num_set_bits()
    data = np.random.randint(0, np.iinfo(DTYPE).max, NUM, dtype=DTYPE)
    # data = np.full(NUM, np.iinfo(DTYPE).max, dtype=np.uint8).reshape(NUM)


    nbytes = np.dtype(DTYPE).itemsize * 8
    index = np.unpackbits(data)
    index = np.reshape(index, (len(data), nbytes)).transpose()
    index = np.packbits(index, axis=1)
    idx_sum = bit_sliced_index(index, DTYPE)
    np_sum = numpy_sum(data)
    p_sum = python_sum(data)
    std_sum = standard_sum(data)
    assert idx_sum == np_sum, f'Wrong sum {idx_sum} != {np_sum}'
    print('Ok')

if __name__ == '__main__':
    main()
