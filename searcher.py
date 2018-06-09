import re
import argparse


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
        result = re.findall(reg, line)
        results = results + result
    return results


def count_matches(reg, file):
    counter = 0
    for line in file:
        result = re.findall(reg, line)
        counter += len(result)
    return counter


def count_lines(reg, file):
    counter = 0
    for line in file:
        result = re.search(reg, line)
        if(result):
            counter += 1
    return counter


def get_statistic_dict(reg, file):
    results = {}
    for line in file:
        result = re.findall(reg, line)
        for item in result:
            if item in results:
                results[item] += 1
            else:
                results[item] = 1
    return results


def sort_matches(reg, file, freq_or_abc):
    statistic_dict = get_statistic_dict(reg, file)
    sorted_results = []
    if freq_or_abc == 'freq':
        sorted_results = sorted(statistic_dict.items(), key=lambda x: x[1])
        sorted_results = [x[0] for x in sorted_results]
    if freq_or_abc == 'abc':
        sorted_results = sorted(statistic_dict.keys())
    return sorted_results


def stat(reg, file, freq_or_abc):
    results = {}
    sorted_results = []
    for line in file:
        result = re.findall(reg, line)
        for item in result:
            if item in results:
                results[item] += 1
            else:
                results[item] = 1
    if freq_or_abc == 'freq':
        s = sorted(results.items(), key=lambda x: x[1])
        for k in sorted(results.items(), key=lambda x: x[1]):
            sorted_results.append([k[0], results[k[0]]])
    if freq_or_abc == 'abc':
        for k in sorted(results.keys()):
            sorted_results.append([k, results[k]])
    return sorted_results


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
                print(count_matches(params.reg[0], file))
            elif params.count_lines:
                print(count_lines(params.reg[0], file))
            elif params.sort:
                if params.sort == 'freq':
                    print(sort_matches(params.reg[0], file, 'freq'))
                elif params.sort == 'abc':
                    print(sort_matches(params.reg[0], file, 'abc'))
