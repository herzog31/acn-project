'''
Created on 10.12.2014

Created for generating pseudo measurement values. Intended for testing only!
'''

import argparse
import random


def create_values(size, mean, std_dev):
    random.seed()
    values = []
    i = 0

    while i < size:
        values.append(random.normalvariate(mean, std_dev))
        i = i+1

    return values


def write_to_file(values, filename):
    file = open(filename, 'w')

    if values is None or not values:
        file.write("")
    else:
        for value in values:
            file.write("{0}\n".format(value))

    file.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--size",
        help="Number of random values (int, DEFAULT=100)",
        type=int,
        default=100)
    parser.add_argument(
        "--output",
        help="Output file (DEFAULT=output.txt)",
        type=str,
        default="output.txt")
    parser.add_argument(
        "--mean",
        help="Mean value (float, DEFAULT=100.0)",
        type=float,
        default=100.0)
    parser.add_argument(
        "--std_dev",
        help="Standard deviation (float, DEFAULT=10.0)",
        type=float,
        default=10.0)

    args = parser.parse_args()

    values = create_values(args.size, args.mean, args.std_dev)
    write_to_file(values, args.output)

if __name__ == '__main__':
    main()
