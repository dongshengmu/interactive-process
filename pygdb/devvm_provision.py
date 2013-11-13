#
# DevVM provision Data Base.
#
# Author: Dongsheng Mu, 11/7/2013
#

"""
DevVM provision table.

To clone a DevVM from a existing VM on the same server:
    define a DevVM in devvm_provision.py, with the VM specific parameters
    ./vm_prov.py new-vm-name existing-vm

To create a DevVM on a new physical server without any existing DevVM,
we clone the srxbuild06-DevVM, whose disk img is at mounted /home/VMs.
    yum install "*guestfs*", to get virt-edit
    mount -t nfs -o rw cougar-01:/home/VMs /home/VMs
    mkdir /home/localVMs
    cd /home/localVMs
    scp xxx@svl-junos-d013:/homes/dmu/dev/pygdb/*.py .
    scp xxx@cougar-evl02:/etc/libvirt/qemu/srxbuild06-DevVM.xml .
    virsh define srxbuild06-DevVM
    define the new DevVM in devvm_provision.py
    ./vm_prov.py new-vm-name srxbuild06-DevVM
    virsh undefine srxbuild06-DevVM
"""


this_db = {
    'dev IP pool':  ['srxdevvm01.spglab, 10.159.16.231 to srxdevvm10.spglab, 10.159.16.240'],
    'qa IP pool':   ['10.157.79.200 to 10.157.79.209'],

    'cougar-evl02': {'pci-ixgbe' : ('09:10.0', '09:1f.5')},

    'srxbuild06-DevVM': # the sunnyvale DevVM template
    {   'name'         : 'srxbuild06-DevVM',
        'IP'           : '10.159.16.215',
        'img_file'     : '/home/VMs/cougar-kvm03-centos-dev-dmu.snapshot_kvm03_dmu-clone',
        'xml_file'     : '/etc/libvirt/qemu/srxbuild06-DevVM.xml',
        'hostname'     : 'srxbuild06',
        'server'       : 'cougar-evl02',
        'location'     : 'svl',
        'user'         : 'dmu',
        # the PCI device numbers from "lspci | grep 82599"
        'ixgbevf'      : [('0x09', '0x10', '0x0'),
                          ('0x09', '0x10', '0x2'),
                          ('0x09', '0x10', '0x4'),
                          ('0x09', '0x10', '0x6'),
                          ('0x09', '0x11', '0x0'),
                          ('0x09', '0x11', '0x2'),
                          ('0x09', '0x11', '0x4'),
                          ('0x09', '0x11', '0x6')],
    },

    'srxbuild07-DevVM02':
    {   'name'         : 'srxbuild07-DevVM02',
        'IP'           : '10.159.16.216',
        'img_file'     : '/home/localVMs/srxbuild07-DevVM02',
        'xml_file'     : '/etc/libvirt/qemu/srxbuild07-DevVM02.xml',
        'hostname'     : 'srxbuild07',
        'server'       : 'cougar-evl02',
        'location'     : 'svl',
        'user'         : 'jwag',
        'ixgbevf'      : [('0x09', '0x12', '0x0'),
                          ('0x09', '0x12', '0x2'),
                          ('0x09', '0x12', '0x4'),
                          ('0x09', '0x12', '0x6'),
                          ('0x09', '0x13', '0x0'),
                          ('0x09', '0x13', '0x2'),
                          ('0x09', '0x13', '0x4'),
                          ('0x09', '0x13', '0x6')],
    },

    'srxbuild08-DevVM03':
    {   'name'         : 'srxbuild08-DevVM03',
        'IP'           : '10.159.16.217',
        'img_file'     : '/home/localVMs/srxbuild08-DevVM03',
        'xml_file'     : '/etc/libvirt/qemu/srxbuild08-DevVM03.xml',
        'hostname'     : 'srxbuild08',
        'server'       : 'cougar-evl02',
        'location'     : 'svl',
        'user'         : 'jiama',
        'ixgbevf'      : [('0x09', '0x14', '0x0'),
                          ('0x09', '0x14', '0x2'),
                          ('0x09', '0x14', '0x4'),
                          ('0x09', '0x14', '0x6'),
                          ('0x09', '0x15', '0x0'),
                          ('0x09', '0x15', '0x2'),
                          ('0x09', '0x15', '0x4'),
                          ('0x09', '0x15', '0x6')],
    },

    'srxbuild05-DevVM04':
    {   'name'         : 'srxbuild05-DevVM04',
        'IP'           : '10.159.16.214',
        'img_file'     : '/home/localVMs/srxbuild05-DevVM04',
        'xml_file'     : '/etc/libvirt/qemu/srxbuild05-DevVM04.xml',
        'hostname'     : 'srxbuild05',
        'server'       : 'cougar-evl02',
        'location'     : 'svl',
        'user'         : '',
        'ixgbevf'      : [('0x09', '0x16', '0x0'),
                          ('0x09', '0x16', '0x2'),
                          ('0x09', '0x16', '0x4'),
                          ('0x09', '0x16', '0x6'),
                          ('0x09', '0x17', '0x0'),
                          ('0x09', '0x17', '0x2'),
                          ('0x09', '0x17', '0x4'),
                          ('0x09', '0x17', '0x6')],
    },

    'cougar-lnx'  : {'pci-ixgbe' : ('07:10.0', '07:1f.5')},

    'cougar-kvm02-DevVM05':
    {   'name'         : 'cougar-kvm02-DevVM05',
        'IP'           : '10.159.16.222',
        'img_file'     : '/home/localVMs/cougar-kvm02-DevVM05',
        'xml_file'     : '/etc/libvirt/qemu/cougar-kvm02-DevVM05.xml',
        'hostname'     : 'cougar-kvm02',
        'server'       : 'cougar-lnx',
        'location'     : 'svl',
        'user'         : 'dmu',
        'ixgbevf'      : [('0x07', '0x10', '0x0'),
                          ('0x07', '0x10', '0x2'),
                          ('0x07', '0x10', '0x4'),
                          ('0x07', '0x10', '0x6'),
                          ('0x07', '0x11', '0x0'),
                          ('0x07', '0x11', '0x2'),
                          ('0x07', '0x11', '0x4'),
                          ('0x07', '0x11', '0x6')],
    },

    'cougar-kvm03-DevVM06':
    {   'name'         : 'cougar-kvm03-DevVM06',
        'IP'           : '10.159.16.223',
        'img_file'     : '/home/localVMs/cougar-kvm03-DevVM06',
        'xml_file'     : '/etc/libvirt/qemu/cougar-kvm03-DevVM06.xml',
        'hostname'     : 'cougar-kvm03',
        'server'       : 'cougar-lnx',
        'location'     : 'svl',
        'user'         : 'dmu',
        'ixgbevf'      : [('0x07', '0x12', '0x0'),
                          ('0x07', '0x12', '0x2'),
                          ('0x07', '0x12', '0x4'),
                          ('0x07', '0x12', '0x6'),
                          ('0x07', '0x13', '0x0'),
                          ('0x07', '0x13', '0x2'),
                          ('0x07', '0x13', '0x4'),
                          ('0x07', '0x13', '0x6')],
    },

    'srxdevvm01':
    {   'name'         : 'srxdevvm01',
        'IP'           : '10.159.16.231',
        'img_file'     : '/home/localVMs/srxdevvm01',
        'xml_file'     : '/etc/libvirt/qemu/srxdevvm01.xml',
        'hostname'     : 'srxdevvm01',
        'server'       : 'cougar-lnx',
        'location'     : 'svl',
        'user'         : 'dmu',
        'ixgbevf'      : [('0x07', '0x14', '0x0'),
                          ('0x07', '0x14', '0x2'),
                          ('0x07', '0x14', '0x4'),
                          ('0x07', '0x14', '0x6'),
                          ('0x07', '0x15', '0x0'),
                          ('0x07', '0x15', '0x2'),
                          ('0x07', '0x15', '0x4'),
                          ('0x07', '0x15', '0x6')],
    },

    'srxdevvm02':
    {   'name'         : 'srxdevvm02',
        'IP'           : '10.159.16.232',
        'img_file'     : '/home/localVMs/srxdevvm02',
        'xml_file'     : '/etc/libvirt/qemu/srxdevvm02.xml',
        'hostname'     : 'srxdevvm02',
        'server'       : 'cougar-lnx',
        'location'     : 'svl',
        'user'         : 'dmu',
        'ixgbevf'      : [('0x07', '0x16', '0x0'),
                          ('0x07', '0x16', '0x2'),
                          ('0x07', '0x16', '0x4'),
                          ('0x07', '0x16', '0x6'),
                          ('0x07', '0x17', '0x0'),
                          ('0x07', '0x17', '0x2'),
                          ('0x07', '0x17', '0x4'),
                          ('0x07', '0x17', '0x6')],
    },

    # For QA
    'ngsrxqa01'  : {'pci-ixgbe' : ('03:10.0', '03:1f.5')},

    'ngsrxqa01-DevVM01':
    {   'name'         : 'ngsrxqa01-DevVM01',
        'IP'           : '10.157.79.200',
        'img_file'     : '/home/localVMs/ngsrxqa01-DevVM01',
        'xml_file'     : '/etc/libvirt/qemu/ngsrxqa01-DevVM01.xml',
        'hostname'     : 'ngsrxqa01vm01',
        'server'       : 'ngsrxqa01',
        'location'     : 'svl',
        'user'         : 'dmu',
        'ixgbevf'      : [('0x03', '0x10', '0x0'),
                          ('0x03', '0x10', '0x2'),
                          ('0x03', '0x10', '0x4'),
                          ('0x03', '0x10', '0x6'),
                          ('0x03', '0x11', '0x0'),
                          ('0x03', '0x11', '0x2'),
                          ('0x03', '0x11', '0x4'),
                          ('0x03', '0x11', '0x6')],
    },

    'ngsrxqa01-DevVM02':
    {   'name'         : 'ngsrxqa01-DevVM02',
        'IP'           : '10.157.79.201',
        'img_file'     : '/home/localVMs/ngsrxqa01-DevVM02',
        'xml_file'     : '/etc/libvirt/qemu/ngsrxqa01-DevVM02.xml',
        'hostname'     : 'ngsrxqa01vm02',
        'server'       : 'ngsrxqa01',
        'location'     : 'svl',
        'user'         : 'dmu',
        'ixgbevf'      : [('0x03', '0x12', '0x0'),
                          ('0x03', '0x12', '0x2'),
                          ('0x03', '0x12', '0x4'),
                          ('0x03', '0x12', '0x6'),
                          ('0x03', '0x13', '0x0'),
                          ('0x03', '0x13', '0x2'),
                          ('0x03', '0x13', '0x4'),
                          ('0x03', '0x13', '0x6')],
    },

    'ngsrxqa01-DevVM03':
    {   'name'         : 'ngsrxqa01-DevVM03',
        'IP'           : '10.157.79.202',
        'img_file'     : '/home/localVMs/ngsrxqa01-DevVM03',
        'xml_file'     : '/etc/libvirt/qemu/ngsrxqa01-DevVM03.xml',
        'hostname'     : 'ngsrxqa01vm03',
        'server'       : 'ngsrxqa01',
        'location'     : 'svl',
        'user'         : 'dmu',
        'ixgbevf'      : [('0x03', '0x14', '0x0'),
                          ('0x03', '0x14', '0x2'),
                          ('0x03', '0x14', '0x4'),
                          ('0x03', '0x14', '0x6'),
                          ('0x03', '0x15', '0x0'),
                          ('0x03', '0x15', '0x2'),
                          ('0x03', '0x15', '0x4'),
                          ('0x03', '0x15', '0x6')],
    },

    'ngsrxqa01-DevVM04':
    {   'name'         : 'ngsrxqa01-DevVM04',
        'IP'           : '10.157.79.203',
        'img_file'     : '/home/localVMs/ngsrxqa01-DevVM04',
        'xml_file'     : '/etc/libvirt/qemu/ngsrxqa01-DevVM04.xml',
        'hostname'     : 'ngsrxqa01vm04',
        'server'       : 'ngsrxqa01',
        'location'     : 'svl',
        'user'         : 'dmu',
        'ixgbevf'      : [('0x03', '0x16', '0x0'),
                          ('0x03', '0x16', '0x2'),
                          ('0x03', '0x16', '0x4'),
                          ('0x03', '0x16', '0x6'),
                          ('0x03', '0x17', '0x0'),
                          ('0x03', '0x17', '0x2'),
                          ('0x03', '0x17', '0x4'),
                          ('0x03', '0x17', '0x6')],
    },

    'ngsrxqa01-DevVM05':
    {   'name'         : 'ngsrxqa01-DevVM05',
        'IP'           : '10.157.79.204',
        'img_file'     : '/home/localVMs/ngsrxqa01-DevVM05',
        'xml_file'     : '/etc/libvirt/qemu/ngsrxqa01-DevVM05.xml',
        'hostname'     : 'ngsrxqa01vm05',
        'server'       : 'ngsrxqa01',
        'location'     : 'svl',
        'user'         : 'dmu',
        'ixgbevf'      : [('0x03', '0x18', '0x0'),
                          ('0x03', '0x18', '0x2'),
                          ('0x03', '0x18', '0x4'),
                          ('0x03', '0x18', '0x6'),
                          ('0x03', '0x19', '0x0'),
                          ('0x03', '0x19', '0x2'),
                          ('0x03', '0x19', '0x4'),
                          ('0x03', '0x19', '0x6')],
    },


#end
}


## test
if __name__ == '__main__':
    import rlcompleter, readline
    readline.parse_and_bind('tab: complete')
