import unittest
import searcher


class SearcherTests(unittest.TestCase):

    def test_get_matches_list(self):
      self.assertEqual(searcher.get_matches_list('a', [' aa']), ['a', 'a'])
      self.assertEqual(searcher.get_matches_list('a', ['aba','a']), ['a', 'a', 'a'])

    def test_count_matches(self):
      self.assertEqual(searcher.count_matches('a', ['aa']), 2)
      self.assertEqual(searcher.count_matches('a', ['aa', 'a']), 3)

    def test_count_lines(self):
        self.assertEqual(searcher.count_lines('a', ['aa']), 1)
        self.assertEqual(searcher.count_lines('a', ['aa', 'a']), 2)

    def test_sort_matches(self):
        self.assertEqual(searcher.sort_matches('\w+@([\w.-_]+)',
                                               ['test@ytr.com test@mail.ru '
                                                'test@mail.ru'], 'abc'),
                         ['mail.ru', 'ytr.com'])
        self.assertEqual(searcher.sort_matches('\w+@([\w.-_]+)',
                                               ['test@ytr.com test@mail.ru '
                                                'test@mail.ru'], 'freq'),
                         ['ytr.com', 'mail.ru'])

if __name__ == '__main__':
    unittest.main()