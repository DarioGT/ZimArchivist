#!/usr/bin/env python

import unittest 

from processtext import strip_noarchive

class TestEditline(unittest.TestCase):

    #Function strip_noarchive
    def test_oneline(self):
        text = "keep me {noarchive} erase me {/noarchive} keep me"
        valid = "keep me  keep me"
        result = strip_noarchive(text) 
        self.assertEqual(result, valid)

    def test_multiline(self):
        text = """
keep me
{noarchive}
erase me
{/noarchive}
keep me again
        """
        valid = """
keep me

keep me again
        """
        result = strip_noarchive(text) 
        self.assertEqual(result, valid)




if __name__ == '__main__':
    unittest.main()
