#!/usr/bin/env python

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>

"""
Functions dealing with zim notebooks
"""

import logging
import re
import os
import shutil
import glob
#import uuid



#our libs
from ZimArchivist import utils
#from ZimArchivist import archive
#from ZimArchivist import editline
from ZimArchivist import processtext
from ZimArchivist import timechecker

def get_zim_files(zim_root):
    """
    get the list of txt zim files
    """
    logging.info('Looking for zim files in ' + str(zim_root))
    zim_files = []
    for root, dirnames, filenames in os.walk(zim_root):
        #Do not inspect .Archive
        if '.Archive' in dirnames:
            dirnames.remove(".Archive")
        logging.debug('look in ' + str(root))
        for filename in glob.glob(os.path.join(root, '*.txt')):
            logging.debug('file ' + filename)
            
            zim_files.append(filename)
    if zim_files == []:
        logging.warning('No zim file found!')
    logging.debug('List of zim files')
    logging.debug(zim_files)
    return zim_files


import threading
from queue import Queue

class ThreadZimfiles(threading.Thread):
    """
    Process Zim files to create archives
    """
    def __init__(self, lock, zim_file_queue, zim_root, process_text_method, *args):
        """
        Constructor

        lock : lock from Threading
        zim_file_queue : Queue contraing zim files
        zim_root : filepath of the zim notebook root
        zim_archive_path : .Archive
        process_text_method : Function processing the text
        args : arguments for process_text_method
        """
        threading.Thread.__init__(self)
        self.lock = lock
        self.zim_file_queue = zim_file_queue
        self.zim_root = zim_root
        self.process_text_method = process_text_method
        self.args = args
    
    def run(self):
        """ Job: 
        Read the zim file
        Look for links
        Archive links when necessary
        """
        while True:
            zim_file = self.zim_file_queue.get()
            print(zim_file)
            #read
            with open(zim_file, 'r') as thefile:
                original_text = thefile.read()
            
            #process
            new_text = self.process_text_method(original_text, *self.args)
            
            #write
            with open(zim_file, 'w') as thefile:
                thefile.write(new_text)

            #Update time
            relativepath = zim_file.split(self.zim_root + '/')[1]
            with self.lock:
                timechecker.set_time(relativepath)

            #Done
            self.zim_file_queue.task_done()

def process_zim_file(zim_root, zim_files,  process_text_method, checktime, num_thread, *method_args):
    """
    Archive links in zim_files

    zim_root : filepath of the zim notebook root
    zim_files : 
    process_text_method : Function processing the text
    checktime : Check last modification time prior processing
    num_threads : number of threads
    method_args : arguments for process_text_method
    """

    file_queue = Queue()
    lock = threading.Lock()
    #Set up threads
    for thread in range(num_thread):
        worker = ThreadZimfiles(lock, file_queue, zim_root, process_text_method, *method_args)
        worker.setDaemon(True)
        worker.start()

    for thisfile in zim_files:
        thisfile_relativepath = thisfile.split(zim_root + '/')[1]
        #TODO need a lock here I guess...
        if timechecker.get_file_modif_status(zim_root, thisfile_relativepath) and checktime:
            #This zimfile has been updated, do it
            file_queue.put(thisfile)
        elif not checktime: 
            #We don't check time, do it
            file_queue.put(thisfile)
        else:
            #Nothing to do
            pass

    file_queue.join()

if __name__ == '__main__':
    pass



#def process_zim_file_old(zim_file, zim_archive_path):
#    """
#    Read the zim file
#    Look for links
#    Archive links when necessary
#    """
#    #read
#    thefile = open(zim_file, 'r')
#    original_text = thefile.read()
#    thefile.close()
#    
#    #process
#    new_text = processtext.process_text(original_text, zim_archive_path)
#    
#    #write
#    #TODO compare original and old file
#    thefile = open(zim_file, 'w')
#    thefile.write(new_text)
#    thefile.close()

