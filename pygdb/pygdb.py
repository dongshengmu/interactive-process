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

#
# a live gdb session.
#
class gdb_session(interactive_subprocess):
    def __init__(self, prog, prog_args='',
                 name='gdb', prompt='(gdb) ', timeout=5, delay=0.001,
                 print_input=lambda x: print_cyan(x, end=''),
                 print_output=print_no_newline,
                 print_stderr=lambda x: print_magenta(x, end=''),
                 print_warn=print_red,
                 hide_output=False):
        """
        Open a interactive_subprocess with default settings for gdb.
        """
        self.program = prog
        self.prog_args = prog_args
        interactive_subprocess.__init__(self, cmd = 'gdb %s' % prog,
                                        name=name, prompt=prompt, timeout=timeout, delay=delay,
                                        print_input=print_input, print_output=print_output,
                                        print_stderr=print_stderr, print_warn=print_warn,
                                        hide_output=hide_output)
        # setup gdb environment
        self.send('set args %s\n' % prog_args)
        self.send('set print pretty\n')
        self.send('set output-radix 16\n')
        # disable printf buffering in the program, so its printf output can be
        # flushed to gdb stdout
        self.send('b main\n')
        self.send('commands\n', expect='>')
        #self.send('silent\n', expect='>')
        if sys.platform == 'darwin':
            # Mac OSX gdb fails to call void function
            #self.send('call setbuf(__stdoutp, 0)\n', expect='>')
            self.send('print "Note, to see program output, call setbuf(stdout, 0) in main()."\n', expect='>')
            pass
        elif sys.platform.startswith('freebsd'):
            self.send('call setbuf(__stdoutp, 0)\n', expect='>')
        else:
            # linux
            #self.send('call setbuf(stdout, 0)\n', expect='>')
            self.send('print "Note, to see program output, call setbuf(stdout, 0) in main()."\n', expect='>')
        self.send('cont\n', expect='>')
        self.send('end\n')


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
    gdb = gdb_session(prog=program, prog_args='',
                      # print_input = lambda x: print_cyan(x[:-1] if x.endswith('\n') else x) or pause_for_a_key()
                      )
    
    print_green('Set breakpoints.')
    gdb.send('b %s\n' % bp)
    gdb.send('break cmfwdd_pic_online if msg->fpc_slot==0\n')
    gdb.send('commands\n', expect='>')
    #gdb.send('silent\n', expect='>')
    gdb.send('print "msg->fpc_slot is %d, I will change it to 1.", msg->fpc_slot\n', expect='>')
    gdb.send('set msg->fpc_slot = 1\n', expect='>')
    gdb.send('cont\n', expect='>')
    gdb.send('end\n')
    gdb.send('info break\n')
    
    print_green('Now run the program.')
    gdb.send('run\n')
    
    print_green('Exam some data.')
    o, e = gdb.send('p %s\n' % var)
    o1, e1 = gdb.send('p a_nonexist_var\n')
    o += o1
    e += e1
    
    print_green('Check the result.')    
    if pat in o:
        n = int(re.search('item_count = (\w+),', o).groups()[0], 16)
        print_green('PASS: %s has been initialized @ %s(), with %d modules.' % (var, bp, n))
    else:
        print_red('FAIL: %s has NOT been initialized @ %s.' % (var, bp))

    print_green('Continue.')
    gdb.send('c\n', expect=None, delay=0.1)
    print_green('Send Ctrl-C.')
    gdb.ctrl_c()

    print_green('Now close the program.')
    gdb.close()

