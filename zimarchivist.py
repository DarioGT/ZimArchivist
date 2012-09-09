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
#
# Author: Francois Boulogne <fboulogne at sciunto dot org>, 2012

#System...
import sys
import os
import argparse

import logging


#our lib...
from ZimArchivist import zimnotes
from ZimArchivist import utils
from ZimArchivist import timechecker
from ZimArchivist import archive
from ZimArchivist import processtext
from ZimArchivist.timechecker import TimeChecker

from ZimArchivist import info

#############
# Main
#############



if __name__ == '__main__':


    parser = argparse.ArgumentParser(description=info.SHORT_DESCRIPTION,
                     epilog='')

    parser.add_argument('--version', action='version', version=info.NAME + ' ' + info.VERSION) 
    parser.add_argument('--action', help='Action: cache (default) or clean', choices=['cache','clean'], default='cache')
    parser.add_argument('zimroot', help='Zim Notes directory', metavar='DIR')
    parser.add_argument('-f', help='Zim Notes file', metavar='FILE')
    parser.add_argument('--notimecheck', help='No timecheck', action='store_true') 
    #TODO LOG
    #parser.add_argument('--log', help='log') #FIXME no option
    #        #logging.basicConfig(filename=log_filename, filemode='w', level=logging.DEBUG)

    args = parser.parse_args()






    try:
        os.makedirs(os.path.expanduser('~/.zimarchivist'), exist_ok=True)
    except:
        print('Impossible to create ~/.zimarchivist/, Exiting...')
        sys.exit(2)

    lock_file = "~/.zimarchivist/zimarchivist.lock"

    utils.create_pidfile(lock_file)

    log_filename = os.path.expanduser('~/.zimarchivist/zimarchivist.log')
    logging.basicConfig(filename=log_filename, filemode='w', level=logging.DEBUG)

    #TODO : need realpath ?
    #paths...
    #        zim_root = os.path.realpath(arg) 
    

    zim_archive_path = os.path.join(args.zimroot, '.Archive')
    if args.action == 'cache':
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
        
        
        if args.f == None: 
            zim_files = zimnotes.get_zim_files(args.zimroot)
        else:
            zim_files = [args.f]

        logging.info('Processing zim files')

        timechecker = TimeChecker('~/.zimarchivist/time.db', args.zimroot)
        zimnotes.process_zim_file(timechecker, args.zimroot, zim_files, processtext.process_text, args.notimecheck, 3 , zim_archive_path)


    if args.action == 'clean':
        logging.info('Cache cleaning')
        zim_files = zimnotes.get_zim_files(args.zimroot)
        archive.clean_archive(zim_files, zim_archive_path)


    utils.release_pidfile(lock_file)
