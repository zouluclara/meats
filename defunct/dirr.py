#!/usr/bin/env python

import re

def dirr(obj, like=''):
    """Print attributes of object/module etc. matching regular expression."""
    test = re.compile(like, re.IGNORECASE)
    for i in dir(obj):
        if test.search(i):
            print i

def getr(obj, like=''):
    """Return first attribute matching regular expression."""
    test = re.compile(like, re.IGNORECASE)
    for i in dir(obj):
        if test.search(i):
            return getattr(obj, i)
    return None

def hlp(obj, like=''):
    """Print help for first attribute matching regular expression."""
    test = re.compile(like, re.IGNORECASE)
    for i in dir(obj):
        if test.search(i):
            help(getattr(obj, i))
            return True
    return False

def interactive():
    try:
        import readline
        import atexit
        import os
        histfile = os.path.expanduser("~/.dirr_history")
        try:
            readline.read_history_file(histfile)
        except IOError:
            pass
        atexit.register(readline.write_history_file, histfile)
    except:
        pass
    modules = []
    try:
        while True:
            cmd = raw_input('dirr> ')
            if cmd == 'q':
                break
            if cmd.startswith('i '):
                try:
                    modules.append(__import__(cmd[2:]))
                    print " == Loaded modules:", ", ".join([m.__name__ for m in modules])
                except ImportError:
                    print "ERROR: Could not import: '%s'" % (cmd[2:],)
            elif cmd.startswith('h '):
                for m in modules:
                    if hlp(m, cmd[2:]):
                        break
            elif cmd == '': # prevent flooding on nervous enter pressing
                pass
            else:
                if cmd.startswith('\\'):
                    # escaping commands like i, q, h,
                    # or even empty query (== show all)
                    cmd = cmd[1:]
                for m in modules:
                    if getr(m, cmd) is not None:
                        print "  ---  In module %s:  ---  " % (m.__name__,)
                        dirr(m, cmd)
    except EOFError:
        pass
    print "\nBe seeing you..."

if __name__ == '__main__':
    interactive()
