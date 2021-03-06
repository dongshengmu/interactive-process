"""
Page output and find dimensions of console.

This module deals with paging on Linux terminals and Windows consoles in
a cross-platform way. The major difference for paging here is line ends.
Not line end characters, but the console behavior when the last character
on a line is printed.  To get technical details, run this module without
parameters::

  python pager.py

Author:  anatoly techtonik <techtonik@gmail.com>
License: Public Domain (use MIT if Public Domain doesn't work for you)
"""

__version__ = 0.1

import os,sys
from termcolor import colored

# Windows constants
# http://msdn.microsoft.com/en-us/library/ms683231%28v=VS.85%29.aspx

STD_INPUT_HANDLE  = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE  = -12

if os.name == 'nt':
    # get console handle
    from ctypes import windll, Structure, byref
    try:
        from ctypes.wintypes import SHORT, WORD, DWORD
    # workaround for missing types in Python 2.5
    except ImportError:
        from ctypes import (
            c_short as SHORT, c_ushort as WORD, c_ulong as DWORD)
    console_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    # CONSOLE_SCREEN_BUFFER_INFO Structure
    class COORD(Structure):
        _fields_ = [("X", SHORT), ("Y", SHORT)]

    class SMALL_RECT(Structure):
        _fields_ = [("Left", SHORT), ("Top", SHORT),
                    ("Right", SHORT), ("Bottom", SHORT)]

    class CONSOLE_SCREEN_BUFFER_INFO(Structure):
        _fields_ = [("dwSize", COORD),
                    ("dwCursorPosition", COORD),
                    ("wAttributes", WORD),
                    ("srWindow", SMALL_RECT),
                    ("dwMaximumWindowSize", DWORD)]


def _windows_get_window_size():
    """Return (width, height) of available window area on Windows.
       (0, 0) if no console is allocated.
    """
    sbi = CONSOLE_SCREEN_BUFFER_INFO()
    ret = windll.kernel32.GetConsoleScreenBufferInfo(console_handle, byref(sbi))
    if ret == 0:
        return (0, 0)
    return (sbi.srWindow.Right - sbi.srWindow.Left + 1,
            sbi.srWindow.Bottom - sbi.srWindow.Top + 1)

def _posix_get_window_size():
    """Return (width, height) of console terminal on POSIX system.
       (0, 0) on IOError, i.e. when no console is allocated.
    """
    # see README.txt for reference information
    # http://www.kernel.org/doc/man-pages/online/pages/man4/tty_ioctl.4.html

    from fcntl import ioctl
    from termios import TIOCGWINSZ
    from array import array

    """
    struct winsize {
        unsigned short ws_row;
        unsigned short ws_col;
        unsigned short ws_xpixel;   /* unused */
        unsigned short ws_ypixel;   /* unused */
    };
    """
    winsize = array("H", [0] * 4)
    try:
        ioctl(sys.stdout.fileno(), TIOCGWINSZ, winsize)
    except IOError:
        # for example IOError: [Errno 25] Inappropriate ioctl for device
        # when output is redirected
        pass
    return (winsize[1], winsize[0])

def getwidth():
    """
    Return width of available window in characters.  If detection fails,
    return value of standard width 80.  Coordinate of the last character
    on a line is -1 from returned value. 

    Windows part uses console API through ctypes module.
    *nix part uses termios ioctl TIOCGWINSZ call.
    """
    width = None
    if os.name == 'nt':
        width = _windows_get_window_size()[0]
        return width or 200
    elif os.name == 'posix':
        width = _posix_get_window_size()[0]
    else:
        # 'mac', 'os2', 'ce', 'java', 'riscos' need implementations
        pass

    return width or 80

def getheight():
    """
    Return available window height in characters or 25 if detection fails.
    Coordinate of the last line is -1 from returned value. 

    Windows part uses console API through ctypes module.
    *nix part uses termios ioctl TIOCGWINSZ call.
    """
    height = None
    if os.name == 'nt':
        height = _windows_get_window_size()[1]
        return height or 50
    elif os.name == 'posix':
        height = _posix_get_window_size()[1]
    else:
        # 'mac', 'os2', 'ce', 'java', 'riscos' need implementations
        pass

    return height or 25

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

def prompt():
    """
    Show default prompt to continue and process keypress.

    It assumes terminal/console understands carriage return \r character.
    """
    if os.name == 'nt' and sys.modules.has_key('idlelib'):
        prompt = colored("Press ENTER to continue, or Q to quit...", 'green')
        sys.stdout.write(prompt)
        sys.stdout.flush()
        c = getch()
        # Win IDLE doesn't do carriage return for '\r'.
        sys.stdout.write('\r')
        sys.stdout.flush()
    else:
        prompt = colored("Press Q to quit, any other key to continue...", 'green')
        sys.stdout.write(prompt)
        sys.stdout.flush()
        c = getch()
        sys.stdout.write('\r' + ' '*len(prompt) + '\r')
        sys.stdout.flush()

    if 'q' in c or 'Q' in c:
        return True
    else:
        return False


last_position = 0
resume_position = 0

def start_paging():
    global resume_position
    resume_position += 1

def end_paging():
    global resume_position, last_position
    resume_position -= 1
    if not resume_position:
        last_position = 0

def print_page(content, pagecallback=prompt, position=None):
    """
    Output content, call `pagecallback` after every page.

    Default callback just shows prompt and waits for keypress.
    """
    global last_position, resume_position
    
    width = getwidth()
    height = getheight()

    if type(content) == str:
        content = content.splitlines()
        content = iter(content)

    try:
        line = content.next().rstrip("\r\n")
    except StopIteration:
        #pagecallback()
        return position if position != None else None

    previous_position = (position if position != None else (last_position if resume_position else 0))
    if previous_position >= height - 1:
        previous_position = 0
    while True:     # page cycle
        linesleft = height - previous_position - 1 # leave the last line for the prompt callback
        previous_position = 0
        while linesleft:
            linelist = [line[i:i+width] for i in xrange(0, len(line), width)]
            if not linelist:
                linelist = ['']
            lines2print = min(len(linelist), linesleft)
            for i in xrange(lines2print):
                if os.name == 'nt' and len(line) == width:
                    # avoid extra blank line by skipping linefeed print
                    sys.stdout.write(linelist[i])
                    sys.stdout.flush()
                else:
                    print(linelist[i])
            linesleft -= lines2print
            linelist = linelist[lines2print:]

            if linelist: # prepare symbols left on the line for the next iteration
                line = ''.join(linelist)
                continue
            else:
                try:
                    line = content.next().rstrip("\r\n")
                except StopIteration:
                    #pagecallback()
                    last_position = (height - linesleft - 1)
                    return (height - linesleft - 1) if position != None else None
        if pagecallback():
            #break
            last_position = 0
            return 0 if position != None else None


if __name__ == '__main__':
    print("Manual tests for pager module.")
    # [ ] find appropriate term of 'console' for Linux
    print("\nconsole size: width %s, height %s" % (getwidth(), getheight()))
    sys.stdout.write("--<enter>--")
    getch()

    print("\nsys.stdout.write() doesn't insert newlines automatically,")
    print("that's why it is used for console output in non-trivial")
    print("cases here.")
    sys.stdout.write("--<enter>--")
    getch()

    print("\nThe following test outputs string equal to the width of the\n"
          "screen and waits for you to press <enter>. It behaves\n"
          "differently on Linux and Windows - W. scrolls the window and\n"
          "places cursor on the next line immediately, while L. window\n"
          "doesn't scroll until the next character is output.")
    print("Tested on:")
    print("  Windows Vista - cmd.exe console")
    print("  Debian Lenny - native terminal")
    print("  Debian Lenny - PuTTY SSH terminal from Windows Vista")
    sys.stdout.write("--<enter>--")
    getch()

    sys.stdout.write("<" + "-"*(getwidth()-2) + ">")
    getch()
    print("^ note there is no newline when the next character is printed")
    print("At least this part works similar on all platforms. It is just\n"
          "the state of the console after the last character on the line\n"
          "is printed that is different.")
    sys.stdout.write("--<enter>--")
    getch()

    print("\nBut there is one special case.")
    print("It is when the next character is a newline.")
    print("The following test prints line equal to the width of the\n"
          "console, waits for <enter>, then outputs newline '\\n',\n"
          "waits for another key press, then outputs 'x' char.")
    sys.stdout.write("--<enter>--")
    getch()

    sys.stdout.write("<" + "-"*(getwidth()-2) + ">")
    getch()
    sys.stdout.write("\n")
    getch()
    sys.stdout.write("x")
    getch()

    print("\n^ here is the difference:")
    print("On Windows you will get:\n"
          "  <----------->\n"
          "  \n"
          "  x")
    print("Linux will show you:\n"
          "  <----------->\n"
          "  x")
    sys.stdout.write("--<enter>--")
    getch()

    print("\nThe next test will fill the screen with '1' digits\n"
          "numbering each line staring from 1.")
    print("It works the same on Linux and Windows, because the next\n"
          "character after the last on the line is not linefeed.\n")
    sys.stdout.write("--<enter>--")
    getch()
    numwidth = len(str(getwidth()))
    strlen = getwidth() - numwidth - 2 # 2 = '. ' after the line number
    filler = '1' * strlen
    for i in xrange(getheight()-1):     # -1 to leave last line for --<enter>--
        lineno = ("%" + str(numwidth) + "s. ") % (i+1)
        #sys.stdout.write(lineno + filler)
        print(lineno + filler)
    sys.stdout.write("--<enter>--")
    getch()

    print("\nNext test prints this source code using print_page() function")
    sys.stdout.write("--<enter>--")
    getch()
    try:
        content = open(__file__)
    except:
        content = open(r"C:\Documents and Settings\dmu\My Documents\My Dropbox\Private\rsi_analyzer_3\pager.py")
    print_page(content)
    sys.stdout.write("--<enter>--")
    getch()
