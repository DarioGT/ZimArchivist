#!/usr/bin/env python

import unittest 

from utils import protect

class TestZimarchive(unittest.TestCase):

    def test_protect_question(self):
        result = protect('?text&text')
        self.assertEqual(result, '\?text\&text')


if __name__ == '__main__':
    unittest.main()

