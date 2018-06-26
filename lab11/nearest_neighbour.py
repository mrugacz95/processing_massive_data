import os
from collections import defaultdict

import numpy as np
import progressbar

DATA = 'C:/Users/mruga/Documents/PMD/facts.csv'


def main():
    users = defaultdict(set)
    songs = defaultdict(set)
    first_100 = []
    first_100_set = set()

    def process_line(line):
        song_id, user_id, _ = map(int, line.split(','))
        users[user_id].add(song_id)
        songs[song_id].add(user_id)
        if len(first_100) < 100 and user_id not in first_100_set:
            first_100.append(user_id)
            first_100_set.add(user_id)

    with open(DATA, 'r') as file:
        size = os.path.getsize(DATA)
        current = 0
        next(file)
        pb = progressbar.ProgressBar(max_value=size)
        for idx, row in enumerate(file):
            process_line(row)
            current += len(row)
            if idx % 500000 == 0:
                pb.update(current)
    print("\nData read")
    with open('result.txt', 'w', encoding='utf8') as file:
        pb = progressbar.ProgressBar()
        for user in pb(first_100):
            file.write(f'User = {user}\n')
            others = set()
            for song in users[user]:
                others = others | set(songs[song])
            similarity = np.empty(len(others))
            for idx, other in enumerate(others):
                similarity[idx] = len(users[user] & users[other]) / len(users[user] | users[other])
            for sim, other in sorted(zip(similarity, others), reverse=True)[:100]:
                file.write(f'{str(other).rjust(7)} {sim:.3f}\n')


if __name__ == '__main__':
    main()
