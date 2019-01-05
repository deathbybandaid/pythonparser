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
import requests
from fake_useragent import UserAgent


# user agent and header
ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}


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
    dividerbar()
    if not gitpull(dbbparse):
        return

    # starting cleanup
    dividerbar()
    tempclean(dbbparse)

    # Run logs
    logsclean(dbbparse)

    # Check internet connection
    dividerbar()
    if not internet():
        return

    dbbparse = settings_get(dbbparse)

    dbbparse.lists = dict()

    # Download Files
    dbbparse = filedownloader(dbbparse)

    # Final cleanup
    dividerbar()
    tempclean(dbbparse)

    dividerbar()
    dbbparse.time['script_end'] = time.time()

    howlongcomplete = humanized_time(dbbparse.time['script_end'] - dbbparse.time['script_start'])
    osd(textarray='Script took ' + howlongcomplete + ' to complete.', color='GREEN')
    print('\n' * 2)

    # push to github
    dividerbar()
    if dbbparse.settings['github_push']:
        if not gitpush(dbbparse):
            return
    else:
        osd(textarray='Not Pushing to github, to change this, edit the config file.', color='purple')


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


def filedownloader(dbbparse):

    for listtype in ["TLD", "Black", "White"]:

        dividerbar("blue")
        osd(textarray='Dowloading all ' + listtype + ' Lists, as well as saving mirrors.', color='YELLOW')

        dbbparse.lists[listtype] = dict()

        listindexdir = os.path.join(dbbparse.paths['listindexes'], listtype)

        listmirrordir = os.path.join(dbbparse.paths['mirrors'], listtype)

        if os.path.isdir(listindexdir):

            if len(os.listdir(listindexdir)) > 0:

                for listindexlist in os.listdir(listindexdir):

                    if listindexlist != "PERMANENT_PLACEHOLDER":

                        dividerbar("purple")
                        osd(textarray='Dowloading all ' + listindexlist + ' Lists.', color='blue', indent=1)

                        dbbparse.lists[listtype][listindexlist] = dict()

                        dbbparse.lists[listtype][listindexlist]['urls'] = []

                        lines = [line.rstrip('\n') for line in open(os.path.join(listindexdir, listindexlist))]

                        for line in lines:
                            if line.startswith(tuple(["https://", "http://"])):
                                dbbparse.lists[listtype][listindexlist]['urls'].append(line)

                        totalurls = len(dbbparse.lists[listtype][listindexlist]['urls'])

                        osd(textarray=listindexlist + " has " + str(totalurls) + " list(s).", color='purple', indent=2)

                        indexnum = 1
                        dbbparse.lists[listtype][listindexlist]['urlnums'] = dict()

                        for addr in dbbparse.lists[listtype][listindexlist]['urls']:

                            osd(textarray="Processing " + listindexlist + " list " + str(indexnum) + " of " + str(totalurls) + ".", color='purple', indent=3)

                            listmirrorpath = os.path.join(listmirrordir, listindexlist + "." + str(indexnum))

                            # try to get data
                            try:
                                page = requests.get(addr, headers=header)
                            except Exception as e:
                                page = None

                            if page and not str(page.status_code).startswith(tuple(["4", "5"])):

                                pagecontents = page.content
                                dbbparse.lists[listtype][listindexlist]['urlnums'][indexnum] = pagecontents

                                # save mirror
                                if not os.path.exists(listmirrorpath):
                                    open(listmirrorpath, 'a').close()
                                mirrorsave = open(listmirrorpath, "w")
                                mirrorsave.write(str(pagecontents))
                                mirrorsave.close()
                                osd(textarray=listindexlist + " list " + str(indexnum) + " of " + str(totalurls) + " downloaded successfully.", color='green', indent=4)
                            else:
                                osd(textarray=listindexlist + " list " + str(indexnum) + " of " + str(totalurls) + " failed to download.", color='red', indent=4)

                            indexnum += 1

    return dbbparse


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


def dividerbar(color='BOLD'):

    osd(textarray=["___________________________________________________________"], color='BOLD')


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


def settings_get(dbbparse):

    # Read dictionary from file, if not, enable an empty dict
    filereadgood = True
    inf = codecs.open(dbbparse.paths['settings'], "r", encoding='utf-8')
    infread = inf.read()
    try:
        dict_from_file = eval(infread)
    except Exception as e:
        filereadgood = False
        osd(textarray=["Error loading Settings File: %s" % (e)], color='red', indent=1)
        dict_from_file = dict()
    # Close File
    inf.close()

    dbbparse.settings = dict_from_file

    print('\n' * 2)

    return dbbparse


def gitpull(dbbparse):
    osd(textarray='Pulling From Github.', color='YELLOW')
    try:
        g = git.cmd.Git(dbbparse.paths['root'])
        g.pull()
        osd("Pulling " + str(dbbparse.paths['root']) + " From Github Success", color='green', indent=1)
        print('\n' * 2)
        return True
    except Exception as e:
        osd("Pulling " + str(dbbparse.paths['root']) + " From Github Failed: " + str(e), color='RED', indent=1)
    print('\n' * 2)
    return False


def gitpush(dbbparse):

    osd("Pushing To Github", color='yellow')
    try:
        repo = git.Repo(dbbparse.paths['root'])
        repo.git.add(update=True)
        committime = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        repo.index.commit("Update lists " + committime)
        origin = repo.remote(name='origin')
        origin.push()
        osd("Pushing " + str(dbbparse.paths['root']) + " To Github Success", color='green', indent=1)
        print('\n' * 2)
        return True
    except Exception as e:
        osd("Pushing " + str(dbbparse.paths['root']) + " To Github Failed: " + str(e), color='RED', indent=2)
        print('\n' * 2)
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

    dbbparse.paths['logs'] = os.path.join(dbbparse.paths['root'], 'Logs')

    dbbparse.paths['reqtxt'] = os.path.join(dbbparse.paths['scripts_common'], 'requirements.txt')

    dbbparse.paths['parser'] = os.path.join(dbbparse.paths['scripts_common'], 'parser.py')

    dbbparse.paths['mirrors'] = os.path.join(dbbparse.paths['root'], 'Mirrors')
    dbbparse.paths['subscribable'] = os.path.join(dbbparse.paths['root'], 'Subscribable')
    dbbparse.paths['listindexes'] = os.path.join(dbbparse.paths['root'], 'listindexes')

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


def logsclean(dbbparse):
    osd(textarray='Cleaning Logs Directory.', color='YELLOW')
    for root, dirs, files in os.walk(dbbparse.paths['logs'], topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    placeholderfile = os.path.join(dbbparse.paths['logs'], 'PERMANENT_PLACEHOLDER')
    open(placeholderfile, 'a').close()
    print('\n' * 2)


def logswrite():
    dd = 5


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
