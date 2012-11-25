#!/usr/bin/env python

import unittest 

from processtext import strip_noarchive
from processtext import _get_urls

class TestEditline(unittest.TestCase):

    #########################
    #Function strip_noarchive
    #########################
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

    def test_shorttag(self):
        text = """
Before
!@ blah blah
After
"""
        valid = """
Before

After
"""
        result = strip_noarchive(text)
        self.assertEqual(result, valid)


    #########################
    # _get_urls()
    #########################
    def test_simple_url(self):
        text = """
        http://www.fsf.org
        """
        result = _get_urls(text)
        valid = ['http://www.fsf.org']
        self.assertEqual(result, valid)

    def test_multiple_url(self):
        text = """
        http://www.fsf.org and http://www.april.org
        """
        result = _get_urls(text)
        valid = ['http://www.fsf.org', 'http://www.april.org']
        self.assertEqual(result, valid)

    @unittest.skip("Known bug")
    def test_url_with_parenthesis(self):
        text = """
        (http://www.fsf.org)
        """
        result = _get_urls(text)
        valid = ['http://www.fsf.org']
        self.assertEqual(result, valid)


if __name__ == '__main__':
    unittest.main()
