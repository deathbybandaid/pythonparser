#!/usr/bin/env python
# coding=utf-8

# system imports
import os
import sys

# other imports
import time
import socket
import git


"""
This is the central script
"""


def mainfunction():

    # create dynamic class
    dbbparse = class_create('dbbparse')

    # save relative paths of interest
    dbbparse = relativepaths(dbbparse)

    # Logo
    dbb_avatar(dbbparse)
    print('\n' * 2)

    osd(textarray='Pulling From Github.', color='YELLOW')
    if not gitpull(dbbparse):
        return
    print('\n' * 2)

    osd(textarray='Cleaning Temp Directory.', color='YELLOW')
    tempclean(dbbparse)
    print('\n' * 2)

    # Check internet connection
    osd(textarray='Checking for internet connection.', color='YELLOW')
    if not internet():
        osd(textarray='Internet appears to be down!', color='RED')
        return
    osd(textarray='Internet connection success!!', indent=1, color='GREEN')
    print('\n' * 2)


"""
Network Functions
"""


def internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        return False


"""
Display Functions
"""


def dbb_avatar(dbbparse):
    filepath = os.path.join(dbbparse.paths['scripts_common'], 'avatar.txt')
    lines = [line.rstrip('\n') for line in open(filepath)]
    osd(textarray=lines)


def osd(textarray=[], indent=0, color='BOLD'):

    if not isinstance(textarray, list):
        textarray = [str(textarray)]

    if len(textarray) == 0:
        return

    try:
        coloreval = eval('bcolors.' + color.upper())
        endcolor = bcolors.ENDC
    except AttributeError:
        coloreval = ''
        endcolor = ''

    for entry in textarray:
        indentstr = ''
        if indent:
            if not isinstance(indent, int):
                indent = 1
            indentstr = "     " * indent
        print indentstr + coloreval + entry + endcolor


"""
File Structures
"""


def gitpull(dbbparse):
    if os.path.isdir(dbbparse.paths['root']):
        osd("Pulling " + str(dbbparse.paths['root']) + "From Github.", color='GREEN', indent=1)
        try:
            g = git.cmd.Git(dbbparse.paths['root'])
            g.pull()
            return True
        except Exception as e:
            osd("Pulling " + str(dbbparse.paths['root']) + "From Github Failed: " + str(e), color='RED', indent=1)
    else:
        osd("Pulling " + str(dbbparse.paths['root']) + "From Github Failed: Not a Valid Directory.", color='RED', indent=1)
    return False


def gitpush(dbbparse):
    if os.path.isdir(dbbparse.paths['root']):
        osd("Pushing " + str(dbbparse.paths['root']) + "To Github.", color='GREEN', indent=1)
        try:
            g = git.cmd.Git(dbbparse.paths['root'])
            g.push()
            return True
        except Exception as e:
            osd("Pulling " + str(dbbparse.paths['root']) + "To Github Failed: " + str(e), color='RED', indent=1)
    else:
        osd("Pulling " + str(dbbparse.paths['root']) + "To Github Failed: Not a Valid Directory.", color='RED', indent=1)
    return False


def relativepaths(dbbparse):
    dbbparse.paths = dict()

    dbbparse.paths['scripts'] = os.path.split(os.path.abspath(os.path.realpath(sys.argv[0])))[0]

    dbbparse.paths['scripts_common'] = os.path.join(dbbparse.paths['scripts'], 'Common')

    dbbparse.paths['root'] = os.path.dirname(dbbparse.paths['scripts'])

    dbbparse.paths['temp'] = os.path.join(dbbparse.paths['root'], 'Temp')

    return dbbparse


def tempclean(dbbparse):
    for root, dirs, files in os.walk(dbbparse.paths['temp'], topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    placeholderfile = os.path.join(dbbparse.paths['temp'], 'PERMANENT_PLACEHOLDER')
    open(placeholderfile, 'a').close()
    for tempsub in ['Bak', 'Processing']:
        tempsubdir = os.path.join(dbbparse.paths['temp'], tempsub)
        os.mkdir(tempsubdir)
        placeholderfile = os.path.join(tempsubdir, 'PERMANENT_PLACEHOLDER')
        open(placeholderfile, 'a').close()


"""
Classes
"""


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


class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


"""
Nothing else below this line
"""


mainfunction()
