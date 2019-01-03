#!/usr/bin/env python
# coding=utf-8

# system imports
import os
import sys


"""
This is the central script
"""


def mainfunction():

    # create dynamic class
    dbbparse = class_create('dbbparse')

    print 'herea'

    # save relative paths of interest
    dbbparse = relativepaths(dbbparse)

    print 'hereb'

    print str(dbbparse.paths)

    # dbb_avatar(dbbparse)


def relativepaths(dbbparse):
    dbbparse.paths = dict()

    dbbparse.paths['scripts'] = os.path.split(os.path.abspath(os.path.realpath(sys.argv[0])))[0]

    dbbparse.paths['root'] = os.path.dirname(dbbparse.paths['scripts'])

    return dbbparse


def dbb_avatar():
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
