#!/usr/bin/env python
# coding=utf-8

# system imports
import os
import sys


# other imports
import json
import codecs
import time
import socket
import git


"""
This is the central script
"""


def mainfunction():

    print('\n' * 2)

    # create dynamic class
    dbbparse = class_create('dbbparse')

    dbbparse.time = dict()

    dbbparse.time['script_start'] = time.time()

    # save relative paths of interest
    dbbparse = relativepaths(dbbparse)

    # pull from github
    if not gitpull(dbbparse):
        return

    # starting cleanup
    tempclean(dbbparse)

    # Check internet connection
    if not internet():
        return

    # Final cleanup
    tempclean(dbbparse)

    dbbparse.time['script_end'] = time.time()

    howlongcomplete = humanized_time(dbbparse.time['script_end'] - dbbparse.time['script_start'])
    osd(textarray='Script took ' + howlongcomplete + ' to complete.', color='GREEN')
    print('\n' * 2)

    # push to github
    if not gitpush(dbbparse):
        return


"""
Network Functions
"""


def internet(host="8.8.8.8", port=53, timeout=3):
    osd(textarray='Checking for internet connection.', color='YELLOW')
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        osd(textarray='Internet connection success!!', indent=1, color='GREEN')
        print('\n' * 2)
        return True
    except Exception as ex:
        osd(textarray='Internet appears to be down!', color='RED', indent=1)
        return False


"""
Display Functions
"""


def dbb_avatar(dbbparse):
    filepath = os.path.join(dbbparse.paths['scripts_common'], 'avatar.txt')
    lines = [line.rstrip('\n') for line in open(filepath)]
    osd(textarray=lines)


def humanized_time(countdownseconds):
    time = float(countdownseconds)
    if time == 0:
        return "0 seconds"
    year = time // (365 * 24 * 3600)
    time = time % (365 * 24 * 3600)
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minute = time // 60
    time %= 60
    second = time
    displaymsg = None
    timearray = ['year', 'day', 'hour', 'minute', 'second']
    for x in timearray:
        currenttimevar = eval(x)
        if currenttimevar >= 1:
            timetype = x
            if currenttimevar > 1:
                timetype = str(x+"s")
            if displaymsg:
                displaymsg = str(displaymsg + " " + str(int(currenttimevar)) + " " + timetype)
            else:
                displaymsg = str(str(int(currenttimevar)) + " " + timetype)
    if not displaymsg:
        return "0 seconds"
    return displaymsg


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
    osd(textarray='Pulling From Github.', color='YELLOW')

    print('\n' * 2)
    return True

    if os.path.isdir(dbbparse.paths['root']):
        try:
            g = git.cmd.Git(dbbparse.paths['root'])
            g.pull()
            print('\n' * 2)
            return True
        except Exception as e:
            osd("Pulling " + str(dbbparse.paths['root']) + " From Github Failed: " + str(e), color='RED', indent=1)
    else:
        osd("Pulling " + str(dbbparse.paths['root']) + " From Github Failed: Not a Valid Directory.", color='RED', indent=1)
    return False


def gitpush(dbbparse):

    osd("Pushing To Github", color='GREEN')
    try:
        repo = git.Repo(dbbparse.paths['root'])
        repo.git.add(update=True)
        repo.index.commit("Update lists " + str(time.time()))
        repo.git.push("origin", "HEAD:refs/for/master")
        print('\n' * 2)
        return True
    except Exception as e:
        osd("Pushing " + str(dbbparse.paths['root']) + " To Github Failed: " + str(e), color='RED', indent=2)
    return False


def relativepaths(dbbparse):
    dbbparse.paths = dict()

    dbbparse.paths['current'] = os.path.split(os.path.abspath(os.path.realpath(sys.argv[0])))[0]

    dbbparse.paths['scripts_common'] = dbbparse.paths['current']

    dbbparse.paths['scripts'] = os.path.dirname(dbbparse.paths['current'])

    dbbparse.paths['root'] = os.path.dirname(dbbparse.paths['scripts'])

    dbbparse.paths['installdir'] = os.path.dirname(dbbparse.paths['root'])

    dbbparse.paths['settings'] = os.path.join(dbbparse.paths['installdir'], 'pythonparser.json')

    dbbparse.paths['temp'] = os.path.join(dbbparse.paths['root'], 'Temp')

    dbbparse.paths['reqtxt'] = os.path.join(dbbparse.paths['scripts_common'], 'requirements.txt')

    dbbparse.paths['parser'] = os.path.join(dbbparse.paths['scripts_common'], 'parser.py')

    return dbbparse


def tempclean(dbbparse):
    osd(textarray='Cleaning Temp Directory.', color='YELLOW')
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
    print('\n' * 2)


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
