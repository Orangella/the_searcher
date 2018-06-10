import unittest
import searcher


class SearcherTests(unittest.TestCase):

    def test_get_matches_list(self):
      self.assertEqual(searcher.get_matches_list('a', [' aa']), ['a', 'a'])
      self.assertEqual(searcher.get_matches_list('a', ['aba','a']),
                       ['a', 'a', 'a'])

    def test_count_matches(self):
      self.assertEqual(searcher.count_matches('a', ['aa']), 2)
      self.assertEqual(searcher.count_matches('a', ['aa', 'a']), 3)

    def test_count_lines(self):
        self.assertEqual(searcher.count_lines('a', ['aa']), 1)
        self.assertEqual(searcher.count_lines('a', ['aa', 'a']), 2)

    def test_sort_matches(self):
        test_re = '\w+@([\w.-_]+)'
        test_arr = ['test@ytr.com test@mail.ru test@mail.ru test@mail.ru']
        self.assertEqual(searcher.sort_matches(test_re, test_arr, 'abc'),
                         ['mail.ru', 'ytr.com'])
        self.assertEqual(searcher.sort_matches(test_re, test_arr, 'freq'),
                         ['ytr.com', 'mail.ru'])
        self.assertEqual(searcher.sort_matches(test_re, test_arr, 'abc',
                                               unique=False),
                         ['mail.ru', 'mail.ru', 'mail.ru', 'ytr.com'])
        self.assertEqual(searcher.sort_matches(test_re, test_arr, 'freq',
                                               unique=False),
                         ['ytr.com', 'mail.ru', 'mail.ru', 'mail.ru'])

    def test_stat(self):
        test_re = '\w+@([\w.-_]+)'
        test_arr = ['test@ytr.com test@mail.ru test@mail.ru test@mail.ru']
        self.assertEqual(searcher.stat(test_re, test_arr, 'count',
                                       sort='abc', ord='asc'),
                         [['mail.ru', 3], ['ytr.com', 1]])
        self.assertEqual(searcher.stat(test_re, test_arr, 'freq',
                                       sort='abc', ord='asc'),
                         [['mail.ru', 0.75], ['ytr.com', 0.25]])
        self.assertEqual(searcher.stat(test_re, test_arr, 'count',
                                       sort='freq', ord='asc'),
                         [['ytr.com', 1], ['mail.ru', 3]])
        self.assertEqual(searcher.stat(test_re, test_arr, 'freq',
                                       sort='freq', ord='asc'),
                         [['ytr.com', 0.25], ['mail.ru', 0.75]])
        self.assertEqual(searcher.stat(test_re, test_arr, 'count',
                                       sort='abc', ord='desc'),
                         [['ytr.com', 1], ['mail.ru', 3]])
        self.assertEqual(searcher.stat(test_re, test_arr, 'freq',
                                       sort='abc', ord='desc'),
                         [['ytr.com', 0.25], ['mail.ru', 0.75]])
        self.assertEqual(searcher.stat(test_re, test_arr, 'count',
                                       sort='freq', ord='desc'),
                         [['mail.ru', 3], ['ytr.com', 1]])
        self.assertEqual(searcher.stat(test_re, test_arr, 'freq',
                                       sort='freq', ord='desc'),
                         [['mail.ru', 0.75], ['ytr.com', 0.25]])

if __name__ == '__main__':
    unittest.main()