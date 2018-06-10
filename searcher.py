import re
import argparse

ERROR_END = 'Usage: searcher.py [OPTIONS] PATTERN [FILENAME] \n\n' \
            'Usage "searcher.py --help" for more information'
ERROR_FILE_EXPANSION = 'Error: FILENAME should ends with ".txt" \n' + ERROR_END
ERROR_NO_FILE = 'Error while opening "{0}": no such file \n' + ERROR_END
ERROR_FILE = 'Error while opening "{0}" \n' + ERROR_END
EMPTY_FILE_ERROR = 'Error: file "{0}" is empty'
HELP_INFO = """Usage: searcher.py [OPTIONS] PATTERN [FILENAME] \n
    Show a list of all matches of the regular expression PATTERN in the FILENAME

    PATTERN is a regular expression like '“\w+@[\w.-_]+”'
    FILENAME is a filename like 'example.txt'
    OPTIONS:
        -u                \tList unique matches only
        -c                \tGet total count of found matches
        -l                \tGet total count of lines, where at least one match
                                was found
        -s <sort_option>  \tSorting of found matches by alphabet or frequency
                                (related to all found matches).
                                Default sorting by alphabet
                                sort_option: 'abc' | 'freq'
        -o <order_option>  \tSpecify sorting order (ascending, descending).
                                Default order is ascending.
                                order_option: 'asc' | 'desc'
        -n                 \tList first N matches
        -stat <option>     \tList unique matches with statistic
                                (count or frequency in percents).
                                Default statistic is count.
                                option: 'count' | 'freq'
    """


def create_parser():
    """
    :return: an arguments parser
    """

    parser = argparse.ArgumentParser(conflict_handler='resolve')
    options = [
        ['-u', 'unique', 'store_true'],
        ['-c', 'count', 'store_true'],
        ['-l', 'count_lines', 'store_true'],
        ['-n', 'first_n', 'store'],
        ['-stat', 'statistic', 'store'],
        ['--help', 'help', 'store_true']
    ]
    for option, name, action in options:
        parser.add_argument(option, dest=name, action=action)

    options = [
        ['-s', 'sort', 'store', 'abc'],
        ['-o', 'order', 'store', 'asc']
    ]
    for option, name, action, const in options:
        parser.add_argument(option, dest=name, action=action,
                            const=const)

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

    sorted_statistic = []
    statistic_dict = get_statistic_dict(reg, file)
    total = count_matches(reg, file)
    if sort == 'abc':
        for k in sort_matches(reg, file, 'abc'):
            if output_format == 'count':
                sorted_statistic.append([k, statistic_dict[k]])
            elif output_format == 'freq':
                sorted_statistic.append([k, statistic_dict[k]/total])
    elif sort == 'freq':
        for k in sort_matches(reg, file, 'freq'):
            if output_format == 'count':
                sorted_statistic.append([k, statistic_dict[k]])
            elif output_format == 'freq':
                sorted_statistic.append([k, statistic_dict[k]/total])
    if ord == 'asc':
        return sorted_statistic
    elif ord == 'desc':
        sorted_statistic.reverse()
        return sorted_statistic


def show_stat(list, first_n):
    if first_n:
        for i in range(first_n):
            print(list[i])
    else:
        print(output)


def show_list(list, first_n):
    if first_n:
        for i in range(first_n):
            print(list[i])
    else:
        print(output)


def main(params):
    data = []
    output_list = []
    output_stat = []

    if params.help:  # Show help
        print(HELP_INFO)
        return

    if params.file and params.reg:
        filename = params.file[0]
        if not filename.endswith('.txt'):  # Check file expansion
            print(ERROR_FILE_EXPANSION)
            return
        try:
            with open(filename, 'r') as file:  # Fill data from file
                for line in file:
                    data.append(line)
        except FileNotFoundError:
            print(ERROR_NO_FILE.format(filename))
            return
        except IOError:
            print(ERROR_FILE.format(filename))
            return
        if not data:  # Check if data is empty
            print(EMPTY_FILE_ERROR.format(filename))
            return

        first_n = int(params.first_n) if params.first_n else 0
        if params.unique:
            matches_list = get_matches_list(params.reg[0], data)
            matches_list = set(matches_list)
            if params.count:
                print(len(matches_list))
            else:
                output_list = matches_list
        elif params.count:
            print(count_matches(params.reg[0], data))
        elif params.count_lines:
            print(count_lines(params.reg[0], data))
        elif params.sort:
            if params.sort == 'freq':
                output_list = sort_matches(params.reg[0], data, 'freq')
            elif params.sort == 'abc':
                output_list = sort_matches(params.reg[0], data, 'abc')
        elif params.statistic:
            if params.statistic == 'freq':
                output_stat = stat(params.reg[0], data, 'freq')
            elif params.statistic == 'count':
                output_stat = stat(params.reg[0], data, 'count')
        else:  # no options
            output_list = get_matches_list(params.reg[0], data)
        if output_list:
            show_list(output_list, first_n)
        if output_stat:
            show_list(output_stat, first_n)


if __name__ == '__main__':

    output = []
    parser = create_parser()
    params = parser.parse_args()
    print(params)
    main(params)


