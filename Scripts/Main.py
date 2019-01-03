#!/usr/bin/env python
# coding=utf-8


"""
This is the central script
"""


def mainfunction():
    dbbparse = class_create('dbbparse')
    print 'here'
    # relativepaths()
    # dbb_avatar()


def relativepaths():
    dd = 5


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
