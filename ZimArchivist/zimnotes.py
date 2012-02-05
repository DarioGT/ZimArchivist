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
import uuid



#our libs
from ZimArchivist import utils
from ZimArchivist import archive

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

def add_label(html_path, url, line):
    """
    Add the label "Archive" to the archive after the url in the line 
    Return the line
    """
    new_url = url + " [[" + utils.get_unexpanded_path(html_path) + "|(Archive)]]"
    url = utils.protect(url)
    line = re.sub(url, new_url, line)
    return line

def link_archive_status(url, line):
    """ 
    Is the url in the line already archived?
    Basically, it checks if [[path|(Archive)]] follows the url
    False: Not archived 
    True: Archived
    """
    logging.debug('line= ' + str(line))
    link_archived = re.compile(str(url) + '\s\[\[.*\|\(Archive\)\]\]')
    matching = link_archived.search(line)
    if matching == None:
        return False
    else:
        return True

def extract_labels_filepath(line):
    filepaths = []
    #First, we detect labels
    re_archive = re.compile('\s\[\[(.+)\|\(Archive\)\]\]')
    labels = re.findall('\s\[\[(.+?)\|\(Archive\)\]\]',line) #? is for non-greedy (minimal) fashion
    for label in labels:
        filepaths.append(label)
    return filepaths

def process_zim_file(zim_file, zim_archive_path):
    """
    Read the zim file
    Look for links
    Archive links when necessary
    """
    link = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    begin_noarchive = re.compile('\{noarchive\}')
    end_noarchive = re.compile('\{\/noarchive\}')


    #for zim_file in zim_files:
    logging.debug('Processing file = ' + str(zim_file))
    #TODO exception
    copy = open(zim_file + '.copy', 'w')

    noarchive = False

    for line in open(zim_file, 'r'):
        if begin_noarchive.search(line) != None:
            noarchive = True
        if end_noarchive.search(line) != None:
            noarchive = False
        #If we are not in a noarchive block:
        if noarchive == False:
            urls = link.findall(line)
            if urls != []:
                for url in urls:
                    #Is it already archived?
                    logging.debug('url: ' + str(url))
                    if not link_archive_status(url, line):
                        file_uuid = uuid.uuid4()
                        html_file_path = os.path.join(str(zim_archive_path), str(file_uuid) + ".html" )
                        #line = make_archive(html_file_path, url, line)
                        try:
                            archive.make_archive(html_file_path, url)
                        except archive.URLError:
                            #TODO
                            pass
                        else:
                            #We successfully get the page
                            #We change the line
                            logging.debug('Add label')
                            line = add_label(html_file_path, url, line)
        copy.write(line)
    copy.close()
    #The new file is prepared, move it...
    logging.debug('Move the copy to the original file')
    shutil.copyfile(zim_file + '.copy', zim_file)
    os.remove(zim_file + '.copy')


if __name__ == '__main__':
    #TODO doctest
    pass
