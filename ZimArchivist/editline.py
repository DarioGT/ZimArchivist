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
from ZimArchivist import utils


def add_label(html_path, url, line):
    """
    Add the label "Archive" to the archive after the url in the line 
    Return the line
    """
    integrated_link = re.compile('\[\[' + utils.protect(url) + '(\|.*\]\])')
    matching = integrated_link.search(line)
    if matching == None:
        #It is not an integrated link
        effective_pattern = url
        new_url = effective_pattern + " [[" + utils.get_unexpanded_path(html_path) + "|(Archive)]]"
    else:
        #It is...
        effective_pattern = '[[' + url + matching.groups()[0]
        new_url = effective_pattern + " [[" + utils.get_unexpanded_path(html_path) + "|(Archive)]]" 
    effective_pattern = utils.protect(effective_pattern)
    line = re.sub(effective_pattern, new_url, line)
    return line

def link_archive_status(url, line):
    """ 
    Is the url in the line already archived?
    Basically, it checks if [[path|(Archive)]] follows the url
    False: Not archived 
    True: Archived
    """
    logging.debug('line: ' + str(line))
    link_archived = re.compile(utils.protect(url) + '(\|.*\]\])?\s\[\[.*\|\(Archive\)\]\]')
    matching = link_archived.search(line)
    if matching == None:
        return False
    else:
        return True

def extract_labels_filepath(line):
    filepaths = []
    #First, we detect labels
    re_archive = re.compile('\s\[\[(.+)\|\(Archive\)\]\]')
    labels = re.findall('\s\[\[(.+?)\|\(Archive\)\]\]', line) #? is for non-greedy (minimal) fashion
    for label in labels:
        filepaths.append(label)
    return filepaths
