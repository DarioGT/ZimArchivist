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
import shutil
import glob
import getopt

#Regex
import re

#HTTP
import urllib.request
import socket #for exceptions
import http.client

import logging
import uuid



def protect(s):
    """Protect Metacaracters in a string"""
    s = re.sub('\&', '\\\&', s)
    s = re.sub('\?', '\\\?', s)
    return s

def get_zim_files(zim_root):
    """get the list of txt zim files """
    logging.info('Looking for zim files in ' + str(zim_root))
    zim_files = []
    for root, dirnames, filenames in os.walk(zim_root):
        for filename in glob.glob(str(root) + '*.txt' ):
            zim_files.append(filename)
    if zim_files == []:
        logging.warning('No zim file found!')
    return zim_files

def get_unexpanded_path(path):
    """
    Convert /home/foo by ~ in a path

    >>> get_unexpanded_path('/home/foo/dir')
    '~/dir'
    """
    newpath = os.path.relpath(path, start=os.getenv('HOME'))
    newpath = os.path.join('~', newpath)
    return newpath

def make_archive(html_path, url, line):
    """ Make an archive """
    timeout = 15 #seconds
    logging.debug('get ' + url)
    try:
        #Open the URL
        opener = urllib.request.build_opener()
        #Several websites do not accept python...
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        data = opener.open(url, timeout=timeout)
    except http.client.InvalidURL as e:
        logging.warning('Invalid URL: ' + str(url))
    except socket.timeout as socket_timeout:
        logging.warning('socket.timeout: ' + str(url))
    except urllib.error.URLError as e:
        logging.warning('URLError: ' + str(url))
    except urllib.error.HTTPError as http_err:
        logging.warning('HTTPError: ' + str(url))
    else:
        try:
            #Read data from the url
            foo = data.read()
        except socket.timeout as socket_timeout:
            logging.warning('read() socket.timeout: ' + str(socket_timeout))
        except socket.error as socket_err:
            logging.warning('read() socket.timeout: ' + str(socket_err))
        except:
            logging.warning('read() oops!')
        else:
            logging.debug(html_path)
            try:
                filehandler = open(html_path, 'wb')
                filehandler.write(foo)
            except IOError:
                logging.critical('could not write in ' + str(html_path) + ', leaving...') 
                sys.exit(1)
            else:
                #everything is fine, add the link
                new_url = url + " [[" + get_unexpanded_path(html_path) + "|Archive]]"
                url = protect(url)
                line = re.sub(url, new_url, line)
    return line

def link_archive_status(url, line):
    """ 
    Is the url in the line already archived? 
    False: Not archived 
    True: Archived
    """
    logging.debug('line= ' + str(line))
    link_archived = re.compile(str(url) + '\s\[\[.*\|Archive\]\]')
    matching = link_archived.search(line)
    if matching == None:
        return False
    else:
        return True

def process_zim_file(zim_file, zim_archive_path):
    """ Add in the zim file the link"""
    link = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    logging.debug('Processing file = ' + str(zim_file))
    copy = open(zim_file + '.copy', 'w')

    for line in open(zim_file, 'r'):
        urls = link.findall(line)
        if urls == []:
            #there is no link
            copy.write(line)
            pass
        else:
            for url in urls:
                #Is it already archived?
                if not link_archive_status(url, line):
                    file_uuid = uuid.uuid4()
                    html_file_path = os.path.join(str(zim_archive_path), str(file_uuid) + ".html" )
                    line = make_archive(html_file_path, url, line)
            #All urls have been treated, write the line
            copy.write(line)
    copy.close()
    #The new file is prepared, move it...
    shutil.copyfile(zim_file + '.copy', zim_file)
    os.remove(zim_file + '.copy')

#FIXME accent dans URL


def usage():
    usage = """
    zimarchive -f ~/Notes -o ~/Archive

    -f: Zim notes directory
    -o: Archive dirctory
        by default, Zim_Notes_Directory/.Archive

    """

    print(usage)


if __name__ == '__main__':
    #TODO: write ~ instead of /home/foo/ in zim
    log_filename = os.path.join(os.getenv('HOME'), 'zimarchivist.log')
    logging.basicConfig(filename=log_filename, filemode='w', level=logging.DEBUG)
    zim_root = None
    zim_archive_path = None
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hf:o:", ['help'])
    except getopt.GetoptError:
        logging.critical('Wrong option')
        usage() 
        sys.exit(2)

    for opt, arg in opts:   
        if opt in ('-h', '--help'):
            logging.debug("Option -h")
            usage()
        elif opt in '--log':
            pass
            #TODO
            #logging.basicConfig(filename=log_filename, filemode='w', level=logging.DEBUG)
        elif opt in '-f':
            logging.debug("Option -f: " + str(arg))
            zim_root = os.path.realpath(arg) 
        elif opt in '-o':
            logging.debug("Option -o: " + str(arg))
            zim_archive_path = os.path.realpath(arg) 

    if zim_root == None:
        logging.critical('Missing -f option. Exiting')
        usage()
        sys.exit(2)

    if zim_archive_path == None:
        zim_archive_path = os.path.join(zim_root, '.Archive')

    if not (os.path.isdir(zim_archive_path)):
        try:
            os.mkdir(zim_archive_path)
        except OSError:
            logging.critical('could not make', zim_archive_path)
            sys.exit(1)
        except IOError:
            logging.critical('could not make', zim_archive_path)
            sys.exit(1)
    
    zim_files = get_zim_files(zim_root)
   
    logging.info('Processing zim files')
    for zim_file in zim_files:
        process_zim_file(zim_file, zim_archive_path)
