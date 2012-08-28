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

import re
import logging
import uuid
import os
from ZimArchivist import archive
from ZimArchivist import editline


def strip_noarchive(text):
    """
    Remove the content inside
    {noarchive}
    {/noarchive}
    and the tags
    """
    text = re.sub('\{noarchive\}(\n|.)*?\{\/noarchive\}', '', text) #re.DOTALL buggy? FIXME
    return text

    
def process_text(original_text, zim_archive_path):
    """
    Core function, process the whole text
    """
    link = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#~]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    #get a copy without noarchive stuffs
    copy_text = strip_noarchive(original_text)

    #get all URLs
    urls = link.findall(copy_text)

    for url in urls:
        #Is it already archived?
        logging.debug('url: ' + str(url))
        if not editline.link_archive_status(url, copy_text):
            file_uuid = uuid.uuid4()
            try:
                #archive.make_archive(html_file_path, url)
                #new version:
                extension = archive.make_archive_thread(zim_archive_path, file_uuid, url)
            except archive.URLError:
                logging.error('URLError: ' + str(url))
                #TODO
                pass
            else:
                #We successfully get the page
                #We change the line
                logging.debug('Add label')
                file_path = os.path.join(str(zim_archive_path), str(file_uuid) + str(extension) )
                original_text = editline.add_label(file_path, url, original_text)
        else:
            logging.debug('Already archived')
    return original_text

    
    
