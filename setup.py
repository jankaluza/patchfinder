#!/usr/bin/env python
"""
Setup script
"""

import os,sys
pkg_dir = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),
                       'src')

from distutils.core import setup
version = '0.1'

import shutil

if not os.path.exists('scripts'):
    os.makedirs('scripts')
shutil.copyfile('patchfinder.py', 'scripts/patchfinder')


setup(
    name = 'patchfinder',
    description = 'Tool for searching for patches of particular component',
    data_files = [('/usr/share/patchfinder/', [ 'gentoo.db' ] ) ],
    version = version,
    license = 'GPLv2+',
    download_url = 'https://github.com/hanzz/patchfinder',
    url = 'https://github.com/hanzz/patchfinder',
    package_dir = {'patchfinder': 'patchfinder'},
    packages = ['patchfinder', 'patchfinder.plugins'],
    package_data = { '': ['*.tmpl','version']},
    scripts = ["scripts/patchfinder"],
    maintainer  = 'Jan Kaluza',
    maintainer_email = 'hanzz.k@gmail.com'
)
