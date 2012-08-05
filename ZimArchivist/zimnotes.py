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

def get_zim_files(zim_root):
    """
    get the list of txt zim files
    """
    logging.info('Looking for zim files in ' + str(zim_root))
    zim_files = []
    for root, dirnames, filenames in os.walk(zim_root):
        logging.debug('look in ' + str(root))
        for filename in glob.glob(os.path.join(root, '*.txt')):
            logging.debug('file ' + filename)
            
            zim_files.append(filename)
    if zim_files == []:
        logging.warning('No zim file found!')
    logging.debug('List of zim files')
    logging.debug(zim_files)
    return zim_files

def process_zim_file(zim_file, zim_archive_path):
    """
    Read the zim file
    Look for links
    Archive links when necessary
    """
    #read
    thefile = open(zim_file, 'r')
    original_text = thefile.read()
    thefile.close()
    
    #process
    new_text = processtext.process_text(original_text, zim_archive_path)
    
    #write
    #TODO compare original and old file
    thefile = open(zim_file, 'w')
    thefile.write(new_text)
    thefile.close()
    
    
if __name__ == '__main__':
    #TODO doctest
    pass
