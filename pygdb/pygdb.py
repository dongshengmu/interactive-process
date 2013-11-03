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
import subprocess, fcntl
import shlex

from util import *

#
# subprocess, to interact with shell, process.
#
def interactive_popen(cmd):
    """
    Open a programmably interactive process, useful to control
    a command line interface driven process, like gdb.

    Note 1: it uses fcntl to have a non-blocking pipe file object for
    subprocess, so that stdout.read won't hang. This only works for UNIX.
    
    Note 2: for telnet, ftp, etc, socket based telnetlib.Telnet and
    ftplib.FTP are more effective.
    """
    cmd_list = shlex.split(cmd)
    p = subprocess.Popen(cmd_list, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True)
    # change the pipe to non-blocking
    fd = p.stdout.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    return p

def interactive_exec(p, input=None, delay=0.1, expect='', timeout=1):
    """
    Send a cmd to an interactive process, return the output.

    p : process returned by interactive_popen()
    input : key stokes to send to the process. Need to include '\n' for command.
    delay : seconds or sub-seconds to smooth out any jitter when process outputing.
    expect : return when the expect string appears.
    timeout: max seconds to wait for the process to complete its output.
    """
    # send input to process
    if input:
        p.stdin.write(input)
    # now wait for the output.
    start_time = time.time()
    output = ''
    while p.poll() == None: # check whether the process exits.
        # delay first, give the process time to run.
        time.sleep(delay)
        try:
            output += p.stdout.read()
        except IOError:
            # Process has no new output during the delay period,
            # it either completed output, or encountered error.
            #print_red('Got IOError')
            pass
        if expect and expect in output:
            break
        if time.time() - start_time > timeout:
            break
    return output

def interactive_pclose(p):
    p.terminate()


## test
if __name__ == '__main__':

    ###
    ### A sample of Python controlled GDB session for white-box test.
    ###

    print_green('=== This is a sample of Python controlled GDB session for white-box testing.\n')
    program = '/var/tmp/flowd'
    bp = 'ukern_module_init'
    var = '*module_node_toolkit_table'
    pat = 'Module toolkit'
    gdb_prompt = '(gdb)'

    print_green('\n\n=== Starting GDB for %s\n' % program)
    p = interactive_popen('gdb %s' % program)
    o = interactive_exec(p, input='', expect=gdb_prompt, timeout=10)
    print(o)
    
    print_green('\n\n=== Setup gdb environment.')
    o = interactive_exec(p, input='set args\n', expect=gdb_prompt)
    o += interactive_exec(p, input='set print pretty\n', expect=gdb_prompt)
    o += interactive_exec(p, input='set output-radix 16\n', expect=gdb_prompt)
    print(o)

    bp = 'ukern_module_init'
    print_green('\n\n=== Set breakpoints.')
    o = interactive_exec(p, input='b %s\n' % bp, expect=gdb_prompt)
    o += interactive_exec(p, input='break cmfwdd_pic_online if msg->fpc_slot==0\n'
                                   'commands\n'
                                   'silent\n'
                                   'print "msg->fpc_slot is %d, I will change it to 1.", msg->fpc_slot\n'
                                   'msg->fpc_slot = 1\n'
                                   'cont\n'
                                   'end\n', expect=gdb_prompt)
    print(o)
    o = interactive_exec(p, input='info break\n', expect=gdb_prompt)
    print(o)
    
    print_green('\n\n=== Now run the program.')
    o = interactive_exec(p, input='run\n', expect=gdb_prompt)
    print(o)
    
    print_green('\n\n=== Exam some data.')
    o = interactive_exec(p, input='p %s\n' % var, expect=gdb_prompt)
    print(o)

    print_green('\n\n=== Check the result.')    
    if pat in o:
        n = int(re.search('item_count = (\w+),', o).groups()[0], 16)
        print_green('PASS: %s has been initialized @ %s(), with %d modules.' % (var, bp, n))
    else:
        print_red('FAIL: %s has NOT been initialized @ %s.' % (var, bp))

