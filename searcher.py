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
        ['-s', 'sort', 'store'],
        ['-o', 'order', 'store'],
        ['-n', 'first_n', 'store'],
        ['-stat', 'statistic', 'store']
    ]
    for option, name, action in options:
        parser.add_argument(option, dest=name, action=action)

    parser.add_argument('reg', nargs=1)
    parser.add_argument('file', nargs=1)

    return parser


def get_matches_list(reg, file):
    results = []
    for line in file:
        result = re.search(reg, line).group(0)
        results.append(result)
    return results


if __name__ == '__main__':

    parser = create_parser()
    params = parser.parse_args()
    print(params)
    if params.file:
        with open(params.file[0], 'r') as file:
            if params.unique:
                results = get_matches_list(params.reg[0], file)
                results = set(results)
                if params.count:
                    print(len(results))
                else:
                    print(results)
            elif params.count:
                results = get_matches_list(params.reg[0], file)
                print(len(results))
