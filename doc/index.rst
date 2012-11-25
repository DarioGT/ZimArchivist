.. ZimArchivist documentation master file, created by
   sphinx-quickstart on Thu Sep 27 22:13:53 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ZimArchivist's documentation!
========================================
ZimArchivist is designed for your Zim wiki: zim-wiki.org
It makes copies of your links in your notes on your disk.

Contents:

.. toctree::
   :maxdepth: 2



What is ZimArchivist?
=====================

Based on the fact that web changes everyday, the link you save in your zim notes could be obsolete (dead, the page moved...)
This is a bit annoying. The solution is to keep on your hard drive a copy of the web page.
To open it easily, ZimArchiver add a link to this copy next to the URL in your notes.
Just click on it, it will be opened in your broswer.

What is the license?
======================
GNU GPL v3 or later.


How to install
==============

Requirements
------------

* python 3
* `python-libZimSciunto <http://pypi.python.org/pypi/libZimSciunto/>`_
* BeautifulSoup 4

Install
-------

A package is available on `pypi <http://pypi.python.org/pypi/ZimArchivist/>`_.
Otherwise, you can install it by running:

.. code-block:: sh

    python setup.py install --root='/'


How to run ZimArchivist?
========================
There is two ways to use ZimArchivist.

The Hacker's way
----------------
You can run the software from the command line. This means the job could be done by a cron task.


The zim way
-----------
In tool menu, add the zimarchivist command. 
You can choose to apply on one file or on the whole zim notebook.
This is **not** recommended yet, see the FAQ.

OK, and the command is?
=======================
The command

.. code-block:: sh

    zimarchivist -h 

gives you all details.

Make a cache of a specific file URLs 
-------------------------------------

.. code-block:: sh

    zimarchivist -f ~/Notes/Home.txt ~/Notes

Make a cache of the notebook URLs
---------------------------------

.. code-block:: sh

    zimarchivist ~/Notes 


Clean archive cache
-------------------
If you remove in your note a line with a link and its archive label, the archive itself is not removed.
To clean up your archive, run

.. code-block:: sh

    zimarchivist --action=clean ~/Notes 


Features 
========
Some intersting features.

Mime Type
--------
ZimArchivist will try to guess the format behind a link.
For instance, if your url links to a pdf or a jpeg file, it is saved as it.
Otherwise, ZimArchivist will consider that the page is in html. In that case, it will download images included in the page.

Do not archive this page/part 
-----------------------------
From time to time, you could desire to avoid archiving.

.. code-block:: text

    Everything below the tag
    {noarchive}
    will be ignored.
    http://www.foo.org
    If you want to stop this behaviour, write
    {/noarchive}

.. code-block:: text

    or on a single line {noarchive} http://www.bar.org {/noarchive} like that.

or a simpler way:

.. code-block:: text

    !@ this line is not processed by ZimArchivist

Things you may want to know 
---------------------------

ZimArchivist first get the last modification date of each zimfile.
If it is known that no modification occurs after the last caching process, nothing is done.
This behavior could be override by adding the option --no-timecheck

Logfiles, pid files and other internal files are stored in ~/.zimarchivist/

FAQ
===

Where can I find my archives? 
-----------------------------
There are located in .Archive in your notebook path.
Each archive is named by an ID.

Why the paths are ~/Notes and not /home/user/Notes?
-----------------------------------------------------
This is because I'm syncing my notes on several computers with different usernames.
Thus, my paths work on every systems.

Is it dangerous for my notes? 
----------------------------
I don't think so. I'm using it every day and I have never seen any drawback.
The thing you should know is that Zim does not reload the notebook when a file is modified.
This means you can have a conflict if you continue to edit your notes after a cache process.
Hopefully, this will be fixed soon. See https://bugs.launchpad.net/zim/+bug/792058 for more information.


Moreover, I keep track of my notes in a git repository. So, I can revert if something goes wrong.
You can do the same.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

