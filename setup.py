#!/usr/bin/env python

from distutils.core import setup
from ZimArchivist import info

setup(
    name         = 'ZimArchivist',
    version      = info.VERSION,
    url          = info.URL,
    author       = "Francois Boulogne",
    license      = info.LICENSE,
    author_email = info.EMAIL,
    description  = info.SHORT_DESCRIPTION,
    packages     = ['ZimArchivist'],
    scripts      = ['zimarchivist'],
    requires     = ['libZimSciunto (>=0.3)'],
)
