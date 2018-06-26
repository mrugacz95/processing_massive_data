import os

import progressbar

from lab10.flajolet_martin import FlajoletMartin
from lab9.bloom_filter import BloomFilter

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
    k = 3
    bf = BloomFilter(k, size, 1000000)
    count = 0
    for song in read_data():
        if song not in bf:
            bf.add(song)
            count += 1
    # BloomCount distinct:  332122
    print('BloomCount distinct: ', count)

def bloom_count_aprox():
    size = 1000000
    k = 3
    bf = BloomFilter(k, size, 1000000)
    for song in read_data():
        if song not in bf:
            bf.add(song)
    print('BloomCountAprox distinct: ', bf.aprox_count())
    # BloomCountAprox distinct: 117840.45010593644


def flajolet_martin_count():
    fm = FlajoletMartin(2 ** 32, 4, 1)
    print('FlajoletMartin', fm.count(read_data()))
    # FlajoletMartin 294912.0


if __name__ == '__main__':
    simple_count()
    bloom_count()
    bloom_count_many_hash()
    bloom_count_aprox()
    flajolet_martin_count()
