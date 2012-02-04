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

#System...
import sys
import os
import glob
import getopt

#Regex
import re

import logging


#our lib...
import zimnotes
import utils
import timechecker



#############
# Archives
#############

#TODO split...
def clean_archive(zim_files, zim_archive_path):
    """ Remove archives with no entry """
   
    #First, we bluid a dictionary
    #to list usefull archives
    file_archives = {}
    for filename in archive.get_archive_list(zim_archive_path): 
        file_archives[filename] = False
   
    re_archive = re.compile('\s\[\[.*\|\(Archive\)\]\]')
    for filename in zim_files:
        for line in open(filename, 'r'):
            for path in zimnotes.extract_labels_filepath(line):
                #FIXME (just filename)
                #FIXME the key may not exist, should be handled
                file_archives[path] = True

    for arch in file_archives.keys():
        if file_archives[arch] == False:
            #os.remove
            pass
    pass


#############
# Main
#############

def usage():
    """ Print usage... """
    usage = """
    zimarchive --cache -d ~/Notes

    Actions:
        --cache: make a cache
        Arg: 
            -d: Zim notes directory
        Option:
            -f: Zim file path (Otherwise, the notebook is processed)


        --clean: clean the cache by removing inecessary archives
        Arg: 
            -d: Zim notes directory
    """

    print(usage)


if __name__ == '__main__':
    try:
        os.makedirs(os.path.expanduser('~/.zimarchivist'), exist_ok=True)
    except:
        print('Impossible to create ~/.zimarchivist/, Exiting...')
        sys.exit(2)

    utils.create_pidfile()

    log_filename = os.path.expanduser('~/.zimarchivist/zimarchivist.log')
    logging.basicConfig(filename=log_filename, filemode='w', level=logging.DEBUG)

    
    zim_root = None
    zim_archive_path = None
    zim_file_path = None
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hd:f:", ['help', 'clean', 'cache'])
    except getopt.GetoptError:
        logging.critical('Wrong option')
        usage() 
        sys.exit(2)

        
    action_make_archive = False
    action_clean_archive = False
        
    for opt, arg in opts:   
        if opt in ('-h', '--help'):
            logging.debug("Option -h")
            usage()
            sys.exit(0)
        elif opt in '--log':
            pass
            #TODO
            #logging.basicConfig(filename=log_filename, filemode='w', level=logging.DEBUG)
        elif opt in '--clean':
            logging.debug("Option --clean")
            action_clean_archive = True
        elif opt in '--cache':
            logging.debug("Option --cache")
            action_make_archive = True
        elif opt in '-d':
            logging.debug("Option -d: " + str(arg))
            zim_root = os.path.realpath(arg) 
        elif opt in '-f':
            logging.debug("Option -f: " + str(arg))
            zim_file_path = os.path.realpath(arg) 

    if action_clean_archive or action_make_archive:
        #Check if we know paths...         
        if zim_root == None:
            logging.critical('Missing Notebook filepath. Exiting')
            usage()
            sys.exit(2)
        zim_archive_path = os.path.join(zim_root, '.Archive')

    if action_make_archive:
        #Create the .Archive file
        if not (os.path.isdir(zim_archive_path)):
            try:
                os.mkdir(zim_archive_path)
            except OSError:
                logging.critical('could not make ', zim_archive_path)
                sys.exit(1)
            except IOError:
                logging.critical('could not make ', zim_archive_path)
                sys.exit(1)
        if zim_file_path == None: 
            #All file should be processed
            zim_files = zimnotes.get_zim_files(zim_root)
    
            logging.info('Processing zim files')
            for zim_file in zim_files:
                zim_file_relativepath = zim_file.split(zim_root + '/')[1]
                if timechecker.get_file_modif_status(zim_root, zim_file_relativepath):
                    zimnotes.process_zim_file(zim_file, zim_archive_path)
                    timechecker.set_time(zim_file_relativepath)
        else:
            #Only one file
            zim_file_relativepath = zim_file_path.split(zim_root + '/')[1]
            if timechecker.get_file_modif_status(zim_root, zim_file_relativepath):
                zimnotes.process_zim_file(zim_file_path, zim_archive_path)
                timechecker.set_time(zim_file_relativepath)

    if action_clean_archive:
        pass
        zim_files = zimnotes.get_zim_files(zim_root)
        clean_archive(zim_files, zim_archive_path)


    utils.release_pidfile()
