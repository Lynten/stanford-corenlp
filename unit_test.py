import unittest
from stanfordcorenlp import StanfordCoreNLP


class MyTestCase(unittest.TestCase):
    def test_args(self):
        self.assertRaises(IOError, StanfordCoreNLP, '/abc')
        self.assertRaises(ValueError, StanfordCoreNLP, r'G:/JavaLibraries/stanford-corenlp-full-2016-10-31/',
                          lang='abc')
        self.assertRaises(ValueError, StanfordCoreNLP, r'G:/JavaLibraries/stanford-corenlp-full-2016-10-31/',
                          memory='4m')


if __name__ == '__main__':
    unittest.main()
