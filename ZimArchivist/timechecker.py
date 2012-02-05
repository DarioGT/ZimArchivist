#!/usr/bin/env python

import shelve
import os
import time


def set_time(filename):
    """
    Put the current time in the database for the filename
    """
    database = shelve.open(os.path.expanduser('~/.zimarchivist/time.db'))
    try:
        database[filename] = time.time()
    finally:
        database.close()


def get_file_modif_status(zimroot, filename):
    """ 
    Check if the file changed
    True: The file changed in the mean time
    False: ...
    """
    database = shelve.open(os.path.expanduser('~/.zimarchivist/time.db'))
    try:
        previous_time = database[filename]
    except KeyError:
        #We don't know...
        return True
    finally:
        database.close()

    if os.path.getmtime(os.path.join(zimroot, filename)) < previous_time:
        return False
    else:
        return True

if __name__ == '__main__':
    pass
