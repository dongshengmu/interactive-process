#!/usr/bin/env python
#
# Sample script for NG-SRX RE and FlowD commands.
#
# Author: Dongsheng Mu, 10/30/2013
#


import re
import time
import sys
import os

from util import *

def re_cmd(cmd):
    '''Execute a RE command and return the string output.'''
    return os.popen('rsh -l root vre %s' % cmd).read()

def flowd_cmd(cmd):
    '''Execute a FlowD command and return the string output.'''
    return os.popen('rsh -l root vre cprod -A 1 -c %s' % cmd).read().replace('================ master ================\n\n', '')

def flowd_cmds(cmds):
    '''Execute a batch of FlowD commands and return the string output.'''
    tmp = '/var/tmp/flowd_cmds'
    re_cmd('echo "%s" > %s' % (cmds[0], tmp))
    for i in xrange(1, len(cmds)):
        re_cmd('echo "%s" >> %s' % (cmds[i], tmp))
    return os.popen('rsh -l root vre cprod -A 1 %s' % tmp).read().replace('================ master ================\n\n', '')


## test
if __name__ == '__main__':
    import rlcompleter, readline
    readline.parse_and_bind('tab: complete')
    
    print_green('\n\n=== Here is a sample of executing RE CLI command.')
    cmd = 'cli show version'
    print('%% %s\n%s\n' % (cmd, re_cmd(cmd)))

    pause_for_a_key()
    print_green('\n\n=== And a sample of executing RE shell command.')
    cmd = 'top'
    o1 = re_cmd(cmd)
    print('%% %s\n%s\n' % (cmd, o1))
    s=re.search('up ([\w:\+]+) ', o1)
    if s:
        print_green('=== Cmd output analysis: the NG-SRX VRE is up and running for %s.' % s.groups()[0])

    pause_for_a_key()
    print_green('\n\n=== And a sample of JWeb.')
    o= os.popen('curl vre').read()
    print(o)

    pause_for_a_key()
    print_green('\n\n=== And, here is a sample of executing FlowD command.')
    cmd = 'show socket'
    o = flowd_cmd(cmd)
    print('[flowd]# %s\n%s\n' % (cmd, o))
    print_green('=== Cmd output analysis: there are %d sockets in FlowD.' % len(re.findall(' \w{2}/\w{2} ', o)))

    pause_for_a_key()
    cmd = ['show ver', 'show route ip table']
    print_green('\n\n=== And, execute a batch of FlowD commands.\n%s' % cmd)
    o = flowd_cmds(cmd)
    print('%s\n' % o)
    
