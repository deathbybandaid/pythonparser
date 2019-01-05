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

    # save relative paths of interest
    dbbparse = relativepaths(dbbparse)

    # Logo
    dbb_avatar(dbbparse)
    print('\n' * 2)

    depchecks(dbbparse)


def depchecks(dbbparse):

    # pip Dependencies
    osd(textarray='Checking Dependencies.', color='YELLOW')

    osd(textarray='Checking pip.', color='YELLOW', indent=1)
    try:
        __import__('pip')
    except ImportError:
        return osd(textarray='Pip must be installed to check for relevant dependencies!', color='RED', indent=2)
    osd(textarray='pip already installed.', color='green', indent=2)
    print('\n' * 1)

    osd(textarray='Checking pipreqs.', color='YELLOW', indent=1)
    try:
        __import__('pipreqs')
        preinstalled = True
    except ImportError:
        preinstalled = False
    if not preinstalled:
        osd(textarray='pipreqs not installed, installing now.', color='blue', indent=2)
        from pip._internal import main as pipmain
        pipmain(['install', 'pipreqs'])
    else:
        osd(textarray='pipreqs already installed.', color='green', indent=2)
    import pipreqs
    osd(textarray='pipreqs is generating a list of dependencies.', color='purple', indent=3)
    print('\n' * 1)

    pipreqsdeps = []
    os.popen(str("pipreqs " + dbbparse.paths['scripts_common'] + " --force"))
    if os.path.exists(dbbparse.paths['reqtxt']):
        piprequires = [line.rstrip('\n') for line in open(os.path.join(dbbparse.paths['reqtxt']))]
        for pypipreq in piprequires:
            if pypipreq not in ['']:
                if "=" in pypipreq:
                    pypipreq = pypipreq.split("=")[0]
                if ">" in pypipreq:
                    pypipreq = pypipreq.split(">")[0]
                if "<" in pypipreq:
                    pypipreq = pypipreq.split("<")[0]
                pipreqsdeps.append(pypipreq)
    else:
        return osd(textarray='pipreqs failed to generate a list!', color='RED', indent=3)

    if pipreqsdeps != []:
        for pipdep in pipreqsdeps:
            osd(textarray='Checking ' + pipdep + '.', color='YELLOW', indent=1)
            try:
                __import__(str(pipdep))
                preinstalled = True
            except ImportError:
                preinstalled = False
            if not preinstalled:
                osd(textarray=pipdep + ' not installed, installing now.', color='blue', indent=2)
                from pip._internal import main as pipmain
                pipmain(['install', pipdep])
            else:
                osd(textarray=pipdep + ' already installed.', color='green', indent=2)
            print('\n' * 1)
        print('\n' * 1)
    else:
        osd(textarray='No other requirements needed.', color='green', indent=1)
        print('\n' * 2)

    osd(textarray='Script is ready to start!', color='blue')

    os.system('python ' + dbbparse.paths['parser'])


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
    sys.stdout.flush()


"""
File Structures
"""


def relativepaths(dbbparse):
    dbbparse.paths = dict()

    dbbparse.paths['scripts'] = os.path.split(os.path.abspath(os.path.realpath(sys.argv[0])))[0]

    dbbparse.paths['scripts_common'] = os.path.join(dbbparse.paths['scripts'], 'Common')

    dbbparse.paths['root'] = os.path.dirname(dbbparse.paths['scripts'])

    dbbparse.paths['temp'] = os.path.join(dbbparse.paths['root'], 'Temp')

    dbbparse.paths['reqtxt'] = os.path.join(dbbparse.paths['scripts_common'], 'requirements.txt')

    dbbparse.paths['parser'] = os.path.join(dbbparse.paths['scripts_common'], 'parser.py')

    return dbbparse


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
