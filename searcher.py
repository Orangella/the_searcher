import re
import argparse

ERROR_END = 'Usage: searcher.py [OPTIONS] PATTERN [FILENAME] \n\n' \
            'Usage "searcher.py --help" for more information'
ERROR_FILE_EXPANSION = 'Error: FILENAME should ends with ".txt" \n' + ERROR_END
ERROR_NO_FILE = 'Error while opening "{0}": no such file \n' + ERROR_END
ERROR_FILE = 'Error while opening "{0}" \n' + ERROR_END
EMPTY_FILE_ERROR = 'Error: file "{0}" is empty'
ERROR_FIRST_N_VALUE = 'Error: option "-n {0}" should be greater than zero'
MSG_NO_MATCHES = 'No matches of regular expression in the file'
MSG_UNKNOWN_ERROR = 'Sorry, an unknown error occured'


def create_parser():
    """
    :return: an arguments parser
    """

    parser = argparse.ArgumentParser(conflict_handler='resolve')
    options = [
        ['-u', 'unique', 'store_true',
         'List unique matches only'],

        ['-c', 'count', 'store_true',
         'Get total count of found matches'],

        ['-l', 'count_lines', 'store_true',
         """Get total count of lines, where at least one match was found"""]
    ]
    for option, name, action, help in options:
        parser.add_argument(option, dest=name, action=action, help=help)

    options = [
        ['-s', 'sort', 'store', ['abc', 'freq'],
         """Sorting of found matches by alphabet or frequency
         (related to all found matches). Default sorting is 'abc'
        """],

        ['-o', 'order', 'store', ['asc', 'desc'],
         """Specify sorting order (ascending, descending).
         Default order is 'asc'
        """],

        ['-stat', 'statistic', 'store', ['count', 'freq'],
         """List unique matches with statistic (count or frequency in percents).
         """]
    ]
    for option, name, action, choices, help in options:
        parser.add_argument(option, dest=name, action=action, choices=choices, help=help)

    parser.add_argument('-n', dest='first_n', action='store', type=int,
                        help='List first N matches')
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
    if not results:  # no matches
        raise NoMatchException()
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
    if not results:  # no matches
        raise NoMatchException()
    return results


def sort_matches(reg, file, sort='abc', unique=True):
    """
    :param reg: regular expression
    :param file: filename
    :param sort: sorting of found matches by frequency (sort='freq')
        or alphabet (sort='abc')
    :param unique: return array of nonrepeating matches
    :return: sorted list of matches
    """

    statistic_dict = get_statistic_dict(reg, file)
    sorted_unique_results = []
    if sort == 'freq':
        sorted_unique_results = sorted(statistic_dict.items(),
                                       key=lambda x: x[1])  # sorting by freq
        # get sorted list of matches
        sorted_unique_results = [x[0] for x in sorted_unique_results]
    if sort == 'abc':
        sorted_unique_results = sorted(statistic_dict.keys()) # sorting by abc
    if unique:
        return sorted_unique_results
    # if need to return all matches as many times as this match in the file
    else:
        sorted_all_results = []
        for res in sorted_unique_results:
            for i in range(statistic_dict[res]):
                sorted_all_results.append(res)
        return sorted_all_results


def stat(reg, file, output_format, sort):
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
    total = count_matches(reg, file)  # total count of all found matches
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

    return sorted_statistic


def show_stat(list, first_n, reverse):
    if reverse:
        list.reverse()
    if first_n:
        for i in range(first_n):
            print(list[i])
    else:
        for item in list:
            print(item)


def show_list(list, first_n, reverse):
    if reverse:
        list.reverse()
    if first_n:
        for i in range(first_n):
            print(list[i])
    else:
        for item in list:
            print(item)


class NoMatchException(Exception):
    pass


def main(params):
    data = []
    output_list = []
    output_stat = []
    reverse = True if params.order == 'desc' else False  # default order
    sort_option = 'freq' if params.sort == 'freq' else 'abc'  # default sort
    # check if first n in options for output
    first_n = int(params.first_n) if params.first_n else None
    if first_n and first_n <= 0:  # check if first n greater than zero
        print(ERROR_FIRST_N_VALUE.format(first_n))
        return

    filename = params.file[0]  # get filename
    reg = params.reg[0]  # get regular expression
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

    if params.unique:
        if params.count:  # if -u -c
            matches_list = get_matches_list(reg, data)
            matches_list = set(matches_list)
            print(len(matches_list))
            return
        else:  # if -u
            output_list = sort_matches(reg, data, sort=sort_option)
    elif params.count:  # if -c
        print(count_matches(reg, data))
        return
    elif params.count_lines:  # if -l
        print(count_lines(reg, data))
        return
    elif params.statistic:  # if -stat
        output_stat = stat(reg, data, params.statistic, sort_option)
    else:  # no options
        output_list = sort_matches(reg, data, sort_option, unique=False)

    if output_list:
        show_list(output_list, first_n, reverse)
    elif output_stat:
        show_stat(output_stat, first_n, reverse)


if __name__ == '__main__':

    output = []
    parser = create_parser()
    params = parser.parse_args()
    print(params)
    try:
        main(params)
    except NoMatchException:  # no match in file
        print(MSG_NO_MATCHES)
    except:  # hide all errors
        print(MSG_UNKNOWN_ERROR)


