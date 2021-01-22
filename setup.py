#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright (C) 2020 David Miguel Susano Pinto <david.pinto@bioch.ox.ac.uk>
##
## Copying and distribution of this file, with or without modification,
## are permitted in any medium without royalty provided the copyright
## notice and this notice are preserved.  This file is offered as-is,
## without any warranty.

import setuptools
import setuptools.command.sdist

project_name = "napari-microscope"
project_version = "0.0.2"

# Modify the sdist command class to include extra files in the source
# distribution.  Seems a bit ridiculous that we have to do this but
# the only alternative is to have a MANIFEST file and we don't want
# to have yet another configuration file.
#
# The package_data (from setuptools) and data_files (from distutils)
# options are for files that will be installed and we don't want to
# install this files, we just want them on the source distribution
# for user information.
manifest_files = [
    "COPYING",
    "NEWS",
    "README",
]


class sdist(setuptools.command.sdist.sdist):
    def make_distribution(self):
        self.filelist.extend(manifest_files)
        setuptools.command.sdist.sdist.make_distribution(self)


setuptools.setup(
    name=project_name,
    version=project_version,
    description="Napari plugin for Microscope.",
    long_description=open("README", "r").read(),
    license="GPL-3.0+",
    author="David Miguel Susano Pinto",
    author_email="david.pinto@bioch.ox.ac.uk",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["Pyro4", "microscope", "napari_plugin_engine",],
    entry_points={"napari.plugin": "microscope = napari_microscope",},
    # https://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Plugins",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
    cmdclass={"sdist": sdist,},
)
