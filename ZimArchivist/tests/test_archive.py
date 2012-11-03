#!/usr/bin/env python

import unittest 
import tempfile
import os.path

from archive import get_archive_list
class TestGetArchiveList(unittest.TestCase):

    def test_one_file(self):
        path = tempfile.TemporaryDirectory()
        tmpfile = tempfile.NamedTemporaryFile(dir=path.name, delete=False)
        result = get_archive_list(path.name)
        valid = [os.path.basename(tmpfile.name)]
        self.assertEqual(result, valid)

    def test_one_dir_one_file(self):
        """ Only files must be returned"""
        path = tempfile.TemporaryDirectory()
        tmpfile = tempfile.NamedTemporaryFile(dir=path.name, delete=False)
        tmpdir = tempfile.TemporaryDirectory(dir=path.name)
        result = get_archive_list(path.name)
        valid = [os.path.basename(tmpfile.name)]
        self.assertEqual(result, valid)

from archive import get_unlinked_archive

class TestGetUnlinkedArchive(unittest.TestCase):

    def test_all_linked(self):
        text = """
        http://toto.org/link.html [[archive1.html|(Archive)]]
        http://toto.org/link2.html [[archive2.html|(Archive)]]
        
        """
        temp = tempfile.mkstemp()[1]
        with open(temp, 'w') as tmp:
            tmp.write(text)

        zim_files = [temp]
        zim_archives = ['archive1.html', 'archive2.html']
        valid = [] 
        result = get_unlinked_archive(zim_files, zim_archives) 
        self.assertEqual(result, valid)

    def test_all_missing(self):
        text = """
        
        """
        temp = tempfile.mkstemp()[1]
        with open(temp, 'w') as tmp:
            tmp.write(text)

        zim_files = [temp]
        zim_archives = ['archive1.html', 'archive2.html']
        valid =  ['archive1', 'archive2']
        result = get_unlinked_archive(zim_files, zim_archives) 
        self.assertEqual(result, valid)

    def test_mix(self):
        text = """
        http://toto.org/link.html [[archive1.html|(Archive)]]
        
        """
        temp = tempfile.mkstemp()[1]
        with open(temp, 'w') as tmp:
            tmp.write(text)

        zim_files = [temp]
        zim_archives = ['archive1.html', 'archive2.html']
        valid =  ['archive2']
        result = get_unlinked_archive(zim_files, zim_archives) 
        self.assertEqual(result, valid)

    def test_link_exists_twice(self):
        text = """
        http://toto.org/link.html [[archive1.html|(Archive)]]
        
        http://toto.org/link.html [[archive1.html|(Archive)]]
        """
        temp = tempfile.mkstemp()[1]
        with open(temp, 'w') as tmp:
            tmp.write(text)

        zim_files = [temp]
        zim_archives = ['archive1.html', 'archive2.html']
        valid =  ['archive2']
        result = get_unlinked_archive(zim_files, zim_archives) 
        self.assertEqual(result, valid)



if __name__ == '__main__':
    unittest.main()
