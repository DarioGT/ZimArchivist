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

""" Functions dealing with the archive"""

import logging
import os
import sys
import glob
import re
import shutil

#HTTP
import urllib.request
import socket #for exceptions
import http.client

#TODO remove unecessary libs
from bs4 import BeautifulSoup as bs
import urllib.parse as urlparse
from urllib.request import urlopen, urlretrieve



from ZimArchivist import editline

class URLError(Exception):
    def __init__(self):
        Exception.__init__(self)



import threading
import random
import os.path
import os
from queue import Queue

class ThreadImg(threading.Thread):
    """
    Download img with threads
    """
    def __init__(self, lock, uuid, imgs, parsed, htmlpath):
        """
        Constructor
        
        """
        threading.Thread.__init__(self)
        self.lock = lock
        self.queue = imgs
        self.uuid = uuid
        self.parsed = parsed
        self.htmlpath = htmlpath
    
    def run(self):
        """
        One job...
        
        """
        #TODO deals with URLError
        #TODO deals with IOError (connection down?)
        while True:
            img = self.queue.get()

            number = random.random() #Another choice ?
            original_filename = img["src"].split("/")[-1]
            new_filename = str(self.uuid) + '-' + str(number) + str(os.path.splitext(original_filename)[1])
            self.parsed[2] = img["src"]
            
            print('thread: ' + '--> ' + original_filename + '--' + str(number))
            #Directory for pictures
            pic_dir = os.path.join(self.htmlpath, str(self.uuid))
            self.lock.acquire()
            if not os.path.exists(pic_dir):
                os.mkdir(pic_dir)
            self.lock.release()
            outpath = os.path.join(pic_dir, new_filename) 

            #if src start with http...
            if img["src"].lower().startswith("http"):
               urlretrieve(img["src"], outpath)
            #else
            else:
                urlretrieve(urlparse.urlunparse(self.parsed), outpath)
            img["src"] = os.path.relpath(outpath, self.htmlpath) # rel path
            #end...
            self.queue.task_done()
                




def get_archive_list(archive_path):
    """ Return the list of archive files"""
    return glob.glob(os.path.join(archive_path, '*'))
        
        
        
#def make_archive(html_path, url, line):
def make_archive(html_path, url):
    """ Make an archive 
        from the url to the path
    """
    timeout = 15 #seconds
    logging.debug('get ' + url)
    try:
        #Open the URL
        opener = urllib.request.build_opener()
        #Several websites do not accept python...
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        #url = urllib.parse.quote(url, safe='/:?&')
        data = opener.open(url, timeout=timeout)
    except http.client.InvalidURL as e:
        logging.warning('Invalid URL: ' + str(url))
        raise URLError
    except socket.timeout as socket_timeout:
        logging.warning('socket.timeout: ' + str(url))
        raise URLError
    except urllib.error.URLError as e:
        logging.warning('URLError: ' + str(url))
        raise URLError
    except urllib.error.HTTPError as http_err:
        logging.warning('HTTPError: ' + str(url))
        raise URLError
    except:
        logging.warning('URL oops!')
        raise URLError
    else:
        try:
            #Read data from the url
            foo = data.read()
        except socket.timeout as socket_timeout:
            logging.warning('read() socket.timeout: ' + str(socket_timeout))
            raise URLError
        except socket.error as socket_err:
            logging.warning('read() socket.timeout: ' + str(socket_err))
            raise URLError
        except:
            logging.warning('read() oops!')
            raise URLError
        else:
            logging.debug(html_path)
            try:
                filehandler = open(html_path, 'wb')
                filehandler.write(foo)
            except IOError:
                logging.critical('could not write in ' + str(html_path) + ', leaving...') 
                sys.exit(1)

                
                
def make_archive_thread_old(html_path, uuid, url):
    """
    Download the url in html_path
    and everything is named uuid
    """
    #TODO deals with URLError
    from queue import Queue
    from threading import Thread, Lock
    
    logging.debug('get ' + url)
    #Open the url
    soup = bs(urlopen(url))
    #Parsed url
    parsed = list(urlparse.urlparse(url))

    img_queue = Queue()
    number_of_threads = 10

    def download_img_worker(i, lock, image):
        while True:
            img = image.get()
            import random
            number = random.random() #Another choice ?
            original_filename = img["src"].split("/")[-1]
            new_filename = str(uuid) + '-' + str(number) + str(os.path.splitext(original_filename)[1])
            parsed[2] = img["src"]
            
            print('thread: ' + str(i) + '--> ' + original_filename + '--' + str(number))
            #Directory for pictures
            pic_dir = os.path.join(html_path, str(uuid))
            lock.acquire()
            if not os.path.exists(pic_dir):
                os.mkdir(pic_dir)
            lock.release()
            outpath = os.path.join(pic_dir, new_filename) 

            #if src start with http...
            if img["src"].lower().startswith("http"):
               urlretrieve(img["src"], outpath)
            #else
            else:
                urlretrieve(urlparse.urlunparse(parsed), outpath)
            img["src"] = os.path.relpath(outpath, html_path) # rel path
            #end...
            image.task_done()

    #Set up threads
    lock = Lock()
    for thread in range(number_of_threads):
        worker = Thread(target=download_img_worker, args=(thread, lock, img_queue))
        worker.setDaemon(True)
        worker.start()

    #Download images
    for img in soup.findAll("img"):
        img_queue.put(img)

    #wait all the threads...
    print('waiting')
    img_queue.join()
    print('done')
    html_file = os.path.join(html_path, str(uuid) + '.html')
    with open(html_file, 'w') as htmlfile: 
        htmlfile.write(soup.prettify())


def make_archive_thread(html_path, uuid, url):
    """
    Download the url in html_path
    and everything is named uuid
    """
    logging.debug('get ' + url)
    #Open the url
    soup = bs(urlopen(url))
    #Parsed url
    parsed = list(urlparse.urlparse(url))

    img_queue = Queue()
    number_of_threads = 10
    lock = threading.Lock()

    #Set up threads
    for thread in range(number_of_threads):
        worker = ThreadImg(lock, uuid, img_queue, parsed, html_path)
        worker.setDaemon(True)
        worker.start()

    #Download images
    for img in soup.findAll("img"):
        img_queue.put(img)

    #wait all the threads...
    print('waiting')
    img_queue.join()
    print('done')
    html_file = os.path.join(html_path, str(uuid) + '.html')
    with open(html_file, 'w') as htmlfile: 
        htmlfile.write(soup.prettify())



def clean_archive(zim_files, zim_archive_path):
    """ Remove archives with no entry """

    #First, we bluid a dictionary
    #to list html archives which are
    #still in Notes
    file_archives = {}
    for filepath in get_archive_list(zim_archive_path): 
        if filepath.endswith('.html'):
            file_archives[filepath] = False
  
    #We process all zim files
    #To get existing links
    re_archive = re.compile('\s\[\[.*\|\(Archive\)\]\]')
    for filename in zim_files:
        for line in open(filename, 'r'):
            for path in editline.extract_labels_filepath(line):
                print(path)
                #FIXME the key may not exist, should be handled
                path = os.path.expanduser(path)
                #it exists -> True
                file_archives[path] = True

    #We delete all path related to False value
    for htmlfile in file_archives.keys():
        if file_archives[htmlfile] == False:
            print('key')
            print(htmlfile)
            logging.info('remove ' + str(htmlfile))
            os.remove(htmlfile)
            directory = htmlfile.rstrip('.html')
            if os.path.exists(directory):
                shutil.rmtree(directory) 
                
                
if __name__ == '__main__':
    pass
