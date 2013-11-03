#!/usr/bin/env python
#
# Python controlled GDB session.
#
# Author: Dongsheng Mu, 10/30/2013
#

"""
Python controlled GDB session for whitebox test.
"""

import re
import time
import sys
import os

from util import *
from interact import *



## test
if __name__ == '__main__':
    import rlcompleter, readline
    readline.parse_and_bind('tab: complete')

    ###
    ### A sample of Python controlled GDB session for white-box test.
    ###

    print_green('=== This is a sample of Python controlled GDB session for white-box testing.\nby Dongsheng Mu, 11/02/2013\n')
    program = 'a.out' #'/var/tmp/flowd'
    bp = 'ukern_module_init'
    var = '*module_node_toolkit_table'
    pat = 'Module toolkit'

    print_green('Starting GDB for %s\n' % program)
    gdb = interactive_subprocess(cmd='gdb %s' % program, name='gdb', prompt='(gdb) ',
                                 # print_input = lambda x: print_cyan(x[:-1] if x.endswith('\n') else x) or pause_for_a_key()
                                 )
    
    print_green('Setup gdb environment.')
    gdb.send('set args\n')
    gdb.send('set print pretty\n')
    gdb.send('set output-radix 16\n')

    print_green('Set breakpoints.')
    gdb.send('b %s\n' % bp)
    gdb.send('break cmfwdd_pic_online if msg->fpc_slot==0\n')
    gdb.send('commands\n', expect='>')
    gdb.send('silent\n', expect='>')
    gdb.send('print "msg->fpc_slot is %d, I will change it to 1.", msg->fpc_slot\n', expect='>')
    gdb.send('msg->fpc_slot = 1\n', expect='>')
    gdb.send('cont\n', expect='>')
    gdb.send('end\n')
    gdb.send('info break\n')
    
    print_green('Now run the program.')
    gdb.send('run\n')
    
    print_green('Exam some data.')
    o = gdb.send('p %s\n' % var)

    print_green('Check the result.')    
    if pat in o:
        n = int(re.search('item_count = (\w+),', o).groups()[0], 16)
        print_green('PASS: %s has been initialized @ %s(), with %d modules.' % (var, bp, n))
    else:
        print_red('FAIL: %s has NOT been initialized @ %s.' % (var, bp))

    print_green('Continue.')
    gdb.send('c\n', expect=None)
    print_green('Send Ctrl-C.')
    gdb.ctrl_c()
    print_green('Now close the program.')
    gdb.close()

