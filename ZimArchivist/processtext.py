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
    text = re.sub("!@.*", '', text)
    return text

    
def process_text(original_text, zim_archive_path):
    """
    Core function, process the whole text:
    * Look for the URLs in the text
    * Download the content
    * Add internal links in the text

    The function returns a status (bool) indicating if true
    that something goes wrong; and the remplacing text.

    :returns: Tuple (boolean, string)
    """
    link = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#~]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    #get a copy without noarchive stuffs
    copy_text = strip_noarchive(original_text)

    #get all URLs
    urls = link.findall(copy_text)

    errors = False

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
                logging.error('URLError: ' + str(url) + ' Not archived.')
                errors = True
            else:
                #We successfully get the page
                #We change the line
                logging.debug('Add label')
                file_path = os.path.join(str(zim_archive_path), str(file_uuid) + str(extension) )
                original_text = editline.add_label(file_path, url, original_text)
        else:
            logging.debug('Already archived')
    return (errors, original_text)

