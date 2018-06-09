import re
import argparse


def create_parser():
    """
    :return: an arguments parser
    """

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
    """
    :param reg: regular expression
    :param file: filename
    :return: a list of all matches of the regular expression in the file
    """

    results = []
    for line in file:
        result = re.findall(reg, line)
        results = results + result
    return results


def count_matches(reg, file):
    """
    :param reg: regular expression
    :param file: filename
    :return: total count of all matches of the regular expression in the file
    """

    counter = 0
    for line in file:
        result = re.findall(reg, line)
        counter += len(result)
    return counter


def count_lines(reg, file):
    """
    :param reg: regular expression
    :param file: filename
    :return: total count of lines, where at least one match was found
    """

    counter = 0
    for line in file:
        result = re.search(reg, line)
        if(result):
            counter += 1
    return counter


def get_statistic_dict(reg, file):
    """
    :param reg: regular expression
    :param file: filename
    :return: dict with
        keys: match of the regular expression in the file;
        values: total count of this match
    """

    results = {}
    for line in file:
        result = re.findall(reg, line)
        for item in result:
            if item in results:
                results[item] += 1
            else:
                results[item] = 1
    return results


def sort_matches(reg, file, sort='abc'):
    """
    :param reg: regular expression
    :param file: filename
    :param sort: sorting of found matches by frequency (sort='freq')
        or alphabet (sort='abc')
    :return: sorted list of matches
    """
    
    statistic_dict = get_statistic_dict(reg, file)
    sorted_results = []
    if sort == 'freq':
        sorted_results = sorted(statistic_dict.items(), key=lambda x: x[1])
        sorted_results = [x[0] for x in sorted_results]
    if sort == 'abc':
        sorted_results = sorted(statistic_dict.keys())
    return sorted_results


def stat(reg, file, output_format, sort='abc', ord='asc'):
    """
    :param reg: regular expression
    :param file: filename
    :param output_format: output count of matches (output_format='count')
        or frequency in percents (output_format='freq')
    :param sort: sorting of found matches by frequency (sort='freq')
        or alphabet (sort='abc')
    :param ord: sorting of found matches by ascending (ord='asc')
        or descending (ord='desc') order
    :return: sorted statistic list
    """

    output = []
    statistic_dict = get_statistic_dict(reg, file)
    total = count_matches(reg, file)
    if sort == 'abc':
        for k in sort_matches(reg, file, 'abc'):
            if output_format == 'count':
                output.append([k, statistic_dict[k]])
            elif output_format == 'freq':
                output.append([k, statistic_dict[k]/total])
    elif sort == 'freq':
        for k in sort_matches(reg, file, 'freq'):
            if output_format == 'count':
                output.append([k, statistic_dict[k]])
            elif output_format == 'freq':
                output.append([k, statistic_dict[k]/total])
    if ord == 'asc':
        return output
    elif ord == 'desc':
        output.reverse()
        return output


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
            elif params.statistic:
                if params.statistic == 'freq':
                    print(stat(params.reg[0], file, 'freq'))
                elif params.statistic == 'count':
                    print(stat(params.reg[0], file, 'count'))
