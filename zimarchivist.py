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

#TODO detect links containing pdf...
#TODO detect obsolete archived html files
#TODO prevent a URL archivement
#FIXME accent dans URL
#thread for downloading?
#TODO catch sigterm, keyinterrupt...




#############
# Archives
#############

#TODO split...
def clean_archive(zim_files, zim_archive_path):
    """ Remove archives with no entry """
    #TODO
    file_archives = {}
    for filename in glob.glob(os.path.join(zim_archive_path, '*')): #fonction faite
        #faire un dico nom -> bool = False
        file_archives[filename] = False
   
    re_archive = re.compile('\s\[\[.*\|Archive\]\]')
    for filename in zim_files:
        for line in open(filename, 'r'):
            #lire ligne par ligne
            #récupérer les partie archives -> nom de fichier.
            #passer le bool à True
            
            archive_tags = re_archive.findall(line)
            
            if archive_tags != []:
                print(line)
                for tag in archive_tags:
                    print(tag)
                    pass
                    #TODO

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
    zimarchive --cache -f ~/Notes -o ~/Archive

    Actions:
        --cache: make a cache
        --clean: clean the cache
    
    Paths:
        -f: Zim notes directory
        -o: Archive dirctory
            by default, Zim_Notes_Directory/.Archive

    """

    print(usage)


if __name__ == '__main__':
    log_filename = os.path.join(os.getenv('HOME'), 'zimarchivist.log')
    logging.basicConfig(filename=log_filename, filemode='w', level=logging.DEBUG)
    zim_root = None
    zim_archive_path = None
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hf:o:", ['help', 'clean', 'cache'])
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
        elif opt in '-f':
            logging.debug("Option -f: " + str(arg))
            zim_root = os.path.realpath(arg) 
        elif opt in '-o':
            logging.debug("Option -o: " + str(arg))
            zim_archive_path = os.path.realpath(arg) 

    if action_clean_archive or action_make_archive:
        #Check if we know paths...         
        if zim_root == None:
            logging.critical('Missing -f option. Exiting')
            usage()
            sys.exit(2)
        if zim_archive_path == None:
            zim_archive_path = os.path.join(zim_root, '.Archive')

    if action_make_archive:
        if not (os.path.isdir(zim_archive_path)):
            try:
                os.mkdir(zim_archive_path)
            except OSError:
                logging.critical('could not make ', zim_archive_path)
                sys.exit(1)
            except IOError:
                logging.critical('could not make ', zim_archive_path)
                sys.exit(1)
        
        zim_files = zimnotes.get_zim_files(zim_root)
    
        logging.info('Processing zim files')
        zimnotes.add_cache_zim_files(zim_files, zim_archive_path)

    if action_clean_archive:
        zim_files = zimnotes.get_zim_files(zim_root)
        clean_archive(zim_files, zim_archive_path)