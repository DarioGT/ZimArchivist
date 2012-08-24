#!/usr/bin/env python


import unittest

from timechecker import set_time
from timechecker import get_file_modif_status

class TestZimarchive(unittest.TestCase):

    def test_modified(self):
        try:
            os.remove('/tmp/testfile')
        except:
            pass
        set_time('testfile')
        test = open('/tmp/testfile', 'w')
        test.close()
        status = get_file_modif_status('/tmp', 'testfile')
        self.assertTrue(status)

    def test_not_modified(self):
        test = open('/tmp/testfile', 'w')
        test.close()
        set_time('testfile')
        status = get_file_modif_status('/tmp', 'testfile')
        self.assertFalse(status)

if __name__ == '__main__':
    unittest.main()

