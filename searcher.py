import re
import argparse
import unittest


def create_parser():
    # arguments parser
    parser = argparse.ArgumentParser()
    options = [
        ['-u', 'unique', 'store_true'],
        ['-c', 'count', 'store_true'],
        ['-l', 'count_lines', 'store_true'],
        ['-s', 'sort', 'store_const'],
        ['-o', 'order', 'store_const'],
        ['-n', 'first_n', 'store_const'],
        ['-stat', 'statistic', 'store_const']
    ]
    for option, name, action in options:
        parser.add_argument(option, dest= name, action=action, nargs='?')
    parser.add_argument('reg', nargs=1)
    parser.add_argument('file', nargs=1)

    return parser


if __name__ == '__main__':

    parser = create_parser()
    params = parser.parse_args()
    print(params)
    if params.file:
        with open(params.file[0], 'r') as file:
            for line in file:
                result = re.search(params.reg[0], line).group(0)
                print(result)