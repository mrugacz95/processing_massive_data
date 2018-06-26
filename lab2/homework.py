import argparse
import random

import itertools
import numpy as np
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='days', type=int)
    parser.add_argument(dest='people', type=int)
    parser.add_argument(dest='go_to_hotel_prob', type=float)
    parser.add_argument(dest='hotels', type=int)
    args = parser.parse_args()
    print('days:', args.days, 'people:', args.people, 'prob:', args.go_to_hotel_prob, 'hotels: ', args.hotels)
    meet_data = np.zeros((args.people, args.people), dtype=np.uint32)
    for day in range(args.days):
        day_data = np.zeros((args.hotels, args.people), dtype=np.uint32)
        people_in_hotel = np.zeros((args.hotels,), dtype=np.uint32)
        # simulate hotel choose
        for p in range(args.people):
            if args.go_to_hotel_prob > random.random():
                selected_hotel = np.random.randint(args.hotels)
                day_data[selected_hotel,people_in_hotel[selected_hotel]] = p
                people_in_hotel[selected_hotel] += 1
        for h in range(args.hotels):
            hotel_data = day_data[h, :people_in_hotel[h]]
            for pair in itertools.permutations(hotel_data, 2):
                meet_data[pair] += 1
    print('How many time man x meet man y:', meet_data)

    suspected = np.sum(np.any(meet_data > 1, axis=1)) / 2
    print('Suspected people number:', suspected)

    meet_hist = meet_data[meet_data != 0]
    plt.hist(meet_hist)
    plt.show()
    hist = np.bincount(meet_hist)
    print('histogram:', hist)



if __name__ == '__main__':
    main()
