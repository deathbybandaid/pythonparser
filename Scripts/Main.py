#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# system imports
import os
import sys


"""
This is the central script
"""


def mainfunction():

    # create dynamic class
    dbbparse = class_create('dbbparse')

    # save relative paths of interest
    dbbparse = relativepaths(dbbparse)

    print str(dbbparse.paths)

    # dbb_avatar(dbbparse)


def relativepaths(dbbparse):
    dbbparse.paths = dict()

    dbbparse.paths['current'] = os.path.dirname(__file__)

    return dbbparse


def dbb_avatar(dbbparse):
    filepath = 'sadsdf'
    inf = codecs.open(filepath, "r", encoding='utf-8')
    infread = inf.read()
    inf.close()
    for line in infread:
        print line


def class_create(classname):
    compiletext = """
        def __init__(self):
            self.default = str(self.__class__.__name__)
        def __repr__(self):
            return repr(self.default)
        def __str__(self):
            return str(self.default)
        def __iter__(self):
            return str(self.default)
        pass
        """
    exec(compile("class class_" + str(classname) + ": " + compiletext, "", "exec"))
    newclass = eval('class_'+classname+"()")
    return newclass


"""
Nothing else below this line
"""


mainfunction()
