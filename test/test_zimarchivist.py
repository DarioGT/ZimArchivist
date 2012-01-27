#!/usr/bin/env python


import unittest 

from zimarchivist import make_archive
from zimarchivist import protect
from zimarchivist import link_archive_status


class TestZimarchive(unittest.TestCase):
    
    def test_simple_url(self):
        result = make_archive('toto.html', 'http://www.google.fr', 'Link : http://www.google.fr a Comment')
        self.assertEqual(result, 'Link : http://www.google.fr [[toto.html|Archive]] a Comment')

    def test_autre(self):
        result = make_archive('toto.html', 'https://encrypted.google.com/webhp?hl=fr', 'https://encrypted.google.com/webhp?hl=fr')
        self.assertEqual(result, 'https://encrypted.google.com/webhp?hl=fr [[toto.html|Archive]]')


    def test_special_caracters(self):
        link = 'http://www.python-forum.org/pythonforum/viewforum.php?f=17&sid=96a6f6cdd10e9b11c3a40a1664d6f2aa'
        result = make_archive('toto.html', link, link)
        print(result)
        self.assertEqual(result, link + ' [[toto.html|Archive]]')

    def test_protect_question(self):
        result = protect('?text&text')
        self.assertEqual(result, '\?text\&text')


    def test_link_archive_status_OK(self):
        url = 'http://www.toto.org'
        line = 'A nice line with http://www.toto.org [[/a/great/path/file.html|Archive]]'
        result = link_archive_status(url, line)
        self.assertTrue(result)

    def test_link_archive_status_NO(self):
        url = 'http://www.toto.org'
        line = 'A nice line with http://www.toto.org Another info'
        result = link_archive_status(url, line)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()

