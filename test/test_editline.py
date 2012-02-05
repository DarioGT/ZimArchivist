#!/usr/bin/env python

import unittest 

from editline import link_archive_status
from editline import add_label
from editline import extract_labels_filepath

class TestEditline(unittest.TestCase):

    #Function link_archive_status
    def test_link_archive_status_OK(self):
        url = 'http://www.toto.org'
        line = 'A nice line with http://www.toto.org [[/a/great/path/file.html|(Archive)]]'
        result = link_archive_status(url, line)
        self.assertTrue(result)

    def test_link_archive_status_NO(self):
        url = 'http://www.toto.org'
        line = 'A nice line with http://www.toto.org Another info'
        result = link_archive_status(url, line)
        self.assertFalse(result)

    #Function add_label
    def test_simple_url(self):
        result = add_label('toto.html', 'http://www.google.fr', 'Link : http://www.google.fr a Comment')
        self.assertEqual(result, 'Link : http://www.google.fr [[toto.html|(Archive)]] a Comment')

    def test_simple_url_in_parenthesis(self):
        result = add_label('toto.html', 'http://wiki.april.org/w/PlanetApril', 'Link : (http://wiki.april.org/w/PlanetApril) a Comment')
        self.assertEqual(result, 'Link : (http://wiki.april.org/w/PlanetApril [[toto.html|(Archive)]]) a Comment')

    def test_url_with_accent(self):
        result = add_label('toto.html', 'http://fr.wikipedia.org/wiki/Éléphant', 'http://fr.wikipedia.org/wiki/Éléphant')
        self.assertEqual(result, 'http://fr.wikipedia.org/wiki/Éléphant [[toto.html|(Archive)]]')

    def test_autre(self):
        result = add_label('toto.html', 'https://encrypted.google.com/webhp?hl=fr', 'https://encrypted.google.com/webhp?hl=fr')
        self.assertEqual(result, 'https://encrypted.google.com/webhp?hl=fr [[toto.html|(Archive)]]')


    def test_special_caracters(self):
        link = 'http://www.python-forum.org/pythonforum/viewforum.php?f=17&sid=96a6f6cdd10e9b11c3a40a1664d6f2aa'
        result = add_label('toto.html', link, link)
        print(result)
        self.assertEqual(result, link + ' [[toto.html|(Archive)]]')

    #Function extract_labels_filepath
    def test_extraction_simple(self):
        line = 'This is a line http://www.foo.org [[~/Notes/.Archive/aa.html|(Archive)]]' 
        result = extract_labels_filepath(line)
        self.assertEqual(result, ['~/Notes/.Archive/aa.html'])
    def test_extraction(self):
        line = 'This is a line http://www.foo.org [[~/Notes/.Archive/aa.html|(Archive)]] and http://www.bar.org [[~/Notes/.Archive/bb.html|(Archive)]] and so on'
        result = extract_labels_filepath(line)
        self.assertEqual(result, ['~/Notes/.Archive/aa.html', '~/Notes/.Archive/bb.html'])
        
        
        

if __name__ == '__main__':
    unittest.main()

