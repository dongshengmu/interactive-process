#!/usr/bin/env python
#
# A utility to provision a DevVM based on the parameters 
# specified in devvm_provision Data Base.
#
# Author: Dongsheng Mu, 11/7/2013
#

"""
A utility to provision a DevVM based on the parameters
specified in devvm_provision Data Base.
    
Syntax: vm_prov.py name-of-new-vm
"""

import re
import time
import sys
import os

from util import *
from interact import *
from devvm_provision import this_db


class DevVM_class():
    def __init__(self, name, template='srxbuild06-DevVM'):
        self.name = name
        self.db = this_db[name]
        self.template = template
        self.tmdb = this_db[template]


    def clone_template(self):
        # virt-clone --original srxbuild06-DevVM --name srxbuild07-DevVM02 --file srxbuild07-DevVM02
        img = self.db['img_file']
        print_green('Cloning DevVM template to %s...' % img)
        # virt-clone copies the disk img and creates xml file with unique uuid and mac.
        return os.system('virt-clone --original %s --name %s --file %s' 
               	         % (self.template, self.db['name'], img))


    def define_vm(self):
        xf = self.db['xml_file']
        print_green('Defining VM %s...' % xf)
        if 0 == os.system('virsh define %s' % xf):
            print_green('VM %s successfully cloned based on %s.\n'
                        'Run "virsh start --console %s" to start the VM.'
                        % (self.db['name'], self.tmdb['name'], self.db['name']))
        else:
            print_red('Fail to define VM %s.' % self.db['name'])


    def modify_img(self):
        img = self.db['img_file']
        file_changes = [ # (filename, old, new)
            # IP address
            ('/etc/sysconfig/network-scripts/ifcfg-eth0', self.tmdb['IP'], self.db['IP']),
            # hostname
            ('/etc/sysconfig/network', self.tmdb['hostname'], self.db['hostname'])
            ]

        for change in file_changes:
            print_green('Modifying %s %s' % (img, change[0]))     
            os.system("virt-edit -a %s %s -e 's/%s/%s/'" 
                      % (img, change[0], change[1], change[2]))

 
    def start(self):
        os.system('virsh start %s' % self.db['name'])

    '''
    def console_and_customize(self):
        print_green('In VM console, do below then reboot.')
        print_green("sed -i -e 's/%s/%s/' /etc/sysconfig/network-scripts/ifcfg-eth0" % (self.tmdb['IP'], self.db['IP']))
        print_green("sed -i -e 's/%s/%s/' /etc/sysconfig/network\n" % (self.tmdb['hostname'], self.db['hostname']))
        # start vm and connect to console
        con = interactive_subprocess(cmd='virsh console %s --force' % self.db['name'],
                                     name='VM-Console', prompt=' ~]# ')
        con.send(input=None, expect='login: ', timeout=180)
        con.send('root\n', expect='Password: ')
        con.send('Embe1mpls\n')
        #sed -i -e 's/old hostname line/new hostname line/' /etc/HOSTNAME
        con.send("sed -i -e 's/%s/%s/' /etc/sysconfig/network-scripts/ifcfg-eth0\n" % (self.tmdb['IP'], self.db['IP']))
        con.send("sed -i -e 's/%s/%s/' /etc/sysconfig/network\n" % (self.tmdb['hostname'], self.db['hostname']))
        con.send("reboot\n", expect='Restarting system.', timeout=300)
        con.ctrl_square()
    '''


    def modify_qemu_xml_file(self):
        xf = self.db['xml_file']
        print_green('Modifying qemu XML file,  %s...' % xf)
        
        s = open(xf).read()
        
        # MAC, UUID, disk img file, are updated by virt-clone.

        # replace the ixgbevf pci devices
        ixgbevf = self.db['ixgbevf']
        tm = self.tmdb['ixgbevf']
        for i in xrange(8):
            s = s.replace("<address domain='0x0000' bus='%s' slot='%s' function='%s'/>"
                          % (tm[i][0], tm[i][1], tm[i][2]),
                          "<address domain='0x0000' bus='%s' slot='%s' function='%s'/>"
                          % (ixgbevf[i][0], ixgbevf[i][1], ixgbevf[i][2]))

        # save the file
        open(xf, 'w').write(s)



# test
if __name__ == '__main__':
    import rlcompleter, readline
    readline.parse_and_bind('tab: complete')

        
    # copy template img
    if not (len(sys.argv) == 3 and sys.argv[1] in this_db and sys.argv[2] in this_db):
        print_red('Please provision a DevVM in devvm_provision.py, then\n'
                  '"vm_prov.py name-of-new-vm template-vm"')
        sys.exit('No or unknown DevVM name provided.')

    name = sys.argv[1]
    template = sys.argv[2]
    # Clone a VM at the Host Machine
    vm = DevVM_class(name, template)
    if (vm.clone_template()):
        sys.exit('Fail to clone')
    vm.modify_qemu_xml_file()
    vm.modify_img()
    # Now define the VM
    vm.define_vm()

