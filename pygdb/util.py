#!/usr/bin/env python
#
# Misc little utilities.
#
# Author: Dongsheng Mu, 10/30/2013
#

from __future__ import print_function  # to use Python3 print function.

import re
import time
import sys
import os

from termcolor import colored
from pager import getwidth


#
# Colored print
#
def print_green(s):
    print(colored(s, 'green'))

def print_red(s):
    print(colored(s, 'red'))

def print_blue(s):
    print(colored(s, 'blue'))

def print_cyan(s):
    print(colored(s, 'cyan'))

def print_no_newline(s):
    print(s, end='')

def print_progress(msg, width=None):
    if not width:
        width = getwidth()
    sys.stderr.write(colored('\r' + ' '*width + '\r' + msg[0 : width -1], 'green'))
    sys.stderr.flush()

def getch():
    """
    Wait for keypress and return character in a cross-platform way.
    """
    import sys
    if os.name == 'nt' and sys.modules.has_key('idlelib'):
        return raw_input()
    # Credits: Danny Yoo, Python Cookbook
    try:
        import msvcrt
        return msvcrt.getch()
    except ImportError:
        ''' we're not on Windows, so we try the Unix-like approach '''
        import sys, tty, termios
        fd = sys.stdin.fileno( )
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def pause_for_a_key(msg='Press any key to continue...'):
    print_progress(msg)
    c = getch()
    print_progress('')
    return c


## test
if __name__ == '__main__':
    print_red('print red.')
    print_green('print green.')
    pause_for_a_key()
    print_green('test done.')

