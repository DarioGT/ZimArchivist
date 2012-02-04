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

#HTTP
import urllib.request
import socket #for exceptions
import http.client

class URLError(Exception):
    def __init__(self):
        Exception.__init__(self)

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

