#!/usr/bin/env python
#
# Class interactive_subprocess.
#
# Author: Dongsheng Mu, 11/02/2013
#

"""
Module for an interactive subprocess class.
A programmably interactive process, useful to control
a command line interface driven process, such like gdb.
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
class interactive_subprocess():
    def __init__(self, cmd, name='', prompt='', timeout=5, delay=0.1,
                 print_input=lambda x: print_cyan(x[:-1] if x.endswith('\n') else x),
                 print_output=print_no_newline,
                 print_warn=print_red,
                 hide_output=False):
        """
        Open a programmably interactive process, useful to control
        a command line interface driven process, like gdb.
        
        Parameters:
            cmd:    the command line to start the process.
            name:   a string name for the process.
            prompt: the command prompt of the process. When this prompt is found
                    in the program output, a command execution is considered done.
            timeout: value in seconds, to timeout a command execution, in case
                    the prompt or expected output is not found.
            delay:  value in second (can be 0.x), to smooth out any jitter when
                    process outputing.
            print_intput: method to print the input command send to the process.
            print_output: method to print the process output.
            print_warn:   method to print any warning or error.
            hide_output: if True, don't print the output of process starting.
        
        Note 1: it uses fcntl to have a non-blocking pipe file object for
        subprocess, so that stdout.read won't hang. This only works for UNIX.
        
        Note 2: for telnet, ftp, etc, socket based telnetlib.Telnet and
        ftplib.FTP are more effective.
        """

        # init default values
        self.cmdline = cmd
        self.name = name
        self.prompt = prompt
        self.delay = delay
        self.timeout = timeout
        self.remaining_output = ''  # remaining output from previous execution
        no_print = lambda x: None
        self.print_input = print_input if print_input else no_print
        self.print_output = print_output if print_output else no_print
        self.print_warn = print_warn if print_warn else no_print
        
        # open the process, as a subprocess.Popen object.
        cmd_list = shlex.split(cmd)
        self.print_input('Starting interactive-process %s: %s' % (self.name, cmd))
        p = subprocess.Popen(cmd_list, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             universal_newlines=True)
        if not p:
            self.print_warn('ERROR: fail to open %s process, "%s".' % (self.name, input))

        # change the pipe to non-blocking
        fd = p.stdout.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        self.process = p
        self.flush(hide_output=hide_output)


    def send(self, input, expect='', timeout=None, hide_output=False):
        """
        Execute a cmd in the process, or send some input to the process.
        
        input:  key stokes to send to the process. Need to include '\n' for 
                command.
        expect: a string is expected from the process output. Return when it 
                is found.
                If not specified, the execution returns when the
                process prompt is found.
                If expect is None, return immediately, without waiting for
                any output.
        timeout: timeout value (in second) for the command execution. If not
                specified, the default timeout of the process is used.
        hide_output: if True, don't print the process output for this call.
     
        return: the process's output.
        """

        p = self.process
        timeout = timeout if timeout else self.timeout
        no_wait = expect == None
        expect = expect if expect else self.prompt
        print_output = (lambda x: None) if hide_output else self.print_output

        # send input to process
        if input:
            self.print_input(input)
            p.stdin.write(input)

        # now wait for the output.
        if self.remaining_output:
            output = self.remaining_output
            print_output('(previous remaining output: "%s")' % self.remaining_output)
            self.remaining_output = ''
        else:
            output = ''

        start_time = time.time()
        if p.poll() != None:
            self.print_warn('Process %s has exited with code %s' % (self.name, p.poll()))
        while p.poll() == None: # check whether the process exits.
            # delay first, give the process time to run.
            time.sleep(self.delay)
            o = ''
            try:
                o = p.stdout.read()
                print_output(o)
                output += o
            except IOError:
                # Process has no new output during the delay period,
                # it might be busy, completed output, or encountered error.
                pass
            if no_wait:
                break
            if expect and expect in output:
                self.remaining_output = output[output.rfind(expect) + len(expect) :]
                output = output[: output.rfind(expect) + len(expect)]
                break
            if time.time() - start_time > timeout:
                self.print_warn('WARN: %s timed out for "%s", timeout %d seconds, '
                           'expect "%s".'
                           % (self.name, input, timeout, expect))
                break

        if (not no_wait) and (not output):
            self.print_warn('WARN: %s has no output for "%s".' % (self.name, input))
    
        return output
    


    def flush(self, expect='', timeout=None, hide_output=False):
        """
        Flush any previous output buffered.
        
        Note:
            Useful to flush the remaining output after a cmd was executed with an
            expect string, so the next cmd execution will only check its own output.
            
        This is same as calling send(input=None, expect, timeout, hide_output). 
        The parameters are same as in send()
        """

        return self.send(input=None, expect=expect, timeout=timeout, 
                         hide_output=hide_output)


    def ctrl_c(self, expect=''):
        """
        Send a Ctrl-C SIGINT to the process.
        """
        self.print_input('Send Ctrl-C SIGINT to %s.' % self.name)
        self.process.send_signal(subprocess.signal.SIGINT)
        self.flush(expect=expect)
 
    
    def close(self):
        """
        Terminate the process.
        """
        self.print_input('Closing %s with SIGTERM.' % self.name)
        self.flush(expect=None)
        self.process.terminate()
        

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

