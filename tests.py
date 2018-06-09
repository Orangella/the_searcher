import unittest
import searcher


class SearcherTests(unittest.TestCase):

  def test_get_matches_list(self):
      self.assertEqual(searcher.get_matches_list('a', ['aa']), ['a'])
      self.assertEqual(searcher.get_matches_list('a', ['aa','a']), ['a', 'a'])

  def test_count_lines(self):
      self.assertEqual(searcher.count_lines('a', ['aa']), 1)
      self.assertEqual(searcher.count_lines('a', ['aa', 'a']), 2)


if __name__ == '__main__':
    unittest.main()